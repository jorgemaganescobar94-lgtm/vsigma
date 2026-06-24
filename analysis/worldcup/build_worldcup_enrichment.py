"""
WORLD CUP 2026 - per-fixture API ENRICHMENT collector (ISOLATED, analysis/worldcup/).

Pulls EVERY non-betting per-match datum the API offers and stores it per fixture, so the
briefing can show a few [REAL] lines post-FT and analysts get a full store for later.

PURIFIED: ZERO market. /odds, /predictions, /odds/live are HARD-FORBIDDEN here (EXCLUDED
guard raises if ever requested). NOT production (WC league id 1 is rejected by the
allowlist). No .env edits, no git, no betting logic.

Two hooks, wired as SEPARATE workflow steps (never inside the briefing render):

  prematch  For the fixtures in the card window: /fixtures/headtohead + the slow per-team
            lane (/teams/statistics, /transfers, /trophies-by-coach, /sidelined, /coachs,
            /venues). Cached 7/30/90d so it barely costs quota.

  postft    For each SETTLED fixture: /fixtures/statistics (full, incl. real xG) +
            /fixtures/events + /fixtures/players. Cached "forever" (a finished match never
            changes) AND store-guarded (already-enriched fixtures make ZERO API calls).

SOFT-FAIL everywhere: any API/parse error -> that section is skipped, NEVER raises, so the
briefing can never break (same contract as fetch_lineups/fetch_injuries in the card builder).

Store: data/processed/worldcup/api_enrichment/<fixture_id>.json  (already .gitignored), with
fetched_at_utc + endpoints_called for quota traceability.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
ROOT = OUT_DIR.parents[1]
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "api_enrichment"
CARDS = OUT_DIR / "worldcup_cards.csv"
LOG = OUT_DIR / "worldcup_predictions_log.csv"

WC_LEAGUE = 1
WC_SEASON = 2026

# Cache TTLs (hours) per the approved plan.
TTL_FIXTURES = 6           # reuse the card builder's cached /fixtures (6h)
TTL_FT = 24 * 3650         # ~forever: a finished match's stats/events/players never change
TTL_7D = 24 * 7            # team form / availability (teams/statistics, sidelined)
TTL_30D = 24 * 30          # slow-moving (h2h history, transfers, trophies, coachs)
TTL_90D = 24 * 90          # ~static (venues)

FINISHED = {"FT", "AET", "PEN"}

# PURIFICATION: these endpoints are forbidden in the World Cup product. Requesting one is a bug.
EXCLUDED = {"/odds", "/predictions", "/odds/live"}

# /fixtures/statistics 'type' -> summary key (the few stats shown on the ficha post-FT)
STAT_KEYS = {
    "Total Shots": "shots",
    "Ball Possession": "possession",
    "Corner Kicks": "corners",
    "expected_goals": "xg",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _client():
    """Construct the shared API client lazily (so importing this module needs no .env)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from api_football_client import APIFootballClient  # noqa: E402
    return APIFootballClient()


def _sig(path: str, params: dict | None) -> str:
    if not params:
        return path
    kv = "&".join(f"{k}={params[k]}" for k in sorted(params))
    return f"{path}?{kv}"


def _get(client, path, params, ttl, trace):
    """One cached, SOFT-FAILING request. Returns the 'response' payload, or None on any error.
    Appends the call signature to `trace` (cache hits included) for traceability. Never raises
    except for the purification guard, which is a programmer error, not a runtime condition."""
    if path in EXCLUDED:
        raise RuntimeError(f"PURIFICATION VIOLATION: {path} is forbidden in the World Cup product")
    try:
        resp = client.request(path, params, ttl_hours=ttl)
        trace.append(_sig(path, params))
        if isinstance(resp, dict):
            return resp.get("response")
        return None
    except Exception:
        return None  # soft-fail: never break the briefing


def _num(v):
    """Parse an API stat value (handles '58%', None, numeric strings)."""
    if v is None:
        return None
    if isinstance(v, str):
        v = v.strip().rstrip("%")
        if v == "":
            return None
    try:
        return float(v)
    except Exception:
        return None


# --------------------------------------------------------------------- store
def _store_path(fid) -> Path:
    return STORE_DIR / f"{int(fid)}.json"


def load_store(fid) -> dict:
    p = _store_path(fid)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_store(fid, data) -> None:
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    _store_path(fid).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------- parsing
def parse_statistics_summary(stat_resp, home_id, away_id) -> dict:
    """/fixtures/statistics response -> {shots_home, shots_away, possession_*, corners_*, xg_*}."""
    out = {}
    for t in stat_resp or []:
        tid = (t.get("team") or {}).get("id")
        side = "home" if tid == home_id else ("away" if tid == away_id else None)
        if side is None:
            continue
        for s in t.get("statistics", []) or []:
            key = STAT_KEYS.get(s.get("type"))
            if key:
                out[f"{key}_{side}"] = _num(s.get("value"))
    return out


