"""
Regression tests for the inj_home/inj_away column-name collision that crashed the paginated card render
(build_worldcup_full_card.py) once knockout fixtures had published lineups.

ROOT CAUSE: build_worldcup_cards.py stored the injured-names DISPLAY string under inj_home/inj_away,
the SAME columns pred_1x2 reads as the injury-adjusted PROBABILITY. When the injury adjuster produced no
numeric probability, inj_home stayed a string and `f"{lh*100:.0f}"` raised
"ValueError: Unknown format code 'f' for object of type 'str'".

FIX (A): names live in inj_names_home/inj_names_away; inj_home/inj_away are probability-only.
FIX (B): pred_1x2 validates every probability candidate with _safe_prob (numeric in [0,1]) and ignores
non-numeric values, falling back to the next source — a string is NEVER returned as a probability.

NO betting, NO odds, NO market — pure render guards.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_worldcup_full_card as fc  # noqa: E402


# ---------------------------------------------------------------- safe coercion helpers
def test_safe_prob_rejects_non_numeric_and_out_of_range():
    assert fc._safe_prob("Pedri; Gavi") is None        # the exact bug value
    assert fc._safe_prob("") is None
    assert fc._safe_prob(None) is None
    assert fc._safe_prob(float("nan")) is None
    assert fc._safe_prob(1.5) is None                  # out of [0,1]
    assert fc._safe_prob(-0.1) is None
    assert fc._safe_prob(0.45) == 0.45
    assert fc._safe_prob(0.0) == 0.0 and fc._safe_prob(1.0) == 1.0


def test_safe_num_allows_xg_but_rejects_strings():
    assert fc._safe_num("1.8") == 1.8                  # numeric string ok for xG
    assert fc._safe_num(1.8) == 1.8
    assert fc._safe_num("not a number") is None
    assert fc._safe_num(None) is None


# ---------------------------------------------------------------- pred_1x2 behaviour
def _row(**kw):
    base = {"home": "Spain", "away": "Brazil", "round": "Round of 32",
            "kickoff_utc": "2026-06-29 19:00"}
    base.update(kw)
    return pd.Series(base)


def test_pred_1x2_ignores_names_string_and_falls_back():
    # inj_home holds the injured-NAMES string (the bug); must fall back to the numeric mx_* source.
    r = _row(inj_home="Pedri; Gavi", inj_away="", inj_draw="",
             mx_home=0.45, mx_draw=0.27, mx_away=0.28, mx_xg_home=1.6, mx_xg_away=1.2)
    lh, ld, la, xgh, xga, _note = fc.pred_1x2(r)
    assert lh == 0.45 and ld == 0.27 and la == 0.28    # used mx_*, NOT the string
    assert not isinstance(lh, str)


def test_pred_1x2_uses_inj_probability_when_numeric():
    # the CORRECT use: inj_home is a valid probability -> it wins (highest priority in the chain).
    r = _row(inj_home=0.50, inj_draw=0.25, inj_away=0.25, inj_xg_home=1.7, inj_xg_away=1.0,
             mx_home=0.45, mx_draw=0.27, mx_away=0.28)
    lh, ld, la, *_ = fc.pred_1x2(r)
    assert (lh, ld, la) == (0.50, 0.25, 0.25)


def test_pred_1x2_all_sources_invalid_returns_none():
    r = _row(inj_home="x", mx_home="y", our_home=None)
    assert fc.pred_1x2(r) == (None, None, None, None, None, None)


# ---------------------------------------------------------------- match_block must not crash
def test_match_block_no_crash_on_knockout_names_string():
    # exact reproduction of the CI failure: knockout fixture, inj_home = names string.
    r = _row(inj_home="Pedri; Gavi", inj_away="", inj_draw="", inj_note="",
             mx_home=0.45, mx_draw=0.27, mx_away=0.28,
             our_home=0.44, our_draw=0.28, our_away=0.28)
    lines = fc.match_block(r)                            # would raise ValueError before the fix
    assert any("Resultado a 90'" in ln for ln in lines)
    assert any("45%" in ln for ln in lines)             # rendered the numeric fallback


def test_inj_names_column_does_not_pollute_probability():
    # the injured-names DISPLAY string now lives in inj_names_*; inj_home stays a clean probability,
    # so pred_1x2 returns the numeric value and match_block renders without crashing.
    r = _row(inj_names_home="Pedri; Gavi", inj_names_away="Neymar",
             inj_home=0.50, inj_draw=0.25, inj_away=0.25,
             mx_home=0.45, mx_draw=0.27, mx_away=0.28)
    lh = fc.pred_1x2(r)[0]
    assert lh == 0.50 and not isinstance(lh, str)        # inj_home probability, NOT the names
    lines = fc.match_block(r)
    assert any("Resultado a 90'" in ln for ln in lines)


def test_compact_render_reads_names_from_inj_names(tmp_path, monkeypatch, capsys):
    # the compact lineups view reads injured names from inj_names_* (build_worldcup_cards writes them
    # there). A names string in inj_names_* must render fine and never reach a numeric format.
    cards = tmp_path / "cards.csv"
    pd.DataFrame([{
        "fixture_id": 1, "kickoff_utc": "2026-06-29 19:00", "home": "Spain", "away": "Brazil",
        "round": "Round of 32", "mx_home": 0.45, "mx_draw": 0.27, "mx_away": 0.28,
        "mx_xg_home": 1.6, "mx_xg_away": 1.2, "lineup_home": "prob", "lineup_away": "prob",
        "inj_names_home": "Pedri; Gavi", "inj_names_away": "Neymar",
    }]).to_csv(cards, index=False)
    monkeypatch.setattr(fc, "CARDS", cards)
    fc.main("2026-06-29", "2026-06-30", limit=10, compact=True, show_lineups=True)
    text = capsys.readouterr().out
    assert "Pedri" in text                               # names shown from inj_names_*
