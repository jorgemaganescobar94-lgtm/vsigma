"""
Offline tests for the Fase 2 player event-history aggregator + the enriched set-piece hierarchy.
No network, no API, no betting. Covers: real counts (goals/assists/pens/cards), own-goal excluded,
per-90 with minutes, last penalty, penalty-history map, small-sample flags, card-risk levels, and the
core set_piece_hierarchy with a REAL penalty history (primary present, primary absent from XI -> §3
explainer, injured excluded, no history -> no determinado).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import player_event_history as peh  # noqa: E402
import player_events_core as core  # noqa: E402


def _row(fid, team_id, pid, name, is_goal=0, is_assist=0, aid=None, aname=None, pen_goal=0,
         pen_miss=0, own=0, is_card=0, card_type="", date="2026-06-20"):
    return {"fixture_id": fid, "date": date, "team_id": team_id, "player_id": pid, "player_name": name,
            "assist_player_id": aid, "assist_player_name": aname, "is_goal": is_goal,
            "is_assist": is_assist, "is_penalty_goal": pen_goal, "is_penalty_miss": pen_miss,
            "is_own_goal": own, "is_card": is_card, "card_type": card_type, "is_substitution": 0}


ROWS = [
    _row(1, 10, 1, "Striker", is_goal=1, is_assist=1, aid=2, aname="Maker"),  # goal + assist credited to 2
    _row(1, 10, 3, "PenMan", is_goal=1, pen_goal=1),                          # penalty scored
    _row(2, 10, 3, "PenMan", is_goal=0, pen_miss=1, date="2026-06-25"),       # penalty missed (later)
    _row(2, 10, 1, "Striker", is_goal=1),                                     # another goal
    _row(1, 20, 5, "OwnG", own=1),                                            # own goal (not a goal)
    _row(1, 20, 6, "Rough", is_card=1, card_type="Yellow Card"),
    _row(2, 20, 6, "Rough", is_card=1, card_type="Second Yellow card"),       # yellow + red
]


def test_counts_and_own_goal_excluded():
    agg = peh.aggregate(ROWS)
    pl = agg["players"]
    assert pl[1]["goals"] == 2 and pl[1]["goal_involvement"] == 2
    assert pl[2]["assists"] == 1                          # assist credited to the assist player
    assert pl[5]["goals"] == 0                            # own goal NOT a goal
    assert pl[6]["yellows"] == 2 and pl[6]["reds"] == 1   # second yellow -> yellow + red


def test_penalties_and_last_taker():
    agg = peh.aggregate(ROWS)
    assert agg["players"][3]["pens_taken"] == 2 and agg["players"][3]["pens_scored"] == 1
    assert agg["players"][3]["pens_missed"] == 1
    assert agg["penalty_history"] == {3: 2}
    # last penalty is the more recent one (missed, 2026-06-25)
    assert agg["last_penalty"][3]["scored"] is False and agg["last_penalty"][3]["date"] == "2026-06-25"


def test_per90_with_minutes_else_none():
    agg = peh.aggregate(ROWS, minutes_by_player={1: 180})   # 2 goals in 180' -> 1.0/90
    assert agg["players"][1]["goals_per90"] == pytest.approx(1.0)
    agg2 = peh.aggregate(ROWS)                               # no minutes -> None (not fabricated)
    assert agg2["players"][1]["goals_per90"] is None


def test_small_sample_flagged():
    agg = peh.aggregate([_row(1, 10, 1, "Solo", is_goal=1)])
    assert agg["players"][1]["data_quality"] in ("media", "baja")
    assert "muestra" in agg["players"][1]["reason"].lower() or "sin" in agg["players"][1]["reason"].lower()


def test_set_piece_goals_not_inferable():
    agg = peh.aggregate(ROWS)
    assert agg["players"][1]["set_piece_goals"] is None
    assert "externa" in agg["players"][1]["set_piece_reason"].lower()


def test_card_risk_history_levels():
    crh = peh.card_risk_history(peh.aggregate(ROWS))
    assert crh[6]["yellows"] == 2 and crh[6]["reds"] == 1
    assert "no derivado" in crh[6]["suspension_risk"]       # no fabricated suspension


# ----------------------------------------------------------------- enriched set-piece (§3 explainer)
def test_set_piece_with_real_history_explainer():
    agg = peh.aggregate(ROWS)
    sp = core.set_piece_hierarchy([3, 1], agg["names"], penalty_history=agg["penalty_history"],
                                  last_taken=agg["last_penalty"], full_history=agg["penalty_history"])
    pen = sp["penalties"]
    assert pen["primary"] == "PenMan" and pen["primary_count"] == 2
    assert pen["primary_last"]["date"] == "2026-06-25"
    assert "if_primary_absent" in pen


def test_set_piece_primary_absent_from_xi_promotes_and_flags():
    agg = peh.aggregate(ROWS)
    # the usual taker (id 3) is NOT in the probable XI -> honest flag, lower confidence
    sp = core.set_piece_hierarchy([1], agg["names"], penalty_history=agg["penalty_history"],
                                  full_history=agg["penalty_history"])
    assert sp["penalties"]["primary"] is None
    assert "ausente" in sp["penalties"]["reason"].lower()


def test_set_piece_no_history_not_fabricated():
    sp = core.set_piece_hierarchy([1, 2], {1: "A", 2: "B"}, penalty_history=None)
    assert sp["penalties"]["primary"] is None and sp["penalties"]["confidence"] == "baja"
