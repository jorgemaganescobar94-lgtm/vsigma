"""
Offline tests for the qualification engine (qual_engine) and its use as the INFORMATION line in the
ficha (build_worldcup_cards.compute_group_info + build_worldcup_full_card render). NO network, NO API.

Covers: the engine classifies the canonical scenarios correctly (qualified / draw_enough / must_win /
depends_on_others / eliminated / alive_as_third) · best thirds depend on format (6 groups -> thirds) ·
compute_group_info builds the line for a last-matchday 4-team group and is None otherwise (knockout,
not-last-matchday, missing) · the ficha shows 'Contexto de grupo' ONLY for groups and labels it as
INFORMATION (not the prediction).

Run:  python analysis/worldcup/test_qual_engine.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qual_engine as Q                  # noqa: E402
import build_worldcup_cards as BC        # noqa: E402
import build_worldcup_full_card as F     # noqa: E402


def _tbl(rows):
    # rows: [(key, pts)]
    return {k: {"pts": p, "played": 2} for k, p in rows}


# ----------------------------------------------------------------- engine
def test_qualified_certain():
    g = _tbl([("A", 6), ("B", 2), ("C", 1), ("D", 1)])
    _, lab = Q.classify_team(g, "A", "B", "A", [g], 8)
    assert lab == "qualified"


def test_draw_enough():
    g = _tbl([("A", 4), ("B", 3), ("C", 1), ("D", 1)])
    _, lab = Q.classify_team(g, "A", "B", "A", [g], 8)
    assert lab == "draw_enough"


def test_must_win():
    g = _tbl([("A", 3), ("B", 3), ("C", 1), ("D", 1)])
    _, lab = Q.classify_team(g, "A", "B", "A", [g], 8)
    assert lab == "must_win"


def test_depends_on_others():
    g = _tbl([("A", 3), ("B", 3), ("C", 3), ("D", 0)])
    _, lab = Q.classify_team(g, "A", "B", "A", [g], 8)
    assert lab in ("depends_on_others", "gd_dependent")


def test_eliminated_certain_last():
    g = _tbl([("A", 6), ("B", 6), ("C", 4), ("T", 0)])
    _, lab = Q.classify_team(g, "T", "C", "T", [g], 6)   # T can't be top-2 nor 3rd -> eliminated
    assert lab == "eliminated"


def test_alive_as_third_only_with_thirds_format():
    # 3rd by points: with 6-group format (thirds advance) -> alive_as_third; with 8-group (no thirds)
    # the same team is NOT alive_as_third (would be eliminated/neutral).
    g = _tbl([("A", 6), ("B", 6), ("C", 1), ("D", 1)])
    _, lab6 = Q.classify_team(g, "C", "D", "C", [g], 6)
    _, lab8 = Q.classify_team(g, "C", "D", "C", [g], 8)
    assert lab6 == "alive_as_third"
    assert lab8 != "alive_as_third"


def test_unknown_when_not_4_team():
    g = _tbl([("A", 3), ("B", 3), ("C", 0)])
    _, lab = Q.classify_team(g, "A", "B", "A", [g], 8)
    assert lab == "unknown"


# ----------------------------------------------------------------- compute_group_info (live line)
def _ctx_groups(played=2):
    # build_status_maps-shaped: group name -> [ {name, points, played, gd} ]
    return {"Group A": [{"name": "A", "points": 4, "played": played, "gd": 2},
                        {"name": "B", "points": 3, "played": played, "gd": 0},
                        {"name": "C", "points": 1, "played": played, "gd": -1},
                        {"name": "D", "points": 1, "played": played, "gd": -1}]}


def test_group_info_builds_for_last_matchday():
    s = BC.compute_group_info(_ctx_groups(played=2), "A", "B")
    assert s and "A le vale el empate" in s and "B" in s


def test_group_info_none_when_not_last_matchday():
    assert BC.compute_group_info(_ctx_groups(played=1), "A", "B") is None   # rem>1 -> no line


def test_group_info_none_when_teams_not_in_a_group():
    assert BC.compute_group_info(_ctx_groups(), "A", "ZZ") is None


# ----------------------------------------------------------------- ficha render
def _row(**kw):
    base = {"home": "A", "away": "B", "round": "Group Stage - 3", "kickoff_utc": "2026-06-26 20:00",
            "home_group": "A", "away_group": "A",
            "our_home": 0.45, "our_draw": 0.30, "our_away": 0.25,
            "our_xg_home": 1.4, "our_xg_away": 1.1, "our_elo_home": 0.3, "our_elo_away": -0.1}
    base.update(kw)
    return pd.Series(base)


def test_ficha_shows_group_info_for_groups():
    txt = "\n".join(F.match_block(_row(group_info="A le vale el empate · B debe ganar")))
    assert "Contexto de grupo" in txt and "información, no es la predicción" in txt
    assert "A le vale el empate" in txt


def test_ficha_hides_group_info_in_knockout():
    txt = "\n".join(F.match_block(_row(round="Round of 16", group_info="X ya clasificado")))
    assert "Contexto de grupo" not in txt          # knockout -> no group context line


def test_ficha_no_group_info_when_absent():
    txt = "\n".join(F.match_block(_row()))
    assert "Contexto de grupo" not in txt


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} qual-engine tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
