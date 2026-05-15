from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Iterable

import pandas as pd


DEFAULT_PROCESSED_DIR = Path("data/processed")

PRE_SUMMARY_FILENAME = "daily_pre_summary.md"
POST_SUMMARY_FILENAME = "daily_post_summary.md"
SHADOW_CANDIDATE_V2_PRE_SUMMARY_FILENAME = "daily_pre_shadow_candidate_v2.md"
SHADOW_CANDIDATE_V2_POST_SUMMARY_FILENAME = "daily_post_shadow_candidate_v2.md"

PRE_COUNT_FILES = {
    "Approved premium": "vsigma_final_approved_premium_candidates.csv",
    "Approved standard": "vsigma_final_approved_standard_candidates.csv",
    "Downgraded": "vsigma_final_downgraded_candidates.csv",
    "Blocked": "vsigma_final_blocked_candidates.csv",
    "Watch": "vsigma_final_watch_candidates.csv",
}

PRE_REPORT_COUNT_COLUMNS = {
    "Approved premium": "approved_premium_rows",
    "Approved standard": "approved_standard_rows",
    "Downgraded": "downgraded_rows",
    "Blocked": "blocked_rows",
    "Watch": "watch_rows",
}

EXPLANATION_COLUMNS = [
    "pick_main_why",
    "pick_primary_risk",
    "pick_bucket_rationale",
    "pick_rank_rationale",
    "pick_failure_mode",
    "pick_confirmation_layers",
]

GRADED_RESULTS = {"WIN", "LOSS", "PUSH", "VOID"}


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def fmt_num(value: object, digits: int = 3) -> str:
    try:
        if pd.isna(value):
            return "NA"
        return f"{float(value):.{digits}f}"
    except Exception:
        return "NA"


def markdown_cell(value: object) -> str:
    text = norm_text(value)
    if not text:
        return "NA"
    return text.replace("|", "/").replace("\n", " ")


def snapshot_dir_for(processed_dir: Path, today_dir: Path | None, match_date: str) -> Path:
    return (today_dir if today_dir is not None else processed_dir / "today") / match_date


def candidate_paths(processed_dir: Path, snapshot_dir: Path, filename: str) -> Iterable[Path]:
    yield snapshot_dir / filename
    yield processed_dir / filename


def read_csv_optional(processed_dir: Path, snapshot_dir: Path, filename: str) -> pd.DataFrame:
    for path in candidate_paths(processed_dir, snapshot_dir, filename):
        if not path.exists() or path.stat().st_size == 0:
            continue
        try:
            return pd.read_csv(path)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()


def count_rows_from_file(processed_dir: Path, snapshot_dir: Path, filename: str) -> int:
    df = read_csv_optional(processed_dir, snapshot_dir, filename)
    return int(len(df))


def resolve_timezone(
    processed_dir: Path,
    snapshot_dir: Path,
    timezone_name: str | None,
    report_filename: str,
) -> str:
    if timezone_name:
        return timezone_name
    report = read_csv_optional(processed_dir, snapshot_dir, report_filename)
    if not report.empty and "timezone" in report.columns:
        value = norm_text(report.loc[0, "timezone"])
        if value:
            return value
    return "UNKNOWN"


def pre_pipeline_counts(processed_dir: Path, snapshot_dir: Path) -> dict[str, int]:
    report = read_csv_optional(processed_dir, snapshot_dir, "today_pipeline_report.csv")
    counts: dict[str, int] = {}
    for label, filename in PRE_COUNT_FILES.items():
        report_col = PRE_REPORT_COUNT_COLUMNS[label]
        if not report.empty and report_col in report.columns and pd.notna(report.loc[0, report_col]):
            counts[label] = int(report.loc[0, report_col])
        else:
            counts[label] = count_rows_from_file(processed_dir, snapshot_dir, filename)
    return counts


def fixture_label(row: pd.Series) -> str:
    home = norm_text(row.get("home_team"))
    away = norm_text(row.get("away_team"))
    if home or away:
        return f"{home or 'UNKNOWN'} vs {away or 'UNKNOWN'}"
    return f"fixture_id={markdown_cell(row.get('fixture_id'))}"


