"""
WORLD CUP 2026 — MARCADOR ACUMULADO de STATS POR EQUIPO (córners / tiros / tarjetas), predicho vs real.
READ-ONLY · NO model touch · NO API · NO market/odds · NO betting endpoints.

Mide el modelo de stats (córners/tiros/tarjetas) contra el resultado real, acumulado durante el torneo.
SOLO LEE el log del learning loop (worldcup_predictions_log.csv), que ya guarda la predicción del modelo
de stats CONGELADA al saque (st_corners_total / st_shots_total / st_cards_total — esta última oculta en
la ficha, pero logueada) y el VALOR REAL extraído al liquidar (result_corners/cards/shots, los MISMOS
totales que alimentan las líneas [REAL] del briefing, vía /fixtures/statistics).

UNIDAD: total por partido (suma de ambos equipos) — es el dato frozen+disponible en el log; el modelo
de stats es per-equipo pero el log solo persiste los totales y el real liquidado también es total.

ANTI-HINDSIGHT / ANTI-LEAKAGE: la predicción st_* la escribe el learning loop SOLO pre-KO y la congela
al saque; el real result_* se rellena al liquidar. Este marcador nunca recalcula la predicción con el
resultado: solo compara lo ya logueado.

POR STAT acumula:
  * error:        MAE y RMSE (predicho vs real).
  * sesgo:        media(predicho − real) + media predicha vs media real (¿infra/sobre-estima?).
  * acierto línea O/U: solo córners (st_corners_over/line en el log); real Over = result_corners > línea.
  * N partidos.

HONESTIDAD: córners es BAJA confianza y tarjetas es RUIDO -> es ESPERABLE un error alto; el marcador lo
refleja sin maquillar. Con muestra pequeña (N<SMALL_N) las métricas son orientativas (se marca). NO
declara nada "bueno/malo": solo acumula. NO toca modelo ni predicciones.

SALIDA (solo lectura, git-add explícito):
  * worldcup_team_stats_scorecard.txt  (línea 1 = resumen compacto; luego el detalle)
  * worldcup_team_stats_scorecard.csv  (una fila por stat: stat,n,mae,rmse,bias,mean_pred,mean_real,line_acc)

Run:  python analysis/worldcup/worldcup_team_stats_scorer.py
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Reuse the learning-loop binary metric helper (line O/U accuracy) — single source of truth, no
# re-implementation. Importing has NO side effects (its CLI is guarded under __main__).
import worldcup_learning_loop as ll  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LOG = HERE / "worldcup_predictions_log.csv"
SCORECARD_TXT = HERE / "worldcup_team_stats_scorecard.txt"
SCORECARD_CSV = HERE / "worldcup_team_stats_scorecard.csv"

SMALL_N = 30  # below this the metrics are flagged "muestra pequeña, orientativo"
# bias = sesgo CRUDO del modelo (mean pred-real); bias_corr = sesgo tras la corrección de nivel
# actual (crudo + correccion_total leída de worldcup_stats_level_correction.csv) -> verifica que baja.
CSV_COLUMNS = ["stat", "n", "mae", "rmse", "bias", "bias_corr", "mean_pred", "mean_real", "line_acc"]
# read-only: the level-correction state written by worldcup_stats_level_correction.py (soft).
CORRECTION_CSV = HERE / "worldcup_stats_level_correction.csv"

# stat key -> (display es, predicted total col, real col, low-confidence note)
STATS = [
    ("corners", "córners", "st_corners_total", "result_corners", "baja confianza"),
    ("shots", "tiros", "st_shots_total", "result_shots", "orientativo"),
    ("cards", "tarjetas", "st_cards_total", "result_cards", "ruido (oculto en ficha)"),
]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _settled(df):
    """Settled rows with a real 1X2 (i.e. the match actually finished and was liquidated)."""
    if df.empty or "settled" not in df.columns:
        return df.iloc[0:0]
    s = df[df["settled"].fillna(0).astype(int) == 1].copy()
    if "result_1x2" in s.columns:
        s = s[s["result_1x2"].isin(["H", "D", "A"])]
    return s


def _load_corrections(path=CORRECTION_CSV):
    """{stat: correction_total} from the level-correction state file, or {} (soft). Read-only — the
    scorer never estimates the correction; it just reads what the correction module saved, to report
    the post-correction bias alongside the raw one."""
    p = Path(path)
    if not p.exists():
        return {}
    try:
        df = pd.read_csv(p)
    except Exception:
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            out[str(r["stat"])] = float(r["correction_total"])
        except Exception:
            continue
    return out


def _line_acc(s):
    """Córners O/U: model call (st_corners_over>=0.5) vs reality (result_corners > st_corners_line).
    Returns (acc_pct, n, real_over_pct) or (None, 0, None) if the columns aren't usable."""
    need = {"st_corners_over", "st_corners_line", "result_corners"}
    if not need <= set(s.columns):
        return None, 0, None
    sub = s.dropna(subset=list(need))
    if not len(sub):
        return None, 0, None
    po = sub["st_corners_over"].to_numpy(float)
    line = sub["st_corners_line"].to_numpy(float)
    real_over = (sub["result_corners"].to_numpy(float) > line).astype(int)
    acc, _brier, _ll = ll._binary_metrics(po, real_over)
    return acc * 100.0, int(len(sub)), float(real_over.mean()) * 100.0


