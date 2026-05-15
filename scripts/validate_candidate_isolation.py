from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from daily_hardening import (
        BASELINE_FILES,
        CANDIDATE_REQUIRED_FILES,
        PROCESSED_DIR,
        TODAY_DIR,
        copy_paths_to_snapshot,
        format_markdown_table,
    )
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        BASELINE_FILES,
        CANDIDATE_REQUIRED_FILES,
        PROCESSED_DIR,
        TODAY_DIR,
        copy_paths_to_snapshot,
        format_markdown_table,
    )


ISOLATION_CSV = "vsigma_candidate_isolation_report.csv"
ISOLATION_TXT = "vsigma_candidate_isolation_report.txt"


def validate_isolation(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    snapshot_dir: Path | None = None,
) -> pd.DataFrame:
    target_date = target_date or date.today().isoformat()
    snapshot_dir = snapshot_dir or TODAY_DIR / target_date
    rows: list[dict[str, object]] = []

    for filename in sorted(BASELINE_FILES):
        path = processed_dir / filename
        rows.append(
            {
                "target_date": target_date,
                "check_name": "official_baseline_exists",
                "file_name": filename,
                "status": "PASS" if path.exists() else "ERROR_MISSING_REQUIRED_FILE",
                "detail": "baseline file present" if path.exists() else "official baseline file missing",
            }
        )

    for filename in CANDIDATE_REQUIRED_FILES:
        path = processed_dir / filename
        has_candidate_name = filename.startswith("vsigma_today_candidate_")
        rows.append(
            {
                "target_date": target_date,
                "check_name": "candidate_specific_name",
                "file_name": filename,
                "status": "PASS" if has_candidate_name else "ERROR_CANDIDATE_OVERWRITE_RISK",
                "detail": "candidate output uses candidate-specific name",
            }
        )
        rows.append(
            {
                "target_date": target_date,
                "check_name": "candidate_file_present_or_optional",
                "file_name": filename,
                "status": "PASS" if path.exists() else "WARNING_OPTIONAL_CANDIDATE_MISSING",
                "detail": "candidate file present" if path.exists() else "optional shadow candidate file missing",
            }
        )

    baseline_paths = {str(processed_dir / filename) for filename in BASELINE_FILES}
    for filename in CANDIDATE_REQUIRED_FILES:
        candidate_path = str(processed_dir / filename)
        rows.append(
            {
                "target_date": target_date,
                "check_name": "candidate_does_not_overwrite_baseline_path",
                "file_name": filename,
                "status": "PASS" if candidate_path not in baseline_paths else "ERROR_CANDIDATE_OVERWRITE_RISK",
                "detail": "candidate path is isolated from official baseline paths",
            }
        )

    expected_snapshot = [
        "vsigma_today_competition_top.csv",
        "vsigma_today_candidate_v2_competition_top.csv",
        "vsigma_today_candidate_v4_competition_top.csv",
        "vsigma_today_candidate_v5_competition_top.csv",
        "vsigma_today_candidate_v6_competition_top.csv",
        "vsigma_today_candidate_v7_competition_top.csv",
    ]
    for filename in expected_snapshot:
        path = snapshot_dir / filename
        rows.append(
            {
                "target_date": target_date,
                "check_name": "snapshot_contains_expected_file",
                "file_name": filename,
                "status": "PASS" if path.exists() else "WARNING_SNAPSHOT_FILE_MISSING",
                "detail": str(path),
            }
        )

    return pd.DataFrame(rows)


def write_isolation_reports(
    report: pd.DataFrame,
    processed_dir: Path = PROCESSED_DIR,
    snapshot_dir: Path | None = None,
) -> dict[str, Path]:
    csv_path = processed_dir / ISOLATION_CSV
    txt_path = processed_dir / ISOLATION_TXT
    processed_dir.mkdir(parents=True, exist_ok=True)
    report.to_csv(csv_path, index=False)
    counts = report["status"].value_counts().to_dict() if not report.empty else {}
    lines = [
        "# vSIGMA Candidate Isolation Report",
        "",
        f"- Target date: {report['target_date'].iloc[0] if not report.empty else ''}",
        f"- PASS: {counts.get('PASS', 0)}",
        f"- Warnings: {sum(count for status, count in counts.items() if str(status).startswith('WARNING'))}",
        f"- Errors: {sum(count for status, count in counts.items() if str(status).startswith('ERROR'))}",
        "",
        format_markdown_table(report, max_rows=200) if not report.empty else "_No checks run._",
        "",
    ]
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    if snapshot_dir is not None:
        copy_paths_to_snapshot([csv_path, txt_path], snapshot_dir)
    return {"csv": csv_path, "txt": txt_path}


def run_validation(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    snapshot_dir: Path | None = None,
) -> dict[str, Path]:
    target_date = target_date or date.today().isoformat()
    snapshot_dir = snapshot_dir or TODAY_DIR / target_date
    report = validate_isolation(processed_dir, target_date, snapshot_dir)
    return write_isolation_reports(report, processed_dir, snapshot_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate shadow candidate isolation from official baseline files.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--snapshot-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    snapshot_dir = args.snapshot_dir or TODAY_DIR / target_date
    paths = run_validation(args.processed_dir, target_date, snapshot_dir)
    print(f"Candidate isolation CSV: {paths['csv']}")
    print(f"Candidate isolation report: {paths['txt']}")


if __name__ == "__main__":
    main()
