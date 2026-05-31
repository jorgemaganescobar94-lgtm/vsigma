from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
REGISTRY = P / "governance" / "vsigma_probable_lineup_source_registry.csv"
ACCURACY = P / "governance" / "vsigma_probable_lineup_accuracy_ledger.csv"
EXTRACTION = P / "governance" / "vsigma_probable_lineup_extraction_quality_ledger.csv"

FIELDS = [
    "target_date", "generated_at", "source_name", "current_status", "current_reliability_score",
    "current_priority_weight", "evaluated_rows", "promoted_rows", "learning_only_rows", "avg_accuracy",
    "grade_counts", "quarantine_rows", "parser_failure_rows", "parser_failure_classes",
    "sample_gate", "reliability_verdict", "recommended_registry_action", "recommended_weight_action",
    "reason", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "sources_reviewed", "sample_gate_counts", "verdict_counts",
    "recommended_action_counts", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def fnum(x, default=0.0):
    try:
        t = s(x)
        return float(t) if t else default
    except ValueError:
        return default


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{k: row.get(k, "") for k in fields} for row in rows])


def d(day: str, name: str) -> Path:
    return P / "today" / day / name


def registry_rows(day: str) -> dict[str, dict[str, str]]:
    rows = read(d(day, "vsigma_probable_lineup_source_registry.csv")) or read(REGISTRY)
    out = {}
    for row in rows:
        name = s(row.get("source_name"))
        if name:
            out[name] = row
    return out


def all_accuracy_rows(day: str) -> list[dict[str, str]]:
    seen = set()
    out = []
    for path in [ACCURACY, d(day, "vsigma_probable_lineup_accuracy_ledger.csv")]:
        for row in read(path):
            key = (
                s(row.get("target_date")), s(row.get("fixture_id")), s(row.get("team_side")),
                s(row.get("source_name")), s(row.get("probable_status")), s(row.get("matched_players_count")),
            )
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out


def all_extraction_rows(day: str) -> list[dict[str, str]]:
    seen = set()
    out = []
    for path in [EXTRACTION, d(day, "vsigma_probable_lineup_extraction_quality_ledger.csv")]:
        for row in read(path):
            key = (s(row.get("target_date")), s(row.get("source_name")), s(row.get("import_reason")), s(row.get("rows")))
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out


def sample_gate(evaluated: int, promoted: int, learning: int) -> str:
    if evaluated < 5:
        return "INSUFFICIENT_SAMPLE"
    if promoted < 3:
        return "INSUFFICIENT_PROMOTED_SAMPLE"
    if evaluated < 12:
        return "EARLY_SAMPLE"
    return "MATURE_SAMPLE"


def verdict(avg_accuracy: float, evaluated: int, promoted: int, parser_failures: int) -> tuple[str, str, str, str]:
    if evaluated < 5:
        return (
            "HOLD_SAMPLE",
            "KEEP_ACTIVE_NO_WEIGHT_CHANGE",
            "NO_WEIGHT_CHANGE",
            "sample below minimum; learn more before changing registry",
        )
    if parser_failures >= evaluated and promoted == 0:
        return (
            "PARSER_BLOCKED_HOLD_SOURCE",
            "KEEP_ACTIVE_REVIEW_PARSER",
            "NO_WEIGHT_CHANGE",
            "evidence points to parser/extraction failure rather than source failure",
        )
    if promoted < 3:
        return (
            "HOLD_PROMOTION",
            "KEEP_ACTIVE_NO_WEIGHT_CHANGE",
            "NO_WEIGHT_CHANGE",
            "not enough promoted rows to adjust source reliability",
        )
    if avg_accuracy >= 0.78:
        return (
            "RELIABLE_CANDIDATE",
            "CONSIDER_SMALL_UPWEIGHT_AFTER_CONFIRMATION",
            "ADVISORY_UPWEIGHT_ONLY",
            "strong accuracy but still requires consecutive non-regression before registry edit",
        )
    if avg_accuracy >= 0.62:
        return (
            "USABLE_SUPPORTING_SOURCE",
            "KEEP_ACTIVE_NO_WEIGHT_CHANGE",
            "NO_WEIGHT_CHANGE",
            "source can support consensus but does not justify upweight",
        )
    if avg_accuracy >= 0.45:
        return (
            "LEARNING_ONLY_SOURCE",
            "KEEP_ACTIVE_BUT_REQUIRE_PROMOTION_GATE",
            "NO_WEIGHT_CHANGE",
            "accuracy is below promotion quality; use for learning only until improved",
        )
    return (
        "WEAK_OR_BAD_EXTRACTION_SIGNAL",
        "KEEP_ACTIVE_REVIEW_PARSER_FIRST",
        "NO_WEIGHT_CHANGE",
        "low accuracy; do not punish source until parser/fetch issues are separated",
    )