def parse_events_summary(events_resp, home_id, away_id) -> dict:
    """/fixtures/events response -> first-goal timing + yellow/red card counts."""
    out = {"yellow": 0, "red": 0, "n_goals": 0}
    goals = []
    for e in events_resp or []:
        typ = e.get("type")
        tid = (e.get("team") or {}).get("id")
        minute = (e.get("time") or {}).get("elapsed")
        if typ == "Goal":
            goals.append((minute if minute is not None else 999, tid))
        elif typ == "Card":
            d = (e.get("detail") or "").lower()
            if "yellow" in d:
                out["yellow"] += 1
            elif "red" in d:
                out["red"] += 1
    out["n_goals"] = len(goals)
    if goals:
        goals.sort(key=lambda g: g[0])
        m, tid = goals[0]
        out["first_goal_minute"] = m
        out["first_goal_side"] = "home" if tid == home_id else ("away" if tid == away_id else "?")
    return out


# --------------------------------------------------------------------- fixtures index
def _fixtures_index(client, trace) -> dict:
    """id -> {home_id, away_id, home, away, venue_id, status} from the cached /fixtures call."""
    resp = _get(client, "/fixtures", {"league": WC_LEAGUE, "season": WC_SEASON}, TTL_FIXTURES, trace)
    idx = {}
    for f in resp or []:
        fx = f.get("fixture", {}) or {}
        fid = fx.get("id")
        if fid is None:
            continue
        teams = f.get("teams", {}) or {}
        idx[int(fid)] = {
            "home_id": (teams.get("home") or {}).get("id"),
            "away_id": (teams.get("away") or {}).get("id"),
            "home": (teams.get("home") or {}).get("name"),
            "away": (teams.get("away") or {}).get("name"),
            "venue_id": (fx.get("venue") or {}).get("id"),
            "status": (fx.get("status") or {}).get("short"),
        }
    return idx


# --------------------------------------------------------------------- prematch hook
def _team_slow_lane(client, tid, trace) -> dict:
    """Slow, rarely-changing per-team data (all cached 7/30d). /trophies BY COACH, not player."""
    sect = {}
    sect["team_statistics"] = _get(
        client, "/teams/statistics",
        {"league": WC_LEAGUE, "season": WC_SEASON, "team": tid}, TTL_7D, trace)
    sect["transfers"] = _get(client, "/transfers", {"team": tid}, TTL_30D, trace) or []
    sect["sidelined"] = _get(client, "/sidelined", {"team": tid}, TTL_7D, trace) or []
    coachs = _get(client, "/coachs", {"team": tid}, TTL_30D, trace) or []
    sect["coachs"] = coachs
    coach_id = next((co.get("id") for co in coachs if co.get("id") is not None), None)
    sect["trophies"] = (_get(client, "/trophies", {"coach": coach_id}, TTL_30D, trace) or []) \
        if coach_id is not None else []
    return sect


def enrich_prematch(fixture_ids=None, date_from=None, date_to=None, client=None, force=False) -> dict:
    """h2h for the window's fixtures + the slow per-team lane. Cached -> tiny quota cost."""
    import pandas as pd  # local import keeps module import light
    if client is None:
        client = _client()
    trace = []
    idx = _fixtures_index(client, trace)

    if fixture_ids is None:
        fixture_ids = []
        if CARDS.exists():
            try:
                cdf = pd.read_csv(CARDS)
                if "fixture_id" in cdf.columns:
                    fixture_ids = [int(x) for x in cdf["fixture_id"].dropna().astype(int).tolist()]
            except Exception:
                fixture_ids = []

    teams_done, venues_done = {}, {}
    enriched = 0
    for fid in fixture_ids:
        meta = idx.get(int(fid))
        if not meta:
            continue
        home_id, away_id, venue_id = meta["home_id"], meta["away_id"], meta["venue_id"]
        ftrace = []
        h2h = _get(client, "/fixtures/headtohead", {"h2h": f"{home_id}-{away_id}"}, TTL_30D, ftrace) \
            if (home_id and away_id) else None

        team_sections = {}
        for tid in (home_id, away_id):
            if tid is None:
                continue
            if tid not in teams_done:
                teams_done[tid] = _team_slow_lane(client, tid, ftrace)
            team_sections[str(tid)] = teams_done[tid]

        venue = None
        if venue_id is not None:
            if venue_id not in venues_done:
                venues_done[venue_id] = _get(client, "/venues", {"id": venue_id}, TTL_90D, ftrace)
            venue = venues_done[venue_id]

        store = load_store(fid)
        store.setdefault("fixture_id", int(fid))
        store["home"], store["away"] = meta["home"], meta["away"]
        store["home_id"], store["away_id"], store["venue_id"] = home_id, away_id, venue_id
        store["prematch"] = {"headtohead": h2h or [], "teams": team_sections, "venue": venue or []}
        store["fetched_at_utc"] = _now()
        store["endpoints_called"] = sorted(set(store.get("endpoints_called", [])) | set(ftrace))
        save_store(fid, store)
        enriched += 1
        trace.extend(ftrace)

    return {"hook": "prematch", "fixtures": len(fixture_ids), "enriched": enriched,
            "api_calls_traced": len(trace), "trace": trace}


