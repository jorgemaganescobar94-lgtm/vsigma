from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from vsigma_player_name_matcher import match_players

P = Path("data/processed")
RAW = Path("data/raw")
INPUT_NAMES = [
    "probable_lineup_sources.csv",
    "probable_lineup_sources_manual.csv",
    "probable_lineup_sources_autonomous.csv",
    "vsigma_probable_lineup_sources_manual.csv",
    "vsigma_probable_lineup_sources_autonomous.csv",
]
OFFICIAL_NAMES = [
    "vsigma_official_lineup_sources.csv",
    "official_lineup_sources.csv",
    "vsigma_fixture_official_lineups.csv",
    "fixture_official_lineups.csv",
]
OUT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "league", "country", "home_team", "away_team",
    "team_side", "source_name", "source_url", "probable_xi", "input_file", "import_status",
    "import_reason", "quality_score", "quality_notes", "auto_apply", "production_change",
]
TEMPLATE_FIELDS = [
    "target_date", "fixture_id", "league", "country", "home_team", "away_team",
    "team_side", "source_name", "source_url", "probable_xi", "notes",
]
REPORT_FIELDS = [
    "target_date", "generated_at", "rows_seen", "rows_imported", "rows_learning_only", "rows_rejected", "rows_quarantined",
    "input_files", "import_status_counts", "quarantine_reason_counts", "sources_seen", "template_rows",
    "auto_apply", "production_change",
]
BAD_TOKEN_PATTERNS = [
    "lineup", "line-up", "prediction", "preview", "team news", "possible", "starting", "eleven",
    "sports mole", "odds", "betting", "injured", "doubtful", "unavailable", "substitutes",
    "formation", "manager", "coach", "vs ", "latest", "match", "confirmed", "probable",
]
PROMOTION_MATCH_THRESHOLD = 8
QUARANTINE_MATCH_THRESHOLD = 2


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day, name):
    return P / "today" / day / name


def norm_player(x: str) -> str:
    x = s(x).lower()
    x = re.sub(r"\([^)]*\)", " ", x)
    x = re.sub(r"\s+", " ", x)
    x = re.sub(r"[^a-z0-9áéíóúüñçãõàèìòùâêîôû \-']", "", x)
    return x.strip()


def split_players(raw: str) -> list[str]:
    if not s(raw):
        return []
    parts = re.split(r"[;|,]", s(raw))
    out = []
    for p in parts:
        np = norm_player(p)
        if np and np not in out:
            out.append(np)
    return out[:11]


def fixture_rows(day):
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_daily_execution_board.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows:
            return rows, name
    return [], "NONE"


def registry_sources(day):
    rows = read(d(day, "vsigma_probable_lineup_source_registry.csv")) or read(P / "governance" / "vsigma_probable_lineup_source_registry.csv")
    return [s(r.get("source_name")) for r in rows if s(r.get("source_name")) and s(r.get("enabled")).upper() == "YES"]


def input_rows(day):
    out = []
    used = []
    for name in INPUT_NAMES:
        for path in [d(day, name), P / "governance" / name, RAW / name]:
            rows = read(path)
            if rows:
                for r in rows:
                    rr = dict(r)
                    rr["_input_file"] = str(path)
                    out.append(rr)
                used.append(str(path))
    return out, used


def norm_side(x):
    v = s(x).lower()
    if v in {"home", "h", "local", "1"}:
        return "home"
    if v in {"away", "a", "visitante", "2"}:
        return "away"
    return ""


def norm_source(x):
    return s(x).lower().replace(" ", "_")


def fixture_map(fixtures):
    return {s(r.get("fixture_id")): r for r in fixtures if s(r.get("fixture_id"))}


def official_map(day):
    out = {}
    for name in OFFICIAL_NAMES:
        for path in [d(day, name), P / "governance" / name, RAW / name]:
            rows = read(path)
            for r in rows:
                fid = s(r.get("fixture_id"))
                side = norm_side(r.get("team_side") or r.get("side") or r.get("team"))
                raw = s(r.get("official_xi") or r.get("lineup_xi") or r.get("starting_xi") or r.get("players") or r.get("xi"))
                players = split_players(raw)
                if fid and side and players:
                    out[(fid, side)] = players
    return out


def bad_token_hits(players):
    hits = []
    for p in players:
        for bad in BAD_TOKEN_PATTERNS:
            if bad in p:
                hits.append(f"{p}:{bad}")
                break
    return hits


