from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, TODAY_DIR, make_run_id, split_fresh_stale_rows, stale_date_summary, stamp_csv, utc_now_iso
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, TODAY_DIR, make_run_id, split_fresh_stale_rows, stale_date_summary, stamp_csv, utc_now_iso


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"

MORNING_TOP = "vsigma_today_competition_top.csv"
PRELOCK_TOP = "vsigma_today_prelock_competition_top.csv"
PRELOCK_COMPARISON = "vsigma_today_prelock_comparison.csv"
PRELOCK_REPORT = "vsigma_today_prelock_report.txt"
IMMUTABLE_LEDGER_STEP = "scripts/update_immutable_daily_ledger.py"
EXPERIMENT_PERFORMANCE_STEP = "scripts/build_experiment_performance_report.py"
MASTER_REPORT_STEP = "scripts/build_daily_competition_master_report.py"
SCOREBOARD_STEP = "scripts/update_competition_scoreboard.py"
GOVERNANCE_STEP = "scripts/build_promotion_threshold_governance.py"
ODDS_SNAPSHOT_STEP = "scripts/capture_odds_snapshots.py"
CLV_REPORT_STEP = "scripts/build_clv_calibration_report.py"
V7_CALIBRATION_ADVISOR_STEP = "scripts/build_candidate_v7_calibration_advisor.py"

REFRESH_STEPS = [
    "scripts/enrich_injuries_availability.py",
    "scripts/enrich_fixture_lineups.py",
    "scripts/enrich_odds_context_v3.py",
    "scripts/enrich_odds_structure_depth.py",
]

PRELOCK_COLUMNS = [
    "date",
    "league",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "prelock_status",
    "prelock_minutes_to_kickoff",
    "prelock_lineup_state",
    "prelock_odds_state",
    "prelock_availability_state",
    "prelock_decision",
    "prelock_decision_reason",
]


