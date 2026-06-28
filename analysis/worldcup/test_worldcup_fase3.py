"""
Fase 3 offline tests (NO network, NO API, NO betting). Covers the external-context layer:
  * each adapter: CSV present+valid / absent / missing minimum columns -> ({}/None, reason)
  * expand_player with REAL xG/xA replacing proxy, and PARTIAL real (real only where present, proxy else)
  * set_piece_takers.csv feeding free-kicks/corners (source_priority_used)
  * referee context with sufficient sample / weather without strong impact / coach tactical profile
  * matchups with sufficient positional data and with insufficient data (heuristic_only)
  * Telegram render carries NO betting language and labels real vs proxy
  * every block exposes data_quality / confidence / reason
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402
import player_events_core as core  # noqa: E402
import referee_context as refctx  # noqa: E402
import weather_context as wxctx  # noqa: E402
import coach_tactical_context as coachctx  # noqa: E402
import player_matchups as pmatch  # noqa: E402
import build_worldcup_player_events as bpe  # noqa: E402
import build_worldcup_player_events_telegram as tg  # noqa: E402


# ============================================================ adapters: absent / invalid / valid
def test_adapters_absent_return_empty_reason(tmp_path):
    for loader in (adapters.load_player_xg_xa, adapters.load_set_piece_takers,
                   adapters.load_referee_profiles, adapters.load_weather_by_fixture,
                   adapters.load_coach_profiles, adapters.load_positional_profiles):
        data, reason = loader(tmp_path / "nope.csv")
        assert data == {} and isinstance(reason, str) and reason


def test_adapter_missing_columns_marks_invalid(tmp_path):
    p = tmp_path / "xg.csv"
    pd.DataFrame([{"player_id": 1, "xg90": 0.5}]).to_csv(p, index=False)  # missing xa90
    data, reason = adapters.load_player_xg_xa(p)
    assert data == {} and "faltan columnas" in reason and "xa90" in reason

    p2 = tmp_path / "sp.csv"
    pd.DataFrame([{"team_id": 1, "player_id": 2}]).to_csv(p2, index=False)  # missing role
    data2, reason2 = adapters.load_set_piece_takers(p2)
    assert data2 == {} and "faltan columnas" in reason2


def test_adapter_xg_xa_valid(tmp_path):
    p = tmp_path / "xg.csv"
    pd.DataFrame([{"player_id": 7, "xg90": 0.66, "xa90": 0.33, "shots90": 3.1, "sot90": 1.4,
                   "source": "FBref"}]).to_csv(p, index=False)
    data, reason = adapters.load_player_xg_xa(p)
    assert data[7]["xg90"] == 0.66 and data[7]["sot90"] == 1.4 and "real" in reason.lower()
    # an absent optional column is None, never fabricated
    assert data[7]["crosses90"] is None


def test_adapter_set_piece_takers_ranked(tmp_path):
    p = tmp_path / "sp.csv"
    pd.DataFrame([
        {"team_id": 5, "player_id": 10, "player_name": "PK1", "role": "penalty", "rank": 1, "attempts": 8},
        {"team_id": 5, "player_id": 11, "player_name": "PK2", "role": "penalty", "rank": 2, "attempts": 2},
        {"team_id": 5, "player_id": 12, "player_name": "CK", "role": "corner_left", "rank": 1, "attempts": 20},
        {"team_id": 5, "player_id": 13, "player_name": "Bad", "role": "throw_in", "rank": 1},  # unknown role
    ]).to_csv(p, index=False)
    data, reason = adapters.load_set_piece_takers(p)
    assert data[5]["penalty"][0]["player_name"] == "PK1"          # rank 1 first
    assert "corner_left" in data[5] and "throw_in" not in data[5]  # unknown role dropped


# ============================================================ core: real xG/xA replaces proxy
def _row(pid, lam_goal=0.2, exp_shots=1.0, lam_son=0.5, lam_assist=0.1, basis="probable_x"):
    return {"player": f"P{pid}", "player_id": pid, "team": "T", "is_xi": 1, "basis": basis,
            "lam_goal": lam_goal, "exp_shots": exp_shots, "lam_shot_on": lam_son,
            "lam_assist": lam_assist, "p_card": 0.1}


def test_expand_player_real_replaces_proxy():
    real = {"xg90": 0.9, "xa90": 0.5, "shots90": 4.0, "sot90": 2.0, "key_passes90": 2.5}
    e = core.expand_player(_row(1, lam_goal=0.2, exp_shots=1.0, lam_son=0.5, lam_assist=0.1), real=real)
    assert e["expected_goals"] == 0.9 and e["expected_assists"] == 0.5
    assert e["expected_sot"] == 2.0 and e["expected_shots"] == 4.0
    assert e["source_used"] == "real_xg_xa"
    assert e["goal_source"] == "real" and e["assist_source"] == "real" and e["shots_source"] == "real"
    assert "real" in e["reason"].lower()


def test_expand_player_partial_real_keeps_proxy_elsewhere():
    # only xg90 present -> goals real, assists/shots stay proxy and are flagged proxy
    e = core.expand_player(_row(2, lam_goal=0.2, lam_assist=0.1, lam_son=0.5), real={"xg90": 0.7})
    assert e["expected_goals"] == 0.7 and e["goal_source"] == "real"
    assert e["expected_assists"] == 0.1 and e["assist_source"] == "proxy"
    assert e["expected_sot"] == 0.5 and e["shots_source"] == "proxy"
    assert e["source_used"] == "real_xg_xa"   # at least one real field used


def test_expand_player_no_real_is_pure_proxy():
    e = core.expand_player(_row(3, lam_goal=0.3))
    assert e["source_used"] == "proxy" and e["goal_source"] == "proxy"
    assert e["expected_goals"] == 0.3


# ============================================================ set-piece priority (build module)
def test_csv_takers_fill_free_kicks_and_corners():
    csv_takers = {
        "direct_free_kick": [{"player_id": 21, "player_name": "FK", "rank": 1, "attempts": 5,
                              "confidence": "alta", "last_taken_date": "2026-06-10"}],
        "corner_left": [{"player_id": 22, "player_name": "CK", "rank": 1, "attempts": 9,
                         "confidence": "media", "last_taken_date": None}],
    }
    names = {21: "FK", 22: "CK"}
    xi = {21, 22, 23}
    block = bpe._csv_role_block(csv_takers, "direct_free_kicks", xi, names)
    assert block["primary"] == "FK" and block["source_priority_used"] == "set_piece_takers_csv"
    # a player NOT in the XI is not used (no fabrication)
    assert bpe._csv_role_block(csv_takers, "corners_left", {99}, names) is None


def test_build_set_piece_block_source_priority():
    # core block: penalties from REAL events (primary present), but NO free-kick/corner primaries
    core_block = {
        "penalties": {"primary": "RealPK", "secondary": None, "confidence": "alta", "reason": "x"},
        "direct_free_kicks": {"primary": None, "confidence": "baja", "reason": "sin evento"},
        "corners_left": {"primary": None, "confidence": "baja", "reason": "sin evento"},
        "corners_right": {"primary": None, "confidence": "baja", "reason": "sin evento"},
    }
    csv_takers = {"direct_free_kick": [{"player_id": 21, "player_name": "FK", "rank": 1,
                                        "attempts": 5, "confidence": "alta"}]}
    names = {21: "FK"}
    out = bpe.build_set_piece_block(core_block, csv_takers, {21}, names)
    assert out["penalties"]["source_priority_used"] == "eventos_reales_mundial"   # real events win
    assert out["direct_free_kicks"]["primary"] == "FK"
    assert out["direct_free_kicks"]["source_priority_used"] == "set_piece_takers_csv"
    assert "source_priority_used" in out and "reason" in out


# ============================================================ referee context
def test_referee_context_sufficient_sample():
    profiles = {"strict sam": {"referee_name": "Strict Sam", "matches": 40, "yellow_cards_pg": 5.2,
                               "red_cards_pg": 0.2, "penalties_pg": 0.35, "tournament_context": "elite",
                               "confidence": "alta"}}
    ctx = refctx.build_referee_context("Strict Sam", profiles, "loaded")
    assert ctx["referee_name"] == "Strict Sam"
    assert "alto" in ctx["expected_card_environment"]
    assert ctx["confidence"] == "media" and ctx["data_quality"] == "alta"
    assert ctx["reason"]


def test_referee_context_absent_degrades():
    ctx = refctx.build_referee_context(None, {}, "no configurado")
    assert ctx["referee_name"] is None and ctx["confidence"] == "baja"
    assert ctx["expected_card_environment"] == "no determinado" and ctx["reason"]


# ============================================================ weather context
def test_weather_no_strong_impact():
    wmap = {99: {"temperature": 22.0, "wind_speed": 10.0, "rain_probability": 0.05,
                 "pitch_condition": "seco", "confidence": "media"}}
    ctx = wxctx.build_weather_context(99, wmap, "loaded")
    assert ctx["extreme"] is False
    assert ctx["impact_on_tempo"] == "neutro" and ctx["impact_on_shots"] == "neutro"
    assert "normales" in ctx["reason"]


def test_weather_extreme_wind_flags_impact():
    wmap = {99: {"temperature": 20.0, "wind_speed": 45.0, "rain_probability": 0.0}}
    ctx = wxctx.build_weather_context(99, wmap, "loaded")
    assert ctx["extreme"] is True and ctx["impact_on_crosses"] != "neutro"


def test_weather_absent_degrades():
    ctx = wxctx.build_weather_context(1, {}, "clima no configurado")
    assert ctx["weather_summary"] == "no determinado" and ctx["confidence"] == "baja"


# ============================================================ coach tactical context
def test_coach_tactical_profile_builds_style():
    cmap = {7: {"coach_name": "Mr C", "base_formation": "4-3-3", "pressing_level": "alto",
                "defensive_block": "medio", "transition_speed": "alto", "width_usage": "bandas",
                "build_up_style": "corto", "set_piece_emphasis": "alto",
                "substitution_aggression": "alto", "knockout_risk_profile": "conservador",
                "confidence": "media", "source": "manual"}}
    ctx = coachctx.build_tactical_context(7, 8, "Home", "Away", cmap, "loaded")
    assert "4-3-3" in ctx["home_style"]["style"] and "presión alta" in ctx["home_style"]["style"]
    assert ctx["away_style"]["style"].startswith("estilo no determinado")  # team 8 has no profile
    assert ctx["expected_match_script"] and ctx["reason"]
    assert ctx["source"].startswith("manual")


# ============================================================ matchups
def _xi(ids, team):
    return [{"player_id": i, "player_name": f"{team}{i}", "team": team} for i in ids]


def test_matchups_sufficient_positional_data():
    pos = {
        1: {"position": "RW", "pace_threat": 0.9, "one_v_one": 0.8, "crossing_threat": 0.7},
        2: {"position": "ST", "pace_threat": 0.85, "aerial_threat": 0.5},
        11: {"position": "RB", "defensive_weight": 0.3},
        12: {"position": "CB", "pace_threat": 0.3, "aerial_threat": 0.4},
    }
    # adapter stores "1v1_threat" as key; map it through
    pos[1]["1v1_threat"] = pos[1].pop("one_v_one")
    home = _xi([1, 2], "H"); away = _xi([11, 12], "A")
    mu = pmatch.build_matchups(home, away, positional_map=pos)
    assert mu and not all(m.get("matchups_heuristic_only") for m in mu)
    zones = {m.get("zone") for m in mu}
    assert any("extremo vs lateral" in z for z in zones) or any("delantero" in z for z in zones)
    for m in mu:
        assert "confidence" in m and "reason" in m and "possible_effect_on_prediction" in m


def test_matchups_insufficient_data_heuristic_only():
    home = _xi([1, 2], "H"); away = _xi([3, 4], "A")
    mu = pmatch.build_matchups(home, away, positional_map={}, positional_reason="sin perfiles")
    assert len(mu) == 1 and mu[0]["matchups_heuristic_only"] is True
    assert mu[0]["confidence"] == "baja" and mu[0]["reason"]


# ============================================================ Telegram: no betting language + labels
def _synthetic_fixture(uses_real):
    src = "real_xg_xa" if uses_real else "proxy"
    return {
        "fixture": {"home": "H", "away": "A", "round": "Group", "kickoff_utc": "2026-06-20T18:00:00Z"},
        "data_quality": "media", "confidence": "media",
        "team_context": {"p_home": 0.5, "p_draw": 0.3, "p_away": 0.2, "xg_home": 1.6, "xg_away": 1.1,
                         "top_score": "1-1", "exp_corners_total": 9.5, "exp_cards_total": 4.0,
                         "exp_sot_home": 5.0, "exp_sot_away": 3.5},
        "external_data_status": {"xg_xa_available": uses_real, "referee_available": True,
                                 "weather_available": True, "coach_profile_available": True,
                                 "set_piece_available": True, "positional_profile_available": True},
        "referee_context": {"referee_name": "Strict Sam", "expected_card_environment": "alto",
                            "possible_penalty_environment": "en la media", "confidence": "media",
                            "data_quality": "alta", "reason": "perfil externo; 40 partidos"},
        "weather_context": {"weather_summary": "31°C, viento 12 km/h", "extreme": False,
                            "impact_on_tempo": "neutro", "impact_on_shots": "neutro",
                            "impact_on_crosses": "neutro", "impact_on_fatigue": "neutro",
                            "confidence": "media", "reason": "clima dentro de rangos normales"},
        "tactical_context": {"home_style": {"style": "formación base 4-3-3; presión alta"},
                             "away_style": {"style": "bloque bajo replegado"},
                             "expected_match_script": "presión alta contra bloque bajo",
                             "confidence": "media", "reason": "ambos perfiles externos"},
        "key_matchups": [{"player_a": "H1", "player_b": "A11", "zone": "extremo vs lateral",
                          "advantage": "H1", "confidence": "media", "reason": "x",
                          "possible_effect_on_prediction": "más centros"}],
        "player_predictions": {
            "likely_scorers": [{"player": "H2", "team": "H", "probability_goal": 0.4,
                                "expected_goals": 0.6, "source_used": src}],
            "likely_shots_on_target": [{"player": "H2", "team": "H", "probability_1_sot": 0.7,
                                        "expected_sot": 1.5, "source_used": src}],
            "likely_assisters": [{"player": "H1", "team": "H", "probability_assist": 0.25,
                                  "source_used": src}],
            "set_piece_takers": {
                "home": {"penalties": {"primary": "H2", "confidence": "alta",
                                       "source_priority_used": "eventos_reales_mundial"},
                         "direct_free_kicks": {"primary": "H1", "confidence": "media"},
                         "corners_left": {"primary": "H1", "confidence": "media"}},
                "away": {"penalties": {"primary": None, "confidence": "baja"},
                         "direct_free_kicks": {"primary": None, "confidence": "baja"},
                         "corners_left": {"primary": None, "confidence": "baja"}}},
            "card_risk": [{"player": "A11", "team": "A", "probability_card": 0.3}],
            "key_matchups": []},
    }


def test_telegram_render_no_betting_language_real():
    text = tg.render_fixture(_synthetic_fixture(uses_real=True))
    tg.assert_no_betting_language(text)                # raises if any betting word leaks
    assert "datos reales" in text and "Árbitro" in text and "Duelos clave" in text
    assert "Strict Sam" in text


def test_telegram_render_no_betting_language_proxy():
    text = tg.render_fixture(_synthetic_fixture(uses_real=False))
    tg.assert_no_betting_language(text)
    assert "proxy" in text.lower()
    assert "Avisos de datos" in text   # proxy -> a data warning is shown


def test_telegram_guard_catches_betting_word():
    with pytest.raises(AssertionError):
        tg.assert_no_betting_language("este es un value bet con buena cuota")
