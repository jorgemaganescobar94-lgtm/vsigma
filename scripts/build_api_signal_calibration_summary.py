from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
HISTORY_PATH = PROCESSED / "governance" / "vsigma_api_enriched_postmatch_accuracy_ledger_history.csv"

MARKETS = [
    ("api_1x2_result", "API_1X2"),
    ("api_double_chance_result", "API_DOUBLE_CHANCE"),
    ("api_dnb_result", "API_DNB"),
    ("over_1_5_result", "OVER_1_5"),
    ("over_2_5_result", "OVER_2_5"),
    ("under_3_5_result", "UNDER_3_5"),
    ("btts_result", "BTTS_YES"),
]

ROW_FIELDS = [
    "target_date", "generated_at", "group_type", "group_value", "market", "sample_rows",
    "evaluated_rows", "hit_rows", "miss_rows", "void_rows", "pending_rows", "not_evaluated_rows",
    "hit_rate_pct", "hit_or_void_rate_pct", "miss_rate_pct", "calibration_status",
    "sample_warning", "recommended_use", "canonical_board_permission", "pick_permission",
    "stake_permission", "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "source_rows", "finished_rows", "pending_rows",
    "summary_rows", "top_market_by_hit_rate", "top_market_by_hit_or_void_rate",
    "sample_warning_counts", "calibration_status_counts", "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


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
    return "; ".join(f"{k}={v}" for k, v in counter.most_common()) if counter else "none"


def load_ledger_rows(processed: Path, day: str) -> list[dict[str, str]]:
    history = read_rows(HISTORY_PATH)
    if history:
        return history
    rows = read_rows(processed / "today" / day / "vsigma_api_enriched_postmatch_accuracy_ledger.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_enriched_postmatch_accuracy_ledger.csv")
    return rows


def score_bucket(row: dict[str, str]) -> str:
    score = as_int(row.get("candidate_signal_score"))
    if score >= 90:
        return "SCORE_90_PLUS"
    if score >= 80:
        return "SCORE_80_89"
    if score >= 70:
        return "SCORE_70_79"
    if score >= 55:
        return "SCORE_55_69"
    return "SCORE_BELOW_55"


def source_groups(row: dict[str, str]) -> list[tuple[str, str]]:
    return [
        ("ALL", "ALL"),
        ("SIGNAL_BAND", norm(row.get("candidate_signal_band")) or "UNKNOWN_SIGNAL_BAND"),
        ("REVIEW_PRIORITY", norm(row.get("review_priority")) or "UNKNOWN_REVIEW_PRIORITY"),
        ("PREDICTED_SIDE", norm(row.get("predicted_side")) or "UNKNOWN_SIDE"),
        ("SCORE_BUCKET", score_bucket(row)),
    ]


def pct(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return ""
    return f"{(100.0 * numerator / denominator):.1f}"


def sample_warning(evaluated: int) -> str:
    if evaluated < 20:
        return "INSUFFICIENT_SAMPLE_UNDER_20"
    if evaluated < 50:
        return "LOW_SAMPLE_UNDER_50"
    if evaluated < 100:
        return "MEDIUM_SAMPLE_UNDER_100"
    return "SAMPLE_OK_100_PLUS"


def calibration_status(market: str, hit_rows: int, miss_rows: int, void_rows: int, evaluated_rows: int) -> str:
    if evaluated_rows < 20:
        return "CALIBRATION_OBSERVE_ONLY"
    hit_rate = hit_rows / evaluated_rows if evaluated_rows else 0.0
    hit_or_void_rate = (hit_rows + void_rows) / evaluated_rows if evaluated_rows else 0.0
    if market == "API_DNB":
        if hit_or_void_rate >= 0.75 and miss_rows / evaluated_rows <= 0.25:
            return "CALIBRATION_STRONG_PROTECTED_MARKET"
        if hit_or_void_rate >= 0.65:
            return "CALIBRATION_MEDIUM_PROTECTED_MARKET"
    if hit_rate >= 0.75:
        return "CALIBRATION_STRONG_OBSERVED_EDGE"
    if hit_rate >= 0.65:
        return "CALIBRATION_MEDIUM_OBSERVED_EDGE"
    if hit_rate < 0.50:
        return "CALIBRATION_WEAK_OR_NEGATIVE"
    return "CALIBRATION_NEUTRAL"


def recommended_use(status: str, warning: str) -> str:
    if warning.startswith("INSUFFICIENT") or warning.startswith("LOW_SAMPLE"):
        return "REVIEW_ONLY_COLLECT_MORE_SAMPLE"
    if status in {"CALIBRATION_STRONG_OBSERVED_EDGE", "CALIBRATION_STRONG_PROTECTED_MARKET"}:
        return "CANDIDATE_FOR_FUTURE_RULE_REVIEW_ONLY"
    if status in {"CALIBRATION_MEDIUM_OBSERVED_EDGE", "CALIBRATION_MEDIUM_PROTECTED_MARKET"}:
        return "WATCHLIST_FOR_FUTURE_RULE_REVIEW_ONLY"
    if status == "CALIBRATION_WEAK_OR_NEGATIVE":
        return "DO_NOT_PROMOTE_FROM_THIS_BUCKET"
    return "REVIEW_ONLY_NO_PROMOTION"


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_ledger_rows(processed, day)
    grouped: dict[tuple[str, str, str], list[str]] = defaultdict(list)

    for row in rows:
        for group_type, group_value in source_groups(row):
            for field, market in MARKETS:
                grouped[(group_type, group_value, market)].append(up(row.get(field)) or "NOT_EVALUATED")

    out: list[dict[str, object]] = []
    for (group_type, group_value, market), values in sorted(grouped.items()):
        hit_rows = sum(1 for value in values if value == "HIT")
        miss_rows = sum(1 for value in values if value == "MISS")
        void_rows = sum(1 for value in values if value == "VOID")
        pending_rows = sum(1 for value in values if value == "PENDING_RESULT")
        not_evaluated_rows = sum(1 for value in values if value in {"NOT_EVALUATED", ""})
        evaluated_rows = hit_rows + miss_rows + void_rows
        warning = sample_warning(evaluated_rows)
        status = calibration_status(market, hit_rows, miss_rows, void_rows, evaluated_rows)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "group_type": group_type,
            "group_value": group_value,
            "market": market,
            "sample_rows": len(values),
            "evaluated_rows": evaluated_rows,
            "hit_rows": hit_rows,
            "miss_rows": miss_rows,
            "void_rows": void_rows,
            "pending_rows": pending_rows,
            "not_evaluated_rows": not_evaluated_rows,
            "hit_rate_pct": pct(hit_rows, evaluated_rows),
            "hit_or_void_rate_pct": pct(hit_rows + void_rows, evaluated_rows),
            "miss_rate_pct": pct(miss_rows, evaluated_rows),
            "calibration_status": status,
            "sample_warning": warning,
            "recommended_use": recommended_use(status, warning),
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    finished_rows = sum(1 for row in rows if up(row.get("result_status")) == "FINISHED_RESULT")
    pending_rows = sum(1 for row in rows if up(row.get("result_status")) != "FINISHED_RESULT")
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "source_rows": len(rows),
        "finished_rows": finished_rows,
        "pending_rows": pending_rows,
        "summary_rows": len(out),
        "top_market_by_hit_rate": top_market(out, "hit_rate_pct"),
        "top_market_by_hit_or_void_rate": top_market(out, "hit_or_void_rate_pct"),
        "sample_warning_counts": counts(out, "sample_warning"),
        "calibration_status_counts": counts(out, "calibration_status"),
        "next_action": "Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def top_market(rows: list[dict[str, object]], field: str) -> str:
    eligible = [row for row in rows if int(row.get("evaluated_rows") or 0) >= 20 and norm(row.get(field))]
    if not eligible:
        return "none_sample_too_small"
    best = max(eligible, key=lambda row: float(row.get(field) or 0.0))
    return f"{best['group_type']}={best['group_value']} | {best['market']} | {field}={best[field]} | evaluated={best['evaluated_rows']}"


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Signal Calibration Summary - {day}",
        "",
        "## Summary",
        f"- source_rows: {summary['source_rows']}",
        f"- finished_rows: {summary['finished_rows']}",
        f"- pending_rows: {summary['pending_rows']}",
        f"- summary_rows: {summary['summary_rows']}",
        f"- top_market_by_hit_rate: {summary['top_market_by_hit_rate']}",
        f"- top_market_by_hit_or_void_rate: {summary['top_market_by_hit_or_void_rate']}",
        f"- sample_warning_counts: {summary['sample_warning_counts']}",
        f"- calibration_status_counts: {summary['calibration_status_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Global Market Calibration",
    ]
    global_rows = [row for row in rows if row["group_type"] == "ALL"]
    for row in sorted(global_rows, key=lambda r: r["market"]):
        lines.append(
            f"- {row['market']} | evaluated={row['evaluated_rows']} | HIT={row['hit_rows']} | MISS={row['miss_rows']} | VOID={row['void_rows']} | hit_rate={row['hit_rate_pct']} | hit_or_void={row['hit_or_void_rate_pct']} | status={row['calibration_status']} | sample={row['sample_warning']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )
    lines += ["", "## Signal Band Calibration"]
    band_rows = [row for row in rows if row["group_type"] == "SIGNAL_BAND"]
    for row in sorted(band_rows, key=lambda r: (str(r["group_value"]), str(r["market"]))):
        lines.append(
            f"- {row['group_value']} | {row['market']} | evaluated={row['evaluated_rows']} | HIT={row['hit_rows']} | MISS={row['miss_rows']} | VOID={row['void_rows']} | hit_rate={row['hit_rate_pct']} | hit_or_void={row['hit_or_void_rate_pct']} | status={row['calibration_status']} | sample={row['sample_warning']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This summary is calibration-only.",
        "- It does not create picks, stake, canonical board permission, whitelist permission, or execution permission.",
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
    section = "## API Signal Calibration Summary"
    lines = [
        section,
        f"- source_rows: {summary.get('source_rows', 'UNKNOWN')}",
        f"- finished_rows: {summary.get('finished_rows', 'UNKNOWN')}",
        f"- pending_rows: {summary.get('pending_rows', 'UNKNOWN')}",
        f"- summary_rows: {summary.get('summary_rows', 'UNKNOWN')}",
        f"- top_market_by_hit_rate: {summary.get('top_market_by_hit_rate', 'UNKNOWN')}",
        f"- top_market_by_hit_or_void_rate: {summary.get('top_market_by_hit_or_void_rate', 'UNKNOWN')}",
        f"- sample_warning_counts: {summary.get('sample_warning_counts', 'UNKNOWN')}",
        f"- calibration_status_counts: {summary.get('calibration_status_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            md_path.write_text(replace_or_append_section(text, section, block), encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_signal_calibration_summary.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_signal_calibration_summary_meta.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_signal_calibration_summary.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API SIGNAL CALIBRATION SUMMARY ===")
    print(f"source_rows={summary[0]['source_rows']}")
    print(f"finished_rows={summary[0]['finished_rows']}")
    print(f"pending_rows={summary[0]['pending_rows']}")
    print(f"summary_rows={summary[0]['summary_rows']}")
    print(f"top_market_by_hit_rate={summary[0]['top_market_by_hit_rate']}")
    print(f"top_market_by_hit_or_void_rate={summary[0]['top_market_by_hit_or_void_rate']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
