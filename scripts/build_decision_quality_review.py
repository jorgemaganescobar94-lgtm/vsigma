from __future__ import annotations

import argparse
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

OUTPUT_COLUMNS = [
    "target_date",
    "generated_at",
    "ledger_id",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "official_action",
    "executable_now",
    "final_block_reason",
    "execution_family_status",
    "is_actionable",
    "is_non_actionable",
    "is_expired",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
    "result_status",
    "result_source",
    "decision_quality_label",
    "quality_bucket",
    "quality_reason",
    "improvement_signal",
    "recommended_followup",
]

RESULT_COLUMNS = [
    "result",
    "market_result",
    "bet_result",
    "outcome",
    "final_result",
    "grade",
    "status",
    "market_primary_result",
    "selection_result",
    "primary_result",
    "actionable_result",
]

WIN_VALUES = {"WIN", "WON", "HIT", "GREEN", "✅", "TRUE", "SUCCESS"}
LOSS_VALUES = {"LOSS", "LOST", "MISS", "RED", "❌", "FALSE", "FAIL", "FAILED"}
VOID_VALUES = {"PUSH", "VOID", "NULL", "CANCELLED", "CANCELED", "REFUND", "REFUNDED", "NO_ACTION"}
UNRESOLVED_VALUES = {
    "",
    "NA",
    "N/A",
    "NONE",
    "NAN",
    "NS",
    "TBD",
    "PENDING",
    "SKIPPED",
    "UNKNOWN",
    "UNRESOLVED",
    "OPEN",
    "NOT_AVAILABLE",
    "RESULT_PENDING",
}