def build(day: str, tz: str):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    registry = registry_rows(day)
    accuracy = all_accuracy_rows(day)
    extraction = all_extraction_rows(day)

    by_source = defaultdict(list)
    for row in accuracy:
        name = s(row.get("source_name"))
        if name:
            by_source[name].append(row)

    extraction_by_source = defaultdict(list)
    for row in extraction:
        name = s(row.get("source_name"))
        if name:
            extraction_by_source[name].append(row)

    sources = sorted(set(registry) | set(by_source) | set(extraction_by_source))
    rows = []
    for source in sources:
        acc_rows = by_source.get(source, [])
        evaluated = [r for r in acc_rows if s(r.get("evaluation_status")) == "EVALUATED"]
        promoted = [r for r in evaluated if s(r.get("probable_status")) == "IMPORTED"]
        learning = [r for r in evaluated if s(r.get("probable_status")) == "LEARNING_ONLY"]
        accuracies = [fnum(r.get("accuracy_11"), 0.0) for r in evaluated if s(r.get("accuracy_11"))]
        avg = sum(accuracies) / len(accuracies) if accuracies else 0.0
        grades = Counter(s(r.get("lineup_accuracy_grade")) or "UNKNOWN" for r in evaluated)

        ext_rows = extraction_by_source.get(source, [])
        quarantine_rows = sum(int(fnum(r.get("quarantined_rows"), 0)) for r in ext_rows)
        parser_failures = sum(
            int(fnum(r.get("rows"), 0))
            for r in ext_rows
            if "PARSER" in s(r.get("parser_failure_class")) or "BOUNDARY" in s(r.get("parser_failure_class"))
        )
        parser_classes = Counter(s(r.get("parser_failure_class")) or "UNKNOWN" for r in ext_rows)

        reg = registry.get(source, {})
        gate = sample_gate(len(evaluated), len(promoted), len(learning))
        rel, action, weight_action, reason = verdict(avg, len(evaluated), len(promoted), parser_failures)
        if gate.startswith("INSUFFICIENT") and rel not in {"PARSER_BLOCKED_HOLD_SOURCE"}:
            action = "KEEP_ACTIVE_COLLECT_MORE_DATA"
            weight_action = "NO_WEIGHT_CHANGE"

        rows.append({
            "target_date": day,
            "generated_at": generated,
            "source_name": source,
            "current_status": s(reg.get("status")) or "UNKNOWN",
            "current_reliability_score": s(reg.get("reliability_score")),
            "current_priority_weight": s(reg.get("priority_weight")),
            "evaluated_rows": str(len(evaluated)),
            "promoted_rows": str(len(promoted)),
            "learning_only_rows": str(len(learning)),
            "avg_accuracy": f"{avg:.3f}",
            "grade_counts": "; ".join(f"{k}={v}" for k, v in grades.items()) if grades else "none",
            "quarantine_rows": str(quarantine_rows),
            "parser_failure_rows": str(parser_failures),
            "parser_failure_classes": "; ".join(f"{k}={v}" for k, v in parser_classes.items()) if parser_classes else "none",
            "sample_gate": gate,
            "reliability_verdict": rel,
            "recommended_registry_action": action,
            "recommended_weight_action": weight_action,
            "reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "sources_reviewed": str(len(rows)),
        "sample_gate_counts": "; ".join(f"{k}={v}" for k, v in Counter(r["sample_gate"] for r in rows).items()) if rows else "none",
        "verdict_counts": "; ".join(f"{k}={v}" for k, v in Counter(r["reliability_verdict"] for r in rows).items()) if rows else "none",
        "recommended_action_counts": "; ".join(f"{k}={v}" for k, v in Counter(r["recommended_registry_action"] for r in rows).items()) if rows else "none",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return rows, summary


def md(day: str, rows: list[dict[str, str]], summary: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Probable Lineup Source Reliability Governor - {day}", "", "## Summary"]
    if summary:
        r = summary[0]
        lines += [
            f"- sources_reviewed: {r['sources_reviewed']}",
            f"- sample_gate_counts: {r['sample_gate_counts']}",
            f"- verdict_counts: {r['verdict_counts']}",
            f"- recommended_action_counts: {r['recommended_action_counts']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Source Verdicts"]
    if not rows:
        lines.append("- none. Need accuracy or extraction-quality rows first.")
    for r in rows:
        lines.append(
            f"- {r['source_name']} | verdict={r['reliability_verdict']} | gate={r['sample_gate']} "
            f"| evaluated={r['evaluated_rows']} | promoted={r['promoted_rows']} | learning={r['learning_only_rows']} "
            f"| avg={r['avg_accuracy']} | action={r['recommended_registry_action']} | weight={r['recommended_weight_action']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Governor is advisory only and never edits the registry automatically.",
        "- No source is downweighted from parser/extraction failures alone.",
        "- Upweight recommendations require larger samples and manual confirmation.",
        "- No picks, stakes, or production decisions are changed here.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_probable_lineup_source_reliability_governor.csv", rows, FIELDS)
        write(base / "vsigma_probable_lineup_source_reliability_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_probable_lineup_source_reliability_governor.md").write_text(md(day, rows, summary), encoding="utf-8")
    print("=== VSIGMA PROBABLE LINEUP SOURCE RELIABILITY GOVERNOR ===")
    print(f"sources_reviewed={summary[0]['sources_reviewed'] if summary else 0}")
    print(f"verdict_counts={summary[0]['verdict_counts'] if summary else 'none'}")
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
