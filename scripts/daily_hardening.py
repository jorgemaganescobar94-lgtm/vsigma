from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"
SCOREBOARD_PATH = ROOT / "notes" / "competition_scoreboard.md"

METADATA_COLUMNS = [
    "target_date",
    "generated_at",
    "pipeline_mode",
    "candidate_version",
    "source_file_date_check",
    "run_id",
]

DATE_COLUMNS = ["date", "match_date", "fixture_date"]
NO_BET_EMPTY_COLUMNS = [
    "date",
    "league",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "primary_odds_used",
]

PRE_LOCK_NOTE = (
    "PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never "
    "overwrites the frozen morning official baseline."
)


CSV_OUTPUT_SPECS: list[tuple[str, str, str, bool]] = [
    ("vsigma_today_competition_shortlist.csv", "PRE", "OFFICIAL_BASELINE", True),
    ("vsigma_today_competition_top.csv", "PRE", "OFFICIAL_BASELINE", True),
    ("vsigma_today_candidate_v2_competition_shortlist.csv", "PRE", "CANDIDATE_V2", True),
    ("vsigma_today_candidate_v2_competition_top.csv", "PRE", "CANDIDATE_V2", True),
    ("vsigma_today_candidate_v4_competition_shortlist.csv", "PRE", "CANDIDATE_V4", True),
    ("vsigma_today_candidate_v4_competition_top.csv", "PRE", "CANDIDATE_V4", True),
    ("vsigma_today_candidate_v5_competition_shortlist.csv", "PRE", "CANDIDATE_V5", True),
    ("vsigma_today_candidate_v5_competition_top.csv", "PRE", "CANDIDATE_V5", True),
    ("vsigma_today_candidate_v6_competition_shortlist.csv", "PRE", "CANDIDATE_V6", True),
    ("vsigma_today_candidate_v6_competition_top.csv", "PRE", "CANDIDATE_V6", True),
    ("vsigma_today_candidate_v7_competition_shortlist.csv", "PRE", "CANDIDATE_V7", True),
    ("vsigma_today_candidate_v7_competition_top.csv", "PRE", "CANDIDATE_V7", True),
    ("vsigma_today_baseline_vs_candidate_v2.csv", "PRE", "COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv", "PRE", "COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv", "PRE", "COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv", "PRE", "COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv", "PRE", "COMPARISON", False),
    ("vsigma_today_match_script_forecasts.csv", "PRE", "FORECAST", True),
    ("vsigma_today_candidate_v2_match_script_forecasts.csv", "PRE", "FORECAST_CANDIDATE_V2", True),
    ("vsigma_today_candidate_v4_match_script_forecasts.csv", "PRE", "FORECAST_CANDIDATE_V4", True),
    ("vsigma_today_prelock_competition_top.csv", "PRELOCK", "OFFICIAL_BASELINE_PRELOCK", True),
    ("vsigma_today_prelock_comparison.csv", "PRELOCK", "PRELOCK_COMPARISON", True),
    ("vsigma_execution_shortlist_results_ledger.csv", "POST", "OFFICIAL_RESULTS", True),
    ("vsigma_execution_shortlist_results_summary.csv", "POST", "OFFICIAL_RESULTS", True),
    ("vsigma_today_candidate_v2_results_ledger.csv", "POST", "CANDIDATE_V2_RESULTS", True),
    ("vsigma_today_candidate_v2_results_summary.csv", "POST", "CANDIDATE_V2_RESULTS", True),
    ("vsigma_today_candidate_v4_results_ledger.csv", "POST", "CANDIDATE_V4_RESULTS", True),
    ("vsigma_today_candidate_v4_results_summary.csv", "POST", "CANDIDATE_V4_RESULTS", True),
    ("vsigma_today_candidate_v5_results_ledger.csv", "POST", "CANDIDATE_V5_RESULTS", True),
    ("vsigma_today_candidate_v5_results_summary.csv", "POST", "CANDIDATE_V5_RESULTS", True),
    ("vsigma_today_candidate_v6_results_ledger.csv", "POST", "CANDIDATE_V6_RESULTS", True),
    ("vsigma_today_candidate_v6_results_summary.csv", "POST", "CANDIDATE_V6_RESULTS", True),
    ("vsigma_today_candidate_v7_results_ledger.csv", "POST", "CANDIDATE_V7_RESULTS", True),
    ("vsigma_today_candidate_v7_results_summary.csv", "POST", "CANDIDATE_V7_RESULTS", True),
    ("vsigma_today_baseline_vs_candidate_v2_results.csv", "POST", "RESULT_COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_results.csv", "POST", "RESULT_COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_results.csv", "POST", "RESULT_COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6_results.csv", "POST", "RESULT_COMPARISON", False),
    ("vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7_results.csv", "POST", "RESULT_COMPARISON", False),
]

BASELINE_FILES = {
    "vsigma_today_competition_shortlist.csv",
    "vsigma_today_competition_top.csv",
    "vsigma_today_competition_report.txt",
}

