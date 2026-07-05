"""
Regression for the Telegram dispatcher line-cut vs the WC clean card. NO network, NO API.

Bug: scripts/dispatch_telegram_alert.py used to clip every body to 25 lines ('corto para movil').
WC fixtures WITH the 👥 Jugadores section exceed 25 lines (worse in knockouts, +1 for the '🏅 Avanza'
line) -> the tail (📈 Córners/tiros + the ℹ️ footer/Atribución) got dropped when SENT, even though the
RAW block from _match_block_clean is complete. Fix (opción A): dispatcher gained an OPTIONAL --max-lines
(default 25 = unchanged for every other caller); the WC send step passes --max-lines 60.

These tests: (1) render a KNOCKOUT fixture WITH props, apply the dispatcher's clip with max_lines=60 ->
córners/tiros AND the footer survive; with the default 25 they do NOT (the bug) -> 60 fixes it.
(2) regression: clip_body default is 25 and a 30-line body still clips to 25 (historic behaviour intact).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import build_worldcup_full_card as F  # noqa: E402
import dispatch_telegram_alert as D  # noqa: E402


def _ko_row_with_props():
    """A KNOCKOUT fixture row that has props (via the props cache) + córners/tiros + xg, so the block
    contains ALL sections (headline+Avanza, goles, 👥 Jugadores, 📈 Córners/tiros, footer)."""
    F._props_cache = pd.DataFrame([
        {"fixture_id": -9001, "team": "Germany", "player": "K. Havertz", "is_xi": 1,
         "basis": "probable_xi", "p_goal": 0.29, "p_assist": 0.13, "p_card": 0.10, "exp_shots": 3.1},
        {"fixture_id": -9001, "team": "Germany", "player": "J. Musiala", "is_xi": 1,
         "basis": "probable_xi", "p_goal": 0.26, "p_assist": 0.15, "p_card": 0.08, "exp_shots": 2.7},
        {"fixture_id": -9001, "team": "Mexico", "player": "E. Álvarez", "is_xi": 1,
         "basis": "probable_xi", "p_goal": 0.10, "p_assist": 0.09, "p_card": 0.22, "exp_shots": 1.4},
    ])
    return pd.Series({
        "fixture_id": -9001, "home": "Mexico", "away": "England", "round": "Round of 16",
        "kickoff_utc": "2026-07-05 20:00", "our_elo_home": 1.2, "our_elo_away": 1.5,
        "fd_home": 0.32, "fd_draw": 0.26, "fd_away": 0.42, "fd_xg_home": 1.2, "fd_xg_away": 1.3,
        "st_corners_home": 4.5, "st_corners_away": 5.1, "st_shots_home": 11.0, "st_shots_away": 13.0})


def test_ko_props_block_survives_dispatcher_with_max_lines_60():
    F.CLEAN_FORMAT = True
    F.EXPLAIN_PER_METRIC = True
    F.N_SCORELINES = 6
    block = F.match_block(_ko_row_with_props())
    body = "\n".join(block)
    # RAW block is complete (sanity: this is NOT a _match_block_clean bug)
    assert "📈 Córners/tiros" in body
    assert "ℹ️ Modelo propio de selecciones" in body and "Atribución:" in body
    assert len(block) > 25   # a knockout props block genuinely exceeds the historic 25-line cap

    # WITH the fix (--max-lines 60): córners/tiros AND footer/Atribución survive the send
    sent60 = D.clip_body(body, 60)
    assert "📈 Córners/tiros" in sent60
    assert "ℹ️ Modelo propio de selecciones" in sent60 and "Atribución:" in sent60

    # WITHOUT the fix (historic default 25): the tail is dropped -> proves 60 is what fixes it
    sent25 = D.clip_body(body, 25)
    assert "📈 Córners/tiros" not in sent25
    assert "Atribución:" not in sent25


def test_dispatcher_default_is_25_backward_compatible():
    """Regression: the default is 25 and clips a 30-line body to exactly 25 (every caller that does not
    pass --max-lines keeps the previous 'corto para movil' behaviour)."""
    import inspect
    assert inspect.signature(D.clip_body).parameters["max_lines"].default == 25
    thirty = "\n".join(f"linea {i}" for i in range(1, 31))
    clipped = D.clip_body(thirty, 25)              # default value, explicit
    assert clipped.count("\n") + 1 == 25
    assert "linea 25" in clipped and "linea 26" not in clipped
    # and the shared default matches the CLI default (no silent drift)
    assert D.clip_body(thirty, 25) == D.clip_body(thirty)


def test_max_lines_zero_means_no_clip():
    body = "\n".join(f"l{i}" for i in range(1, 41))
    assert D.clip_body(body, 0) == body           # 0 -> sin recorte
