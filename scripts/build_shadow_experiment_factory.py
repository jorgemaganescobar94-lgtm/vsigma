from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
MIN_REVIEW_SAMPLE = 30
FIELDS = [
    "target_date", "generated_at", "experiment_id", "source_readiness_rank",
    "pattern_key", "readiness_state", "sample_count", "closed_sample_count",
    "shadow_status", "shadow_hypothesis", "shadow_rule", "min_review_sample",
    "next_action", "auto_apply", "production_change", "guardrail_status"
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def as_int(v: object) -> int:
    try:
        return int(float(norm(v) or 0))
    except ValueError:
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def source_path(processed: Path, target_date: str) -> Path:
    p = processed / "today" / target_date / "vsigma_pattern_promotion_readiness.csv"
    return p if p.exists() else processed / "governance" / "vsigma_pattern_promotion_readiness.csv"


def experiment_id(pattern: str) -> str:
    clean = "_".join(part for part in pattern.replace("::", "_").replace("/", "_").split() if part)
    return f"shadow_{clean.lower()}"[:120]


def hypothesis(pattern: str) -> str:
    if "FAILURE_MODE_LOW_CONVERSION" in up(pattern):
        return "Test whether low-conversion risk should downgrade or delay similar over/goal markets."
    if "WAITING_PRELOCK" in up(pattern):
        return "Test whether prelock timing state should gate execution more strictly."
    return "Test whether this repeated pattern improves outcomes in shadow mode."


def rule(pattern: str) -> str:
    p = up(pattern)
    if "FAILURE_MODE_LOW_CONVERSION" in p and "OVER_1_5" in p:
        return "Shadow downgrade OVER_1_5 when failure_mode_low_conversion is present until stronger conversion evidence appears."
    if "FAILURE_MODE_LOW_CONVERSION" in p and "OVER_2_5" in p:
        return "Shadow downgrade OVER_2_5 when failure_mode_low_conversion is present unless odds/price and chance volume clear stricter gates."
    if "WAITING_PRELOCK" in p:
        return "Shadow block execution until prelock window confirms timing and status."
    return "Shadow monitor only; no production behavior change."


def status(row: dict[str, str]) -> str:
    state = up(row.get("readiness_state"))
    closed = as_int(row.get("closed_sample_count"))
    if state == "SHADOW_REQUIRED":
        return "CREATE_SHADOW_ONLY"
    if state == "BLOCKED_BY_SAMPLE_SIZE":
        return "CONTINUE_SHADOW_ONLY" if closed > 0 else "CREATE_SHADOW_ONLY"
    return "NO_SHADOW_ACTION"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    rows = read_rows(source_path(processed, target_date))
    out: list[dict[str, object]] = []
    for row in rows:
        state = up(row.get("readiness_state"))
        if state not in {"SHADOW_REQUIRED", "BLOCKED_BY_SAMPLE_SIZE"}:
            continue
        pattern = norm(row.get("pattern_key"))
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "experiment_id": experiment_id(pattern),
            "source_readiness_rank": norm(row.get("readiness_rank")),
            "pattern_key": pattern,
            "readiness_state": state,
            "sample_count": as_int(row.get("sample_count")),
            "closed_sample_count": as_int(row.get("closed_sample_count")),
            "shadow_status": status(row),
            "shadow_hypothesis": hypothesis(pattern),
            "shadow_rule": rule(pattern),
            "min_review_sample": MIN_REVIEW_SAMPLE,
            "next_action": "FORWARD_TEST_SHADOW_ONLY",
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "SHADOW_FACTORY_REPORT_ONLY_NO_PRODUCTION_CHANGE",
        })
    out.sort(key=lambda r: (0 if r["shadow_status"] == "CREATE_SHADOW_ONLY" else 1, -int(r["sample_count"]), str(r["experiment_id"])))
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Experiment Factory - {target_date}", "",
        "## Summary",
        f"- shadow_experiments: {len(rows)}",
        f"- shadow_status_counts: {counts(rows, 'shadow_status')}",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Experiments",
    ]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- {r['experiment_id']} | {r['shadow_status']} | pattern={r['pattern_key']} | sample={r['sample_count']} | closed={r['closed_sample_count']} | rule={r['shadow_rule']}")
    lines += ["", "## Guardrails", "- Shadow experiments do not change production picks.", "- Promotion still requires clean data, closed sample threshold, and separate review."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_shadow_experiment_factory.csv", rows)
        (base / "vsigma_shadow_experiment_factory.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA SHADOW EXPERIMENT FACTORY ===")
    print(f"shadow_experiments={len(rows)}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
