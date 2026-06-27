"""
WORLD CUP 2026 - one-time /injuries extractor for the LIVE injuries layer (ISOLATED).

Pulls /injuries for the upcoming (status NS) World Cup fixtures and persists each fixture's
parsed absences to a FOREVER JSON store (data/processed/worldcup/injuries_live/), STORE-GUARDED:
a fixture already in the store is SKIPPED (0 API). So the first run costs ~N calls (one per
upcoming fixture) and every later run costs 0 unless new fixtures appear. NO market (no odds/
predictions). SOFT-FAIL per fixture. Honours a hard API budget (--max-api) and NEVER forces the
API when the quota may be exhausted (CLAUDE.md hard rule): on a limit error it stops and reports.

The cards pipeline (build_worldcup_cards.fetch_injuries) reads this store first, so once warmed
the live adjustment needs ZERO injury API calls.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402
import worldcup_injuries_live as injlive  # noqa: E402

WC_LEAGUE = 1
WC_SEASON = 2026


def _parse_by_team(resp):
    """API /injuries response -> {team_name: [[player, reason], ...]}."""
    by = {}
    for it in resp or []:
        tn = (it.get("team") or {}).get("name")
        pl = it.get("player") or {}
        nm = pl.get("name")
        reason = pl.get("reason") or pl.get("type") or ""
        if tn and nm:
            by.setdefault(tn, []).append([nm, reason])
    return by


def main(max_api=80, only_within_days=None):
    c = APIFootballClient()

    def true_quota():
        try:
            return (c.request("/status", None, ttl_hours=0, force_refresh=True)
                    .get("response", {}).get("requests") or {}).get("current")
        except Exception:
            return None

    api0 = true_quota()
    now = datetime.now(timezone.utc)
    fx = c.fixtures(league=WC_LEAGUE, season=WC_SEASON).get("response", []) or []
    upcoming = []
    for f in fx:
        fxd = f.get("fixture", {})
        if ((fxd.get("status") or {}).get("short")) != "NS":
            continue
        fid = fxd.get("id")
        if fid is None:
            continue
        if only_within_days is not None:
            try:
                days = (datetime.fromisoformat(fxd.get("date") or "") - now).total_seconds() / 86400.0
                if not (0 <= days <= only_within_days):
                    continue
            except Exception:
                pass
        upcoming.append((int(fid), (fxd.get("date") or "")[:16]))
    upcoming.sort(key=lambda t: t[1])

    spent = 0
    cached = pulled = empty = skipped_budget = 0
    limit_hit = False
    for fid, ko in upcoming:
        if injlive.load_injuries_store(fid) is not None:
            cached += 1
            continue
        if spent >= max_api:
            skipped_budget += 1
            continue
        try:
            resp = c.injuries(fixture=fid).get("response", []) or []
            spent += 1
        except APIFootballError as e:
            msg = str(e).lower()
            if "limit" in msg or "exceeded" in msg or "quota" in msg:
                print(f"API_LIMIT_EXHAUSTED at fixture {fid}: {e}")
                limit_hit = True
                break
            print(f"  soft-fail fixture {fid}: {type(e).__name__}: {e}")
            continue
        by = _parse_by_team(resp)
        injlive.save_injuries_store(fid, by)   # persist FOREVER, even if empty (store-guard)
        pulled += 1
        if not by:
            empty += 1

    api1 = true_quota()
    delta = (api1 - api0) if (api0 is not None and api1 is not None) else "n/a"
    print("-" * 80)
    print(f"injuries_live store: {len(upcoming)} upcoming NS fixtures | already cached: {cached} | "
          f"pulled now: {pulled} (empty: {empty}) | skipped (budget): {skipped_budget}")
    print(f"API /injuries calls THIS run: {spent} (cap {max_api}) | true quota delta: {delta} | "
          f"now: {api1}/7500" + ("  ⚠️ API_LIMIT_EXHAUSTED" if limit_hit else ""))
    print(f"store dir: {injlive.STORE_DIR}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="One-time /injuries extractor (forever store-guard).")
    ap.add_argument("--max-api", type=int, default=80,
                    help="hard cap on /injuries calls this run (store-guarded; re-runs cost 0)")
    ap.add_argument("--within-days", type=float, default=None,
                    help="only fixtures kicking off within the next N days (default: all upcoming)")
    a = ap.parse_args()
    main(a.max_api, a.within_days)
