from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DEFAULT_PROCESSED_DIR = Path("data/processed")
OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "official_action",
    "executable_now",
    "final_block_reason",
    "execution_family_status",
    "is_actionable",
    "is_non_actionable",
    "is_expired",
    "result_status",
    "decision_quality_label",
    "quality_bucket",
    "improvement_signal",
    "recommended_followup",
    "accuracy_primary_risk",
    "competition_calibrated_prob",
    "learning_family",
    "learning_status",
    "sample_key",
    "learning_priority",
    "learning_note",
]


@dataclass(frozen=True)
class LearningLedgerPaths:
    today_csv: Path
    today_md: Path
    governance_csv: Path
    governance_md: Path


def norm(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]
    except Exception:
        return []


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in OUTPUT_COLUMNS})


def rows_for_date(rows: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    filtered: list[dict[str, str]] = []
    for row in rows:
        for column in ("target_date", "date", "fixture_date", "match_date"):
            value = norm(row.get(column))[:10]
            if value == target_date:
                filtered.append(row)
                break
    return filtered


def row_key(row: dict[str, str]) -> tuple[str, str]:
    return (norm(row.get("fixture_id")), upper(row.get("market_primary")))


def pick_first(*values: object) -> str:
    for value in values:
        text = norm(value)
        if text:
            return text
    return ""


def index_by_key(rows: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    result: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        key = row_key(row)
        if key[0] and key[1] and key not in result:
            result[key] = row
    return result


def classify_learning_family(row: dict[str, str]) -> str:
    action = upper(row.get("official_action"))
    family_status = upper(row.get("execution_family_status"))
    block_reason = upper(row.get("final_block_reason"))
    quality = upper(row.get("decision_quality_label"))
    executable = upper(row.get("executable_now"))

    if action == "EXECUTABLE" or upper(row.get("is_actionable")) == "YES" or executable == "YES":
        return "ACTIONABLE_RESULT"
    if quality.startswith("EXPIRED_PRELOCK") or family_status == "EXPIRED" or block_reason == "KICKOFF_ALREADY_PASSED" or upper(row.get("is_expired")) == "YES":
        return "EXPIRED_PRELOCK"
    if "WAIT" in family_status or block_reason in {"OUTSIDE_PRELOCK_WINDOW", "OUTSIDE_90_MIN_PRELOCK_WINDOW"}:
        return "WAITING_PRELOCK"
    if any(token in block_reason for token in ("DATA", "ODDS", "LINEUP", "AVAILABILITY", "MISSING")) or "DATA" in family_status:
        return "DATA_BLOCKED"
    if action == "TECHNICAL_REVIEW" or "TECHNICAL" in quality or "TECHNICAL" in family_status:
        return "TECHNICAL_REVIEW"
    if action == "NO_BET" or upper(row.get("is_non_actionable")) == "YES":
        return "NO_BET_BLOCK"
    return "UNRESOLVED"


def classify_learning_status(row: dict[str, str], family: str) -> tuple[str, str, str]:
    quality = upper(row.get("decision_quality_label"))
    signal = upper(row.get("improvement_signal"))
    result_status = upper(row.get("result_status")) or "UNRESOLVED"

    if family == "EXPIRED_PRELOCK":
        return "TIMING_REVIEW", "P1", "Execution timing/prelock state must be reviewed; not a predictive model change."
    if family == "DATA_BLOCKED":
        return "DATA_REVIEW", "P1", "Provider/odds/lineup/data coverage blocked execution; improve data path before changing model."
    if family == "TECHNICAL_REVIEW":
        return "TECHNICAL_REVIEW", "P1", "Technical state requires workflow or reporting inspection."
    if quality in {"ACTIONABLE_LOSS", "NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"}:
        return "REVIEW_PATTERN", "P2", "Potential learning signal; collect repeated samples before proposing any change."
    if signal in {"REVIEW_AUTO_TIMING", "REVIEW_PRELOCK_STRICTNESS", "REVIEW_NON_ACTIONABLE_BLOCK"}:
        return "REVIEW_PATTERN", "P2", "Operational pattern candidate; keep collecting evidence."
    if family == "ACTIONABLE_RESULT" and result_status in {"WIN", "LOSS", "VOID"}:
        return "COLLECT_MORE_SAMPLE", "P3", "Resolved actionable result logged for sample accumulation."
    if family == "NO_BET_BLOCK" and result_status in {"WIN", "LOSS", "VOID"}:
        return "COLLECT_MORE_SAMPLE", "P3", "Resolved block result logged for no-bet quality sample."
    if result_status == "UNRESOLVED":
        return "COLLECT_MORE_SAMPLE", "P3", "Outcome unresolved; wait for post-results labeling."
    return "PROMOTION_NOT_ALLOWED", "P3", "Evidence only; promotion requires separate shadow experiment and promotion gate."


def sample_key(row: dict[str, str], family: str) -> str:
    market = upper(row.get("market_primary")) or "UNKNOWN_MARKET"
    risk = upper(row.get("accuracy_primary_risk")) or "UNKNOWN_RISK"
    signal = upper(row.get("improvement_signal")) or "NO_SIGNAL"
    return "::".join([family, market, risk, signal])


def build_learning_rows(target_date: str, decision_rows: list[dict[str, str]], quality_rows: list[dict[str, str]], generated_at: str) -> list[dict[str, str]]:
    quality_by_key = index_by_key(quality_rows)
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    for decision in decision_rows:
        key = row_key(decision)
        quality = quality_by_key.get(key, {})
        combined = {**decision, **quality}
        family = classify_learning_family(combined)
        status, priority, note = classify_learning_status(combined, family)
        rows.append(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": norm(pick_first(combined.get("fixture_id"), decision.get("fixture_id"))),
                "league": norm(pick_first(combined.get("league"), decision.get("league"))),
                "home_team": norm(pick_first(combined.get("home_team"), decision.get("home_team"))),
                "away_team": norm(pick_first(combined.get("away_team"), decision.get("away_team"))),
                "market_primary": upper(pick_first(combined.get("market_primary"), decision.get("market_primary"))),
                "official_action": upper(combined.get("official_action")),
                "executable_now": upper(combined.get("executable_now")),
                "final_block_reason": upper(combined.get("final_block_reason")),
                "execution_family_status": upper(combined.get("execution_family_status")),
                "is_actionable": upper(combined.get("is_actionable")),
                "is_non_actionable": upper(combined.get("is_non_actionable")),
                "is_expired": upper(combined.get("is_expired")),
                "result_status": upper(combined.get("result_status")) or "UNRESOLVED",
                "decision_quality_label": upper(combined.get("decision_quality_label")),
                "quality_bucket": upper(combined.get("quality_bucket")),
                "improvement_signal": upper(combined.get("improvement_signal")),
                "recommended_followup": norm(combined.get("recommended_followup")),
                "accuracy_primary_risk": norm(combined.get("accuracy_primary_risk")),
                "competition_calibrated_prob": norm(combined.get("competition_calibrated_prob")),
                "learning_family": family,
                "learning_status": status,
                "sample_key": sample_key(combined, family),
                "learning_priority": priority,
                "learning_note": note,
            }
        )
        if key[0] and key[1]:
            seen.add(key)

    for quality in quality_rows:
        key = row_key(quality)
        if key in seen:
            continue
        family = classify_learning_family(quality)
        status, priority, note = classify_learning_status(quality, family)
        row = {column: "" for column in OUTPUT_COLUMNS}
        row.update(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": norm(quality.get("fixture_id")),
                "league": norm(quality.get("league")),
                "home_team": norm(quality.get("home_team")),
                "away_team": norm(quality.get("away_team")),
                "market_primary": upper(quality.get("market_primary")),
                "official_action": upper(quality.get("official_action")),
                "final_block_reason": upper(quality.get("final_block_reason")),
                "execution_family_status": upper(quality.get("execution_family_status")),
                "is_actionable": upper(quality.get("is_actionable")),
                "is_non_actionable": upper(quality.get("is_non_actionable")),
                "is_expired": upper(quality.get("is_expired")),
                "result_status": upper(quality.get("result_status")) or "UNRESOLVED",
                "decision_quality_label": upper(quality.get("decision_quality_label")),
                "quality_bucket": upper(quality.get("quality_bucket")),
                "improvement_signal": upper(quality.get("improvement_signal")),
                "recommended_followup": norm(quality.get("recommended_followup")),
                "accuracy_primary_risk": norm(quality.get("accuracy_primary_risk")),
                "competition_calibrated_prob": norm(quality.get("competition_calibrated_prob")),
                "learning_family": family,
                "learning_status": status,
                "sample_key": sample_key(quality, family),
                "learning_priority": priority,
                "learning_note": note,
            }
        )
        rows.append(row)
    return rows


