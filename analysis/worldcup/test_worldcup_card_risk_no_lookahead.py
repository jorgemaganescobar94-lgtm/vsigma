"""
Fase 4H offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the ANTI-LOOK-AHEAD evaluation: pre_fixture uses only earlier-day events, leave_one_out excludes
the evaluated fixture, profiles drive the reconstructed adjustment, metrics/segmentation, and the
conservative recommendation (mantener vs shadow/freeze). Verifies no betting language.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import evaluate_worldcup_card_risk_adjustment_no_lookahead as nl  # noqa: E402

FORBIDDEN = ["apuesta", "apostar", "cuota", "odds", "edge", "pick", "stake", "roi", "mercado"]

_EV_COLS = ["fixture_id", "date", "team_id", "team_name", "opponent_id", "opponent_name",
            "player_id", "player_name", "event_type", "card_type", "is_card", "is_goal"]


def _card(fid, date, team_id, opp_id, pid, pname):
    return {"fixture_id": fid, "date": date, "team_id": team_id, "team_name": "T",
            "opponent_id": opp_id, "opponent_name": "O", "player_id": pid, "player_name": pname,
            "event_type": "Card", "card_type": "Yellow Card", "is_card": 1, "is_goal": 0}


def _events(rows):
    return pd.DataFrame([{c: r.get(c) for c in _EV_COLS} for r in rows], columns=_EV_COLS)


def _props(rows):
    cols = ["fixture_id", "kickoff_utc", "team_id", "team", "player_id", "player", "p_card",
            "act_card", "settled"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


# ---------------------------------------------------------------- pre_fixture / leave_one_out windows
def _scenario():
    # player 10 (team 100) booked heavily in EARLIER fixtures, and again in a FUTURE one.
    events = _events([
        _card(1, "2026-06-20", 100, 200, 10, "Hot"), _card(1, "2026-06-20", 100, 200, 10, "Hot"),
        _card(2, "2026-06-22", 100, 300, 10, "Hot"),
        _card(9, "2026-06-26", 100, 400, 10, "Hot"),   # FUTURE relative to the evaluated fixture (06-25)
    ])
    # evaluated fixture 5 on 06-25, player 10 predicted p_card 0.30, got booked.
    props = _props([{"fixture_id": 5, "kickoff_utc": "2026-06-25 18:00", "team_id": 100, "team": "T",
                     "player_id": 10, "player": "Hot", "p_card": 0.30, "act_card": 1, "settled": 1}])
    pos_map = {10: "MID"}
    referees = {5: None}
    return events, props, pos_map, referees


def test_pre_fixture_excludes_same_and_future_events():
    events, props, pos_map, referees = _scenario()
    rows = nl.build_rows(props, events, pos_map, referees)
    assert len(rows) == 1
    r = rows[0]
    # pre_fixture profile = events from 06-20/06-22 only (NOT fixture 5 itself, NOT future fixture 9).
    # cumulative includes the future booking -> a STRONGER 'alto' history -> higher adjusted than pre.
    assert r["p_adjusted_pre_fixture"] <= r["p_adjusted_cumulative"] + 1e-9
    assert r["p_adjusted_pre_fixture"] >= r["p_original"]              # prior history still pushes up


def test_leave_one_out_excludes_evaluated_fixture_only():
    events, props, pos_map, referees = _scenario()
    # build profiles directly for the two regimes for fixture 5
    pre = events[events["date"].astype(str).str[:10] < "2026-06-25"]
    loo = events[events["fixture_id"].astype("Int64") != 5]
    assert set(pre["fixture_id"]) == {1, 2}                           # only earlier days
    assert 9 in set(loo["fixture_id"]) and 5 not in set(loo["fixture_id"])  # future kept, self removed


def test_prior_history_produces_upward_adjustment():
    events, props, pos_map, referees = _scenario()
    pre_idx, pre_ref = nl.build_profiles_from_events(
        events[events["date"].astype(str).str[:10] < "2026-06-25"], pos_map, referees)
    adj, pos, _ = nl._adjust_with(pre_idx, pre_ref, 0.30, 10, 100, None, pos_map)
    assert adj["adjustment_direction"] == "subir"
    assert adj["probability_card_adjusted"] > 0.30


def test_no_prior_history_is_neutral():
    # evaluate the EARLIEST fixture -> no earlier events -> empty pre profiles -> neutral, low conf.
    events = _events([_card(1, "2026-06-20", 100, 200, 10, "Hot")])
    props = _props([{"fixture_id": 1, "kickoff_utc": "2026-06-20 18:00", "team_id": 100, "team": "T",
                     "player_id": 10, "player": "Hot", "p_card": 0.30, "act_card": 1, "settled": 1}])
    rows = nl.build_rows(props, events, {10: "MID"}, {1: None})
    r = rows[0]
    assert r["adjustment_direction_pre_fixture"] == "neutro"
    assert r["p_adjusted_pre_fixture"] == r["p_original"]
    assert r["confidence"] == "baja" and "sin historial previo" in r["reason"]


# ---------------------------------------------------------------- metrics / segmentation
def _mode_rows_synth():
    return [
        {"p_original": 0.5, "p_adjusted_pre_fixture": 0.7, "p_adjusted_leave_one_out": 0.7,
         "p_adjusted_cumulative": 0.7, "act_card": 1, "fixture_id": 1, "player_id": 1,
         "player_name": "A", "team": "T", "team_id": 1, "position": "DEF", "referee_name": "R",
         "adjustment_direction_pre_fixture": "subir", "adjustment_direction_leave_one_out": "subir",
         "adjustment_direction_cumulative": "subir", "confidence": "media-baja"},
        {"p_original": 0.5, "p_adjusted_pre_fixture": 0.3, "p_adjusted_leave_one_out": 0.3,
         "p_adjusted_cumulative": 0.3, "act_card": 0, "fixture_id": 2, "player_id": 2,
         "player_name": "B", "team": "T", "team_id": 1, "position": "FWD", "referee_name": "R",
         "adjustment_direction_pre_fixture": "bajar", "adjustment_direction_leave_one_out": "bajar",
         "adjustment_direction_cumulative": "bajar", "confidence": "media-baja"},
    ]


def test_mode_summary_metrics_and_segments():
    rows = _mode_rows_synth()
    mrows = nl._mode_rows(rows, "p_adjusted_pre_fixture", "adjustment_direction_pre_fixture")
    mb = nl._mode_summary(mrows)
    assert mb["n"] == 2 and mb["brier_adjusted"] < mb["brier_original"]   # moved toward outcomes
    assert "by_direction" in mb["segments"] and "by_position" in mb["segments"]
    assert mb["real_rate_by_direction"]["subir"]["real_card_rate"] == 1.0
    assert mb["real_rate_by_direction"]["bajar"]["real_card_rate"] == 0.0


# ---------------------------------------------------------------- recommendation
def _mb(n, db, dl):
    return {"n": n, "n_positive": 40, "delta_brier": db, "delta_logloss": dl}


def test_recommend_keep_when_material_improvement_survives():
    rec = nl.recommend(_mb(400, -0.01, -0.03), _mb(400, -0.008, -0.02), _mb(400, -0.008, -0.02))
    assert rec["improvement_survives_no_lookahead"] is True
    assert "mantener" in rec["weights"].lower()


def test_recommend_shadow_when_improvement_vanishes():
    # cumulative improves a lot, pre_fixture only negligibly -> freeze as shadow.
    rec = nl.recommend(_mb(400, -0.013, -0.045), _mb(400, -0.0001, -0.0004), _mb(400, -0.0001, -0.0004))
    assert rec["improvement_survives_no_lookahead"] is False
    assert "shadow" in rec["weights"].lower()
    assert rec["negligible_pre_fixture"] is True
    assert any("look-ahead" in n for n in rec["notes"])


def test_recommend_lower_when_worsens_no_lookahead():
    rec = nl.recommend(_mb(400, -0.01, -0.03), _mb(400, 0.01, 0.03), _mb(400, 0.01, 0.03))
    assert "bajar" in rec["weights"].lower()


def test_recommend_low_sample_does_not_conclude():
    rec = nl.recommend(_mb(10, -0.01, -0.03), _mb(10, -0.01, -0.03), _mb(10, -0.01, -0.03))
    assert "no tocar" in rec["weights"].lower() or "muestra" in rec["weights"].lower()


# ---------------------------------------------------------------- report wording + no betting
def test_report_no_betting_language():
    events, props, pos_map, referees = _scenario()
    rows = nl.build_rows(props, events, pos_map, referees)
    cum = nl._mode_summary(nl._mode_rows(rows, "p_adjusted_cumulative", "adjustment_direction_cumulative"))
    pre = nl._mode_summary(nl._mode_rows(rows, "p_adjusted_pre_fixture", "adjustment_direction_pre_fixture"))
    loo = nl._mode_summary(nl._mode_rows(rows, "p_adjusted_leave_one_out",
                                         "adjustment_direction_leave_one_out"))
    payload = {"meta": {"n_predictions": len(rows)}, "cumulative": cum, "pre_fixture": pre,
               "leave_one_fixture_out": loo, "recommendation": nl.recommend(cum, pre, loo)}
    txt = nl.render_txt(payload).lower()
    assert "anti-look-ahead" in txt and "recomendación" in txt
    assert not any(w in txt for w in FORBIDDEN)


# ---------------------------------------------------------------- artifact round-trip
def test_build_writes_artifacts(tmp_path, monkeypatch):
    events, props, pos_map, referees = _scenario()
    ev_csv = tmp_path / "events.csv"; events.to_csv(ev_csv, index=False)
    pr_csv = tmp_path / "props.csv"; props.to_csv(pr_csv, index=False)
    monkeypatch.setattr(nl, "OUT_CSV", tmp_path / "eval.csv")
    monkeypatch.setattr(nl, "OUT_JSON", tmp_path / "eval.json")
    monkeypatch.setattr(nl, "OUT_TXT", tmp_path / "eval.txt")
    # referees map comes from refauto.load_fixture_referees(FIXTURE_REFEREES); point it at an empty file
    payload = nl.build(props_path=pr_csv, events_path=ev_csv, write=True)
    assert (tmp_path / "eval.csv").exists() and (tmp_path / "eval.json").exists()
    assert "recommendation" in payload
    df = pd.read_csv(tmp_path / "eval.csv")
    assert list(df.columns) == nl.CSV_COLUMNS