def sort_by_rank(df: pd.DataFrame, rank_col: str) -> pd.DataFrame:
    if df.empty or rank_col not in df.columns:
        return df.copy()
    out = df.copy()
    out["_rank_sort"] = pd.to_numeric(out[rank_col], errors="coerce")
    return out.sort_values("_rank_sort", ascending=True, na_position="last").drop(
        columns=["_rank_sort"]
    )


def pick_table(df: pd.DataFrame, rank_col: str) -> list[str]:
    if df.empty:
        return ["_No rows._", ""]

    ordered = sort_by_rank(df, rank_col)
    lines = [
        "| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- | --- |",
    ]
    for _, row in ordered.iterrows():
        rank = markdown_cell(row.get(rank_col, row.get("execution_rank", "")))
        bucket = markdown_cell(row.get("execution_shortlist_source", row.get("final_execution_bucket")))
        lines.append(
            "| "
            + " | ".join(
                [
                    rank,
                    markdown_cell(fixture_label(row)),
                    markdown_cell(row.get("league")),
                    markdown_cell(row.get("market_primary")),
                    markdown_cell(row.get("final_recommendation")),
                    bucket,
                    fmt_num(row.get("execution_score"), 3),
                    markdown_cell(row.get("pick_main_why")),
                    markdown_cell(row.get("pick_primary_risk")),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def execution_blocks(shortlist: pd.DataFrame) -> list[str]:
    if shortlist.empty:
        return ["_No executable picks._", ""]

    lines: list[str] = []
    for _, row in sort_by_rank(shortlist, "execution_rank").iterrows():
        lines.extend(
            [
                f"### #{markdown_cell(row.get('execution_rank'))} {markdown_cell(fixture_label(row))}",
                f"- League: {markdown_cell(row.get('league'))}",
                f"- Market: {markdown_cell(row.get('market_primary'))}",
                f"- Bucket: {markdown_cell(row.get('execution_shortlist_source', row.get('final_execution_bucket')))}",
                f"- Recommendation: {markdown_cell(row.get('final_recommendation'))}",
                f"- Execution score: {fmt_num(row.get('execution_score'), 3)}",
                f"- Main why: {markdown_cell(row.get('pick_main_why'))}",
                f"- Primary risk: {markdown_cell(row.get('pick_primary_risk'))}",
                f"- Bucket rationale: {markdown_cell(row.get('pick_bucket_rationale'))}",
                f"- Rank rationale: {markdown_cell(row.get('pick_rank_rationale'))}",
                f"- Confirmation layers: {markdown_cell(row.get('pick_confirmation_layers'))}",
                "",
            ]
        )
    return lines


def forecast_blocks(forecasts: pd.DataFrame) -> list[str]:
    if forecasts.empty:
        return ["_No match-script forecasts available._", ""]

    lines: list[str] = []
    for _, row in sort_by_rank(forecasts, "forecast_rank").iterrows():
        lines.extend(
            [
                f"### #{markdown_cell(row.get('forecast_rank'))} {markdown_cell(fixture_label(row))}",
                f"- Market: {markdown_cell(row.get('market_primary'))}",
                f"- Script: {markdown_cell(row.get('predicted_match_script'))}",
                f"- Scoreline: main {markdown_cell(row.get('predicted_score_main'))}; alt {markdown_cell(row.get('predicted_score_alt'))}",
                f"- xG: home {markdown_cell(row.get('predicted_home_xg_range'))}; away {markdown_cell(row.get('predicted_away_xg_range'))}; total {markdown_cell(row.get('predicted_total_goals_range'))}",
                f"- Shots: home {markdown_cell(row.get('predicted_home_shots_range'))}; away {markdown_cell(row.get('predicted_away_shots_range'))}; SOT {markdown_cell(row.get('predicted_home_sot_range'))} vs {markdown_cell(row.get('predicted_away_sot_range'))}",
                f"- Corners / possession: {markdown_cell(row.get('predicted_total_corners_range'))}; {markdown_cell(row.get('predicted_possession_split'))}",
                f"- Pick path: {markdown_cell(row.get('predicted_pick_path'))}",
                f"- Pick breaker: {markdown_cell(row.get('predicted_pick_breaker'))}",
                "",
            ]
        )
    return lines


def build_pre_summary(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    today_dir: Path | None = None,
    match_date: str | None = None,
    timezone_name: str | None = None,
) -> Path:
    match_date = match_date or date.today().isoformat()
    processed_dir = Path(processed_dir)
    snapshot_dir = snapshot_dir_for(processed_dir, today_dir, match_date)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    timezone_label = resolve_timezone(processed_dir, snapshot_dir, timezone_name, "today_pipeline_report.csv")

    counts = pre_pipeline_counts(processed_dir, snapshot_dir)
    safe = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_safe_top5.csv")
    balanced = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_balanced_top5.csv")
    shortlist = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_execution_shortlist.csv")
    forecasts = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_match_script_forecasts.csv")

    lines: list[str] = [
        "# vSIGMA Daily Decision Journal - Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_label}",
        "",
        "## Pipeline Counts",
        "",
        "| Bucket | Rows |",
        "| --- | ---: |",
    ]
    for label, value in counts.items():
        lines.append(f"| {label} | {value} |")

    lines.extend(["", "## SAFE Picks", ""])
    lines.extend(pick_table(safe, "mode_rank"))
    lines.extend(["## BALANCED Picks", ""])
    lines.extend(pick_table(balanced, "mode_rank"))
    lines.extend(["## Execution Shortlist", ""])
    lines.extend(execution_blocks(shortlist))
    lines.extend(["## Match Script Forecasts", ""])
    lines.extend(forecast_blocks(forecasts))

    output_path = snapshot_dir / PRE_SUMMARY_FILENAME
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def metric_from_report(report: pd.DataFrame, column: str, default: object = "NA") -> object:
    if not report.empty and column in report.columns and pd.notna(report.loc[0, column]):
        return report.loc[0, column]
    return default


def ledger_profit(ledger: pd.DataFrame) -> pd.Series:
    actionable = pd.to_numeric(
        ledger.get("actionable_profit_units", pd.Series(index=ledger.index, dtype=object)),
        errors="coerce",
    )
    primary = pd.to_numeric(
        ledger.get("primary_profit_units", pd.Series(index=ledger.index, dtype=object)),
        errors="coerce",
    )
    return actionable.combine_first(primary)


def enrich_ledger_with_original_explanations(ledger: pd.DataFrame, shortlist: pd.DataFrame) -> pd.DataFrame:
    if ledger.empty or shortlist.empty:
        return ledger.copy()

    keys = [col for col in ["execution_rank", "fixture_id", "market_primary"] if col in ledger.columns and col in shortlist.columns]
    if not keys:
        keys = [col for col in ["fixture_id", "market_primary"] if col in ledger.columns and col in shortlist.columns]
    if not keys:
        return ledger.copy()

    cols = keys + [col for col in EXPLANATION_COLUMNS if col in shortlist.columns]
    original = shortlist[cols].drop_duplicates(subset=keys)
    return ledger.merge(original, on=keys, how="left", sort=False, validate="many_to_one")


def result_status_masks(ledger: pd.DataFrame) -> dict[str, pd.Series]:
    status = ledger.get("ledger_result_status", pd.Series("", index=ledger.index)).map(norm_upper)
    result = ledger.get("actionable_result", pd.Series("", index=ledger.index)).map(norm_upper)
    settled = status.eq("RESULT_AVAILABLE") | result.isin(GRADED_RESULTS)
    return {
        "settled": settled,
        "pending": status.eq("PENDING") | result.eq("PENDING"),
        "unmatched": status.eq("UNMATCHED"),
        "win": result.eq("WIN"),
        "loss": result.eq("LOSS"),
        "push": result.eq("PUSH"),
        "void": result.eq("VOID"),
    }


def post_verdict(row: pd.Series) -> str:
    status = norm_upper(row.get("ledger_result_status"))
    result = norm_upper(row.get("actionable_result"))
    if status == "UNMATCHED":
        return "UNMATCHED_RESULT"
    if status == "PENDING" or result in {"", "PENDING"}:
        return "PENDING_RESULT"
    if result == "WIN":
        return "WIN_CONFIRMED"
    if result == "LOSS":
        if norm_text(row.get("pick_failure_mode")) or norm_text(row.get("pick_primary_risk")):
            return "LOSS_MATCHED_FAILURE_MODE"
        return "LOSS_UNCLEAR"
    if result == "PUSH":
        return "PUSH_NO_DECISION"
    if result == "VOID":
        return "VOID_NO_DECISION"
    return "RESULT_REVIEW_NEEDED"


def post_metrics(report: pd.DataFrame, ledger: pd.DataFrame) -> dict[str, object]:
    masks = result_status_masks(ledger)
    profit = ledger_profit(ledger).where(masks["settled"])
    settled_rows = int(masks["settled"].sum())
    total_profit = float(profit.sum(skipna=True)) if settled_rows else 0.0
    roi = (total_profit / settled_rows * 100.0) if settled_rows else pd.NA
    return {
        "ledger_rows": metric_from_report(report, "ledger_rows", len(ledger)),
        "settled_rows": metric_from_report(report, "result_available_rows", settled_rows),
        "pending_rows": metric_from_report(report, "pending_rows", int(masks["pending"].sum())),
        "unmatched_rows": metric_from_report(report, "unmatched_rows", int(masks["unmatched"].sum())),
        "profit_units_total": metric_from_report(report, "profit_units_total", round(total_profit, 6)),
        "roi_percent": metric_from_report(report, "roi_percent", round(float(roi), 6) if pd.notna(roi) else "NA"),
        "wins": metric_from_report(report, "win_rows", int(masks["win"].sum())),
        "losses": metric_from_report(report, "loss_rows", int(masks["loss"].sum())),
        "pushes": metric_from_report(report, "push_rows", int(masks["push"].sum())),
        "voids": metric_from_report(report, "void_rows", int(masks["void"].sum())),
    }


def ledger_blocks(ledger: pd.DataFrame) -> list[str]:
    if ledger.empty:
        return ["_No ledger rows available._", ""]

    lines: list[str] = []
    rank_col = "execution_rank" if "execution_rank" in ledger.columns else "competition_pick_rank"
    for _, row in sort_by_rank(ledger, rank_col).iterrows():
        result = markdown_cell(row.get("actionable_result"))
        profit = fmt_num(ledger_profit(pd.DataFrame([row])).iloc[0], 3)
        verdict = post_verdict(row)
        lines.extend(
            [
                f"### #{markdown_cell(row.get(rank_col))} {markdown_cell(fixture_label(row))}",
                f"- League: {markdown_cell(row.get('league'))}",
                f"- Market: {markdown_cell(row.get('market_primary'))}",
                f"- Result status: {markdown_cell(row.get('ledger_result_status'))}",
                f"- Result: {result}",
                f"- Profit units: {profit}",
                f"- Original main why: {markdown_cell(row.get('pick_main_why'))}",
                f"- Original primary risk: {markdown_cell(row.get('pick_primary_risk'))}",
                f"- POST_VERDICT: {verdict}",
                "",
            ]
        )
    return lines


def build_post_summary(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    today_dir: Path | None = None,
    match_date: str | None = None,
    timezone_name: str | None = None,
) -> Path:
    match_date = match_date or date.today().isoformat()
    processed_dir = Path(processed_dir)
    snapshot_dir = snapshot_dir_for(processed_dir, today_dir, match_date)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    timezone_label = resolve_timezone(processed_dir, snapshot_dir, timezone_name, "today_post_results_report.csv")

    report = read_csv_optional(processed_dir, snapshot_dir, "today_post_results_report.csv")
    ledger = read_csv_optional(processed_dir, snapshot_dir, "vsigma_execution_shortlist_results_ledger.csv")
    shortlist = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_execution_shortlist.csv")
    enriched = enrich_ledger_with_original_explanations(ledger, shortlist)
    metrics = post_metrics(report, enriched)

    lines: list[str] = [
        "# vSIGMA Daily Decision Journal - Post",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_label}",
        "",
        "## Ledger Summary",
        "",
        f"- Ledger rows: {metrics['ledger_rows']}",
        f"- Settled rows: {metrics['settled_rows']}",
        f"- Pending rows: {metrics['pending_rows']}",
        f"- Unmatched rows: {metrics['unmatched_rows']}",
        f"- Total profit units: {fmt_num(metrics['profit_units_total'], 3)}",
        f"- ROI percent: {fmt_num(metrics['roi_percent'], 3)}",
        "",
        "## Day Summary",
        "",
        f"- Wins: {metrics['wins']}",
        f"- Losses: {metrics['losses']}",
        f"- Pushes: {metrics['pushes']}",
        f"- Voids: {metrics['voids']}",
        "",
        "## Ledger Picks",
        "",
    ]
    lines.extend(ledger_blocks(enriched))

    output_path = snapshot_dir / POST_SUMMARY_FILENAME
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def comparison_table(comparison: pd.DataFrame) -> list[str]:
    if comparison.empty:
        return ["_No comparison rows._", ""]

    columns = [
        "comparison_status",
        "fixture",
        "baseline_rank",
        "candidate_v2_rank",
        "baseline_market",
        "candidate_v2_market",
        "baseline_calibrated_prob",
        "candidate_v2_calibrated_prob",
        "baseline_confidence_score",
        "candidate_v2_confidence_score",
    ]
    present = [col for col in columns if col in comparison.columns]
    lines = [
        "| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |",
        "| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for _, row in comparison[present].iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row.get("comparison_status")),
                    markdown_cell(row.get("fixture")),
                    markdown_cell(row.get("baseline_rank")),
                    markdown_cell(row.get("candidate_v2_rank")),
                    markdown_cell(row.get("baseline_market")),
                    markdown_cell(row.get("candidate_v2_market")),
                    fmt_num(row.get("baseline_calibrated_prob"), 3),
                    fmt_num(row.get("candidate_v2_calibrated_prob"), 3),
                    fmt_num(row.get("baseline_confidence_score"), 3),
                    fmt_num(row.get("candidate_v2_confidence_score"), 3),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def result_comparison_table(comparison: pd.DataFrame) -> list[str]:
    if comparison.empty:
        return ["_No result comparison rows._", ""]

    lines = [
        "| Status | Fixture | Base Result | Cand Result | Base Profit | Cand Profit |",
        "| --- | --- | --- | --- | ---: | ---: |",
    ]
    for _, row in comparison.iterrows():
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(row.get("comparison_status")),
                    markdown_cell(row.get("fixture")),
                    markdown_cell(row.get("baseline_result")),
                    markdown_cell(row.get("candidate_v2_result")),
                    fmt_num(row.get("baseline_profit_units"), 3),
                    fmt_num(row.get("candidate_v2_profit_units"), 3),
                ]
            )
            + " |"
        )
    lines.append("")
    return lines


