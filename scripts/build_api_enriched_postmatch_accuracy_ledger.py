from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
RAW_MATCHES = Path("data/raw/matches.csv")
FINISHED_STATUSES = {"FT", "AET", "PEN"}

ROW_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "league", "country",
    "fixture_status", "result_status", "home_goals", "away_goals", "actual_result",
    "prediction_winner", "predicted_side", "candidate_signal_score", "candidate_signal_band",
    "review_priority", "market_signal_summary", "api_1x2_result", "api_double_chance_result",
    "api_dnb_result", "over_1_5_result", "over_2_5_result", "under_3_5_result", "btts_result",
    "accuracy_bucket", "evaluation_note", "canonical_board_permission", "pick_permission", "stake_permission",
    "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "finished_rows", "pending_rows",
    "accuracy_bucket_counts", "api_1x2_counts", "api_double_chance_counts", "api_dnb_counts",
    "over_1_5_counts", "over_2_5_counts", "under_3_5_counts", "btts_counts",
    "canonical_board_permission_counts", "pick_permission_counts", "stake_permission_counts",
    "next_action", "auto_apply", "production_change",
]

HISTORY_PATH = PROCESSED / "governance" / "vsigma_api_enriched_postmatch_accuracy_ledger_history.csv"


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object):
    text = norm(value)
    if text == "":
        return None
    try:
        return int(float(text))
    except ValueError:
        return None


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def load_api_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_enriched_review_board.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_enriched_review_board.csv")
    return rows


def load_result_rows(raw_matches: Path) -> dict[str, dict[str, str]]:
    rows = read_rows(raw_matches)
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fixture_id = norm(row.get("fixture_id"))
        if fixture_id:
            out[fixture_id] = row
    return out


