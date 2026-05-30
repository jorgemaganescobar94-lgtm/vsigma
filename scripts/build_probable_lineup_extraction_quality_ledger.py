from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

P = Path("data/processed")
LEDGER_FIELDS = [
    "target_date", "generated_at", "source_name", "import_reason", "rows", "fixture_count",
    "accepted_rows", "quarantined_rows", "avg_quality_score", "parser_failure_class",
    "priority", "recommended_action", "example_notes", "auto_apply", "production_change",
]
QUEUE_FIELDS = [
    "target_date", "generated_at", "priority", "source_name", "issue_type", "evidence_count",
    "recommended_patch", "promotion_rule", "auto_apply", "production_change",
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "sources_reviewed", "quarantine_rows", "accepted_rows",
    "queue_items", "priority_counts", "failure_class_counts", "auto_apply", "production_change",
]


def s(x):
    return "" if x is None else str(x).strip()


def n(x, default=0.0):
    try:
        t = s(x)
        return float(t) if t else default
    except ValueError:
        return default


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


def classify(reason: str) -> tuple[str, str, str, str]:
    r = s(reason)
    if r == "official_overlap_too_low":
        return (
            "PARSER_EXTRACTION_FAILURE",
            "HIGH",
            "Keep rows quarantined; improve page section targeting and do not downgrade source reliability from these rows.",
            "Promote parser patch only after extracted XI reaches >=8/11 official overlap on at least 3 fixtures.",
        )
    if r == "name_fragment_too_long":
        return (
            "TEXT_BOUNDARY_FAILURE",
            "HIGH",
            "Tighten regex boundaries and reject narrative fragments before player splitting.",
            "Promote after narrative-fragment quarantine falls below 5% of extracted rows for 3 runs.",
        )
    if r == "bad_text_tokens":
        return (
            "BAD_TOKEN_FAILURE",
            "MEDIUM",
            "Expand bad-token patterns and require player-like tokens before import.",
            "Promote after bad-token rows remain blocked without reducing valid XI imports.",
        )
    if r == "player_count_low":
        return (
            "LOW_PLAYER_COUNT_FAILURE",
            "MEDIUM",
            "Keep minimum player count gate and improve extraction around XI blocks.",
            "Promote after valid rows show >=8 player names consistently.",
        )
    if r == "OK":
        return (
            "ACCEPTED_SIGNAL",
            "NONE",
            "No parser action required.",
            "No promotion needed.",
        )
    return (
        "OTHER_IMPORT_FAILURE",
        "LOW",
        "Review only if repeated across multiple fixtures.",
        "Promote only with repeated evidence.",
    )


def build(day: str, tz: str):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    quarantine = read(d(day, "vsigma_probable_lineup_sources_quarantine.csv")) + read(P / "governance" / "vsigma_probable_lineup_sources_quarantine.csv")
    accepted = read(d(day, "vsigma_probable_lineup_sources.csv")) + read(P / "governance" / "vsigma_probable_lineup_sources.csv")

    seen_q = set()
    q_rows = []
    for r in quarantine:
        key = (s(r.get("target_date")), s(r.get("fixture_id")), s(r.get("team_side")), s(r.get("source_name")), s(r.get("probable_xi")), s(r.get("import_reason")))
        if key in seen_q:
            continue
        seen_q.add(key)
        q_rows.append(r)

    seen_a = set()
    a_rows = []
    for r in accepted:
        key = (s(r.get("target_date")), s(r.get("fixture_id")), s(r.get("team_side")), s(r.get("source_name")), s(r.get("probable_xi")))
        if key in seen_a:
            continue
        seen_a.add(key)
        a_rows.append(r)

    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for r in q_rows:
        groups[(s(r.get("source_name")) or "unknown", s(r.get("import_reason")) or "unknown")].append(r)
    for r in a_rows:
        groups[(s(r.get("source_name")) or "unknown", "OK")].append(r)

    accepted_by_source = Counter(s(r.get("source_name")) or "unknown" for r in a_rows)
    ledger = []
    queue = []
    for (source, reason), rows in sorted(groups.items()):
        fclass, priority, action, promotion = classify(reason)
        qs = [n(r.get("quality_score"), -1) for r in rows if s(r.get("quality_score"))]
        avg_q = sum(qs) / len(qs) if qs else 0.0
        fixtures = {s(r.get("fixture_id")) for r in rows if s(r.get("fixture_id"))}
        examples = []
        for r in rows[:3]:
            note = s(r.get("quality_notes")) or s(r.get("import_reason"))
            if note and note not in examples:
                examples.append(note[:120])
        quarantine_count = len(rows) if reason != "OK" else 0
        accepted_count = len(rows) if reason == "OK" else accepted_by_source.get(source, 0)
        ledger.append({
            "target_date": day,
            "generated_at": generated,
            "source_name": source,
            "import_reason": reason,
            "rows": str(len(rows)),
            "fixture_count": str(len(fixtures)),
            "accepted_rows": str(accepted_count),
            "quarantined_rows": str(quarantine_count),
            "avg_quality_score": f"{avg_q:.3f}",
            "parser_failure_class": fclass,
            "priority": priority,
            "recommended_action": action,
            "example_notes": " | ".join(examples),
            "auto_apply": "NO",
            "production_change": "NO",
        })
        if priority in {"HIGH", "MEDIUM"} and quarantine_count > 0:
            queue.append({
                "target_date": day,
                "generated_at": generated,
                "priority": priority,
                "source_name": source,
                "issue_type": fclass,
                "evidence_count": str(quarantine_count),
                "recommended_patch": action,
                "promotion_rule": promotion,
                "auto_apply": "NO",
                "production_change": "NO",
            })

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "sources_reviewed": str(len({r["source_name"] for r in ledger})),
        "quarantine_rows": str(len(q_rows)),
        "accepted_rows": str(len(a_rows)),
        "queue_items": str(len(queue)),
        "priority_counts": "; ".join(f"{k}={v}" for k, v in Counter(r["priority"] for r in queue).items()) if queue else "none",
        "failure_class_counts": "; ".join(f"{k}={v}" for k, v in Counter(r["issue_type"] for r in queue).items()) if queue else "none",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return ledger, queue, summary


