from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, copy_paths_to_snapshot, stamp_daily_outputs
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, copy_paths_to_snapshot, stamp_daily_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stamp vSIGMA daily CSV outputs with run metadata.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--snapshot-dir", type=Path, default=None)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--phase", choices=["pre", "post", "all"], default="all")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    paths = stamp_daily_outputs(args.processed_dir, target_date, args.run_id, phase=args.phase)
    snapshot_dir = args.snapshot_dir or TODAY_DIR / target_date
    copy_paths_to_snapshot(paths, snapshot_dir)
    print(f"Stamped metadata on {len(paths)} daily CSV outputs.")


if __name__ == "__main__":
    main()
