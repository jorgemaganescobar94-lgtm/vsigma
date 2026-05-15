from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from daily_hardening import (
        PRE_LOCK_NOTE,
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        PRE_LOCK_NOTE,
        PROCESSED_DIR,
        TODAY_DIR,
        format_markdown_table,
        read_csv_lenient,
        split_fresh_stale_rows,
        stale_date_summary,
    )


MASTER_REPORT = "daily_competition_master_report.md"

PICK_COLUMNS = [
    "accuracy_mode_rank",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
]

SUMMARY_COLUMNS = [
    "mode",
    "pick_count",
    "wins",
    "losses",
    "profit_units",
    "roi_percent",
    "pending_rows",
    "candidate_version",
]


def metric_value(summary: pd.DataFrame, metric: str, default: object = 0) -> object:
    if summary.empty or "metric" not in summary.columns:
        return default
    rows = summary[summary["metric"].astype(str).eq(metric)]
    if rows.empty:
        return default
    if "value_num" in rows.columns:
        value = rows.iloc[0]["value_num"]
        if not pd.isna(value):
            return value
    return default


def result_summary_row(label: str, summary: pd.DataFrame) -> dict[str, object] | None:
    if summary.empty:
        return None
    if "metric" in summary.columns:
        return {
            "mode": label,
            "pick_count": metric_value(summary, "shortlist_rows", 0),
            "wins": metric_value(summary, "wins", 0),
            "losses": metric_value(summary, "losses", 0),
            "profit_units": metric_value(summary, "profit_units_total", 0.0),
            "roi_percent": metric_value(summary, "roi_percent", ""),
            "pending_rows": metric_value(summary, "pending_rows", 0),
            "candidate_version": summary["candidate_version"].iloc[0] if "candidate_version" in summary.columns else label,
        }
    row = summary.iloc[0].to_dict()
    return {
        "mode": row.get("mode", label),
        "pick_count": row.get("pick_count", 0),
        "wins": row.get("wins", 0),
        "losses": row.get("losses", 0),
        "profit_units": row.get("profit_units", 0.0),
        "roi_percent": row.get("roi_percent", ""),
        "pending_rows": row.get("pending_rows", 0),
        "candidate_version": row.get("candidate_version", label),
    }


def build_result_summary_table(summaries: list[tuple[str, pd.DataFrame]]) -> pd.DataFrame:
    rows = [result_summary_row(label, summary) for label, summary in summaries]
    rows = [row for row in rows if row is not None]
    return pd.DataFrame(rows)


def read_snapshot_or_processed(processed_dir: Path, snapshot_dir: Path, filename: str) -> pd.DataFrame:
    snapshot_path = snapshot_dir / filename
    if snapshot_path.exists():
        return read_csv_lenient(snapshot_path)
    return read_csv_lenient(processed_dir / filename)


