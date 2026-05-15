from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

import pandas as pd

try:
    from daily_hardening import (
        PROCESSED_DIR,
        SCOREBOARD_PATH,
        file_rows,
        format_markdown_table,
        parse_float,
        read_csv_lenient,
        split_fresh_stale_rows,
        strip_scoreboard_section,
        summary_value,
    )
except ModuleNotFoundError:
    from scripts.daily_hardening import (
        PROCESSED_DIR,
        SCOREBOARD_PATH,
        file_rows,
        format_markdown_table,
        parse_float,
        read_csv_lenient,
        split_fresh_stale_rows,
        strip_scoreboard_section,
        summary_value,
    )


MODES = [
    ("BASELINE", "OFFICIAL_BASELINE", "vsigma_today_competition_top.csv", "vsigma_execution_shortlist_results_summary.csv", "vsigma_execution_shortlist_results_ledger.csv"),
    ("CANDIDATE_V2", "CANDIDATE_V2_SCHEDULE_ANOMALY", "vsigma_today_candidate_v2_competition_top.csv", "vsigma_today_candidate_v2_results_summary.csv", "vsigma_today_candidate_v2_results_ledger.csv"),
    ("CANDIDATE_V4", "CANDIDATE_V4_O25_FIREWALL", "vsigma_today_candidate_v4_competition_top.csv", "vsigma_today_candidate_v4_results_summary.csv", "vsigma_today_candidate_v4_results_ledger.csv"),
    ("CANDIDATE_V5", "CANDIDATE_V5_PLAYER_IMPACT", "vsigma_today_candidate_v5_competition_top.csv", "vsigma_today_candidate_v5_results_summary.csv", "vsigma_today_candidate_v5_results_ledger.csv"),
    ("CANDIDATE_V6", "CANDIDATE_V6_API_PREDICTIONS", "vsigma_today_candidate_v6_competition_top.csv", "vsigma_today_candidate_v6_results_summary.csv", "vsigma_today_candidate_v6_results_ledger.csv"),
]


def ledger_pending_count(path: Path) -> int:
    df = read_csv_lenient(path)
    if df.empty or "ledger_result_status" not in df.columns:
        return 0
    return int(df["ledger_result_status"].astype(str).str.upper().eq("PENDING").sum())


