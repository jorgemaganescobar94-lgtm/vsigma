"""
Fase 4G offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the card-risk adjustment EVALUATION: Brier/LogLoss for original vs adjusted, calibration bins,
segmentation, low-sample handling, real-event detection, predictions-without-result, and the
conservative recommendation. Verifies report wording and absence of betting language.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import evaluate_worldcup_card_risk_adjustment as ev  # noqa: E402

FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado"]


# ---------------------------------------------------------------- pure metrics
def test_brier_and_logloss_basic():
    # perfect forecasts -> 0 Brier, ~0 LogLoss
    assert ev.brier_score([1.0, 0.0], [1, 0]) == 0.0
    assert ev.log_loss([1.0, 0.0], [1, 0]) < 1e-6
    # worse forecasts -> higher
    assert ev.brier_score([0.5, 0.5], [1, 0]) == 0.25
    assert ev.brier_score([], []) is None and ev.log_loss([], []) is None


def test_adjusted_better_when_closer_to_outcome():
    y = [1, 0, 1, 0]
    orig = [0.5, 0.5, 0.5, 0.5]
    adj = [0.7, 0.3, 0.7, 0.3]                 # moved toward the truth
    assert ev.brier_score(adj, y) < ev.brier_score(orig, y)
    assert ev.log_loss(adj, y) < ev.log_loss(orig, y)


def test_adjusted_worse_when_away_from_outcome():
    y = [1, 0, 1, 0]
    orig = [0.6, 0.4, 0.6, 0.4]
    adj = [0.4, 0.6, 0.4, 0.6]                 # moved AWAY from the truth
    assert ev.brier_score(adj, y) > ev.brier_score(orig, y)
    assert ev.log_loss(adj, y) > ev.log_loss(orig, y)


def test_calibration_bins_structure():
    bins = ev.calibration_bins([0.05, 0.15, 0.95], [0, 0, 1])
    assert all({"bin_lo", "bin_hi", "n", "avg_pred", "real_rate"} <= set(b) for b in bins)
    assert sum(b["n"] for b in bins) == 3


# ---------------------------------------------------------------- eval-row construction + labels
class _Resolver:
    def __init__(self, ctx=None):
        self.ctx = ctx or {"card_environment": "no determinado", "confidence": "baja",
                           "matches_sample": None, "referee_name": None}

    def ctx_for(self, fid):
        return self.ctx


def _settled(rows):
    cols = ["fixture_id", "player_id", "team_id", "team", "player", "p_card", "act_card", "settled"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


def test_real_card_event_detected_and_label():
    df = _settled([
        {"fixture_id": 1, "player_id": 10, "team_id": 100, "team": "A", "player": "Booked",
         "p_card": 0.30, "act_card": 1, "settled": 1},
        {"fixture_id": 1, "player_id": 11, "team_id": 100, "team": "A", "player": "Clean",
         "p_card": 0.20, "act_card": 0, "settled": 1},
    ])
    rows = ev.build_evaluation_rows(df, {"players": {}, "teams": {}, "positions": {}}, {}, _Resolver())
    labels = {r["player_name"]: r["label_card"] for r in rows}
    assert labels["Booked"] == 1 and labels["Clean"] == 0
    assert len(rows) == 2


def test_prediction_without_result_is_skipped():
    # missing p_card -> not evaluable (skipped, never fabricated)
    df = _settled([{"fixture_id": 1, "player_id": 10, "team_id": 100, "team": "A", "player": "NoProb",
                    "p_card": None, "act_card": 1, "settled": 1}])
    rows = ev.build_evaluation_rows(df, {"players": {}, "teams": {}, "positions": {}}, {}, _Resolver())
    assert rows == []


def test_adjusted_reconstruction_uses_profiles():
    # an 'alto' player history with a populated team should push the adjusted probability UP.
    cp = {"players": {10: {"player_id": 10, "position": "DEF",
                           "card_risk_player_history": "alto", "confidence": "media"}},
          "teams": {100: {"team_id": 100, "card_environment_team": "alto", "confidence": "media"}},
          "positions": {"DEF": {"position": "DEF", "card_risk_position": "alto", "confidence": "media"}}}
    df = _settled([{"fixture_id": 1, "player_id": 10, "team_id": 100, "team": "A", "player": "Hard",
                    "p_card": 0.30, "act_card": 1, "settled": 1}])
    ctx = {"card_environment": "medio", "confidence": "media", "matches_sample": 4, "referee_name": "Ref X"}
    rows = ev.build_evaluation_rows(df, cp, {}, _Resolver(ctx))
    r = rows[0]
    assert r["probability_card_adjusted"] > r["probability_card_original"]
    assert r["adjustment_direction"] == "subir"
    assert r["position"] == "DEF" and r["referee_name"] == "Ref X"


# ---------------------------------------------------------------- segmentation
def _rows(n_each):
    rows = []
    for pos, n in n_each.items():
        for i in range(n):
            rows.append({"fixture_id": i, "player_id": i, "player_name": f"{pos}{i}", "team": "A",
                         "team_id": 1, "position": pos, "referee_name": "R",
                         "probability_card_original": 0.3, "probability_card_adjusted": 0.32,
                         "adjustment_direction": "subir", "abs_adjustment": 0.02,
                         "label_card": 1 if i % 3 == 0 else 0, "confidence": "media-baja",
                         "data_quality": "baja"})
    return rows


def test_segment_by_position_counts_and_usable_flag():
    rows = _rows({"DEF": 8, "GK": 2})
    seg = ev.segment(rows, lambda r: r["position"])
    assert seg["DEF"]["n"] == 8 and seg["DEF"]["usable"] is True
    assert seg["GK"]["n"] == 2 and seg["GK"]["usable"] is False        # below SEG_MIN


def test_segment_by_direction_present():
    rows = _rows({"MID": 6})
    seg = ev.segment(rows, lambda r: r["adjustment_direction"])
    assert "subir" in seg and seg["subir"]["n"] == 6


# ---------------------------------------------------------------- recommendation (conservative)
def test_recommend_low_sample_does_not_conclude():
    overall = {"n": 10, "n_positive": 2, "delta_brier": -0.5, "delta_logloss": -0.5}
    rec = ev.recommend(overall, {"by_direction": {}, "by_referee": {}})
    assert rec["low_sample"] is True
    assert "no tocar" in rec["weights"].lower() or "muestra" in rec["weights"].lower()


def test_recommend_keep_when_both_improve():
    overall = {"n": 400, "n_positive": 60, "delta_brier": -0.01, "delta_logloss": -0.03}
    rec = ev.recommend(overall, {"by_direction": {}, "by_referee": {}})
    assert "mantener" in rec["weights"].lower()
    assert rec["verdict"] == "adjusted mejora ambas"


def test_recommend_lower_when_both_worsen():
    overall = {"n": 400, "n_positive": 60, "delta_brier": 0.02, "delta_logloss": 0.04}
    rec = ev.recommend(overall, {"by_direction": {}, "by_referee": {}})
    assert "bajar" in rec["weights"].lower()


def test_recommend_flags_referee_inactive():
    overall = {"n": 400, "n_positive": 60, "delta_brier": -0.01, "delta_logloss": -0.03}
    rec = ev.recommend(overall, {"by_direction": {}, "by_referee": {"no determinado": {"n": 400}}})
    assert "inactivo" in rec["factor_referee"].lower()


# ---------------------------------------------------------------- report wording + no betting language
def test_report_has_conservative_recommendation_and_no_betting():
    cp = {"players": {}, "teams": {}, "positions": {}}
    df = _settled([{"fixture_id": i, "player_id": i, "team_id": 1, "team": "A", "player": f"P{i}",
                    "p_card": 0.2, "act_card": 1 if i % 4 == 0 else 0, "settled": 1} for i in range(40)])
    rows = ev.build_evaluation_rows(df, cp, {}, _Resolver())
    overall = ev.metric_block(rows)
    overall["over_adjustment"] = ev._over_adjustment(rows)
    overall["confidence"], overall["data_quality"] = "media-baja", "media-baja"
    payload = {"meta": {"n_predictions": len(rows), "n_with_result": overall["n"]},
               "overall": overall,
               "calibration_original": ev.calibration_bins(
                   [r["probability_card_original"] for r in rows], [r["label_card"] for r in rows]),
               "calibration_adjusted": ev.calibration_bins(
                   [r["probability_card_adjusted"] for r in rows], [r["label_card"] for r in rows]),
               "segments": {"by_position": ev.segment(rows, lambda r: r["position"]),
                            "by_direction": ev.segment(rows, lambda r: r["adjustment_direction"]),
                            "by_confidence": ev.segment(rows, lambda r: r["confidence"]),
                            "by_referee": ev._referee_segment(rows), "by_team": ev._team_segment(rows)},
               "recommendation": ev.recommend(overall, {"by_direction": {}, "by_referee": {}})}
    txt = ev.render_txt(payload).lower()
    assert "recomendación" in txt and ("pesos" in txt)
    assert not any(w in txt for w in FORBIDDEN)


# ---------------------------------------------------------------- artifact round-trip
def test_build_writes_artifacts(tmp_path):
    props = tmp_path / "props.csv"
    _settled([{"fixture_id": i, "player_id": i, "team_id": 1, "team": "A", "player": f"P{i}",
               "p_card": 0.2, "act_card": 1 if i % 4 == 0 else 0, "settled": 1} for i in range(35)]
             ).to_csv(props, index=False)
    # redirect outputs into tmp by monkeypatching module paths
    ev.OUT_CSV = tmp_path / "eval.csv"
    ev.OUT_JSON = tmp_path / "eval.json"
    ev.OUT_TXT = tmp_path / "eval.txt"
    payload = ev.build(props_path=props, card_profiles={"players": {}, "teams": {}, "positions": {}},
                       write=True)
    assert (tmp_path / "eval.csv").exists() and (tmp_path / "eval.json").exists()
    assert payload["overall"]["n"] == 35
    assert "recommendation" in payload