def md_ledger(day: str, ledger: list[dict[str, str]], summary: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Probable XI Extraction Quality Ledger - {day}", "", "## Summary"]
    if summary:
        r = summary[0]
        lines += [
            f"- sources_reviewed: {r['sources_reviewed']}",
            f"- quarantine_rows: {r['quarantine_rows']}",
            f"- accepted_rows: {r['accepted_rows']}",
            f"- queue_items: {r['queue_items']}",
            f"- priority_counts: {r['priority_counts']}",
            f"- failure_class_counts: {r['failure_class_counts']}",
            "- auto_apply: NO",
            "- production_change: NO",
        ]
    lines += ["", "## Source / Reason Rows"]
    if not ledger:
        lines.append("- none. No accepted or quarantined probable XI rows found.")
    for r in ledger:
        lines.append(
            f"- {r['source_name']} | reason={r['import_reason']} | class={r['parser_failure_class']} | priority={r['priority']} "
            f"| rows={r['rows']} | accepted={r['accepted_rows']} | quarantined={r['quarantined_rows']} | q={r['avg_quality_score']}"
        )
    lines += ["", "## Guardrails", "- This ledger is diagnostic only.", "- It must not reduce source reliability automatically.", "- Parser changes require later validation/promotion rules."]
    return "\n".join(lines) + "\n"


def md_queue(day: str, queue: list[dict[str, str]]) -> str:
    lines = [f"# vSIGMA Probable XI Parser Improvement Queue - {day}", "", "## Queue"]
    if not queue:
        lines.append("- none.")
    for r in queue:
        lines.append(
            f"- {r['priority']} | {r['source_name']} | {r['issue_type']} | evidence={r['evidence_count']} | patch={r['recommended_patch']} | promotion={r['promotion_rule']}"
        )
    lines += ["", "## Guardrails", "- Queue is advisory only.", "- No parser patch is promoted automatically from a single bad run.", "- Source reliability is protected from parser failures."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    ledger, queue, summary = build(day, tz)
    for base in [P / "today" / day, P / "governance"]:
        write(base / "vsigma_probable_lineup_extraction_quality_ledger.csv", ledger, LEDGER_FIELDS)
        write(base / "vsigma_probable_lineup_parser_improvement_queue.csv", queue, QUEUE_FIELDS)
        write(base / "vsigma_probable_lineup_extraction_quality_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_probable_lineup_extraction_quality_ledger.md").write_text(md_ledger(day, ledger, summary), encoding="utf-8")
        (base / "vsigma_probable_lineup_parser_improvement_queue.md").write_text(md_queue(day, queue), encoding="utf-8")
    print("=== VSIGMA PROBABLE XI EXTRACTION QUALITY LEDGER ===")
    print(f"sources_reviewed={summary[0]['sources_reviewed'] if summary else 0}")
    print(f"quarantine_rows={summary[0]['quarantine_rows'] if summary else 0}")
    print(f"queue_items={summary[0]['queue_items'] if summary else 0}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    a = p.parse_args()
    run(a.date, a.timezone)


if __name__ == "__main__":
    main()
