"""
PLAYER EVENT HISTORY aggregator (Fase 2). PURE, reusable, NO I/O, NO API, NO betting.

Aggregates the clean event table (from build_worldcup_fixture_events.py) into per-player history that
feeds the player-events core: goals, assists, penalties taken/scored/missed, cards, goal involvement,
last known penalty taker, sample, and honest data_quality/confidence/reason. Set-piece (free-kick /
corner) goals are NOT inferable from /fixtures/events -> returned as None + reason (Fase 3 external).

NEVER invents: a player with no events simply has no entry; small samples are flagged, not hidden.
"""
from __future__ import annotations

from typing import Optional

import pandas as pd

YELLOW = "Yellow Card"
SECOND_YELLOW = "Second Yellow card"
RED = "Red Card"
SMALL_SAMPLE = 4   # below this many appearances, history is "baja" confidence (orientativo)


def _rows(events):
    """Accept a DataFrame or a list of dicts -> list of dicts."""
    if isinstance(events, pd.DataFrame):
        return events.to_dict("records")
    return list(events or [])


def _to_int(x):
    try:
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return None
        return int(x)
    except Exception:
        return None


def aggregate(events, minutes_by_player: Optional[dict] = None) -> dict:
    """events: clean event rows (DataFrame or list). minutes_by_player: {player_id: minutes} for /90
    (optional; absent -> per90 None, never fabricated). Returns:
      {players:{pid:{...}}, penalty_history:{pid:pens_taken}, last_penalty:{pid:{...}}, names:{pid:name}}
    """
    rows = _rows(events)
    players: dict = {}
    names: dict = {}
    minutes_by_player = minutes_by_player or {}

    def _p(pid, name=None):
        pid = _to_int(pid)
        if pid is None:
            return None
        if pid not in players:
            players[pid] = {"player_id": pid, "player_name": name, "goals": 0, "assists": 0,
                            "pens_taken": 0, "pens_scored": 0, "pens_missed": 0,
                            "yellows": 0, "reds": 0, "goal_involvement": 0,
                            "fixtures": set(), "last_penalty": None}
        if name and not players[pid]["player_name"]:
            players[pid]["player_name"] = name
        if name:
            names[pid] = name
        return pid

    for r in rows:
        fid = r.get("fixture_id")
        date = r.get("date")
        pid = _p(r.get("player_id"), r.get("player_name"))
        if pid is not None:
            players[pid]["fixtures"].add(fid)
        # goals (own goals already excluded upstream)
        if int(r.get("is_goal") or 0) == 1 and pid is not None:
            players[pid]["goals"] += 1
        # penalties (taken = scored + missed) credited to the taker (player_id)
        if int(r.get("is_penalty_goal") or 0) == 1 and pid is not None:
            players[pid]["pens_taken"] += 1
            players[pid]["pens_scored"] += 1
            players[pid]["last_penalty"] = {"fixture_id": fid, "date": date, "scored": True}
        if int(r.get("is_penalty_miss") or 0) == 1 and pid is not None:
            players[pid]["pens_taken"] += 1
            players[pid]["pens_missed"] += 1
            players[pid]["last_penalty"] = {"fixture_id": fid, "date": date, "scored": False}
        # assists credited to the ASSIST player (not player_id)
        if int(r.get("is_assist") or 0) == 1:
            apid = _p(r.get("assist_player_id"), r.get("assist_player_name"))
            if apid is not None:
                players[apid]["assists"] += 1
                players[apid]["fixtures"].add(fid)
        # cards
        if int(r.get("is_card") or 0) == 1 and pid is not None:
            ct = str(r.get("card_type") or "")
            if ct == YELLOW:
                players[pid]["yellows"] += 1
            elif ct == SECOND_YELLOW:
                players[pid]["yellows"] += 1
                players[pid]["reds"] += 1
            elif ct == RED:
                players[pid]["reds"] += 1

    penalty_history, last_penalty = {}, {}
    for pid, d in players.items():
        n_fix = len([f for f in d["fixtures"] if f is not None])
        d["sample_fixtures"] = n_fix
        d["goal_involvement"] = d["goals"] + d["assists"]
        mins = minutes_by_player.get(pid)
        d["goals_per90"] = (round(d["goals"] / (mins / 90.0), 3) if mins and mins > 0 else None)
        # set-piece goals can't be inferred from /fixtures/events
        d["set_piece_goals"] = None
        d["set_piece_reason"] = "no inferible desde /fixtures/events (requiere fuente externa · Fase 3)"
        if n_fix == 0:
            d["data_quality"], d["confidence"] = "baja", "baja"
            d["reason"] = "sin apariciones con eventos"
        elif n_fix < SMALL_SAMPLE:
            d["data_quality"], d["confidence"] = "media", "baja"
            d["reason"] = f"muestra pequeña ({n_fix} partidos con eventos) — orientativo"
        else:
            d["data_quality"], d["confidence"] = "alta", "media"
            d["reason"] = f"{n_fix} partidos con eventos reales"
        d["fixtures"] = sorted(f for f in d["fixtures"] if f is not None)
        if d["pens_taken"] > 0:
            penalty_history[pid] = d["pens_taken"]
        if d["last_penalty"]:
            last_penalty[pid] = d["last_penalty"]

    return {"players": players, "penalty_history": penalty_history,
            "last_penalty": last_penalty, "names": names}


def card_risk_history(agg: dict) -> dict:
    """{player_id: {yellows, reds, sample, level}} for the card-risk note. level from yellow rate; never
    invents a suspension — accumulation suspensions need the competition rule + booking count which we
    flag as not derived here."""
    out = {}
    for pid, d in agg.get("players", {}).items():
        n = d.get("sample_fixtures", 0)
        yr = (d["yellows"] / n) if n else 0.0
        level = "alto" if yr >= 0.5 else ("medio" if yr >= 0.25 else "bajo")
        out[pid] = {"yellows": d["yellows"], "reds": d["reds"], "sample_fixtures": n,
                    "yellow_rate": round(yr, 3), "level": (level if n else "n/d"),
                    "suspension_risk": "no derivado (requiere reglas de acumulación de la competición)"}
    return out
