from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient


ROOT = Path(__file__).resolve().parents[1]

REVIEW_COLUMNS = [
    "target_date",
    "priority",
    "category",
    "title",
    "reason",
    "expected_impact",
    "risk",
    "recommended_action",
    "apply_now",
    "evidence",
]

DECISION_COLUMNS = [
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "official_action",
    "executable_now",
    "final_block_reason",
    "retry_allowed",
    "next_retry_time",
    "data_gap_flags",
    "execution_family_status",
    "decision_state",
    "exclusion_reason",
    "next_action",
]

SIDE_MARKETS = {
    "HOME_WIN",
    "AWAY_WIN",
    "DRAW",
    "HOME_DNB",
    "AWAY_DNB",
    "DNB",
    "1X",
    "X2",
    "12",
    "HOME_DOUBLE_CHANCE",
    "AWAY_DOUBLE_CHANCE",
}


@dataclass(frozen=True)
class ReviewPaths:
    governance_md: Path
    governance_csv: Path
    today_md: Path


def norm_text(value: object) -> str:
    if value is None or pd.isna(value):
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_int(value: object, default: int = 0) -> int:
    try:
        if value is None or pd.isna(value):
            return default
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def read_text_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def snapshot_dir(processed_dir: Path, target_date: str) -> Path:
    return processed_dir / "today" / target_date


def csv_path_rows(path: Path) -> int:
    if not path.exists():
        return 0
    return int(len(read_csv_lenient(path)))


def first_existing_frame(paths: Iterable[Path]) -> pd.DataFrame:
    for path in paths:
        if path.exists():
            return read_csv_lenient(path)
    return pd.DataFrame()


def parse_bullet_value(text: str, label: str, default: str = "UNKNOWN") -> str:
    pattern = re.compile(rf"^\s*-\s*{re.escape(label)}:\s*(.+?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else default


def decision_candidate_count(decisions: pd.DataFrame) -> int:
    if decisions.empty:
        return 0
    if "final_block_reason" in decisions.columns:
        reasons = set(decisions.get("final_block_reason", pd.Series("", index=decisions.index)).astype(str))
        if reasons and reasons.issubset({"NO_CANDIDATES"}):
            return 0
    states = set(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str))
    if states and states.issubset({"NO_BET", "PAST_DATE_NO_PRE_REFRESH"}):
        return 0
    return int(len(decisions))


def target_date_rows(df: pd.DataFrame, target_date: str) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    for column in ["target_date", "date", "fixture_date", "match_date"]:
        if column in df.columns:
            mask = df[column].astype(str).str[:10].eq(target_date)
            return df[mask].copy().reset_index(drop=True)
    return df.copy().reset_index(drop=True)


def ledger_closed_mask(ledger: pd.DataFrame) -> pd.Series:
    if ledger.empty:
        return pd.Series(dtype=bool)
    result_status = ledger.get("result_status", pd.Series("", index=ledger.index)).astype(str).str.upper()
    record_status = ledger.get("record_status", pd.Series("", index=ledger.index)).astype(str).str.upper()
    result = ledger.get("result", pd.Series("", index=ledger.index)).astype(str).str.upper()
    is_pick = ~record_status.eq("NO_BET_RECORD")
    if "is_official_pick" in ledger.columns:
        is_pick = is_pick & ledger["is_official_pick"].astype(str).isin(["1", "1.0", "True", "TRUE", "true"])
    closed = result_status.isin(["RESULT_AVAILABLE", "SETTLED", "GRADED"]) | record_status.eq("SETTLED")
    closed = closed | result.isin(["WIN", "LOSS", "PUSH", "VOID"])
    return is_pick & closed


def labeled_closed_count(labeled: pd.DataFrame) -> int:
    if labeled.empty:
        return 0
    status = labeled.get("actionable_result", pd.Series("", index=labeled.index)).astype(str).str.upper()
    primary = labeled.get("primary_result", pd.Series("", index=labeled.index)).astype(str).str.upper()
    action = labeled.get("actionable_flag", pd.Series("", index=labeled.index)).astype(str)
    closed = status.isin(["WIN", "LOSS", "PUSH", "VOID"]) | primary.isin(["WIN", "LOSS", "PUSH", "VOID"])
    if "actionable_flag" in labeled.columns:
        closed = closed & action.isin(["1", "1.0", "True", "TRUE", "true"])
    return int(closed.sum())


def value_counts_summary(df: pd.DataFrame, column: str, max_items: int = 6) -> str:
    if df.empty or column not in df.columns:
        return "none"
    counts = df[column].dropna().astype(str).str.strip()
    counts = counts[counts.ne("")]
    if counts.empty:
        return "none"
    return "; ".join(f"{key}: {value}" for key, value in counts.value_counts().head(max_items).items())


