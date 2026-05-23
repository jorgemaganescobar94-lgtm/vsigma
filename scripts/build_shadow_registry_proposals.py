from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "proposal_rank", "proposed_experiment_id",
    "source_factory_experiment_id", "pattern_key", "experiment_type", "shadow_status",
    "activation_scope", "baseline_policy", "candidate_policy", "expected_effect",
    "sample_requirements", "promotion_gate", "production_impact", "auto_apply",
    "guardrail_status", "proposal_action"
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


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


def source(processed: Path, target_date: str, filename: str) -> Path:
    p = processed / "today" / target_date / filename
    return p if p.exists() else processed / "governance" / filename


def exp_type(pattern: str) -> str:
    p = up(pattern)
    if "OVER_2_5" in p and "LOW_CONVERSION" in p:
        return "LOW_CONVERSION_OVER25_SHRINKAGE_SHADOW"
    if "WAITING_PRELOCK" in p:
        return "PRELOCK_LOW_CONVERSION_TIMING_SHADOW"
    if "OVER_1_5" in p and "LOW_CONVERSION" in p:
        return "LOW_CONVERSION_OVER15_SHRINKAGE_SHADOW"
    return "GENERIC_SHADOW_REVIEW"


def proposed_id(pattern: str) -> str:
    return f"SHADOW::{exp_type(pattern)}::{pattern}"


def candidate_policy(pattern: str) -> str:
    p = up(pattern)
    if "OVER_2_5" in p:
        return "For matching candidates, apply shadow-only downgrade/check requiring stricter price, chance-volume, and conversion evidence before treating OVER_2_5 as premium."
    if "WAITING_PRELOCK" in p:
        return "For matching candidates, shadow-block execution until prelock timing and result state are confirmed."
    return "For matching candidates, apply shadow-only downgrade/check requiring stronger conversion evidence."


def expected_effect(pattern: str) -> str:
    if "LOW_CONVERSION" in up(pattern):
        return "Reduce false positives in low-conversion over/goal clusters while preserving official baseline picks."
    return "Measure whether the shadow rule improves decision quality without touching production."


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    sync_rows = read_rows(source(processed, target_date, "vsigma_shadow_registry_sync.csv"))
    rows: list[dict[str, object]] = []
    for row in sync_rows:
        if up(row.get("sync_status")) != "REGISTRY_CREATE_NEEDED":
            continue
        pattern = norm(row.get("pattern_key"))
        rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "proposal_rank": len(rows) + 1,
            "proposed_experiment_id": proposed_id(pattern),
            "source_factory_experiment_id": norm(row.get("factory_experiment_id")),
            "pattern_key": pattern,
            "experiment_type": exp_type(pattern),
            "shadow_status": "ACTIVE_SHADOW_ONLY",
            "activation_scope": "MATCHING_FUTURE_CANDIDATES_ONLY",
            "baseline_policy": "CURRENT_PRODUCTION_LOGIC_UNCHANGED",
            "candidate_policy": candidate_policy(pattern),
            "expected_effect": expected_effect(pattern),
            "sample_requirements": "Minimum 30 closed matching samples before promotion review; prefer 50+ if variance is high.",
            "promotion_gate": "Promotion requires better decision quality, no worse drawdown, no increased missed winners, and separate promotion gate approval.",
            "production_impact": "NONE",
            "auto_apply": "NO",
            "guardrail_status": "REGISTRY_PROPOSAL_ONLY_NO_AUTO_WRITE",
            "proposal_action": "REVIEW_AND_APPEND_TO_SHADOW_REGISTRY_IF_ACCEPTED",
        })
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Shadow Registry Proposals - {target_date}", "",
        "## Summary",
        f"- proposal_rows: {len(rows)}",
        f"- experiment_type_counts: {counts(rows, 'experiment_type')}",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Proposed Registry Rows",
    ]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- #{r['proposal_rank']} | {r['experiment_type']} | pattern={r['pattern_key']} | action={r['proposal_action']}")
    lines += ["", "## Guardrails", "- This report does not modify vsigma_shadow_experiments.csv.", "- Registry append requires separate review/PR.", "- Production picks remain unchanged."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_shadow_registry_proposals.csv", rows)
        (base / "vsigma_shadow_registry_proposals.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA SHADOW REGISTRY PROPOSALS ===")
    print(f"proposal_rows={len(rows)}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