def build_shadow_candidate_v2_pre_summary(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    today_dir: Path | None = None,
    match_date: str | None = None,
    timezone_name: str | None = None,
) -> Path:
    match_date = match_date or date.today().isoformat()
    processed_dir = Path(processed_dir)
    snapshot_dir = snapshot_dir_for(processed_dir, today_dir, match_date)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    timezone_label = resolve_timezone(processed_dir, snapshot_dir, timezone_name, "today_shadow_candidate_v2_report.csv")

    report = read_csv_optional(processed_dir, snapshot_dir, "today_shadow_candidate_v2_report.csv")
    top = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_competition_top.csv")
    shortlist = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_competition_shortlist.csv")
    comparison = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2.csv")
    forecasts = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_match_script_forecasts.csv")

    metric = lambda col, fallback: metric_from_report(report, col, fallback)
    lines: list[str] = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_label}",
        "- Mode: SHADOW / experimental / non-official",
        "- Lab layers: schedule strength + anomaly cleaning",
        "",
        "## Shadow Counts",
        "",
        f"- Baseline official competition rows: {metric('baseline_competition_rows', 'NA')}",
        f"- Candidate v2 competition rows: {metric('candidate_v2_competition_rows', len(shortlist))}",
        f"- Overlap rows: {metric('overlap_rows', 'NA')}",
        f"- Baseline-only rows: {metric('baseline_only_rows', 'NA')}",
        f"- Candidate-only rows: {metric('candidate_v2_only_rows', 'NA')}",
        "",
        "## Candidate v2 Shadow Top",
        "",
    ]
    lines.extend(pick_table(top, "accuracy_mode_rank"))
    lines.extend(["## Candidate v2 Match Script Forecasts", ""])
    lines.extend(forecast_blocks(forecasts))
    lines.extend(["## Baseline vs Candidate v2", ""])
    lines.extend(comparison_table(comparison))

    output_path = snapshot_dir / SHADOW_CANDIDATE_V2_PRE_SUMMARY_FILENAME
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def build_shadow_candidate_v2_post_summary(
    processed_dir: Path = DEFAULT_PROCESSED_DIR,
    today_dir: Path | None = None,
    match_date: str | None = None,
    timezone_name: str | None = None,
) -> Path:
    match_date = match_date or date.today().isoformat()
    processed_dir = Path(processed_dir)
    snapshot_dir = snapshot_dir_for(processed_dir, today_dir, match_date)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    timezone_label = resolve_timezone(processed_dir, snapshot_dir, timezone_name, "today_shadow_candidate_v2_post_report.csv")

    report = read_csv_optional(processed_dir, snapshot_dir, "today_shadow_candidate_v2_post_report.csv")
    ledger = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_results_ledger.csv")
    top = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_candidate_v2_competition_top.csv")
    comparison = read_csv_optional(processed_dir, snapshot_dir, "vsigma_today_baseline_vs_candidate_v2_results.csv")
    enriched = enrich_ledger_with_original_explanations(ledger, top)
    metrics = post_metrics(pd.DataFrame(), enriched)

    metric = lambda col, fallback: metric_from_report(report, col, fallback)
    lines: list[str] = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v2 Post",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_label}",
        "- Mode: SHADOW / experimental / non-official",
        "",
        "## Baseline vs Candidate Result Summary",
        "",
        f"- Baseline pick count: {metric('baseline_pick_count', 'NA')}",
        f"- Candidate v2 pick count: {metric('candidate_v2_pick_count', len(ledger))}",
        f"- Overlap picks: {metric('overlap_picks', 'NA')}",
        f"- Baseline wins/losses: {metric('baseline_wins', 'NA')} / {metric('baseline_losses', 'NA')}",
        f"- Candidate wins/losses: {metric('candidate_v2_wins', metrics['wins'])} / {metric('candidate_v2_losses', metrics['losses'])}",
        f"- Baseline profit/ROI: {fmt_num(metric('baseline_profit_units', 'NA'), 3)} / {fmt_num(metric('baseline_roi_percent', 'NA'), 3)}%",
        f"- Candidate profit/ROI: {fmt_num(metric('candidate_v2_profit_units', metrics['profit_units_total']), 3)} / {fmt_num(metric('candidate_v2_roi_percent', metrics['roi_percent']), 3)}%",
        "",
        "## Result Comparison",
        "",
    ]
    lines.extend(result_comparison_table(comparison))
    lines.extend(["## Candidate v2 Ledger Picks", ""])
    lines.extend(ledger_blocks(enriched))

    output_path = snapshot_dir / SHADOW_CANDIDATE_V2_POST_SUMMARY_FILENAME
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build daily vSIGMA decision-journal markdown files.")
    parser.add_argument("--processed-dir", default=str(DEFAULT_PROCESSED_DIR))
    parser.add_argument("--today-dir", default=None)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--phase", choices=["pre", "post", "both"], default="both")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    processed_dir = Path(args.processed_dir)
    today_dir = Path(args.today_dir) if args.today_dir else None
    if args.phase in {"pre", "both"}:
        pre_path = build_pre_summary(processed_dir, today_dir, args.date, args.timezone)
        print(f"PRE_SUMMARY: {pre_path}")
    if args.phase in {"post", "both"}:
        post_path = build_post_summary(processed_dir, today_dir, args.date, args.timezone)
        print(f"POST_SUMMARY: {post_path}")


if __name__ == "__main__":
    main()