def coverage_value_summary(df: pd.DataFrame, column: str) -> str:
    if df.empty or column not in df.columns:
        return "UNKNOWN"
    series = df[column].dropna()
    if series.empty:
        return "UNKNOWN"
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.notna().any():
        return f"{int((numeric.fillna(0) > 0).sum())}/{len(series)}"
    return value_counts_summary(df, column, max_items=4)


def collect_current_pick_source(processed_dir: Path, target_date: str, decisions: pd.DataFrame) -> pd.DataFrame:
    snap = snapshot_dir(processed_dir, target_date)
    if not decisions.empty and not decisions["fixture_id"].astype(str).str.strip().eq("").all():
        return decisions.copy()
    return first_existing_frame(
        [
            snap / "vsigma_today_prelock_competition_top.csv",
            snap / "vsigma_today_competition_top.csv",
        ]
    )


def summarize_data_coverage(
    target_date: str,
    current_source: pd.DataFrame,
    coverage_matrix: pd.DataFrame,
    odds_depth: pd.DataFrame,
) -> list[str]:
    rows: list[str] = []
    current = target_date_rows(current_source, target_date)
    coverage_classes = value_counts_summary(current, "league_coverage_class")
    if coverage_classes == "none" and not coverage_matrix.empty:
        coverage_classes = value_counts_summary(coverage_matrix, "league_coverage_class")
    rows.append(f"- coverage rich / partial / weak: {coverage_classes}")

    for label, column in [
        ("odds coverage", "league_has_odds_coverage"),
        ("fixture stats coverage", "league_has_fixture_stats_coverage"),
        ("injuries coverage", "league_has_injuries_coverage"),
        ("lineups coverage", "league_has_lineups_coverage"),
        ("predictions coverage", "league_has_predictions_coverage"),
    ]:
        value = coverage_value_summary(current, column)
        if value == "UNKNOWN":
            value = coverage_value_summary(coverage_matrix, column)
        rows.append(f"- {label}: {value}")

    depth_status = "UNKNOWN"
    if not odds_depth.empty:
        depth_status = value_counts_summary(odds_depth, "metric")
        if "rows_total" in odds_depth.columns and "metric" in odds_depth.columns:
            metric_rows = odds_depth[["metric", "rows_total"]].head(5)
            depth_status = "; ".join(
                f"{norm_text(row['metric'])}: {norm_text(row['rows_total'])}" for _, row in metric_rows.iterrows()
            )
    rows.append(f"- odds structure depth: {depth_status}")

    gaps: list[str] = []
    for label, column in [
        ("odds", "league_has_odds_coverage"),
        ("fixture_stats", "league_has_fixture_stats_coverage"),
        ("injuries", "league_has_injuries_coverage"),
        ("lineups", "league_has_lineups_coverage"),
        ("predictions", "league_has_predictions_coverage"),
    ]:
        source = current if column in current.columns else coverage_matrix
        if source.empty or column not in source.columns:
            continue
        numeric = pd.to_numeric(source[column], errors="coerce").fillna(0)
        if (numeric <= 0).any():
            gaps.append(label)
    rows.append(f"- API gaps detected: {', '.join(sorted(set(gaps))) if gaps else 'none detected in available coverage inputs'}")
    return rows


def market_family(market: object) -> str:
    market_text = norm_upper(market)
    if market_text in {"OVER_1_5", "OVER_2_5", "UNDER_3_5", "BTTS_YES"}:
        return market_text
    if market_text in SIDE_MARKETS or market_text.endswith("_DNB"):
        return "SIDES_DNB_1X_X2"
    return market_text or "UNKNOWN"


