"""
Offline tests for the KNOCKOUT display fixes in build_worldcup_full_card. NO network, NO API.

Covers: round chip in knockouts vs group chip in groups (FIX 1) · P(advance) heuristic line + draw
relabel ONLY in knockouts, sums coherent (FIX 3) · AET/PEN annotation in 'cómo acertamos ayer',
never inventing the penalty winner, 1X2 still 90' (FIX 2).

Run:  python analysis/worldcup/test_knockout_display.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_full_card as F  # noqa: E402


def _row(**kw):
    base = {"home": "Germany", "away": "Mexico", "kickoff_utc": "2026-07-04 20:00",
            "round": "Round of 16", "home_group": "Group E",
            "our_home": 0.56, "our_draw": 0.24, "our_away": 0.20,
            "our_xg_home": 1.8, "our_xg_away": 1.0}
    base.update(kw)
    return pd.Series(base)


# ---------------------------------------------------------------- FIX 1 round chip
def test_round_label_map():
    assert F.is_knockout("Round of 16") and not F.is_knockout("Group Stage - 3")
    assert F.round_label_es("Round of 32") == "Dieciseisavos"
    assert F.round_label_es("Round of 16") == "Octavos"
    assert F.round_label_es("Quarter-finals") == "Cuartos"
    assert F.round_label_es("Semi-finals") == "Semifinal"   # 'final' substring must NOT win
    assert F.round_label_es("3rd Place Final") == "3.º y 4.º puesto"
    assert F.round_label_es("Final") == "Final"


def test_chip_knockout_shows_round_not_group():
    line0 = F.match_block(_row(round="Round of 16", home_group="Group E"))[0]
    assert "Octavos" in line0 and "Gr. E" not in line0


def test_chip_group_unchanged():
    line0 = F.match_block(_row(round="Group Stage - 3", home_group="Group E"))[0]
    assert "Gr. E" in line0


# ---------------------------------------------------------------- FIX 3 advance line
def test_advance_line_only_in_knockout_and_sums():
    txt = "\n".join(F.match_block(_row(round="Round of 16")))
    assert "Empate a 90' (→ prórroga)" in txt
    assert "Avance" in txt and "moneda al aire" in txt
    # P(advance): home 0.56 + 0.24*0.5 = 0.68 -> 68% ; away 0.20 + 0.12 = 0.32 -> 32% (sum 100)
    assert "68%" in txt and "32%" in txt


def test_group_match_has_no_advance_line():
    txt = "\n".join(F.match_block(_row(round="Group Stage - 1")))
    assert "Avance" not in txt and "→ prórroga" not in txt
    assert "Empate 24%" in txt   # normal draw label in groups


# ---------------------------------------------------------------- FIX 2 AET/PEN annotation
def test_aet_annotation_names_extratime_winner():
    r = pd.Series({"result_status": "AET", "result_final_gh": 2, "result_final_ga": 1})
    s = F._ko_resolution_es(r, "Ale", "Mex")
    assert "2-1 tras prórroga" in s and "ganó Ale" in s


def test_pen_annotation_does_not_invent_winner():
    r = pd.Series({"result_status": "PEN", "result_final_gh": 1, "result_final_ga": 1})
    s = F._ko_resolution_es(r, "Ale", "Mex")
    assert "penaltis" in s and "Ale" not in s and "Mex" not in s   # winner not stored -> not invented


def test_ft_has_no_annotation():
    assert F._ko_resolution_es(pd.Series({"result_status": "FT"}), "A", "B") == ""
    assert F._ko_resolution_es(pd.Series({}), "A", "B") == ""


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} knockout-display tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
