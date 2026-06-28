"""
WORLD CUP 2026 — REAL FIXTURE-EVENTS extractor (Fase 2). READ-ONLY · NO market/odds · NO betting.

Parses REAL /fixtures/events (goals, assists, cards, substitutions) for settled World Cup fixtures and
writes a clean per-event table. Source of events = the enrichment store the post-FT step already cached
(data/processed/worldcup/api_enrichment/<fid>.json -> postft.events); optionally fetches missing ones
via the shared client (store-guarded, cached "forever" -> ~0 marginal API). NEVER invents an event.

WHAT /fixtures/events RELIABLY GIVES (so we only emit these):
  * goals: Normal Goal / Penalty / Own Goal / Missed Penalty  (+ assist player when present)
  * cards: Yellow Card / Red Card / Second Yellow card
  * substitutions
NOT reliably available from this endpoint (so we DO NOT emit / mark as insufficient downstream):
  * direct free-kick takers, corner takers, set-piece assist source  -> Fase 3 (FBref/StatsBomb/Opta)

Output (read-only, git-add explicit): worldcup_fixture_events.csv  (one row per real event).
Run:  python analysis/worldcup/build_worldcup_fixture_events.py
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

import build_worldcup_enrichment as enr  # noqa: E402  (store loader + client; import has no side effects)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LOG = HERE / "worldcup_predictions_log.csv"
OUT_CSV = HERE / "worldcup_fixture_events.csv"
COMPETITION = "World Cup 2026"

COLUMNS = [
    "fixture_id", "date", "competition", "team_id", "team_name", "opponent_id", "opponent_name",
    "player_id", "player_name", "assist_player_id", "assist_player_name",
    "event_type", "event_detail", "minute", "extra_minute",
    "is_goal", "is_assist", "is_penalty_goal", "is_penalty_miss", "is_own_goal",
    "is_card", "card_type", "is_substitution", "data_quality", "confidence", "source",
]

# explicit detail strings the endpoint uses (anything else -> conservative flags, never guessed)
GOAL_SCORED = {"Normal Goal", "Penalty"}
PEN_MISS = {"Missed Penalty"}
CARD_DETAILS = {"Yellow Card", "Red Card", "Second Yellow card"}


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _team_ids_in(events):
    ids = []
    for e in events or []:
        tid = (e.get("team") or {}).get("id")
        if tid is not None and tid not in ids:
            ids.append(tid)
    return ids


def _classify(e):
    """Return the boolean/typed flags for one event from its (type, detail). Never guesses beyond the
    explicit strings the endpoint provides."""
    typ = e.get("type")
    detail = e.get("detail") or ""
    is_goal = int(typ == "Goal" and detail in GOAL_SCORED)        # own goals EXCLUDED from player goals
    is_pen_goal = int(typ == "Goal" and detail == "Penalty")
    is_pen_miss = int(typ == "Goal" and detail in PEN_MISS)
    is_own = int(typ == "Goal" and detail == "Own Goal")
    is_card = int(typ == "Card")
    card_type = detail if (is_card and detail in CARD_DETAILS) else ("" if not is_card else detail)
    is_subst = int(typ == "subst")
    assist = e.get("assist") or {}
    # an assist only counts on a REAL goal (not own goal, not miss, not a substitution's 'assist' field)
    has_assist = int(is_goal == 1 and assist.get("id") is not None)
    # confidence: explicit known detail -> alta; unknown/blank detail -> media (still a real event)
    known = (typ == "Goal" and detail in (GOAL_SCORED | PEN_MISS | {"Own Goal"})) \
        or (is_card and detail in CARD_DETAILS) or is_subst
    return {
        "is_goal": is_goal, "is_penalty_goal": is_pen_goal, "is_penalty_miss": is_pen_miss,
        "is_own_goal": is_own, "is_card": is_card, "card_type": card_type,
        "is_substitution": is_subst, "is_assist": has_assist,
        "confidence": "alta" if known else "media",
    }


def parse_fixture_events(events_resp, meta) -> list:
    """PURE: /fixtures/events list + fixture meta -> clean §1 rows. meta: {fixture_id, date}. Team and
    opponent are derived from the events themselves (team.id/name). [] if no events (no fabrication)."""
    events = events_resp or []
    if not events:
        return []
    team_ids = _team_ids_in(events)
    name_by_id = {}
    for e in events:
        t = e.get("team") or {}
        if t.get("id") is not None:
            name_by_id[t["id"]] = t.get("name")
    rows = []
    for e in events:
        t = e.get("team") or {}
        tid = t.get("id")
        opp_id = next((x for x in team_ids if x != tid), None)
        p = e.get("player") or {}
        a = e.get("assist") or {}
        tm = e.get("time") or {}
        fl = _classify(e)
        # the 'assist' field on a substitution is the player coming off — NOT a goal assist; null it out
        assist_id = a.get("id") if fl["is_assist"] else None
        assist_name = a.get("name") if fl["is_assist"] else None
        rows.append({
            "fixture_id": meta.get("fixture_id"), "date": meta.get("date"), "competition": COMPETITION,
            "team_id": tid, "team_name": name_by_id.get(tid),
            "opponent_id": opp_id, "opponent_name": name_by_id.get(opp_id),
            "player_id": p.get("id"), "player_name": p.get("name"),
            "assist_player_id": assist_id, "assist_player_name": assist_name,
            "event_type": e.get("type"), "event_detail": e.get("detail"),
            "minute": tm.get("elapsed"), "extra_minute": tm.get("extra"),
            **{k: fl[k] for k in ("is_goal", "is_assist", "is_penalty_goal", "is_penalty_miss",
                                  "is_own_goal", "is_card", "card_type", "is_substitution")},
            "data_quality": "alta", "confidence": fl["confidence"], "source": "api_football_events",
        })
    return rows


def _settled_fixtures(log_path=LOG):
    """(fixture_id, date) for settled WC fixtures from the committed predictions log."""
    p = Path(log_path)
    if not p.exists():
        return []
    try:
        df = pd.read_csv(p)
    except Exception:
        return []
    if "settled" not in df.columns:
        return []
    df = df[df["settled"].fillna(0).astype(int) == 1]
    out = []
    for _, r in df.iterrows():
        try:
            out.append({"fixture_id": int(r["fixture_id"]),
                        "date": str(r.get("kickoff_utc") or "")[:10]})
        except Exception:
            continue
    return out


def extract(log_path=LOG, out_csv=OUT_CSV, fetch_missing=False):
    """Build the clean events table for all settled WC fixtures. Reads cached events from the post-FT
    store; if fetch_missing and a fixture is absent, fetches once via the client (store-guarded)."""
    fixtures = _settled_fixtures(log_path)
    all_rows, n_with, n_without = [], 0, 0
    client = None
    for meta in fixtures:
        fid = meta["fixture_id"]
        events = (enr.load_store(fid).get("postft") or {}).get("events")
        if not events and fetch_missing:
            try:
                client = client or enr._client()
                trace = []
                events = enr._get(client, "/fixtures/events", {"fixture": fid}, enr.TTL_FT, trace)
            except Exception:
                events = None
        rows = parse_fixture_events(events, meta)
        if rows:
            n_with += 1
            all_rows.extend(rows)
        else:
            n_without += 1
    df = pd.DataFrame(all_rows, columns=COLUMNS)
    df.to_csv(out_csv, index=False)
    print(f"fixture-events: {len(df)} eventos de {n_with} fixtures con datos "
          f"({n_without} liquidados sin eventos en store) -> {out_csv.name}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup real fixture-events extractor (read-only).")
    ap.add_argument("--fetch-missing", action="store_true",
                    help="fetch events for settled fixtures absent from the store (store-guarded, cached)")
    a = ap.parse_args()
    extract(fetch_missing=a.fetch_missing)
