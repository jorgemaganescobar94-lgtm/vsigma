from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient, split_fresh_stale_rows


ROOT = Path(__file__).resolve().parents[1]

OFFICIAL_TOP = "vsigma_today_competition_top.csv"
PRELOCK_TOP = "vsigma_today_prelock_competition_top.csv"
PRELOCK_REPORT = "vsigma_today_prelock_report.txt"
PRELOCK_AUDIT = "vsigma_prelock_exclusion_audit.csv"
DECISION_SUMMARY_CSV = "vsigma_cloud_decision_summary.csv"
DECISION_SUMMARY_MD = "vsigma_cloud_decision_summary.md"

CANDIDATE_TOP_FILES = [
    "vsigma_today_candidate_v2_competition_top.csv",
    "vsigma_today_candidate_v4_competition_top.csv",
    "vsigma_today_candidate_v5_competition_top.csv",
    "vsigma_today_candidate_v6_competition_top.csv",
    "vsigma_today_candidate_v7_competition_top.csv",
]

REFRESH_TEXT_TRIGGERS = [
    "only stale rows found",
    "ledger has no rows for target date",
    "official_baseline_output | WARNING",
    "Morning official picks reviewed: 0",
]

SUMMARY_COLUMNS = [
    "target_date",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
    "fixture_datetime",
    "minutes_to_kickoff",
    "prelock_retained",
    "prelock_decision",
    "prelock_decision_reason",
    "exclusion_reason",
    "decision_state",
    "decision_reason",
    "next_action",
]

BLOCKING_PRELOCK_DECISIONS = {"PRELOCK_REMOVED", "PRELOCK_DOWNGRADED", "PRELOCK_NOT_AVAILABLE"}
CLOUD_RUNNER_PYTHON_MARKERS = ("cloud runner python active", "local .venv not required")


@dataclass(frozen=True)
class AutoRunResult:
    pre_refreshed: bool
    refresh_reasons: list[str]
    summary_paths: dict[str, Path]
    summary: pd.DataFrame
    technical_warnings: "TechnicalWarnings"


@dataclass(frozen=True)
class StepResult:
    script_path: str
    args: list[str]
    returncode: int
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class TechnicalWarnings:
    healthcheck_status: str = "NOT_RUN"
    pre_refresh_attempted: bool = False
    pre_refresh_failed: bool = False
    pre_refresh_skipped_reason: str = ""
    pre_refresh_error: str = ""
    prelock_failed: bool = False
    prelock_error: str = ""
    audit_failed: bool = False
    audit_error: str = ""

    def has_failure(self) -> bool:
        return (
            self.healthcheck_status == "BROKEN"
            or self.pre_refresh_failed
            or self.prelock_failed
            or self.audit_failed
        )


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def today_in_timezone(timezone_name: str) -> str:
    return datetime.now(ZoneInfo(timezone_name)).date().isoformat()


def run_step(script_path: str, args: list[str], allow_failure: bool = False) -> StepResult:
    command = [sys.executable, script_path, *args]
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    print("\n=== AUTO RUNNING ===", flush=True)
    print(" ".join(command), flush=True)
    try:
        completed = subprocess.run(command, cwd=ROOT, check=False, env=env)
    except OSError as exc:
        result = StepResult(script_path=script_path, args=list(args), returncode=1, error=f"{script_path} failed to start: {exc}")
        if allow_failure:
            print(f"WARNING: {result.error}", flush=True)
            return result
        raise RuntimeError(result.error) from exc
    result = StepResult(
        script_path=script_path,
        args=list(args),
        returncode=int(completed.returncode),
        error="" if completed.returncode == 0 else f"{script_path} exited with {completed.returncode}",
    )
    if completed.returncode != 0:
        if allow_failure:
            print(f"WARNING: {result.error}", flush=True)
            return result
        raise RuntimeError(result.error)
    return result


