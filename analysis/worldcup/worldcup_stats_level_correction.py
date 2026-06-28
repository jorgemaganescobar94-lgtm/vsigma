"""
WORLD CUP 2026 — CORRECCIÓN DE NIVEL auto-aprendida y REVERSIBLE para las stats MOSTRADAS
(córners + tiros). ISOLATED, analysis/worldcup/. NO market/odds, NO betting endpoints, NO API.

QUÉ HACE: el marcador worldcup_team_stats_scorer mide un SESGO sistemático del modelo de stats
(subestima córners/tiros: media real > media predicha). Esta capa estima ese sesgo desde los
partidos LIQUIDADOS del Mundial y aplica una corrección ADITIVA por equipo al VALOR MOSTRADO de
los fixtures futuros (post-hoc, solo display) para reducirlo. Se RE-ESTIMA sola cada día al
acumular partidos = auto-aprendizaje.

QUÉ NO TOCA: 1X2 / goles / props NO se tocan. TARJETAS EXCLUIDAS (ruido / ocultas en la ficha).
NO toca el modelo ni la predicción logueada: el log del learning loop sigue guardando el st_* CRUDO
(la corrección se aplica solo al df en memoria de la ficha al renderizar). Es READ-ONLY sobre el
modelo: corrección post-hoc del valor mostrado.

ANTI-LEAKAGE / ANTI-HINDSIGHT: la corrección se estima de partidos YA LIQUIDADOS (terminados, por
tanto estrictamente anteriores) y se aplica a fixtures FUTUROS (no empezados). Nunca usa el propio
partido que se predice. El marcador mide siempre el st_* CRUDO del log; el "sesgo corregido" que
reporta es la simulación (crudo + corrección actual), para verificar que baja.

ENCOGIDO POR MUESTRA (anti-overfit): correccion_total = sesgo_medido × N/(N+K), K≈25 (parcial con
poca muestra, crece hacia el sesgo completo al acumular). Cap razonable por stat. El total se reparte
a por-equipo proporcional al valor predicho de cada equipo (coherente: quien genera más, más sube).

FLAG: STATS_LEVEL_CORRECTION. True -> aplica. False -> reversa EXACTA (Δ=0), valores actuales.

SALIDA (read-only, git-add explícito): worldcup_stats_level_correction.csv (estado/auditoría:
stat, n, raw_bias, target, shrink, correction_total, k, cap, capped).

Run:  python analysis/worldcup/worldcup_stats_level_correction.py   (re-estima y guarda el estado)
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
# Reuse the existing marker for the raw bias (single source of truth; read-only, no side effects).
import worldcup_team_stats_scorer as ts  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ----- governance flag: True -> correction applied; False -> exact revert (Δ=0) -----
STATS_LEVEL_CORRECTION = True

K_SHRINK = 25.0                       # partial-pooling constant: corr = bias × N/(N+K)
STATS = ("corners", "shots")          # ONLY shown stats; cards EXCLUDED (noise/hidden)
CAP_TOTAL = {"corners": 4.0, "shots": 8.0}   # cap on the additive TOTAL correction (sanity bound)
STATE_CSV = HERE / "worldcup_stats_level_correction.csv"
STATE_COLUMNS = ["stat", "n", "raw_bias", "target", "shrink", "correction_total", "k", "cap", "capped"]

# (stat, per-team predicted col home, away, total col) for applying the display correction
APPLY_COLS = {
    "corners": ("st_corners_home", "st_corners_away", "st_corners_total"),
    "shots": ("st_shots_home", "st_shots_away", "st_shots_total"),
}


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clip(v, lo, hi):
    return max(lo, min(hi, v))


# ----------------------------------------------------------------- estimate
def estimate(log_path=ts.LOG):
    """Estimate the shrunk additive TOTAL correction per shown stat from settled matches. Pure read
    (reuses the team-stats marker). Returns {stat: {n, raw_bias, target, shrink, correction_total,
    cap, capped}}. raw_bias = mean(pred-real); target = -raw_bias (what to ADD to reduce the bias)."""
    res = ts.compute_from_log(log_path)
    out = {}
    for r in res["rows"]:
        stat = r["stat"]
        if stat not in STATS:          # exclude cards (and anything not shown)
            continue
        n = int(r["n"])
        raw_bias = float(r["bias"])    # mean(pred - real); negative => under-estimate
        target = -raw_bias             # additive direction that reduces the bias
        shrink = n / (n + K_SHRINK) if (n + K_SHRINK) > 0 else 0.0
        raw_corr = target * shrink
        cap = CAP_TOTAL.get(stat, 4.0)
        corr = _clip(raw_corr, -cap, cap)
        out[stat] = {
            "n": n, "raw_bias": raw_bias, "target": target, "shrink": shrink,
            "correction_total": corr, "cap": cap, "capped": abs(raw_corr) > cap + 1e-9,
        }
    return out


def estimate_and_save(log_path=ts.LOG, state_path=STATE_CSV):
    est = estimate(log_path)
    rows = [{
        "stat": s, "n": d["n"], "raw_bias": round(d["raw_bias"], 4), "target": round(d["target"], 4),
        "shrink": round(d["shrink"], 4), "correction_total": round(d["correction_total"], 4),
        "k": K_SHRINK, "cap": d["cap"], "capped": d["capped"],
    } for s, d in est.items()]
    pd.DataFrame(rows, columns=STATE_COLUMNS).to_csv(state_path, index=False)
    return est


def load_corrections(state_path=STATE_CSV):
    """{stat: correction_total} from the saved state. Respects the flag: returns {} when the flag is
    OFF (exact revert) or the state is absent/unreadable (soft-fail -> no correction)."""
    if not STATS_LEVEL_CORRECTION:
        return {}
    p = Path(state_path)
    if not p.exists():
        return {}
    try:
        df = pd.read_csv(p)
    except Exception:
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            if str(r["stat"]) in STATS:
                out[str(r["stat"])] = float(r["correction_total"])
        except Exception:
            continue
    return out


# ----------------------------------------------------------------- apply (display only)
def corrected_per_team(home, away, corr_total):
    """Split the additive TOTAL correction across the two teams proportional to each predicted value
    (coherent: more predicted -> more correction), clamped to be non-negative. Returns (h, a)."""
    if pd.isna(home) or pd.isna(away):
        return home, away
    h, a = float(home), float(away)
    denom = h + a
    if denom <= 0:
        sh = sa = 0.5
    else:
        sh, sa = h / denom, a / denom
    return max(0.0, h + corr_total * sh), max(0.0, a + corr_total * sa)


def apply_to_df(df, state_path=STATE_CSV):
    """Apply the level correction to the DISPLAYED stat columns of a cards DataFrame, IN MEMORY only
    (the on-disk cards.csv / the learning-loop log stay RAW). No-op (Δ=0) when the flag is OFF or
    there is no correction. Returns the number of (stat) corrections applied. Cards never touched."""
    corr = load_corrections(state_path)
    if not corr:
        return 0
    applied = 0
    for stat, (hc, ac, tc) in APPLY_COLS.items():
        c = corr.get(stat)
        if c is None or abs(c) < 1e-12:
            continue
        if hc not in df.columns or ac not in df.columns:
            continue
        new_h, new_a = [], []
        for h, a in zip(df[hc], df[ac]):
            nh, na = corrected_per_team(h, a, c)
            new_h.append(nh)
            new_a.append(na)
        df[hc] = new_h
        df[ac] = new_a
        if tc in df.columns:
            # total stays consistent = corrected home + away (preserves the +corr_total level shift)
            df[tc] = [
                (nh + na) if (not pd.isna(nh) and not pd.isna(na)) else t
                for nh, na, t in zip(new_h, new_a, df[tc])
            ]
        applied += 1
    return applied


def main(log_path=ts.LOG, state_path=STATE_CSV):
    est = estimate_and_save(log_path, state_path)
    on = "ON" if STATS_LEVEL_CORRECTION else "OFF (revert, Δ=0)"
    print(f"stats-level correction [{on}] -> {state_path}")
    for s, d in est.items():
        print(f"  {s:8} N={d['n']:>3} raw_bias={d['raw_bias']:+.3f} "
              f"shrink={d['shrink']:.3f} correction_total={d['correction_total']:+.3f}"
              + ("  (CAP)" if d["capped"] else ""))
    if not est:
        print("  (sin partidos liquidados con stats -> sin corrección)")
    return est


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup stats-level correction (shown córners/tiros).")
    ap.add_argument("--log", default=str(ts.LOG))
    ap.add_argument("--state", default=str(STATE_CSV))
    a = ap.parse_args()
    main(a.log, a.state)