def summarize_model_market(
    current_source: pd.DataFrame,
    labeled: pd.DataFrame,
    ledger: pd.DataFrame,
    calibration_table: pd.DataFrame,
) -> list[str]:
    frames = [df for df in [current_source, labeled, ledger] if not df.empty and "market_primary" in df.columns]
    combined = pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()
    rows: list[str] = []
    rows.append(f"- markets appearing in current/historical inputs: {value_counts_summary(combined, 'market_primary')}")
    rows.append(f"- failure modes principales: {first_failure_mode_summary(current_source, labeled, ledger)}")

    for family in ["OVER_1_5", "OVER_2_5", "SIDES_DNB_1X_X2"]:
        if family == "SIDES_DNB_1X_X2":
            family_rows = combined[combined["market_primary"].map(market_family).eq(family)] if not combined.empty else pd.DataFrame()
            table_rows = calibration_table[
                calibration_table.get("market_primary", pd.Series("", index=calibration_table.index)).map(market_family).eq(family)
            ] if not calibration_table.empty else pd.DataFrame()
            label = "sides / DNB / 1X / X2"
        else:
            family_rows = combined[combined["market_primary"].astype(str).str.upper().eq(family)] if not combined.empty else pd.DataFrame()
            table_rows = calibration_table[
                calibration_table.get("market_primary", pd.Series("", index=calibration_table.index)).astype(str).str.upper().eq(family)
            ] if not calibration_table.empty else pd.DataFrame()
            label = family
        sample = int(pd.to_numeric(table_rows.get("sample_size", pd.Series(dtype=float)), errors="coerce").fillna(0).max()) if not table_rows.empty else 0
        status = "needs more sample"
        if sample >= 30:
            status = "has usable sample for review"
        if sample >= 100:
            status = "has strong sample for proposal"
        rows.append(f"- {label}: appearances={len(family_rows)}; calibration_sample={sample}; status={status}")

    good_signal: list[str] = []
    needs_sample: list[str] = []
    if not calibration_table.empty and "market_primary" in calibration_table.columns:
        for market, group in calibration_table.groupby("market_primary", dropna=True):
            sample = int(pd.to_numeric(group.get("sample_size", pd.Series(dtype=float)), errors="coerce").fillna(0).max())
            usable = pd.to_numeric(group.get("usable_for_lookup", pd.Series(dtype=float)), errors="coerce").fillna(0).max()
            if sample >= 30 and usable > 0:
                good_signal.append(norm_upper(market))
            elif sample > 0:
                needs_sample.append(f"{norm_upper(market)} ({sample})")
    rows.append(f"- mercados con buena senal: {', '.join(sorted(set(good_signal))) if good_signal else 'none yet by sample rule'}")
    rows.append(f"- mercados que necesitan mas muestra: {', '.join(sorted(set(needs_sample))) if needs_sample else 'none detected'}")
    return rows


def first_failure_mode_summary(current_source: pd.DataFrame, labeled: pd.DataFrame, ledger: pd.DataFrame) -> str:
    for df, columns in [
        (current_source, ["accuracy_primary_risk", "pick_failure_mode", "risk_tags"]),
        (labeled, ["accuracy_primary_risk", "pick_failure_mode", "risk_tags"]),
        (ledger, ["risk_tags"]),
    ]:
        if df.empty:
            continue
        pieces: list[str] = []
        for column in columns:
            if column not in df.columns:
                continue
            values = df[column].dropna().astype(str)
            for value in values:
                for token in re.split(r"[;|]", value):
                    token = token.strip()
                    if token.startswith("FAILURE_MODE_") or token in {"LOW_CONVERSION", "DRAW_LIVE"}:
                        pieces.append(token)
        if pieces:
            return "; ".join(f"{key}: {value}" for key, value in pd.Series(pieces).value_counts().head(6).items())
    return "none"


def calibration_review(
    ledger: pd.DataFrame,
    labeled: pd.DataFrame,
    calibration_report: str,
) -> tuple[list[str], int, str, str]:
    ledger_closed = int(ledger_closed_mask(ledger).sum()) if not ledger.empty else 0
    labeled_closed = labeled_closed_count(labeled)
    closed_picks = max(ledger_closed, labeled_closed)
    enough_sample = "YES" if closed_picks >= 30 else "NO"
    recalibration_allowed = "YES" if closed_picks >= 100 else "NO"
    if closed_picks < 30:
        recommendation = "Do not recalibrate; keep collecting closed picks."
    elif closed_picks < 100:
        recommendation = "Suggest-only review is allowed; do not apply predictive changes."
    else:
        recommendation = "Strong recalibration proposal is allowed, but automatic application remains disabled."
    rows = [
        f"- closed picks available: {closed_picks}",
        f"- enough_sample: {enough_sample}",
        f"- recalibration_allowed: {recalibration_allowed}",
        f"- recommendation: {recommendation}",
        f"- calibration report present: {'YES' if calibration_report else 'NO'}",
    ]
    return rows, closed_picks, enough_sample, recalibration_allowed


def add_recommendation(
    rows: list[dict[str, object]],
    target_date: str,
    priority: str,
    category: str,
    title: str,
    reason: str,
    expected_impact: str,
    risk: str,
    recommended_action: str,
    apply_now: str,
    evidence: str,
) -> None:
    rows.append(
        {
            "target_date": target_date,
            "priority": priority,
            "category": category,
            "title": title,
            "reason": reason,
            "expected_impact": expected_impact,
            "risk": risk,
            "recommended_action": recommended_action,
            "apply_now": apply_now,
            "evidence": evidence,
        }
    )