def compute_from_log(log_path=LOG):
    """Read the log and return the accumulated team-stats marker. Pure read; NO recompute of any
    prediction. Returns {rows: [...], generated_at}. Each row: stat key/label + MAE/RMSE/bias/means/N
    (+ line O/U for córners)."""
    p = Path(log_path)
    if not p.exists():
        return {"rows": []}
    try:
        df = pd.read_csv(p)
    except Exception:
        return {"rows": []}

    s = _settled(df)
    if not len(s):
        return {"rows": []}

    # resolve CORRECTION_CSV at call time (module global) so it stays patchable / testable
    corrections = _load_corrections(CORRECTION_CSV)   # {stat: correction_total} (empty if absent)
    rows = []
    for key, label, pcol, rcol, note in STATS:
        if pcol not in s.columns or rcol not in s.columns:
            continue
        sub = s.dropna(subset=[pcol, rcol])
        n = len(sub)
        if n == 0:
            continue
        pred = sub[pcol].to_numpy(float)
        real = sub[rcol].to_numpy(float)
        diff = pred - real
        bias = float(np.mean(diff))
        # post-correction bias = raw + correction_total (the level fix ADDS correction_total to the
        # predicted total -> shifts the bias toward 0). None when this stat has no correction (cards).
        corr = corrections.get(key)
        bias_corr = (bias + corr) if corr is not None else None
        row = {
            "stat": key, "label": label, "note": note, "n": n,
            "mae": float(np.mean(np.abs(diff))),
            "rmse": float(np.sqrt(np.mean(diff ** 2))),
            "bias": bias, "bias_corr": bias_corr, "correction": corr,
            "mean_pred": float(np.mean(pred)),
            "mean_real": float(np.mean(real)),
            "line_acc": None, "line_n": 0, "line_real_over": None,
        }
        if key == "corners":
            la, ln, ro = _line_acc(s)
            row["line_acc"], row["line_n"], row["line_real_over"] = la, ln, ro
        rows.append(row)

    return {"rows": rows, "generated_at": now_iso()}


def _bias_es(bias):
    """Honest one-word reading of the signed bias (pred − real)."""
    if abs(bias) < 0.25:
        return "≈ neutral"
    return "infraestima" if bias < 0 else "sobrestima"


def briefing_summary(res):
    """Compact one-liner (txt header). '' when nothing settled yet. NOT pushed to Telegram by default
    (stats are low-conf); kept for the txt and any caller that wants it."""
    if not res["rows"]:
        return ""
    n = max((r["n"] for r in res["rows"]), default=0)
    bits = [f"{r['label']} MAE {r['mae']:.1f} ({_bias_es(r['bias'])})" for r in res["rows"]]
    tail = "  (muestra pequeña, orientativo)" if n < SMALL_N else ""
    return f"📐 Stats modelo vs real (N={n}): " + " · ".join(bits) + tail