@dataclass(frozen=True)
class DecisionQualityPaths:
    governance_md: Path
    governance_csv: Path
    today_md: Path
    today_csv: Path


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def yes_no(value: bool) -> str:
    return "YES" if value else "NO"


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def target_date_rows(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    fresh, _stale = split_fresh_stale_rows(df, target_date, include_target_date=True)
    if not fresh.empty:
        return fresh.reset_index(drop=True)
    for column in ["target_date", "date", "fixture_date", "match_date"]:
        if column in df.columns:
            return df[df[column].astype(str).str[:10].eq(target_date)].copy().reset_index(drop=True)
    return df.copy().reset_index(drop=True)


def first_available(row: pd.Series | dict[str, object] | None, columns: Iterable[str]) -> object:
    if row is None:
        return ""
    for column in columns:
        if column in row and norm_text(row.get(column)):
            return row.get(column)
    return ""


def row_key(row: pd.Series | dict[str, object]) -> tuple[str, str]:
    return (norm_text(row.get("fixture_id")), norm_upper(row.get("market_primary")))


def normalize_result(value: object) -> str:
    raw = norm_upper(value)
    if raw in WIN_VALUES:
        return "WIN"
    if raw in LOSS_VALUES:
        return "LOSS"
    if raw in VOID_VALUES:
        return "VOID"
    if raw in UNRESOLVED_VALUES:
        return "UNRESOLVED"
    compact = raw.replace(" ", "_").replace("-", "_")
    if compact in WIN_VALUES:
        return "WIN"
    if compact in LOSS_VALUES:
        return "LOSS"
    if compact in VOID_VALUES:
        return "VOID"
    if compact in UNRESOLVED_VALUES:
        return "UNRESOLVED"
    return "UNRESOLVED"


def result_from_row(row: pd.Series, source_label: str) -> tuple[str, str]:
    for column in RESULT_COLUMNS:
        if column not in row.index:
            continue
        status = normalize_result(row.get(column))
        if status != "UNRESOLVED":
            return status, f"{source_label}:{column}"
    return "UNRESOLVED", source_label


def build_result_index(sources: list[tuple[str, pd.DataFrame]], target_date: str) -> dict[tuple[str, str], tuple[str, str]]:
    index: dict[tuple[str, str], tuple[str, str]] = {}
    unresolved_seen: dict[tuple[str, str], str] = {}
    for source_label, df in sources:
        current = target_date_rows(df, target_date)
        if current.empty or "fixture_id" not in current.columns or "market_primary" not in current.columns:
            continue
        for _, row in current.iterrows():
            key = row_key(row)
            if not key[0] or not key[1]:
                continue
            status, result_source = result_from_row(row, source_label)
            if status != "UNRESOLVED" and key not in index:
                index[key] = (status, result_source)
            elif key not in unresolved_seen:
                unresolved_seen[key] = result_source
    for key, result_source in unresolved_seen.items():
        index.setdefault(key, ("UNRESOLVED", result_source))
    return index


def classify_decision_quality(
    *,
    official_action: object,
    result_status: object,
    final_block_reason: object = "",
    execution_family_status: object = "",
    is_expired: object = "",
) -> tuple[str, str]:
    action = norm_upper(official_action)
    result = normalize_result(result_status)
    expired = (
        norm_upper(final_block_reason) == "KICKOFF_ALREADY_PASSED"
        or norm_upper(execution_family_status) == "EXPIRED"
        or norm_upper(is_expired) == "YES"
    )

    if action == "EXECUTABLE":
        if result == "WIN":
            label = "ACTIONABLE_WIN"
        elif result == "LOSS":
            label = "ACTIONABLE_LOSS"
        elif result == "VOID":
            label = "ACTIONABLE_VOID"
        else:
            label = "ACTIONABLE_UNRESOLVED"
    elif action == "NO_BET":
        if result == "WIN":
            label = "NO_BET_MISSED_WIN"
        elif result == "LOSS":
            label = "NO_BET_CORRECT_AVOIDED_LOSS"
        elif result == "VOID":
            label = "NO_BET_NEUTRAL_VOID"
        else:
            label = "NO_BET_UNRESOLVED"
    elif action == "WAIT":
        if result == "WIN" and expired:
            label = "WAIT_MISSED_WIN"
        elif result == "LOSS" and expired:
            label = "WAIT_CORRECT_AVOIDED_LOSS"
        elif result == "WIN":
            label = "WAIT_MISSED_WIN"
        elif result == "LOSS":
            label = "WAIT_CORRECT_AVOIDED_LOSS"
        elif result == "VOID":
            label = "WAIT_NEUTRAL_VOID"
        else:
            label = "WAIT_UNRESOLVED"
    elif action == "TECHNICAL_REVIEW":
        label = "TECHNICAL_REVIEW_RESULT_KNOWN" if result in {"WIN", "LOSS", "VOID"} else "TECHNICAL_REVIEW_UNRESOLVED"
    else:
        label = "UNRESOLVED" if result == "UNRESOLVED" else f"{action or 'UNKNOWN'}_RESULT_KNOWN"

    return label, quality_bucket_for_label(label)


def quality_bucket_for_label(label: str) -> str:
    if label.startswith("TECHNICAL_REVIEW"):
        return "TECHNICAL_REVIEW"
    if "UNRESOLVED" in label:
        return "NEEDS_MORE_DATA"
    if label in {"ACTIONABLE_WIN", "NO_BET_CORRECT_AVOIDED_LOSS", "WAIT_CORRECT_AVOIDED_LOSS"}:
        return "GOOD_DECISION"
    if label in {"ACTIONABLE_LOSS", "NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"}:
        return "BAD_DECISION"
    if "VOID" in label or "PUSH" in label:
        return "NEUTRAL_OR_UNRESOLVED"
    return "NEUTRAL_OR_UNRESOLVED"


def improvement_signal_for(row: pd.Series, label: str, result_source: str) -> str:
    final_block_reason = norm_upper(row.get("final_block_reason"))
    market = norm_upper(row.get("market_primary"))
    risk = norm_upper(row.get("accuracy_primary_risk"))
    if not result_source:
        return "IMPROVE_POST_RESULT_LABELING"
    if "UNRESOLVED" in label:
        return "WAIT_FOR_POST_RESULTS"
    if label == "NO_BET_CORRECT_AVOIDED_LOSS":
        return "PRELOCK_BLOCKING_HELPFUL"
    if label in {"NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"}:
        if "PRELOCK_NOT_AVAILABLE" in final_block_reason:
            return "REVIEW_PRELOCK_STRICTNESS"
        if final_block_reason == "KICKOFF_ALREADY_PASSED":
            return "REVIEW_AUTO_TIMING"
        return "REVIEW_NON_ACTIONABLE_BLOCK"
    if label == "ACTIONABLE_LOSS" and market == "OVER_1_5" and "LOW_CONVERSION" in risk:
        return "REVIEW_OVER15_LOW_CONVERSION_SHRINKAGE"
    if label == "ACTIONABLE_LOSS":
        return "REVIEW_ACTIONABLE_MARKET_RISK"
    return "MONITOR_DECISION_QUALITY"


def quality_reason_for(row: pd.Series, label: str, result_status: str) -> str:
    action = norm_upper(row.get("official_action")) or "UNKNOWN"
    reason = norm_upper(row.get("final_block_reason")) or "NONE"
    if "UNRESOLVED" in label:
        return f"{action} decision cannot be graded yet; result_status={result_status}."
    if label == "ACTIONABLE_WIN":
        return "Executable official decision won after result labeling."
    if label == "ACTIONABLE_LOSS":
        return "Executable official decision lost after result labeling."
    if label == "NO_BET_MISSED_WIN":
        return f"System blocked a market that later won; block_reason={reason}."
    if label == "NO_BET_CORRECT_AVOIDED_LOSS":
        return f"System blocked a market that later lost; block_reason={reason}."
    if label.startswith("WAIT_"):
        return f"WAIT decision resolved with result_status={result_status}; block_reason={reason}."
    if label.startswith("TECHNICAL_REVIEW"):
        return f"Technical review row; result_status={result_status}."
    return f"Decision quality label={label}; result_status={result_status}."


def followup_for(label: str, signal: str) -> str:
    if signal == "WAIT_FOR_POST_RESULTS":
        return "Run POST results labeling when finished scores are available."
    if signal == "IMPROVE_POST_RESULT_LABELING":
        return "Verify result label columns and POST output availability."
    if signal == "REVIEW_PRELOCK_STRICTNESS":
        return "Review PRELOCK_NOT_AVAILABLE blocking once at least 3 missed wins share the same cause."
    if signal == "REVIEW_AUTO_TIMING":
        return "Review AUTO/PRELOCK scheduling so decisions resolve before kickoff."
    if signal == "REVIEW_OVER15_LOW_CONVERSION_SHRINKAGE":
        return "Collect sample and review OVER_1_5 low-conversion loss pattern; do not auto-change scoring."
    if signal == "PRELOCK_BLOCKING_HELPFUL":
        return "Keep block evidence separated from actionable results."
    if "UNRESOLVED" in label:
        return "Keep decision in unresolved quality bucket."
    return "Monitor in daily decision quality sample."


def build_quality_rows(
    ledger_rows: pd.DataFrame,
    result_index: dict[tuple[str, str], tuple[str, str]],
    target_date: str,
    generated_at: str,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, ledger_row in ledger_rows.iterrows():
        key = row_key(ledger_row)
        result_status, result_source = result_index.get(key, ("UNRESOLVED", ""))
        final_block_reason = norm_upper(ledger_row.get("final_block_reason"))
        is_expired = yes_no(
            norm_upper(ledger_row.get("is_expired")) == "YES"
            or final_block_reason == "KICKOFF_ALREADY_PASSED"
            or norm_upper(ledger_row.get("execution_family_status")) == "EXPIRED"
        )
        label, bucket = classify_decision_quality(
            official_action=ledger_row.get("official_action"),
            result_status=result_status,
            final_block_reason=final_block_reason,
            execution_family_status=ledger_row.get("execution_family_status"),
            is_expired=is_expired,
        )
        signal = improvement_signal_for(ledger_row, label, result_source)
        rows.append(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "ledger_id": norm_text(ledger_row.get("ledger_id")),
                "fixture_id": norm_text(ledger_row.get("fixture_id")),
                "league": norm_text(ledger_row.get("league")),
                "home_team": norm_text(ledger_row.get("home_team")),
                "away_team": norm_text(ledger_row.get("away_team")),
                "market_primary": norm_upper(ledger_row.get("market_primary")),
                "official_action": norm_upper(ledger_row.get("official_action")),
                "executable_now": norm_upper(ledger_row.get("executable_now")),
                "final_block_reason": final_block_reason,
                "execution_family_status": norm_upper(ledger_row.get("execution_family_status")),
                "is_actionable": norm_upper(ledger_row.get("is_actionable")) or "NO",
                "is_non_actionable": norm_upper(ledger_row.get("is_non_actionable")) or "YES",
                "is_expired": is_expired,
                "competition_calibrated_prob": ledger_row.get("competition_calibrated_prob", ""),
                "accuracy_confidence_score": ledger_row.get("accuracy_confidence_score", ""),
                "accuracy_primary_risk": norm_text(ledger_row.get("accuracy_primary_risk")),
                "result_status": result_status,
                "result_source": result_source,
                "decision_quality_label": label,
                "quality_bucket": bucket,
                "quality_reason": quality_reason_for(ledger_row, label, result_status),
                "improvement_signal": signal,
                "recommended_followup": followup_for(label, signal),
            }
        )
    return pd.DataFrame(rows, columns=OUTPUT_COLUMNS)


def count_label(df: pd.DataFrame, label: str) -> int:
    if df.empty or "decision_quality_label" not in df.columns:
        return 0
    return int(df["decision_quality_label"].astype(str).eq(label).sum())


def top_value(df: pd.DataFrame, column: str, default: str = "NONE") -> str:
    if df.empty or column not in df.columns:
        return default
    values = df[column].dropna().astype(str).str.strip()
    values = values[values.ne("")]
    if values.empty:
        return default
    counts = values.value_counts()
    return f"{counts.index[0]} ({int(counts.iloc[0])})"


def market_recommendation(group: pd.DataFrame) -> str:
    rows = len(group)
    actionable_losses = int(group["decision_quality_label"].astype(str).eq("ACTIONABLE_LOSS").sum())
    missed = int(group["decision_quality_label"].astype(str).isin(["NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"]).sum())
    unresolved = int(group["quality_bucket"].astype(str).eq("NEEDS_MORE_DATA").sum())
    if rows and unresolved == rows:
        return "WAIT_FOR_POST_RESULTS"
    if actionable_losses >= 3:
        return "REVIEW_MARKET_RISK_AFTER_SAMPLE"
    if missed >= 3:
        return "REVIEW_BLOCKING_CAUSE_AFTER_SAMPLE"
    return "MONITOR"


def system_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    resolved = int((~df["result_status"].astype(str).eq("UNRESOLVED")).sum()) if not df.empty else 0
    unresolved = int(df["result_status"].astype(str).eq("UNRESOLVED").sum()) if not df.empty else 0

    def add(priority: str, category: str, title: str, reason: str, apply_now: str = "NO") -> None:
        rows.append(
            {
                "priority": priority,
                "category": category,
                "title": title,
                "reason": reason,
                "apply_now": apply_now,
            }
        )

    if resolved < 30:
        add("P3", "sample", "Do not recalibrate from quality sample yet", f"resolved_rows={resolved} is below minimum 30.")
    if unresolved > resolved:
        add("P3", "post_results", "Wait for POST results or improve labeling", f"unresolved_rows={unresolved}; resolved_rows={resolved}.")

    if not df.empty:
        missed = df[df["decision_quality_label"].astype(str).isin(["NO_BET_MISSED_WIN", "WAIT_MISSED_WIN"])]
        if not missed.empty and "final_block_reason" in missed.columns:
            for reason, count in missed["final_block_reason"].astype(str).value_counts().items():
                if int(count) >= 3:
                    add("P1", "execution", f"Review missed wins blocked by {reason}", f"{count} missed wins share final_block_reason={reason}.")
        losses = df[df["decision_quality_label"].astype(str).eq("ACTIONABLE_LOSS")]
        if not losses.empty:
            group_cols = ["market_primary", "accuracy_primary_risk"]
            for (market, risk), group in losses.groupby(group_cols, dropna=False):
                if len(group) >= 3:
                    add("P2", "model_market_review", f"Review actionable losses in {market}", f"{len(group)} losses share market={market} and risk={risk}.")
        if count_label(df, "NO_BET_CORRECT_AVOIDED_LOSS") > 0:
            add("P2", "execution", "Track helpful blocking evidence", "NO_BET rows avoided at least one labeled loss.")

    if not rows:
        add("P3", "monitoring", "Continue collecting decision quality evidence", "No aggregate review trigger reached.")

    return pd.DataFrame(rows, columns=["priority", "category", "title", "reason", "apply_now"])


def build_markdown(df: pd.DataFrame, target_date: str, generated_at: str) -> str:
    rows_reviewed = len(df)
    actionable = int(df["is_actionable"].astype(str).eq("YES").sum()) if not df.empty else 0
    non_actionable = int(df["is_non_actionable"].astype(str).eq("YES").sum()) if not df.empty else 0
    resolved = int((~df["result_status"].astype(str).eq("UNRESOLVED")).sum()) if not df.empty else 0
    unresolved = int(df["result_status"].astype(str).eq("UNRESOLVED").sum()) if not df.empty else 0
    good = int(df["quality_bucket"].astype(str).eq("GOOD_DECISION").sum()) if not df.empty else 0
    bad = int(df["quality_bucket"].astype(str).eq("BAD_DECISION").sum()) if not df.empty else 0
    neutral = int(df["quality_bucket"].astype(str).isin(["NEUTRAL_OR_UNRESOLVED", "NEEDS_MORE_DATA"]).sum()) if not df.empty else 0
    top_signal = top_value(df, "improvement_signal")
    current_recommendation = "Do not recalibrate; collect more labeled outcomes." if resolved < 30 else "Review aggregate quality signals; do not auto-apply scoring changes."

    table = df.copy()
    if not table.empty:
        table["fixture"] = table["home_team"].astype(str) + " vs " + table["away_team"].astype(str)
    else:
        table = pd.DataFrame(columns=[*OUTPUT_COLUMNS, "fixture"])

    block_rows = [
        f"- NO_BET_MISSED_WIN count: {count_label(df, 'NO_BET_MISSED_WIN')}",
        f"- NO_BET_CORRECT_AVOIDED_LOSS count: {count_label(df, 'NO_BET_CORRECT_AVOIDED_LOSS')}",
        f"- WAIT_MISSED_WIN count: {count_label(df, 'WAIT_MISSED_WIN')}",
        f"- WAIT_CORRECT_AVOIDED_LOSS count: {count_label(df, 'WAIT_CORRECT_AVOIDED_LOSS')}",
        f"- PRELOCK_NOT_AVAILABLE rows: {int(df['final_block_reason'].astype(str).str.contains('PRELOCK_NOT_AVAILABLE', regex=False).sum()) if not df.empty else 0}",
        f"- KICKOFF_ALREADY_PASSED rows: {int(df['final_block_reason'].astype(str).eq('KICKOFF_ALREADY_PASSED').sum()) if not df.empty else 0}",
    ]

    market_rows: list[dict[str, object]] = []
    if not df.empty:
        for market, group in df.groupby("market_primary", dropna=False):
            market_rows.append(
                {
                    "market_primary": market,
                    "rows": len(group),
                    "wins": int(group["result_status"].astype(str).eq("WIN").sum()),
                    "losses": int(group["result_status"].astype(str).eq("LOSS").sum()),
                    "no_bet_missed_win": int(group["decision_quality_label"].astype(str).eq("NO_BET_MISSED_WIN").sum()),
                    "no_bet_correct_avoided_loss": int(group["decision_quality_label"].astype(str).eq("NO_BET_CORRECT_AVOIDED_LOSS").sum()),
                    "unresolved": int(group["result_status"].astype(str).eq("UNRESOLVED").sum()),
                    "recommendation": market_recommendation(group),
                }
            )
    market_df = pd.DataFrame(
        market_rows,
        columns=[
            "market_primary",
            "rows",
            "wins",
            "losses",
            "no_bet_missed_win",
            "no_bet_correct_avoided_loss",
            "unresolved",
            "recommendation",
        ],
    )

    recommendation_df = system_recommendations(df)
    lines = [
        f"# vSIGMA Decision Quality Review - {target_date}",
        "",
        "## Executive Summary",
        f"- generated_at: {generated_at}",
        f"- rows reviewed: {rows_reviewed}",
        f"- actionable rows: {actionable}",
        f"- non-actionable rows: {non_actionable}",
        f"- resolved rows: {resolved}",
        f"- unresolved rows: {unresolved}",
        f"- good decisions: {good}",
        f"- bad decisions: {bad}",
        f"- neutral/unresolved: {neutral}",
        f"- top improvement signal: {top_signal}",
        f"- current recommendation: {current_recommendation}",
        "",
        "## Decision Quality Table",
        format_markdown_table(
            table,
            [
                "fixture",
                "market_primary",
                "official_action",
                "final_block_reason",
                "result_status",
                "decision_quality_label",
                "quality_bucket",
                "improvement_signal",
            ],
            max_rows=100,
        ),
        "",
        "## Block Quality Review",
        *block_rows,
        "",
        "## Market Quality Review",
        format_markdown_table(market_df, list(market_df.columns), max_rows=100),
        "",
        "## System Recommendations",
        format_markdown_table(recommendation_df, list(recommendation_df.columns), max_rows=50),
        "",
        "## Guardrails",
        "- automatic scoring changes applied: NO",
        "- threshold changes applied: NO",
        "- calibration changes applied: NO",
        "",
    ]
    return "\n".join(lines)


def build_decision_quality_review(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = PROCESSED_DIR,
    now: datetime | None = None,
) -> tuple[pd.DataFrame, DecisionQualityPaths]:
    target_date = pd.Timestamp(target_date).date().isoformat()
    timezone = ZoneInfo(timezone_name)
    now = now.astimezone(timezone) if now is not None else datetime.now(timezone)
    generated_at = now.isoformat(timespec="seconds")
    snap = snapshot_dir(processed_dir, target_date)
    governance_dir = processed_dir / "governance"
    governance_dir.mkdir(parents=True, exist_ok=True)
    snap.mkdir(parents=True, exist_ok=True)

    decision_ledger = read_csv_lenient(processed_dir / "ledger" / "vsigma_decision_outcome_ledger.csv")
    immutable_ledger = read_csv_lenient(processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv")
    today_labeled = read_csv_lenient(snap / "vsigma_market_results_labeled.csv")
    global_labeled = read_csv_lenient(processed_dir / "vsigma_market_results_labeled.csv")
    read_csv_lenient(snap / "vsigma_cloud_decision_summary.csv")
    read_csv_lenient(snap / "vsigma_prelock_decision_resolver.csv")
    read_csv_lenient(snap / "vsigma_today_competition_top.csv")

    ledger_rows = target_date_rows(decision_ledger, target_date)
    if not ledger_rows.empty and "fixture_id" in ledger_rows.columns:
        ledger_rows = ledger_rows[ledger_rows["fixture_id"].fillna("").astype(str).str.strip().ne("")].copy().reset_index(drop=True)

    result_sources = [
        (str(snap / "vsigma_market_results_labeled.csv"), today_labeled),
        (str(processed_dir / "vsigma_market_results_labeled.csv"), global_labeled),
        (str(processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv"), immutable_ledger),
    ]
    result_index = build_result_index(result_sources, target_date)
    review = build_quality_rows(ledger_rows, result_index, target_date, generated_at)

    paths = DecisionQualityPaths(
        governance_md=governance_dir / "vsigma_decision_quality_review.md",
        governance_csv=governance_dir / "vsigma_decision_quality_review.csv",
        today_md=snap / "vsigma_decision_quality_review.md",
        today_csv=snap / "vsigma_decision_quality_review.csv",
    )
    markdown = build_markdown(review, target_date, generated_at)
    review.to_csv(paths.governance_csv, index=False)
    review.to_csv(paths.today_csv, index=False)
    paths.governance_md.write_text(markdown, encoding="utf-8")
    paths.today_md.write_text(markdown, encoding="utf-8")
    return review, paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA decision quality review from official decisions and labeled results.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        review, paths = build_decision_quality_review(args.date, args.timezone, args.processed_dir)
    except Exception as exc:
        print(f"ERROR: decision quality review failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("=== VSIGMA DECISION QUALITY REVIEW ===")
    print(f"Rows: {len(review)}")
    print(f"Governance MD: {paths.governance_md}")
    print(f"Governance CSV: {paths.governance_csv}")
    print(f"Today MD: {paths.today_md}")
    print(f"Today CSV: {paths.today_csv}")


if __name__ == "__main__":
    main()