def split_current_prelock(prelock: pd.DataFrame, target_date: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    if prelock.empty:
        return prelock.copy(), prelock.copy()
    return split_fresh_stale_rows(prelock, target_date, include_target_date=True)


def no_bet_text(label: str, df: pd.DataFrame) -> str:
    if not df.empty:
        return ""
    return f"\n{label}: NO_BET. Empty output is valid when no pick clears the frozen competition filters.\n"


def failure_mode_summary(frames: list[pd.DataFrame]) -> pd.DataFrame:
    values: list[str] = []
    for df in frames:
        for column in ["accuracy_primary_risk", "pick_primary_risk", "failure_mode_flag"]:
            if column in df.columns:
                values.extend(df[column].dropna().astype(str).tolist())
    cleaned = [value for value in values if value and value.upper() not in {"NAN", "NONE"}]
    if not cleaned:
        return pd.DataFrame(columns=["failure_mode", "rows"])
    return (
        pd.Series(cleaned, name="failure_mode")
        .value_counts()
        .rename_axis("failure_mode")
        .reset_index(name="rows")
    )


def clv_data_sufficiency(clv_summary: pd.DataFrame, minimum_rows: int = 10) -> str:
    if clv_summary.empty:
        return "INSUFFICIENT_CLV_DATA"
    usable = 0
    if "clv_usable_for_threshold_calibration_flag" in clv_summary.columns:
        usable = int(pd.to_numeric(clv_summary["clv_usable_for_threshold_calibration_flag"], errors="coerce").fillna(0).eq(1).sum())
    direction = clv_summary.get("clv_direction", pd.Series(dtype=object)).astype(str).str.upper()
    available = int((~direction.isin(["", "NAN", "CLV_UNAVAILABLE"])).sum())
    if usable < minimum_rows and available < minimum_rows:
        return "INSUFFICIENT_CLV_DATA"
    return "CLV_DATA_SUFFICIENT_FOR_REVIEW"


def current_day_status(baseline: pd.DataFrame, result_summary: pd.DataFrame, prelock: pd.DataFrame) -> str:
    if baseline.empty:
        return "NO_BET"
    pending = pd.to_numeric(result_summary.get("pending_rows", pd.Series(dtype=float)), errors="coerce").fillna(0)
    settled = pd.to_numeric(result_summary.get("wins", pd.Series(dtype=float)), errors="coerce").fillna(0) + pd.to_numeric(
        result_summary.get("losses", pd.Series(dtype=float)), errors="coerce"
    ).fillna(0)
    if settled.sum() > 0 and pending.sum() == 0:
        return "POST_SETTLED"
    if not prelock.empty and "prelock_status" in prelock.columns and prelock["prelock_status"].astype(str).eq("IN_PRELOCK_WINDOW").any():
        return "PRE_LOCK_REVIEWED"
    return "PRE_LOCK_PENDING"


def build_master_report(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    snapshot_dir: Path | None = None,
) -> Path:
    target_date = target_date or date.today().isoformat()
    snapshot_dir = snapshot_dir or TODAY_DIR / target_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_competition_top.csv")
    v2 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_competition_top.csv")
    v4 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v4_competition_top.csv")
    v5 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v5_competition_top.csv")
    v6 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v6_competition_top.csv")
    v7 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v7_competition_top.csv")
    v7_shortlist = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v7_competition_shortlist.csv")
    forecasts = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_match_script_forecasts.csv")
    comparison_v2 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2.csv")
    comparison_v4 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv")
    comparison_v5 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv")
    comparison_v6 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv")
    comparison_v7 = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv")
    freshness = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_daily_freshness_report.csv")
    isolation = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_candidate_isolation_report.csv")
    raw_prelock = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_prelock_comparison.csv")
    prelock, stale_prelock = split_current_prelock(raw_prelock, target_date)
    drift = read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_drift_monitor_summary.csv")
    if drift.empty:
        drift = read_csv_lenient(processed_dir / "vsigma_drift_monitor_summary.csv")
    extended = read_csv_lenient(processed_dir / "extended_historical" / "vsigma_extended_backtest_summary.csv")
    ledger_dir = processed_dir / "ledger"
    odds_dir = processed_dir / "odds_snapshots"
    immutable_ledger = read_csv_lenient(ledger_dir / "vsigma_immutable_daily_pick_ledger.csv")
    if not immutable_ledger.empty and "target_date" in immutable_ledger.columns:
        ledger_day = immutable_ledger[immutable_ledger["target_date"].astype(str).eq(target_date)].copy()
    else:
        ledger_day = pd.DataFrame()
    ledger_pick_day = ledger_day[
        ~ledger_day.get("record_status", pd.Series(dtype=object)).fillna("").astype(str).eq("NO_BET_RECORD")
    ].copy() if not ledger_day.empty else pd.DataFrame()
    performance = read_csv_lenient(ledger_dir / "vsigma_experiment_performance_summary.csv")
    governance_dir = processed_dir / "governance"
    promotion_governance = read_csv_lenient(governance_dir / "vsigma_promotion_governance_summary.csv")
    threshold_governance = read_csv_lenient(governance_dir / "vsigma_threshold_governance_summary.csv")
    governance_dashboard = snapshot_dir / "vsigma_governance_dashboard.md"
    if not governance_dashboard.exists():
        governance_dashboard = governance_dir / "vsigma_governance_dashboard.md"
    clv_summary = read_csv_lenient(odds_dir / "vsigma_clv_summary.csv")
    clv_day = clv_summary[clv_summary.get("target_date", pd.Series(dtype=object)).astype(str).eq(target_date)].copy() if not clv_summary.empty else pd.DataFrame()
    v7_advice = read_csv_lenient(odds_dir / "vsigma_candidate_v7_calibration_advice.csv")
    ledger_report_path = snapshot_dir / "vsigma_ledger_daily_report.md"
    if not ledger_report_path.exists():
        ledger_report_path = ledger_dir / "vsigma_ledger_daily_report.md"
    controller_status_path = snapshot_dir / "daily_controller_status.md"
    controller_plan_path = snapshot_dir / "daily_run_plan.csv"
    controller_status_text = controller_status_path.read_text(encoding="utf-8") if controller_status_path.exists() else ""
    controller_next_action = "CONTROLLER_STATUS_NOT_AVAILABLE"
    controller_prelock_due = ""
    if controller_status_text:
        for line in controller_status_text.splitlines():
            if line.startswith("- Action:"):
                controller_next_action = line.split(":", 1)[1].strip()
                break
    controller_plan = read_csv_lenient(controller_plan_path)
    if not controller_plan.empty and "prelock_window_start" in controller_plan.columns:
        due_values = [
            str(value).strip()
            for value in controller_plan["prelock_window_start"].dropna().tolist()
            if str(value).strip()
        ]
        controller_prelock_due = min(due_values) if due_values else ""
    supervisor_status_path = snapshot_dir / "daily_supervisor_status.csv"
    supervisor_report_path = snapshot_dir / "daily_supervisor_report.md"
    supervisor_status = read_csv_lenient(supervisor_status_path)
    supervisor_latest_status = "SUPERVISOR_STATUS_NOT_AVAILABLE"
    supervisor_last_mode = ""
    supervisor_last_time = ""
    supervisor_next_action = ""
    supervisor_logs_path = "C:\\vsigma\\automation_logs\\supervisor"
    supervisor_schedule_status = "TASK_STATUS_NOT_DETECTED"
    if not supervisor_status.empty:
        supervisor_row = supervisor_status.iloc[0]
        supervisor_latest_status = str(supervisor_row.get("supervisor_status", ""))
        supervisor_last_mode = str(supervisor_row.get("mode", ""))
        supervisor_last_time = str(supervisor_row.get("run_finished_at", ""))
        supervisor_next_action = str(supervisor_row.get("next_recommended_action", ""))
        supervisor_logs_path = str(supervisor_row.get("logs_path", supervisor_logs_path))
        supervisor_schedule_status = str(supervisor_row.get("scheduled_automation_status", supervisor_schedule_status))
    elif (Path(__file__).resolve().parents[1] / "scripts" / "register_vsigma_windows_tasks.ps1").exists():
        supervisor_schedule_status = "REGISTRATION_SCRIPT_AVAILABLE_STATUS_NOT_QUERIED"
    health_summary = read_csv_lenient(processed_dir / "health" / "vsigma_healthcheck_summary.csv")
    health_report_path = snapshot_dir / "vsigma_healthcheck_report.md"
    if not health_report_path.exists():
        health_report_path = processed_dir / "health" / "vsigma_healthcheck_report.md"
    health_global_status = "HEALTHCHECK_NOT_AVAILABLE"
    health_critical_warning = "NONE"
    health_recovery_command = ""
    if not health_summary.empty:
        if "target_date" in health_summary.columns:
            health_day = health_summary[health_summary["target_date"].astype(str).eq(target_date)].copy()
            if health_day.empty:
                health_day = health_summary.copy()
        else:
            health_day = health_summary.copy()
        if not health_day.empty:
            health_global_status = str(health_day.iloc[0].get("global_health_status", health_global_status))
            critical = health_day[health_day.get("status", pd.Series(dtype=object)).astype(str).isin(["BROKEN", "NEEDS_ATTENTION", "WARNING"])].copy()
            if not critical.empty:
                row = critical.iloc[0]
                health_critical_warning = f"{row.get('check_name', '')}: {row.get('status', '')} - {row.get('detail', '')}"
                health_recovery_command = str(row.get("recovery_command", ""))

    result_summary = build_result_summary_table(
        [
            ("OFFICIAL_EXECUTION_SHORTLIST", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_execution_shortlist_results_summary.csv")),
            ("CANDIDATE_V2", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_results_summary.csv")),
            ("CANDIDATE_V4", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v4_results_summary.csv")),
            ("CANDIDATE_V5", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v5_results_summary.csv")),
            ("CANDIDATE_V6", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v6_results_summary.csv")),
            ("CANDIDATE_V7", read_snapshot_or_processed(processed_dir, snapshot_dir, "vsigma_today_candidate_v7_results_summary.csv")),
        ]
    )

    lines = [
        f"# vSIGMA Daily Competition Master Report - {target_date}",
        "",
        "## Daily Status",
        current_day_status(baseline, result_summary, prelock),
        "",
        "## Official Baseline Top Picks",
        no_bet_text("Official baseline", baseline) or format_markdown_table(baseline, PICK_COLUMNS),
        "",
        "## Candidate v2 Top Picks",
        no_bet_text("Candidate v2", v2) or format_markdown_table(v2, PICK_COLUMNS),
        "",
        "## Candidate v4/v5/v6 Top Picks",
        "### Candidate v4",
        no_bet_text("Candidate v4", v4) or format_markdown_table(v4, PICK_COLUMNS),
        "",
        "### Candidate v5",
        no_bet_text("Candidate v5", v5) or format_markdown_table(v5, PICK_COLUMNS),
        "",
        "### Candidate v6",
        no_bet_text("Candidate v6", v6) or format_markdown_table(v6, PICK_COLUMNS),
        "",
        "### Candidate v7",
        no_bet_text("Candidate v7", v7) or format_markdown_table(v7, PICK_COLUMNS + ["price_discipline_decision"]),
        "",
        "## Match Script Forecasts",
        format_markdown_table(forecasts, max_rows=15),
        "",
        "## Baseline vs Candidate Comparison",
        "### Candidate v2",
        format_markdown_table(comparison_v2, max_rows=15),
        "",
        "### Candidate v4",
        format_markdown_table(comparison_v4, max_rows=15),
        "",
        "### Candidate v5",
        format_markdown_table(comparison_v5, max_rows=15),
        "",
        "### Candidate v6",
        format_markdown_table(comparison_v6, max_rows=15),
        "",
        "### Candidate v7",
        format_markdown_table(comparison_v7, max_rows=15),
        "",
        "## Price Discipline / CLV / Drift Execution Guard",
        format_markdown_table(
            v7_shortlist,
            [
                "fixture_id",
                "home_team",
                "away_team",
                "market_primary",
                "price_discipline_decision",
                "price_discipline_min_edge_required",
                "price_discipline_actual_edge",
                "price_discipline_edge_surplus",
                "price_discipline_drift_status",
                "candidate_v7_prelock_status",
                "candidate_v7_execution_status",
                "clv_direction",
                "price_discipline_reason",
            ],
            max_rows=20,
        ),
        "",
        "## Pre-Lock Execution Status",
        f"- Pre-lock data fresh: {'YES' if not prelock.empty else 'NO_CURRENT_PRELOCK_ROWS'}",
        f"- Stale pre-lock excluded: {'YES' if not stale_prelock.empty else 'NO'}",
        f"- Execution allowed by v7: {int(pd.to_numeric(v7_shortlist.get('candidate_v7_execution_allowed_flag', v7_shortlist.get('price_discipline_execution_allowed_flag', pd.Series(dtype=object))), errors='coerce').fillna(0).eq(1).sum()) if not v7_shortlist.empty else 0}",
        "",
        "### Official Baseline Picks",
        format_markdown_table(
            baseline,
            ["fixture_id", "league", "home_team", "away_team", "market_primary", "accuracy_mode_rank", "competition_calibrated_prob"],
            max_rows=20,
        ),
        "",
        "### Candidate v7 Pre-Lock Status",
        format_markdown_table(
            v7_shortlist,
            [
                "fixture_id",
                "home_team",
                "away_team",
                "market_primary",
                "price_discipline_decision",
                "candidate_v7_prelock_status",
                "candidate_v7_execution_status",
                "candidate_v7_execution_allowed_flag",
                "price_discipline_reason",
            ],
            max_rows=20,
        ),
        "",
        "### Active Pre-Lock Decisions",
        format_markdown_table(
            prelock,
            [
                "fixture_id",
                "home_team",
                "away_team",
                "market_primary",
                "prelock_status",
                "prelock_minutes_to_kickoff",
                "prelock_decision",
                "prelock_decision_reason",
            ],
            max_rows=20,
        ),
        "",
        "### Stale Pre-Lock Warning",
        (
            f"STALE_PRELOCK_EXCLUDED: previous target_date={stale_date_summary(stale_prelock, include_target_date=True)}\n\n"
            + format_markdown_table(
                stale_prelock,
                ["target_date", "date", "fixture_id", "home_team", "away_team", "market_primary", "prelock_status", "prelock_decision"],
                max_rows=20,
            )
            if not stale_prelock.empty
            else "_No stale pre-lock rows excluded._"
        ),
        "",
        "## Odds Snapshot / CLV Calibration",
        "### CLV Summary",
        format_markdown_table(
            clv_day,
            [
                "fixture_id",
                "home_team",
                "away_team",
                "market_primary",
                "experiment_id",
                "pre_price",
                "prelock_price",
                "close_proxy_price",
                "clv_delta",
                "clv_direction",
                "result",
                "profit_units",
            ],
            max_rows=30,
        ),
        "",
        "### Candidate v7 Calibration Advice",
        format_markdown_table(
            v7_advice,
            [
                "market_family",
                "failure_mode",
                "drift_status",
                "clv_direction",
                "n",
                "profit_units",
                "roi_percent",
                "recommendation",
                "recommendation_reason",
            ],
            max_rows=20,
        ),
        "",
        "## Post-Results Summary",
        format_markdown_table(result_summary, SUMMARY_COLUMNS, max_rows=10),
        "",
        "## Pre-Lock Status",
        format_markdown_table(
            prelock,
            [
                "fixture_id",
                "home_team",
                "away_team",
                "market_primary",
                "prelock_status",
                "prelock_minutes_to_kickoff",
                "prelock_decision",
                "prelock_decision_reason",
            ],
            max_rows=15,
        ),
        "",
        "## Drift Monitor Status",
        format_markdown_table(drift, ["pattern", "settled_rows", "wins", "losses", "profit_units", "drift_status"], max_rows=20),
        "",
        "## Baseline vs Candidate Trend",
        format_markdown_table(extended, ["mode", "rows", "settled_rows", "wins", "losses", "profit_units", "roi_percent", "max_drawdown"], max_rows=10),
        "",
        "## Immutable Ledger / Experiment Registry",
        f"- Ledger update status: {'AVAILABLE' if not ledger_day.empty else 'NOT_AVAILABLE'}",
        f"- Official picks registered: {int(ledger_pick_day.get('is_official_pick', pd.Series(dtype=object)).astype(str).eq('1').sum()) if not ledger_pick_day.empty else 0}",
        f"- Shadow picks registered: {int(ledger_pick_day.get('is_shadow_pick', pd.Series(dtype=object)).astype(str).eq('1').sum()) if not ledger_pick_day.empty else 0}",
        f"- No-bet records: {int(ledger_day.get('record_status', pd.Series(dtype=object)).astype(str).eq('NO_BET_RECORD').sum()) if not ledger_day.empty else 0}",
        f"- Ledger report: {ledger_report_path}",
        "",
        "## Daily Controller Status",
        f"- Next recommended action: {controller_next_action}",
        f"- Pre-lock due time: {controller_prelock_due or 'NOT_AVAILABLE'}",
        f"- Status path: {controller_status_path if controller_status_path.exists() else 'NOT_AVAILABLE'}",
        "",
        "## Daily Supervisor",
        f"- Supervisor latest status: {supervisor_latest_status}",
        f"- Last run mode/time: {supervisor_last_mode or 'NOT_AVAILABLE'} / {supervisor_last_time or 'NOT_AVAILABLE'}",
        f"- Next recommended action: {supervisor_next_action or controller_next_action}",
        f"- Scheduled automation status: {supervisor_schedule_status}",
        f"- Logs path: {supervisor_logs_path}",
        f"- Report path: {supervisor_report_path if supervisor_report_path.exists() else 'NOT_AVAILABLE'}",
        "",
        "## Healthcheck",
        f"- Global health status: {health_global_status}",
        f"- Critical warnings: {health_critical_warning}",
        f"- Recovery command: `{health_recovery_command}`" if health_recovery_command else "- Recovery command: ",
        f"- Report path: {health_report_path if health_report_path.exists() else 'NOT_AVAILABLE'}",
        "",
        "### Current Experiment Daily Summary",
        format_markdown_table(
            ledger_day,
            ["experiment_id", "fixture_id", "home_team", "away_team", "market_primary", "prelock_decision", "result", "profit_units", "record_status"],
            max_rows=30,
        ),
        "",
        "### Experiment Performance Summary",
        format_markdown_table(
            performance,
            ["experiment_id", "status", "picks_total", "settled_picks", "wins", "losses", "profit_units", "roi_percent", "current_verdict"],
            max_rows=20,
        ),
        "",
        "## Promotion & Threshold Governance",
        f"- Official baseline status: {'KEEP_OFFICIAL_BASELINE' if not promotion_governance.empty else 'GOVERNANCE_NOT_AVAILABLE'}",
        f"- Governance dashboard: {governance_dashboard}",
        "",
        "### Candidate Promotion Recommendations",
        format_markdown_table(
            promotion_governance,
            ["experiment_id", "settled_picks", "roi_percent", "brier_score", "promotion_recommendation", "required_next_evidence"],
            max_rows=20,
        ),
        "",
        "### Threshold Recommendations",
        format_markdown_table(
            threshold_governance,
            ["market_family", "failure_mode", "experiment_id", "settled_rows", "roi_percent", "clv_direction", "threshold_recommendation"],
            max_rows=20,
        ),
        "",
        f"- CLV data sufficiency: {clv_data_sufficiency(clv_summary)}",
        f"- Drift alerts: {int(threshold_governance.get('threshold_recommendation', pd.Series(dtype=object)).astype(str).isin(['ACTIVE_DRIFT_REVIEW', 'NEEDS_RECALIBRATION', 'WATCH_PATTERN', 'RAISE_MIN_EDGE']).sum()) if not threshold_governance.empty else 0}",
        "",
        "## Failure Mode Summary",
        format_markdown_table(failure_mode_summary([baseline, v2, v4, v5, v6, v7])),
        "",
        "## Freshness Validation",
        format_markdown_table(freshness, ["file_name", "candidate_version", "status", "detail", "rows"], max_rows=30),
        "",
        "## Candidate Isolation",
        format_markdown_table(isolation, ["check_name", "file_name", "status", "detail"], max_rows=30),
        "",
        "## Pre-Lock",
        PRE_LOCK_NOTE,
        "",
    ]
    output_path = snapshot_dir / MASTER_REPORT
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the vSIGMA daily competition master report.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--snapshot-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    snapshot_dir = args.snapshot_dir or TODAY_DIR / target_date
    path = build_master_report(args.processed_dir, target_date, snapshot_dir)
    print(f"Daily competition master report: {path}")


if __name__ == "__main__":
    main()