def build_improvement_queue(
    target_date: str,
    auto_status: str,
    health_status: str,
    decisions: pd.DataFrame,
    decision_outcome_ledger: pd.DataFrame,
    current_source: pd.DataFrame,
    audit: pd.DataFrame,
    closed_picks: int,
    enough_sample: str,
    recalibration_allowed: str,
    missing_inputs: list[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    if health_status == "BROKEN":
        add_recommendation(
            rows,
            target_date,
            "P0",
            "operations",
            "Fix broken healthcheck before execution",
            "AUTO reports a broken technical health state.",
            "Prevents executing decisions on unreliable pipeline state.",
            "Operational fix may expose additional downstream warnings.",
            "Inspect healthcheck report and repair the failing check before changing model logic.",
            "YES",
            f"healthcheck_status={health_status}",
        )

    if "vsigma_cloud_decision_summary.csv" in missing_inputs:
        add_recommendation(
            rows,
            target_date,
            "P0",
            "operations",
            "Restore cloud decision summary generation",
            "The primary AUTO decision summary CSV is missing.",
            "Restores the canonical source for execution governance review.",
            "Low; diagnostic/reporting path only.",
            "Run AUTO controller and inspect upstream failures before any execution.",
            "YES",
            "missing decision summary CSV",
        )

    unresolved_prelock_unavailable = False
    if not audit.empty and audit.get("exclusion_reason", pd.Series("", index=audit.index)).astype(str).str.upper().eq("PRELOCK_NOT_AVAILABLE").any():
        if "final_block_reason" in decisions.columns:
            reasons = decisions.get("final_block_reason", pd.Series("", index=decisions.index)).astype(str).str.upper()
            actions = decisions.get("official_action", pd.Series("", index=decisions.index)).astype(str).str.upper()
            unresolved_prelock_unavailable = reasons.eq("PRELOCK_NOT_AVAILABLE_UNCLASSIFIED").any() or actions.eq("TECHNICAL_REVIEW").any()
        else:
            unresolved_prelock_unavailable = True

    if unresolved_prelock_unavailable:
        add_recommendation(
            rows,
            target_date,
            "P1",
            "execution",
            "Harden prelock unavailable handling",
            "Current candidates can reach the prelock window with no reliable pre-lock data.",
            "Improves execution explainability and prevents ambiguous no-action states.",
            "Low if limited to reporting and retry scheduling.",
            "Add explicit retry/no-bet timing diagnostics for PRELOCK_NOT_AVAILABLE rows.",
            "YES",
            "exclusion_reason=PRELOCK_NOT_AVAILABLE",
        )

    if not decisions.empty and "official_action" in decisions.columns:
        fixture_present = decisions.get("fixture_id", pd.Series("", index=decisions.index)).fillna("").astype(str).str.strip().ne("")
        actions = decisions.get("official_action", pd.Series("", index=decisions.index)).astype(str).str.upper()
        blocked = int((fixture_present & actions.isin(["NO_BET", "TECHNICAL_REVIEW"])).sum())
        waiting = int((fixture_present & actions.eq("WAIT")).sum())
    else:
        blocked = int(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str).isin(["PRELOCK_BLOCKED", "IN_WINDOW_BUT_BLOCKED"]).sum()) if not decisions.empty else 0
        waiting = int(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str).eq("WAITING_FOR_PRELOCK_WINDOW").sum()) if not decisions.empty else 0
    if blocked or waiting:
        add_recommendation(
            rows,
            target_date,
            "P1",
            "execution",
            "Keep actionable and non-actionable buckets separated",
            "The current day has waiting or blocked decisions.",
            "Keeps ledger/backtest interpretation aligned with execution reality.",
            "Low; reporting-only validation.",
            "Continue reporting all rows, actionable only, non-actionable, and graded bets separately.",
            "YES",
            f"blocked={blocked}; waiting={waiting}; auto_status={auto_status}",
        )

    expired_fixture_ids: set[str] = set()
    if not decision_outcome_ledger.empty:
        target_ledger = target_date_rows(decision_outcome_ledger, target_date)
        reasons = target_ledger.get("final_block_reason", pd.Series("", index=target_ledger.index)).astype(str).str.upper()
        actions = target_ledger.get("official_action", pd.Series("", index=target_ledger.index)).astype(str).str.upper()
        expired = target_ledger.get("is_expired", pd.Series("", index=target_ledger.index)).astype(str).str.upper().eq("YES")
        expired_fixture_ids = set(target_ledger.loc[expired, "fixture_id"].fillna("").astype(str).str.strip())
        prelock_not_available = reasons.str.contains("PRELOCK_NOT_AVAILABLE", regex=False)
        no_bet = actions.eq("NO_BET")
        odds_no_bet = no_bet & reasons.str.contains("ODDS_NOT_AVAILABLE", regex=False)
        lineups_no_bet = no_bet & reasons.str.contains("LINEUPS_NOT_AVAILABLE", regex=False)

        if int((prelock_not_available | expired).sum()) > 0:
            add_recommendation(
                rows,
                target_date,
                "P1",
                "execution",
                "Improve prelock timing schedule",
                "Decision outcome ledger includes expired or prelock unavailable decisions.",
                "Reduces non-actionable PRELOCK outcomes caused by late or missing execution windows.",
                "Low if limited to scheduling and reporting diagnostics.",
                "Review AUTO/PRELOCK timing so resolver runs before kickoff and captures a useful in-window slot.",
                "YES",
                f"prelock_not_available={int(prelock_not_available.sum())}; expired={int(expired.sum())}",
            )

        if int(odds_no_bet.sum()) > 0:
            add_recommendation(
                rows,
                target_date,
                "P1",
                "odds",
                "Improve in-window odds refresh",
                "Decision outcome ledger has NO_BET rows blocked by missing odds.",
                "Improves executable pick retention when model selection is already available.",
                "Medium; API quota and cache growth must remain bounded.",
                "Refresh odds for candidate fixtures inside the PRELOCK window before resolving final action.",
                "YES",
                f"no_bet_odds_not_available={int(odds_no_bet.sum())}",
            )

        if int(lineups_no_bet.sum()) > 0:
            add_recommendation(
                rows,
                target_date,
                "P2",
                "api_data",
                "Fetch candidate lineups in-window",
                "Decision outcome ledger has NO_BET rows blocked by missing lineups.",
                "Improves PRELOCK evidence for candidate fixtures without broad calendar enrichment.",
                "Medium; lineup availability varies by league and kickoff timing.",
                "Target lineup fetches to candidate fixtures inside the PRELOCK window.",
                "YES",
                f"no_bet_lineups_not_available={int(lineups_no_bet.sum())}",
            )

    api_data_evidence = api_gap_evidence(current_source, audit, exclude_fixture_ids=expired_fixture_ids)
    if api_data_evidence:
        add_recommendation(
            rows,
            target_date,
            "P2",
            "api_data",
            "Target API enrichment to candidate fixtures only",
            "Coverage gaps are present, but broad calendar enrichment would add cost and repo churn.",
            "Improves prelock evidence where it matters without expanding data volume unnecessarily.",
            "Medium; API quotas and cache growth must be controlled.",
            "Fetch lineups only for candidate picks in-window, injuries only for reliable leagues, and fixture statistics only for TOP candidates; keep cache bounds.",
            "YES",
            api_data_evidence,
        )

    if closed_picks < 30:
        add_recommendation(
            rows,
            target_date,
            "P3",
            "model_calibration",
            "Defer recalibration until minimum closed-pick sample",
            "Fewer than 30 closed picks are available.",
            "Avoids fitting thresholds or probability adjustments to noise.",
            "Low; no predictive change is applied.",
            "Keep calibration reporting active and wait for at least 30 closed picks before suggestions.",
            "NO",
            f"closed_picks={closed_picks}; enough_sample={enough_sample}; recalibration_allowed={recalibration_allowed}",
        )
    elif closed_picks < 100:
        add_recommendation(
            rows,
            target_date,
            "P3",
            "model_calibration",
            "Limit calibration to suggest-only review",
            "Closed-pick sample is between 30 and 99.",
            "Supports evidence gathering without automatic predictive changes.",
            "Medium if promoted too early.",
            "Generate proposal notes only; do not change scoring, thresholds, or probabilities.",
            "NO",
            f"closed_picks={closed_picks}; enough_sample={enough_sample}; recalibration_allowed={recalibration_allowed}",
        )
    else:
        add_recommendation(
            rows,
            target_date,
            "P3",
            "model_calibration",
            "Prepare strong recalibration proposal without auto-apply",
            "At least 100 closed picks are available.",
            "Enables a rigorous proposal for probability or threshold changes.",
            "High if applied without separate review.",
            "Build a human-reviewed proposal artifact; keep AUTO from applying it automatically.",
            "NO",
            f"closed_picks={closed_picks}; enough_sample={enough_sample}; recalibration_allowed={recalibration_allowed}",
        )

    if not rows:
        add_recommendation(
            rows,
            target_date,
            "P1",
            "execution",
            "Continue evidence accumulation",
            "No critical operational gaps were detected from available reports.",
            "Maintains reproducible monitoring while samples mature.",
            "Low.",
            "Keep AUTO review generation enabled and inspect daily queue deltas.",
            "YES",
            "no high-priority gaps detected",
        )

    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    out = pd.DataFrame(rows, columns=REVIEW_COLUMNS)
    return out.sort_values(["priority", "category", "title"], key=lambda col: col.map(order) if col.name == "priority" else col).reset_index(drop=True)


