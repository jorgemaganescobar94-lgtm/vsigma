from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

PROCESSED = Path("data/processed")

def read_guard(day: str, processed: Path) -> dict[str, str]:
    path = processed / "today" / day / "vsigma_api_subscription_guard.csv"
    if not path.exists():
        path = processed / "governance" / "vsigma_api_subscription_guard.csv"

    if not path.exists():
        return {
            "api_calls_allowed": "NO",
            "executor_mode": "SKIP_API_EXECUTION",
            "recommended_executor_limit": "0",
            "guard_reason": "subscription guard output missing",
        }

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if not rows:
        return {
            "api_calls_allowed": "NO",
            "executor_mode": "SKIP_API_EXECUTION",
            "recommended_executor_limit": "0",
            "guard_reason": "subscription guard output empty",
        }

    # Prefer same-day row if governance contains multiple rows later.
    for row in rows:
        if str(row.get("target_date", "")).strip() == day:
            return row

    return rows[0]

def run(day: str, tz: str, processed: Path) -> int:
    guard = read_guard(day, processed)

    allowed = str(guard.get("api_calls_allowed", "NO")).strip()
    mode = str(guard.get("executor_mode", "SKIP_API_EXECUTION")).strip()
    limit = str(guard.get("recommended_executor_limit", "0")).strip() or "0"

    print(f"API guard: allowed={allowed} mode={mode} limit={limit}")

    cmd = [
        sys.executable,
        "scripts/run_max_coverage_api_enrichment_executor.py",
        "--date",
        day,
        "--timezone",
        tz,
    ]

    if allowed != "YES":
        print("API execution skipped by subscription guard.")
        cmd += ["--limit", "0"]
    elif limit == "0":
        cmd += ["--execute"]
    else:
        cmd += ["--execute", "--limit", limit]

    print("Executor command:", " ".join(cmd))
    completed = subprocess.run(cmd, check=False)
    return int(completed.returncode)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    raise SystemExit(run(args.date, args.timezone, args.processed_dir))

if __name__ == "__main__":
    main()
