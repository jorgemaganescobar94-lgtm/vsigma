"""
Offline tests for the FULL-DATA model (no network). Covers: feature list stability, the live
predictor (valid output / impute-neutral no-crash / None when the artifact is absent), and — the
key contract — EXACT reversibility of the display resolver: with fd_* absent the shown prediction
is EXACTLY the ensemble (delta 0); with fd_* present it becomes the base; ctx_*/inj_* still outrank it.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_full_data_model as ffdm  # noqa: E402
import build_worldcup_full_card as fc  # noqa: E402


# ----------------------------------------------------------------- feature list
def test_feature_list_count_and_uniqueness():
    assert len(ffdm.FEATURES) == 26
    assert len(ffdm.FEATURES_CF) == 27 and ffdm.FEATURES_CF[-1] == "club_form_diff"
    assert len(ffdm.FEATURES_EXTRA) == 31                       # +4 intl player-agg
    assert ffdm.FEATURES_EXTRA[:27] == ffdm.FEATURES_CF          # extra is a superset
    assert len(set(ffdm.FEATURES_EXTRA)) == len(ffdm.FEATURES_EXTRA)   # no dups
    for k in ("l3_logit_h", "l3_xg_h", "neutral", "team_rating_diff"):
        assert k in ffdm.FEATURES
    for s in ffdm.STAT_FIELDS:
        assert f"{s}_diff" in ffdm.FEATURES
    for x in ffdm.EXTRA_FIELDS:
        assert f"{x}_diff" in ffdm.FEATURES_EXTRA


def test_active_features_follow_flags(monkeypatch):
    # 3-tier: extra(31) > club_form(27) > base(26); each flag reverts EXACTLY down a tier
    monkeypatch.setattr(ffdm, "EXTRA_PLAYER_AGG", True)
    monkeypatch.setattr(ffdm, "CLUB_FORM_FEATURE", True)
    assert ffdm.active_features() == ffdm.FEATURES_EXTRA and len(ffdm.active_features()) == 31
    monkeypatch.setattr(ffdm, "EXTRA_PLAYER_AGG", False)
    assert ffdm.active_features() == ffdm.FEATURES_CF and len(ffdm.active_features()) == 27
    monkeypatch.setattr(ffdm, "CLUB_FORM_FEATURE", False)
    assert ffdm.active_features() == list(ffdm.FEATURES) and len(ffdm.active_features()) == 26


def test_artifact_matches_active_feature_list():
    path = ffdm.active_artifact_path()
    if not path.exists():
        pytest.skip("artifact not trained in this checkout")
    art = ffdm._load_artifact(path)
    assert len(art["features"]) == len(art["mean"]) == len(art["std"]) == len(art["logit_W"])


# ----------------------------------------------------------------- live predictor
def test_predict_none_without_artifact(monkeypatch, tmp_path):
    # artifact missing -> None (caller reverts to ensemble). Never raises.
    monkeypatch.setattr(ffdm, "ARTIFACT", tmp_path / "nope.json")
    monkeypatch.setattr(ffdm, "_ARTIFACT_CACHE", None)
    assert ffdm.predict(10, 8, "2026-06-25", 1, 0.45, 0.28, 0.27, 1.4, 1.1) is None


def test_predict_valid_output_and_impute_neutral():
    if not ffdm.ARTIFACT.exists():
        pytest.skip("artifact not trained in this checkout")
    # unknown team ids -> most features missing -> imputed neutral, still a valid prediction (no crash)
    r = ffdm.predict(999001, 999002, "2026-06-25", 1, 0.40, 0.30, 0.30, 1.3, 1.2)
    assert r is not None
    s = r["fd_home"] + r["fd_draw"] + r["fd_away"]
    assert abs(s - 1.0) < 1e-6
    for k in ("fd_home", "fd_draw", "fd_away"):
        assert 0.0 <= r[k] <= 1.0
    assert 0.05 <= r["fd_xg_home"] <= 6.0 and 0.05 <= r["fd_xg_away"] <= 6.0
    assert r["n_features"] == len(ffdm.active_features())   # 26 or 27 per the flag
    assert r["n_missing"] >= 20   # unknown teams -> the point-in-time features are all missing


def test_predict_real_team_is_finite():
    # regression: a team with rich rolling-stat history must never yield NaN probs (non-finite
    # feature values -> impute-neutral, not propagated). England (id 10) has deep cache coverage.
    if not ffdm.ARTIFACT.exists():
        pytest.skip("artifact not trained in this checkout")
    import math
    r = ffdm.predict(10, 4673, "2026-06-25", 1, 0.72, 0.19, 0.09, 2.2, 0.6)
    assert r is not None
    for k in ("fd_home", "fd_draw", "fd_away", "fd_xg_home", "fd_xg_away"):
        assert math.isfinite(r[k])
    assert abs(r["fd_home"] + r["fd_draw"] + r["fd_away"] - 1.0) < 1e-6


def test_predict_soft_fails_to_none_on_bad_input(monkeypatch):
    if not ffdm.ARTIFACT.exists():
        pytest.skip("artifact not trained in this checkout")
    # a corrupt artifact (missing logit_W/etc.) must NOT raise from predict() -> returns None.
    # Corrupt the cache under the ACTIVE artifact's path key so _load_artifact serves it.
    key = str(ffdm.active_artifact_path())
    monkeypatch.setattr(ffdm, "_ARTIFACT_CACHE", {key: {"features": list(ffdm.active_features())}})
    assert ffdm.predict(10, 8, "2026-06-25", 1, 0.45, 0.28, 0.27, 1.4, 1.1) is None


# ----------------------------------------------------------------- reversibility (display resolver)
ENS = {"ens_home": 0.50, "ens_draw": 0.30, "ens_away": 0.20,
       "ens_xg_home": 1.6, "ens_xg_away": 1.0}
FD = {"fd_home": 0.44, "fd_draw": 0.31, "fd_away": 0.25, "fd_xg_home": 1.5, "fd_xg_away": 1.1}


def test_revert_exact_when_fd_absent():
    # FULL_DATA_LIVE off (or fd None) -> no fd_* -> resolver returns the ENSEMBLE exactly (delta 0)
    ph, pdr, pa, xgh, xga, note = fc.pred_1x2(dict(ENS))
    assert (ph, pdr, pa, xgh, xga) == (0.50, 0.30, 0.20, 1.6, 1.0)
    assert note == fc.ENS_NOTE


def test_fd_becomes_base_when_present():
    # fd_* present -> it outranks ens_* as the shown base
    r = {**ENS, **FD}
    ph, pdr, pa, xgh, xga, note = fc.pred_1x2(r)
    assert (ph, pdr, pa, xgh, xga) == (0.44, 0.31, 0.25, 1.5, 1.1)
    assert note == fc.FD_NOTE


def test_ctx_and_inj_still_outrank_fd():
    # context/injuries chain ON TOP of fd -> they must still win the resolver
    r = {**ENS, **FD, "ctx_home": 0.42, "ctx_draw": 0.32, "ctx_away": 0.26,
         "ctx_xg_home": 1.4, "ctx_xg_away": 1.2, "context_note": "escenario X"}
    ph, pdr, pa, _xgh, _xga, note = fc.pred_1x2(r)
    assert (ph, pdr, pa) == (0.42, 0.32, 0.26) and note == "escenario X"
    r2 = {**r, "inj_home": 0.40, "inj_draw": 0.33, "inj_away": 0.27,
          "inj_xg_home": 1.35, "inj_xg_away": 1.25}
    ph2, pdr2, pa2, *_ = fc.pred_1x2(r2)
    assert (ph2, pdr2, pa2) == (0.40, 0.33, 0.27)


# ----------------------------------------------------------------- club_form feature
def test_flags_select_artifact_tiers(monkeypatch):
    monkeypatch.setattr(ffdm, "EXTRA_PLAYER_AGG", False)
    monkeypatch.setattr(ffdm, "CLUB_FORM_FEATURE", False)
    assert ffdm.active_artifact_path() == ffdm.ARTIFACT
    monkeypatch.setattr(ffdm, "CLUB_FORM_FEATURE", True)
    assert ffdm.active_artifact_path() == (ffdm.ARTIFACT_CF if ffdm.ARTIFACT_CF.exists() else ffdm.ARTIFACT)
    monkeypatch.setattr(ffdm, "EXTRA_PLAYER_AGG", True)
    assert ffdm.active_artifact_path() == (ffdm.ARTIFACT_EXTRA if ffdm.ARTIFACT_EXTRA.exists()
                                           else ffdm.ARTIFACT_CF if ffdm.ARTIFACT_CF.exists() else ffdm.ARTIFACT)


def test_predict_finite_across_all_tiers(monkeypatch):
    if not ffdm.ARTIFACT.exists():
        pytest.skip("artifact not trained in this checkout")
    import math
    for extra, cf in ((True, True), (False, True), (False, False)):
        monkeypatch.setattr(ffdm, "EXTRA_PLAYER_AGG", extra)
        monkeypatch.setattr(ffdm, "CLUB_FORM_FEATURE", cf)
        r = ffdm.predict(10, 4673, "2026-06-25", 1, 0.72, 0.19, 0.09, 2.2, 0.6)
        assert r is not None and math.isfinite(r["fd_home"])
        assert abs(r["fd_home"] + r["fd_draw"] + r["fd_away"] - 1.0) < 1e-6


def test_player_agg_table_present():
    # committed per-team-match aggregates: the populated fields exist for downstream rolling
    if not ffdm.INTL_AGG_CSV.exists():
        pytest.skip("intl player-agg table not built in this checkout")
    import pandas as pd
    df = pd.read_csv(ffdm.INTL_AGG_CSV)
    for x in ffdm.EXTRA_FIELDS:
        assert x in df.columns


def test_club_form_table_sanity():
    # committed per-team table: 48 teams, elite club-form > minnows (redundant-with-L3 ordering)
    if not ffdm.CLUB_FORM_CSV.exists():
        pytest.skip("club_form table not built in this checkout")
    import pandas as pd
    cf = pd.read_csv(ffdm.CLUB_FORM_CSV).set_index("team")
    assert cf["team_id"].nunique() == 48
    if {"Germany", "South Africa"} <= set(cf.index):
        assert cf.loc["Germany", "club_form"] > cf.loc["South Africa", "club_form"]


# ----------------------------------------------------------------- A/B scorer helpers
def test_ab_scorer_metric_helpers():
    import numpy as np
    import worldcup_full_data_ab_scorer as sc
    P = np.array([[0.6, 0.3, 0.1], [0.2, 0.3, 0.5]])
    y = np.array([0, 2])
    assert sc._ll(P, y) > 0
    assert 0.0 <= sc._acc(P, y) <= 1.0
    assert sc._brier(P, y) >= 0.0