def read_csv_optional(path: Path, columns: list[str] | None = None) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=columns or [])
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=columns or [])


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def numeric(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def run_optional_step(script_path: str) -> bool:
    command = [sys.executable, script_path]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    return completed.returncode == 0


def run_optional_step_with_args(script_path: str, extra_args: list[str]) -> bool:
    command = [sys.executable, script_path, *extra_args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    if completed.returncode != 0:
        print(f"WARNING: optional step failed ({script_path}) with exit code {completed.returncode}", flush=True)
        return False
    return True


def refresh_prelock_layers(enabled: bool = True) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    if not enabled:
        return [{"step": "REFRESH_SKIPPED", "status": "SKIPPED"}]
    for step in REFRESH_STEPS:
        ok = run_optional_step(step)
        rows.append({"step": step, "status": "PASS" if ok else "WARNING_REFRESH_FAILED"})
    return rows


def attach_raw_timing(picks: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
    if picks.empty or raw.empty or "fixture_id" not in picks.columns or "fixture_id" not in raw.columns:
        return picks.copy()
    timing_cols = [c for c in ["fixture_id", "fixture_datetime_utc", "fixture_timestamp", "status", "fixture_status_short"] if c in raw.columns]
    if len(timing_cols) <= 1:
        return picks.copy()
    out = picks.drop(columns=[c for c in timing_cols if c != "fixture_id" and c in picks.columns], errors="ignore")
    return out.merge(raw[timing_cols].drop_duplicates("fixture_id"), on="fixture_id", how="left")


def minutes_to_kickoff(row: pd.Series, now_utc: datetime | None = None) -> float | None:
    for column in ["prelock_minutes_to_kickoff", "lineup_minutes_to_kickoff"]:
        if column in row.index and pd.notna(row.get(column)):
            return numeric(row.get(column), default=float("nan"))
    now_utc = now_utc or datetime.now(timezone.utc)
    if "fixture_datetime_utc" in row.index and norm_text(row.get("fixture_datetime_utc")):
        try:
            kickoff = pd.Timestamp(row.get("fixture_datetime_utc")).to_pydatetime()
            if kickoff.tzinfo is None:
                kickoff = kickoff.replace(tzinfo=timezone.utc)
            return round((kickoff.astimezone(timezone.utc) - now_utc).total_seconds() / 60.0, 2)
        except (TypeError, ValueError):
            return None
    return None


def lineup_state(row: pd.Series) -> str:
    home_starters = numeric(row.get("home_lineup_known_starters_count"), 0)
    away_starters = numeric(row.get("away_lineup_known_starters_count"), 0)
    quality = norm_upper(row.get("lineup_quality_flag"))
    activation = norm_upper(row.get("lineup_activation_state"))
    if home_starters >= 10 and away_starters >= 10:
        return "LINEUPS_CONFIRMED"
    if quality in {"FULL", "CONFIRMED"}:
        return "LINEUPS_CONFIRMED"
    if home_starters or away_starters:
        return "LINEUPS_PARTIAL"
    if activation == "INACTIVE":
        return "LINEUPS_NOT_AVAILABLE"
    return "LINEUPS_UNKNOWN"


def odds_state(row: pd.Series) -> str:
    support = numeric(row.get("odds_market_support_count"), 0)
    coherence = norm_upper(row.get("odds_structure_coherence_flag"))
    depth = norm_upper(row.get("odds_structure_depth_status"))
    if support >= 3 or coherence in {"COHERENT", "STRONG"} or depth in {"FULL", "RICH"}:
        return "ODDS_CONFIRMED"
    if support > 0 or depth:
        return "ODDS_PARTIAL"
    return "ODDS_NOT_AVAILABLE"


def availability_state(row: pd.Series) -> str:
    quality = norm_upper(row.get("injuries_quality_flag"))
    risk = numeric(row.get("availability_known_risk_score"), 0)
    attack_penalty = numeric(row.get("availability_attack_penalty"), 0)
    if quality in {"", "NONE"} and risk == 0 and attack_penalty == 0:
        return "AVAILABILITY_NOT_AVAILABLE"
    if attack_penalty >= 2.0:
        return "AVAILABILITY_CONTRADICTION"
    if risk >= 12.0:
        return "AVAILABILITY_RISK_ELEVATED"
    if quality in {"FULL", "SUPPORTED"}:
        return "AVAILABILITY_CONFIRMED"
    return "AVAILABILITY_PARTIAL"


def explicit_contradictions(row: pd.Series) -> list[str]:
    reasons: list[str] = []
    market = norm_upper(row.get("market_primary"))
    odds_hint = norm_upper(row.get("odds_market_translation_hint"))
    goal_band = norm_upper(row.get("odds_goal_expectation_band"))
    over15 = norm_upper(row.get("odds_over15_support_flag"))
    over25 = norm_upper(row.get("odds_over25_support_flag"))
    btts = norm_upper(row.get("odds_btts_support_flag"))
    line_aggression = norm_upper(row.get("odds_line_aggression_flag"))
    attack_penalty = numeric(row.get("availability_attack_penalty"), 0)
    known_risk = numeric(row.get("availability_known_risk_score"), 0)

    if market in {"OVER_1_5", "OVER_2_5"}:
        if "UNDER" in odds_hint or goal_band in {"LOW", "LOW_GOALS"} or line_aggression in {"UNDER", "LOW"}:
            reasons.append("odds lean low scoring against goals thesis")
        if market == "OVER_2_5" and over25 in {"NO", "WEAK", "UNSUPPORTED"}:
            reasons.append("over 2.5 support weakened")
        if market == "OVER_1_5" and over15 in {"NO", "WEAK", "UNSUPPORTED"}:
            reasons.append("over 1.5 support weakened")
        if attack_penalty >= 2.0:
            reasons.append("availability weakens attacking path")
    if market == "BTTS_YES":
        if btts in {"NO", "WEAK", "UNSUPPORTED"} or "BTTS_NO" in odds_hint:
            reasons.append("BTTS support weakened")
        if attack_penalty >= 2.0:
            reasons.append("attacking availability risk weakens BTTS")
    if market in {"HOME_WIN", "AWAY_WIN"} and known_risk >= 12.0:
        reasons.append("side-market availability risk elevated")
    return reasons


def support_reasons(row: pd.Series) -> list[str]:
    reasons: list[str] = []
    if lineup_state(row) == "LINEUPS_CONFIRMED":
        reasons.append("lineups confirmed")
    if odds_state(row) == "ODDS_CONFIRMED":
        reasons.append("odds support available")
    if availability_state(row) == "AVAILABILITY_CONFIRMED":
        reasons.append("availability coverage confirmed")
    return reasons


def classify_prelock_decision(row: pd.Series, window_minutes: int, now_utc: datetime | None = None) -> dict[str, object]:
    minutes = minutes_to_kickoff(row, now_utc)
    in_window = minutes is not None and 0 <= minutes <= window_minutes
    l_state = lineup_state(row)
    o_state = odds_state(row)
    a_state = availability_state(row)
    if not in_window:
        return {
            "prelock_status": "OUTSIDE_PRELOCK_WINDOW",
            "prelock_minutes_to_kickoff": minutes if minutes is not None else pd.NA,
            "prelock_lineup_state": l_state,
            "prelock_odds_state": o_state,
            "prelock_availability_state": a_state,
            "prelock_decision": "PRELOCK_NOT_AVAILABLE",
            "prelock_decision_reason": "fixture is outside requested pre-lock window",
        }

    contradictions = explicit_contradictions(row)
    supports = support_reasons(row)
    if len(contradictions) >= 2:
        decision = "PRELOCK_REMOVED"
        reason = "; ".join(contradictions)
    elif len(contradictions) == 1:
        decision = "PRELOCK_DOWNGRADED"
        reason = contradictions[0]
    elif supports:
        decision = "PRELOCK_CONFIRMED"
        reason = "; ".join(supports)
    elif l_state in {"LINEUPS_NOT_AVAILABLE", "LINEUPS_UNKNOWN"} and o_state == "ODDS_NOT_AVAILABLE" and a_state == "AVAILABILITY_NOT_AVAILABLE":
        decision = "PRELOCK_NOT_AVAILABLE"
        reason = "no reliable pre-lock data available; missing data is neutral"
    else:
        decision = "PRELOCK_NO_CHANGE"
        reason = "no explicit pre-lock contradiction detected"
    return {
        "prelock_status": "IN_PRELOCK_WINDOW",
        "prelock_minutes_to_kickoff": round(minutes, 2) if minutes is not None else pd.NA,
        "prelock_lineup_state": l_state,
        "prelock_odds_state": o_state,
        "prelock_availability_state": a_state,
        "prelock_decision": decision,
        "prelock_decision_reason": reason,
    }


def build_prelock_outputs(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    target_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    window_minutes: int = 90,
    refresh: bool = True,
    now_utc: datetime | None = None,
) -> dict[str, Path]:
    target_date = target_date or date.today().isoformat()
    snapshot_dir = today_dir / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    refresh_rows = refresh_prelock_layers(refresh)

    raw_morning = read_csv_optional(processed_dir / MORNING_TOP, PRELOCK_COLUMNS)
    morning, stale_morning = split_fresh_stale_rows(raw_morning, target_date, include_target_date=True)
    raw = read_csv_optional(RAW_MATCHES_CSV)
    source = attach_raw_timing(morning, raw)
    rows: list[dict[str, object]] = []
    for _, row in source.iterrows():
        out = row.to_dict()
        out.update(classify_prelock_decision(row, window_minutes, now_utc))
        rows.append(out)
    comparison = pd.DataFrame(rows)
    if comparison.empty:
        comparison = pd.DataFrame(columns=[*PRELOCK_COLUMNS, "target_date", "generated_at", "pipeline_mode", "candidate_version", "source_file_date_check", "run_id"])
    prelock_top = comparison[
        comparison.get("prelock_status", pd.Series(dtype=object)).astype(str).eq("IN_PRELOCK_WINDOW")
        & ~comparison.get("prelock_decision", pd.Series(dtype=object)).astype(str).eq("PRELOCK_REMOVED")
    ].copy() if not comparison.empty else pd.DataFrame(columns=comparison.columns)

    comparison_path = processed_dir / PRELOCK_COMPARISON
    top_path = processed_dir / PRELOCK_TOP
    report_path = processed_dir / PRELOCK_REPORT
    comparison.to_csv(comparison_path, index=False)
    prelock_top.to_csv(top_path, index=False)
    run_id = make_run_id(target_date)
    stamp_csv(comparison_path, target_date, "PRELOCK", "PRELOCK_COMPARISON", run_id)
    stamp_csv(top_path, target_date, "PRELOCK", "OFFICIAL_BASELINE_PRELOCK", run_id)

    counts = comparison["prelock_decision"].value_counts().to_dict() if "prelock_decision" in comparison.columns else {}
    lines = [
        "# vSIGMA Pre-Lock Report",
        "",
        f"- Target date: {target_date}",
        f"- Timezone: {timezone_name}",
        f"- Window minutes: {window_minutes}",
        f"- Morning official picks reviewed: {len(morning)}",
        f"- Stale morning rows excluded: {len(stale_morning)}",
        f"- Stale morning row dates: {stale_date_summary(stale_morning, include_target_date=True) if not stale_morning.empty else 'none'}",
        f"- In-window pre-lock picks retained: {len(prelock_top)}",
        f"- Generated at: {utc_now_iso()}",
        "",
        "## Refresh Steps",
        pd.DataFrame(refresh_rows).to_string(index=False),
        "",
        "## Decisions",
        pd.DataFrame([counts]).to_string(index=False) if counts else "No morning picks available.",
        "",
        "Missing pre-lock data is treated as uncertainty, not weakness. No official morning file is overwritten.",
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    for path in [comparison_path, top_path, report_path]:
        if path.exists():
            shutil.copy2(path, snapshot_dir / path.name)
    return {"prelock_top": top_path, "prelock_comparison": comparison_path, "prelock_report": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run vSIGMA pre-lock execution review without overwriting morning picks.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--skip-refresh", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    paths = build_prelock_outputs(
        PROCESSED_DIR,
        TODAY_DIR,
        target_date,
        args.timezone,
        args.window_minutes,
        refresh=not args.skip_refresh,
    )
    snapshot_dir = TODAY_DIR / target_date
    run_optional_step_with_args(ODDS_SNAPSHOT_STEP, ["--date", target_date, "--stage", "PRELOCK"])
    run_optional_step_with_args(CLV_REPORT_STEP, ["--date", target_date])
    run_optional_step_with_args(V7_CALIBRATION_ADVISOR_STEP, ["--date", target_date])
    run_optional_step_with_args(IMMUTABLE_LEDGER_STEP, ["--date", target_date, "--stage", "PRELOCK"])
    run_optional_step_with_args(EXPERIMENT_PERFORMANCE_STEP, [])
    run_optional_step_with_args(GOVERNANCE_STEP, ["--date", target_date])
    run_optional_step_with_args(MASTER_REPORT_STEP, ["--date", target_date, "--snapshot-dir", str(snapshot_dir)])
    run_optional_step_with_args(SCOREBOARD_STEP, ["--date", target_date])
    print("\n=== TODAY PRE-LOCK PIPELINE COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
