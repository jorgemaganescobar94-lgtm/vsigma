from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import (
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )
    from run_today_prelock_pipeline import minutes_to_kickoff
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )
    from scripts.run_today_prelock_pipeline import minutes_to_kickoff


ROOT = Path(__file__).resolve().parents[1]

PLAN_CSV = "daily_run_plan.csv"
PLAN_MD = "daily_run_plan.md"
PLAN_LATEST_MD = "daily_run_plan_latest.md"
STATUS_MD = "daily_controller_status.md"

OFFICIAL_TOP = "vsigma_today_competition_top.csv"
CANDIDATE_V2_TOP = "vsigma_today_candidate_v2_competition_top.csv"
CANDIDATE_V7_TOP = "vsigma_today_candidate_v7_competition_top.csv"
CANDIDATE_V7_SHORTLIST = "vsigma_today_candidate_v7_competition_shortlist.csv"
PRELOCK_COMPARISON = "vsigma_today_prelock_comparison.csv"
PRELOCK_ORCHESTRATOR_SUMMARY = "vsigma_today_prelock_orchestrator_summary.csv"
TODAY_PIPELINE_REPORT = "today_pipeline_report.csv"
TODAY_POST_REPORT = "today_post_results_report.csv"
OFFICIAL_POST_LEDGER = "vsigma_execution_shortlist_results_ledger.csv"
IMMUTABLE_LEDGER = "ledger/vsigma_immutable_daily_pick_ledger.csv"
GOVERNANCE_DASHBOARD = "governance/vsigma_governance_dashboard.md"


PICK_FILES = {
    "OFFICIAL_BASELINE": OFFICIAL_TOP,
    "CANDIDATE_V2": CANDIDATE_V2_TOP,
    "CANDIDATE_V7": CANDIDATE_V7_TOP,
    "CANDIDATE_V7_SHORTLIST": CANDIDATE_V7_SHORTLIST,
}

REQUIRED_PLAN_COLUMNS = [
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "kickoff_time",
    "minutes_to_kickoff",
    "prelock_window_start",
    "prelock_status",
    "recommended_next_action",
    "recommended_command",
]

SETTLED_RECORD_STATUSES = {"SETTLED", "VOID"}
PENDING_RECORD_STATUSES = {"PRE_REGISTERED", "PRELOCK_UPDATED", "PENDING"}
V7_REJECTED_STATUSES = {"V7_PRELOCK_REJECTED", "V7_PRICE_REJECTED", "V7_SECONDARY_ONLY"}


