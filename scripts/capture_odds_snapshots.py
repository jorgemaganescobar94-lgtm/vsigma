from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"
ODDS_SNAPSHOT_DIR = PROCESSED_DIR / "odds_snapshots"
SNAPSHOT_CSV = ODDS_SNAPSHOT_DIR / "vsigma_odds_snapshots.csv"
SNAPSHOT_JSONL = ODDS_SNAPSHOT_DIR / "vsigma_odds_snapshots.jsonl"

SNAPSHOT_COLUMNS = [
    "snapshot_id",
    "target_date",
    "generated_at",
    "pipeline_stage",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "market_alt",
    "experiment_id",
    "source_candidate_version",
    "odds_market_name",
    "bookmaker_count",
    "odds_available_flag",
    "selected_price",
    "median_price",
    "best_price",
    "implied_probability",
    "odds_dispersion_score",
    "source_file",
    "source_file_hash",
    "snapshot_rebuild_mode",
    "true_pre_snapshot_available_flag",
    "clv_usable_for_threshold_calibration_flag",
    "source_snapshot_stage",
    "source_snapshot_note",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_float(value: object, default: float | None = None) -> float | None:
    try:
        if pd.isna(value) or norm_text(value) == "":
            return default
        return float(value)
    except Exception:
        return default


def normalize_date_value(value: object) -> str:
    if pd.isna(value):
        return ""
    text = norm_text(value)
    if not text:
        return ""
    try:
        return pd.Timestamp(text).date().isoformat()
    except Exception:
        return text[:10]


def source_row_date(row: pd.Series) -> str:
    for column in ["target_date", "date", "fixture_date", "match_date", "historical_batch_date"]:
        if column in row.index:
            observed = normalize_date_value(row.get(column))
            if observed:
                return observed
    fixture_dt = normalize_date_value(row.get("fixture_datetime_utc")) if "fixture_datetime_utc" in row.index else ""
    return fixture_dt


def file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_hash(parts: list[object], length: int = 32) -> str:
    text = "|".join(norm_text(part) for part in parts)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def selected_price(row: pd.Series) -> float | None:
    return safe_float(row.get("primary_odds_used"), safe_float(row.get("selected_price"), None))


def implied_probability(row: pd.Series, price: float | None) -> float | None:
    implied = safe_float(row.get("primary_implied_prob"), safe_float(row.get("implied_probability"), None))
    if implied is not None:
        return implied
    if price is not None and price > 1.0:
        return round(1.0 / price, 6)
    return None


def market_alt(row: pd.Series) -> object:
    return row.get("market_alt", "")


def pass_all(df: pd.DataFrame) -> pd.DataFrame:
    return df


def bet_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "final_recommendation" not in df.columns:
        return df.iloc[0:0].copy()
    return df[df["final_recommendation"].astype(str).str.upper().eq("BET")].copy()


def watch_high_edge_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    recommendation = df.get("final_recommendation", pd.Series("", index=df.index)).astype(str).str.upper()
    edge = pd.to_numeric(df.get("primary_edge", pd.Series(dtype=object)), errors="coerce")
    return df[recommendation.isin(["WATCH", "LEAN_PLAY"]) & edge.ge(0.12)].copy()


def stage_sources(stage: str) -> list[dict[str, Any]]:
    stage = stage.upper()
    common = [
        {
            "filename": "vsigma_today_competition_top.csv",
            "experiment_id": "OFFICIAL_BASELINE",
            "source_candidate_version": "OFFICIAL_BASELINE",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_today_candidate_v2_competition_top.csv",
            "experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY",
            "source_candidate_version": "CANDIDATE_V2",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_today_candidate_v7_competition_top.csv",
            "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
            "source_candidate_version": "CANDIDATE_V7",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_today_execution_shortlist.csv",
            "experiment_id": "OFFICIAL_BASELINE",
            "source_candidate_version": "EXECUTION_SHORTLIST",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_deep_analysis_candidates.csv",
            "experiment_id": "DEEP_ANALYSIS_CANDIDATES",
            "source_candidate_version": "DEEP_ANALYSIS_BET",
            "filter": bet_rows,
        },
        {
            "filename": "vsigma_final_watch_candidates.csv",
            "experiment_id": "WATCH_HIGH_EDGE",
            "source_candidate_version": "WATCH_HIGH_EDGE",
            "filter": watch_high_edge_rows,
        },
    ]
    prelock = [
        {
            "filename": "vsigma_today_prelock_comparison.csv",
            "experiment_id": "OFFICIAL_BASELINE",
            "source_candidate_version": "OFFICIAL_BASELINE_PRELOCK",
            "filter": pass_all,
        }
    ]
    post = [
        {
            "filename": "vsigma_execution_shortlist_results_ledger.csv",
            "experiment_id": "OFFICIAL_BASELINE",
            "source_candidate_version": "OFFICIAL_RESULTS",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_today_candidate_v2_results_ledger.csv",
            "experiment_id": "CANDIDATE_V2_SCHEDULE_ANOMALY",
            "source_candidate_version": "CANDIDATE_V2_RESULTS",
            "filter": pass_all,
        },
        {
            "filename": "vsigma_today_candidate_v7_results_ledger.csv",
            "experiment_id": "CANDIDATE_V7_PRICE_DISCIPLINE",
            "source_candidate_version": "CANDIDATE_V7_RESULTS",
            "filter": pass_all,
        },
    ]
    if stage == "PRELOCK":
        return prelock
    if stage in {"POST", "CLOSE_PROXY"}:
        return post if stage == "POST" else prelock
    return common


def row_to_snapshot(row: pd.Series, source: dict[str, Any], source_path: Path, target_date: str, generated_at: str, stage: str) -> dict[str, object]:
    price = selected_price(row)
    implied = implied_probability(row, price)
    source_hash = file_hash(source_path)
    experiment_id = source["experiment_id"]
    source_version = source["source_candidate_version"]
    fixture_id = row.get("fixture_id", "")
    market = norm_upper(row.get("market_primary"))
    snapshot_id = stable_hash([target_date, stage, experiment_id, source_version, fixture_id, market, source_path.name, source_hash])
    return {
        "snapshot_id": snapshot_id,
        "target_date": target_date,
        "generated_at": generated_at,
        "pipeline_stage": stage,
        "fixture_id": norm_text(fixture_id),
        "league": row.get("league", ""),
        "home_team": row.get("home_team", ""),
        "away_team": row.get("away_team", ""),
        "market_primary": market,
        "market_alt": market_alt(row),
        "experiment_id": experiment_id,
        "source_candidate_version": source_version,
        "odds_market_name": market,
        "bookmaker_count": row.get("odds_bookmaker_support_count", row.get("odds_market_support_count", "")),
        "odds_available_flag": 1 if price is not None and price > 1.0 else 0,
        "selected_price": price if price is not None else pd.NA,
        "median_price": price if price is not None else pd.NA,
        "best_price": row.get("best_price", price if price is not None else pd.NA),
        "implied_probability": implied if implied is not None else pd.NA,
        "odds_dispersion_score": row.get("odds_dispersion_score", ""),
        "source_file": source_path.name,
        "source_file_hash": source_hash,
        "snapshot_rebuild_mode": "CANONICAL_CAPTURED",
        "true_pre_snapshot_available_flag": 1 if stage.upper() == "PRE" else 0,
        "clv_usable_for_threshold_calibration_flag": 1,
        "source_snapshot_stage": stage.upper(),
        "source_snapshot_note": "Captured by odds snapshot pipeline.",
    }


def build_snapshot_rows(processed_dir: Path, target_date: str, stage: str, generated_at: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    mismatches: list[str] = []
    for source in stage_sources(stage):
        path = processed_dir / source["filename"]
        df = read_csv_optional(path)
        if df.empty:
            continue
        filter_func: Callable[[pd.DataFrame], pd.DataFrame] = source["filter"]
        filtered = filter_func(df)
        if filtered.empty:
            continue
        for _, row in filtered.iterrows():
            observed_date = source_row_date(row)
            if observed_date and observed_date != target_date:
                mismatches.append(f"{path.name}:{norm_text(row.get('fixture_id'))}:{observed_date}")
                continue
            if stage.upper() == "PRELOCK":
                if norm_upper(row.get("prelock_status")) != "IN_PRELOCK_WINDOW":
                    continue
                price = selected_price(row)
                if price is None or price <= 1.0:
                    continue
            if norm_text(row.get("fixture_id")) and norm_upper(row.get("market_primary")):
                rows.append(row_to_snapshot(row, source, path, target_date, generated_at, stage.upper()))
    if mismatches:
        preview = ", ".join(mismatches[:10])
        suffix = "" if len(mismatches) <= 10 else f", ... (+{len(mismatches) - 10} more)"
        print(
            f"WARNING CLV_DATE_MISMATCH: excluded {len(mismatches)} {stage.upper()} snapshot source rows "
            f"whose source date did not match requested target_date={target_date}: {preview}{suffix}",
            flush=True,
        )
    return pd.DataFrame(rows, columns=SNAPSHOT_COLUMNS)


def read_existing_snapshots(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    try:
        df = pd.read_csv(path, dtype=str)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    for column in SNAPSHOT_COLUMNS:
        if column not in df.columns:
            df[column] = ""
    return df[SNAPSHOT_COLUMNS].copy()


def append_jsonl(new_rows: pd.DataFrame, path: Path) -> None:
    if new_rows.empty:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for record in new_rows[SNAPSHOT_COLUMNS].fillna("").to_dict(orient="records"):
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def capture_odds_snapshots(
    processed_dir: Path = PROCESSED_DIR,
    odds_dir: Path = ODDS_SNAPSHOT_DIR,
    target_date: str | None = None,
    stage: str = "PRE",
) -> dict[str, Path]:
    target_date = target_date or date.today().isoformat()
    stage = stage.strip().upper()
    if stage not in {"PRE", "PRELOCK", "CLOSE_PROXY", "POST"}:
        raise ValueError(f"Unsupported pipeline stage: {stage}")
    odds_dir.mkdir(parents=True, exist_ok=True)
    csv_path = odds_dir / SNAPSHOT_CSV.name
    jsonl_path = odds_dir / SNAPSHOT_JSONL.name
    generated_at = utc_now_iso()
    new_rows = build_snapshot_rows(processed_dir, target_date, stage, generated_at)
    existing = read_existing_snapshots(csv_path)
    existing_ids = set(existing.get("snapshot_id", pd.Series(dtype=object)).astype(str).tolist())
    rows_for_jsonl = new_rows[~new_rows.get("snapshot_id", pd.Series(dtype=object)).astype(str).isin(existing_ids)].copy() if not new_rows.empty else new_rows
    combined = pd.concat([existing, new_rows], ignore_index=True) if not new_rows.empty else existing
    if not combined.empty:
        combined = combined.drop_duplicates("snapshot_id", keep="last")
    for column in SNAPSHOT_COLUMNS:
        if column not in combined.columns:
            combined[column] = ""
    combined[SNAPSHOT_COLUMNS].to_csv(csv_path, index=False)
    append_jsonl(rows_for_jsonl, jsonl_path)
    snapshot_dir = TODAY_DIR / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    for path in [csv_path, jsonl_path]:
        if path.exists():
            target = snapshot_dir / "odds_snapshots"
            target.mkdir(parents=True, exist_ok=True)
            target_file = target / path.name
            if path.is_file():
                target_file.write_bytes(path.read_bytes())
    return {"snapshots_csv": csv_path, "snapshots_jsonl": jsonl_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture append-safe vSIGMA odds snapshots from existing processed outputs.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--stage", choices=["PRE", "PRELOCK", "CLOSE_PROXY", "POST"], default="PRE")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--odds-dir", type=Path, default=ODDS_SNAPSHOT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    paths = capture_odds_snapshots(args.processed_dir, args.odds_dir, target_date, args.stage)
    print("\n=== ODDS SNAPSHOTS CAPTURED ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
