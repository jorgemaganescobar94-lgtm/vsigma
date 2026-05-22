from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_PROCESSED_DIR = Path("data/processed")
MIN_SHADOW_SAMPLE = 3
MIN_REVIEW_SAMPLE = 30
OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "readiness_rank",
    "pattern_key",
    "source_type",
    "proposal_status",
    "promotion_decision",
    "closed_sample_count",
    "wins",
    "losses",
    "sample_count",
    "data_quality_blocked",
    "readiness_state",
    "readiness_reason",
    "next_action",
    "auto_apply",
    "production_change",
    "guardrail_status",
]


@dataclass(frozen=True)
class PatternPromotionReadinessPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        return int(float(norm(value) or 0))
    except ValueError:
        return 0


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except Exception:
        return []


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def first_rows(processed_dir: Path, target_date: str, filename: str) -> list[dict[str, str]]:
    today = processed_dir / "today" / target_date / filename
    governance = processed_dir / "governance" / filename
    rows = read_csv_rows(today)
    return rows if rows else read_csv_rows(governance)


def data_quality_blocked(data_quality_rows: list[dict[str, str]]) -> bool:
    return any(upper(row.get("blocks_model_change")) == "YES" for row in data_quality_rows)


def key_from_proposal(row: dict[str, str]) -> str:
    return norm(row.get("source_pattern_key")) or norm(row.get("proposal_id"))


def key_from_gate(row: dict[str, str]) -> str:
    return norm(row.get("source_pattern_key")) or norm(row.get("experiment_id"))


def build_index(rows: list[dict[str, str]], key_fn) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = key_fn(row)
        if key and key not in out:
            out[key] = row
    return out


def classify(
    key: str,
    proposal: dict[str, str] | None,
    gate: dict[str, str] | None,
    blocked: bool,
) -> tuple[str, str, str]:
    proposal_status = upper((proposal or {}).get("proposal_status"))
    proposal_type = upper((proposal or {}).get("proposal_type"))
    sample_count = as_int((proposal or {}).get("sample_count"))
    promotion_decision = upper((gate or {}).get("promotion_decision"))
    closed = as_int((gate or {}).get("closed_sample_count"))
    wins = as_int((gate or {}).get("wins"))
    losses = as_int((gate or {}).get("losses"))

    if blocked:
        return (
            "BLOCKED_BY_DATA_QUALITY",
            "P1/P2 data-quality issues block model promotion and threshold/calibration changes.",
            "RESOLVE_DATA_QUALITY_FIRST",
        )
    if promotion_decision == "PROMOTION_CANDIDATE_REVIEW_ONLY" and closed >= MIN_REVIEW_SAMPLE and wins >= losses:
        return (
            "PROMOTION_REVIEW_CANDIDATE",
            "Closed sample threshold is met and promotion gate marks review-only promotion candidate.",
            "OPEN_SEPARATE_PROMOTION_PR_REVIEW_ONLY",
        )
    if gate and closed < MIN_REVIEW_SAMPLE:
        return (
            "BLOCKED_BY_SAMPLE_SIZE",
            f"Only {closed} closed samples; minimum review sample is {MIN_REVIEW_SAMPLE}.",
            "CONTINUE_SHADOW_FORWARD_TEST",
        )
    if proposal_status == "SHADOW_CANDIDATE_REQUIRED" and sample_count >= MIN_SHADOW_SAMPLE:
        return (
            "SHADOW_REQUIRED",
            "Pattern is repeated enough to create or continue shadow-only experiment.",
            "CREATE_OR_CONTINUE_SHADOW_ONLY",
        )
    if proposal_type == "MODEL_SHADOW_PROPOSAL":
        return (
            "MONITOR_MORE_EVIDENCE",
            "Model-shadow proposal exists but evidence is not promotion-ready.",
            "COLLECT_MORE_SAMPLES",
        )
    if proposal_type == "DATA_QUALITY_PROPOSAL":
        return (
            "DATA_QUALITY_REVIEW",
            "Pattern is data-quality related and should not become predictive change.",
            "CLEAN_EVIDENCE",
        )
    if proposal:
        return (
            "MONITOR_ONLY",
            "Proposal does not clear shadow or promotion gates.",
            "KEEP_MONITORING",
        )
    return (
        "NO_ACTION",
        "No matching proposal or gate signal found.",
        "NO_ACTION",
    )


