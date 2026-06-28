"""
WORLD CUP 2026 — MARCADOR ACUMULADO "Motor máximo (mx) vs L3" (read-only · NO model touch · NO API).

ÁRBITRO EN VIVO del A/B invertido: el motor máximo (mx_*) corre EN VIVO y el L3 queda como sombra.
Este marcador NO recalcula ninguna predicción ni toca el modelo: solo LEE el log del learning loop
(worldcup_predictions_log.csv), que ya guarda l3_* y mx_* CONGELADOS al saque (lock-at-KO) y result_*
tras liquidar, y mide el cara a cara ACUMULADO sobre los partidos liquidados en los que EXISTE
predicción mx (es decir, desde que el motor máximo entró en vivo).

ANTI-LEAKAGE / ANTI-HINDSIGHT: solo entran filas settled==1 con result_1x2 en {H,D,A} Y mx_home/draw/
away no nulos. mx_* nunca se rellena retroactivamente (lo escribe el learning loop solo pre-KO y lo
congela al saque), así que esta capa nunca puntúa un partido que mx no predijo antes del saque.

MÉTRICAS (mx vs L3, ambos sobre el MISMO conjunto liquidado):
  * 1X2:   acierto/N (%), log-loss, Brier.
  * Over 2.5 y BTTS: derivados del xG vía Poisson (mismas fórmulas que el scorecard), acc/logloss/Brier.
  * Para cada métrica: quién va por delante (líder) y la diferencia.
  * N y fecha de inicio (cuándo entró mx en vivo = primer saque liquidado con mx).

HONESTIDAD: NO declara ganador hasta N razonable (umbral SMALL_N); muestra el acumulado y lo deja
crecer hasta el final del Mundial. Si el mx queda por detrás al final, este marcador + el A/B son la
base para decidir revertir (MAXMODEL_LIVE=False). NO toca predicciones ni modelo. NO mercado/cuotas.

SALIDA (solo lectura, git-add explícito):
  * worldcup_mx_vs_l3_scorecard.txt  (línea 1 = bloque compacto para Telegram; luego el detalle)
  * worldcup_mx_vs_l3_scorecard.csv  (una fila por métrica: market,metric,l3,mx,leader,diff,n,since)

Run:  python analysis/worldcup/worldcup_mx_vs_l3_scorer.py
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
# Single source of truth for the Poisson Over2.5 / BTTS derivation and the metric helpers — reused,
# never re-implemented. Importing has NO side effects (the learning loop guards its CLI under __main__).
import worldcup_learning_loop as ll  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LOG = HERE / "worldcup_predictions_log.csv"
SCORECARD_TXT = HERE / "worldcup_mx_vs_l3_scorecard.txt"
SCORECARD_CSV = HERE / "worldcup_mx_vs_l3_scorecard.csv"

SMALL_N = 30          # below this we DO NOT declare a winner — accumulate, "orientativo"
TIE_LL = 5e-4         # log-loss/Brier closer than this -> empate
TIE_ACC = 1e-3        # accuracy closer than this -> empate
RES_IDX = {"H": 0, "D": 1, "A": 2}
CSV_COLUMNS = ["market", "metric", "l3", "mx", "leader", "diff", "n", "since"]

# Spanish 3-letter month abbreviations for the "desde DD-mmm" tag (display only).
_ES_MONTH = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _since_tag(kickoff_series):
    """'DD-mmm' (es) of the EARLIEST kickoff in the mx-present settled set, or '?' if unparseable."""
    best = None
    for s in kickoff_series:
        ko = ll._parse_ko(s)
        if ko is not None and (best is None or ko < best):
            best = ko
    if best is None:
        return "?", None
    return f"{best.day:02d}-{_ES_MONTH[best.month - 1]}", best


def _leader(l3, mx, *, lower_better, tie):
    """Who leads on a metric + the absolute gap. 'empate' inside the tie band."""
    if l3 is None or mx is None or np.isnan(l3) or np.isnan(mx):
        return "n/d", float("nan")
    diff = abs(l3 - mx)
    if diff <= tie:
        return "empate", diff
    if lower_better:
        return ("mx" if mx < l3 else "L3"), diff
    return ("mx" if mx > l3 else "L3"), diff


def _1x2_metrics(df, prefix):
    """acc/logloss/brier for a 1X2 predictor prefix over rows where all three probs exist."""
    cols = [f"{prefix}_home", f"{prefix}_draw", f"{prefix}_away"]
    if not all(c in df.columns for c in cols):
        return None
    P = df[cols].to_numpy(float)
    y = df["result_1x2"].map(RES_IDX).to_numpy(int)
    mask = ~np.isnan(P).any(axis=1)
    if mask.sum() == 0:
        return None
    Y = np.eye(3)[y[mask]]
    m = ll._metrics(P[mask], Y)              # {logloss, brier, acc, ece}
    return {"acc": m["acc"], "logloss": m["logloss"], "brier": m["brier"], "n": int(mask.sum())}


def _binary_from_xg(df, prefix, kind):
    """Poisson Over2.5/BTTS prob per row from a model's xG columns (NaN where xG missing)."""
    xh = df[f"{prefix}_xg_home"].to_numpy(float)
    xa = df[f"{prefix}_xg_away"].to_numpy(float)
    fn = ll._pois_over25 if kind == "over25" else ll._pois_btts
    ok = ~(np.isnan(xh) | np.isnan(xa))
    p = np.full(len(df), np.nan)
    for i in range(len(df)):
        if ok[i]:
            p[i] = fn(xh[i], xa[i])
    return p