def value_from(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = norm(row.get(name))
        if value:
            return value
    return ""


def prediction_winner(row: dict[str, str]) -> str:
    explicit = value_from(row, "prediction_winner", "prediction_winner_name")
    if explicit:
        return explicit
    summary = norm(row.get("market_signal_summary"))
    marker = "prediction_winner="
    if marker in summary:
        tail = summary.split(marker, 1)[1]
        return norm(tail.split("|", 1)[0])
    return ""


def candidate_score(row: dict[str, str]) -> int:
    value = as_int(value_from(row, "candidate_signal_score", "score", "review_score", "composite_score"))
    return value if value is not None else 0


def candidate_band(row: dict[str, str]) -> str:
    return value_from(row, "candidate_signal_band", "review_signal_band", "signal_band")


def normalize_team(value: str) -> str:
    return up(value).replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")


def predicted_side(row: dict[str, str], winner: str) -> str:
    winner_n = normalize_team(winner)
    home_n = normalize_team(norm(row.get("home_team")))
    away_n = normalize_team(norm(row.get("away_team")))
    if not winner_n:
        return "UNKNOWN"
    if winner_n in {"DRAW", "EMPATE", "X"}:
        return "DRAW"
    if winner_n == home_n or winner_n in home_n or home_n in winner_n:
        return "HOME"
    if winner_n == away_n or winner_n in away_n or away_n in winner_n:
        return "AWAY"
    return "UNKNOWN"


def result_payload(api_row: dict[str, str], result_row: dict[str, str] | None) -> tuple[str, str, int | None, int | None]:
    status = value_from(api_row, "fixture_status", "fixture_status_short", "status")
    home_goals = None
    away_goals = None
    if result_row:
        status = value_from(result_row, "fixture_status_short", "status", "fixture_status", "fixture_status_long") or status
        home_goals = as_int(value_from(result_row, "goals_home", "score_fulltime_home", "home_goals"))
        away_goals = as_int(value_from(result_row, "goals_away", "score_fulltime_away", "away_goals"))
    if status.upper() not in FINISHED_STATUSES or home_goals is None or away_goals is None:
        return status or "UNKNOWN", "PENDING_RESULT", home_goals, away_goals
    return status, "FINISHED_RESULT", home_goals, away_goals


def actual_result(home_goals: int | None, away_goals: int | None) -> str:
    if home_goals is None or away_goals is None:
        return "UNKNOWN"
    if home_goals > away_goals:
        return "HOME"
    if away_goals > home_goals:
        return "AWAY"
    return "DRAW"


def eval_1x2(side: str, actual: str) -> str:
    if actual == "UNKNOWN" or side == "UNKNOWN":
        return "NOT_EVALUATED"
    return "HIT" if side == actual else "MISS"


def eval_double_chance(side: str, actual: str) -> str:
    if actual == "UNKNOWN" or side not in {"HOME", "AWAY"}:
        return "NOT_EVALUATED"
    if side == "HOME":
        return "HIT" if actual in {"HOME", "DRAW"} else "MISS"
    return "HIT" if actual in {"AWAY", "DRAW"} else "MISS"


def eval_dnb(side: str, actual: str) -> str:
    if actual == "UNKNOWN" or side not in {"HOME", "AWAY"}:
        return "NOT_EVALUATED"
    if actual == "DRAW":
        return "VOID"
    return "HIT" if side == actual else "MISS"


def eval_total(total_goals: int | None, threshold: float, direction: str) -> str:
    if total_goals is None:
        return "NOT_EVALUATED"
    if direction == "OVER":
        return "HIT" if total_goals > threshold else "MISS"
    return "HIT" if total_goals < threshold else "MISS"


def eval_btts(home_goals: int | None, away_goals: int | None) -> str:
    if home_goals is None or away_goals is None:
        return "NOT_EVALUATED"
    return "HIT" if home_goals > 0 and away_goals > 0 else "MISS"


def accuracy_bucket(result_status: str, api_1x2: str, dc: str, dnb: str, over15: str, btts: str) -> str:
    if result_status != "FINISHED_RESULT":
        return "PENDING_RESULT"
    hits = sum(1 for value in [api_1x2, dc, dnb, over15, btts] if value == "HIT")
    misses = sum(1 for value in [api_1x2, dc, dnb, over15, btts] if value == "MISS")
    if hits >= 4 and misses <= 1:
        return "STRONG_SIGNAL_VALIDATED"
    if hits >= 2:
        return "PARTIAL_SIGNAL_VALIDATED"
    if misses >= 3:
        return "SIGNAL_FAILED"
    return "MIXED_SIGNAL"


def build(day: str, tz: str, processed: Path, raw_matches: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    api_rows = load_api_rows(processed, day)
    result_by_fixture = load_result_rows(raw_matches)
    out: list[dict[str, object]] = []

    for row in api_rows:
        fixture_id = norm(row.get("fixture_id"))
        result_row = result_by_fixture.get(fixture_id)
        status, result_status, home_goals, away_goals = result_payload(row, result_row)
        actual = actual_result(home_goals, away_goals)
        winner = prediction_winner(row)
        side = predicted_side(row, winner)
        total = None if home_goals is None or away_goals is None else home_goals + away_goals

        api_1x2 = eval_1x2(side, actual) if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        dc = eval_double_chance(side, actual) if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        dnb = eval_dnb(side, actual) if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        over15 = eval_total(total, 1.5, "OVER") if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        over25 = eval_total(total, 2.5, "OVER") if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        under35 = eval_total(total, 3.5, "UNDER") if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        btts = eval_btts(home_goals, away_goals) if result_status == "FINISHED_RESULT" else "PENDING_RESULT"
        bucket = accuracy_bucket(result_status, api_1x2, dc, dnb, over15, btts)

        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": fixture_id,
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "fixture_status": status,
            "result_status": result_status,
            "home_goals": "" if home_goals is None else home_goals,
            "away_goals": "" if away_goals is None else away_goals,
            "actual_result": actual,
            "prediction_winner": winner,
            "predicted_side": side,
            "candidate_signal_score": candidate_score(row),
            "candidate_signal_band": candidate_band(row),
            "review_priority": norm(row.get("review_priority")),
            "market_signal_summary": norm(row.get("market_signal_summary")),
            "api_1x2_result": api_1x2,
            "api_double_chance_result": dc,
            "api_dnb_result": dnb,
            "over_1_5_result": over15,
            "over_2_5_result": over25,
            "under_3_5_result": under35,
            "btts_result": btts,
            "accuracy_bucket": bucket,
            "evaluation_note": "Postmatch evaluation only. This ledger cannot create picks, stake, or canonical board permission.",
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    finished = [row for row in out if row["result_status"] == "FINISHED_RESULT"]
    pending = [row for row in out if row["result_status"] != "FINISHED_RESULT"]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(out),
        "finished_rows": len(finished),
        "pending_rows": len(pending),
        "accuracy_bucket_counts": counts(out, "accuracy_bucket"),
        "api_1x2_counts": counts(out, "api_1x2_result"),
        "api_double_chance_counts": counts(out, "api_double_chance_result"),
        "api_dnb_counts": counts(out, "api_dnb_result"),
        "over_1_5_counts": counts(out, "over_1_5_result"),
        "over_2_5_counts": counts(out, "over_2_5_result"),
        "under_3_5_counts": counts(out, "under_3_5_result"),
        "btts_counts": counts(out, "btts_result"),
        "canonical_board_permission_counts": counts(out, "canonical_board_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API-Enriched Postmatch Accuracy Ledger - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- finished_rows: {summary['finished_rows']}",
        f"- pending_rows: {summary['pending_rows']}",
        f"- accuracy_bucket_counts: {summary['accuracy_bucket_counts']}",
        f"- api_1x2_counts: {summary['api_1x2_counts']}",
        f"- api_double_chance_counts: {summary['api_double_chance_counts']}",
        f"- api_dnb_counts: {summary['api_dnb_counts']}",
        f"- over_1_5_counts: {summary['over_1_5_counts']}",
        f"- over_2_5_counts: {summary['over_2_5_counts']}",
        f"- under_3_5_counts: {summary['under_3_5_counts']}",
        f"- btts_counts: {summary['btts_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Evaluated Rows",
    ]
    if not rows:
        lines.append("- none. No API-enriched review rows available.")
    for row in rows[:120]:
        score = f"{row['home_goals']}-{row['away_goals']}" if row["result_status"] == "FINISHED_RESULT" else "pending"
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | result={score} | prediction={row['prediction_winner']} | "
            f"side={row['predicted_side']} | signal={row['candidate_signal_score']} {row['candidate_signal_band']} | "
            f"1x2={row['api_1x2_result']} | dc={row['api_double_chance_result']} | dnb={row['api_dnb_result']} | "
            f"o1.5={row['over_1_5_result']} | o2.5={row['over_2_5_result']} | u3.5={row['under_3_5_result']} | btts={row['btts_result']} | bucket={row['accuracy_bucket']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This ledger is postmatch calibration only.",
        "- It does not create picks, stake, canonical board permission, or whitelist permission.",
        "- Historical promotion rules must be implemented separately after enough sample size exists.",
    ]
    return "\n".join(lines) + "\n"


def replace_or_append_section(text: str, section: str, block: str) -> str:
    if section not in text:
        return text.rstrip() + block
    before = text.split(section, 1)[0].rstrip()
    after = text.split(section, 1)[1]
    next_idx = after.find("\n## ")
    tail = after[next_idx:] if next_idx >= 0 else ""
    return before + block + tail


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## API-Enriched Postmatch Accuracy Ledger"
    lines = [
        section,
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- finished_rows: {summary.get('finished_rows', 'UNKNOWN')}",
        f"- pending_rows: {summary.get('pending_rows', 'UNKNOWN')}",
        f"- accuracy_bucket_counts: {summary.get('accuracy_bucket_counts', 'UNKNOWN')}",
        f"- api_1x2_counts: {summary.get('api_1x2_counts', 'UNKNOWN')}",
        f"- api_double_chance_counts: {summary.get('api_double_chance_counts', 'UNKNOWN')}",
        f"- api_dnb_counts: {summary.get('api_dnb_counts', 'UNKNOWN')}",
        f"- over_1_5_counts: {summary.get('over_1_5_counts', 'UNKNOWN')}",
        f"- over_2_5_counts: {summary.get('over_2_5_counts', 'UNKNOWN')}",
        f"- under_3_5_counts: {summary.get('under_3_5_counts', 'UNKNOWN')}",
        f"- btts_counts: {summary.get('btts_counts', 'UNKNOWN')}",
        f"- pick_permission_counts: {summary.get('pick_permission_counts', 'UNKNOWN')}",
        f"- stake_permission_counts: {summary.get('stake_permission_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            text = replace_or_append_section(text, section, block)
            md_path.write_text(text, encoding="utf-8")


def update_history(rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    existing = read_rows(HISTORY_PATH)
    merged: dict[tuple[str, str], dict[str, object]] = {}
    for row in existing:
        key = (norm(row.get("target_date")), norm(row.get("fixture_id")))
        if key[0] and key[1]:
            merged[key] = row
    for row in rows:
        key = (norm(row.get("target_date")), norm(row.get("fixture_id")))
        if key[0] and key[1]:
            merged[key] = row
    ordered = sorted(merged.values(), key=lambda r: (norm(r.get("target_date")), norm(r.get("fixture_id"))))
    write_csv(HISTORY_PATH, ordered, ROW_FIELDS)


def run(day: str, tz: str, processed: Path, raw_matches: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed, raw_matches)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_enriched_postmatch_accuracy_ledger.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_enriched_postmatch_accuracy_ledger_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_enriched_postmatch_accuracy_ledger.md").write_text(md, encoding="utf-8")
    update_history(rows)
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API-ENRICHED POSTMATCH ACCURACY LEDGER ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"finished_rows={summary[0]['finished_rows']}")
    print(f"pending_rows={summary[0]['pending_rows']}")
    print(f"accuracy_bucket_counts={summary[0]['accuracy_bucket_counts']}")
    print(f"pick_permission_counts={summary[0]['pick_permission_counts']}")
    print(f"stake_permission_counts={summary[0]['stake_permission_counts']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    parser.add_argument("--raw-matches", type=Path, default=RAW_MATCHES)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir, args.raw_matches)


if __name__ == "__main__":
    main()