def count(rows: list[dict[str, str]], column: str, value: str) -> int:
    return sum(1 for row in rows if upper(row.get(column)) == value)


def counter(rows: list[dict[str, str]], column: str) -> Counter[str]:
    return Counter(upper(row.get(column)) or "UNKNOWN" for row in rows)


def format_counter(values: Counter[str]) -> str:
    if not values:
        return "none"
    return "; ".join(f"{key}={count}" for key, count in values.most_common())


def build_markdown(target_date: str, generated_at: str, rows: list[dict[str, str]]) -> str:
    actionable_wins = sum(1 for row in rows if upper(row.get("learning_family")) == "ACTIONABLE_RESULT" and upper(row.get("result_status")) == "WIN")
    actionable_losses = sum(1 for row in rows if upper(row.get("learning_family")) == "ACTIONABLE_RESULT" and upper(row.get("result_status")) == "LOSS")
    lines = [
        f"# vSIGMA Learning Ledger - {target_date}",
        "",
        "## Executive Learning Summary",
        f"- generated_at: {generated_at}",
        f"- rows reviewed: {len(rows)}",
        f"- actionable wins: {actionable_wins}",
        f"- actionable losses: {actionable_losses}",
        f"- no-bet missed wins: {count(rows, 'decision_quality_label', 'NO_BET_MISSED_WIN')}",
        f"- no-bet avoided losses: {count(rows, 'decision_quality_label', 'NO_BET_CORRECT_AVOIDED_LOSS')}",
        f"- expired prelock rows: {count(rows, 'learning_family', 'EXPIRED_PRELOCK')}",
        f"- data blocked rows: {count(rows, 'learning_family', 'DATA_BLOCKED')}",
        f"- top improvement signals: {format_counter(counter(rows, 'improvement_signal'))}",
        "",
        "## Market Family Summary",
        f"- learning_family_counts: {format_counter(counter(rows, 'learning_family'))}",
        f"- learning_status_counts: {format_counter(counter(rows, 'learning_status'))}",
        f"- market_counts: {format_counter(counter(rows, 'market_primary'))}",
        "",
        "## Learning Recommendations",
        "- Treat this ledger as evidence collection only.",
        "- Promote no change from a single row or short sample.",
        "- Repeated sample keys should feed a future pattern miner and shadow experiment engine.",
        "",
        "## Guardrails",
        "- predictive changes applied: NO",
        "- threshold changes applied: NO",
        "- calibration changes applied: NO",
        "- ranking changes applied: NO",
        "- market-selection changes applied: NO",
        "",
    ]
    return "\n".join(lines)


