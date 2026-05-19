from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, read_csv_lenient, split_fresh_stale_rows
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, read_csv_lenient, split_fresh_stale_rows


DECISION_LEDGER_CSV = "vsigma_decision_outcome_ledger.csv"
DECISION_LEDGER_JSONL = "vsigma_decision_outcome_ledger.jsonl"


@dataclass(frozen=True)
class MaterializedFile:
    name: str
    source: Path
    destination: Path
    status: str
    rows: int | None = None


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def normalize_target_date(value: str) -> str:
    return pd.Timestamp(value).date().isoformat()


def target_date_rows(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    fresh, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    if not fresh.empty:
        return fresh.reset_index(drop=True)
    if "target_date" in df.columns:
        return df[df["target_date"].astype(str).str[:10].eq(target_date)].copy().reset_index(drop=True)
    return pd.DataFrame(columns=df.columns)


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return False


def copy_if_exists(name: str, sources: Iterable[Path], destination: Path) -> MaterializedFile:
    for source in sources:
        if not source.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not same_path(source, destination):
            shutil.copy2(source, destination)
        return MaterializedFile(name=name, source=source, destination=destination, status="MATERIALIZED")
    return MaterializedFile(name=name, source=Path(""), destination=destination, status="MISSING")


def materialize_decision_ledger_csv(processed_dir: Path, target_date: str) -> MaterializedFile:
    source = processed_dir / "ledger" / DECISION_LEDGER_CSV
    destination = snapshot_dir(processed_dir, target_date) / DECISION_LEDGER_CSV
    if not source.exists():
        return copy_if_exists(DECISION_LEDGER_CSV, [destination], destination)
    ledger = read_csv_lenient(source)
    daily = target_date_rows(ledger, target_date)
    destination.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(destination, index=False)
    return MaterializedFile(
        name=DECISION_LEDGER_CSV,
        source=source,
        destination=destination,
        status="MATERIALIZED",
        rows=len(daily),
    )


def jsonl_target_date(line: str, target_date: str) -> bool:
    try:
        payload = json.loads(line)
    except json.JSONDecodeError:
        return f'"target_date": "{target_date}"' in line or f'"target_date":"{target_date}"' in line
    return str(payload.get("target_date", ""))[:10] == target_date


def materialize_decision_ledger_jsonl(processed_dir: Path, target_date: str) -> MaterializedFile:
    source = processed_dir / "ledger" / DECISION_LEDGER_JSONL
    destination = snapshot_dir(processed_dir, target_date) / DECISION_LEDGER_JSONL
    if not source.exists():
        return copy_if_exists(DECISION_LEDGER_JSONL, [destination], destination)
    rows = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8", errors="ignore") as src, destination.open("w", encoding="utf-8", newline="\n") as dst:
        for line in src:
            if jsonl_target_date(line, target_date):
                dst.write(line if line.endswith("\n") else f"{line}\n")
                rows += 1
    return MaterializedFile(
        name=DECISION_LEDGER_JSONL,
        source=source,
        destination=destination,
        status="MATERIALIZED",
        rows=rows,
    )


def optional_file_specs(processed_dir: Path, snap: Path) -> list[tuple[str, list[Path]]]:
    ledger_dir = processed_dir / "ledger"
    governance_dir = processed_dir / "governance"
    health_dir = processed_dir / "health"
    return [
        ("vsigma_ledger_daily_report.md", [snap / "vsigma_ledger_daily_report.md", ledger_dir / "vsigma_ledger_daily_report.md"]),
        ("vsigma_system_review.md", [snap / "vsigma_system_review.md", governance_dir / "vsigma_system_review.md"]),
        ("vsigma_system_review.csv", [snap / "vsigma_system_review.csv", governance_dir / "vsigma_system_review.csv"]),
        ("vsigma_prelock_decision_resolver.md", [snap / "vsigma_prelock_decision_resolver.md", governance_dir / "vsigma_prelock_decision_resolver_latest.md"]),
        ("vsigma_prelock_decision_resolver.csv", [snap / "vsigma_prelock_decision_resolver.csv"]),
        ("vsigma_cloud_decision_summary.md", [snap / "vsigma_cloud_decision_summary.md"]),
        ("vsigma_cloud_decision_summary.csv", [snap / "vsigma_cloud_decision_summary.csv"]),
        ("vsigma_decision_quality_review.md", [snap / "vsigma_decision_quality_review.md", governance_dir / "vsigma_decision_quality_review.md"]),
        ("vsigma_decision_quality_review.csv", [snap / "vsigma_decision_quality_review.csv", governance_dir / "vsigma_decision_quality_review.csv"]),
        ("vsigma_governance_dashboard.md", [snap / "vsigma_governance_dashboard.md", governance_dir / "vsigma_governance_dashboard.md"]),
        ("vsigma_healthcheck_report.md", [snap / "vsigma_healthcheck_report.md", health_dir / "vsigma_healthcheck_report.md"]),
        ("vsigma_healthcheck_summary.csv", [snap / "vsigma_healthcheck_summary.csv", health_dir / "vsigma_healthcheck_summary.csv"]),
    ]


def materialize_daily_audit_bundle(
    target_date: str,
    processed_dir: Path = PROCESSED_DIR,
) -> list[MaterializedFile]:
    target_date = normalize_target_date(target_date)
    snap = snapshot_dir(processed_dir, target_date)
    snap.mkdir(parents=True, exist_ok=True)

    materialized = [
        materialize_decision_ledger_csv(processed_dir, target_date),
        materialize_decision_ledger_jsonl(processed_dir, target_date),
    ]
    for name, sources in optional_file_specs(processed_dir, snap):
        materialized.append(copy_if_exists(name, sources, snap / name))
    return materialized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the daily vSIGMA audit bundle under data/processed/today/YYYY-MM-DD.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    files = materialize_daily_audit_bundle(args.date, args.processed_dir)
    print("=== VSIGMA DAILY AUDIT BUNDLE ===")
    for item in files:
        rows = "" if item.rows is None else f" rows={item.rows}"
        print(f"{item.status}: {item.name} -> {item.destination}{rows}")


if __name__ == "__main__":
    main()
