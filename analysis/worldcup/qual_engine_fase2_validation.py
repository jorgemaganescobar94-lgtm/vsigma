"""
FASE 2 VALIDATION (READ-ONLY) — exercises the PRODUCTION functions now wired to the honest engine:
  (1) build_worldcup_cards.compute_group_info  -> the ficha "Contexto de grupo" line (info, conditional)
  (2) worldcup_context_shadow.classify_fixture -> the MULTIPLIER decision (tag + mult per team)
for EVERY last-matchday group, using the REAL live standings + REAL last-matchday pairings.

NO API CALLS, NO betting endpoints, NO writes to any production path. Data sources (read-only):
  - standings: data/processed/worldcup/context/standings_<day>.json (store-guarded cache)
  - pairings : cached /fixtures(league=1,season=2026) row in the api_football sqlite cache (read-only)

Both (1) and (2) call the SAME qual_engine.analyze_team -> info and multiplier can never disagree.
The CONDITIONAL scenarios (le_vale_empate_cond / gana_y_pasa / gana_y_pasa_cond / vivo_mejor_tercero /
depende) MUST come out NEUTRAL (×1.0). Only the 4 point-certain ones adjust.

Run:  .\.venv\Scripts\python.exe analysis/worldcup/qual_engine_fase2_validation.py
"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
ROOT = OUT_DIR.parents[1]
sys.path.insert(0, str(OUT_DIR))
sys.path.insert(0, str(ROOT / "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import build_worldcup_cards as BC      # compute_group_info (the ficha info line)
import worldcup_context_shadow as CTX  # classify_fixture (the multiplier), build_status_maps

STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "context"
CACHE_DB = ROOT / "data" / "cache" / "api_football_cache.sqlite3"
LEAGUE, SEASON = 1, 2026
LAST_ROUND = "Group Stage - 3"


def _latest_standings():
    cands = sorted(STORE_DIR.glob("standings_*.json"))
    if not cands:
        raise SystemExit(f"no cached standings under {STORE_DIR}")
    return cands[-1]


def _pairings():
    """{(home, away)} for the LAST round, from the cached /fixtures row (read-only sqlite)."""
    con = sqlite3.connect(f"file:{CACHE_DB}?mode=ro", uri=True)
    try:
        row = con.execute("SELECT response_json FROM api_cache WHERE path='/fixtures' AND params_json=?",
                          (json.dumps({"league": LEAGUE, "season": SEASON}, separators=(",", ":")),)).fetchone()
    finally:
        con.close()
    payload = json.loads(row[0]) if row else {}
    resp = payload.get("response", payload) if isinstance(payload, dict) else payload
    out = []
    for f in (resp or []):
        if str((f.get("league") or {}).get("round")) != LAST_ROUND:
            continue
        h = ((f.get("teams") or {}).get("home") or {}).get("name")
        a = ((f.get("teams") or {}).get("away") or {}).get("name")
        if h and a:
            out.append((h, a))
    return out


def main():
    src = _latest_standings()
    standings_resp = json.loads(src.read_text(encoding="utf-8"))
    groups, team_group = CTX.build_status_maps(standings_resp)   # production shape
    pairings = _pairings()

    # which 4-team lettered groups are at the last matchday (each team played exactly 2)?
    last_groups = {g: rows for g, rows in groups.items()
                   if g.startswith("Group ") and len(rows) == 4 and all(int(r.get("played", 0)) == 2 for r in rows)}

    lines = []
    lines.append("=" * 96)
    lines.append("FASE 2 VALIDATION — ficha info line (compute_group_info) + multiplier (classify_fixture)")
    lines.append("=" * 96)
    lines.append(f"standings: {src.name} | last-matchday groups: {len(last_groups)} | format: 12 grupos, 8 terceros")
    lines.append("")

    adjusted, neutral = [], []
    for g in sorted(last_groups):
        names = {r["name"] for r in last_groups[g]}
        gp = [(h, a) for (h, a) in pairings if h in names and a in names]
        std = "  ".join(f"{r['name']}={int(r['points'])}" for r in sorted(last_groups[g], key=lambda r: -r["points"]))
        lines.append("-" * 96)
        lines.append(f"{g}:  {std}")
        for (h, a) in gp:
            # (1) the ficha INFO line (honest, conditional) — the SAME for both fixtures of the group
            info = BC.compute_group_info(groups, h, a)
            lines.append(f"  ℹ️ Contexto de grupo [{h} vs {a}]: {info}")
            # (2) the MULTIPLIER decision
            th, ta, mh, ma, nt = CTX.classify_fixture(LAST_ROUND, h, a, groups, team_group)
            verdict = "AJUSTA" if nt else "NEUTRAL"
            lines.append(f"     multiplicador -> {h}: {th} ×{mh}  |  {a}: {ta} ×{ma}   => {verdict}")
            (adjusted if nt else neutral).append((g, h, a, th, ta, mh, ma))
        lines.append("")

    lines.append("=" * 96)
    lines.append(f"RESUMEN MULTIPLICADOR: {len(adjusted)} partidos AJUSTAN · {len(neutral)} NEUTRALES")
    lines.append("=" * 96)
    lines.append("Partidos que AJUSTAN (algún equipo con escenario CIERTO por puntos):")
    for g, h, a, th, ta, mh, ma in adjusted:
        lines.append(f"  {g}: {h}({th} ×{mh}) vs {a}({ta} ×{ma})")
    lines.append("")
    lines.append("Partidos NEUTRALES (condicional/incierto -> sin ajuste, ×1.0 ambos):")
    for g, h, a, th, ta, mh, ma in neutral:
        lines.append(f"  {g}: {h}({th}) vs {a}({ta})")

    out = "\n".join(lines)
    print(out)
    rep = OUT_DIR / "qual_engine_fase2_validation_report.txt"
    rep.write_text(out, encoding="utf-8")
    print(f"\n-> {rep}")


if __name__ == "__main__":
    main()
