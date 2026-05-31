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
PROBABLE_FILES = [
    "vsigma_probable_lineup_sources.csv",
    "probable_lineup_sources.csv",
    "vsigma_probable_lineup_sources_learning_only.csv",
    "probable_lineup_sources_learning_only.csv",
]
OFFICIAL_FILES = [
    "vsigma_official_lineup_sources.csv",
    "official_lineup_sources.csv",
    "vsigma_fixture_official_lineups.csv",
    "fixture_official_lineups.csv",
]
FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "team_side", "source_name",
    "probable_status", "probable_players_count", "official_players_count", "matched_players_count", "accuracy_11",
    "lineup_accuracy_grade", "matched_players", "missing_players", "wrong_players", "evaluation_status",
    "source_url", "source_guard", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "evaluated_rows", "pending_rows", "learning_only_rows",
    "promoted_rows", "grade_counts", "source_grade_summary", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows([{k: r.get(k, "") for k in fields} for r in rows])


def d(day: str, name: str) -> Path:
    return P / "today" / day / name


def norm_player(x: str) -> str:
    x = s(x).lower()
    x = re.sub(r"\([^)]*\)", " ", x)
    x = re.sub(r"\s+", " ", x)
    x = re.sub(r"[^a-z0-9áéíóúüñçãõàèìòùâêîôû \-']", "", x)
    return x.strip()


def player_list_from_row(row: dict[str, str], *names: str) -> list[str]:
    raw = ""
    for name in names:
        raw = s(row.get(name))
        if raw:
            break
    if raw:
        parts = re.split(r"[;|,]", raw)
    else:
        parts = [s(row.get(f"player_{i}")) for i in range(1, 12)]
    out: list[str] = []
    for p in parts:
        np = norm_player(p)
        if np and np not in out:
            out.append(np)
    return out[:11]


def team_side(row: dict[str, str]) -> str:
    v = s(row.get("team_side") or row.get("side") or row.get("team")).lower()
    if v in {"home", "h", "local", "1"}:
        return "home"
    if v in {"away", "a", "visitante", "2"}:
        return "away"
    return ""


def fixture_rows(day: str) -> dict[str, dict[str, str]]:
    for name in ["matches_vsigma_scored_v3.csv", "vsigma_daily_execution_board.csv", "matches_league_filtered.csv"]:
        rows = read(d(day, name))
        if rows:
            return {s(r.get("fixture_id")): r for r in rows if s(r.get("fixture_id"))}
    return {}


def probable_rows(day: str) -> tuple[list[dict[str, str]], str]:
    out: list[dict[str, str]] = []
    used: list[str] = []
    seen = set()
    for name in PROBABLE_FILES:
        for path in [d(day, name), P / "governance" / name, RAW / name]:
            rows = read(path)
            if not rows:
                continue
            used.append(str(path))
            inferred_status = "LEARNING_ONLY" if "learning_only" in name else "IMPORTED"
            for r in rows:
                fid = s(r.get("fixture_id"))
                side = team_side(r)
                src = s(r.get("source_name") or r.get("source") or r.get("provider")).lower().replace(" ", "_")
                players = player_list_from_row(r, "probable_xi", "players", "xi")
                status = s(r.get("import_status")) or inferred_status
                key = (fid, side, src, status, tuple(players), s(r.get("source_url") or r.get("url")))
                if not fid or not side or not src or not players or key in seen:
                    continue
                seen.add(key)
                rr = dict(r)
                rr["_players"] = ";".join(players)
                rr["_source_file"] = str(path)
                rr["_probable_status"] = status
                out.append(rr)
    return out, ";".join(used) if used else "NO_ACCEPTED_OR_LEARNING_PROBABLE_SOURCE_FILE"


