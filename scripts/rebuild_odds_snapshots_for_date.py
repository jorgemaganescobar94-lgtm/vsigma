from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

try:
    from capture_odds_snapshots import (
        ODDS_SNAPSHOT_DIR,
        PROCESSED_DIR,
        SNAPSHOT_COLUMNS,
        SNAPSHOT_CSV,
        TODAY_DIR,
        build_snapshot_rows,
        norm_text,
        norm_upper,
        read_existing_snapshots,
        stable_hash,
        utc_now_iso,
    )
except ModuleNotFoundError:
    from scripts.capture_odds_snapshots import (
        ODDS_SNAPSHOT_DIR,
        PROCESSED_DIR,
        SNAPSHOT_COLUMNS,
        SNAPSHOT_CSV,
        TODAY_DIR,
        build_snapshot_rows,
        norm_text,
        norm_upper,
        read_existing_snapshots,
        stable_hash,
        utc_now_iso,
    )


ARCHIVE_DIRNAME = "archive"
REBUILD_MODE_CAPTURED = "CANONICAL_CAPTURED"
REBUILD_MODE_BACKFILLED = "BACKFILLED_FROM_AVAILABLE_OUTPUTS"
AUDIT_ONLY_NOTE = "CLV_BACKFILLED_AUDIT_ONLY"
TRUE_PRE_MISSING_NOTE = "CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING"
ALLOWED_STAGES = {"PRE", "PRELOCK", "CLOSE_PROXY", "POST"}


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


def snapshot_key(row: pd.Series) -> tuple[str, str, str]:
    return (
        norm_text(row.get("fixture_id")),
        norm_upper(row.get("market_primary")),
        norm_text(row.get("experiment_id")),
    )


def stage_key(row: pd.Series) -> tuple[str, str, str, str, str, str]:
    return (
        norm_text(row.get("fixture_id")),
        norm_upper(row.get("market_primary")),
        norm_text(row.get("experiment_id")),
        norm_upper(row.get("pipeline_stage")),
        norm_text(row.get("source_candidate_version")),
        norm_text(row.get("source_file")),
    )


def ensure_snapshot_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for column in SNAPSHOT_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    return out[SNAPSHOT_COLUMNS].copy()