def _binary_metrics_pair(df, kind):
    """acc/logloss/brier for L3 vs mx on a derived binary market, over the COMMON mask (both xG)."""
    if kind == "over25":
        real = (df["result_ft_gh"].to_numpy(float) + df["result_ft_ga"].to_numpy(float) >= 3).astype(int)
    else:  # btts
        gh = df["result_ft_gh"].to_numpy(float)
        ga = df["result_ft_ga"].to_numpy(float)
        real = ((gh >= 1) & (ga >= 1)).astype(int)
    pl3 = _binary_from_xg(df, "l3", kind)
    pmx = _binary_from_xg(df, "mx", kind)
    common = ~(np.isnan(pl3) | np.isnan(pmx))
    if common.sum() == 0:
        return None, None, 0
    yv = real[common].astype(float)
    a3, b3, l3ll = ll._binary_metrics(pl3[common], yv)
    am, bm, mll = ll._binary_metrics(pmx[common], yv)
    L3 = {"acc": a3, "logloss": l3ll, "brier": b3}
    MX = {"acc": am, "logloss": mll, "brier": bm}
    return L3, MX, int(common.sum())


# ----------------------------------------------------------------- core
def compute_from_log(log_path=LOG):
    """Read the log and return the accumulated mx-vs-L3 head-to-head. Pure read; NO recompute of any
    prediction beyond the deterministic Poisson Over2.5/BTTS already used by the scorecard. Returns a
    dict with n, since, since_dt, and per-(market,metric) rows {l3, mx, leader, diff}."""
    p = Path(log_path)
    if not p.exists():
        return {"n": 0, "since": "?", "since_dt": None, "rows": []}
    try:
        df = pd.read_csv(p)
    except Exception:
        return {"n": 0, "since": "?", "since_dt": None, "rows": []}

    need = {"settled", "result_1x2", "mx_home", "mx_draw", "mx_away"}
    if df.empty or not need <= set(df.columns):
        return {"n": 0, "since": "?", "since_dt": None, "rows": []}

    # ANTI-HINDSIGHT FILTER: settled + real 1X2 + mx prediction present (mx never backfilled).
    s = df[df["settled"].fillna(0).astype(int) == 1].copy()
    s = s[s["result_1x2"].isin(["H", "D", "A"])]
    mx_present = ~(s["mx_home"].isna() | s["mx_draw"].isna() | s["mx_away"].isna())
    s = s[mx_present].copy()
    n = len(s)
    if n == 0:
        return {"n": 0, "since": "?", "since_dt": None, "rows": []}

    since, since_dt = _since_tag(s["kickoff_utc"]) if "kickoff_utc" in s.columns else ("?", None)

    rows = []

    def add(market, metric, l3v, mxv, lower_better):
        leader, diff = _leader(l3v, mxv, lower_better=lower_better,
                               tie=(TIE_ACC if metric == "acc" else TIE_LL))
        rows.append({"market": market, "metric": metric, "l3": l3v, "mx": mxv,
                     "leader": leader, "diff": diff})

    # 1X2
    mL3 = _1x2_metrics(s, "l3")
    mMX = _1x2_metrics(s, "mx")
    if mL3 and mMX:
        add("1X2", "acc", mL3["acc"] * 100, mMX["acc"] * 100, lower_better=False)
        add("1X2", "logloss", mL3["logloss"], mMX["logloss"], lower_better=True)
        add("1X2", "brier", mL3["brier"], mMX["brier"], lower_better=True)

    # Over 2.5 + BTTS (Poisson from xG)
    for market, kind in (("Over 2.5", "over25"), ("BTTS", "btts")):
        L3b, MXb, _nb = _binary_metrics_pair(s, kind)
        if L3b and MXb:
            add(market, "acc", L3b["acc"] * 100, MXb["acc"] * 100, lower_better=False)
            add(market, "logloss", L3b["logloss"], MXb["logloss"], lower_better=True)
            add(market, "brier", L3b["brier"], MXb["brier"], lower_better=True)

    return {"n": n, "since": since, "since_dt": since_dt, "rows": rows}


