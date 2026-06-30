"""
Offline tests for the World Cup player-events glue + Telegram report. No network, no API, no betting.
Covers: the §13 Telegram message has the required football sections and NO betting language, the
betting-language guard actually fires, and the builder degrades cleanly when there are no overlapping
player rows (empty -> no spam).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "players"))

import player_events_core as core  # noqa: E402
import build_worldcup_player_events_telegram as tg  # noqa: E402


def _fixture_obj():
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
    obj["xa_source"] = "no configurada"
    obj["adapters_status"] = {"xa90": False, "referee_card_rates": False, "weather": False}
    return obj


def test_telegram_has_required_sections():
    msg = tg.render_fixture(_fixture_obj())
    for needle in ("Resultado:", "Marcador más probable", "Tiros a puerta esp", "Córners esp",
                   "Más probables para marcar", "Más probables para tirar a puerta",
                   "Más probables para asistir", "Balón parado", "Riesgo de tarjeta",
                   "Guion probable", "Confianza"):
        assert needle in msg, f"falta sección: {needle}"
    assert "Striker H" in msg                      # set-piece taker surfaced (had history)
    assert "no es consejo de juego" in msg


def test_telegram_has_no_betting_language():
    msg = tg.render_fixture(_fixture_obj())
    low = msg.lower()
    for bad in ("cuota", "odds", "edge", "pick", "stake", "roi", "mercado", "apostar"):
        assert bad not in low


def test_betting_guard_fires():
    with pytest.raises(AssertionError):
        tg.assert_no_betting_language("Mejor pick con cuota 2.0 y edge alto")


# ---- whole-word guard (\b): real betting jargon still caught; benign substrings no longer false-positive
@pytest.mark.parametrize("word", [w for w in tg.FORBIDDEN if " " not in w])
def test_guard_catches_real_betting_word_standalone(word):
    """Every single-word FORBIDDEN token still fires when it appears as a STANDALONE word."""
    with pytest.raises(AssertionError):
        tg.assert_no_betting_language(f"texto previo {word} texto posterior")


@pytest.mark.parametrize("phrase", [w for w in tg.FORBIDDEN if " " in w])
def test_guard_catches_real_betting_phrase(phrase):
    """Multi-word FORBIDDEN phrases ('value bet', 'casa de apuestas'…) still fire."""
    with pytest.raises(AssertionError):
        tg.assert_no_betting_language(f"esto es un {phrase} claro")


@pytest.mark.parametrize("benign", [
    "J. Pickford",        # 'pick' inside the England GK surname (the real false positive)
    "Charles Pickel",     # 'pick' inside the Switzerland midfielder surname
    "una mistake táctica",  # 'stake' inside 'mistake'
    "un gol heroico",     # 'roi' inside 'heroico'
    "hizo un hedge",      # 'edge' inside 'hedge'
])
def test_guard_does_not_fire_on_benign_substrings(benign):
    """Benign words that merely CONTAIN a forbidden token (player surnames, common words) must pass."""
    tg.assert_no_betting_language(benign)            # must NOT raise


def test_clean_player_events_message_passes_guard():
    """A normal rendered player-events fixture (which contains player names) passes the guard."""
    msg = tg.render_fixture(_fixture_obj())          # render_fixture asserts internally
    tg.assert_no_betting_language(msg)               # explicit: must NOT raise
    # and a Pickford-style name embedded in a realistic line is fine
    tg.assert_no_betting_language("  J. Pickford vs volumen de tiro de Congo DR (portero) [baja]")


def test_match_script_from_own_numbers():
    assert "dominio del local" in tg.match_script({"p_home": 0.6, "p_away": 0.2,
                                                   "xg_home": 1.8, "xg_away": 1.6})
    assert "bloque bajo" in tg.match_script({"p_home": 0.34, "p_away": 0.33,
                                             "xg_home": 0.9, "xg_away": 0.8})


def test_builder_empty_when_no_overlap(tmp_path, monkeypatch):
    # an events json with a fixture that has no ranked players -> no messages (no spam)
    import json
    empty = [{"fixture": {"home": "H", "away": "A"}, "player_predictions":
              {"likely_scorers": [], "likely_shots_on_target": [], "likely_assisters": [],
               "set_piece_takers": {}, "card_risk": [], "key_matchups": []}}]
    p = tmp_path / "ev.json"
    p.write_text(json.dumps(empty), encoding="utf-8")
    monkeypatch.setattr(tg, "MANIFEST", tmp_path / "man.txt")
    monkeypatch.setattr(tg, "COMBINED", tmp_path / "comb.txt")
    monkeypatch.setattr(tg, "HERE", tmp_path)
    assert tg.main(p) == 0