def official_rows_from_files(day: str) -> tuple[dict[tuple[str, str], list[str]], str]:
    official: dict[tuple[str, str], list[str]] = {}
    used: list[str] = []
    for name in OFFICIAL_FILES:
        for path in [d(day, name), P / "governance" / name, RAW / name]:
            rows = read(path)
            if not rows:
                continue
            used.append(str(path))
            for r in rows:
                fid = s(r.get("fixture_id"))
                side = team_side(r)
                players = player_list_from_row(r, "official_xi", "lineup_xi", "starting_xi", "players", "xi")
                if fid and side and players:
                    official[(fid, side)] = players
    return official, ";".join(used) if used else "NO_OFFICIAL_SOURCE_FILE"


def official_rows_from_matches(day: str, fixtures: dict[str, dict[str, str]]) -> tuple[dict[tuple[str, str], list[str]], str]:
    official: dict[tuple[str, str], list[str]] = {}
    for fid, r in fixtures.items():
        home = player_list_from_row(r, "home_official_xi", "home_lineup_xi", "home_starting_xi", "home_lineup_players")
        away = player_list_from_row(r, "away_official_xi", "away_lineup_xi", "away_starting_xi", "away_lineup_players")
        if home:
            official[(fid, "home")] = home
        if away:
            official[(fid, "away")] = away
    return official, "MATCH_COLUMNS" if official else "NO_MATCH_OFFICIAL_PLAYER_COLUMNS"


def grade(matched: int, official_count: int) -> str:
    if official_count <= 0:
        return "NO_OFFICIAL_LINEUP"
    if matched >= 10:
        return "A"
    if matched >= 8:
        return "B"
    if matched >= 6:
        return "C"
    return "D"


def evaluate(probable: list[str], official: list[str]) -> tuple[int, list[str], list[str], list[str]]:
    matches, missing, wrong = match_players(probable, official)
    matched = [f"{m['probable']}~{m['official']}:{m['score']}" for m in matches]
    return len(matches), matched, missing, wrong


