from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from build_learning_ledger import (
        OUTPUT_COLUMNS,
        build_learning_rows,
        format_counter,
        read_csv_rows,
        rows_for_date,
        upper,
        write_csv,
    )
except ModuleNotFoundError:
    from scripts.build_learning_ledger import (
        OUTPUT_COLUMNS,
        build_learning_rows,
        format_counter,
        read_csv_rows,
        rows_for_date,
        upper,
        write_csv,
    )


DEFAULT_PROCESSED_DIR = Path("data/processed")
BACKFILL_COLUMNS = [*OUTPUT_COLUMNS, "source_dates_seen", "backfill_scope"]


@dataclass(frozen=True)
class LearningBackfillPaths:
    all_csv: Path
    all_md: Path
    report_md: Path


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def collect_dates(rows: list[dict[str, str]]) -> list[str]:
    dates: set[str] = set()
    for row in rows:
        for column in ("target_date", "date", "fixture_date", "match_date"):
            value = norm(row.get(column))[:10]
            if value:
                try:
                    dates.add(date.fromisoformat(value).isoformat())
                except ValueError:
                    continue
    return sorted(dates)


def load_historical_inputs(processed_dir: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    decision_paths = [
        processed_dir / "ledger" / "vsigma_decision_outcome_ledger.csv",
        processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv",
    ]
    quality_paths = [processed_dir / "governance" / "vsigma_decision_quality_review.csv"]

    today_root = processed_dir / "today"
    if today_root.exists():
        for day_dir in sorted(path for path in today_root.iterdir() if path.is_dir()):
            decision_paths.append(day_dir / "vsigma_decision_outcome_ledger.csv")
            quality_paths.append(day_dir / "vsigma_decision_quality_review.csv")

    decision_rows: list[dict[str, str]] = []
    quality_rows: list[dict[str, str]] = []
    for path in decision_paths:
        decision_rows.extend(read_csv_rows(path))
    for path in quality_paths:
        quality_rows.extend(read_csv_rows(path))
    return decision_rows, quality_rows


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str, str, str]] = set()
    deduped: list[dict[str, str]] = []
    for row in rows:
        key = (
            norm(row.get("target_date")),
            norm(row.get("fixture_id")),
            upper(row.get("market_primary")),
            upper(row.get("official_action")),
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def write_backfill_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=BACKFILL_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in BACKFILL_COLUMNS})


def build_markdown(generated_at: str, rows: list[dict[str, str]], source_dates: list[str]) -> str:
    family_counts = Counter(upper(row.get("learning_family")) or "UNKNOWN" for row in rows)
    status_counts = Counter(upper(row.get("learning_status")) or "UNKNOWN" for row in rows)
    market_counts = Counter(upper(row.get("market_primary")) or "UNKNOWN" for row in rows)
    sample_counts = Counter(norm(row.get("sample_key")) or "UNKNOWN" for row in rows)
    actionable_wins = sum(1 for row in rows if upper(row.get("learning_family")) == "ACTIONABLE_RESULT" and upper(row.get("result_status")) == "WIN")
    actionable_losses = sum(1 for row in rows if upper(row.get("learning_family")) == "ACTIONABLE_RESULT" and upper(row.get("result_status")) == "LOSS")

    top_samples = "; ".join(f"{key}={value}" for key, value in sample_counts.most_common(10)) if sample_counts else "none"
    lines = [
        "# vSIGMA Learning Backfill Report",
        "",
        "## Executive Backfill Summary",
        f"- generated_at: {generated_at}",
        f"- source_dates_seen: {len(source_dates)}",
        f"- date_range: {source_dates[0] if source_dates else 'N/A'} to {source_dates[-1] if source_dates else 'N/A'}",
        f"- rows reviewed: {len(rows)}",
        f"- actionable wins: {actionable_wins}",
        f"- actionable losses: {actionable_losses}",
        f"- learning_family_counts: {format_counter(family_counts)}",
        f"- learning_status_counts: {format_counter(status_counts)}",
        f"- market_counts: {format_counter(market_counts)}",
        f"- top_sample_keys: {top_samples}",
        "",
        "## Learning Use",
        "- This file backfills historical evidence for future pattern mining.",
        "- It does not alter model formulas, thresholds, calibration, ranking, or market selection.",
        "- Repeated sample keys should feed vsigma-learning-pattern-miner-v08.",
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


def build_learning_backfill(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    timezone_name: str = "Atlantic/Canary",
    now: datetime | None = None,
) -> tuple[list[dict[str, str]], LearningBackfillPaths]:
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")

    decision_rows_all, quality_rows_all = load_historical_inputs(processed_dir)
    source_dates = sorted(set(collect_dates(decision_rows_all)) | set(collect_dates(quality_rows_all)))

    all_learning_rows: list[dict[str, str]] = []
    for target_date in source_dates:
        decision_rows = rows_for_date(decision_rows_all, target_date)
        quality_rows = rows_for_date(quality_rows_all, target_date)
        all_learning_rows.extend(build_learning_rows(target_date, decision_rows, quality_rows, generated_at))

    all_learning_rows = dedupe_rows(all_learning_rows)
    source_dates_text = ";".join(source_dates)
    for row in all_learning_rows:
        row["source_dates_seen"] = source_dates_text
        row["backfill_scope"] = "HISTORICAL_ALL_AVAILABLE"

    governance = processed_dir / "governance"
    governance.mkdir(parents=True, exist_ok=True)
    paths = LearningBackfillPaths(
        all_csv=governance / "vsigma_learning_ledger_all.csv",
        all_md=governance / "vsigma_learning_ledger_all.md",
        report_md=governance / "vsigma_learning_backfill_report.md",
    )
    markdown = build_markdown(generated_at, all_learning_rows, source_dates)
    write_backfill_csv(paths.all_csv, all_learning_rows)
    paths.all_md.write_text(markdown, encoding="utf-8")
    paths.report_md.write_text(markdown, encoding="utf-8")
    return all_learning_rows, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill historical vSIGMA learning ledger evidence.")
    parser.add_argument("--processed-dir", type=Path, default=DEFAULT_PROCESSED_DIR)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows, paths = build_learning_backfill(args.processed_dir, args.timezone)
    print("=== VSIGMA LEARNING BACKFILL ===")
    print(f"rows={len(rows)}")
    print(f"all_csv={paths.all_csv}")
    print(f"all_md={paths.all_md}")
    print(f"report_md={paths.report_md}")


if __name__ == "__main__":
    main()