def quality_gate(players, official_players):
    unique_players = list(dict.fromkeys(players))
    bad_hits = bad_token_hits(unique_players)
    notes = []
    score = min(1.0, len(unique_players) / 11.0)
    if len(unique_players) < 8:
        return "QUARANTINED", "player_count_low", score, f"players={len(unique_players)}"
    if bad_hits:
        score = max(0.0, score - 0.35)
        return "QUARANTINED", "bad_text_tokens", score, "|".join(bad_hits[:5])
    long_fragments = [p for p in unique_players if len(p.split()) >= 6]
    if long_fragments:
        score = max(0.0, score - 0.25)
        return "QUARANTINED", "name_fragment_too_long", score, "|".join(long_fragments[:5])
    if len(official_players) >= 10:
        matches, _, _ = match_players(unique_players, official_players)
        overlap = len(matches)
        match_preview = ",".join(f"{m['probable']}~{m['official']}:{m['score']}" for m in matches[:5])
        notes.append(f"fuzzy_official_overlap={overlap}/{len(official_players)}")
        notes.append(f"promotion_gate={PROMOTION_MATCH_THRESHOLD}/11")
        if match_preview:
            notes.append(f"matches={match_preview}")
        if overlap <= QUARANTINE_MATCH_THRESHOLD:
            score = max(0.0, overlap / 11.0)
            return "QUARANTINED", "official_overlap_too_low", score, ";".join(notes)
        if overlap < PROMOTION_MATCH_THRESHOLD:
            score = max(0.0, overlap / 11.0)
            return "LEARNING_ONLY", "below_promotion_accuracy_gate", score, ";".join(notes)
    return "IMPORTED", "OK", score, ";".join(notes) if notes else "quality_ok"


