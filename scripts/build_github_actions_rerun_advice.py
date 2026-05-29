from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

PROCESSED = Path("data/processed")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def day_path(day: str, filename: str) -> Path:
    return PROCESSED / "today" / day / filename


def full_post_match_advice(day: str) -> str:
    guard = read_csv(day_path(day, "vsigma_learning_chain_empty_output_guard.csv"))
    sanity = read_csv(day_path(day, "vsigma_learning_chain_output_sanity.csv"))
    blocked = any(row.get("commit_allowed") == "NO" for row in guard)
    warned = any(row.get("guard_decision") == "WARN_ONLY" for row in guard)
    empty_with_fallback = any(row.get("sanity_status") == "EMPTY_WITH_VALID_FALLBACK" for row in sanity)
    empty_no_fallback = any(row.get("sanity_status") == "EMPTY_NO_FALLBACK" for row in sanity)

    lines = ["## Rerun / self-healing advice"]
    if blocked:
        lines += [
            "- Status: `STOP`.",
            "- Rerun workflow: `vSIGMA Full Post-Match Learning Chain`.",
            f"- Use date: `{day}`.",
            "- Inspect first: `vsigma_learning_chain_empty_output_guard.md`.",
            "- Then inspect: `vsigma_learning_chain_output_sanity.md`.",
            "- Do not trust degraded learning outputs until rerun passes.",
        ]
    elif empty_with_fallback:
        lines += [
            "- Status: `WARN`.",
            "- Same-date fallback exists for at least one empty output.",
            f"- Optional rerun: `vSIGMA Full Post-Match Learning Chain` with date `{day}`.",
            "- Fallback-safe scripts may still produce usable shadow outputs.",
        ]
    elif warned or empty_no_fallback:
        lines += [
            "- Status: `WARN`.",
            f"- Optional rerun after late data settles: `vSIGMA Full Post-Match Learning Chain` with date `{day}`.",
            "- Review sanity output before using calibration changes.",
        ]
    else:
        lines += ["- Status: `OK`.", "- No rerun required."]
    lines += ["- Auto apply: `NO`.", "- Production change: `NO`."]
    return "\n".join(lines) + "\n"


def operator_advice(day: str) -> str:
    rows = read_csv(day_path(day, "vsigma_operator_brief.csv"))
    by_section = {row.get("section", ""): row for row in rows}
    action = by_section.get("operator_action_level", {}).get("status", "UNKNOWN")
    alert = by_section.get("operator_alert_route", {}).get("status", "UNKNOWN")
    sanity = by_section.get("operator_sanity_check", {}).get("status", "UNKNOWN")
    learning = by_section.get("learning_chain_output_sanity", {}).get("status", "UNKNOWN")

    lines = ["## Rerun / self-healing advice"]
    if action in {"BROKEN", "REVIEW_NOW"} or alert == "CRITICAL_STOP" or sanity == "FAIL":
        lines += [
            "- Status: `STOP`.",
            "- Rerun workflow after fixing source issue: `vSIGMA Daily Operator Brief`.",
            f"- Use date: `{day}`.",
            "- Inspect: `vsigma_operator_brief.md` and `vsigma_operator_brief.csv`.",
        ]
    elif alert in {"LOCAL_ONLY", "GITHUB_ISSUE_COMMENT"} or learning == "WARN":
        lines += [
            "- Status: `WARN`.",
            f"- Optional rerun: `vSIGMA Daily Operator Brief` with date `{day}` after related workflow completes.",
            "- Review alert route and calibration addendum before manual action.",
        ]
    elif action == "LIVE":
        lines += [
            "- Status: `LIVE`.",
            "- No rerun required unless the live window changes.",
            "- Use live validator/recheck workflow before manual live review.",
        ]
    else:
        lines += ["- Status: `OK`.", "- No rerun required."]
    lines += ["- Auto apply: `NO`.", "- Production change: `NO`."]
    return "\n".join(lines) + "\n"


def run(day: str, mode: str, output: str | None) -> None:
    day = date.fromisoformat(day).isoformat()
    text = full_post_match_advice(day) if mode == "full_post_match" else operator_advice(day)
    if output:
        path = Path(output)
        with path.open("a", encoding="utf-8") as file:
            file.write("\n")
            file.write(text)
    print(text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--mode", required=True, choices=["full_post_match", "operator_brief"])
    parser.add_argument("--output")
    args = parser.parse_args()
    run(args.date, args.mode, args.output)


if __name__ == "__main__":
    main()
