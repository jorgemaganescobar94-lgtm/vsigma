"""
QUAL-ENGINE AUDIT (READ-ONLY) — runs the HONEST qualification engine over EVERY current World Cup group
using the REAL live standings + the REAL last-matchday pairings, so the labels can be checked by hand.

NO API CALLS, NO betting endpoints, NO writes to any production path. Data sources (read-only):
  - live standings: data/processed/worldcup/context/standings_<day>.json (the store-guarded cache)
  - last-matchday pairings: the cached /fixtures(league=1,season=2026) row in the api_football sqlite cache

For each group it prints, per team, the coarse tag AND the honest conditional phrase. Finished groups
(every team played all 3) are reported as final (top-2 -> qualified, 3rd -> best-third pending, 4th -> out).

Run:  .\.venv\Scripts\python.exe analysis/worldcup/qual_engine_audit.py
      .\.venv\Scripts\python.exe analysis/worldcup/qual_engine_audit.py --day 2026-06-25
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
ROOT = OUT_DIR.parents[1]
sys.path.insert(0, str(OUT_DIR))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import qual_engine as Q  # noqa: E402

STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "context"
CACHE_DB = ROOT / "data" / "cache" / "api_football_cache.sqlite3"
LEAGUE, SEASON = 1, 2026
LAST_ROUND = "Group Stage - 3"


def _latest_standings_path(day=None):
    if day:
        p = STORE_DIR / f"standings_{day}.json"
        return p if p.exists() else None
    cands = sorted(STORE_DIR.glob("standings_*.json"))
    return cands[-1] if cands else None


def load_groups(day=None):
    """group letter -> [ {name, pts, played} ] from the cached /standings response (lettered tables only)."""
    p = _latest_standings_path(day)
    if p is None:
        raise SystemExit(f"no cached standings json under {STORE_DIR}")
    data = json.loads(p.read_text(encoding="utf-8"))
    groups = {}
    for blk in data:
        for tbl in ((blk.get("league") or {}).get("standings") or []):
            for t in tbl:
                gname = str(t.get("group") or "")
                if not (gname.startswith("Group ") and len(gname.split()) == 2 and len(gname.split()[-1]) == 1):
                    continue  # skip the aggregate 'Group Stage' table
                name = (t.get("team") or {}).get("name")
                if not name:
                    continue
                row = {"name": name, "pts": float(t.get("points") or 0),
                       "played": int((t.get("all") or {}).get("played") or 0)}
                g = groups.setdefault(gname, [])
                groups[gname] = [r for r in g if r["name"] != name] + [row]
    return groups, p.name


def load_last_matchday_pairings():
    """group letter -> [(home, away), (home, away)] for the LAST round, from the cached /fixtures row.
    READ-ONLY query against the sqlite cache (no API)."""
    if not CACHE_DB.exists():
        return {}
    con = sqlite3.connect(f"file:{CACHE_DB}?mode=ro", uri=True)
    try:
        row = con.execute(
            "SELECT response_json FROM api_cache WHERE path='/fixtures' AND params_json=?",
            (json.dumps({"league": LEAGUE, "season": SEASON}, separators=(",", ":")),),
        ).fetchone()
    finally:
        con.close()
    if not row:
        return {}
    payload = json.loads(row[0])
    resp = payload.get("response", payload) if isinstance(payload, dict) else payload
    pairings = defaultdict(list)
    for f in resp:
        lg = f.get("league") or {}
        if str(lg.get("round")) != LAST_ROUND:
            continue
        teams = f.get("teams") or {}
        h = (teams.get("home") or {}).get("name")
        a = (teams.get("away") or {}).get("name")
        if h and a:
            pairings[(h, a)].append(f.get("fixture", {}).get("date", ""))
    return resp, pairings


def _group_of(name, groups):
    for g, rows in groups.items():
        if any(r["name"] == name for r in rows):
            return g
    return None


def _pairings_for_group(group_rows, all_pairings):
    names = {r["name"] for r in group_rows}
    out = [(h, a) for (h, a) in all_pairings if h in names and a in names]
    return out


def audit(day=None):
    groups, src = load_groups(day)
    fixtures, all_pairings = load_last_matchday_pairings()
    n_groups = sum(1 for rows in groups.values() if len(rows) == 4)
    all_tables = [{r["name"]: {"pts": r["pts"]} for r in rows} for rows in groups.values() if len(rows) == 4]
    n_thirds = Q.THIRDS_BY_NGROUPS.get(n_groups, 0)

    lines = []
    lines.append("=" * 90)
    lines.append("QUAL-ENGINE AUDIT — honest conditional labels, EVERY current group (READ-ONLY, no API)")
    lines.append("=" * 90)
    lines.append(f"standings source : {src}")
    lines.append(f"format           : {n_groups} groups -> top-2 + {n_thirds} best thirds advance")
    lines.append("")

    for g in sorted(groups):
        rows = sorted(groups[g], key=lambda r: -r["pts"])
        lines.append("-" * 90)
        std = "  ".join(f"{r['name']}={int(r['pts'])}(pj{r['played']})" for r in rows)
        lines.append(f"{g}:  {std}")
        if len(rows) != 4:
            lines.append("  (no es un grupo de 4 -> omitido)")
            lines.append("")
            continue
        table = {r["name"]: {"pts": r["pts"]} for r in rows}
        remaining = max(3 - max(r["played"] for r in rows), 0)
        all_played = all(r["played"] >= 3 for r in rows)
        pgroup = _pairings_for_group(rows, all_pairings)

        if all_played:
            # finished group: final order is set; best-third cutoff is cross-group (not all groups final)
            for i, r in enumerate(rows):
                if i < 2:
                    lab = "ya clasificado (top-2, grupo terminado)"
                elif i == 2:
                    alive = Q.alive_as_third(r["pts"], all_tables, table, n_thirds)
                    lab = ("3º — vivo como mejor tercero (pendiente del corte)" if alive
                           else "3º — eliminado (no entra como mejor tercero)")
                else:
                    lab = "eliminado (4º)"
                lines.append(f"    {r['name']:24} [final]            {lab}")
            lines.append("")
            continue

        if any(r["played"] != 2 for r in rows) or len(pgroup) != 2:
            lines.append(f"  (no es última jornada limpia: pj!=2 o pairings={len(pgroup)} -> motor honesto omitido)")
            lines.append("")
            continue

        lines.append(f"  última jornada — partidos: {pgroup[0][0]} vs {pgroup[0][1]}  ||  {pgroup[1][0]} vs {pgroup[1][1]}")
        for (h, a) in pgroup:
            for team in (h, a):
                sc = Q.analyze_team(table, (h, a), team, all_tables, n_groups)
                tag = Q.short_tag(sc)
                phrase = Q.phrase_es(sc)
                lines.append(f"    {team:24} [{tag:20}] {phrase}")
        lines.append("")

    out = "\n".join(lines)
    print(out)
    rep = OUT_DIR / "qual_engine_audit_report.txt"
    rep.write_text(out, encoding="utf-8")
    print(f"\n-> {rep}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Honest qual-engine audit over all current WC groups (read-only).")
    ap.add_argument("--day", default=None, help="standings_<day>.json to use (default: latest cached)")
    audit(ap.parse_args().day)
