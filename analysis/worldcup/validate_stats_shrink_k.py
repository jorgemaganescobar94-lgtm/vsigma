"""
WORLD CUP 2026 — validación del K del shrink de la corrección de nivel (córners/tiros). OFFLINE, 0 API,
read-only sobre el modelo. Elige K por DATOS liquidados, no a ojo.

La corrección de nivel es aditiva: corr = -raw_bias × N/(N+K) (partial pooling). Bajar K corrige MÁS.
IN-SAMPLE el residual = raw_bias × K/(N+K) es monótono en K y NUNCA sobrepasa (μ_corr<μ_real siempre para
K>0), así que in-sample no informa del riesgo de overshoot. El juez honesto es WALK-FORWARD (anti-look-
ahead): en orden de saque, la corrección de cada partido se estima SOLO con los partidos previos y se
aplica al siguiente; el residual se mide out-of-sample. Ahí un K demasiado bajo SÍ puede sobrepasar
(μ_corr>μ_real) si el sesgo temprano es más grande que el estable.

CRITERIO: elegir el K que MINIMIZA |residual walk-forward| SIN overshoot (media del residual corregido
≤ 0, es decir μ_corr no sobrepasa μ_real). Tarjetas EXCLUIDAS. NO escribe estado ni toca el modelo.

Run: python analysis/worldcup/validate_stats_shrink_k.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_team_stats_scorer as ts  # noqa: E402
import worldcup_stats_level_correction as lc  # noqa: E402

STATS = [("corners", "córners", "st_corners_total", "result_corners"),
         ("shots", "tiros", "st_shots_total", "result_shots")]
K_GRID = [5.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0]
MIN_PRIOR = 5   # walk-forward: no correction until this many prior settled matches (avoid degenerate)
# Regularization floor: below this K the shrink exceeds ~0.85 and the partial-pooling regularizer is
# effectively abandoned (near-full trust in the current, group-stage-dominated bias). We do NOT pick
# below it even if the residual keeps shrinking, to stay robust to a knockout regime shift (fewer
# corners/shots) the current sample cannot yet see. Documented, reversible.
K_FLOOR = 10.0


def _series(log_path=ts.LOG):
    """Per-stat arrays of (pred_total, real_total) for SETTLED matches, ORDERED by kickoff. Point-in-
    time honest: uses the frozen st_* pred and the liquidated real, same as the scorer."""
    df = pd.read_csv(log_path)
    s = ts._settled(df).copy()
    if "kickoff_utc" in s.columns:
        s = s.sort_values("kickoff_utc")
    out = {}
    for key, _lab, pcol, rcol in STATS:
        if pcol not in s.columns or rcol not in s.columns:
            continue
        sub = s.dropna(subset=[pcol, rcol])
        out[key] = (sub[pcol].to_numpy(float), sub[rcol].to_numpy(float))
    return out


def _corr_for(pred_prior, real_prior, k, cap):
    """The additive TOTAL correction the module WOULD compute from the prior matches with shrink K.
    Mirrors worldcup_stats_level_correction.estimate() exactly (shrink + cap)."""
    n = len(pred_prior)
    if n == 0:
        return 0.0
    raw_bias = float(np.mean(pred_prior - real_prior))
    target = -raw_bias
    shrink = n / (n + k)
    return lc._clip(target * shrink, -cap, cap)


def walk_forward_residual(pred, real, k, cap):
    """Mean out-of-sample residual (corrected_pred − real) applying, at each match, the correction
    estimated from the PRIOR settled matches only. Matches with <MIN_PRIOR priors are left uncorrected.
    Returns (mean_residual, n_eval). mean_residual>0 => overshoot on average."""
    res = []
    for i in range(len(pred)):
        corr = _corr_for(pred[:i], real[:i], k, cap) if i >= MIN_PRIOR else 0.0
        res.append((pred[i] + corr) - real[i])
    return float(np.mean(res)), len(res)


def insample_residual(pred, real, k, cap):
    """Residual with the correction estimated on the FULL sample (what the live state does today)."""
    n = len(pred)
    raw_bias = float(np.mean(pred - real))
    corr = lc._clip(-raw_bias * n / (n + k), -cap, cap)
    return raw_bias + corr


def run(log_path=ts.LOG):
    series = _series(log_path)
    lines = []

    def out(s=""):
        print(s); lines.append(s)

    out("=" * 92)
    out("VALIDACIÓN K del shrink (córners/tiros) — walk-forward anti-look-ahead · read-only · 0 API")
    out("=" * 92)
    chosen = {}
    for key, lab, _pc, _rc in STATS:
        if key not in series:
            continue
        pred, real = series[key]
        n = len(pred)
        cap = lc.CAP_TOTAL.get(key, 4.0)
        raw_bias = float(np.mean(pred - real))
        mu_pred, mu_real = float(np.mean(pred)), float(np.mean(real))
        out("")
        out(f"[{lab}]  N={n}  μ_pred={mu_pred:.2f}  μ_real={mu_real:.2f}  sesgo_crudo={raw_bias:+.2f}  cap={cap}")
        out(f"  {'K':>4} {'shrink':>7} {'resid_insample':>15} {'resid_walkfwd':>14} {'overshoot?':>11}")
        rows = []
        for k in K_GRID:
            shrink = n / (n + k)
            r_in = insample_residual(pred, real, k, cap)
            r_wf, _ne = walk_forward_residual(pred, real, k, cap)
            overshoot = r_wf > 1e-9
            rows.append((k, shrink, r_in, r_wf, overshoot))
            mark = "  <-- actual" if abs(k - lc.K_SHRINK) < 1e-9 else ""
            out(f"  {k:>4.0f} {shrink:>7.3f} {r_in:>+15.3f} {r_wf:>+14.3f} {str(overshoot):>11}{mark}")
        # choose: min |resid_walkfwd| among K WITHOUT overshoot (μ_corr ≤ μ_real out-of-sample) AND at
        # or above the regularization floor (K>=K_FLOOR). The floor stops the naive argmin from diving
        # to K→0 (overfitting the current sample). Residual is monotone in K, so this picks K=K_FLOOR
        # whenever the floor is itself overshoot-free.
        safe = [row for row in rows if not row[4] and row[0] >= K_FLOOR - 1e-9]
        pool = safe if safe else [row for row in rows if not row[4]] or rows
        best = min(pool, key=lambda row: abs(row[3]))
        chosen[key] = best[0]
        out(f"  -> elegido K={best[0]:.0f} (|resid_walkfwd|={abs(best[3]):.3f} mínimo sin overshoot, "
            f"K>=suelo {K_FLOOR:.0f})")
    out("")
    # single K for the module constant: the MAX of the per-stat choices (más conservador -> no overshoot
    # en ninguna de las dos; una sola constante gobierna ambas en el módulo actual).
    if chosen:
        k_final = max(chosen.values())
        out(f"RECOMENDACIÓN (una sola constante K_SHRINK para ambas): K={k_final:.0f}  "
            f"(máx de {chosen} -> no overshoot en ninguna)")
    return chosen, lines


if __name__ == "__main__":
    run()