# --------------------------------------------------------------------- postft hook
def enrich_postft(fixture_ids=None, client=None, force=False) -> dict:
    """Per settled fixture: full statistics (incl. real xG) + events + players. Store-guarded:
    an already-enriched fixture makes ZERO API calls on re-run (FT data is immutable)."""
    import pandas as pd
    if client is None:
        client = _client()
    trace = []

    if fixture_ids is None:
        if not LOG.exists():
            return {"hook": "postft", "fixtures": 0, "enriched": 0, "api_calls_traced": 0, "trace": []}
        try:
            df = pd.read_csv(LOG)
        except Exception:
            return {"hook": "postft", "fixtures": 0, "enriched": 0, "api_calls_traced": 0, "trace": []}
        if "settled" in df.columns:
            df = df[df["settled"].fillna(0).astype(int) == 1]
        fixture_ids = [int(x) for x in df["fixture_id"].dropna().astype(int).tolist()] \
            if "fixture_id" in df.columns else []

    idx = _fixtures_index(client, trace)
    enriched = 0
    for fid in fixture_ids:
        store = load_store(fid)
        # store-guard: a finished match never changes -> don't re-fetch (0 API on 2nd pass)
        if not force and (store.get("postft") or {}).get("summary"):
            continue
        meta = idx.get(int(fid), {})
        home_id, away_id = meta.get("home_id"), meta.get("away_id")

        ftrace = []
        stat = _get(client, "/fixtures/statistics", {"fixture": fid}, TTL_FT, ftrace)
        events = _get(client, "/fixtures/events", {"fixture": fid}, TTL_FT, ftrace)
        players = _get(client, "/fixtures/players", {"fixture": fid}, TTL_FT, ftrace)
        if stat is None and events is None and players is None:
            continue  # all soft-failed -> write nothing, retry next run

        summary = {}
        summary.update(parse_statistics_summary(stat, home_id, away_id))
        summary.update(parse_events_summary(events, home_id, away_id))

        store.setdefault("fixture_id", int(fid))
        if meta.get("home"):
            store["home"], store["away"] = meta.get("home"), meta.get("away")
        store["home_id"], store["away_id"] = home_id, away_id
        store["postft"] = {
            "statistics": stat or [],
            "events": events or [],
            "players": players or [],
            "summary": summary,
        }
        store["fetched_at_utc"] = _now()
        store["endpoints_called"] = sorted(set(store.get("endpoints_called", [])) | set(ftrace))
        save_store(fid, store)
        enriched += 1
        trace.extend(ftrace)

    return {"hook": "postft", "fixtures": len(fixture_ids), "enriched": enriched,
            "api_calls_traced": len(trace), "trace": trace}


# --------------------------------------------------------------------- ficha helper
def real_lines_for_fixture(fid, score=None) -> list[str]:
    """Up to 2 [REAL] lines for the post-FT briefing, from the stored summary. [] if no store
    (SOFT: the briefing then looks exactly as before this feature)."""
    summary = ((load_store(fid).get("postft") or {}).get("summary")) or {}
    if not summary:
        return []

    def pair(key):
        h, a = summary.get(f"{key}_home"), summary.get(f"{key}_away")
        return (h, a) if (h is not None and a is not None) else None

    lines = []
    seg1 = []
    xg = pair("xg")
    if xg:
        seg1.append(f"xG {xg[0]:.1f}-{xg[1]:.1f}")
    sh = pair("shots")
    if sh:
        seg1.append(f"tiros {sh[0]:.0f}-{sh[1]:.0f}")
    po = pair("possession")
    if po:
        seg1.append(f"posesión {po[0]:.0f}-{po[1]:.0f}")
    co = pair("corners")
    if co:
        seg1.append(f"córners {co[0]:.0f}-{co[1]:.0f}")
    if seg1:
        lines.append("[REAL] " + " · ".join(seg1))

    seg2 = []
    if summary.get("first_goal_minute") is not None:
        side = {"home": "local", "away": "visit."}.get(summary.get("first_goal_side"), "")
        seg2.append(f"1er gol min {int(summary['first_goal_minute'])}" + (f" ({side})" if side else ""))
    if "yellow" in summary:
        seg2.append(f"tarjetas {int(summary.get('yellow', 0))}A/{int(summary.get('red', 0))}R")
    if score:
        seg2.append(f"final {score}")
    if seg2:
        lines.append("[REAL] " + " · ".join(seg2))
    return lines


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup per-fixture API enrichment (isolated, shadow).")
    ap.add_argument("cmd", choices=["prematch", "postft"])
    ap.add_argument("--from", dest="dfrom", default=None)
    ap.add_argument("--to", dest="dto", default=None)
    ap.add_argument("--fixtures", default=None, help="comma-separated fixture ids (validation/manual)")
    ap.add_argument("--force", action="store_true", help="ignore the store-guard and re-fetch")
    a = ap.parse_args()
    fids = [int(x) for x in a.fixtures.split(",")] if a.fixtures else None
    if a.cmd == "prematch":
        result = enrich_prematch(fids, a.dfrom, a.dto, force=a.force)
    else:
        result = enrich_postft(fids, force=a.force)
    print(json.dumps(result, ensure_ascii=False))