def immutable_ledger_summary(processed_dir: Path, target_date: str, mode: str, experiment_id: str, top_file: str) -> dict[str, object] | None:
    ledger = read_csv_lenient(processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv")
    if ledger.empty or "target_date" not in ledger.columns or "experiment_id" not in ledger.columns:
        return None
    rows = ledger[
        ledger["target_date"].astype(str).eq(target_date)
        & ledger["experiment_id"].astype(str).eq(experiment_id)
    ].copy()
    if rows.empty:
        return None
    picks = rows[~rows.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy()
    result = picks.get("result", pd.Series(dtype=object)).astype(str).str.upper()
    profit = pd.to_numeric(picks.get("profit_units", pd.Series(dtype=object)), errors="coerce")
    pending = int(picks.get("record_status", pd.Series(dtype=object)).astype(str).isin({"PRE_REGISTERED", "PRELOCK_UPDATED", "PENDING"}).sum()) if not picks.empty else 0
    settled = int(picks.get("record_status", pd.Series(dtype=object)).astype(str).isin({"SETTLED", "VOID"}).sum()) if not picks.empty else 0
    profit_total = round(float(profit.sum(skipna=True)), 6) if not profit.empty else 0.0
    roi = round((profit_total / settled) * 100.0, 6) if settled else ""
    return {
        "mode": mode,
        "top_file": top_file,
        "picks": int(len(picks)),
        "post_summary_present": 1,
        "wins": int(result.eq("WIN").sum()) if not result.empty else 0,
        "losses": int(result.eq("LOSS").sum()) if not result.empty else 0,
        "profit": profit_total,
        "roi": roi,
        "pending": pending,
        "settled": settled,
        "status": "NO_BET" if picks.empty else "PICKS_AVAILABLE",
    }


def mode_summary(processed_dir: Path, target_date: str, mode: str, experiment_id: str, top_file: str, summary_file: str, ledger_file: str) -> dict[str, object]:
    from_immutable = immutable_ledger_summary(processed_dir, target_date, mode, experiment_id, top_file)
    if from_immutable is not None:
        return from_immutable
    top_path = processed_dir / top_file
    top_rows = file_rows(top_path)
    summary = read_csv_lenient(processed_dir / summary_file)
    pick_count = int(parse_float(summary_value(summary, "pick_count", top_rows or 0), top_rows or 0))
    if mode == "BASELINE" and top_rows is not None:
        pick_count = int(top_rows)

    wins = int(parse_float(summary_value(summary, "wins", summary_value(summary, "win_rows", 0)), 0))
    losses = int(parse_float(summary_value(summary, "losses", summary_value(summary, "loss_rows", 0)), 0))
    profit = parse_float(
        summary_value(summary, "profit_units", summary_value(summary, "profit_units_total", 0.0)),
        0.0,
    )
    roi = summary_value(summary, "roi_percent", "")
    pending = ledger_pending_count(processed_dir / ledger_file)
    settled = wins + losses
    return {
        "mode": mode,
        "top_file": top_file,
        "picks": int(top_rows or 0),
        "post_summary_present": int(not summary.empty),
        "wins": wins,
        "losses": losses,
        "profit": round(profit, 6),
        "roi": roi,
        "pending": pending,
        "settled": settled,
        "status": "NO_BET" if int(top_rows or 0) == 0 else "PICKS_AVAILABLE",
    }


def determine_day_winner(rows: list[dict[str, object]]) -> str:
    if all(int(row["picks"]) == 0 for row in rows):
        return "NO_BET_DAY"
    comparable = [row for row in rows if row["mode"] in {"BASELINE", "CANDIDATE_V2", "CANDIDATE_V4"} and int(row["settled"]) > 0]
    if not comparable:
        return "NO_SETTLED_RESULTS"
    best_profit = max(parse_float(row["profit"]) for row in comparable)
    winners = [row["mode"] for row in comparable if parse_float(row["profit"]) == best_profit]
    if len(winners) != 1:
        return "TIE"
    return str(winners[0])


def prelock_status(processed_dir: Path, target_date: str) -> str:
    df = read_csv_lenient(processed_dir / "vsigma_today_prelock_comparison.csv")
    if df.empty or "prelock_status" not in df.columns:
        return "PRE_LOCK_PENDING"
    df, stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    if df.empty and not stale.empty:
        return "STALE_PRELOCK_EXCLUDED"
    if df["prelock_status"].astype(str).eq("IN_PRELOCK_WINDOW").any():
        decisions = df.get("prelock_decision", pd.Series("", index=df.index)).astype(str).value_counts().to_dict()
        return "; ".join(f"{key}:{value}" for key, value in decisions.items())
    return "PRE_LOCK_NOT_AVAILABLE"


def drift_status(processed_dir: Path) -> str:
    df = read_csv_lenient(processed_dir / "vsigma_drift_monitor_summary.csv")
    if df.empty or "drift_status" not in df.columns:
        return "DRIFT_NOT_RUN"
    counts = df["drift_status"].astype(str).value_counts().to_dict()
    return "; ".join(f"{key}:{value}" for key, value in counts.items())


def governance_status(processed_dir: Path) -> dict[str, str]:
    governance_dir = processed_dir / "governance"
    promotion = read_csv_lenient(governance_dir / "vsigma_promotion_governance_summary.csv")
    threshold = read_csv_lenient(governance_dir / "vsigma_threshold_governance_summary.csv")
    if promotion.empty:
        promotion_status = "GOVERNANCE_NOT_RUN"
    else:
        recs = promotion.get("promotion_recommendation", pd.Series(dtype=object)).astype(str).value_counts().to_dict()
        promotion_status = "; ".join(f"{key}:{value}" for key, value in recs.items())
    if threshold.empty:
        threshold_status = "THRESHOLD_GOVERNANCE_NOT_RUN"
    else:
        recs = threshold.get("threshold_recommendation", pd.Series(dtype=object)).astype(str).value_counts().head(5).to_dict()
        threshold_status = "; ".join(f"{key}:{value}" for key, value in recs.items())
    major = threshold[
        threshold.get("threshold_recommendation", pd.Series(dtype=object)).astype(str).isin(
            ["ACTIVE_DRIFT_REVIEW", "NEEDS_RECALIBRATION", "RAISE_MIN_EDGE", "SECONDARY_ONLY"]
        )
    ].copy() if not threshold.empty else pd.DataFrame()
    if major.empty:
        major_alerts = "none"
    else:
        major_alerts = "; ".join(
            f"{row.get('market_family', '')}+{row.get('failure_mode', '')}:{row.get('threshold_recommendation', '')}"
            for _, row in major.head(5).iterrows()
        )
    return {
        "promotion_status": promotion_status,
        "threshold_status": threshold_status,
        "major_alerts": major_alerts,
    }


def build_scoreboard_section(processed_dir: Path, target_date: str) -> str:
    rows = [mode_summary(processed_dir, target_date, *mode) for mode in MODES]
    winner = determine_day_winner(rows)
    governance = governance_status(processed_dir)
    table = format_markdown_table(
        pd.DataFrame(rows),
        ["mode", "status", "picks", "wins", "losses", "profit", "roi", "pending", "top_file"],
    )
    no_bet_modes = [row["mode"] for row in rows if row["status"] == "NO_BET"]
    lines = [
        f"<!-- VSIGMA_SCOREBOARD_START {target_date} -->",
        f"## {target_date}",
        "",
        f"- Winner: {winner}",
        f"- Governance daily winner: {winner}",
        f"- Promotion status: {governance['promotion_status']}",
        f"- Threshold alerts: {governance['threshold_status']}",
        f"- Major drift/threshold alerts: {governance['major_alerts']}",
        f"- NO BET modes: {', '.join(no_bet_modes) if no_bet_modes else 'none'}",
        f"- Pre-lock: {prelock_status(processed_dir, target_date)}",
        f"- Drift: {drift_status(processed_dir)}",
        "- Failure modes: see daily master report for pick-level risks.",
        "",
        table,
        f"<!-- VSIGMA_SCOREBOARD_END {target_date} -->",
    ]
    return "\n".join(lines)


def update_scoreboard(
    processed_dir: Path = PROCESSED_DIR,
    target_date: str | None = None,
    scoreboard_path: Path = SCOREBOARD_PATH,
) -> Path:
    target_date = target_date or date.today().isoformat()
    section = build_scoreboard_section(processed_dir, target_date)
    scoreboard_path.parent.mkdir(parents=True, exist_ok=True)
    existing = scoreboard_path.read_text(encoding="utf-8") if scoreboard_path.exists() else "# vSIGMA Competition Scoreboard\n"
    cleaned = strip_scoreboard_section(existing, target_date)
    content = f"{cleaned.rstrip()}\n\n{section}\n"
    scoreboard_path.write_text(content, encoding="utf-8")
    return scoreboard_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the vSIGMA daily competition scoreboard.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--scoreboard-path", type=Path, default=SCOREBOARD_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_date = pd.Timestamp(args.date).date().isoformat()
    path = update_scoreboard(args.processed_dir, target_date, args.scoreboard_path)
    print(f"Competition scoreboard: {path}")


if __name__ == "__main__":
    main()