def _fmt(metric, v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "n/d"
    return f"{v:.1f}" if metric == "acc" else f"{v:.4f}"


def _get(res, market, metric):
    for r in res["rows"]:
        if r["market"] == market and r["metric"] == metric:
            return r
    return None


def briefing_line(res):
    """Compact one-liner for the Telegram briefing header. '' when there is nothing settled yet."""
    if res["n"] == 0:
        return ""
    bits = []
    a1 = _get(res, "1X2", "acc")
    if a1:
        bits.append(f"1X2 {a1['mx']:.0f}% vs {a1['l3']:.0f}%")
    ao = _get(res, "Over 2.5", "acc")
    if ao:
        bits.append(f"O2.5 {ao['mx']:.0f}% vs {ao['l3']:.0f}%")
    ab = _get(res, "BTTS", "acc")
    if ab:
        bits.append(f"BTTS {ab['mx']:.0f}% vs {ab['l3']:.0f}%")
    tail = "  (muestra pequeña, orientativo)" if res["n"] < SMALL_N else ""
    return f"⚙️ Motor máximo vs L3 (N={res['n']} · desde {res['since']}): " + " · ".join(bits) + tail


def render_txt(res):
    L = []
    L.append(briefing_line(res) or
             f"⚙️ Motor máximo vs L3: aún sin partidos liquidados con predicción mx ({now_iso()[:10]}).")
    L.append("")
    L.append("===== detalle mx vs L3 =====")
    if res["n"] == 0:
        L.append("0 partidos liquidados con predicción mx todavía; el marcador se llena cuando el motor "
                 "máximo (en vivo) tenga su primer partido liquidado. NO se declara ganador.")
        L.append("")
        L.append(f"generated_at_utc: {now_iso()}")
        return "\n".join(L)

    L.append(f"N={res['n']} partidos liquidados con predicción mx (lock-at-KO, anti-hindsight) · "
             f"desde {res['since']} · cara a cara vs RESULTADOS REALES, sin mercado")
    hdr = f"  {'mercado/métrica':22} {'L3':>9} {'mx':>9} {'líder':>8} {'Δ':>9}"
    L.append(hdr)
    L.append("  " + "-" * (len(hdr) - 2))
    labels = {"acc": "acc%", "logloss": "logloss", "brier": "brier"}
    for market in ("1X2", "Over 2.5", "BTTS"):
        for metric in ("acc", "logloss", "brier"):
            r = _get(res, market, metric)
            if not r:
                continue
            name = f"{market} {labels[metric]}"
            dtxt = "-" if r["leader"] in ("empate", "n/d") else _fmt(metric, r["diff"])
            L.append(f"  {name:22} {_fmt(metric, r['l3']):>9} {_fmt(metric, r['mx']):>9} "
                     f"{r['leader']:>8} {dtxt:>9}")
    L.append("")
    # honest verdict — NEVER a winner below SMALL_N
    if res["n"] < SMALL_N:
        L.append(f"VEREDICTO: muestra pequeña (N={res['n']} < {SMALL_N}) — NO se declara ganador; "
                 "el acumulado crece hasta el final del Mundial. Orientativo.")
    else:
        ll_row = _get(res, "1X2", "logloss")
        who = ll_row["leader"] if ll_row else "n/d"
        if who in ("mx", "L3"):
            L.append(f"VEREDICTO: con N={res['n']}, lidera {who} en log-loss 1X2 (Δ{ll_row['diff']:.4f}). "
                     "Sigue acumulando; este marcador + el A/B son la base para revertir (MAXMODEL_LIVE).")
        else:
            L.append(f"VEREDICTO: con N={res['n']}, mx y L3 empatados en log-loss 1X2. Sigue acumulando.")
    L.append("")
    L.append(f"generated_at_utc: {now_iso()}")
    return "\n".join(L)


def write_csv(res, path=SCORECARD_CSV):
    rows = []
    for r in res["rows"]:
        rows.append({
            "market": r["market"], "metric": r["metric"],
            "l3": (round(r["l3"], 1) if r["metric"] == "acc" else round(r["l3"], 4)),
            "mx": (round(r["mx"], 1) if r["metric"] == "acc" else round(r["mx"], 4)),
            "leader": r["leader"],
            "diff": ("" if r["leader"] in ("empate", "n/d")
                     else (round(r["diff"], 1) if r["metric"] == "acc" else round(r["diff"], 4))),
            "n": res["n"], "since": res["since"],
        })
    df = pd.DataFrame(rows, columns=CSV_COLUMNS)
    df.to_csv(path, index=False)
    return df


def main(log_path=LOG, txt_path=SCORECARD_TXT, csv_path=SCORECARD_CSV):
    res = compute_from_log(log_path)
    Path(txt_path).write_text(render_txt(res), encoding="utf-8")
    write_csv(res, csv_path)
    print(f"mx-vs-L3 scorer: N={res['n']} (desde {res['since']}) -> {txt_path} + {csv_path}")
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup mx-vs-L3 accumulated marker (read-only, shadow).")
    ap.add_argument("--log", default=str(LOG))
    ap.add_argument("--txt", default=str(SCORECARD_TXT))
    ap.add_argument("--csv", default=str(SCORECARD_CSV))
    a = ap.parse_args()
    main(a.log, a.txt, a.csv)