def build(day: str, tz: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    fixtures = fixture_rows(day)
    official, official_guard = official_rows_from_files(day)
    official_match, official_match_guard = official_rows_from_matches(day, fixtures)
    official.update({k: v for k, v in official_match.items() if k not in official})
    probs, probable_guard = probable_rows(day)
    rows: list[dict[str, str]] = []
    for p in probs:
        fid = s(p.get("fixture_id"))
        side = team_side(p)
        fixture = fixtures.get(fid, {})
        source = s(p.get("source_name") or p.get("source") or p.get("provider")).lower().replace(" ", "_")
        probable_status = s(p.get("_probable_status")) or "UNKNOWN"
        probable_players = [x for x in s(p.get("_players")).split(";") if x]
        official_players = official.get((fid, side), [])
        if official_players:
            matched_n, matched, missing, wrong = evaluate(probable_players, official_players)
            accuracy = f"{matched_n / 11:.3f}"
            status = "EVALUATED"
            g = grade(matched_n, len(official_players))
        else:
            matched_n, matched, missing, wrong = 0, [], [], probable_players
            accuracy = ""
            status = "NO_OFFICIAL_LINEUP"
            g = "NO_OFFICIAL_LINEUP"
        rows.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fid,
            "home_team": s(fixture.get("home_team")) or s(p.get("home_team")),
            "away_team": s(fixture.get("away_team")) or s(p.get("away_team")),
            "team_side": side,
            "source_name": source,
            "probable_status": probable_status,
            "probable_players_count": str(len(probable_players)),
            "official_players_count": str(len(official_players)),
            "matched_players_count": str(matched_n),
            "accuracy_11": accuracy,
            "lineup_accuracy_grade": g,
            "matched_players": ";".join(matched),
            "missing_players": ";".join(missing),
            "wrong_players": ";".join(wrong),
            "evaluation_status": status,
            "source_url": s(p.get("source_url") or p.get("url")),
            "source_guard": f"probable={probable_guard}; official={official_guard}; match_official={official_match_guard}; matcher=fuzzy_v67_2; promotion_gate=v67_3",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    evaluated = [r for r in rows if r["evaluation_status"] == "EVALUATED"]
    grade_counts = Counter(r["lineup_accuracy_grade"] for r in rows)
    by_source: dict[str, list[str]] = {}
    for r in evaluated:
        by_source.setdefault(r["source_name"], []).append(r["accuracy_11"])
    source_summary = []
    for source, vals in sorted(by_source.items()):
        nums = [float(v) for v in vals if v]
        if nums:
            source_summary.append(f"{source}:n={len(nums)},avg={sum(nums)/len(nums):.3f}")
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": str(len(rows)),
        "evaluated_rows": str(len(evaluated)),
        "pending_rows": str(len(rows) - len(evaluated)),
        "learning_only_rows": str(sum(1 for r in rows if r["probable_status"] == "LEARNING_ONLY")),
        "promoted_rows": str(sum(1 for r in rows if r["probable_status"] == "IMPORTED")),
        "grade_counts": "; ".join(f"{k}={v}" for k, v in grade_counts.items()) if grade_counts else "none",
        "source_grade_summary": "; ".join(source_summary) if source_summary else "none",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return rows, summary


def merge_governance(existing: list[dict[str, str]], new_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for r in existing + new_rows:
        key = (s(r.get("target_date")), s(r.get("fixture_id")), s(r.get("team_side")), s(r.get("source_name")), s(r.get("probable_status")))
        if key[0] and key[1] and key[2] and key[3]:
            merged[key] = r
    return list(merged.values())


def md(day: str, rows: list[dict[str, str]], summary: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Probable XI Accuracy Ledger - {day}", "", "## Summary"]
    if summary:
        r = summary[0]
        lines += [
            f"- rows_reviewed: {r['rows_reviewed']}",
            f"- evaluated_rows: {r['evaluated_rows']}",
            f"- pending_rows: {r['pending_rows']}",
            f"- learning_only_rows: {r['learning_only_rows']}",
            f"- promoted_rows: {r['promoted_rows']}",
            f"- grade_counts: {r['grade_counts']}",
            f"- source_grade_summary: {r['source_grade_summary']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Rows"]
    if not rows:
        lines.append("- none. No accepted or learning-only probable lineup rows after quarantine.")
    for row in rows[:80]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | side={row['team_side']} | source={row['source_name']} "
            f"| probable_status={row['probable_status']} | status={row['evaluation_status']} | grade={row['lineup_accuracy_grade']} "
            f"| match={row['matched_players_count']}/{row['official_players_count']} | probable={row['probable_players_count']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Accuracy ledger is learning-only and never applies production changes.",
        "- IMPORTED rows may feed consensus; LEARNING_ONLY rows are evaluated but must not feed consensus/prelock.",
        "- Accuracy ledger never reads autonomous raw rows directly.",
        "- Fuzzy player matching is used for evaluation only and does not fabricate players.",
        "- Source reliability changes must be handled by a later governor module.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary = build(day, tz)
    today = P / "today" / day
    write(today / "vsigma_probable_lineup_accuracy_ledger.csv", rows, FIELDS)
    write(today / "vsigma_probable_lineup_accuracy_summary.csv", summary, SUMMARY_FIELDS)
    (today / "vsigma_probable_lineup_accuracy_ledger.md").write_text(md(day, rows, summary), encoding="utf-8")

    gov_path = P / "governance" / "vsigma_probable_lineup_accuracy_ledger.csv"
    gov_rows = merge_governance(read(gov_path), rows)
    write(gov_path, gov_rows, FIELDS)
    write(P / "governance" / "vsigma_probable_lineup_accuracy_summary.csv", summary, SUMMARY_FIELDS)
    (P / "governance" / "vsigma_probable_lineup_accuracy_ledger.md").write_text(md(day, rows, summary), encoding="utf-8")

    print("=== VSIGMA PROBABLE XI ACCURACY LEDGER ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed'] if summary else 0}")
    print(f"evaluated_rows={summary[0]['evaluated_rows'] if summary else 0}")
    print(f"learning_only_rows={summary[0]['learning_only_rows'] if summary else 0}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
