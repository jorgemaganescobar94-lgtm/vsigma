from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.calibrate_vsigma_thresholds import (
    BET_RESULTS,
    NUMERIC_THRESHOLD_SPECS,
    apply_rule,
    norm_text,
    parse_bool_series,
    require_columns,
    safe_numeric,
    summarize_subset,
)


DEFAULT_LABELED_CSV = Path("data/processed/vsigma_market_results_labeled.csv")
DEFAULT_DEEP_CSV = Path("data/processed/vsigma_deep_analysis_candidates.csv")
DEFAULT_OUTPUT_DIR = Path("data/processed")
PROMOTED_RULES_FILENAME = "vsigma_threshold_promoted_rules.csv"
PROMOTED_RULES_PRODUCTION_CSV = "vsigma_promoted_rules_production_report.csv"
PROMOTED_RULES_PRODUCTION_TXT = "vsigma_promoted_rules_production_report.txt"

PROMOTED_RULE_REQUIRED_COLUMNS = [
    "rule_type",
    "metric",
    "direction",
    "threshold",
    "rule",
]

PRODUCTION_REPORT_COLUMNS = [
    "production_rank",
    "production_status",
    "production_rule_tier",
    "production_rule_diagnostic",
    "rule_type",
    "metric",
    "direction",
    "threshold",
    "rule",
    "validation_windows",
    "validation_positive_windows",
    "validation_negative_windows",
    "validation_positive_window_rate_pct",
    "source_split_ids",
    "first_validation_start_day",
    "last_validation_end_day",
    "validation_rows_total",
    "validation_graded_bets",
    "validation_wins",
    "validation_losses",
    "validation_pushes",
    "validation_voids",
    "validation_stake_units",
    "validation_profit_units",
    "validation_roi_pct",
    "validation_hit_rate_decided_pct",
    "current_rows_total",
    "current_match_rate_pct",
    "current_actionable_rows",
    "current_actionable_coverage_pct",
    "current_non_actionable_rows",
    "current_graded_bets",
    "current_wins",
    "current_losses",
    "current_pushes",
    "current_voids",
    "current_stake_units",
    "current_profit_units",
    "current_roi_pct",
    "current_hit_rate_decided_pct",
    "promotion_reason",
]

GENERIC_RULE_MATCH_RATE_PCT = 65.0
GENERIC_RULE_ACTIONABLE_COVERAGE_PCT = 65.0
PREMIUM_MIN_VALIDATION_WINDOWS = 2
PREMIUM_MIN_POSITIVE_WINDOW_RATE_PCT = 75.0
PREMIUM_MIN_VALIDATION_GRADED = 14
PREMIUM_MIN_VALIDATION_ROI_PCT = 12.0
PREMIUM_MIN_CURRENT_GRADED = 25
PREMIUM_MIN_CURRENT_ROI_PCT = 5.0