def normalize_date(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()[:10]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def parse_target_date(value: str) -> str:
    return pd.Timestamp(value).date().isoformat()


def local_now(timezone_name: str) -> datetime:
    return datetime.now(ZoneInfo(timezone_name))


def command_for(mode: str, target_date: str, timezone_name: str, window_minutes: int) -> str:
    base = f".\\.venv\\Scripts\\python.exe scripts\\run_daily_competition_controller.py --date {target_date} --timezone {timezone_name}"
    if mode == "prelock":
        return f"{base} --mode prelock --window-minutes {window_minutes}"
    return f"{base} --mode {mode}"


def run_step(script_path: str, args: list[str]) -> bool:
    command = [sys.executable, script_path, *args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    print("\n=== CONTROLLER RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    if completed.returncode != 0:
        print(f"WARNING: {script_path} exited with {completed.returncode}", flush=True)
        return False
    return True


def snapshot_dir_for(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def read_snapshot_or_processed(processed_dir: Path, target_date: str, filename: str) -> pd.DataFrame:
    snapshot_path = snapshot_dir_for(processed_dir, target_date) / filename
    if snapshot_path.exists():
        return read_csv_lenient(snapshot_path)
    return read_csv_lenient(processed_dir / filename)


def current_rows(df: pd.DataFrame, target_date: str, include_target_date: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    if df.empty:
        return df.copy(), df.copy()
    fresh, stale = split_fresh_stale_rows(df, target_date, include_target_date=include_target_date)
    return fresh.reset_index(drop=True), stale.reset_index(drop=True)


def read_current_file(processed_dir: Path, target_date: str, filename: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    return current_rows(read_snapshot_or_processed(processed_dir, target_date, filename), target_date)


def safe_first(row: pd.Series, names: list[str], default: object = "") -> object:
    for name in names:
        if name in row.index:
            value = row.get(name)
            if norm_text(value):
                return value
    return default


def kickoff_from_row(row: pd.Series, now_utc: datetime, minutes: float | None) -> datetime | None:
    value = safe_first(row, ["fixture_datetime_utc", "kickoff_time", "fixture_date", "date"])
    text = norm_text(value)
    if text and len(text) > 10:
        try:
            kickoff = pd.Timestamp(text).to_pydatetime()
            if kickoff.tzinfo is None:
                kickoff = kickoff.replace(tzinfo=timezone.utc)
            return kickoff.astimezone(timezone.utc)
        except (TypeError, ValueError):
            pass
    if "fixture_timestamp" in row.index and norm_text(row.get("fixture_timestamp")):
        try:
            return datetime.fromtimestamp(float(row.get("fixture_timestamp")), tz=timezone.utc)
        except (TypeError, ValueError, OSError):
            pass
    if minutes is not None and pd.notna(minutes):
        return now_utc + timedelta(minutes=float(minutes))
    return None


def row_minutes(row: pd.Series, now_utc: datetime) -> float | None:
    value = minutes_to_kickoff(row, now_utc=now_utc)
    if value is None or pd.isna(value):
        return None
    explicit_minutes = any(column in row.index and norm_text(row.get(column)) for column in ["prelock_minutes_to_kickoff", "lineup_minutes_to_kickoff"])
    generated_at = norm_text(row.get("generated_at"))
    if explicit_minutes and generated_at:
        try:
            generated = pd.Timestamp(generated_at).to_pydatetime()
            if generated.tzinfo is None:
                generated = generated.replace(tzinfo=timezone.utc)
            age_minutes = (now_utc - generated.astimezone(timezone.utc)).total_seconds() / 60.0
            return float(value) - age_minutes
        except (TypeError, ValueError):
            return float(value)
    return float(value)


def pre_done(processed_dir: Path, target_date: str) -> bool:
    report, _ = read_current_file(processed_dir, target_date, TODAY_PIPELINE_REPORT)
    if not report.empty:
        return True
    baseline, _ = read_current_file(processed_dir, target_date, OFFICIAL_TOP)
    return not baseline.empty


def post_state(processed_dir: Path, target_date: str) -> str:
    post_report, _ = read_current_file(processed_dir, target_date, TODAY_POST_REPORT)
    ledger = read_csv_lenient(processed_dir / IMMUTABLE_LEDGER)
    if not ledger.empty and "target_date" in ledger.columns:
        day = ledger[ledger["target_date"].astype(str).eq(target_date)].copy()
        picks = day[~day.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy()
        if not picks.empty:
            statuses = picks.get("record_status", pd.Series(dtype=object)).astype(str).str.upper()
            if statuses.isin(SETTLED_RECORD_STATUSES).all():
                return "SETTLED"
            if statuses.isin(PENDING_RECORD_STATUSES).any():
                return "PENDING"
    official_ledger, _ = read_current_file(processed_dir, target_date, OFFICIAL_POST_LEDGER)
    if not official_ledger.empty:
        status = official_ledger.get("ledger_result_status", pd.Series(dtype=object)).astype(str).str.upper()
        if status.eq("RESULT_AVAILABLE").all():
            return "SETTLED"
        return "PENDING"
    if not post_report.empty:
        pending = pd.to_numeric(post_report.get("pending_rows", pd.Series(dtype=object)), errors="coerce").fillna(0)
        return "PENDING" if pending.sum() > 0 else "SETTLED"
    return "PENDING"


def ledger_state(processed_dir: Path, target_date: str) -> tuple[str, pd.DataFrame]:
    ledger = read_csv_lenient(processed_dir / IMMUTABLE_LEDGER)
    if ledger.empty or "target_date" not in ledger.columns:
        return "MISSING", pd.DataFrame()
    day = ledger[ledger["target_date"].astype(str).eq(target_date)].copy()
    if day.empty:
        return "MISSING_FOR_DATE", day
    statuses = day.get("record_status", pd.Series(dtype=object)).astype(str).str.upper()
    if statuses.isin(SETTLED_RECORD_STATUSES).any():
        return "POST_UPDATED", day
    if day.get("pipeline_stage", pd.Series(dtype=object)).astype(str).str.upper().eq("PRELOCK").any():
        return "PRELOCK_UPDATED", day
    if day.get("pipeline_stage", pd.Series(dtype=object)).astype(str).str.upper().eq("PRE").any():
        return "PRE_UPDATED", day
    return "AVAILABLE", day


def v7_counts(v7_shortlist: pd.DataFrame) -> dict[str, int]:
    if v7_shortlist.empty:
        return {"waiting": 0, "confirmed": 0, "rejected": 0, "unavailable": 0}
    status = v7_shortlist.get("candidate_v7_execution_status", pd.Series("", index=v7_shortlist.index)).astype(str).str.upper()
    prelock_status = v7_shortlist.get("candidate_v7_prelock_status", pd.Series("", index=v7_shortlist.index)).astype(str).str.upper()
    return {
        "waiting": int((status.eq("V7_WAITING_FOR_PRELOCK") | prelock_status.eq("V7_WAITING_FOR_PRELOCK")).sum()),
        "confirmed": int(status.eq("V7_PRELOCK_CONFIRMED").sum()),
        "rejected": int(status.isin(V7_REJECTED_STATUSES).sum()),
        "unavailable": int(status.eq("V7_PRELOCK_UNAVAILABLE").sum()),
    }


def collect_pick_rows(processed_dir: Path, target_date: str) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    stale_frames: list[pd.DataFrame] = []
    for label, filename in PICK_FILES.items():
        fresh, stale = read_current_file(processed_dir, target_date, filename)
        if not fresh.empty:
            fresh = fresh.copy()
            fresh["controller_source"] = label
        frames[label] = fresh
        if not stale.empty:
            stale = stale.copy()
            stale["controller_source_file"] = filename
            stale_frames.append(stale)
    stale_all = pd.concat(stale_frames, ignore_index=True) if stale_frames else pd.DataFrame()
    return frames, stale_all


def current_prelock(processed_dir: Path, target_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    return read_current_file(processed_dir, target_date, PRELOCK_COMPARISON)


@dataclass(frozen=True)
class ControllerState:
    target_date: str
    timezone_name: str
    window_minutes: int
    now_local: datetime
    processed_dir: Path
    snapshot_dir: Path
    picks: dict[str, pd.DataFrame]
    stale_pick_rows: pd.DataFrame
    prelock: pd.DataFrame
    stale_prelock: pd.DataFrame
    ledger_status: str
    ledger_day: pd.DataFrame
    post_status: str
    pre_done: bool


def build_state(
    processed_dir: Path,
    target_date: str,
    timezone_name: str,
    window_minutes: int,
    now_local_value: datetime | None = None,
) -> ControllerState:
    now = now_local_value or local_now(timezone_name)
    picks, stale_pick_rows = collect_pick_rows(processed_dir, target_date)
    prelock, stale_prelock = current_prelock(processed_dir, target_date)
    ledger_status_value, ledger_day = ledger_state(processed_dir, target_date)
    return ControllerState(
        target_date=target_date,
        timezone_name=timezone_name,
        window_minutes=window_minutes,
        now_local=now,
        processed_dir=processed_dir,
        snapshot_dir=snapshot_dir_for(processed_dir, target_date),
        picks=picks,
        stale_pick_rows=stale_pick_rows,
        prelock=prelock,
        stale_prelock=stale_prelock,
        ledger_status=ledger_status_value,
        ledger_day=ledger_day,
        post_status=post_state(processed_dir, target_date),
        pre_done=pre_done(processed_dir, target_date),
    )


def prelock_status_for(row: pd.Series, state: ControllerState, minutes: float | None) -> str:
    fixture_id = norm_text(row.get("fixture_id"))
    market = norm_upper(row.get("market_primary"))
    if not state.prelock.empty:
        matches = state.prelock[
            state.prelock.get("fixture_id", pd.Series(dtype=object)).map(norm_text).eq(fixture_id)
            & state.prelock.get("market_primary", pd.Series(dtype=object)).map(norm_upper).eq(market)
        ].copy()
        if not matches.empty:
            return norm_upper(matches.iloc[0].get("prelock_decision")) or norm_upper(matches.iloc[0].get("prelock_status")) or "PRELOCK_REVIEWED"
    v7_status = norm_upper(row.get("candidate_v7_execution_status"))
    if v7_status == "V7_PRELOCK_CONFIRMED":
        return "CONFIRMED"
    if v7_status in V7_REJECTED_STATUSES:
        return "REJECTED"
    if v7_status == "V7_PRELOCK_UNAVAILABLE":
        return "UNAVAILABLE"
    if minutes is not None and 0 <= minutes <= state.window_minutes:
        return "DUE_NOW"
    if minutes is not None and minutes > state.window_minutes:
        return "PENDING_OUTSIDE_WINDOW"
    if minutes is not None and minutes < 0:
        return "KICKOFF_PASSED"
    return "PENDING_TIMING_UNKNOWN"


def recommended_action_for(row: pd.Series, state: ControllerState, prelock_status: str, no_bet_day: bool) -> tuple[str, str]:
    if not state.pre_done:
        return "RUN_PRE", command_for("pre", state.target_date, state.timezone_name, state.window_minutes)
    if no_bet_day:
        return "NO_BET_DAY", command_for("status", state.target_date, state.timezone_name, state.window_minutes)
    if not state.stale_prelock.empty:
        return "CHECK_STALE_OUTPUTS", command_for("status", state.target_date, state.timezone_name, state.window_minutes)
    if state.post_status == "SETTLED":
        return "ALL_SETTLED", command_for("status", state.target_date, state.timezone_name, state.window_minutes)
    if prelock_status == "DUE_NOW":
        return "RUN_PRELOCK_NOW", command_for("prelock", state.target_date, state.timezone_name, state.window_minutes)
    if prelock_status in {"PENDING_OUTSIDE_WINDOW", "PENDING_TIMING_UNKNOWN"}:
        return "WAIT_FOR_PRELOCK", command_for("prelock", state.target_date, state.timezone_name, state.window_minutes)
    return "RUN_POST_AFTER_FINISH", command_for("post", state.target_date, state.timezone_name, state.window_minutes)


def build_plan_frame(state: ControllerState) -> pd.DataFrame:
    pick_frames = [df for df in state.picks.values() if not df.empty]
    now_utc = state.now_local.astimezone(timezone.utc)
    no_bet_day = not pick_frames
    rows: list[dict[str, object]] = []
    source = pd.concat(pick_frames, ignore_index=True) if pick_frames else pd.DataFrame()
    if source.empty:
        action, command = recommended_action_for(pd.Series(dtype=object), state, "NO_CURRENT_PICKS", True)
        rows.append(
            {
                "fixture_id": "",
                "league": "",
                "home_team": "",
                "away_team": "",
                "market_primary": "",
                "kickoff_time": "",
                "minutes_to_kickoff": "",
                "prelock_window_start": "",
                "prelock_status": "NO_CURRENT_PICKS",
                "recommended_next_action": action,
                "recommended_command": command,
            }
        )
    else:
        key_cols = [column for column in ["fixture_id", "market_primary"] if column in source.columns]
        source = source.drop_duplicates(key_cols or None).reset_index(drop=True)
        for _, row in source.iterrows():
            minutes = row_minutes(row, now_utc)
            kickoff = kickoff_from_row(row, now_utc, minutes)
            window_start = kickoff - timedelta(minutes=state.window_minutes) if kickoff is not None else None
            prelock_status = prelock_status_for(row, state, minutes)
            action, command = recommended_action_for(row, state, prelock_status, no_bet_day=False)
            rows.append(
                {
                    "fixture_id": norm_text(row.get("fixture_id")),
                    "league": norm_text(row.get("league")),
                    "home_team": norm_text(row.get("home_team")),
                    "away_team": norm_text(row.get("away_team")),
                    "market_primary": norm_upper(row.get("market_primary")),
                    "kickoff_time": kickoff.isoformat() if kickoff is not None else "",
                    "minutes_to_kickoff": round(float(minutes), 2) if minutes is not None else "",
                    "prelock_window_start": window_start.isoformat() if window_start is not None else "",
                    "prelock_status": prelock_status,
                    "recommended_next_action": action,
                    "recommended_command": command,
                }
            )
    out = pd.DataFrame(rows)
    for column in REQUIRED_PLAN_COLUMNS:
        if column not in out.columns:
            out[column] = ""
    return out[REQUIRED_PLAN_COLUMNS]


def next_action(plan: pd.DataFrame) -> tuple[str, str]:
    priority = [
        "RUN_PRE",
        "RUN_PRELOCK_NOW",
        "CHECK_STALE_OUTPUTS",
        "WAIT_FOR_PRELOCK",
        "RUN_POST_AFTER_FINISH",
        "NO_BET_DAY",
        "ALL_SETTLED",
    ]
    if plan.empty:
        return "NO_BET_DAY", ""
    for action in priority:
        rows = plan[plan["recommended_next_action"].astype(str).eq(action)]
        if not rows.empty:
            return action, norm_text(rows.iloc[0].get("recommended_command"))
    return norm_text(plan.iloc[0].get("recommended_next_action")), norm_text(plan.iloc[0].get("recommended_command"))


def write_plan_outputs(plan: pd.DataFrame, state: ControllerState) -> dict[str, Path]:
    state.snapshot_dir.mkdir(parents=True, exist_ok=True)
    csv_path = state.snapshot_dir / PLAN_CSV
    md_path = state.snapshot_dir / PLAN_MD
    latest_path = state.processed_dir / PLAN_LATEST_MD
    plan.to_csv(csv_path, index=False)
    action, command = next_action(plan)
    lines = [
        f"# vSIGMA Daily Run Plan - {state.target_date}",
        "",
        f"- Timezone: {state.timezone_name}",
        f"- Generated at: {state.now_local.isoformat()}",
        f"- Window minutes: {state.window_minutes}",
        f"- Next recommended action: {action}",
        f"- Next command: `{command}`" if command else "- Next command: ",
        "",
        "## Fixtures",
        format_markdown_table(plan, REQUIRED_PLAN_COLUMNS, max_rows=50),
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    shutil.copy2(md_path, latest_path)
    return {"plan_csv": csv_path, "plan_md": md_path, "latest_plan_md": latest_path}


def picks_summary(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    return format_markdown_table(
        df,
        ["fixture_id", "league", "home_team", "away_team", "market_primary", "accuracy_mode_rank", "candidate_v7_execution_status", "price_discipline_decision"],
        max_rows=20,
    )


def write_status_output(plan: pd.DataFrame, state: ControllerState) -> Path:
    state.snapshot_dir.mkdir(parents=True, exist_ok=True)
    status_path = state.snapshot_dir / STATUS_MD
    action, command = next_action(plan)
    v7_shortlist = state.picks.get("CANDIDATE_V7_SHORTLIST", pd.DataFrame())
    counts = v7_counts(v7_shortlist)
    governance_snapshot = state.snapshot_dir / "vsigma_governance_dashboard.md"
    governance_path = governance_snapshot if governance_snapshot.exists() else state.processed_dir / GOVERNANCE_DASHBOARD
    stale_warning = "NONE"
    if not state.stale_prelock.empty:
        stale_warning = f"STALE_PRELOCK_EXCLUDED: {stale_date_summary(state.stale_prelock, include_target_date=True)}"
    elif not state.stale_pick_rows.empty:
        stale_warning = f"STALE_PICK_ROWS_IGNORED: {stale_date_summary(state.stale_pick_rows, include_target_date=True)}"
    lines = [
        f"# vSIGMA Daily Controller Status - {state.target_date}",
        "",
        "## Step State",
        f"- PRE: {'DONE' if state.pre_done else 'MISSING'}",
        f"- Pre-lock: {plan['prelock_status'].astype(str).drop_duplicates().tolist() if not plan.empty else ['NO_CURRENT_PICKS']}",
        f"- POST: {state.post_status}",
        f"- Ledger: {state.ledger_status}",
        f"- Governance: {'AVAILABLE' if governance_path.exists() else 'MISSING'}",
        f"- Stale warnings: {stale_warning}",
        "",
        "## Next Operator Command",
        f"- Action: {action}",
        f"- Command: `{command}`" if command else "- Command: ",
        "",
        "## Official Baseline Picks",
        picks_summary(state.picks.get("OFFICIAL_BASELINE", pd.DataFrame())),
        "",
        "## Candidate v2 Picks",
        picks_summary(state.picks.get("CANDIDATE_V2", pd.DataFrame())),
        "",
        "## Candidate v7 Decisions",
        f"- Waiting: {counts['waiting']}",
        f"- Confirmed: {counts['confirmed']}",
        f"- Rejected: {counts['rejected']}",
        f"- Unavailable: {counts['unavailable']}",
        picks_summary(v7_shortlist),
        "",
        "## Pre-Lock Timing",
        format_markdown_table(plan, ["fixture_id", "home_team", "away_team", "market_primary", "kickoff_time", "minutes_to_kickoff", "prelock_window_start", "prelock_status", "recommended_next_action"], max_rows=50),
        "",
        "## Ledger State",
        format_markdown_table(
            state.ledger_day,
            ["experiment_id", "fixture_id", "home_team", "away_team", "market_primary", "pipeline_stage", "record_status", "result_status", "result", "profit_units"],
            max_rows=40,
        ),
        "",
        "## Controller Outputs",
        f"- Plan CSV: {state.snapshot_dir / PLAN_CSV}",
        f"- Plan MD: {state.snapshot_dir / PLAN_MD}",
        f"- Status MD: {status_path}",
        "",
    ]
    status_path.write_text("\n".join(lines), encoding="utf-8")
    return status_path


def build_plan_and_status(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    window_minutes: int = 90,
    now_local_value: datetime | None = None,
) -> tuple[pd.DataFrame, dict[str, Path], ControllerState]:
    target_date = target_date or date.today().isoformat()
    state = build_state(processed_dir, target_date, timezone_name, window_minutes, now_local_value)
    plan = build_plan_frame(state)
    paths = write_plan_outputs(plan, state)
    paths["status_md"] = write_status_output(plan, state)
    return plan, paths, state


def run_pre_mode(target_date: str, timezone_name: str) -> bool:
    return run_step("scripts/run_today_match_pipeline.py", ["--date", target_date, "--timezone", timezone_name])


def run_prelock_mode(target_date: str, timezone_name: str, window_minutes: int) -> bool:
    return run_step(
        "scripts/run_today_prelock_orchestrator.py",
        ["--date", target_date, "--timezone", timezone_name, "--window-minutes", str(window_minutes)],
    )


def run_post_mode(target_date: str, timezone_name: str) -> bool:
    return run_step("scripts/run_today_post_results_pipeline.py", ["--date", target_date, "--timezone", timezone_name])


def rebuild_controller_side_reports(target_date: str, timezone_name: str, window_minutes: int, processed_dir: Path) -> None:
    snapshot_dir = snapshot_dir_for(processed_dir, target_date)
    common = ["--date", target_date, "--processed-dir", str(processed_dir)]
    build_plan_and_status(processed_dir, target_date, timezone_name, window_minutes)
    run_step("scripts/build_daily_competition_master_report.py", [*common, "--snapshot-dir", str(snapshot_dir)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vSIGMA daily competition controller.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--mode", choices=["plan", "pre", "prelock", "post", "full", "status"], default="status")
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = parse_target_date(args.date)
    processed_dir = args.processed_dir
    processed_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "pre":
        ok = run_pre_mode(target_date, args.timezone)
        rebuild_controller_side_reports(target_date, args.timezone, args.window_minutes, processed_dir)
        if not ok:
            raise SystemExit(1)
    elif args.mode == "prelock":
        ok = run_prelock_mode(target_date, args.timezone, args.window_minutes)
        rebuild_controller_side_reports(target_date, args.timezone, args.window_minutes, processed_dir)
        if not ok:
            raise SystemExit(1)
    elif args.mode == "post":
        ok = run_post_mode(target_date, args.timezone)
        rebuild_controller_side_reports(target_date, args.timezone, args.window_minutes, processed_dir)
        if not ok:
            raise SystemExit(1)
    elif args.mode == "full":
        ok = run_pre_mode(target_date, args.timezone)
        plan, paths, _state = build_plan_and_status(processed_dir, target_date, args.timezone, args.window_minutes)
        action, command = next_action(plan)
        print("\n=== DAILY CONTROLLER FULL PLAN ===")
        print(f"PRE status: {'PASS' if ok else 'FAILED'}")
        print(f"Plan: {paths['plan_md']}")
        print(f"Next recommended action: {action}")
        print(f"Next recommended command: {command}")
        if not ok:
            raise SystemExit(1)
    else:
        plan, paths, _state = build_plan_and_status(processed_dir, target_date, args.timezone, args.window_minutes)
        action, command = next_action(plan)
        label = "PLAN" if args.mode == "plan" else "STATUS"
        print(f"\n=== DAILY CONTROLLER {label} ===")
        print(f"Plan CSV: {paths['plan_csv']}")
        print(f"Plan MD: {paths['plan_md']}")
        print(f"Status MD: {paths['status_md']}")
        print(f"Next recommended action: {action}")
        print(f"Next recommended command: {command}")


if __name__ == "__main__":
    main()