def import_row(row, fixtures_by, officials, day, generated):
    fixture_id = s(row.get("fixture_id"))
    fx = fixtures_by.get(fixture_id, {})
    side = norm_side(row.get("team_side") or row.get("side") or row.get("team"))
    source = norm_source(row.get("source_name") or row.get("source") or row.get("provider"))
    xi = s(row.get("probable_xi") or row.get("players") or row.get("xi"))
    status = "IMPORTED"
    reason = "OK"
    q_score = ""
    q_notes = ""
    players = split_players(xi)
    if not fixture_id or fixture_id not in fixtures_by:
        status, reason = "REJECTED", "fixture_id_not_in_daily_fixtures"
    elif side not in {"home", "away"}:
        status, reason = "REJECTED", "team_side_missing_or_invalid"
    elif not source:
        status, reason = "REJECTED", "source_name_missing"
    elif not xi:
        status, reason = "REJECTED", "probable_xi_empty"
    else:
        status, reason, score, q_notes = quality_gate(players, officials.get((fixture_id, side), []))
        q_score = f"{score:.3f}"
    return {
        "target_date": day,
        "generated_at": generated,
        "fixture_id": fixture_id,
        "league": s(fx.get("league")) or s(row.get("league")),
        "country": s(fx.get("country")) or s(row.get("country")),
        "home_team": s(fx.get("home_team")) or s(row.get("home_team")),
        "away_team": s(fx.get("away_team")) or s(row.get("away_team")),
        "team_side": side,
        "source_name": source,
        "source_url": s(row.get("source_url") or row.get("url")),
        "probable_xi": ";".join(players) if players else xi,
        "input_file": s(row.get("_input_file")),
        "import_status": status,
        "import_reason": reason,
        "quality_score": q_score,
        "quality_notes": q_notes,
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build_template(day, fixtures, sources):
    active_sources = [x for x in sources if x] or ["sportsmole", "whoscored", "rotowire"]
    rows = []
    for fx in fixtures:
        for side in ["home", "away"]:
            for source in active_sources[:5]:
                rows.append({
                    "target_date": day,
                    "fixture_id": s(fx.get("fixture_id")),
                    "league": s(fx.get("league")),
                    "country": s(fx.get("country")),
                    "home_team": s(fx.get("home_team")),
                    "away_team": s(fx.get("away_team")),
                    "team_side": side,
                    "source_name": source,
                    "source_url": "",
                    "probable_xi": "",
                    "notes": "Fill probable_xi as semicolon-separated 11 players. Leave blank if unavailable.",
                })
    return rows


def md(day, report, imported_rows, learning_rows, quarantine_rows, rejected_rows):
    lines = [
        f"# vSIGMA Probable Lineup Source Import - {day}",
        "",
        "## Summary",
    ]
    if report:
        r = report[0]
        lines += [
            f"- rows_seen: {r['rows_seen']}",
            f"- rows_imported: {r['rows_imported']}",
            f"- rows_learning_only: {r['rows_learning_only']}",
            f"- rows_rejected: {r['rows_rejected']}",
            f"- rows_quarantined: {r['rows_quarantined']}",
            f"- input_files: {r['input_files']}",
            f"- import_status_counts: {r['import_status_counts']}",
            f"- quarantine_reason_counts: {r['quarantine_reason_counts']}",
            f"- sources_seen: {r['sources_seen']}",
            f"- template_rows: {r['template_rows']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Imported Rows"]
    if not imported_rows:
        lines.append("- none. No probable XI rows passed promotion gate for consensus.")
    for r in imported_rows[:50]:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | side={r['team_side']} | source={r['source_name']} | status={r['import_status']} | reason={r['import_reason']} | q={r.get('quality_score','')} | notes={r.get('quality_notes','')}")
    lines += ["", "## Learning Only Rows"]
    if not learning_rows:
        lines.append("- none.")
    for r in learning_rows[:50]:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | side={r['team_side']} | source={r['source_name']} | reason={r['import_reason']} | q={r.get('quality_score','')} | notes={r.get('quality_notes','')}")
    lines += ["", "## Quarantined Rows"]
    if not quarantine_rows:
        lines.append("- none.")
    for r in quarantine_rows[:50]:
        lines.append(f"- {r['home_team']} vs {r['away_team']} | side={r['team_side']} | source={r['source_name']} | reason={r['import_reason']} | q={r.get('quality_score','')} | notes={r.get('quality_notes','')}")
    lines += ["", "## Rejected Rows"]
    if not rejected_rows:
        lines.append("- none.")
    for r in rejected_rows[:30]:
        lines.append(f"- fixture={r['fixture_id']} | side={r['team_side']} | source={r['source_name']} | reason={r['import_reason']}")
    lines += [
        "",
        "## Guardrails",
        "- IMPORTED rows may feed consensus/prelock.",
        "- LEARNING_ONLY rows may feed accuracy ledger but must not feed consensus.",
        "- Bad extraction quarantine blocks low-quality rows before consensus and accuracy ledger.",
        "- Fuzzy player matching is used only for official-overlap validation, not to create players.",
        "- Probable XI never equals official lineup.",
    ]
    return "\n".join(lines) + "\n"


def run(day, tz):
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    fixtures, fixture_source = fixture_rows(day)
    fx_by = fixture_map(fixtures)
    officials = official_map(day)
    sources = registry_sources(day)
    raw_rows, input_files = input_rows(day)
    normalized = [import_row(r, fx_by, officials, day, generated) for r in raw_rows]
    imported = [r for r in normalized if r["import_status"] == "IMPORTED"]
    learning_only = [r for r in normalized if r["import_status"] == "LEARNING_ONLY"]
    rejected = [r for r in normalized if r["import_status"] == "REJECTED"]
    quarantined = [r for r in normalized if r["import_status"] == "QUARANTINED"]
    template = build_template(day, fixtures, sources)
    status_counts = Counter(r["import_status"] for r in normalized)
    quarantine_counts = Counter(r["import_reason"] for r in quarantined)
    source_counts = Counter(r["source_name"] for r in normalized if r.get("source_name"))
    report = [{
        "target_date": day,
        "generated_at": generated,
        "rows_seen": len(normalized),
        "rows_imported": len(imported),
        "rows_learning_only": len(learning_only),
        "rows_rejected": len(rejected),
        "rows_quarantined": len(quarantined),
        "input_files": ";".join(input_files) if input_files else "none",
        "import_status_counts": "; ".join(f"{k}={v}" for k, v in status_counts.items()) if status_counts else "none",
        "quarantine_reason_counts": "; ".join(f"{k}={v}" for k, v in quarantine_counts.items()) if quarantine_counts else "none",
        "sources_seen": "; ".join(f"{k}={v}" for k, v in source_counts.items()) if source_counts else "none",
        "template_rows": len(template),
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_probable_lineup_sources.csv", imported, OUT_FIELDS)
        write(base / "probable_lineup_sources.csv", imported, OUT_FIELDS)
        write(base / "vsigma_probable_lineup_sources_learning_only.csv", learning_only, OUT_FIELDS)
        write(base / "probable_lineup_sources_learning_only.csv", learning_only, OUT_FIELDS)
        write(base / "vsigma_probable_lineup_sources_quarantine.csv", quarantined, OUT_FIELDS)
        write(base / "vsigma_probable_lineup_source_import_report.csv", report, REPORT_FIELDS)
        write(base / "vsigma_probable_lineup_source_import_template.csv", template, TEMPLATE_FIELDS)
        (base / "vsigma_probable_lineup_source_import_report.md").write_text(md(day, report, imported, learning_only, quarantined, rejected), encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP SOURCE IMPORT ===")
    print(f"fixture_source={fixture_source}")
    print(f"rows_seen={len(normalized)}")
    print(f"rows_imported={len(imported)}")
    print(f"rows_learning_only={len(learning_only)}")
    print(f"rows_quarantined={len(quarantined)}")
    print(f"rows_rejected={len(rejected)}")
    print("auto_apply=NO")
    print("production_change=NO")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