def load_inputs(processed_dir: Path, target_date: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    today = processed_dir / "today" / target_date
    decision_sources = [
        today / "vsigma_decision_outcome_ledger.csv",
        processed_dir / "ledger" / "vsigma_decision_outcome_ledger.csv",
        processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv",
    ]
    quality_sources = [
        today / "vsigma_decision_quality_review.csv",
        processed_dir / "governance" / "vsigma_decision_quality_review.csv",
    ]
    decision_rows: list[dict[str, str]] = []
    quality_rows: list[dict[str, str]] = []
    for path in decision_sources:
        decision_rows.extend(rows_for_date(read_csv_rows(path), target_date))
    for path in quality_sources:
        quality_rows.extend(rows_for_date(read_csv_rows(path), target_date))
    return decision_rows, quality_rows


def build_learning_ledger(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[list[dict[str, str]], LearningLedgerPaths]:
    target_date = date.fromisoformat(target_date).isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    today = processed_dir / "today" / target_date
    governance = processed_dir / "governance"
    today.mkdir(parents=True, exist_ok=True)
    governance.mkdir(parents=True, exist_ok=True)

    decision_rows, quality_rows = load_inputs(processed_dir, target_date)
    rows = build_learning_rows(target_date, decision_rows, quality_rows, generated_at)
    paths = LearningLedgerPaths(
        today_csv=today / "vsigma_learning_ledger.csv",
        today_md=today / "vsigma_learning_ledger.md",
        governance_csv=governance / "vsigma_learning_ledger.csv",
        governance_md=governance / "vsigma_learning_ledger.md",
    )
    markdown = build_markdown(target_date, generated_at, rows)
    for csv_path in (paths.today_csv, paths.governance_csv):
        write_csv(csv_path, rows)
    for md_path in (paths.today_md, paths.governance_md):
        md_path.write_text(markdown, encoding="utf-8")
    return rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA learning ledger.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_learning_ledger(args.date, args.timezone, args.processed_dir)
    print("=== VSIGMA LEARNING LEDGER ===")
    print(f"rows={len(rows)}")
    print(f"today_csv={paths.today_csv}")
    print(f"today_md={paths.today_md}")
    print(f"governance_csv={paths.governance_csv}")
    print(f"governance_md={paths.governance_md}")


if __name__ == "__main__":
    main()