def api_gap_evidence(current_source: pd.DataFrame, audit: pd.DataFrame, exclude_fixture_ids: set[str] | None = None) -> str:
    evidence: list[str] = []
    exclude_fixture_ids = {fixture_id for fixture_id in (exclude_fixture_ids or set()) if fixture_id}
    for df in [current_source, audit]:
        if df.empty:
            continue
        if exclude_fixture_ids and "fixture_id" in df.columns:
            df = df[~df["fixture_id"].fillna("").astype(str).str.strip().isin(exclude_fixture_ids)].copy()
        if df.empty:
            continue
        if "data_gap_flags" in df.columns:
            summary = value_counts_summary(df, "data_gap_flags", max_items=4)
            if summary != "none":
                evidence.append(f"data_gap_flags={summary}")
        for column in ["prelock_lineup_state", "prelock_odds_state", "prelock_availability_state"]:
            if column in df.columns:
                summary = value_counts_summary(df, column, max_items=4)
                if "NOT_AVAILABLE" in summary or "UNKNOWN" in summary:
                    evidence.append(f"{column}={summary}")
        for column in ["league_has_fixture_stats_coverage", "league_has_injuries_coverage", "league_has_lineups_coverage"]:
            if column in df.columns:
                numeric = pd.to_numeric(df[column], errors="coerce").fillna(0)
                if (numeric <= 0).any():
                    evidence.append(f"{column} has gaps")
    return "; ".join(dict.fromkeys(evidence))


