"""
WORLD CUP 2026 — PLAYER & INDIVIDUAL-EVENTS card builder (Fase 1). READ-ONLY · NO API · NO market/odds.

Glue between the existing per-player props (worldcup_player_props_log.csv, λ's frozen at KO) + the
team-level card (worldcup_cards.csv: 1X2/xG/corners/cards) and the SHARED core
(analysis/players/player_events_core.py), producing the §11 structured player_predictions output for
each upcoming fixture: likely scorers / shots-on-target / assisters, set-piece takers, card risk,
key matchups, two-XI scenario note, with honest data_quality/confidence/reason (§12). Pluggable
external sources (xA / referee / weather) via analysis/players/player_data_adapters.py — absent ->
fields None + reason, NEVER fabricated.

Output (read-only, git-add explicit):
  * worldcup_player_events.json  (list: one object per fixture, the full §11 structure + team summary)
  * worldcup_player_events.csv   (flat: one row per ranked player entry, for quick inspection)

Set-piece takers: Fase 1 reads an OPTIONAL file data/external/set_piece_history.csv
(team_id, player_id, penalties, free_kicks, corners); absent -> "no determinado" + reason (the live
/fixtures/events extractor is Fase 2). NO fabrication.

Run:  python analysis/worldcup/build_worldcup_player_events.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_events_core as core  # noqa: E402
import player_data_adapters as adapters  # noqa: E402
import player_event_history as peh  # noqa: E402  (Fase 2: real per-player history aggregator)
import build_worldcup_fixture_events as fxev  # noqa: E402  (Fase 2: real events extractor)
import worldcup_learning_loop as ll  # noqa: E402  (top_scoreline only; import has no side effects)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CARDS = HERE / "worldcup_cards.csv"
PROPS_LOG = HERE / "worldcup_player_props_log.csv"
SET_PIECE_FILE = ROOT / "data" / "external" / "set_piece_history.csv"
OUT_JSON = HERE / "worldcup_player_events.json"
OUT_CSV = HERE / "worldcup_player_events.csv"
HISTORY_CSV = HERE / "worldcup_player_event_history.csv"


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_set_piece_history(path=SET_PIECE_FILE):
    """Optional {team_id: {'penalties':{pid:ct}, 'free_kicks':{...}, 'corners':{...}}}. Absent -> {}."""
    try:
        if not Path(path).exists():
            return {}
        df = pd.read_csv(path)
    except Exception:
        return {}
    out = {}
    for _, r in df.iterrows():
        try:
            tid = int(r["team_id"]); pid = int(r["player_id"])
        except Exception:
            continue
        d = out.setdefault(tid, {"penalties": {}, "free_kicks": {}, "corners": {}})
        for col, key in (("penalties", "penalties"), ("free_kicks", "free_kicks"), ("corners", "corners")):
            if col in df.columns and pd.notna(r.get(col)):
                try:
                    d[key][pid] = float(r[col])
                except Exception:
                    pass
    return out


def _expand_side(rows, xa_map):
    out = []
    for _, r in rows.iterrows():
        d = r.to_dict()
        pid = d.get("player_id")
        xa = key_passes = None
        try:
            ent = xa_map.get(int(pid)) if pid is not None and not pd.isna(pid) else None
            if ent:
                xa, key_passes = ent.get("xa90"), ent.get("key_passes90")
        except Exception:
            pass
        out.append(core.expand_player(d, xa90=xa, key_passes90=key_passes))
    return out


def _team_summary(team, attack_xg, opp_xg, corners_for, corners_against):
    dom = None
    if corners_for is not None and corners_against is not None:
        tot = corners_for + corners_against
        dom = (corners_for / tot) if tot else None
    return {"team": team, "attack_xg": attack_xg, "def_concede_proxy": opp_xg, "corner_dominance": dom}


def build():
    if not CARDS.exists() or not PROPS_LOG.exists():
        print("player-events: faltan cards o props log; nada que construir (soft).")
        OUT_JSON.write_text("[]", encoding="utf-8")
        pd.DataFrame().to_csv(OUT_CSV, index=False)
        return []
    cards = pd.read_csv(CARDS)
    props = pd.read_csv(PROPS_LOG)
    xa_map, xa_reason = adapters.load_xa_rates()
    sp_hist = _load_set_piece_history()      # optional external file (fk/corners fallback)
    status = adapters.adapters_status()

    # Fase 2 — REAL event history: penalties / last taker / cards from /fixtures/events (cached store).
    events_df = fxev.extract()[fxev.COLUMNS] if True else None
    minutes_by_player = {}
    if "player_id" in props.columns and "act_minutes" in props.columns:
        mm = props.dropna(subset=["player_id"]).groupby("player_id")["act_minutes"].sum()
        minutes_by_player = {int(k): float(v) for k, v in mm.items() if pd.notna(v)}
    agg = peh.aggregate(events_df, minutes_by_player)
    real_pen_hist = agg["penalty_history"]            # GLOBAL {pid: pens_taken} from real events
    real_last_pen = agg["last_penalty"]
    ev_names = agg["names"]
    card_hist = peh.card_risk_history(agg)
    events_source = ("eventos reales (/fixtures/events)" if real_pen_hist
                     else "sin penaltis reales en eventos liquidados todavía")
    # persist the per-player real history as an inspectable artifact (§2 deliverable)
    hist_rows = []
    for pid, d in agg["players"].items():
        hist_rows.append({"player_id": pid, "player_name": d.get("player_name"),
                          "goals": d["goals"], "assists": d["assists"], "goals_per90": d["goals_per90"],
                          "pens_taken": d["pens_taken"], "pens_scored": d["pens_scored"],
                          "pens_missed": d["pens_missed"], "yellows": d["yellows"], "reds": d["reds"],
                          "goal_involvement": d["goal_involvement"], "set_piece_goals": d["set_piece_goals"],
                          "sample_fixtures": d["sample_fixtures"], "data_quality": d["data_quality"],
                          "confidence": d["confidence"], "reason": d["reason"]})
    pd.DataFrame(hist_rows).sort_values("goal_involvement", ascending=False, ignore_index=True).to_csv(
        HISTORY_CSV, index=False) if hist_rows else pd.DataFrame().to_csv(HISTORY_CSV, index=False)

    fixtures_out, flat_rows = [], []
    for _, c in cards.iterrows():
        fid = c.get("fixture_id")
        if pd.isna(fid):
            continue
        fid = int(fid)
        sub = props[pd.to_numeric(props["fixture_id"], errors="coerce") == fid]
        home, away = str(c.get("home")), str(c.get("away"))
        h_rows = sub[sub["team"].astype(str) == home]
        a_rows = sub[sub["team"].astype(str) == away]
        h_exp = _expand_side(h_rows, xa_map)
        a_exp = _expand_side(a_rows, xa_map)

        names_by_id = dict(ev_names)     # real event names first (full names), props names fill gaps
        h_ids, a_ids = [], []
        for _, r in sub.iterrows():
            try:
                pid = int(r["player_id"]); names_by_id.setdefault(pid, r["player"])
                (h_ids if str(r["team"]) == home else a_ids).append(pid)
            except Exception:
                continue
        h_tid = int(h_rows["team_id"].iloc[0]) if len(h_rows) else None
        a_tid = int(a_rows["team_id"].iloc[0]) if len(a_rows) else None
        # penalties from REAL events (global hist; core restricts to each team's XI ids). fk/corners
        # from the optional external file (events can't give them reliably). last taker for the explainer.
        sp_home = core.set_piece_hierarchy(
            h_ids, names_by_id, penalty_history=real_pen_hist, last_taken=real_last_pen,
            full_history=real_pen_hist, fk_history=sp_hist.get(h_tid, {}).get("free_kicks"),
            corner_history=sp_hist.get(h_tid, {}).get("corners"))
        sp_away = core.set_piece_hierarchy(
            a_ids, names_by_id, penalty_history=real_pen_hist, last_taken=real_last_pen,
            full_history=real_pen_hist, fk_history=sp_hist.get(a_tid, {}).get("free_kicks"),
            corner_history=sp_hist.get(a_tid, {}).get("corners"))

        hx, ax = c.get("our_xg_home"), c.get("our_xg_away")
        h_sum = _team_summary(home, hx, ax, c.get("st_corners_home"), c.get("st_corners_away"))
        a_sum = _team_summary(away, ax, hx, c.get("st_corners_away"), c.get("st_corners_home"))
        matchups = core.key_matchups(h_sum, a_sum)

        meta = {"fixture_id": fid, "kickoff_utc": c.get("kickoff_utc"), "home": home, "away": away,
                "round": c.get("round")}
        obj = core.build_player_predictions(meta, h_exp, a_exp, sp_home, sp_away, matchups,
                                            scenarios=core.scenario_delta(h_exp + a_exp, None))
        # team-level context for the Telegram report (1X2, score, xG, corners, cards)
        obj["team_context"] = {
            "p_home": c.get("our_home"), "p_draw": c.get("our_draw"), "p_away": c.get("our_away"),
            "xg_home": hx, "xg_away": ax,
            "top_score": ll.top_scoreline(hx, ax),
            "exp_corners_total": c.get("st_corners_total"), "exp_cards_total": c.get("st_cards_total"),
            "exp_sot_home": c.get("st_shots_home"), "exp_sot_away": c.get("st_shots_away"),
        }
        obj["adapters_status"] = status
        obj["xa_source"] = xa_reason
        obj["events_source"] = events_source
        fixtures_out.append(obj)

        # flat rows
        pp = obj["player_predictions"]
        for cat, items in (("scorer", pp["likely_scorers"]), ("sot", pp["likely_shots_on_target"]),
                           ("assist", pp["likely_assisters"]), ("card_risk", pp["card_risk"])):
            for it in items:
                flat_rows.append({"fixture_id": fid, "home": home, "away": away, "category": cat, **it})

    OUT_JSON.write_text(json.dumps(fixtures_out, ensure_ascii=False, indent=2, default=str),
                        encoding="utf-8")
    pd.DataFrame(flat_rows).to_csv(OUT_CSV, index=False)
    print(f"player-events: {len(fixtures_out)} fixtures -> {OUT_JSON.name} + {OUT_CSV.name} "
          f"| adapters xA={status['xa90']} ref={status['referee_card_rates']} weather={status['weather']}")
    return fixtures_out


if __name__ == "__main__":
    argparse.ArgumentParser(description="World Cup player-events card (read-only, shadow).").parse_args()
    build()
