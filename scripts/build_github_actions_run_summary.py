from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path

PROCESSED = Path("data/processed")


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter = Counter(n(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def row_status(rows: list[dict[str, str]], section: str) -> str:
    for row in rows:
        if row.get("section") == section:
            return n(row.get("status")) or "UNKNOWN"
    return "UNKNOWN"


def day_path(day: str, filename: str) -> Path:
    return PROCESSED / "today" / day / filename


def summary_status_for_full(day: str) -> tuple[str, list[str]]:
    notes: list[str] = []
    sanity = read_csv(day_path(day, "vsigma_learning_chain_output_sanity.csv"))
    readiness = read_csv(day_path(day, "vsigma_shadow_patch_promotion_readiness.csv"))
    shadow = read_csv(day_path(day, "vsigma_calibration_shadow_patch_queue.csv"))

    if any(row.get("severity") in {"ERROR", "CRITICAL"} for row in sanity):
        return "STOP", ["Learning-chain sanity has ERROR/CRITICAL rows."]
    if any(row.get("sanity_status") in {"EMPTY_WITH_VALID_FALLBACK", "EMPTY_NO_FALLBACK"} for row in sanity):
        notes.append("Sanity warnings detected; inspect fallback/empty outputs.")
    if any(row.get("readiness_decision") == "PROMOTION_CANDIDATE_MANUAL_REVIEW" for row in readiness):
        notes.append("Promotion candidate exists; manual review required.")
    if any(row.get("queue_decision") in {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"} for row in shadow):
        notes.append("Shadow calibration tests active; no production change allowed.")

    if notes:
        return "WARN", notes
    return "OK", ["No blocking learning-chain issues detected."]


def full_post_match_summary(day: str) -> str:
    status, notes = summary_status_for_full(day)
    sanity = read_csv(day_path(day, "vsigma_learning_chain_output_sanity.csv"))
    shadow = read_csv(day_path(day, "vsigma_calibration_shadow_patch_queue.csv"))
    readiness = read_csv(day_path(day, "vsigma_shadow_patch_promotion_readiness.csv"))
    calibration_md = read_text(day_path(day, "vsigma_match_stat_forecast_calibration.md"))

    lines = [
        f"# vSIGMA Full Post-Match Learning Summary — {day}",
        "",
        f"**Run status:** `{status}`",
        "",
        "## Key signals",
        f"- Learning sanity: `{counts(sanity, 'sanity_status')}`",
        f"- Shadow queue: `{counts(shadow, 'queue_decision')}`",
        f"- Shadow priorities: `{counts(shadow, 'shadow_priority')}`",
        f"- Promotion readiness: `{counts(readiness, 'readiness_decision')}`",
        f"- Manual review required: `{counts(readiness, 'manual_review_required')}`",
        "- Auto apply: `NO`",
        "- Production change: `NO`",
        "",
        "## Notes",
    ]
    lines += [f"- {note}" for note in notes]
    if calibration_md:
        lines += ["", "## Calibration excerpt", "```", "\n".join(calibration_md.splitlines()[:18]), "```"]
    return "\n".join(lines) + "\n"


def operator_summary(day: str) -> str:
    rows = read_csv(day_path(day, "vsigma_operator_brief.csv"))
    md_text = read_text(day_path(day, "vsigma_operator_brief.md"))
    action = row_status(rows, "operator_action_level")
    final_decision = row_status(rows, "operator_compact_summary")
    alert_route = row_status(rows, "operator_alert_route")
    sanity = row_status(rows, "operator_sanity_check")
    shadow = row_status(rows, "calibration_shadow_summary")
    promotion = row_status(rows, "shadow_promotion_readiness")
    learning_sanity = row_status(rows, "learning_chain_output_sanity")

    if action in {"BROKEN", "REVIEW_NOW"} or alert_route == "CRITICAL_STOP" or sanity == "FAIL":
        status = "STOP"
    elif alert_route in {"GITHUB_ISSUE_COMMENT", "LOCAL_ONLY"} or learning_sanity == "WARN":
        status = "WARN"
    else:
        status = "OK"

    lines = [
        f"# vSIGMA Operator Brief Summary — {day}",
        "",
        f"**Run status:** `{status}`",
        "",
        "## Operator state",
        f"- Action level: `{action}`",
        f"- Final decision: `{final_decision}`",
        f"- Alert route: `{alert_route}`",
        f"- Sanity: `{sanity}`",
        "",
        "## Calibration governance",
        f"- Shadow status: `{shadow}`",
        f"- Promotion readiness: `{promotion}`",
        f"- Learning sanity: `{learning_sanity}`",
        "- Auto apply: `NO`",
        "- Production change: `NO`",
    ]
    if md_text:
        lines += ["", "## Brief excerpt", "```", "\n".join(md_text.splitlines()[:28]), "```"]
    return "\n".join(lines) + "\n"


def run(day: str, mode: str, output: str | None) -> None:
    day = date.fromisoformat(day).isoformat()
    if mode == "full_post_match":
        text = full_post_match_summary(day)
    elif mode == "operator_brief":
        text = operator_summary(day)
    else:
        raise SystemExit(f"Unsupported mode: {mode}")

    if output:
        out_path = Path(output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    print(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--mode", required=True, choices=["full_post_match", "operator_brief"])
    parser.add_argument("--output", required=False)
    args = parser.parse_args()
    run(args.date, args.mode, args.output)


if __name__ == "__main__":
    main()
