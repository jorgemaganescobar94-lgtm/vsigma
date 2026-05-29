from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
OPERATOR_FIELDS = ["target_date", "generated_at", "section", "status", "detail", "next_action"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_operator_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OPERATOR_FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in OPERATOR_FIELDS} for row in rows])


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def source(day: str, filename: str) -> tuple[list[dict[str, str]], str]:
    today_path = PROCESSED / "today" / day / filename
    governance_path = PROCESSED / "governance" / filename
    rows = read_csv(today_path)
    if rows:
        return rows, str(today_path)
    rows = read_csv(governance_path)
    if rows:
        return rows, str(governance_path)
    return [], str(today_path)


def compact_metrics(rows: list[dict[str, str]], decision_fields: set[str]) -> str:
    metrics = []
    for row in rows:
        decision = row.get("queue_decision") or row.get("readiness_decision") or ""
        if decision in decision_fields:
            metric = row.get("metric") or "UNKNOWN"
            if metric not in metrics:
                metrics.append(metric)
    return ",".join(metrics) if metrics else "none"


def build_summary(day: str) -> dict[str, str]:
    shadow_rows, shadow_source = source(day, "vsigma_calibration_shadow_patch_queue.csv")
    readiness_rows, readiness_source = source(day, "vsigma_shadow_patch_promotion_readiness.csv")
    sanity_rows, sanity_source = source(day, "vsigma_learning_chain_output_sanity.csv")

    active_shadow = [row for row in shadow_rows if row.get("queue_decision") in {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}]
    high_shadow = [row for row in active_shadow if row.get("shadow_priority") == "HIGH"]
    promotion_candidates = [row for row in readiness_rows if row.get("readiness_decision") == "PROMOTION_CANDIDATE_MANUAL_REVIEW"]
    keep_shadow = [row for row in readiness_rows if row.get("readiness_decision") == "KEEP_SHADOW_TEST"]
    sanity_warn = [row for row in sanity_rows if row.get("severity") in {"WARN", "ERROR", "CRITICAL"}]

    if active_shadow:
        shadow_status = "ACTIVE"
    elif shadow_rows:
        shadow_status = "STABLE_OR_NO_PATCH"
    else:
        shadow_status = "UNAVAILABLE"

    if promotion_candidates:
        promotion_status = "MANUAL_REVIEW_CANDIDATE"
    elif keep_shadow:
        promotion_status = "KEEP_SHADOW_TEST"
    elif readiness_rows:
        promotion_status = "NO_PROMOTION"
    else:
        promotion_status = "UNAVAILABLE"

    if sanity_warn:
        sanity_status = "WARN"
    elif sanity_rows:
        sanity_status = "PASS"
    else:
        sanity_status = "UNAVAILABLE"

    return {
        "shadow_status": shadow_status,
        "shadow_active_count": str(len(active_shadow)),
        "shadow_high_count": str(len(high_shadow)),
        "shadow_metrics": compact_metrics(shadow_rows, {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}),
        "shadow_decisions": counts(shadow_rows, "queue_decision"),
        "shadow_source": shadow_source,
        "promotion_status": promotion_status,
        "promotion_candidates": str(len(promotion_candidates)),
        "promotion_decisions": counts(readiness_rows, "readiness_decision"),
        "promotion_source": readiness_source,
        "learning_sanity_status": sanity_status,
        "learning_sanity_counts": counts(sanity_rows, "sanity_status"),
        "learning_sanity_severity": counts(sanity_rows, "severity"),
        "learning_sanity_source": sanity_source,
    }


def addendum_md(summary: dict[str, str]) -> str:
    lines = [
        "## Calibration / Shadow Governance",
        f"- calibration_shadow_status: {summary['shadow_status']}",
        f"- shadow_active_candidates: {summary['shadow_active_count']}",
        f"- shadow_high_priority: {summary['shadow_high_count']}",
        f"- shadow_metrics: {summary['shadow_metrics']}",
        f"- shadow_decisions: {summary['shadow_decisions']}",
        f"- promotion_readiness: {summary['promotion_status']}",
        f"- promotion_candidates: {summary['promotion_candidates']}",
        f"- promotion_decisions: {summary['promotion_decisions']}",
        f"- learning_sanity_status: {summary['learning_sanity_status']}",
        f"- learning_sanity_counts: {summary['learning_sanity_counts']}",
        f"- learning_sanity_severity: {summary['learning_sanity_severity']}",
        "- calibration_auto_apply: NO",
        "- production_change: NO",
        "",
        "### Calibration Sources",
        f"- shadow_queue: {summary['shadow_source']}",
        f"- promotion_readiness: {summary['promotion_source']}",
        f"- learning_sanity: {summary['learning_sanity_source']}",
    ]
    return "\n".join(lines) + "\n"


def strip_existing_addendum(text: str) -> str:
    marker = "\n## Calibration / Shadow Governance\n"
    idx = text.find(marker)
    if idx == -1:
        return text.rstrip() + "\n"
    return text[:idx].rstrip() + "\n"


def append_csv_rows(path: Path, day: str, generated_at: str, summary: dict[str, str]) -> None:
    rows = read_csv(path)
    rows = [row for row in rows if row.get("section") not in {
        "calibration_shadow_summary",
        "shadow_promotion_readiness",
        "learning_chain_output_sanity",
    }]
    rows.extend([
        {
            "target_date": day,
            "generated_at": generated_at,
            "section": "calibration_shadow_summary",
            "status": summary["shadow_status"],
            "detail": f"active={summary['shadow_active_count']}; high={summary['shadow_high_count']}; metrics={summary['shadow_metrics']}; decisions={summary['shadow_decisions']}",
            "next_action": "Read shadow queue; no auto-apply.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "section": "shadow_promotion_readiness",
            "status": summary["promotion_status"],
            "detail": f"promotion_candidates={summary['promotion_candidates']}; decisions={summary['promotion_decisions']}",
            "next_action": "Manual review only if promotion candidate appears.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "section": "learning_chain_output_sanity",
            "status": summary["learning_sanity_status"],
            "detail": f"status_counts={summary['learning_sanity_counts']}; severity={summary['learning_sanity_severity']}",
            "next_action": "Review sanity warnings before trusting learning outputs.",
        },
    ])
    write_operator_csv(path, rows)


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    summary = build_summary(day)
    block = addendum_md(summary)

    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        md_path = base / "vsigma_operator_brief.md"
        csv_path = base / "vsigma_operator_brief.csv"
        text = strip_existing_addendum(read_text(md_path))
        write_text(md_path, text + "\n" + block)
        append_csv_rows(csv_path, day, generated_at, summary)

    print("=== VSIGMA OPERATOR BRIEF CALIBRATION ADDENDUM ===")
    print(f"calibration_shadow_status={summary['shadow_status']}")
    print(f"shadow_high_priority={summary['shadow_high_count']}")
    print(f"promotion_readiness={summary['promotion_status']}")
    print(f"learning_sanity_status={summary['learning_sanity_status']}")
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
