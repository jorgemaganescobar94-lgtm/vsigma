from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_SOURCE_CSV = Path("data/processed/vsigma_backtest_enriched_source.csv")
DEFAULT_OUTPUT_DIR = Path("data/processed")

BET_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}

NUMERIC_THRESHOLD_SPECS = [
    ("model_edge_abs_num", ">="),
    ("model_edge_pct_num", ">="),
    ("selection_score", ">="),
    ("vsigma_pre_score", ">="),
    ("primary_model_prob", ">="),
    ("primary_edge", ">="),
    ("odds_num", "<="),
]

CATEGORY_COLUMNS = [
    "market_primary",
    "edge_floor_band",
    "execution_verdict",
    "final_recommendation",
    "confidence_band",
    "shortlist_bucket",
    "analysis_label",
    "league",
]

ROLLING_SPLIT_COLUMNS = [
    "split_id",
    "train_start_day",
    "train_end_day",
    "validation_start_day",
    "validation_end_day",
    "train_days",
    "validation_days",
    "train_rows_total",
    "train_graded_bets",
    "train_profit_units",
    "train_roi_pct",
    "validation_rows_total",
    "validation_graded_bets",
    "validation_profit_units",
    "validation_roi_pct",
]

ROLLING_VALIDATION_COLUMNS = [
    "split_id",
    "train_start_day",
    "train_end_day",
    "validation_start_day",
    "validation_end_day",
    "train_days",
    "validation_days",
    "rule_type",
    "metric",
    "direction",
    "threshold",
    "rule",
    "train_rows_total",
    "train_graded_bets",
    "train_wins",
    "train_losses",
    "train_pushes",
    "train_voids",
    "train_stake_units",
    "train_profit_units",
    "train_roi_pct",
    "train_hit_rate_decided_pct",
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
]

PROMOTED_RULE_COLUMNS = [
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
    "train_window_rows_total",
    "train_window_graded_bets",
    "train_window_wins",
    "train_window_losses",
    "train_window_pushes",
    "train_window_voids",
    "train_window_stake_units",
    "train_window_profit_units",
    "train_window_roi_pct",
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
    "promotion_reason",
]


