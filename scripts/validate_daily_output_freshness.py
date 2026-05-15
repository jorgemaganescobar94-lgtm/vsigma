from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from daily_hardening import (
        CSV_OUTPUT_SPECS,
        PRE_LOCK_NOTE,
        PROCESSED_DIR,
        TODAY_DIR,
        copy_paths_to_snapshot,
        format_markdown_table,
        observed_dates,
        read_csv_lenient,
    )
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        CSV_OUTPUT_SPECS,
        PRE_LOCK_NOTE,
        PROCESSED_DIR,
        TODAY_DIR,
        copy_paths_to_snapshot,
        format_markdown_table,
        observed_dates,
        read_csv_lenient,
    )


FRESHNESS_CSV = "vsigma_daily_freshness_report.csv"
FRESHNESS_TXT = "vsigma_daily_freshness_report.txt"

REQUIRED_PRE_FILES = {
    "vsigma_today_competition_shortlist.csv",
    "vsigma_today_competition_top.csv",
    "vsigma_today_candidate_v2_competition_top.csv",
}


def freshness_status(path: Path, target_date: str, empty_ok: bool) -> tuple[str, str]:
    if not path.exists():
        return "ERROR_MISSING_REQUIRED_FILE", "required output file is missing"
    df = read_csv_lenient(path)
    if df.empty:
        if empty_ok:
            return "EMPTY_OK_NO_BET", "empty output with headers is valid for a no-bet day"
        return "EMPTY_UNEXPECTED", "empty output was not expected for this report"

    if "target_date" in df.columns:
        metadata_dates = sorted({str(value)[:10] for value in df["target_date"].dropna().tolist() if str(value)})
        if metadata_dates and metadata_dates != [target_date]:
            return "WARNING_STALE_GLOBAL_FILE", f"metadata target_date={metadata_dates} does not match {target_date}"

    source_checks = (
        set(df["source_file_date_check"].dropna().astype(str).str.upper().tolist())
        if "source_file_date_check" in df.columns
        else set()
    )
    if "DATE_MISMATCH" in source_checks:
        return "WARNING_STALE_GLOBAL_FILE", "metadata source_file_date_check reports DATE_MISMATCH"

    dates = observed_dates(df, include_target_date=False)
    if dates and dates != [target_date]:
        return "WARNING_STALE_GLOBAL_FILE", f"row dates {dates} do not match {target_date}"
    return "PASS", "output is fresh for requested target date"


def validate_freshness(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    snapshot_dir: Path | None = None,
) -> pd.DataFrame:
    target_date = target_date or date.today().isoformat()
    rows: list[dict[str, object]] = []
    for filename, pipeline_mode, candidate_version, empty_ok in CSV_OUTPUT_SPECS:
        path = processed_dir / filename
        required = filename in REQUIRED_PRE_FILES or path.exists()
        if not required:
            continue
        status, detail = freshness_status(path, target_date, empty_ok)
        if status == "ERROR_MISSING_REQUIRED_FILE" and filename not in REQUIRED_PRE_FILES:
            status = "WARNING_STALE_GLOBAL_FILE"
        rows.append(
            {
                "target_date": target_date,
                "file_name": filename,
                "path": str(path),
                "pipeline_mode": pipeline_mode,
                "candidate_version": candidate_version,
                "status": status,
                "detail": detail,
                "rows": len(read_csv_lenient(path)) if path.exists() else 0,
                "snapshot_path": str((snapshot_dir or TODAY_DIR / target_date) / filename),
            }
        )

    snapshot = snapshot_dir or TODAY_DIR / target_date
    for filename in ["today_pipeline_report.csv", "today_post_results_report.csv"]:
        snapshot_file = snapshot / filename
        status = "PASS" if snapshot_file.exists() else "WARNING_STALE_GLOBAL_FILE"
        rows.append(
            {
                "target_date": target_date,
                "file_name": filename,
                "path": str(snapshot_file),
                "pipeline_mode": "SNAPSHOT",
                "candidate_version": "GLOBAL_LATEST_CONTEXT",
                "status": status,
                "detail": "snapshot context file present" if snapshot_file.exists() else "snapshot context file not present yet",
                "rows": len(read_csv_lenient(snapshot_file)) if snapshot_file.exists() else 0,
                "snapshot_path": str(snapshot_file),
            }
        )
    return pd.DataFrame(rows)


def write_freshness_reports(
    report: pd.DataFrame,
    processed_dir: Path = PROCESSED_DIR,
    snapshot_dir: Path | None = None,
) -> dict[str, Path]:
    csv_path = processed_dir / FRESHNESS_CSV
    txt_path = processed_dir / FRESHNESS_TXT
    processed_dir.mkdir(parents=True, exist_ok=True)
    report.to_csv(csv_path, index=False)

    counts = report["status"].value_counts().to_dict() if not report.empty else {}
    lines = [
        "# vSIGMA Daily Freshness Report",
        "",
        f"- Target date: {report['target_date'].iloc[0] if not report.empty else ''}",
        f"- PASS: {counts.get('PASS', 0)}",
        f"- EMPTY_OK_NO_BET: {counts.get('EMPTY_OK_NO_BET', 0)}",
        f"- WARNING_STALE_GLOBAL_FILE: {counts.get('WARNING_STALE_GLOBAL_FILE', 0)}",
        f"- ERROR_MISSING_REQUIRED_FILE: {counts.get('ERROR_MISSING_REQUIRED_FILE', 0)}",
        f"- EMPTY_UNEXPECTED: {counts.get('EMPTY_UNEXPECTED', 0)}",
        f"- {PRE_LOCK_NOTE}",
        "",
        format_markdown_table(report, max_rows=200) if not report.empty else "_No files checked._",
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
    report = validate_freshness(processed_dir, target_date, snapshot_dir)
    return write_freshness_reports(report, processed_dir, snapshot_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate vSIGMA daily output freshness.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--snapshot-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    snapshot_dir = args.snapshot_dir or TODAY_DIR / target_date
    paths = run_validation(args.processed_dir, target_date, snapshot_dir)
    print(f"Freshness CSV: {paths['csv']}")
    print(f"Freshness report: {paths['txt']}")


if __name__ == "__main__":
    main()