CANDIDATE_REQUIRED_FILES = [
    "vsigma_today_candidate_v2_competition_top.csv",
    "vsigma_today_candidate_v4_competition_top.csv",
    "vsigma_today_candidate_v5_competition_top.csv",
    "vsigma_today_candidate_v6_competition_top.csv",
    "vsigma_today_candidate_v7_competition_top.csv",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_run_id(target_date: str, when: str | None = None) -> str:
    stamp = when or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{target_date}-{stamp}"


def read_csv_lenient(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=columns or NO_BET_EMPTY_COLUMNS)
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=columns or NO_BET_EMPTY_COLUMNS)


def normalize_date(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()[:10]


def observed_dates(df: pd.DataFrame, include_target_date: bool = False) -> list[str]:
    columns = list(DATE_COLUMNS)
    if include_target_date:
        columns.append("target_date")
    dates: set[str] = set()
    for column in columns:
        if column not in df.columns:
            continue
        for value in df[column].dropna().tolist():
            parsed = normalize_date(value)
            if parsed:
                dates.add(parsed)
    return sorted(dates)


def target_date_mask(df: pd.DataFrame, target_date: str, include_target_date: bool = True) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=bool)
    columns = list(DATE_COLUMNS)
    if include_target_date:
        columns.insert(0, "target_date")
    mask = pd.Series(False, index=df.index)
    found_date_column = False
    for column in dict.fromkeys(columns):
        if column not in df.columns:
            continue
        found_date_column = True
        values = df[column].map(normalize_date)
        mask = mask | values.eq(target_date)
    if not found_date_column:
        return pd.Series(False, index=df.index)
    return mask


def split_fresh_stale_rows(df: pd.DataFrame, target_date: str, include_target_date: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty:
        return df.copy(), df.copy()
    mask = target_date_mask(df, target_date, include_target_date)
    return df[mask].copy(), df[~mask].copy()


def stale_date_summary(df: pd.DataFrame, include_target_date: bool = True) -> str:
    dates = observed_dates(df, include_target_date=include_target_date)
    return ", ".join(dates) if dates else "NO_DATE_METADATA"


def source_date_check(df: pd.DataFrame, target_date: str) -> str:
    if df.empty:
        return "EMPTY_OK_NO_BET"
    dates = observed_dates(df)
    if not dates:
        return "NO_DATE_COLUMN"
    if dates == [target_date]:
        return "PASS"
    return "DATE_MISMATCH"


def stamp_csv(
    path: Path,
    target_date: str,
    pipeline_mode: str,
    candidate_version: str,
    run_id: str,
    generated_at: str | None = None,
) -> Path:
    df = read_csv_lenient(path)
    check = source_date_check(df, target_date)
    generated = generated_at or utc_now_iso()
    df = df.assign(
        target_date=target_date,
        generated_at=generated,
        pipeline_mode=pipeline_mode,
        candidate_version=candidate_version,
        source_file_date_check=check,
        run_id=run_id,
    )
    if df.empty:
        df = df.reindex(columns=[*dict.fromkeys([*NO_BET_EMPTY_COLUMNS, *df.columns])])
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def stamp_daily_outputs(
    processed_dir: Path,
    target_date: str,
    run_id: str | None = None,
    generated_at: str | None = None,
    phase: str = "all",
) -> list[Path]:
    run_id = run_id or make_run_id(target_date)
    phase = phase.strip().upper()
    written: list[Path] = []
    for filename, pipeline_mode, candidate_version, _empty_ok in CSV_OUTPUT_SPECS:
        if phase != "ALL" and pipeline_mode.upper() != phase:
            continue
        path = processed_dir / filename
        if not path.exists():
            continue
        written.append(stamp_csv(path, target_date, pipeline_mode, candidate_version, run_id, generated_at))
    return written


def copy_paths_to_snapshot(paths: Iterable[Path], snapshot_dir: Path) -> None:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if path.exists():
            shutil.copy2(path, snapshot_dir / path.name)


def file_rows(path: Path) -> int | None:
    if not path.exists():
        return None
    return int(len(read_csv_lenient(path)))


def format_markdown_table(df: pd.DataFrame, columns: list[str] | None = None, max_rows: int = 20) -> str:
    if df.empty:
        return "_No rows._"
    view = df.copy()
    if columns is not None:
        view = view[[column for column in columns if column in view.columns]]
    if view.empty:
        return "_No display columns available._"
    view = view.head(max_rows).fillna("")
    headers = [str(column) for column in view.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in view.iterrows():
        values = [str(row[column]).replace("\n", " ").replace("|", "/") for column in view.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def summary_value(df: pd.DataFrame, column: str, default: object = 0) -> object:
    if df.empty or column not in df.columns:
        return default
    value = df.iloc[0][column]
    if pd.isna(value):
        return default
    return value


def parse_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def strip_scoreboard_section(text: str, target_date: str) -> str:
    pattern = re.compile(
        rf"\n?<!-- VSIGMA_SCOREBOARD_START {re.escape(target_date)} -->.*?"
        rf"<!-- VSIGMA_SCOREBOARD_END {re.escape(target_date)} -->\n?",
        re.DOTALL,
    )
    return pattern.sub("\n", text).strip()