def build_rows(target_date: str, generated_at: str, processed_dir: Path) -> list[dict[str, object]]:
    proposals = first_rows(processed_dir, target_date, "vsigma_improvement_proposals.csv")
    gate_rows = first_rows(processed_dir, target_date, "vsigma_promotion_gate.csv")
    dq_rows = first_rows(processed_dir, target_date, "vsigma_data_quality_governor.csv")
    blocked = data_quality_blocked(dq_rows)

    proposal_by_key = build_index(proposals, key_from_proposal)
    gate_by_key = build_index(gate_rows, key_from_gate)
    keys = sorted(set(proposal_by_key) | set(gate_by_key))

    rows: list[dict[str, object]] = []
    for key in keys:
        proposal = proposal_by_key.get(key)
        gate = gate_by_key.get(key)
        state, reason, next_action = classify(key, proposal, gate, blocked)
        rows.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "readiness_rank": 0,
            "pattern_key": key,
            "source_type": upper((proposal or {}).get("proposal_type")) or "PROMOTION_GATE_ONLY",
            "proposal_status": upper((proposal or {}).get("proposal_status")),
            "promotion_decision": upper((gate or {}).get("promotion_decision")),
            "closed_sample_count": as_int((gate or {}).get("closed_sample_count")),
            "wins": as_int((gate or {}).get("wins")),
            "losses": as_int((gate or {}).get("losses")),
            "sample_count": as_int((proposal or {}).get("sample_count")),
            "data_quality_blocked": "YES" if blocked else "NO",
            "readiness_state": state,
            "readiness_reason": reason,
            "next_action": next_action,
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "PROMOTION_READINESS_REVIEW_ONLY_NO_AUTO_CHANGE",
        })

    state_rank = {
        "PROMOTION_REVIEW_CANDIDATE": 0,
        "BLOCKED_BY_DATA_QUALITY": 1,
        "SHADOW_REQUIRED": 2,
        "BLOCKED_BY_SAMPLE_SIZE": 3,
        "DATA_QUALITY_REVIEW": 4,
        "MONITOR_MORE_EVIDENCE": 5,
        "MONITOR_ONLY": 6,
        "NO_ACTION": 7,
    }
    rows.sort(key=lambda row: (state_rank.get(str(row["readiness_state"]), 99), -as_int(row["sample_count"]), str(row["pattern_key"])))
    for idx, row in enumerate(rows, start=1):
        row["readiness_rank"] = idx
    return rows


def executive_status(rows: list[dict[str, object]]) -> str:
    states = {str(row.get("readiness_state")) for row in rows}
    if "PROMOTION_REVIEW_CANDIDATE" in states:
        return "PROMOTION_REVIEW_AVAILABLE"
    if "BLOCKED_BY_DATA_QUALITY" in states:
        return "DATA_QUALITY_BLOCKS_PROMOTION"
    if "SHADOW_REQUIRED" in states:
        return "SHADOW_EXPERIMENT_REQUIRED"
    if rows:
        return "MONITORING_ONLY"
    return "NO_PATTERN_SIGNALS"


def counter(rows: list[dict[str, object]], column: str) -> Counter[str]:
    return Counter(str(row.get(column) or "UNKNOWN") for row in rows)


def fmt_counter(values: Counter[str]) -> str:
    return "; ".join(f"{k}={v}" for k, v in values.most_common()) if values else "none"


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Pattern Promotion Readiness - {target_date}",
        "",
        "## Executive Readiness Summary",
        f"- generated_at: {generated_at}",
        f"- executive_status: {executive_status(rows)}",
        f"- patterns_reviewed: {len(rows)}",
        f"- readiness_counts: {fmt_counter(counter(rows, 'readiness_state'))}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Pattern Readiness Decisions",
    ]
    if not rows:
        lines.append("- none")
    else:
        for row in rows[:40]:
            lines.append(
                f"- #{row['readiness_rank']} | {row['readiness_state']} | key={row['pattern_key']} | "
                f"sample={row['sample_count']} | closed={row['closed_sample_count']} | next={row['next_action']} | reason={row['readiness_reason']}"
            )
    lines.extend([
        "",
        "## Guardrails",
        "- No model changes are applied.",
        "- No threshold/calibration/ranking/market-selection changes are applied.",
        "- PROMOTION_REVIEW_CANDIDATE only means a separate PR/review path can be opened.",
        "- BLOCKED_BY_DATA_QUALITY overrides predictive promotion.",
    ])
    return "\n".join(lines)


def build_pattern_promotion_readiness(target_date: str, timezone_name: str = "Atlantic/Canary", processed_dir: Path = DEFAULT_PROCESSED_DIR, now: datetime | None = None) -> tuple[list[dict[str, object]], PatternPromotionReadinessPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    rows = build_rows(target_date, generated_at, processed_dir)
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)
    paths = PatternPromotionReadinessPaths(
        today_csv=today / "vsigma_pattern_promotion_readiness.csv",
        today_md=today / "vsigma_pattern_promotion_readiness.md",
        governance_csv=governance / "vsigma_pattern_promotion_readiness.csv",
        governance_md=governance / "vsigma_pattern_promotion_readiness.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA pattern promotion readiness report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_pattern_promotion_readiness(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA PATTERN PROMOTION READINESS ===")
    print(f"patterns_reviewed={len(rows)}")
    print(f"executive_status={executive_status(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