def read_text_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def fresh_rows(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    fresh, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    return fresh.reset_index(drop=True)


def read_fresh_csv(path: Path, target_date: str) -> pd.DataFrame:
    return fresh_rows(read_csv_lenient(path), target_date)


def key_for_row(row: pd.Series | dict[str, object]) -> tuple[str, str]:
    return (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")))


def index_by_key(df: pd.DataFrame) -> dict[tuple[str, str], pd.Series]:
    rows: dict[tuple[str, str], pd.Series] = {}
    if df.empty:
        return rows
    for _, row in df.iterrows():
        key = key_for_row(row)
        if key[0] and key not in rows:
            rows[key] = row
    return rows


def lookup_row(index: dict[tuple[str, str], pd.Series], row: pd.Series) -> pd.Series | None:
    key = key_for_row(row)
    if key in index:
        return index[key]
    fixture_id = key[0]
    if not fixture_id:
        return None
    matches = [value for candidate_key, value in index.items() if candidate_key[0] == fixture_id]
    return matches[0] if matches else None


def has_rows_for_target(path: Path, target_date: str) -> bool:
    if not path.exists():
        return False
    return not read_fresh_csv(path, target_date).empty


def global_file_has_non_target_rows(path: Path, target_date: str) -> bool:
    if not path.exists():
        return False
    df = read_csv_lenient(path)
    if df.empty:
        return False
    fresh = fresh_rows(df, target_date)
    return len(fresh) != len(df)


def health_summary_requires_pre(summary: pd.DataFrame) -> list[str]:
    reasons: list[str] = []
    if summary.empty:
        return reasons
    status = summary.get("status", pd.Series("", index=summary.index)).astype(str).str.upper()
    check_name = summary.get("check_name", pd.Series("", index=summary.index)).astype(str)
    detail = summary.get("detail", pd.Series("", index=summary.index)).astype(str).str.lower()
    warning_rows = summary[status.isin(["WARNING", "NEEDS_ATTENTION", "BROKEN"])]
    for _, row in warning_rows.iterrows():
        check = norm_text(row.get("check_name"))
        row_detail = norm_text(row.get("detail"))
        if check == "official_baseline_output":
            reasons.append(f"{check} | {row.get('status')}: {row_detail}")
        elif check.startswith("candidate_output"):
            reasons.append(f"{check} | {row.get('status')}: {row_detail}")
    stale = summary[detail.str.contains("only stale rows found", regex=False)]
    if not stale.empty:
        reasons.append("health summary reports only stale rows found")
    ledger = summary[detail.str.contains("ledger has no rows for target date", regex=False)]
    if not ledger.empty:
        reasons.append("health summary reports ledger has no rows for target date")
    return reasons


def read_healthcheck_status(processed_dir: Path, target_date: str, fallback: str) -> str:
    summary_path = processed_dir / "health" / "vsigma_healthcheck_summary.csv"
    summary = read_csv_lenient(summary_path)
    if summary.empty or "global_health_status" not in summary.columns:
        return fallback
    rows = fresh_rows(summary, target_date)
    source = rows if not rows.empty else summary
    status = norm_upper(source.iloc[0].get("global_health_status"))
    if status == "BROKEN" and is_nonfatal_cloud_venv_healthcheck(source, processed_dir):
        return "WARNING"
    return status or fallback


def is_nonfatal_cloud_venv_healthcheck(summary: pd.DataFrame, processed_dir: Path) -> bool:
    if summary.empty:
        return False
    status = summary.get("status", pd.Series("", index=summary.index)).astype(str).str.upper()
    broken = summary[status.eq("BROKEN")].copy()
    if broken.empty:
        return False
    check_names = broken.get("check_name", pd.Series("", index=broken.index)).astype(str)
    if not check_names.eq("venv_python_exists").all():
        return False
    detail_text = " ".join(
        broken.get(column, pd.Series("", index=broken.index)).fillna("").astype(str).str.lower().str.cat(sep=" ")
        for column in ["detail", "recovery_command", "evidence_path"]
        if column in broken.columns
    )
    report_text = read_text_optional(processed_dir / "health" / "vsigma_healthcheck_report.md").lower()
    combined = f"{detail_text} {report_text}"
    return any(marker in combined for marker in CLOUD_RUNNER_PYTHON_MARKERS)


def detect_pre_refresh_needed(processed_dir: Path, target_date: str) -> list[str]:
    reasons: list[str] = []
    snap = snapshot_dir(processed_dir, target_date)
    health_report = processed_dir / "health" / "vsigma_healthcheck_report.md"
    health_summary_path = processed_dir / "health" / "vsigma_healthcheck_summary.csv"
    master_report = snap / "daily_competition_master_report.md"
    snapshot_top = snap / OFFICIAL_TOP
    global_top = processed_dir / OFFICIAL_TOP
    prelock_report = snap / PRELOCK_REPORT

    combined_text = "\n".join(
        [
            read_text_optional(health_report),
            read_text_optional(master_report),
            read_text_optional(prelock_report),
        ]
    )
    lower_text = combined_text.lower()
    for trigger in REFRESH_TEXT_TRIGGERS:
        if trigger.lower() in lower_text:
            reasons.append(f"text trigger: {trigger}")

    if health_summary_path.exists():
        reasons.extend(health_summary_requires_pre(read_csv_lenient(health_summary_path)))

    if not snapshot_top.exists():
        reasons.append(f"missing snapshot official top: {snapshot_top}")
    elif not has_rows_for_target(snapshot_top, target_date):
        reasons.append(f"snapshot official top has no rows for {target_date}")

    master_text = read_text_optional(master_report)
    if "PRE_LOCK_PENDING" in master_text and global_file_has_non_target_rows(global_top, target_date):
        reasons.append("master report has PRE_LOCK_PENDING while global official top includes another target date")

    if global_file_has_non_target_rows(global_top, target_date):
        reasons.append("global official top includes rows outside target date")

    for filename in CANDIDATE_TOP_FILES:
        path = processed_dir / filename
        if global_file_has_non_target_rows(path, target_date):
            reasons.append(f"global candidate top includes rows outside target date: {filename}")

    return sorted(dict.fromkeys(reasons))


def source_candidate_rows(processed_dir: Path, target_date: str) -> tuple[pd.DataFrame, Path]:
    snap_path = snapshot_dir(processed_dir, target_date) / OFFICIAL_TOP
    global_path = processed_dir / OFFICIAL_TOP
    snap_rows = read_fresh_csv(snap_path, target_date)
    if not snap_rows.empty or snap_path.exists():
        return snap_rows, snap_path
    return read_fresh_csv(global_path, target_date), global_path


def first_available(row: pd.Series | None, columns: Iterable[str]) -> object:
    if row is None:
        return ""
    for column in columns:
        if column in row.index and norm_text(row.get(column)):
            return row.get(column)
    return ""


def map_decision_state(
    exclusion_reason: object,
    prelock_retained: object = "",
    prelock_decision: object = "",
    minutes_to_kickoff: object = "",
    *,
    no_candidates: bool = False,
    technical_warning: bool = False,
    past_target_date: bool = False,
) -> str:
    if technical_warning:
        return "TECHNICAL_WARNING"
    if past_target_date and no_candidates:
        return "PAST_DATE_NO_PRE_REFRESH"
    if no_candidates:
        return "NO_BET"
    if past_target_date:
        return "POST_ONLY"

    retained = norm_upper(prelock_retained) in {"YES", "TRUE", "1"}
    decision = norm_upper(prelock_decision)
    exclusion = norm_upper(exclusion_reason)

    if retained and decision not in BLOCKING_PRELOCK_DECISIONS:
        return "EXECUTABLE"
    if exclusion == "OUTSIDE_90_MIN_PRELOCK_WINDOW":
        return "WAITING_FOR_PRELOCK_WINDOW"
    if exclusion == "IN_WINDOW_BUT_NOT_RETAINED":
        return "IN_WINDOW_BUT_BLOCKED"
    if exclusion == "MISSING_KICKOFF_DATETIME":
        return "DATA_PROBLEM"
    if exclusion == "KICKOFF_ALREADY_PASSED":
        return "POST_PENDING"
    if exclusion == "PRELOCK_NOT_AVAILABLE" or decision == "PRELOCK_NOT_AVAILABLE":
        return "PRELOCK_BLOCKED"
    if retained:
        return "IN_WINDOW_BUT_BLOCKED"
    return "PRELOCK_BLOCKED"


def decision_reason_for(state: str, exclusion_reason: str, prelock_decision: str) -> str:
    if state == "EXECUTABLE":
        return "Pick retained in PRELOCK output with no blocking prelock decision."
    if state == "WAITING_FOR_PRELOCK_WINDOW":
        return "Candidate is outside the configured prelock window."
    if state == "IN_WINDOW_BUT_BLOCKED":
        if prelock_decision:
            return f"Prelock decision blocks execution: {prelock_decision}."
        return "Candidate is in the prelock window but was not retained by PRELOCK."
    if state == "PRELOCK_BLOCKED":
        return "PRELOCK was not available for this candidate; execution waits for the next AUTO PRELOCK cycle or no-bet review."
    if state == "DATA_PROBLEM":
        return "Kickoff datetime is missing or unusable."
    if state == "POST_PENDING":
        return "Kickoff has passed and post-result grading is still pending."
    if state == "NO_BET":
        return "No current official baseline candidates exist for the target date."
    if state == "TECHNICAL_WARNING":
        return "A technical step failed in AUTO mode; execution must wait for review of the warning fields."
    if state == "POST_ONLY":
        return "Target date is in the past; AUTO skipped PRE recovery and execution is not applicable."
    if state == "PAST_DATE_NO_PRE_REFRESH":
        return "Target date is in the past and no current candidates exist; AUTO skipped PRE recovery."
    if exclusion_reason:
        return f"PRELOCK did not retain the pick; audit reason: {exclusion_reason}."
    return "Candidates exist but PRELOCK retained no row and no specific audit reason was available."


def next_action_for(state: str, audit_action: str) -> str:
    if state == "EXECUTABLE":
        return "EXECUTE_GOVERNED_PICK"
    if state == "NO_BET":
        return "NO_ACTION"
    if state == "TECHNICAL_WARNING":
        return "REVIEW_AUTO_TECHNICAL_WARNINGS"
    if state == "POST_ONLY":
        return "RUN_POST_WHEN_RESULTS_AVAILABLE"
    if state == "PAST_DATE_NO_PRE_REFRESH":
        return "NO_PRE_REFRESH_FOR_PAST_DATE"
    if state == "PRELOCK_BLOCKED":
        return "WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW"
    if audit_action:
        return audit_action
    return {
        "WAITING_FOR_PRELOCK_WINDOW": "WAIT_FOR_NEXT_PRELOCK_SLOT",
        "IN_WINDOW_BUT_BLOCKED": "DO_NOT_EXECUTE_REVIEW_BLOCK_REASON",
        "DATA_PROBLEM": "FIX_FIXTURE_TIME_FIELDS",
        "POST_PENDING": "RUN_POST_WHEN_RESULTS_AVAILABLE",
        "PRELOCK_BLOCKED": "WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW",
    }.get(state, "CHECK_PRELOCK_OUTPUTS")


def build_decision_summary(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    window_minutes: int = 90,
    pre_refreshed: bool = False,
    refresh_reasons: list[str] | None = None,
    technical_warnings: TechnicalWarnings | None = None,
    past_target_date: bool = False,
) -> tuple[pd.DataFrame, dict[str, Path]]:
    target_date = pd.Timestamp(target_date or date.today().isoformat()).date().isoformat()
    snap = snapshot_dir(processed_dir, target_date)
    snap.mkdir(parents=True, exist_ok=True)
    refresh_reasons = refresh_reasons or []
    technical_warnings = technical_warnings or TechnicalWarnings()

    candidates, candidate_source = source_candidate_rows(processed_dir, target_date)
    prelock_path = snap / PRELOCK_TOP
    audit_path = snap / PRELOCK_AUDIT
    prelock_report_path = snap / PRELOCK_REPORT
    global_candidate_source = processed_dir / OFFICIAL_TOP

    prelock = read_fresh_csv(prelock_path, target_date)
    audit = read_fresh_csv(audit_path, target_date)
    prelock_index = index_by_key(prelock)
    audit_index = index_by_key(audit)

    rows: list[dict[str, object]] = []
    if candidates.empty:
        state = map_decision_state(
            "",
            no_candidates=True,
            past_target_date=past_target_date,
        )
        rows.append(
            {
                "target_date": target_date,
                "fixture_id": "",
                "league": "",
                "home_team": "",
                "away_team": "",
                "market_primary": "",
                "competition_calibrated_prob": "",
                "accuracy_confidence_score": "",
                "accuracy_primary_risk": "",
                "fixture_datetime": "",
                "minutes_to_kickoff": "",
                "prelock_retained": "NO",
                "prelock_decision": "",
                "prelock_decision_reason": "",
                "exclusion_reason": "",
                "decision_state": state,
                "decision_reason": decision_reason_for(state, "", ""),
                "next_action": next_action_for(state, ""),
            }
        )
    else:
        key_columns = [column for column in ["fixture_id", "market_primary"] if column in candidates.columns]
        candidates = candidates.drop_duplicates(key_columns or None).reset_index(drop=True)
        for _, candidate in candidates.iterrows():
            audit_row = lookup_row(audit_index, candidate)
            prelock_row = lookup_row(prelock_index, candidate)
            retained = prelock_row is not None
            prelock_decision = norm_upper(first_available(prelock_row, ["prelock_decision"]))
            prelock_reason = norm_text(first_available(prelock_row, ["prelock_decision_reason"]))
            if not prelock_decision and audit_row is not None:
                prelock_decision = norm_upper(first_available(audit_row, ["prelock_decision"]))
            if not prelock_reason and audit_row is not None:
                prelock_reason = norm_text(first_available(audit_row, ["prelock_decision_reason"]))
            exclusion_reason = norm_upper(first_available(audit_row, ["exclusion_reason"]))
            audit_action = norm_text(first_available(audit_row, ["next_action"]))
            minutes = first_available(audit_row, ["minutes_to_kickoff"])
            state = map_decision_state(
                exclusion_reason,
                "YES" if retained else "NO",
                prelock_decision,
                minutes,
                technical_warning=technical_warnings.has_failure(),
                past_target_date=past_target_date,
            )
            rows.append(
                {
                    "target_date": target_date,
                    "fixture_id": norm_text(candidate.get("fixture_id")),
                    "league": norm_text(first_available(audit_row, ["league"]) or candidate.get("league")),
                    "home_team": norm_text(first_available(audit_row, ["home_team"]) or candidate.get("home_team")),
                    "away_team": norm_text(first_available(audit_row, ["away_team"]) or candidate.get("away_team")),
                    "market_primary": norm_upper(candidate.get("market_primary")),
                    "competition_calibrated_prob": first_available(audit_row, ["competition_calibrated_prob"]) or candidate.get("competition_calibrated_prob", ""),
                    "accuracy_confidence_score": first_available(audit_row, ["accuracy_confidence_score"]) or candidate.get("accuracy_confidence_score", ""),
                    "accuracy_primary_risk": first_available(audit_row, ["accuracy_primary_risk"]) or candidate.get("accuracy_primary_risk", ""),
                    "fixture_datetime": first_available(audit_row, ["fixture_datetime"]) or first_available(candidate, ["fixture_datetime", "fixture_datetime_utc", "date"]),
                    "minutes_to_kickoff": minutes,
                    "prelock_retained": "YES" if retained else "NO",
                    "prelock_decision": prelock_decision,
                    "prelock_decision_reason": prelock_reason,
                    "exclusion_reason": exclusion_reason,
                    "decision_state": state,
                    "decision_reason": decision_reason_for(state, exclusion_reason, prelock_decision),
                    "next_action": next_action_for(state, audit_action),
                }
            )

    summary = pd.DataFrame(rows, columns=SUMMARY_COLUMNS)
    csv_path = snap / DECISION_SUMMARY_CSV
    md_path = snap / DECISION_SUMMARY_MD
    summary.to_csv(csv_path, index=False)

    executable = summary[summary["decision_state"].eq("EXECUTABLE")]
    waiting = summary[summary["decision_state"].eq("WAITING_FOR_PRELOCK_WINDOW")]
    blocked = summary[summary["decision_state"].isin(["IN_WINDOW_BUT_BLOCKED", "PRELOCK_BLOCKED"])]
    data_problem = summary[summary["decision_state"].eq("DATA_PROBLEM")]
    prelock_unavailable = summary[summary["decision_state"].eq("PRELOCK_BLOCKED")]
    no_candidate_states = {"NO_BET", "PAST_DATE_NO_PRE_REFRESH"}
    candidate_count = 0 if set(summary["decision_state"].astype(str)).issubset(no_candidate_states) else len(summary)
    next_auto = automatic_next_action(summary)
    prelock_empty_note = "YES" if prelock.empty else "NO"

    wait_blocked = summary[
        summary["decision_state"].isin(
            [
                "WAITING_FOR_PRELOCK_WINDOW",
                "IN_WINDOW_BUT_BLOCKED",
                "DATA_PROBLEM",
                "POST_PENDING",
                "PRELOCK_BLOCKED",
                "TECHNICAL_WARNING",
                "POST_ONLY",
                "PAST_DATE_NO_PRE_REFRESH",
            ]
        )
    ]
    lines = [
        f"# vSIGMA Cloud Decision Summary - {target_date}",
        "",
        "## Status",
        f"- Auto status: {overall_auto_status(summary)}",
        f"- PRE refreshed: {'YES' if pre_refreshed else 'NO'}",
        f"- Candidates reviewed: {candidate_count}",
        f"- Executable picks: {len(executable)}",
        f"- Waiting picks: {len(waiting)}",
        f"- Blocked picks: {len(blocked)}",
        f"- Data problem picks: {len(data_problem)}",
        f"- Next automatic action: {next_auto}",
        "",
        "## Executable Picks",
        format_markdown_table(executable, ["fixture_id", "league", "home_team", "away_team", "market_primary", "competition_calibrated_prob", "prelock_decision", "next_action"], max_rows=50),
        "",
        "## Waiting / Blocked Picks",
        format_markdown_table(wait_blocked, ["fixture_id", "league", "home_team", "away_team", "market_primary", "fixture_datetime", "minutes_to_kickoff", "decision_state", "exclusion_reason", "next_action"], max_rows=50),
        "",
        "## Technical Warnings",
        f"- healthcheck_status: {technical_warnings.healthcheck_status}",
        f"- pre_refresh_attempted: {'YES' if technical_warnings.pre_refresh_attempted else 'NO'}",
        f"- pre_refresh_failed: {'YES' if technical_warnings.pre_refresh_failed else 'NO'}",
        f"- pre_refresh_skipped_reason: {technical_warnings.pre_refresh_skipped_reason or 'none'}",
        f"- pre_refresh_error: {technical_warnings.pre_refresh_error or 'none'}",
        f"- prelock_failed: {'YES' if technical_warnings.prelock_failed else 'NO'}",
        f"- prelock_error: {technical_warnings.prelock_error or 'none'}",
        f"- audit_failed: {'YES' if technical_warnings.audit_failed else 'NO'}",
        f"- audit_error: {technical_warnings.audit_error or 'none'}",
        "",
        "## Technical Notes",
        f"- Timezone: {timezone_name}",
        f"- Window minutes: {window_minutes}",
        f"- PRE refreshed by auto controller: {'YES' if pre_refreshed else 'NO'}",
        f"- PRE refresh reasons: {'; '.join(refresh_reasons) if refresh_reasons else 'none'}",
        f"- PRELOCK retained no rows: {prelock_empty_note}",
        f"- PRELOCK unavailable rows: {len(prelock_unavailable)}",
        f"- Candidate source used: {candidate_source}",
        f"- Global candidate fallback: {global_candidate_source}",
        f"- PRELOCK source: {prelock_path}",
        f"- Audit source: {audit_path}",
        f"- PRELOCK report: {prelock_report_path}",
        f"- Summary CSV: {csv_path}",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return summary, {"summary_csv": csv_path, "summary_md": md_path}


def overall_auto_status(summary: pd.DataFrame) -> str:
    if summary.empty or summary["decision_state"].eq("NO_BET").all():
        return "NO_BET"
    if summary["decision_state"].eq("PAST_DATE_NO_PRE_REFRESH").all():
        return "PAST_DATE_NO_PRE_REFRESH"
    if summary["decision_state"].eq("TECHNICAL_WARNING").any():
        return "TECHNICAL_WARNING"
    if summary["decision_state"].eq("POST_ONLY").any():
        return "POST_ONLY"
    if summary["decision_state"].eq("EXECUTABLE").any():
        return "EXECUTABLE"
    if summary["decision_state"].eq("DATA_PROBLEM").any():
        return "DATA_PROBLEM"
    if summary["decision_state"].isin(["IN_WINDOW_BUT_BLOCKED", "PRELOCK_BLOCKED", "WAITING_FOR_PRELOCK_WINDOW"]).any():
        return "WAITING_OR_BLOCKED"
    if summary["decision_state"].eq("POST_PENDING").any():
        return "POST_PENDING"
    return "NO_EXECUTABLE_PICK"


def automatic_next_action(summary: pd.DataFrame) -> str:
    status = overall_auto_status(summary)
    return {
        "NO_BET": "NO_ACTION",
        "TECHNICAL_WARNING": "REVIEW_AUTO_TECHNICAL_WARNINGS",
        "POST_ONLY": "RUN_POST_WHEN_RESULTS_AVAILABLE",
        "PAST_DATE_NO_PRE_REFRESH": "NO_PRE_REFRESH_FOR_PAST_DATE",
        "EXECUTABLE": "EXECUTE_GOVERNED_PICK",
        "DATA_PROBLEM": "FIX_DATA_PROBLEMS",
        "WAITING_OR_BLOCKED": "WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW",
        "POST_PENDING": "RUN_POST_WHEN_RESULTS_AVAILABLE",
        "NO_EXECUTABLE_PICK": "WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW",
    }.get(status, "CHECK_PRELOCK_OUTPUTS")


def run_auto_controller(target_date: str, timezone_name: str, window_minutes: int, processed_dir: Path = PROCESSED_DIR) -> AutoRunResult:
    target_date = pd.Timestamp(target_date).date().isoformat()
    local_today = today_in_timezone(timezone_name)
    past_target_date = target_date < local_today

    healthcheck = run_step(
        "scripts/run_vsigma_healthcheck.py",
        ["--date", target_date, "--timezone", timezone_name, "--mode", "full"],
        allow_failure=True,
    )
    healthcheck_status = read_healthcheck_status(
        processed_dir,
        target_date,
        "OK" if healthcheck.ok else "BROKEN",
    )
    if not healthcheck.ok:
        health_summary = read_csv_lenient(processed_dir / "health" / "vsigma_healthcheck_summary.csv")
        health_source = fresh_rows(health_summary, target_date)
        if health_source.empty:
            health_source = health_summary
        if not is_nonfatal_cloud_venv_healthcheck(health_source, processed_dir):
            healthcheck_status = "BROKEN"

    try:
        refresh_reasons = detect_pre_refresh_needed(processed_dir, target_date)
    except Exception as exc:
        refresh_reasons = [f"pre refresh detection failed: {exc}"]

    pre_refreshed = False
    pre_refresh_attempted = False
    pre_refresh_failed = False
    pre_refresh_skipped_reason = "PAST_TARGET_DATE" if past_target_date else ""
    pre_refresh_error = ""

    if past_target_date:
        print("\n=== AUTO PRE REFRESH SKIPPED ===", flush=True)
        print(f"- target_date {target_date} is before local today {local_today}", flush=True)
    elif refresh_reasons:
        print("\n=== AUTO PRE REFRESH TRIGGERED ===", flush=True)
        for reason in refresh_reasons:
            print(f"- {reason}", flush=True)
        pre_refresh_attempted = True
        pre_refresh = run_step(
            "scripts/run_daily_competition_controller.py",
            ["--date", target_date, "--timezone", timezone_name, "--mode", "pre"],
            allow_failure=True,
        )
        pre_refreshed = pre_refresh.ok
        pre_refresh_failed = not pre_refresh.ok
        pre_refresh_error = pre_refresh.error
    else:
        print("\n=== AUTO PRE REFRESH NOT REQUIRED ===", flush=True)

    prelock = run_step(
        "scripts/run_today_prelock_pipeline.py",
        ["--date", target_date, "--timezone", timezone_name, "--window-minutes", str(window_minutes)],
        allow_failure=True,
    )
    audit = run_step(
        "scripts/build_prelock_exclusion_audit.py",
        ["--date", target_date, "--timezone", timezone_name, "--window-minutes", str(window_minutes)],
        allow_failure=True,
    )
    technical_warnings = TechnicalWarnings(
        healthcheck_status=healthcheck_status,
        pre_refresh_attempted=pre_refresh_attempted,
        pre_refresh_failed=pre_refresh_failed,
        pre_refresh_skipped_reason=pre_refresh_skipped_reason,
        pre_refresh_error=pre_refresh_error,
        prelock_failed=not prelock.ok,
        prelock_error=prelock.error,
        audit_failed=not audit.ok,
        audit_error=audit.error,
    )
    summary, paths = build_decision_summary(
        processed_dir,
        target_date,
        timezone_name,
        window_minutes,
        pre_refreshed,
        refresh_reasons,
        technical_warnings,
        past_target_date,
    )
    return AutoRunResult(pre_refreshed, refresh_reasons, paths, summary, technical_warnings)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run vSIGMA automatic cloud controller.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--window-minutes", type=int, default=90)
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    try:
        result = run_auto_controller(target_date, args.timezone, args.window_minutes, args.processed_dir)
    except Exception as exc:
        print(f"ERROR: AUTO controller could not generate decision summary: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    summary = result.summary
    no_candidate_states = {"NO_BET", "PAST_DATE_NO_PRE_REFRESH"}
    candidates = 0 if set(summary["decision_state"].astype(str)).issubset(no_candidate_states) else len(summary)
    executable = int(summary["decision_state"].eq("EXECUTABLE").sum())
    waiting = int(summary["decision_state"].eq("WAITING_FOR_PRELOCK_WINDOW").sum())
    blocked = int(summary["decision_state"].isin(["IN_WINDOW_BUT_BLOCKED", "PRELOCK_BLOCKED"]).sum())
    data_problem = int(summary["decision_state"].eq("DATA_PROBLEM").sum())

    print("\n=== VSIGMA AUTO CONTROLLER ===")
    print(f"AUTO status: {overall_auto_status(summary)}")
    print(f"PRE refreshed: {'YES' if result.pre_refreshed else 'NO'}")
    print(f"Candidates count: {candidates}")
    print(f"Executable count: {executable}")
    print(f"Waiting count: {waiting}")
    print(f"Blocked count: {blocked}")
    print(f"Data problem count: {data_problem}")
    print(f"Healthcheck status: {result.technical_warnings.healthcheck_status}")
    print(f"PRE refresh attempted: {'YES' if result.technical_warnings.pre_refresh_attempted else 'NO'}")
    print(f"PRE refresh failed: {'YES' if result.technical_warnings.pre_refresh_failed else 'NO'}")
    print(f"PRE refresh skipped reason: {result.technical_warnings.pre_refresh_skipped_reason or 'none'}")
    print(f"PRELOCK failed: {'YES' if result.technical_warnings.prelock_failed else 'NO'}")
    print(f"Audit failed: {'YES' if result.technical_warnings.audit_failed else 'NO'}")
    print(f"Summary CSV: {result.summary_paths['summary_csv']}")
    print(f"Summary MD: {result.summary_paths['summary_md']}")


if __name__ == "__main__":
    main()