def safe_float(value, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def classify_production_rule_tier(
    production_status: str,
    row: dict[str, object],
) -> tuple[str, str]:
    if production_status != "PROMOTED_PRODUCTION_READY":
        return "NOT_READY", "Rule is not currently production-ready."

    current_match_rate = safe_float(row.get("current_match_rate_pct"))
    actionable_coverage = safe_float(row.get("current_actionable_coverage_pct"))
    is_generic = (
        current_match_rate >= GENERIC_RULE_MATCH_RATE_PCT
        or actionable_coverage >= GENERIC_RULE_ACTIONABLE_COVERAGE_PCT
    )
    if is_generic:
        return (
            "GENERIC_BROAD",
            "Rule matches too much current production surface to approve candidates by itself.",
        )

    validation_windows = safe_float(row.get("validation_windows"))
    positive_window_rate = safe_float(row.get("validation_positive_window_rate_pct"))
    validation_graded = safe_float(row.get("validation_graded_bets"))
    validation_roi = safe_float(row.get("validation_roi_pct"))
    current_graded = safe_float(row.get("current_graded_bets"))
    current_roi = safe_float(row.get("current_roi_pct"))

    premium = (
        validation_windows >= PREMIUM_MIN_VALIDATION_WINDOWS
        and positive_window_rate >= PREMIUM_MIN_POSITIVE_WINDOW_RATE_PCT
        and validation_graded >= PREMIUM_MIN_VALIDATION_GRADED
        and validation_roi >= PREMIUM_MIN_VALIDATION_ROI_PCT
        and current_graded >= PREMIUM_MIN_CURRENT_GRADED
        and current_roi >= PREMIUM_MIN_CURRENT_ROI_PCT
    )
    if premium:
        return (
            "PREMIUM_EVIDENCE",
            "Rule has strong repeated validation, positive current ROI, and acceptable production selectivity.",
        )

    return (
        "STANDARD_EVIDENCE",
        "Rule has positive promoted-rule evidence but does not meet premium evidence requirements.",
    )


def run_step(command: list[str]) -> None:
    print("\n=== RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    subprocess.run(command, check=True)


def prepare_backtest_source_for_rules(df: pd.DataFrame) -> pd.DataFrame:
    require_columns(
        df,
        [
            "market_result_norm",
            "is_actionable",
            "profit_units_effective",
            "stake_units_effective",
        ],
    )

    out = df.copy()
    out["market_result_norm"] = out["market_result_norm"].map(norm_text)
    out["is_actionable"] = parse_bool_series(out["is_actionable"])
    out["profit_units_effective"] = safe_numeric(out["profit_units_effective"]).fillna(0.0)
    out["stake_units_effective"] = safe_numeric(out["stake_units_effective"]).fillna(0.0)
    out["is_graded_bet"] = out["is_actionable"] & out["market_result_norm"].isin(BET_RESULTS)

    for metric, _ in NUMERIC_THRESHOLD_SPECS:
        if metric in out.columns:
            out[metric] = safe_numeric(out[metric])

    return out


def build_promoted_rules_production_report(
    promoted: pd.DataFrame,
    source: pd.DataFrame,
) -> pd.DataFrame:
    require_columns(promoted, PROMOTED_RULE_REQUIRED_COLUMNS)
    prepared_source = prepare_backtest_source_for_rules(source)
    source_rows_total = int(len(prepared_source))
    source_actionable_total = int(prepared_source["is_actionable"].sum())

    if promoted.empty:
        return pd.DataFrame(columns=PRODUCTION_REPORT_COLUMNS)

    rows = []
    for rank, (_, rule_row) in enumerate(promoted.iterrows(), start=1):
        metric = str(rule_row["metric"])
        metric_exists = metric in prepared_source.columns
        subset = apply_rule(prepared_source, rule_row) if metric_exists else prepared_source.iloc[0:0].copy()
        summary = summarize_subset(subset)

        if not metric_exists:
            production_status = "MISSING_SOURCE_METRIC"
        elif summary["rows_total"] == 0:
            production_status = "PROMOTED_NO_CURRENT_MATCHES"
        elif summary["graded_bets"] == 0:
            production_status = "PROMOTED_NO_CURRENT_GRADED_BETS"
        else:
            production_status = "PROMOTED_PRODUCTION_READY"

        row = {
            "production_rank": rank,
            "production_status": production_status,
            "rule_type": rule_row.get("rule_type"),
            "metric": rule_row.get("metric"),
            "direction": rule_row.get("direction"),
            "threshold": rule_row.get("threshold"),
            "rule": rule_row.get("rule"),
            "validation_windows": rule_row.get("validation_windows"),
            "validation_positive_windows": rule_row.get("validation_positive_windows"),
            "validation_negative_windows": rule_row.get("validation_negative_windows"),
            "validation_positive_window_rate_pct": rule_row.get(
                "validation_positive_window_rate_pct"
            ),
            "source_split_ids": rule_row.get("source_split_ids"),
            "first_validation_start_day": rule_row.get("first_validation_start_day"),
            "last_validation_end_day": rule_row.get("last_validation_end_day"),
            "validation_rows_total": rule_row.get("validation_rows_total"),
            "validation_graded_bets": rule_row.get("validation_graded_bets"),
            "validation_wins": rule_row.get("validation_wins"),
            "validation_losses": rule_row.get("validation_losses"),
            "validation_pushes": rule_row.get("validation_pushes"),
            "validation_voids": rule_row.get("validation_voids"),
            "validation_stake_units": rule_row.get("validation_stake_units"),
            "validation_profit_units": rule_row.get("validation_profit_units"),
            "validation_roi_pct": rule_row.get("validation_roi_pct"),
            "validation_hit_rate_decided_pct": rule_row.get(
                "validation_hit_rate_decided_pct"
            ),
            "current_rows_total": summary["rows_total"],
            "current_match_rate_pct": round(
                summary["rows_total"] / source_rows_total * 100.0,
                4,
            )
            if source_rows_total > 0
            else 0.0,
            "current_actionable_rows": int(subset["is_actionable"].sum()) if metric_exists else 0,
            "current_actionable_coverage_pct": round(
                (int(subset["is_actionable"].sum()) if metric_exists else 0)
                / source_actionable_total
                * 100.0,
                4,
            )
            if source_actionable_total > 0
            else 0.0,
            "current_non_actionable_rows": int((~subset["is_actionable"]).sum())
            if metric_exists else 0,
            "current_graded_bets": summary["graded_bets"],
            "current_wins": summary["wins"],
            "current_losses": summary["losses"],
            "current_pushes": summary["pushes"],
            "current_voids": summary["voids"],
            "current_stake_units": summary["stake_units"],
            "current_profit_units": summary["profit_units"],
            "current_roi_pct": summary["roi_pct"],
            "current_hit_rate_decided_pct": summary["hit_rate_decided_pct"],
            "promotion_reason": rule_row.get("promotion_reason"),
        }
        row["production_rule_tier"], row["production_rule_diagnostic"] = (
            classify_production_rule_tier(production_status, row)
        )
        rows.append(row)

    return pd.DataFrame(rows, columns=PRODUCTION_REPORT_COLUMNS)


def write_promoted_rules_text_report(
    path: Path,
    promoted_rules_path: Path,
    source_path: Path,
    report: pd.DataFrame,
) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== VSIGMA PROMOTED RULES PRODUCTION REPORT ===\n")
        f.write(f"Promoted rules source: {promoted_rules_path}\n")
        f.write(f"Backtest source: {source_path}\n")
        f.write(f"Promoted rules consumed: {len(report)}\n")

        if report.empty:
            f.write("No promoted rules are currently available for production governance.\n")
            return

        status_counts = report["production_status"].value_counts().sort_index()
        f.write("\n--- PRODUCTION STATUS COUNTS ---\n")
        for status, count in status_counts.items():
            f.write(f"{status}: {int(count)}\n")

        f.write("\n--- TOP PROMOTED RULES ---\n")
        display_cols = [
            "production_rank",
            "production_status",
            "production_rule_tier",
            "rule",
            "validation_windows",
            "validation_graded_bets",
            "validation_profit_units",
            "validation_roi_pct",
            "current_match_rate_pct",
            "current_actionable_coverage_pct",
            "current_graded_bets",
            "current_profit_units",
            "current_roi_pct",
        ]
        f.write(report[display_cols].head(25).to_string(index=False))
        f.write("\n")


def generate_promoted_rules_production_outputs(
    promoted_rules_path: Path,
    source_path: Path,
    output_dir: Path,
) -> tuple[Path, Path, pd.DataFrame]:
    if not promoted_rules_path.exists():
        raise FileNotFoundError(f"Promoted rules CSV does not exist: {promoted_rules_path}")
    if not source_path.exists():
        raise FileNotFoundError(f"Backtest source CSV does not exist: {source_path}")

    promoted = pd.read_csv(promoted_rules_path)
    source = pd.read_csv(source_path)
    report = build_promoted_rules_production_report(promoted, source)

    csv_path = output_dir / PROMOTED_RULES_PRODUCTION_CSV
    txt_path = output_dir / PROMOTED_RULES_PRODUCTION_TXT
    report.to_csv(csv_path, index=False)
    write_promoted_rules_text_report(txt_path, promoted_rules_path, source_path, report)
    return csv_path, txt_path, report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run vSIGMA backtest and threshold calibration in sequence."
    )
    parser.add_argument(
        "--labeled-csv",
        default=str(DEFAULT_LABELED_CSV),
        help="CSV etiquetado con resultados reales.",
    )
    parser.add_argument(
        "--deep-csv",
        default=str(DEFAULT_DEEP_CSV),
        help="CSV de deep analysis candidates.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directorio para outputs de backtest y calibracion.",
    )
    parser.add_argument(
        "--stake",
        type=float,
        default=1.0,
        help="Stake plano usado por backtest_vsigma.py.",
    )
    parser.add_argument(
        "--min-graded",
        type=int,
        default=3,
        help="Minimo de graded bets por regla de calibracion.",
    )
    parser.add_argument(
        "--min-train-graded",
        type=int,
        default=None,
        help="Minimo de graded bets por regla dentro de cada ventana train. Default = --min-graded.",
    )
    parser.add_argument(
        "--min-train-roi-pct",
        type=float,
        default=0.0,
        help="ROI minimo dentro de train antes de validar una regla out-of-sample.",
    )
    parser.add_argument(
        "--min-train-profit-units",
        type=float,
        default=0.0,
        help="Profit minimo dentro de train antes de validar una regla out-of-sample.",
    )
    parser.add_argument(
        "--min-validation-graded",
        type=int,
        default=1,
        help="Minimo de graded bets por regla dentro de cada ventana validation.",
    )
    parser.add_argument(
        "--min-train-days",
        type=int,
        default=1,
        help="Minimo de dias cronologicos en cada ventana train.",
    )
    parser.add_argument(
        "--train-window-days",
        type=int,
        default=0,
        help="Dias cronologicos de train por split. 0 = ventana expansiva.",
    )
    parser.add_argument(
        "--validation-window-days",
        type=int,
        default=1,
        help="Dias cronologicos futuros por ventana validation.",
    )
    parser.add_argument(
        "--min-validation-windows",
        type=int,
        default=1,
        help="Minimo de ventanas validation para promover una regla.",
    )
    parser.add_argument(
        "--min-validation-roi-pct",
        type=float,
        default=0.0,
        help="ROI OOS agregado minimo para promover una regla.",
    )
    parser.add_argument(
        "--min-validation-profit-units",
        type=float,
        default=0.0,
        help="Profit OOS agregado minimo para promover una regla.",
    )
    parser.add_argument(
        "--promote-top-n",
        type=int,
        default=25,
        help="Maximo de reglas promovidas tras ordenar por performance OOS. 0 = todas.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    enriched_source = output_dir / "vsigma_backtest_enriched_source.csv"

    backtest_command = [
        sys.executable,
        "scripts/backtest_vsigma.py",
        "--labeled-csv",
        args.labeled_csv,
        "--deep-csv",
        args.deep_csv,
        "--output-dir",
        args.output_dir,
        "--stake",
        str(args.stake),
    ]

    calibration_command = [
        sys.executable,
        "scripts/calibrate_vsigma_thresholds.py",
        "--source-csv",
        str(enriched_source),
        "--output-dir",
        args.output_dir,
        "--min-graded",
        str(args.min_graded),
        "--min-validation-graded",
        str(args.min_validation_graded),
        "--min-train-roi-pct",
        str(args.min_train_roi_pct),
        "--min-train-profit-units",
        str(args.min_train_profit_units),
        "--min-train-days",
        str(args.min_train_days),
        "--train-window-days",
        str(args.train_window_days),
        "--validation-window-days",
        str(args.validation_window_days),
        "--min-validation-windows",
        str(args.min_validation_windows),
        "--min-validation-roi-pct",
        str(args.min_validation_roi_pct),
        "--min-validation-profit-units",
        str(args.min_validation_profit_units),
        "--promote-top-n",
        str(args.promote_top_n),
    ]
    if args.min_train_graded is not None:
        calibration_command.extend(["--min-train-graded", str(args.min_train_graded)])

    run_step(backtest_command)
    run_step(calibration_command)

    promoted_rules_path = output_dir / PROMOTED_RULES_FILENAME
    production_csv_path, production_txt_path, production_report = (
        generate_promoted_rules_production_outputs(
            promoted_rules_path=promoted_rules_path,
            source_path=enriched_source,
            output_dir=output_dir,
        )
    )

    print("\n=== VSIGMA BACKTEST + CALIBRATION COMPLETADO ===")
    print(f"Backtest source: {enriched_source}")
    print(f"Calibration candidates: {output_dir / 'vsigma_threshold_calibration_candidates.csv'}")
    print(f"Rolling splits: {output_dir / 'vsigma_threshold_rolling_splits.csv'}")
    print(f"Rolling validation: {output_dir / 'vsigma_threshold_rolling_validation.csv'}")
    print(f"Promoted rules: {promoted_rules_path}")
    print(f"Calibration report: {output_dir / 'vsigma_threshold_calibration_report.txt'}")
    print(f"Production promoted-rules CSV: {production_csv_path}")
    print(f"Production promoted-rules report: {production_txt_path}")
    print(f"Production promoted rules consumed: {len(production_report)}")


if __name__ == "__main__":
    main()