def render_txt(res):
    L = []
    L.append(briefing_summary(res) or
             f"📐 Stats por equipo vs real: aún sin partidos liquidados con stats ({now_iso()[:10]}).")
    L.append("")
    L.append("===== detalle stats por equipo (predicho vs real) =====")
    if not res["rows"]:
        L.append("0 partidos liquidados con stats reales todavía; el marcador se llena cuando settle "
                 "trae córners/tiros/tarjetas (/fixtures/statistics) al terminar el partido.")
        L.append("")
        L.append(f"generated_at_utc: {now_iso()}")
        return "\n".join(L)

    L.append("total por partido (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) "
             "vs real liquidado · sin mercado")
    hdr = (f"  {'stat':10} {'N':>3} {'MAE':>6} {'RMSE':>6} {'sesgo_crudo':>11} "
           f"{'sesgo_corr':>10} {'μpred':>6} {'μreal':>6} {'lectura':>13}")
    L.append(hdr)
    L.append("  " + "-" * (len(hdr) - 2))
    for r in res["rows"]:
        bc = "—" if r.get("bias_corr") is None else f"{r['bias_corr']:+.2f}"
        L.append(f"  {r['label']:10} {r['n']:>3} {r['mae']:>6.2f} {r['rmse']:>6.2f} "
                 f"{r['bias']:>+11.2f} {bc:>10} {r['mean_pred']:>6.1f} {r['mean_real']:>6.1f} "
                 f"{_bias_es(r['bias']):>13}")
    # raw vs corrected bias check (córners/tiros): the level correction should shrink |sesgo|
    corr_rows = [r for r in res["rows"] if r.get("bias_corr") is not None]
    if corr_rows:
        L.append("")
        L.append("  corrección de nivel (córners/tiros MOSTRADOS): |sesgo| crudo -> corregido")
        for r in corr_rows:
            better = abs(r["bias_corr"]) < abs(r["bias"]) - 1e-9
            L.append(f"    {r['label']:10} |{abs(r['bias']):.2f}| -> |{abs(r['bias_corr']):.2f}| "
                     f"(corr {r['correction']:+.2f}) {'baja ✓' if better else 'no baja'}")
        L.append("    (tarjetas EXCLUIDAS de la corrección; muestra pequeña -> orientativo, no es victoria)")
    # córners line O/U
    cr = next((r for r in res["rows"] if r["stat"] == "corners"), None)
    if cr and cr["line_acc"] is not None:
        L.append(f"  córners O/U (línea modelo): acc {cr['line_acc']:.0f}% sobre n={cr['line_n']} "
                 f"(real Over={cr['line_real_over']:.0f}%)")
    L.append("")
    L.append("HONESTIDAD: córners = BAJA confianza · tarjetas = RUIDO -> error alto ESPERABLE, no se "
             "maquilla. tiros = orientativo. NO se declara nada 'bueno/malo'; solo se acumula.")
    n = max((r["n"] for r in res["rows"]), default=0)
    if n < SMALL_N:
        L.append(f"  muestra pequeña (N={n} < {SMALL_N}): métricas orientativas, aún no concluyentes.")
    L.append("")
    L.append(f"generated_at_utc: {now_iso()}")
    return "\n".join(L)


def write_csv(res, path=SCORECARD_CSV):
    rows = []
    for r in res["rows"]:
        rows.append({
            "stat": r["stat"], "n": r["n"],
            "mae": round(r["mae"], 2), "rmse": round(r["rmse"], 2), "bias": round(r["bias"], 2),
            "bias_corr": ("" if r.get("bias_corr") is None else round(r["bias_corr"], 2)),
            "mean_pred": round(r["mean_pred"], 1), "mean_real": round(r["mean_real"], 1),
            "line_acc": ("" if r["line_acc"] is None else round(r["line_acc"], 0)),
        })
    df = pd.DataFrame(rows, columns=CSV_COLUMNS)
    df.to_csv(path, index=False)
    return df


def main(log_path=LOG, txt_path=SCORECARD_TXT, csv_path=SCORECARD_CSV):
    res = compute_from_log(log_path)
    Path(txt_path).write_text(render_txt(res), encoding="utf-8")
    write_csv(res, csv_path)
    n = max((r["n"] for r in res["rows"]), default=0)
    print(f"team-stats scorer: {len(res['rows'])} stats, N={n} -> {txt_path} + {csv_path}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup team-stats accumulated marker (read-only, shadow).")
    ap.add_argument("--log", default=str(LOG))
    ap.add_argument("--txt", default=str(SCORECARD_TXT))
    ap.add_argument("--csv", default=str(SCORECARD_CSV))
    a = ap.parse_args()
    main(a.log, a.txt, a.csv)
