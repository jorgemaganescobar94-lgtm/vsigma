from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_PROCESSED_DIR = Path("data/processed")
DEFAULT_REPORT_CSV = DEFAULT_PROCESSED_DIR / "vsigma_final_export_reconciliation_report.csv"

DEEP_CSV = "vsigma_deep_analysis_candidates.csv"
SUMMARY_CSV = "vsigma_final_governance_summary.csv"

EXPORT_FILES = {
    "APPROVED_PREMIUM": "vsigma_final_approved_premium_candidates.csv",
    "APPROVED_STANDARD": "vsigma_final_approved_standard_candidates.csv",
    "DOWNGRADED": "vsigma_final_downgraded_candidates.csv",
    "BLOCKED": "vsigma_final_blocked_candidates.csv",
    "WATCH": "vsigma_final_watch_candidates.csv",
}


def read_csv_required(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return pd.read_csv(path)


def parse_expected_dates(values: list[str] | None) -> list[str]:
    return sorted({value.strip() for value in values or [] if value.strip()})


def validate_exports(
    processed_dir: Path,
    expected_dates: list[str] | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    deep = read_csv_required(processed_dir / DEEP_CSV, "combined deep candidates")
    summary = read_csv_required(processed_dir / SUMMARY_CSV, "governance summary")
    exports = {
        bucket: read_csv_required(processed_dir / filename, f"{bucket.lower()} export")
        for bucket, filename in EXPORT_FILES.items()
    }

    errors: list[str] = []
    report_rows: list[dict[str, object]] = [
        {"check_name": "combined_deep_rows", "expected": len(deep), "observed": len(deep), "status": "PASS"}
    ]

    export_total = sum(len(df) for df in exports.values())
    total_status = "PASS" if export_total == len(deep) else "FAIL"
    report_rows.append(
        {
            "check_name": "final_export_total_rows",
            "expected": len(deep),
            "observed": export_total,
            "status": total_status,
        }
    )
    if total_status == "FAIL":
        errors.append(f"Final export rows {export_total} do not match combined deep rows {len(deep)}.")

    deep_fixtures = set(deep["fixture_id"].tolist()) if "fixture_id" in deep.columns else set()
    export_fixtures: set[object] = set()
    fixture_row_count = 0

    for bucket, df in exports.items():
        bucket_rows = len(df)
        report_rows.append(
            {
                "check_name": f"{bucket.lower()}_export_rows",
                "expected": bucket_rows,
                "observed": bucket_rows,
                "status": "PASS",
            }
        )

        if "fixture_id" not in df.columns:
            errors.append(f"{bucket} export is missing fixture_id.")
            continue

        fixture_row_count += len(df["fixture_id"])
        export_fixtures.update(df["fixture_id"].tolist())

        if df["fixture_id"].duplicated().any():
            duplicated = df.loc[df["fixture_id"].duplicated(), "fixture_id"].head(10).tolist()
            errors.append(f"{bucket} export has duplicate fixture_id values: {duplicated}")

        if "final_execution_bucket" not in df.columns:
            errors.append(f"{bucket} export is missing final_execution_bucket.")
            continue

        bad_bucket = df[df["final_execution_bucket"].astype(str) != bucket]
        if not bad_bucket.empty:
            errors.append(
                f"{bucket} export contains rows with another final_execution_bucket: "
                f"{bad_bucket['fixture_id'].head(10).tolist()}"
            )

    if fixture_row_count != len(export_fixtures):
        errors.append("fixture_id overlap exists across final execution export files.")

    if "fixture_id" not in deep.columns:
        errors.append("Combined deep candidates are missing fixture_id.")
    elif deep["fixture_id"].duplicated().any():
        duplicated = deep.loc[deep["fixture_id"].duplicated(), "fixture_id"].head(10).tolist()
        errors.append(f"Combined deep candidates have duplicate fixture_id values: {duplicated}")
    elif export_fixtures != deep_fixtures:
        errors.append(
            f"Final export fixture_id set does not match combined deep candidates: "
            f"exports={len(export_fixtures)} deep={len(deep_fixtures)}."
        )

    overall = summary[summary["summary_scope"].astype(str) == "overall"] if "summary_scope" in summary.columns else pd.DataFrame()
    if len(overall) != 1:
        errors.append(f"Expected exactly one overall governance summary row, found {len(overall)}.")
    else:
        observed = int(overall.iloc[0]["rows_total"])
        report_rows.append(
            {
                "check_name": "summary_overall_rows",
                "expected": len(deep),
                "observed": observed,
                "status": "PASS" if observed == len(deep) else "FAIL",
            }
        )
        if observed != len(deep):
            errors.append(f"Governance summary overall rows_total {observed} does not match deep rows {len(deep)}.")

    bucket_summary = (
        summary[summary["summary_scope"].astype(str) == "by_final_execution_bucket"]
        if "summary_scope" in summary.columns
        else pd.DataFrame()
    )
    summary_counts = {
        str(row["final_execution_bucket"]): int(row["rows_total"])
        for _, row in bucket_summary.iterrows()
        if pd.notna(row.get("final_execution_bucket"))
    }
    for bucket, df in exports.items():
        observed = summary_counts.get(bucket, 0)
        expected = len(df)
        status = "PASS" if observed == expected else "FAIL"
        report_rows.append(
            {
                "check_name": f"summary_{bucket.lower()}_rows",
                "expected": expected,
                "observed": observed,
                "status": status,
            }
        )
        if status == "FAIL":
            errors.append(f"Governance summary {bucket} rows {observed} do not match export rows {expected}.")

    expected_dates = parse_expected_dates(expected_dates)
    if expected_dates:
        if "historical_batch_date" not in deep.columns:
            errors.append("Combined deep candidates are missing historical_batch_date.")
        else:
            observed_dates = sorted(deep["historical_batch_date"].dropna().astype(str).unique().tolist())
            status = "PASS" if observed_dates == expected_dates else "FAIL"
            report_rows.append(
                {
                    "check_name": "historical_batch_dates",
                    "expected": "|".join(expected_dates),
                    "observed": "|".join(observed_dates),
                    "status": status,
                }
            )
            if status == "FAIL":
                errors.append(f"historical_batch_date values {observed_dates} do not match expected {expected_dates}.")

    report = pd.DataFrame(report_rows)
    if errors:
        failed_checks = set(report.loc[report["status"] == "FAIL", "check_name"].astype(str))
        for idx, row in report.iterrows():
            if row["check_name"] in failed_checks:
                continue
            report.loc[idx, "status"] = row["status"]

    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate final execution exports against combined deep candidates and governance summary."
    )
    parser.add_argument("--processed-dir", default=str(DEFAULT_PROCESSED_DIR))
    parser.add_argument("--expected-date", action="append", dest="expected_dates", help="Expected historical batch date.")
    parser.add_argument("--report-csv", default=str(DEFAULT_REPORT_CSV))
    args = parser.parse_args()

    processed_dir = Path(args.processed_dir)
    report, errors = validate_exports(processed_dir, args.expected_dates)

    report_path = Path(args.report_csv)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(report_path, index=False)

    if errors:
        print("FINAL EXPORT RECONCILIATION FAILED")
        for error in errors:
            print(f"- {error}")
        print(f"Report: {report_path}")
        raise SystemExit(1)

    print("FINAL EXPORT RECONCILIATION PASSED")
    print(report.to_string(index=False))
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