def norm_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def parse_bool_series(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series.fillna(False)

    normalized = series.map(norm_text)
    return normalized.isin({"1", "TRUE", "YES", "Y", "SI", "S"})


def require_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in backtest source: {missing}")


def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def summarize_subset(subset: pd.DataFrame) -> dict:
    graded = subset[subset["is_graded_bet"]].copy()
    wins = int((graded["market_result_norm"] == "WIN").sum())
    losses = int((graded["market_result_norm"] == "LOSS").sum())
    pushes = int((graded["market_result_norm"] == "PUSH").sum())
    voids = int((graded["market_result_norm"] == "VOID").sum())
    decided = wins + losses

    stake_units = float(graded["stake_units_effective"].sum())
    profit_units = float(graded["profit_units_effective"].sum())

    return {
        "rows_total": int(len(subset)),
        "graded_bets": int(len(graded)),
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "voids": voids,
        "stake_units": round(stake_units, 4),
        "profit_units": round(profit_units, 4),
        "roi_pct": round((profit_units / stake_units * 100.0), 4) if stake_units > 0 else np.nan,
        "hit_rate_decided_pct": round((wins / decided * 100.0), 4) if decided > 0 else np.nan,
    }


def sort_calibration(calibration: pd.DataFrame) -> pd.DataFrame:
    if calibration.empty:
        return calibration

    return calibration.sort_values(
        ["profit_units", "roi_pct", "graded_bets", "rule"],
        ascending=[False, False, False, True],
        na_position="last",
    ).reset_index(drop=True)


def build_numeric_thresholds(df: pd.DataFrame, min_graded: int) -> pd.DataFrame:
    rows = []

    for metric, direction in NUMERIC_THRESHOLD_SPECS:
        if metric not in df.columns:
            continue

        values = safe_numeric(df[metric]).dropna().sort_values().unique()
        for threshold in values:
            metric_values = safe_numeric(df[metric])
            if direction == ">=":
                subset = df[metric_values >= threshold]
                rule = f"{metric} >= {threshold:g}"
            else:
                subset = df[metric_values <= threshold]
                rule = f"{metric} <= {threshold:g}"

            summary = summarize_subset(subset)
            if summary["graded_bets"] < min_graded:
                continue

            rows.append({
                "rule_type": "NUMERIC_THRESHOLD",
                "metric": metric,
                "direction": direction,
                "threshold": threshold,
                "rule": rule,
                **summary,
            })

    if not rows:
        return pd.DataFrame()

    return sort_calibration(pd.DataFrame(rows))


def build_category_thresholds(df: pd.DataFrame, min_graded: int) -> pd.DataFrame:
    rows = []

    for col in CATEGORY_COLUMNS:
        if col not in df.columns:
            continue

        filled = df[col].fillna("UNKNOWN").astype(str).str.strip().replace("", "UNKNOWN")
        for value, subset_idx in filled.groupby(filled).groups.items():
            subset = df.loc[subset_idx]
            summary = summarize_subset(subset)
            if summary["graded_bets"] < min_graded:
                continue

            rows.append({
                "rule_type": "CATEGORY_BUCKET",
                "metric": col,
                "direction": "==",
                "threshold": value,
                "rule": f"{col} == {value}",
                **summary,
            })

    if not rows:
        return pd.DataFrame()

    return sort_calibration(pd.DataFrame(rows))


def build_candidate_rules(df: pd.DataFrame, min_graded: int) -> pd.DataFrame:
    numeric = build_numeric_thresholds(df, min_graded)
    category = build_category_thresholds(df, min_graded)
    return sort_calibration(pd.concat([numeric, category], ignore_index=True))


def filter_train_candidates(
    candidates: pd.DataFrame,
    min_train_roi_pct: float,
    min_train_profit_units: float,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates

    roi = safe_numeric(candidates["roi_pct"])
    profit = safe_numeric(candidates["profit_units"])
    keep = (profit >= min_train_profit_units) & (roi >= min_train_roi_pct)
    return candidates[keep].copy()


def apply_rule(df: pd.DataFrame, rule_row: pd.Series) -> pd.DataFrame:
    metric = str(rule_row["metric"])
    direction = str(rule_row["direction"])
    threshold = rule_row["threshold"]

    if metric not in df.columns:
        return df.iloc[0:0].copy()

    if rule_row["rule_type"] == "NUMERIC_THRESHOLD":
        metric_values = safe_numeric(df[metric])
        threshold_num = pd.to_numeric(pd.Series([threshold]), errors="coerce").iloc[0]
        if pd.isna(threshold_num):
            return df.iloc[0:0].copy()
        if direction == ">=":
            return df[metric_values >= threshold_num].copy()
        if direction == "<=":
            return df[metric_values <= threshold_num].copy()
        raise ValueError(f"Unsupported numeric rule direction: {direction}")

    if rule_row["rule_type"] == "CATEGORY_BUCKET":
        filled = df[metric].fillna("UNKNOWN").astype(str).str.strip().replace("", "UNKNOWN")
        return df[filled == str(threshold)].copy()

    raise ValueError(f"Unsupported rule type: {rule_row['rule_type']}")


def add_chronological_day(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    if "date_day" in out.columns:
        raw_dates = out["date_day"]
    elif "date_dt" in out.columns:
        raw_dates = out["date_dt"]
    elif "date" in out.columns:
        raw_dates = out["date"]
    else:
        raise ValueError("Rolling calibration requires one of these date columns: date_day, date_dt, date")

    parsed = pd.to_datetime(raw_dates.replace("UNKNOWN_DATE", np.nan), errors="coerce", utc=True)
    out["_chronological_day_dt"] = parsed.dt.floor("D")
    out["_chronological_day"] = out["_chronological_day_dt"].dt.strftime("%Y-%m-%d")
    return out


def make_rolling_splits(
    df: pd.DataFrame,
    train_window_days: int,
    validation_window_days: int,
    min_train_days: int,
) -> list[dict]:
    if validation_window_days < 1:
        raise ValueError("--validation-window-days must be >= 1")
    if train_window_days < 0:
        raise ValueError("--train-window-days must be >= 0")
    if min_train_days < 1:
        raise ValueError("--min-train-days must be >= 1")

    valid_days = (
        df["_chronological_day_dt"]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )
    splits = []

    for validation_start_idx in range(min_train_days, len(valid_days), validation_window_days):
        validation_days = valid_days[
            validation_start_idx: validation_start_idx + validation_window_days
        ]
        if not validation_days:
            continue

        train_start_idx = 0
        if train_window_days:
            train_start_idx = max(0, validation_start_idx - train_window_days)

        train_days = valid_days[train_start_idx:validation_start_idx]
        if len(train_days) < min_train_days:
            continue

        splits.append({
            "split_id": len(splits) + 1,
            "train_days": train_days,
            "validation_days": validation_days,
            "train_start_day": train_days[0].strftime("%Y-%m-%d"),
            "train_end_day": train_days[-1].strftime("%Y-%m-%d"),
            "validation_start_day": validation_days[0].strftime("%Y-%m-%d"),
            "validation_end_day": validation_days[-1].strftime("%Y-%m-%d"),
        })

    return splits


def build_rolling_validation(
    df: pd.DataFrame,
    min_train_graded: int,
    min_train_roi_pct: float,
    min_train_profit_units: float,
    min_validation_graded: int,
    train_window_days: int,
    validation_window_days: int,
    min_train_days: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    working = add_chronological_day(df)
    dated = working[working["_chronological_day_dt"].notna()].copy()
    splits = make_rolling_splits(
        dated,
        train_window_days=train_window_days,
        validation_window_days=validation_window_days,
        min_train_days=min_train_days,
    )

    rows = []
    split_rows = []
    train_candidate_rows_built = 0
    train_candidate_rows_after_filters = 0
    for split in splits:
        train_df = dated[dated["_chronological_day_dt"].isin(split["train_days"])].copy()
        validation_df = dated[dated["_chronological_day_dt"].isin(split["validation_days"])].copy()
        train_split_summary = summarize_subset(train_df)
        validation_split_summary = summarize_subset(validation_df)
        split_rows.append({
            "split_id": split["split_id"],
            "train_start_day": split["train_start_day"],
            "train_end_day": split["train_end_day"],
            "validation_start_day": split["validation_start_day"],
            "validation_end_day": split["validation_end_day"],
            "train_days": len(split["train_days"]),
            "validation_days": len(split["validation_days"]),
            "train_rows_total": train_split_summary["rows_total"],
            "train_graded_bets": train_split_summary["graded_bets"],
            "train_profit_units": train_split_summary["profit_units"],
            "train_roi_pct": train_split_summary["roi_pct"],
            "validation_rows_total": validation_split_summary["rows_total"],
            "validation_graded_bets": validation_split_summary["graded_bets"],
            "validation_profit_units": validation_split_summary["profit_units"],
            "validation_roi_pct": validation_split_summary["roi_pct"],
        })

        train_candidates = build_candidate_rules(train_df, min_train_graded)
        train_candidate_rows_built += int(len(train_candidates))
        train_candidates = filter_train_candidates(
            train_candidates,
            min_train_roi_pct=min_train_roi_pct,
            min_train_profit_units=min_train_profit_units,
        )
        train_candidate_rows_after_filters += int(len(train_candidates))
        if train_candidates.empty:
            continue

        for _, rule_row in train_candidates.iterrows():
            validation_subset = apply_rule(validation_df, rule_row)
            validation_summary = summarize_subset(validation_subset)
            if validation_summary["graded_bets"] < min_validation_graded:
                continue

            rows.append({
                "split_id": split["split_id"],
                "train_start_day": split["train_start_day"],
                "train_end_day": split["train_end_day"],
                "validation_start_day": split["validation_start_day"],
                "validation_end_day": split["validation_end_day"],
                "train_days": len(split["train_days"]),
                "validation_days": len(split["validation_days"]),
                "rule_type": rule_row["rule_type"],
                "metric": rule_row["metric"],
                "direction": rule_row["direction"],
                "threshold": rule_row["threshold"],
                "rule": rule_row["rule"],
                "train_rows_total": int(rule_row["rows_total"]),
                "train_graded_bets": int(rule_row["graded_bets"]),
                "train_wins": int(rule_row["wins"]),
                "train_losses": int(rule_row["losses"]),
                "train_pushes": int(rule_row["pushes"]),
                "train_voids": int(rule_row["voids"]),
                "train_stake_units": float(rule_row["stake_units"]),
                "train_profit_units": float(rule_row["profit_units"]),
                "train_roi_pct": rule_row["roi_pct"],
                "train_hit_rate_decided_pct": rule_row["hit_rate_decided_pct"],
                "validation_rows_total": validation_summary["rows_total"],
                "validation_graded_bets": validation_summary["graded_bets"],
                "validation_wins": validation_summary["wins"],
                "validation_losses": validation_summary["losses"],
                "validation_pushes": validation_summary["pushes"],
                "validation_voids": validation_summary["voids"],
                "validation_stake_units": validation_summary["stake_units"],
                "validation_profit_units": validation_summary["profit_units"],
                "validation_roi_pct": validation_summary["roi_pct"],
                "validation_hit_rate_decided_pct": validation_summary["hit_rate_decided_pct"],
            })

    metadata = {
        "dated_rows": int(len(dated)),
        "undated_rows": int(len(working) - len(dated)),
        "chronological_days": int(dated["_chronological_day"].nunique()) if not dated.empty else 0,
        "splits_built": int(len(splits)),
        "train_candidate_rows_built": train_candidate_rows_built,
        "train_candidate_rows_after_filters": train_candidate_rows_after_filters,
    }

    split_manifest = pd.DataFrame(split_rows, columns=ROLLING_SPLIT_COLUMNS)
    if not rows:
        return pd.DataFrame(columns=ROLLING_VALIDATION_COLUMNS), split_manifest, metadata

    out = pd.DataFrame(rows, columns=ROLLING_VALIDATION_COLUMNS)
    out = out.sort_values(
        [
            "validation_profit_units",
            "validation_roi_pct",
            "validation_graded_bets",
            "split_id",
            "rule",
        ],
        ascending=[False, False, False, True, True],
        na_position="last",
    ).reset_index(drop=True)
    return out, split_manifest, metadata


def aggregate_promoted_rules(
    rolling: pd.DataFrame,
    min_validation_windows: int,
    min_validation_graded: int,
    min_validation_roi_pct: float,
    min_validation_profit_units: float,
    top_n: int,
) -> pd.DataFrame:
    if min_validation_windows < 1:
        raise ValueError("--min-validation-windows must be >= 1")
    if top_n < 0:
        raise ValueError("--promote-top-n must be >= 0")
    if rolling.empty:
        return pd.DataFrame(columns=PROMOTED_RULE_COLUMNS)

    rows = []
    group_cols = ["rule_type", "metric", "direction", "threshold", "rule"]
    for keys, grp in rolling.groupby(group_cols, dropna=False, sort=False):
        validation_stake = float(grp["validation_stake_units"].sum())
        validation_profit = float(grp["validation_profit_units"].sum())
        validation_wins = int(grp["validation_wins"].sum())
        validation_losses = int(grp["validation_losses"].sum())
        validation_decided = validation_wins + validation_losses

        train_stake = float(grp["train_stake_units"].sum())
        train_profit = float(grp["train_profit_units"].sum())
        train_wins = int(grp["train_wins"].sum())
        train_losses = int(grp["train_losses"].sum())

        row = {
            "rule_type": keys[0],
            "metric": keys[1],
            "direction": keys[2],
            "threshold": keys[3],
            "rule": keys[4],
            "validation_windows": int(grp["split_id"].nunique()),
            "validation_positive_windows": int((grp["validation_profit_units"] > 0).sum()),
            "validation_negative_windows": int((grp["validation_profit_units"] < 0).sum()),
            "validation_positive_window_rate_pct": round(
                ((grp["validation_profit_units"] > 0).sum() / grp["split_id"].nunique()) * 100.0,
                4,
            ) if grp["split_id"].nunique() > 0 else np.nan,
            "source_split_ids": ",".join(str(split_id) for split_id in sorted(grp["split_id"].unique())),
            "first_validation_start_day": str(grp["validation_start_day"].min()),
            "last_validation_end_day": str(grp["validation_end_day"].max()),
            "train_window_rows_total": int(grp["train_rows_total"].sum()),
            "train_window_graded_bets": int(grp["train_graded_bets"].sum()),
            "train_window_wins": train_wins,
            "train_window_losses": train_losses,
            "train_window_pushes": int(grp["train_pushes"].sum()),
            "train_window_voids": int(grp["train_voids"].sum()),
            "train_window_stake_units": round(train_stake, 4),
            "train_window_profit_units": round(train_profit, 4),
            "train_window_roi_pct": round(train_profit / train_stake * 100.0, 4)
            if train_stake > 0 else np.nan,
            "validation_rows_total": int(grp["validation_rows_total"].sum()),
            "validation_graded_bets": int(grp["validation_graded_bets"].sum()),
            "validation_wins": validation_wins,
            "validation_losses": validation_losses,
            "validation_pushes": int(grp["validation_pushes"].sum()),
            "validation_voids": int(grp["validation_voids"].sum()),
            "validation_stake_units": round(validation_stake, 4),
            "validation_profit_units": round(validation_profit, 4),
            "validation_roi_pct": round(validation_profit / validation_stake * 100.0, 4)
            if validation_stake > 0 else np.nan,
            "validation_hit_rate_decided_pct": round(validation_wins / validation_decided * 100.0, 4)
            if validation_decided > 0 else np.nan,
        }
        row["promotion_reason"] = (
            f"validation_windows>={min_validation_windows}; "
            f"validation_graded_bets>={min_validation_graded}; "
            f"validation_profit_units>={min_validation_profit_units:g}; "
            f"validation_roi_pct>={min_validation_roi_pct:g}"
        )
        rows.append(row)

    promoted = pd.DataFrame(rows, columns=PROMOTED_RULE_COLUMNS)
    promoted = promoted[
        (promoted["validation_windows"] >= min_validation_windows)
        & (promoted["validation_graded_bets"] >= min_validation_graded)
        & (promoted["validation_profit_units"] >= min_validation_profit_units)
        & (promoted["validation_roi_pct"] >= min_validation_roi_pct)
    ].copy()

    if promoted.empty:
        return pd.DataFrame(columns=PROMOTED_RULE_COLUMNS)

    promoted = promoted.sort_values(
        [
            "validation_profit_units",
            "validation_roi_pct",
            "validation_graded_bets",
            "validation_windows",
            "rule",
        ],
        ascending=[False, False, False, False, True],
        na_position="last",
    ).reset_index(drop=True)

    if top_n:
        promoted = promoted.head(top_n).copy()

    return promoted


def write_report(
    path: Path,
    source_path: Path,
    overall: dict,
    calibration: pd.DataFrame,
    min_graded: int,
    rolling: pd.DataFrame,
    split_manifest: pd.DataFrame,
    promoted: pd.DataFrame,
    rolling_metadata: dict,
    min_train_graded: int,
    min_train_roi_pct: float,
    min_train_profit_units: float,
    min_validation_graded: int,
    min_validation_windows: int,
    train_window_days: int,
    validation_window_days: int,
    min_train_days: int,
    min_validation_roi_pct: float,
    min_validation_profit_units: float,
    promote_top_n: int,
) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("=== VSIGMA THRESHOLD CALIBRATION ===\n")
        f.write(f"Source: {source_path}\n")
        f.write(f"Minimum graded bets per rule: {min_graded}\n\n")
        f.write("--- OVERALL GRADED ACTIONABLE ---\n")
        for key, value in overall.items():
            f.write(f"{key}: {value}\n")

        f.write("\n--- TOP RULES ---\n")
        if calibration.empty:
            f.write("No rules met the minimum graded-bet requirement.\n")
        else:
            f.write(calibration.head(25).to_string(index=False))
            f.write("\n")

        f.write("\n--- ROLLING OUT-OF-SAMPLE VALIDATION ---\n")
        f.write(f"Dated rows: {rolling_metadata['dated_rows']}\n")
        f.write(f"Undated rows excluded from rolling validation: {rolling_metadata['undated_rows']}\n")
        f.write(f"Chronological days: {rolling_metadata['chronological_days']}\n")
        f.write(f"Splits built: {rolling_metadata['splits_built']}\n")
        f.write(f"Train window days: {train_window_days} (0 means expanding window)\n")
        f.write(f"Validation window days: {validation_window_days}\n")
        f.write(f"Minimum train chronological days: {min_train_days}\n")
        f.write(f"Minimum train graded bets per candidate: {min_train_graded}\n")
        f.write(f"Minimum train profit units per candidate: {min_train_profit_units:g}\n")
        f.write(f"Minimum train ROI percentage per candidate: {min_train_roi_pct:g}\n")
        f.write(f"Minimum validation graded bets per split: {min_validation_graded}\n")
        f.write(f"Train candidate rows before filters: {rolling_metadata['train_candidate_rows_built']}\n")
        f.write(
            "Train candidate rows after train filters: "
            f"{rolling_metadata['train_candidate_rows_after_filters']}\n"
        )
        f.write(f"Rolling validation candidate rows: {len(rolling)}\n\n")

        f.write("Rolling split manifest:\n")
        if split_manifest.empty:
            f.write("No chronological train/validation splits were built.\n\n")
        else:
            f.write(split_manifest.to_string(index=False))
            f.write("\n\n")

        if rolling.empty:
            f.write("No rolling validation rows met the validation graded-bet requirement.\n")
        else:
            f.write(rolling.head(25).to_string(index=False))
            f.write("\n")

        f.write("\n--- PROMOTED RULES ---\n")
        f.write(f"Minimum validation windows for promotion: {min_validation_windows}\n")
        f.write(f"Minimum aggregate validation profit units for promotion: {min_validation_profit_units:g}\n")
        f.write(f"Minimum aggregate validation ROI percentage for promotion: {min_validation_roi_pct:g}\n")
        f.write(f"Promote top N: {promote_top_n} (0 means all promoted rules)\n")
        f.write(f"Promoted rules: {len(promoted)}\n\n")
        if promoted.empty:
            f.write("No rules met the rolling promotion requirements.\n")
        else:
            f.write(promoted.head(25).to_string(index=False))
            f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Calibrate vSIGMA thresholds from real graded backtest outcomes."
    )
    parser.add_argument(
        "--source-csv",
        default=str(DEFAULT_SOURCE_CSV),
        help="Backtest enriched source CSV generated by scripts/backtest_vsigma.py.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for calibration outputs.",
    )
    parser.add_argument(
        "--min-graded",
        type=int,
        default=3,
        help="Minimum graded actionable bets required for a candidate rule.",
    )
    parser.add_argument(
        "--min-train-graded",
        type=int,
        default=None,
        help="Minimum graded bets required inside each rolling train window. Defaults to --min-graded.",
    )
    parser.add_argument(
        "--min-train-roi-pct",
        type=float,
        default=0.0,
        help="Minimum in-sample train ROI percentage required before a rule is validated out of sample.",
    )
    parser.add_argument(
        "--min-train-profit-units",
        type=float,
        default=0.0,
        help="Minimum in-sample train profit units required before a rule is validated out of sample.",
    )
    parser.add_argument(
        "--min-validation-graded",
        type=int,
        default=1,
        help="Minimum graded bets required when a trained rule is evaluated on a validation split.",
    )
    parser.add_argument(
        "--min-train-days",
        type=int,
        default=1,
        help="Minimum number of chronological match days in each train window.",
    )
    parser.add_argument(
        "--train-window-days",
        type=int,
        default=0,
        help="Number of chronological match days in each train window. Use 0 for expanding windows.",
    )
    parser.add_argument(
        "--validation-window-days",
        type=int,
        default=1,
        help="Number of future chronological match days in each validation window.",
    )
    parser.add_argument(
        "--min-validation-windows",
        type=int,
        default=1,
        help="Minimum number of rolling validation windows required to promote a rule.",
    )
    parser.add_argument(
        "--min-validation-roi-pct",
        type=float,
        default=0.0,
        help="Minimum aggregate out-of-sample ROI percentage required to promote a rule.",
    )
    parser.add_argument(
        "--min-validation-profit-units",
        type=float,
        default=0.0,
        help="Minimum aggregate out-of-sample profit units required to promote a rule.",
    )
    parser.add_argument(
        "--promote-top-n",
        type=int,
        default=25,
        help="Maximum promoted rules to write after sorting by out-of-sample performance. Use 0 for all.",
    )
    args = parser.parse_args()
    min_train_graded = args.min_train_graded if args.min_train_graded is not None else args.min_graded

    source_path = Path(args.source_csv)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not source_path.exists():
        raise FileNotFoundError(f"Backtest source does not exist: {source_path}")

    df = pd.read_csv(source_path)
    require_columns(
        df,
        [
            "market_result_norm",
            "is_actionable",
            "profit_units_effective",
            "stake_units_effective",
        ],
    )

    df["market_result_norm"] = df["market_result_norm"].map(norm_text)
    df["is_actionable"] = parse_bool_series(df["is_actionable"])
    df["profit_units_effective"] = safe_numeric(df["profit_units_effective"]).fillna(0.0)
    df["stake_units_effective"] = safe_numeric(df["stake_units_effective"]).fillna(0.0)
    df["is_graded_bet"] = df["is_actionable"] & df["market_result_norm"].isin(BET_RESULTS)

    for metric, _ in NUMERIC_THRESHOLD_SPECS:
        if metric in df.columns:
            df[metric] = safe_numeric(df[metric])

    overall = summarize_subset(df[df["is_graded_bet"]].copy())
    calibration = build_candidate_rules(df, args.min_graded)
    rolling, split_manifest, rolling_metadata = build_rolling_validation(
        df,
        min_train_graded=min_train_graded,
        min_train_roi_pct=args.min_train_roi_pct,
        min_train_profit_units=args.min_train_profit_units,
        min_validation_graded=args.min_validation_graded,
        train_window_days=args.train_window_days,
        validation_window_days=args.validation_window_days,
        min_train_days=args.min_train_days,
    )
    promoted = aggregate_promoted_rules(
        rolling,
        min_validation_windows=args.min_validation_windows,
        min_validation_graded=args.min_validation_graded,
        min_validation_roi_pct=args.min_validation_roi_pct,
        min_validation_profit_units=args.min_validation_profit_units,
        top_n=args.promote_top_n,
    )

    candidates_path = output_dir / "vsigma_threshold_calibration_candidates.csv"
    split_manifest_path = output_dir / "vsigma_threshold_rolling_splits.csv"
    rolling_path = output_dir / "vsigma_threshold_rolling_validation.csv"
    promoted_path = output_dir / "vsigma_threshold_promoted_rules.csv"
    report_path = output_dir / "vsigma_threshold_calibration_report.txt"

    calibration.to_csv(candidates_path, index=False)
    split_manifest.to_csv(split_manifest_path, index=False)
    rolling.to_csv(rolling_path, index=False)
    promoted.to_csv(promoted_path, index=False)
    write_report(
        report_path,
        source_path,
        overall,
        calibration,
        args.min_graded,
        rolling,
        split_manifest,
        promoted,
        rolling_metadata,
        min_train_graded,
        args.min_train_roi_pct,
        args.min_train_profit_units,
        args.min_validation_graded,
        args.min_validation_windows,
        args.train_window_days,
        args.validation_window_days,
        args.min_train_days,
        args.min_validation_roi_pct,
        args.min_validation_profit_units,
        args.promote_top_n,
    )

    print("\n=== VSIGMA THRESHOLD CALIBRATION ===")
    print(f"Rows total: {len(df)}")
    print(f"Graded actionable bets: {int(df['is_graded_bet'].sum())}")
    print(f"Candidate rules: {len(calibration)}")
    print(f"Rolling validation splits: {rolling_metadata['splits_built']}")
    print(f"Train candidate rows before filters: {rolling_metadata['train_candidate_rows_built']}")
    print(f"Train candidate rows after train filters: {rolling_metadata['train_candidate_rows_after_filters']}")
    print(f"Rolling validation rows: {len(rolling)}")
    print(f"Promoted rules: {len(promoted)}")
    print(f"Best profit units: {calibration['profit_units'].iloc[0]:.2f}u" if not calibration.empty else "Best profit units: nan")
    print("\n=== ARCHIVOS GENERADOS ===")
    print(candidates_path)
    print(split_manifest_path)
    print(rolling_path)
    print(promoted_path)
    print(report_path)
    print("\n=== CALIBRATION COMPLETADA ===")


if __name__ == "__main__":
    main()
