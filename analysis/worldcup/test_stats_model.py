"""
Tests for the per-team stats model (stats_model.py) after integrating own_str (team's OWN L3
strength, symmetric to opp_str). NO network, NO API, NO market.

Covers:
  * own_str + opp_str both present in the design matrix (fit_stat) and recovered with the right sign.
  * Predictor.predict uses own_str -> a stronger team gets a higher predicted count.
  * Re-validation: the shipped walk-forward lift RISES on real data (shots >= 41%, corners >= 22%),
    above the pre-own_str levels (38.05 / 19.91) -> own_str genuinely helps OOS.
  * Per-stat confidence thresholds (conf_level) and stat_confidence() from the committed calibration:
    shots -> 'media' (lift ~43), corners -> 'baja' (~24), cards -> hidden (~3, noise).
  * Props sanity: per-fixture shots_total / cards_total stay positive and in a plausible range.

Run:  python -m pytest analysis/worldcup/test_stats_model.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stats_model as SM  # noqa: E402


def _lift(y, lam):
    base = np.full(len(y), float(np.mean(y)))
    db, dm = SM.poisson_dev(y, base), SM.poisson_dev(y, lam)
    return 100.0 * (db - dm) / db


# --------------------------------------------------------------------- design matrix / fit
def test_fit_stat_includes_own_and_opp_strength():
    """fit_stat now carries [mu, gamma, b_opp, b_own, att(T), conc(T)] and recovers a POSITIVE own
    coefficient when the OWN-strength feature drives the (synthetic) log-count."""
    rng = np.random.default_rng(0)
    T = 4
    N = 4000
    team_l = rng.integers(0, T, N)
    opp_l = rng.integers(0, T, N)
    home = rng.integers(0, 2, N).astype(float)
    feat_own = rng.normal(size=N)
    feat_opp = rng.normal(size=N)
    # z driven by own (+0.8) and opp (-0.5), plus a small home effect
    z = 1.0 + 0.2 * home + 0.8 * feat_own - 0.5 * feat_opp + 0.05 * rng.normal(size=N)
    w = np.ones(N)
    beta = SM.fit_stat(team_l, opp_l, home, feat_opp, feat_own, z, w, T)
    assert len(beta) == 4 + 2 * T, "design must hold mu, gamma, opp, own + att/conc"
    b_opp, b_own = beta[2], beta[3]
    assert b_own > 0.5, f"own-strength coef should be ~+0.8, got {b_own:.2f}"
    assert b_opp < -0.2, f"opp-strength coef should be ~-0.5, got {b_opp:.2f}"


def test_predict_stronger_team_gets_more():
    """Predictor.predict: with att/conc held equal and ownstr_beta>0, the stronger team's predicted
    count exceeds the weaker team's (own_str moves the prediction, not just the opponent's)."""
    rdf = pd.DataFrame([
        {"team": "Strong", "corners_att": 0.0, "corners_conc": 0.0,
         "cards_att": 0.0, "cards_conc": 0.0, "shots_att": 0.0, "shots_conc": 0.0},
        {"team": "Weak", "corners_att": 0.0, "corners_conc": 0.0,
         "cards_att": 0.0, "cards_conc": 0.0, "shots_att": 0.0, "shots_conc": 0.0},
    ])
    calib = {s: {"mu": 1.0, "gamma": 0.0, "oppstr_beta": 0.0, "ownstr_beta": 0.3,
                 "line": SM.DEFAULT_LINES[s], "show": True, "lift": 40.0, "conf": "media"}
             for s in SM.STATS}
    calib["_oppstr"] = {"mean": 0.0, "std": 1.0}
    pred = SM.Predictor(ratings_df=rdf, calib=calib)
    pred.strength = {"Strong": 3.0, "Weak": -3.0}     # standardised later via os_mean/os_std=0/1
    out = pred.predict("Strong", "Weak")
    assert out is not None
    # home=Strong gets the home (own) lambda; away=Weak gets the away lambda
    assert out["shots_home"] > out["shots_away"], "stronger team must have the higher predicted count"
    # and only own_str differs here (opp coef 0) -> the gap is exactly the own-strength effect
    assert out["shots_home"] > 1.0 and out["shots_away"] > 1.0


# --------------------------------------------------------------------- re-validation on real data
def _real_lift(stat):
    df = SM._load_raw()
    m = float(df["opp_str"].mean()); s = float(df["opp_str"].std()) or 1.0
    df["opp_str_z"] = (df["opp_str"].fillna(m) - m) / s
    df["own_str_z"] = (df["own_str"].fillna(m) - m) / s
    teams = sorted(set(df["team_id"]) | set(df["opp_id"]))
    _, y, lam, oos = SM.walkforward(df, stat, teams)
    return _lift(y[oos], lam[oos])


def test_revalidation_shots_lift_rose():
    """Shots OOS deviance-lift rises to ~43% (was 38.05 before own_str)."""
    assert _real_lift("shots") >= 41.0


def test_revalidation_corners_lift_rose():
    """Corners OOS deviance-lift rises to ~24% (was 19.91 before own_str)."""
    assert _real_lift("corners") >= 22.0


# --------------------------------------------------------------------- per-stat confidence
def test_conf_level_named_thresholds():
    assert SM.conf_level(43.0) == "media"      # >= CONF_MEDIA_MIN (30)
    assert SM.conf_level(30.0) == "media"
    assert SM.conf_level(23.6) == "baja"       # >= SHOW_LIFT_MIN (4), < 30
    assert SM.conf_level(4.0) == "baja"
    assert SM.conf_level(3.4) == "oculta"      # < SHOW_LIFT_MIN -> hidden (cards)
    assert SM.conf_level(None) == "oculta"


def test_stat_confidence_from_committed_calibration():
    """The committed calibration (regenerated by the refit) labels shots=media, corners=baja,
    cards hidden — driven purely by the measured OOS lift."""
    conf = SM.stat_confidence()
    assert conf.get("shots") == "media", f"shots should be media, got {conf}"
    assert conf.get("corners") == "baja", f"corners should be baja, got {conf}"
    assert "cards" not in conf, "cards is noise -> hidden, never labelled"


# --------------------------------------------------------------------- props sanity
def test_props_inputs_stay_sane():
    """The model feeds st_shots_total / st_cards_total into the props. After the refit, a real WC
    pair's totals must stay positive and in a plausible range (no blow-up from own_str)."""
    pred = SM.load_predictor()
    assert pred is not None, "ratings + calibration must exist (run --fit)"
    teams = list(pred.att.get("shots", {}).keys())
    assert len(teams) >= 2
    got = 0
    for a in teams[:8]:
        for b in teams[:8]:
            if a == b:
                continue
            out = pred.predict(a, b)
            if not out:
                continue
            got += 1
            assert 6.0 <= out["shots_total"] <= 45.0, f"shots_total out of range: {out['shots_total']}"
            assert 0.5 <= out["cards_total"] <= 12.0, f"cards_total out of range: {out['cards_total']}"
            assert out["corners_total"] > 0
    assert got >= 1, "expected at least one predictable real pair"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print(f"  PASS {name}")
    print("OK")