def date_scoped_rows(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    if df.empty or "target_date" not in df.columns:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    scoped = df[df["target_date"].map(normalize_date_value).eq(target_date)].copy()
    if scoped.empty:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    return ensure_snapshot_columns(scoped)


def read_per_day_captured_snapshots(today_dir: Path, target_date: str) -> pd.DataFrame:
    path = today_dir / target_date / "odds_snapshots" / SNAPSHOT_CSV.name
    if not path.exists():
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    return date_scoped_rows(read_existing_snapshots(path), target_date)


def captured_true_pre_keys(captured: pd.DataFrame) -> set[tuple[str, str, str]]:
    if captured.empty:
        return set()
    stages = captured["pipeline_stage"].astype(str).str.upper()
    pre = captured[stages.eq("PRE")].copy()
    return {snapshot_key(row) for _, row in pre.iterrows()}


def with_provenance(
    rows: pd.DataFrame,
    rebuild_mode: str,
    true_pre_keys: set[tuple[str, str, str]],
    note: str,
    generated_at: str,
) -> pd.DataFrame:
    if rows.empty:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    out = ensure_snapshot_columns(rows)
    out = out[out["pipeline_stage"].astype(str).str.upper().isin(ALLOWED_STAGES)].copy()
    if out.empty:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    out["pipeline_stage"] = out["pipeline_stage"].astype(str).str.upper()
    out["source_snapshot_stage"] = out["pipeline_stage"]
    out["snapshot_rebuild_mode"] = rebuild_mode
    out["source_snapshot_note"] = note
    if rebuild_mode == REBUILD_MODE_BACKFILLED:
        out["generated_at"] = generated_at
    true_flags = []
    usable_flags = []
    for _, row in out.iterrows():
        key = snapshot_key(row)
        has_true_pre = key in true_pre_keys
        true_flags.append(1 if has_true_pre else 0)
        usable_flags.append(1 if rebuild_mode == REBUILD_MODE_CAPTURED and has_true_pre else 0)
    out["true_pre_snapshot_available_flag"] = true_flags
    out["clv_usable_for_threshold_calibration_flag"] = usable_flags
    return out[SNAPSHOT_COLUMNS].copy()


def build_backfilled_rows(day_source_dir: Path, target_date: str, generated_at: str) -> pd.DataFrame:
    if not day_source_dir.exists():
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    frames = [
        build_snapshot_rows(day_source_dir, target_date, "PRELOCK", generated_at),
        build_snapshot_rows(day_source_dir, target_date, "CLOSE_PROXY", generated_at),
        build_snapshot_rows(day_source_dir, target_date, "POST", generated_at),
    ]
    frames = [frame for frame in frames if not frame.empty]
    if not frames:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    return ensure_snapshot_columns(pd.concat(frames, ignore_index=True))


def dedupe_rebuilt_rows(captured: pd.DataFrame, backfilled: pd.DataFrame) -> pd.DataFrame:
    if captured.empty and backfilled.empty:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    captured_stage_keys = {stage_key(row) for _, row in captured.iterrows()} if not captured.empty else set()
    if not backfilled.empty:
        keep = [stage_key(row) not in captured_stage_keys for _, row in backfilled.iterrows()]
        backfilled = backfilled.loc[keep].copy()
    combined = pd.concat([captured, backfilled], ignore_index=True)
    if combined.empty:
        return pd.DataFrame(columns=SNAPSHOT_COLUMNS)
    combined = combined.drop_duplicates("snapshot_id", keep="first")
    return ensure_snapshot_columns(combined)


def archive_path_for(odds_dir: Path, target_date: str, generated_at: str) -> Path:
    stamp = generated_at.replace(":", "").replace("-", "").replace("+", "Z")
    stamp = stamp.replace("T", "_")
    return odds_dir / ARCHIVE_DIRNAME / f"vsigma_odds_snapshots_{target_date}_{stamp}.csv"


def rebuild_odds_snapshots_for_date(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    mode: str = "archive-and-rebuild",
    dry_run: bool = False,
    processed_dir: Path = PROCESSED_DIR,
    odds_dir: Path = ODDS_SNAPSHOT_DIR,
    today_dir: Path = TODAY_DIR,
    generated_at: str | None = None,
) -> dict[str, object]:
    if mode != "archive-and-rebuild":
        raise ValueError(f"Unsupported rebuild mode: {mode}")
    target_date = pd.Timestamp(target_date).date().isoformat()
    generated_at = generated_at or utc_now_iso()
    csv_path = odds_dir / SNAPSHOT_CSV.name
    existing = read_existing_snapshots(csv_path)
    target_existing = date_scoped_rows(existing, target_date)
    non_target = existing[~existing.get("target_date", pd.Series(dtype=object)).map(normalize_date_value).eq(target_date)].copy()
    non_target = ensure_snapshot_columns(non_target)

    per_day_captured = read_per_day_captured_snapshots(today_dir, target_date)
    captured_source = per_day_captured if len(per_day_captured) > len(target_existing) else target_existing
    true_pre_keys = captured_true_pre_keys(captured_source)
    captured = with_provenance(
        captured_source,
        REBUILD_MODE_CAPTURED,
        true_pre_keys,
        "Canonical captured snapshot preserved during date-scoped rebuild.",
        generated_at,
    )
    day_source_dir = today_dir / target_date if (today_dir / target_date).exists() else processed_dir
    backfilled_raw = build_backfilled_rows(day_source_dir, target_date, generated_at)
    backfill_note = AUDIT_ONLY_NOTE if true_pre_keys else TRUE_PRE_MISSING_NOTE
    backfilled = with_provenance(backfilled_raw, REBUILD_MODE_BACKFILLED, true_pre_keys, backfill_note, generated_at)
    rebuilt = dedupe_rebuilt_rows(captured, backfilled)
    combined = ensure_snapshot_columns(pd.concat([non_target, rebuilt], ignore_index=True))
    archive_path = archive_path_for(odds_dir, target_date, generated_at)

    result = {
        "target_date": target_date,
        "timezone": timezone_name,
        "mode": mode,
        "dry_run": dry_run,
        "snapshots_csv": csv_path,
        "archive_path": archive_path,
        "existing_target_rows": int(len(target_existing)),
        "preserved_non_target_rows": int(len(non_target)),
        "rebuilt_target_rows": int(len(rebuilt)),
        "true_pre_count": int((rebuilt["pipeline_stage"].astype(str).str.upper().eq("PRE") & rebuilt["true_pre_snapshot_available_flag"].astype(str).eq("1")).sum()) if not rebuilt.empty else 0,
        "audit_only_count": int(rebuilt["clv_usable_for_threshold_calibration_flag"].astype(str).ne("1").sum()) if not rebuilt.empty else 0,
        "calibration_usable_count": int(rebuilt["clv_usable_for_threshold_calibration_flag"].astype(str).eq("1").sum()) if not rebuilt.empty else 0,
        "backfilled_rows": int(rebuilt["snapshot_rebuild_mode"].astype(str).eq(REBUILD_MODE_BACKFILLED).sum()) if not rebuilt.empty else 0,
    }
    if dry_run:
        return result

    odds_dir.mkdir(parents=True, exist_ok=True)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    target_existing.to_csv(archive_path, index=False)
    combined.to_csv(csv_path, index=False)
    snapshot_dir = today_dir / target_date / "odds_snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    (snapshot_dir / SNAPSHOT_CSV.name).write_bytes(csv_path.read_bytes())
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive and rebuild canonical odds snapshots for one target date.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--mode", choices=["archive-and-rebuild"], default="archive-and-rebuild")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--odds-dir", type=Path, default=ODDS_SNAPSHOT_DIR)
    parser.add_argument("--today-dir", type=Path, default=TODAY_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = rebuild_odds_snapshots_for_date(
        target_date=args.date,
        timezone_name=args.timezone,
        mode=args.mode,
        dry_run=args.dry_run,
        processed_dir=args.processed_dir,
        odds_dir=args.odds_dir,
        today_dir=args.today_dir,
    )
    print("\n=== ODDS SNAPSHOTS DATE REBUILD ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
