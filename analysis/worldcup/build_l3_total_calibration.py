"""
OFFLINE builder of the L3 calibration JSON for the MATCH-DEPENDENT TOTAL (auditoría candidato #1,
forma b). NO API. Surgical: it PRESERVES the current constant calibration EXACTLY (a0, a1,
total_mean and the current isotonic -> iso_const) so TOTAL_MATCHUP_LIVE=False reverts byte-exactly to
today's production, and ADDS the match-dependent total (total_coef) + its own re-fit isotonic (iso).

Reuses the building blocks (no duplication): total_goals_backtest.walk_forward (the exact L3
walk-forward), l3_offline.raw_xg/wdl, national_elo_layer3.Isotonic. Coefficients fit ONLY on burn-in
(<2024), same as total_mean is fit today. Writes national_elo_layer3_calibration.json.

Run:  python analysis/worldcup/build_l3_total_calibration.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import total_goals_backtest as TG       # walk_forward (leak-free sup/gh/ga/is_oos)
import national_elo_layer3 as L3         # Isotonic, OOS_CUTOFF
import l3_offline                        # raw_xg, wdl, TOTAL_MATCHUP_LIVE

CALIB = HERE / "national_elo_layer3_calibration.json"


def run():
    if not CALIB.exists():
        raise SystemExit(f"missing {CALIB} — need the current calibration to preserve const path")
    cur = json.loads(CALIB.read_text(encoding="utf-8"))
    a0, a1, total_mean = float(cur["a0"]), float(cur["a1"]), float(cur["total_mean"])
    iso_const = cur["iso"] if "iso_const" not in cur else cur["iso_const"]
    # the CURRENT committed isotonic IS the constant-total isotonic -> preserve it verbatim
    if "iso_const" not in cur:
        iso_const = cur["iso"]

    wf = TG.walk_forward().dropna(subset=["sup"])
    burn = wf[wf["is_oos"] == 0]
    sb = burn["sup"].to_numpy(float)
    totb = (burn["gh"] + burn["ga"]).to_numpy(float)
    # match-dependent total (forma b), fit on burn-in real total — igual que total_mean hoy
    total_coef = [float(c) for c in np.linalg.lstsq(
        np.c_[np.ones(len(sb)), np.abs(sb), sb ** 2], totb, rcond=None)[0]]

    # re-fit the MATCHUP isotonic on burn-in with the new total (CRÍTICO: el total nuevo necesita su
    # propia isotónica; el backtest mostró que reusar la vieja rompe el 1X2). Same a0/a1 (la
    # diferencia no cambia), matchup total via raw_xg.
    gh = burn["gh"].to_numpy(float); ga = burn["ga"].to_numpy(float)
    res = np.where(gh > ga, 0, np.where(gh == ga, 1, 2)); Y = np.eye(3)[res]
    P = np.zeros((len(sb), 3))
    for i in range(len(sb)):
        lh, la = l3_offline.raw_xg(sb[i], a0, a1, total_mean, total_coef, matchup=True)
        P[i] = l3_offline.wdl(lh, la)
    P /= P.sum(1, keepdims=True)
    isos = [L3.Isotonic().fit(P[:, k], Y[:, k]) for k in range(3)]
    iso_match = [{"ux": [float(x) for x in io.ux], "uf": [float(x) for x in io.uf]} for io in isos]

    out = {
        "a0": a0, "a1": a1, "total_mean": total_mean, "total_coef": total_coef,
        "iso": iso_match, "iso_const": iso_const,
        "total_matchup": bool(l3_offline.TOTAL_MATCHUP_LIVE),
        "_note": "L3 calibration with MATCH-DEPENDENT total (forma b). a0/a1/total_mean/iso_const "
                 "preserved EXACTLY from the prior constant calibration (flag-off reversal). total_coef "
                 "+ matchup isotonic (iso) fit offline on burn-in (<2024). l3_offline picks by "
                 "TOTAL_MATCHUP_LIVE.",
        "_oos_cutoff": L3.OOS_CUTOFF, "_total_coef_form": "tb0 + tb1*|sup| + tb2*sup^2",
    }
    CALIB.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written: {CALIB}")
    print(f"  a0={a0:+.4f} a1={a1:.4f} total_mean(const)={total_mean:.4f}")
    print(f"  total_coef (forma b) = {total_coef[0]:+.4f} {total_coef[1]:+.4f}|sup| {total_coef[2]:+.4f}sup^2")
    print(f"  burn-in fixtures={len(sb)} | iso(matchup) re-fit | iso_const preserved verbatim")


if __name__ == "__main__":
    run()
