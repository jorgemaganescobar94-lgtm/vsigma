from __future__ import annotations

import argparse
from datetime import date

from build_probable_lineup_source_registry import run as run_source_registry
from build_autonomous_probable_lineup_collector import run as run_autonomous_collector
from import_probable_lineup_sources import run as run_probable_source_import
from build_probable_lineup_consensus_v2 import run as run_probable_consensus_v2
from build_probable_lineup_accuracy_ledger import run as run_probable_accuracy_ledger


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    run_source_registry(day, tz)
    run_autonomous_collector(day, tz)
    run_probable_source_import(day, tz)
    run_probable_consensus_v2(day, tz)
    run_probable_accuracy_ledger(day, tz)
    print("=== VSIGMA PROBABLE LINEUP CONSENSUS WRAPPER ===")
    print("source_registry=BUILT")
    print("autonomous_collector=BUILT")
    print("source_import=BUILT")
    print("consensus_engine=V2_WEIGHTED_REGISTRY")
    print("accuracy_ledger=BUILT")
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
