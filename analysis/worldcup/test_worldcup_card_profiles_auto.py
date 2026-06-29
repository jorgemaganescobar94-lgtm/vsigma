"""
Fase 4F offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the auto CARD-discipline profiles (player / team / position) derived from REAL events, the
conservative card_risk_adjuster, the builder integration (probability_card_original/_adjusted), and the
Telegram card-risk block (adjusted % + motivo + low-sample warning, no betting language).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import build_worldcup_card_profiles_auto as cpa  # noqa: E402
import card_risk_adjuster as cardadj  # noqa: E402
import build_worldcup_player_events as bpe  # noqa: E402
import build_worldcup_player_events_telegram as tg  # noqa: E402
import player_events_core as core  # noqa: E402


# ---------------------------------------------------------------- event fixtures
_EVENT_COLS = ["fixture_id", "team_id", "team_name", "opponent_id", "opponent_name",
               "player_id", "player_name", "event_type", "card_type", "is_card", "is_goal"]


def _ev(rows):
    return pd.DataFrame([{c: r.get(c) for c in _EVENT_COLS} for r in rows], columns=_EVENT_COLS)


def _card(fid, team_id, team_name, opp_id, opp_name, pid, pname, ctype="Yellow Card"):
    return {"fixture_id": fid, "team_id": team_id, "team_name": team_name, "opponent_id": opp_id,
            "opponent_name": opp_name, "player_id": pid, "player_name": pname,
            "event_type": "Card", "card_type": ctype, "is_card": 1, "is_goal": 0}


def _goal(fid, team_id, team_name, opp_id, opp_name, pid, pname):
    return {"fixture_id": fid, "team_id": team_id, "team_name": team_name, "opponent_id": opp_id,
            "opponent_name": opp_name, "player_id": pid, "player_name": pname,
            "event_type": "Goal", "card_type": None, "is_card": 0, "is_goal": 1}


# ---------------------------------------------------------------- §2 player profiles
def test_player_with_cards_gets_profile():
    ev = _ev([_card(1, 10, "A", 20, "B", 100, "Carder", "Yellow Card"),
              _card(2, 10, "A", 30, "C", 100, "Carder", "Yellow Card")])
    profs = {p["player_id"]: p for p in cpa.derive_player_profiles(ev, {100: "MID"})}
    p = profs[100]
    assert p["matches_sample"] == 2 and p["cards_total"] == 2 and p["yellow_cards_total"] == 2
    assert p["cards_pg"] == 1.0
    assert p["card_risk_player_history"] == "alto"        # 1.0 card/game over 2 games
    assert p["position"] == "MID"
    assert p["source"] == "worldcup_events_auto"


def test_player_with_sample_no_cards_is_not_zero_risk():
    # appears (goal) in 2 fixtures, never booked -> sample but no cards: must NOT be a hard zero.
    ev = _ev([_goal(1, 10, "A", 20, "B", 200, "Clean"),
              _goal(2, 10, "A", 30, "C", 200, "Clean")])
    p = {x["player_id"]: x for x in cpa.derive_player_profiles(ev, {})}[200]
    assert p["matches_sample"] == 2 and p["cards_total"] == 0
    assert p["card_risk_player_history"] == "bajo"        # bajo, NOT "no determinado"/zero
    assert p["confidence"] != "no determinado"
    assert "no asumir riesgo cero" in p["reason"]


def test_single_match_card_capped_at_medio():
    ev = _ev([_card(1, 10, "A", 20, "B", 300, "OneGame", "Yellow Card")])
    p = {x["player_id"]: x for x in cpa.derive_player_profiles(ev, {})}[300]
    assert p["matches_sample"] == 1
    assert p["card_risk_player_history"] == "medio"       # 1 game is not a trend -> capped
    assert p["confidence"] == "baja"


def test_red_and_second_yellow_classified():
    assert cpa.classify_card_type("Red Card") == (0, 1, 0)
    assert cpa.classify_card_type("Second Yellow card") == (0, 0, 1)
    assert cpa.classify_card_type("Yellow Card") == (1, 0, 0)
    # a non-card row (is_card=0, NaN type) must NOT count as a card
    assert cpa.card_counts({"is_card": 0, "card_type": None}) == (0, 0, 0)
    assert cpa.card_counts({"is_card": 1, "card_type": None}) == (1, 0, 0)


# ---------------------------------------------------------------- §3 team profiles
def test_team_profile_for_and_against():
    # fixture 1: A gets 2 cards, B gets 1. A's cards_for=2, cards_against=1 over 1 match.
    ev = _ev([_card(1, 10, "A", 20, "B", 100, "a1"), _card(1, 10, "A", 20, "B", 101, "a2"),
              _card(1, 20, "B", 10, "A", 200, "b1")])
    teams = {t["team_id"]: t for t in cpa.derive_team_profiles(ev)}
    a = teams[10]
    assert a["matches_sample"] == 1 and a["cards_total"] == 2
    assert a["cards_for_pg"] == 2.0 and a["cards_against_pg"] == 1.0
    assert a["card_environment_team"] == "alto"           # 2.0 >= TEAM_HIGH_PG


# ---------------------------------------------------------------- §4 position profiles
def test_position_profile_relative_labels():
    rows = []
    pos_map = {}
    # MID heavily carded (3/fixture), DEF lightly (1/fixture), FWD a single card (insufficient).
    for f in range(1, 5):
        for k in range(3):
            pid = 1000 + f * 10 + k
            rows.append(_card(f, 10, "A", 20, "B", pid, "m", "Yellow Card")); pos_map[pid] = "MID"
        pid = 2000 + f
        rows.append(_card(f, 10, "A", 20, "B", pid, "d", "Yellow Card")); pos_map[pid] = "DEF"
    rows.append(_card(1, 10, "A", 20, "B", 999, "fw", "Yellow Card")); pos_map[999] = "FWD"
    profs = {p["position"]: p for p in cpa.derive_position_profiles(_ev(rows), pos_map)}
    assert profs["MID"]["card_risk_position"] == "alto" and profs["MID"]["cards_total"] == 12
    assert profs["DEF"]["card_risk_position"] == "bajo"
    # FWD has 1 card -> below POS_MIN_CARDS -> no determinado (insufficient), never inflated
    assert profs["FWD"]["card_risk_position"] == "no determinado"


# ---------------------------------------------------------------- §5 adjuster
def test_adjust_thin_referee_is_conservative():
    player = {"card_risk_player_history": "alto", "confidence": "media"}
    ref = {"card_environment": "alto", "confidence": "baja", "matches_sample": 1}
    r = cardadj.adjust_card_risk(0.20, player_profile=player, referee_context=ref)
    # referee alto but 1-match -> hard down-weight; total move stays small
    assert r["probability_card_adjusted"] <= 0.225
    assert "muestra baja" in r["adjustment_reason"]


def test_adjust_all_high_moderate_up():
    player = {"card_risk_player_history": "alto", "confidence": "media"}
    pos = {"card_risk_position": "alto", "confidence": "media"}
    team = {"card_environment_team": "alto", "confidence": "media"}
    ref = {"card_environment": "medio", "confidence": "media", "matches_sample": 5}
    r = cardadj.adjust_card_risk(0.20, player_profile=player, position_profile=pos,
                                 team_profile=team, referee_context=ref)
    assert r["adjustment_direction"] == "subir"
    # moderate: up but well within the clamp (never explosive)
    assert 0.20 < r["probability_card_adjusted"] <= 0.20 * cardadj.FACTOR_MAX
    assert r["probability_card_adjusted"] <= 0.26


def test_adjust_insufficient_is_neutral():
    r = cardadj.adjust_card_risk(0.20)
    assert r["adjustment_direction"] == "neutro"
    assert r["probability_card_adjusted"] == r["probability_card_original"] == 0.20


def test_adjust_never_zero_on_absence_of_cards():
    player = {"card_risk_player_history": "bajo", "confidence": "media"}
    r = cardadj.adjust_card_risk(0.20, player_profile=player)
    assert r["probability_card_adjusted"] > 0.0          # bajó pero NUNCA a cero
    assert r["adjustment_direction"] in ("bajar", "neutro")


def test_adjust_conflict_stays_conservative():
    player = {"card_risk_player_history": "alto", "confidence": "media"}
    team = {"card_environment_team": "bajo", "confidence": "media"}
    r = cardadj.adjust_card_risk(0.20, player_profile=player, team_profile=team)
    assert abs(r["probability_card_adjusted"] - 0.20) <= 0.02   # net small
    assert "conflicto" in r["adjustment_reason"]


def test_adjust_components_present():
    r = cardadj.adjust_card_risk(0.20, player_profile={"card_risk_player_history": "alto",
                                                       "confidence": "media"})
    comps = r["card_risk_components"]
    for k in ("player_history", "position_profile", "team_profile", "referee_profile"):
        assert k in comps and "direction" in comps[k] and "weight" in comps[k]


# ---------------------------------------------------------------- §6 builder integration
def test_apply_card_adjustment_injects_fields():
    card_profiles = {
        "players": {7: {"player_id": 7, "position": "DEF", "team_id": 10,
                        "card_risk_player_history": "alto", "confidence": "media"}},
        "teams": {10: {"team_id": 10, "card_environment_team": "alto", "confidence": "media"}},
        "positions": {"DEF": {"position": "DEF", "card_risk_position": "alto", "confidence": "media"}},
    }
    entries = [{"player": "Hard Tackler", "team": "A", "player_id": 7, "probability_card": 0.20,
                "confidence": "baja", "data_quality": "baja"}]
    ref = {"card_environment": "medio", "confidence": "media", "matches_sample": 4}
    out = bpe.apply_card_adjustment(entries, card_profiles, {}, {"A": 10}, ref)
    e = out[0]
    assert "probability_card_original" in e and "probability_card_adjusted" in e
    assert e["adjustment_direction"] == "subir"
    assert e["card_risk_components"]["player_history"]["label"] == "alto"


def test_apply_card_adjustment_keeps_original_when_no_data():
    entries = [{"player": "X", "team": "A", "player_id": 999, "probability_card": 0.20}]
    out = bpe.apply_card_adjustment(entries, {"players": {}, "teams": {}, "positions": {}}, {}, {}, {})
    assert out[0]["adjustment_direction"] == "neutro"
    assert out[0]["probability_card_adjusted"] == out[0]["probability_card_original"] == 0.20


# ---------------------------------------------------------------- §7 Telegram
def _obj_with_card_risk(card_risk):
    h = [core.expand_player({"player": "Striker H", "player_id": 1, "team": "H", "is_xi": 1,
                             "basis": "probable", "lam_goal": 0.5, "exp_shots": 3.0,
                             "lam_shot_on": 1.2, "lam_assist": 0.25, "p_card": 0.18})]
    a = [core.expand_player({"player": "Defender A", "player_id": 2, "team": "A", "is_xi": 1,
                             "basis": "probable", "lam_goal": 0.1, "exp_shots": 0.8,
                             "lam_shot_on": 0.3, "lam_assist": 0.05, "p_card": 0.30})]
    sp = core.set_piece_hierarchy([1], {1: "Striker H"})
    obj = core.build_player_predictions(
        {"fixture_id": 1, "home": "H", "away": "A", "round": "Group Stage - 1",
         "kickoff_utc": "2026-06-30 19:00"}, h, a, sp, sp, core.key_matchups(None, None),
        scenarios=core.scenario_delta(h + a, None))
    obj["player_predictions"]["card_risk"] = card_risk
    obj["team_context"] = {"p_home": 0.5, "p_draw": 0.25, "p_away": 0.25, "xg_home": 1.5,
                           "xg_away": 1.0, "top_score": "1-1", "exp_corners_total": 9.0,
                           "exp_cards_total": 4.0, "exp_sot_home": 5.0, "exp_sot_away": 3.0}
    obj["external_data_status"] = {}
    return obj


def test_telegram_shows_adjustment_and_motivo():
    cr = [{"player": "Defender A", "team": "A", "player_id": 2, "probability_card": 0.30,
           "probability_card_original": 0.30, "probability_card_adjusted": 0.34,
           "adjustment_direction": "subir",
           "adjustment_reason": "ajuste sube: posición DEF; equipo alto; árbitro con muestra baja",
           "confidence": "baja", "data_quality": "baja", "card_risk_components": {}}]
    msg = tg.render_fixture(_obj_with_card_risk(cr))
    assert "Riesgo de tarjeta" in msg
    assert "Defender A" in msg and "ajustado" in msg
    assert "Motivo:" in msg
    assert "Muestra baja" in msg                       # honest warning


def test_telegram_card_block_no_betting_language():
    cr = [{"player": "Defender A", "team": "A", "player_id": 2, "probability_card": 0.30,
           "probability_card_original": 0.30, "probability_card_adjusted": 0.30,
           "adjustment_direction": "neutro", "adjustment_reason": "historial bajo, ajuste neutro",
           "confidence": "baja", "data_quality": "baja", "card_risk_components": {}}]
    msg = tg.render_fixture(_obj_with_card_risk(cr))
    tg.assert_no_betting_language(msg)                 # raises if any betting word leaked


def test_telegram_backward_compatible_without_adjustment():
    # old-style entries (no adjusted fields) must still render
    cr = [{"player": "Defender A", "team": "A", "probability_card": 0.30}]
    msg = tg.render_fixture(_obj_with_card_risk(cr))
    assert "Defender A" in msg
    tg.assert_no_betting_language(msg)


# ---------------------------------------------------------------- §8 artifact round-trip
def test_build_writes_artifacts(tmp_path):
    ev = tmp_path / "events.csv"
    _ev([_card(1, 10, "A", 20, "B", 100, "Carder"),
         _card(2, 10, "A", 30, "C", 100, "Carder")]).to_csv(ev, index=False)
    out_csv = tmp_path / "out.csv"
    out_json = tmp_path / "out.json"
    out_txt = tmp_path / "out.txt"
    payload = cpa.build(ev, None, out_csv, out_json, out_txt, write=True)
    assert out_csv.exists() and out_json.exists() and out_txt.exists()
    assert payload["meta"]["players"] >= 1
    df = pd.read_csv(out_csv)
    assert list(df.columns) == cpa.CSV_COLUMNS
    assert "apuesta" not in out_txt.read_text(encoding="utf-8").lower()