def missing_input_names(paths: dict[str, Path]) -> list[str]:
    return [name for name, path in paths.items() if not path.exists()]


def current_verdict(auto_status: str, health_status: str, executable: int, blocked: int, waiting: int) -> str:
    if health_status == "BROKEN":
        return "TECHNICAL_REVIEW_REQUIRED"
    if executable > 0:
        return "EXECUTION_AVAILABLE_UNDER_GOVERNANCE"
    if blocked > 0:
        return "NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA"
    if waiting > 0:
        return "WAIT_FOR_NEXT_PRELOCK_SLOT"
    if auto_status in {"NO_BET", "PAST_DATE_NO_PRE_REFRESH"}:
        return auto_status
    return "MONITOR_ONLY"


def official_action_summary(decisions: pd.DataFrame) -> str:
    if decisions.empty or "official_action" not in decisions.columns:
        return "UNKNOWN"
    actions = [norm_upper(value) for value in decisions["official_action"].tolist() if norm_upper(value)]
    if not actions:
        return "UNKNOWN"
    unique = set(actions)
    if len(unique) == 1:
        return actions[0]
    if "TECHNICAL_REVIEW" in unique:
        return "TECHNICAL_REVIEW"
    return "MIXED"


def build_system_review(
    target_date: str,
    timezone_name: str = "Atlantic/Canary",
    processed_dir: Path = PROCESSED_DIR,
) -> tuple[pd.DataFrame, ReviewPaths]:
    target_date = pd.Timestamp(target_date).date().isoformat()
    snap = snapshot_dir(processed_dir, target_date)
    governance_dir = processed_dir / "governance"
    governance_dir.mkdir(parents=True, exist_ok=True)
    snap.mkdir(parents=True, exist_ok=True)

    paths = {
        "vsigma_cloud_decision_summary.md": snap / "vsigma_cloud_decision_summary.md",
        "vsigma_cloud_decision_summary.csv": snap / "vsigma_cloud_decision_summary.csv",
        "vsigma_prelock_decision_resolver.csv": snap / "vsigma_prelock_decision_resolver.csv",
        "daily_competition_master_report.md": snap / "daily_competition_master_report.md",
        "vsigma_prelock_exclusion_audit.csv": snap / "vsigma_prelock_exclusion_audit.csv",
        "vsigma_today_competition_top.csv": snap / "vsigma_today_competition_top.csv",
        "vsigma_today_prelock_competition_top.csv": snap / "vsigma_today_prelock_competition_top.csv",
        "vsigma_ledger_daily_report.md": snap / "vsigma_ledger_daily_report.md",
        "vsigma_immutable_daily_pick_ledger.csv": processed_dir / "ledger" / "vsigma_immutable_daily_pick_ledger.csv",
        "vsigma_decision_outcome_ledger.csv": processed_dir / "ledger" / "vsigma_decision_outcome_ledger.csv",
        "vsigma_experiment_performance_report.md": processed_dir / "ledger" / "vsigma_experiment_performance_report.md",
        "vsigma_governance_dashboard.md": governance_dir / "vsigma_governance_dashboard.md",
        "vsigma_probability_calibration_report.txt": processed_dir / "vsigma_probability_calibration_report.txt",
        "vsigma_probability_calibration_table.csv": processed_dir / "vsigma_probability_calibration_table.csv",
        "vsigma_market_results_labeled.csv": processed_dir / "vsigma_market_results_labeled.csv",
        "vsigma_api_league_coverage_matrix.csv": processed_dir / "vsigma_api_league_coverage_matrix.csv",
        "vsigma_odds_structure_depth_summary.csv": processed_dir / "vsigma_odds_structure_depth_summary.csv",
    }
    missing = missing_input_names(paths)

    decision_md = read_text_optional(paths["vsigma_cloud_decision_summary.md"])
    cloud_decisions = read_csv_lenient(paths["vsigma_cloud_decision_summary.csv"])
    resolver_decisions = read_csv_lenient(paths["vsigma_prelock_decision_resolver.csv"])
    decisions = resolver_decisions if not resolver_decisions.empty else cloud_decisions
    audit = read_csv_lenient(paths["vsigma_prelock_exclusion_audit.csv"])
    ledger = read_csv_lenient(paths["vsigma_immutable_daily_pick_ledger.csv"])
    decision_outcome_ledger = read_csv_lenient(paths["vsigma_decision_outcome_ledger.csv"])
    labeled = read_csv_lenient(paths["vsigma_market_results_labeled.csv"])
    calibration_table = read_csv_lenient(paths["vsigma_probability_calibration_table.csv"])
    coverage_matrix = read_csv_lenient(paths["vsigma_api_league_coverage_matrix.csv"])
    odds_depth = read_csv_lenient(paths["vsigma_odds_structure_depth_summary.csv"])
    calibration_report = read_text_optional(paths["vsigma_probability_calibration_report.txt"])

    current_source = collect_current_pick_source(processed_dir, target_date, decisions)

    auto_status = parse_bullet_value(decision_md, "Auto status", "UNKNOWN")
    candidates = safe_int(parse_bullet_value(decision_md, "Candidates reviewed", ""), decision_candidate_count(decisions))
    executable = safe_int(parse_bullet_value(decision_md, "Executable picks", ""), int(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str).eq("EXECUTABLE").sum()) if not decisions.empty else 0)
    waiting = safe_int(parse_bullet_value(decision_md, "Waiting picks", ""), int(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str).eq("WAITING_FOR_PRELOCK_WINDOW").sum()) if not decisions.empty else 0)
    blocked = safe_int(parse_bullet_value(decision_md, "Blocked picks", ""), int(decisions.get("decision_state", pd.Series("", index=decisions.index)).astype(str).isin(["IN_WINDOW_BUT_BLOCKED", "PRELOCK_BLOCKED"]).sum()) if not decisions.empty else 0)
    if not resolver_decisions.empty and "official_action" in resolver_decisions.columns:
        candidate_rows = resolver_decisions.get("fixture_id", pd.Series("", index=resolver_decisions.index)).fillna("").astype(str).str.strip().ne("")
        actions = resolver_decisions.get("official_action", pd.Series("", index=resolver_decisions.index)).astype(str).str.upper()
        candidates = decision_candidate_count(resolver_decisions)
        executable = int((candidate_rows & actions.eq("EXECUTABLE")).sum())
        waiting = int((candidate_rows & actions.eq("WAIT")).sum())
        blocked = int((candidate_rows & actions.isin(["NO_BET", "TECHNICAL_REVIEW"])).sum())
    health_status = parse_bullet_value(decision_md, "healthcheck_status", "UNKNOWN")
    ledger_total = int(len(ledger)) if not ledger.empty else 0
    ledger_target = int(len(target_date_rows(ledger, target_date))) if not ledger.empty else 0
    decision_ledger_total = int(len(decision_outcome_ledger)) if not decision_outcome_ledger.empty else 0
    decision_ledger_actionable = int(decision_outcome_ledger.get("is_actionable", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_non_actionable = int(decision_outcome_ledger.get("is_non_actionable", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_no_bet = int(decision_outcome_ledger.get("official_action", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("NO_BET").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_expired = int(decision_outcome_ledger.get("is_expired", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_waiting = int(decision_outcome_ledger.get("is_waiting", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_blocked = int(decision_outcome_ledger.get("is_blocked", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    decision_ledger_technical = int(decision_outcome_ledger.get("is_technical_review", pd.Series("", index=decision_outcome_ledger.index)).astype(str).str.upper().eq("YES").sum()) if not decision_outcome_ledger.empty else 0
    verdict = current_verdict(auto_status, health_status, executable, blocked, waiting)

    calibration_rows, closed_picks, enough_sample, recalibration_allowed = calibration_review(
        ledger,
        labeled,
        calibration_report,
    )
    queue = build_improvement_queue(
        target_date,
        auto_status,
        health_status,
        decisions,
        decision_outcome_ledger,
        current_source,
        audit,
        closed_picks,
        enough_sample,
        recalibration_allowed,
        missing,
    )

    current_decisions = decisions.copy()
    if current_decisions.empty:
        current_decisions = pd.DataFrame(columns=DECISION_COLUMNS)
    for column in DECISION_COLUMNS:
        if column not in current_decisions.columns:
            current_decisions[column] = ""
    current_decisions = current_decisions[DECISION_COLUMNS]

    generated_at = datetime.now(ZoneInfo(timezone_name)).isoformat(timespec="seconds")
    lines = [
        f"# vSIGMA System Review - {target_date}",
        "",
        "## Executive Status",
        f"- Cloud AUTO status: {auto_status}",
        f"- Candidates reviewed: {candidates}",
        f"- Executable picks: {executable}",
        f"- Waiting picks: {waiting}",
        f"- Blocked picks: {blocked}",
        f"- Official action summary: {official_action_summary(decisions)}",
        f"- Healthcheck status: {health_status}",
        f"- Ledger rows total: {ledger_total}",
        f"- Ledger rows for target date: {ledger_target}",
        f"- Decision outcome ledger rows total: {decision_ledger_total}",
        f"- Decision outcome ledger actionable rows: {decision_ledger_actionable}",
        f"- Decision outcome ledger non-actionable rows: {decision_ledger_non_actionable}",
        f"- Decision outcome ledger no bet rows: {decision_ledger_no_bet}",
        f"- Decision outcome ledger expired rows: {decision_ledger_expired}",
        f"- Decision outcome ledger waiting rows: {decision_ledger_waiting}",
        f"- Decision outcome ledger blocked rows: {decision_ledger_blocked}",
        f"- Decision outcome ledger technical review rows: {decision_ledger_technical}",
        f"- Current operational verdict: {verdict}",
        "",
        "## Current Picks / Decisions",
        format_markdown_table(current_decisions, DECISION_COLUMNS, max_rows=50),
        "",
        "## Data Coverage Review",
        *summarize_data_coverage(target_date, current_source, coverage_matrix, odds_depth),
        "",
        "## Model / Market Review",
        *summarize_model_market(current_source, labeled, ledger, calibration_table),
        "",
        "## Calibration Review",
        *calibration_rows,
        "- action applied: NO",
        "",
        "## API Data Improvement Recommendations",
        "- Fetch lineups only for candidate picks inside the relevant prelock window.",
        "- Fetch injuries only for leagues with reliable coverage and candidate exposure.",
        "- Fetch fixture statistics only for TOP candidates where the data can change execution review.",
        "- Do not enrich the full calendar without a specific diagnostic or execution need.",
        "- Keep API cache bounded and monitor repository size.",
        "",
        "## System Improvement Queue",
        format_markdown_table(
            queue,
            [
                "priority",
                "category",
                "title",
                "reason",
                "expected_impact",
                "risk",
                "recommended_action",
                "apply_now",
                "evidence",
            ],
            max_rows=100,
        ),
        "",
        "## Input Inventory",
        f"- generated_at: {generated_at}",
        f"- timezone: {timezone_name}",
        f"- missing optional inputs: {', '.join(missing) if missing else 'none'}",
        "",
    ]

    governance_md = governance_dir / "vsigma_system_review.md"
    governance_csv = governance_dir / "vsigma_system_review.csv"
    today_md = snap / "vsigma_system_review.md"
    markdown = "\n".join(lines)
    governance_md.write_text(markdown, encoding="utf-8")
    today_md.write_text(markdown, encoding="utf-8")
    queue.to_csv(governance_csv, index=False)
    return queue, ReviewPaths(governance_md=governance_md, governance_csv=governance_csv, today_md=today_md)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA system review diagnostics.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        queue, paths = build_system_review(args.date, args.timezone, args.processed_dir)
    except Exception as exc:
        print(f"ERROR: vSIGMA system review failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
    print("=== VSIGMA SYSTEM REVIEW ===")
    print(f"Rows: {len(queue)}")
    print(f"Governance MD: {paths.governance_md}")
    print(f"Governance CSV: {paths.governance_csv}")
    print(f"Today MD: {paths.today_md}")


if __name__ == "__main__":
    main()
