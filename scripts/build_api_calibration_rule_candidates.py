from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
MIN_SAMPLE_FOR_RULE_REVIEW = 50
MIN_SAMPLE_FOR_OBSERVATION = 20

ROW_FIELDS = [
    "target_date", "generated_at", "rule_id", "group_type", "group_value", "market",
    "sample_rows", "evaluated_rows", "hit_rows", "miss_rows", "void_rows", "pending_rows",
    "hit_rate_pct", "hit_or_void_rate_pct", "miss_rate_pct", "calibration_status",
    "sample_warning", "rule_bucket", "rule_decision", "rule_reason", "future_rule_candidate",
    "activation_permission", "canonical_board_permission", "pick_permission", "stake_permission",
    "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "rows_reviewed", "candidate_rows", "block_rows",
    "observe_rows", "insufficient_sample_rows", "rule_bucket_counts", "rule_decision_counts",
    "future_rule_candidate_counts", "activation_permission_counts", "pick_permission_counts",
    "stake_permission_counts", "next_action", "auto_apply", "production_change",
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


def as_float(value: object) -> float:
    try:
        text = norm(value)
        return float(text) if text else 0.0
    except ValueError:
        return 0.0


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


def load_calibration_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_signal_calibration_summary.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_signal_calibration_summary.csv")
    return rows


def evaluate_rule(row: dict[str, str]) -> tuple[str, str, str, str]:
    market = up(row.get("market"))
    group_type = up(row.get("group_type"))
    group_value = up(row.get("group_value"))
    evaluated = as_int(row.get("evaluated_rows"))
    hit_rate = as_float(row.get("hit_rate_pct"))
    hit_or_void = as_float(row.get("hit_or_void_rate_pct"))
    miss_rate = as_float(row.get("miss_rate_pct"))

    if evaluated < MIN_SAMPLE_FOR_OBSERVATION:
        return (
            "RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE",
            "COLLECT_MORE_SAMPLE",
            f"Only {evaluated} evaluated rows; minimum observation sample is {MIN_SAMPLE_FOR_OBSERVATION}.",
            "NO_SAMPLE_TOO_SMALL",
        )

    if market == "API_1X2" and hit_rate < 60:
        return (
            "RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET",
            "BLOCK_ML_PROMOTION",
            f"API 1X2 hit_rate={hit_rate:.1f}% is below the 60% minimum for any ML review.",
            "NO_BLOCKED_MARKET",
        )

    if market in {"BTTS_YES", "OVER_2_5"} and hit_rate < 55:
        return (
            "RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET",
            f"BLOCK_{market}_PROMOTION",
            f"{market} hit_rate={hit_rate:.1f}% is weak/negative in current calibration.",
            "NO_BLOCKED_MARKET",
        )

    if market == "API_DOUBLE_CHANCE" and hit_rate >= 75:
        if evaluated < MIN_SAMPLE_FOR_RULE_REVIEW:
            return (
                "RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE",
                "WATCH_ONLY_COLLECT_TO_50_SAMPLE",
                f"API double chance hit_rate={hit_rate:.1f}% but sample={evaluated} is below {MIN_SAMPLE_FOR_RULE_REVIEW}.",
                "YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS",
            )
        return (
            "RULE_CANDIDATE_PROTECTED_MARKET",
            "FUTURE_RULE_REVIEW_ONLY",
            f"API double chance hit_rate={hit_rate:.1f}% meets protected-market threshold.",
            "YES_REVIEW_ONLY",
        )

    if market == "API_DNB" and hit_or_void >= 75 and miss_rate <= 25:
        if evaluated < MIN_SAMPLE_FOR_RULE_REVIEW:
            return (
                "RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE",
                "WATCH_ONLY_COLLECT_TO_50_SAMPLE",
                f"API DNB hit_or_void={hit_or_void:.1f}% and miss_rate={miss_rate:.1f}% but sample={evaluated} is below {MIN_SAMPLE_FOR_RULE_REVIEW}.",
                "YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS",
            )
        return (
            "RULE_CANDIDATE_PROTECTED_MARKET",
            "FUTURE_RULE_REVIEW_ONLY",
            f"API DNB hit_or_void={hit_or_void:.1f}% and miss_rate={miss_rate:.1f}% meet protected-market threshold.",
            "YES_REVIEW_ONLY",
        )

    if market == "UNDER_3_5" and hit_rate >= 70:
        if evaluated < MIN_SAMPLE_FOR_RULE_REVIEW:
            return (
                "RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE",
                "WATCH_ONLY_COLLECT_TO_50_SAMPLE",
                f"Under 3.5 hit_rate={hit_rate:.1f}% but sample={evaluated} is below {MIN_SAMPLE_FOR_RULE_REVIEW}.",
                "YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS",
            )
        return (
            "RULE_CANDIDATE_TOTAL_MARKET",
            "FUTURE_RULE_REVIEW_ONLY",
            f"Under 3.5 hit_rate={hit_rate:.1f}% meets total-market threshold.",
            "YES_REVIEW_ONLY",
        )

    if market == "OVER_1_5" and hit_rate >= 65:
        if evaluated < MIN_SAMPLE_FOR_RULE_REVIEW:
            return (
                "RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE",
                "WATCH_ONLY_COLLECT_TO_50_SAMPLE",
                f"Over 1.5 hit_rate={hit_rate:.1f}% but sample={evaluated} is below {MIN_SAMPLE_FOR_RULE_REVIEW}.",
                "YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS",
            )
        return (
            "RULE_CANDIDATE_TOTAL_MARKET",
            "FUTURE_RULE_REVIEW_ONLY",
            f"Over 1.5 hit_rate={hit_rate:.1f}% meets total-market threshold.",
            "YES_REVIEW_ONLY",
        )

    if group_type == "ALL":
        return (
            "RULE_NEUTRAL_OBSERVE_MORE",
            "OBSERVE_MORE_GLOBAL_MARKET",
            f"Global market {market} does not meet candidate/block thresholds decisively.",
            "NO_OBSERVE_MORE",
        )

    return (
        "RULE_OBSERVE_ONLY_SEGMENT",
        "OBSERVE_MORE_SEGMENT",
        f"Segment {group_type}={group_value} for {market} needs more sample before rule review.",
        "NO_SEGMENT_SAMPLE_TOO_SMALL",
    )


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_calibration_rows(processed, day)
    out: list[dict[str, object]] = []

    for idx, row in enumerate(rows, start=1):
        bucket, decision, reason, candidate = evaluate_rule(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "rule_id": f"API_CAL_RULE_{idx:04d}",
            "group_type": norm(row.get("group_type")),
            "group_value": norm(row.get("group_value")),
            "market": norm(row.get("market")),
            "sample_rows": as_int(row.get("sample_rows")),
            "evaluated_rows": as_int(row.get("evaluated_rows")),
            "hit_rows": as_int(row.get("hit_rows")),
            "miss_rows": as_int(row.get("miss_rows")),
            "void_rows": as_int(row.get("void_rows")),
            "pending_rows": as_int(row.get("pending_rows")),
            "hit_rate_pct": norm(row.get("hit_rate_pct")),
            "hit_or_void_rate_pct": norm(row.get("hit_or_void_rate_pct")),
            "miss_rate_pct": norm(row.get("miss_rate_pct")),
            "calibration_status": norm(row.get("calibration_status")),
            "sample_warning": norm(row.get("sample_warning")),
            "rule_bucket": bucket,
            "rule_decision": decision,
            "rule_reason": reason,
            "future_rule_candidate": candidate,
            "activation_permission": "NO_RULE_ACTIVATION_PERMISSION",
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    candidate_rows = [r for r in out if str(r["future_rule_candidate"]).startswith("YES")]
    block_rows = [r for r in out if str(r["rule_bucket"]).startswith("RULE_BLOCK")]
    insufficient_rows = [r for r in out if "INSUFFICIENT_SAMPLE" in str(r["rule_bucket"])]
    observe_rows = [r for r in out if r not in candidate_rows and r not in block_rows]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rows_reviewed": len(out),
        "candidate_rows": len(candidate_rows),
        "block_rows": len(block_rows),
        "observe_rows": len(observe_rows),
        "insufficient_sample_rows": len(insufficient_rows),
        "rule_bucket_counts": counts(out, "rule_bucket"),
        "rule_decision_counts": counts(out, "rule_decision"),
        "future_rule_candidate_counts": counts(out, "future_rule_candidate"),
        "activation_permission_counts": counts(out, "activation_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Calibration Rule Candidates - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- candidate_rows: {summary['candidate_rows']}",
        f"- block_rows: {summary['block_rows']}",
        f"- observe_rows: {summary['observe_rows']}",
        f"- insufficient_sample_rows: {summary['insufficient_sample_rows']}",
        f"- rule_bucket_counts: {summary['rule_bucket_counts']}",
        f"- rule_decision_counts: {summary['rule_decision_counts']}",
        f"- future_rule_candidate_counts: {summary['future_rule_candidate_counts']}",
        f"- activation_permission_counts: {summary['activation_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Candidate Rules",
    ]
    candidate_rows = [r for r in rows if str(r["future_rule_candidate"]).startswith("YES")]
    if not candidate_rows:
        lines.append("- none. No rule candidates yet.")
    for row in candidate_rows[:80]:
        lines.append(
            f"- {row['rule_id']} | {row['group_type']}={row['group_value']} | {row['market']} | evaluated={row['evaluated_rows']} | hit={row['hit_rate_pct']} | hit_or_void={row['hit_or_void_rate_pct']} | miss={row['miss_rate_pct']} | decision={row['rule_decision']} | permission={row['activation_permission']} | reason={row['rule_reason']}"
        )
    lines += ["", "## Block Rules"]
    block_rows = [r for r in rows if str(r["rule_bucket"]).startswith("RULE_BLOCK")]
    if not block_rows:
        lines.append("- none.")
    for row in block_rows[:80]:
        lines.append(
            f"- {row['rule_id']} | {row['group_type']}={row['group_value']} | {row['market']} | evaluated={row['evaluated_rows']} | hit={row['hit_rate_pct']} | miss={row['miss_rate_pct']} | decision={row['rule_decision']} | reason={row['rule_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This board is rule-design only.",
        "- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.",
        "- Any future rule must be implemented separately after enough sample size exists and after explicit review.",
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
    section = "## API Calibration Rule Candidates"
    lines = [
        section,
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- candidate_rows: {summary.get('candidate_rows', 'UNKNOWN')}",
        f"- block_rows: {summary.get('block_rows', 'UNKNOWN')}",
        f"- observe_rows: {summary.get('observe_rows', 'UNKNOWN')}",
        f"- rule_bucket_counts: {summary.get('rule_bucket_counts', 'UNKNOWN')}",
        f"- rule_decision_counts: {summary.get('rule_decision_counts', 'UNKNOWN')}",
        f"- future_rule_candidate_counts: {summary.get('future_rule_candidate_counts', 'UNKNOWN')}",
        f"- activation_permission_counts: {summary.get('activation_permission_counts', 'UNKNOWN')}",
        f"- pick_permission_counts: {summary.get('pick_permission_counts', 'UNKNOWN')}",
        f"- stake_permission_counts: {summary.get('stake_permission_counts', 'UNKNOWN')}",
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
        write_csv(base / "vsigma_api_calibration_rule_candidates.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_calibration_rule_candidates_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_calibration_rule_candidates.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API CALIBRATION RULE CANDIDATES ===")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"candidate_rows={summary[0]['candidate_rows']}")
    print(f"block_rows={summary[0]['block_rows']}")
    print(f"activation_permission_counts={summary[0]['activation_permission_counts']}")
    print(f"pick_permission_counts={summary[0]['pick_permission_counts']}")
    print(f"stake_permission_counts={summary[0]['stake_permission_counts']}")
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
