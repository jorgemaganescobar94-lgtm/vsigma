"""
Fase 4E offline tests (NO network, NO API, NO scraping, NO betting, NO writes to data/external).
Cover the auto referee-profile derivation from REAL events, the manual>auto>none priority in
referee_context, and the Telegram referee block (sample + low-sample warning, no betting language).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import build_worldcup_referee_profiles_auto as refauto  # noqa: E402
import referee_context as refctx  # noqa: E402
import player_events_core as core  # noqa: E402
import build_worldcup_player_events_telegram as tg  # noqa: E402


def _events(rows):
    cols = ["fixture_id", "team_id", "card_type", "is_card", "is_penalty_goal", "is_penalty_miss"]
    return pd.DataFrame([{c: r.get(c) for c in cols} for r in rows], columns=cols)


def _yellow(fid, team_id):
    return {"fixture_id": fid, "team_id": team_id, "card_type": "Yellow Card", "is_card": 1,
            "is_penalty_goal": 0, "is_penalty_miss": 0}


def _pen_goal(fid, team_id):
    return {"fixture_id": fid, "team_id": team_id, "card_type": "", "is_card": 0,
            "is_penalty_goal": 1, "is_penalty_miss": 0}


# ---------------------------------------------------------------- derivation
def test_referee_with_events_gets_cards():
    refs = {1: "Ref A"}
    ev = _events([_yellow(1, 10), _yellow(1, 20), _yellow(1, 10)])
    profs = refauto.derive_referee_profiles(refs, ev)
    p = profs[0]
    assert p["referee_name"] == "Ref A"
    assert p["matches"] == 1 and p["fixtures"] == 1
    assert p["yellow_cards_total"] == 3 and p["cards_total"] == 3
    assert p["cards_pg"] == 3.0
    assert p["confidence"] == "baja"                 # 1 match -> baja (spec §3)
    assert "no extrapolar" in p["reason"]
    assert p["source"] == "worldcup_events_auto"


def test_referee_without_events_is_undetermined():
    refs = {2: "Ref B"}
    ev = _events([_yellow(99, 10)])                  # events only for an unrelated fixture
    profs = refauto.derive_referee_profiles(refs, ev)
    p = profs[0]
    assert p["matches"] == 0 and p["fixtures"] == 1
    assert p["card_environment"] == "no determinado"
    assert p["confidence"] == "no determinado"
    assert p["cards_pg"] is None                     # never a hard 0.0 presented as real


def test_penalty_detected_from_events():
    refs = {1: "Ref P"}
    ev = _events([_yellow(1, 10), _pen_goal(1, 10)])
    p = refauto.derive_referee_profiles(refs, ev)[0]
    assert p["penalties_total"] == 1 and p["matches_with_penalty"] == 1
    assert p["penalty_match_rate"] == 1.0
    # 1 match is too thin for a penalty tendency -> conservative "no determinado"
    assert p["penalty_environment"] == "no determinado"


def test_penalty_environment_with_enough_matches():
    refs = {1: "Ref Q", 2: "Ref Q", 3: "Ref Q", 4: "Ref Q"}
    ev = _events([_pen_goal(1, 10), _pen_goal(2, 10), _pen_goal(3, 10), _pen_goal(4, 10)])
    p = refauto.derive_referee_profiles(refs, ev)[0]
    assert p["matches"] == 4 and p["matches_with_penalty"] == 4
    assert p["penalty_environment"] == "alto"        # 4 matches, every one a penalty


def test_home_away_cards_split():
    refs = {1: "Ref H"}
    ev = _events([_yellow(1, 10), _yellow(1, 10), _yellow(1, 20)])   # 2 home, 1 away
    home_away = {1: (10, 20)}
    p = refauto.derive_referee_profiles(refs, ev, home_away)[0]
    assert p["home_cards_total"] == 2 and p["away_cards_total"] == 1
    assert p["home_cards_pg"] == 2.0 and p["away_cards_pg"] == 1.0


def test_home_away_none_when_ids_unknown():
    refs = {1: "Ref H"}
    ev = _events([_yellow(1, 10)])
    p = refauto.derive_referee_profiles(refs, ev, home_away={})[0]   # no home/away ids
    assert p["home_cards_total"] is None and p["away_cards_pg"] is None


# ---------------------------------------------------------------- referee_context priority
def test_manual_profile_overrides_auto():
    manual = {"strict sam": {"referee_name": "Strict Sam", "matches": 40, "yellow_cards_pg": 5.2,
                             "red_cards_pg": 0.2, "penalties_pg": 0.35, "source": "manual_table"}}
    auto = {"strict sam": {"referee_name": "Strict Sam", "matches": 1, "card_environment": "bajo",
                           "penalty_environment": "no determinado", "confidence": "baja",
                           "data_quality": "baja", "yellow_cards_pg": 1.0, "reason": "solo 1 partido"}}
    ctx = refctx.build_referee_context("Strict Sam", manual, "loaded", auto, "auto loaded")
    assert ctx["profile_source"] == "manual_table"           # manual wins
    assert "alto" in ctx["expected_card_environment"]        # uses the 40-match manual rate
    assert ctx["matches_sample"] == 40


def test_auto_profile_used_when_manual_empty():
    auto = {"ref auto": {"referee_name": "Ref Auto", "matches": 5, "card_environment": "alto",
                         "penalty_environment": "medio", "confidence": "media", "data_quality": "media",
                         "yellow_cards_pg": 5.6, "red_cards_pg": 0.2, "penalties_pg": 0.2,
                         "reason": "5 partidos con eventos reales — muestra media"}}
    ctx = refctx.build_referee_context("Ref Auto", {}, "manual vacío", auto, "auto loaded")
    assert ctx["profile_source"] == "worldcup_events_auto"
    assert ctx["card_environment"] == "alto"
    assert ctx["matches_sample"] == 5 and ctx["confidence"] == "media"
    assert "Mundial auto" in ctx["expected_card_environment"]


def test_context_exposes_sample_confidence_reason():
    auto = {"thin ref": {"referee_name": "Thin Ref", "matches": 1, "card_environment": "alto",
                         "penalty_environment": "no determinado", "confidence": "baja",
                         "data_quality": "baja", "yellow_cards_pg": 6.0,
                         "reason": "solo 1 partido, no extrapolar fuerte"}}
    ctx = refctx.build_referee_context("Thin Ref", {}, "manual vacío", auto, "auto")
    assert ctx["matches_sample"] == 1
    assert ctx["confidence"] == "baja"
    assert "no extrapolar" in ctx["reason"] and "Mundial auto" in ctx["reason"]


def test_context_none_when_no_profile_anywhere():
    ctx = refctx.build_referee_context("Nobody", {}, "manual vacío", {}, "auto vacío")
    assert ctx["referee_name"] is None or ctx["card_environment"] == "no determinado"
    assert ctx["confidence"] == "baja"


# ---------------------------------------------------------------- Telegram render
def _obj_with_referee(referee_ctx):
    h = [core.expand_player({"player": "Striker H", "player_id": 1, "team": "H", "is_xi": 1,
                             "basis": "probable", "lam_goal": 0.5, "exp_shots": 3.0,
                             "lam_shot_on": 1.2, "lam_assist": 0.25, "p_card": 0.18})]
    a = [core.expand_player({"player": "Defender A", "player_id": 2, "team": "A", "is_xi": 1,
                             "basis": "probable", "lam_goal": 0.1, "exp_shots": 0.8,
                             "lam_shot_on": 0.3, "lam_assist": 0.05, "p_card": 0.30})]
    sp = core.set_piece_hierarchy([1], {1: "Striker H"}, penalty_history={1: 3})
    obj = core.build_player_predictions(
        {"fixture_id": 1, "home": "H", "away": "A", "round": "Group Stage - 1",
         "kickoff_utc": "2026-06-30 19:00"}, h, a, sp, sp, core.key_matchups(None, None),
        scenarios=core.scenario_delta(h + a, None))
    obj["team_context"] = {"p_home": 0.55, "p_draw": 0.25, "p_away": 0.20, "xg_home": 1.8,
                           "xg_away": 0.9, "top_score": "2-0", "exp_corners_total": 9.0,
                           "exp_cards_total": 4.0, "exp_sot_home": 6.0, "exp_sot_away": 3.0}
    obj["referee_context"] = referee_ctx
    obj["external_data_status"] = {"referee_available": True}
    return obj


def test_telegram_shows_referee_with_sample_and_warning():
    ctx = refctx.build_referee_context("Thin Ref", {}, "manual vacío",
        {"thin ref": {"referee_name": "Thin Ref", "matches": 1, "card_environment": "alto",
                      "penalty_environment": "no determinado", "confidence": "baja",
                      "data_quality": "baja", "yellow_cards_pg": 6.0,
                      "reason": "solo 1 partido, no extrapolar fuerte"}}, "auto")
    msg = tg.render_fixture(_obj_with_referee(ctx))
    assert "Árbitro: Thin Ref" in msg
    assert "Muestra: 1 partido" in msg
    assert "Muestra baja" in msg                              # honest low-sample warning
    assert "Mundial auto" in msg


def test_telegram_referee_block_has_no_betting_language():
    ctx = refctx.build_referee_context("Ref Auto", {}, "manual vacío",
        {"ref auto": {"referee_name": "Ref Auto", "matches": 6, "card_environment": "alto",
                      "penalty_environment": "alto", "confidence": "alta", "data_quality": "alta",
                      "yellow_cards_pg": 6.0, "penalties_pg": 0.5,
                      "reason": "6 partidos con eventos reales"}}, "auto")
    msg = tg.render_fixture(_obj_with_referee(ctx))
    tg.assert_no_betting_language(msg)                        # raises if any betting word leaked
    assert "Árbitro: Ref Auto" in msg


# ---------------------------------------------------------------- artifact build (round-trip)
def test_build_writes_artifacts(tmp_path):
    refs = tmp_path / "fixture_referees.csv"
    pd.DataFrame([{"fixture_id": 1, "referee_name": "Ref A"}]).to_csv(refs, index=False)
    ev = tmp_path / "events.csv"
    _events([_yellow(1, 10), _yellow(1, 20)]).to_csv(ev, index=False)
    out_csv = tmp_path / "out.csv"
    out_json = tmp_path / "out.json"
    out_txt = tmp_path / "out.txt"
    profs = refauto.build(refs, ev, tmp_path / "nostore", out_csv, out_json, out_txt, write=True)
    assert len(profs) == 1 and out_csv.exists() and out_json.exists() and out_txt.exists()
    df = pd.read_csv(out_csv)
    assert list(df.columns) == refauto.CSV_COLUMNS
    assert "apuesta" not in out_txt.read_text(encoding="utf-8").lower()
