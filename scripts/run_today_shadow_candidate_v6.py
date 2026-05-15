from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates
    from enrich_api_predictions_benchmark import PREDICTION_COLUMNS, add_api_prediction_benchmark_fields
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates
    from scripts.enrich_api_predictions_benchmark import PREDICTION_COLUMNS, add_api_prediction_benchmark_fields


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_SHORTLIST_CSV = "vsigma_today_candidate_v2_competition_shortlist.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"

CANDIDATE_V6_SHORTLIST_CSV = "vsigma_today_candidate_v6_competition_shortlist.csv"
CANDIDATE_V6_TOP_CSV = "vsigma_today_candidate_v6_competition_top.csv"
CANDIDATE_V6_REPORT_TXT = "vsigma_today_candidate_v6_competition_report.txt"
COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv"
COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6_report.txt"
SHADOW_RUN_REPORT = "today_shadow_candidate_v6_report.csv"
PRE_JOURNAL = "daily_pre_shadow_candidate_v6.md"

V6_MODE_NAME = "SHADOW_CANDIDATE_V6_API_PREDICTIONS_BENCHMARK"
NOT_APPLIED = "NOT_APPLIED"
ALIGNED_STRENGTHEN = "API_PREDICTION_ALIGNED_STRENGTHEN"
DISAGREEMENT_WEAKEN = "API_PREDICTION_DISAGREEMENT_WEAKEN"
DISAGREEMENT_SECONDARY = "API_PREDICTION_DISAGREEMENT_SECONDARY"

FRAGILE_FAILURE_MODES = {
    "FAILURE_MODE_LOW_CONVERSION",
    "FAILURE_MODE_BTTS_BREAK",
    "FAILURE_MODE_DRAW_LIVE",
    "LOW_CONVERSION",
    "BTTS_BREAK",
    "DRAW_LIVE",
}

V6_COLUMNS = [
    "api_prediction_benchmark_action",
    "api_prediction_benchmark_changed_inclusion_flag",
    "api_prediction_original_accuracy_eligible_flag",
    "api_prediction_original_confidence_score",
    "api_prediction_original_market",
    "api_prediction_recommended_status",
    *PREDICTION_COLUMNS,
]

EMPTY_V6_COLUMNS = [
    "date",
    "league",
    "fixture_id",
    "home_team",
    "away_team",
    "market_primary",
    "market_alt",
    "accuracy_mode_rank",
    "competition_raw_prob",
    "competition_calibrated_prob",
    "accuracy_confidence_score",
    "accuracy_primary_risk",
    "pick_mode",
    *V6_COLUMNS,
]

COMPARISON_COLUMNS = [
    "comparison_status",
    "fixture_id",
    "fixture",
    "league",
    "baseline_rank",
    "candidate_v2_rank",
    "candidate_v6_rank",
    "baseline_market",
    "candidate_v2_market",
    "candidate_v6_market",
    "candidate_v6_action",
    "candidate_v6_alignment",
    "candidate_v6_confidence_adjustment",
    "baseline_primary_risk",
    "candidate_v2_primary_risk",
    "candidate_v6_primary_risk",
]


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm_text(value).upper()


def safe_float(value: object, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def empty_v6_frame(source: pd.DataFrame | None = None) -> pd.DataFrame:
    source_cols = list(source.columns) if source is not None and not source.empty else []
    columns = list(dict.fromkeys([*source_cols, *EMPTY_V6_COLUMNS]))
    return pd.DataFrame(columns=columns)


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def compare_key(df: pd.DataFrame) -> pd.Series:
    return df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()


def has_fragile_failure_mode(row: pd.Series) -> bool:
    blob = " ".join(
        norm_upper(row.get(col))
        for col in ["accuracy_primary_risk", "pick_primary_risk", "pick_failure_mode", "predicted_pick_breaker"]
    )
    return any(token in blob for token in FRAGILE_FAILURE_MODES)


def append_reason(value: object, tag: str) -> str:
    existing = norm_text(value)
    return (existing + ";" + tag).strip(";") if existing else tag


def benchmark_action(row: pd.Series) -> str:
    quality = norm_upper(row.get("api_prediction_quality_flag"))
    alignment = norm_upper(row.get("api_prediction_alignment_flag"))
    if quality == "UNKNOWN" or alignment in {"UNKNOWN", "NEUTRAL", ""}:
        return NOT_APPLIED
    if alignment == "ALIGNED":
        return ALIGNED_STRENGTHEN
    if alignment == "DISAGREEMENT" and has_fragile_failure_mode(row):
        return DISAGREEMENT_SECONDARY
    if alignment == "DISAGREEMENT":
        return DISAGREEMENT_WEAKEN
    return NOT_APPLIED


def apply_api_predictions_benchmark_layer(
    candidate_v2_shortlist: pd.DataFrame,
    *,
    use_api: bool = True,
    payload_by_fixture: dict[int, dict[str, Any]] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, int]]:
    source, counters = add_api_prediction_benchmark_fields(
        candidate_v2_shortlist,
        use_api=use_api,
        payload_by_fixture=payload_by_fixture,
    )
    if source.empty:
        for col in V6_COLUMNS:
            if col not in source.columns:
                source[col] = pd.Series(dtype=object)
        return source, source.copy(), source.copy(), counters

    out = source.copy()
    out["api_prediction_original_accuracy_eligible_flag"] = out.get("accuracy_mode_eligible_flag", pd.Series(1, index=out.index))
    out["api_prediction_original_confidence_score"] = out.get("accuracy_confidence_score", pd.Series(0.0, index=out.index))
    out["api_prediction_original_market"] = out.get("market_primary", pd.Series("", index=out.index))
    out["api_prediction_benchmark_action"] = [benchmark_action(row) for _, row in out.iterrows()]
    out["api_prediction_benchmark_changed_inclusion_flag"] = 0
    out["api_prediction_recommended_status"] = "KEEP"

    for idx, row in out.iterrows():
        action = norm_upper(row.get("api_prediction_benchmark_action"))
        adjustment = safe_float(row.get("api_prediction_confidence_adjustment"), 0.0)
        if action == NOT_APPLIED:
            continue

        if "accuracy_confidence_score" in out.columns:
            out.loc[idx, "accuracy_confidence_score"] = round(
                max(0.0, safe_float(out.loc[idx, "accuracy_confidence_score"], 0.0) + adjustment),
                3,
            )
        prob_delta = 0.006 if action == ALIGNED_STRENGTHEN else -0.012
        for col in ["primary_model_prob", "competition_raw_prob", "competition_calibrated_prob"]:
            if col in out.columns:
                out.loc[idx, col] = round(max(0.01, min(0.97, safe_float(out.loc[idx, col], 0.0) + prob_delta)), 6)

        if "accuracy_mode_reason" in out.columns:
            out.loc[idx, "accuracy_mode_reason"] = append_reason(out.loc[idx, "accuracy_mode_reason"], action)

        if action == DISAGREEMENT_SECONDARY:
            out.loc[idx, "api_prediction_recommended_status"] = "SECONDARY_ONLY"
            out.loc[idx, "accuracy_mode_eligible_flag"] = 0
            out.loc[idx, "accuracy_mode_bucket"] = "ACCURACY_REJECTED"
            out.loc[idx, "final_recommendation"] = "WATCH"
            out.loc[idx, "api_prediction_benchmark_changed_inclusion_flag"] = 1
            if "accuracy_primary_risk" in out.columns:
                out.loc[idx, "accuracy_primary_risk"] = append_reason(out.loc[idx, "accuracy_primary_risk"], action)
        elif action == DISAGREEMENT_WEAKEN:
            out.loc[idx, "api_prediction_recommended_status"] = "WEAKEN_KEEP"
            if "accuracy_primary_risk" in out.columns:
                out.loc[idx, "accuracy_primary_risk"] = append_reason(out.loc[idx, "accuracy_primary_risk"], action)
        elif action == ALIGNED_STRENGTHEN:
            out.loc[idx, "api_prediction_recommended_status"] = "STRENGTHEN_KEEP"

    out["pick_mode"] = V6_MODE_NAME
    eligible = out[pd.to_numeric(out.get("accuracy_mode_eligible_flag", 0), errors="coerce").fillna(0).eq(1)].copy()
    shortlist = sort_accuracy_candidates(eligible) if not eligible.empty else empty_v6_frame(out)
    if not shortlist.empty:
        shortlist["accuracy_mode_rank"] = range(1, len(shortlist) + 1)
        shortlist["pick_mode"] = V6_MODE_NAME
    top = select_competition_top(shortlist) if not shortlist.empty else empty_v6_frame(out)
    if not top.empty:
        top["pick_mode"] = V6_MODE_NAME
    return out.reset_index(drop=True), shortlist.reset_index(drop=True), top.reset_index(drop=True), counters


def build_three_way_comparison(baseline: pd.DataFrame, candidate_v2: pd.DataFrame, candidate_v6: pd.DataFrame) -> pd.DataFrame:
    frames = {
        "baseline": baseline.copy(),
        "candidate_v2": candidate_v2.copy(),
        "candidate_v6": candidate_v6.copy(),
    }
    by_fixture: dict[str, dict[str, pd.Series]] = {}
    for label, df in frames.items():
        if df.empty:
            continue
        df["_fixture_key"] = compare_key(df)
        for key, row in df.drop_duplicates("_fixture_key").set_index("_fixture_key").iterrows():
            by_fixture.setdefault(key, {})[label] = row

    rows: list[dict[str, object]] = []
    for key in sorted(by_fixture):
        item = by_fixture[key]
        b = item.get("baseline", pd.Series(dtype=object))
        v2 = item.get("candidate_v2", pd.Series(dtype=object))
        v6 = item.get("candidate_v6", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v6)
        rows.append(
            {
                "comparison_status": "+".join(
                    name.upper()
                    for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v6", v6)]
                    if not row.empty
                ),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["accuracy_mode_rank", "execution_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["accuracy_mode_rank", "execution_rank"]) if not v2.empty else pd.NA,
                "candidate_v6_rank": first_available(v6, ["accuracy_mode_rank", "execution_rank"]) if not v6.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v6_market": first_available(v6, ["market_primary"]) if not v6.empty else pd.NA,
                "candidate_v6_action": first_available(v6, ["api_prediction_benchmark_action"]) if not v6.empty else pd.NA,
                "candidate_v6_alignment": first_available(v6, ["api_prediction_alignment_flag"]) if not v6.empty else pd.NA,
                "candidate_v6_confidence_adjustment": first_available(v6, ["api_prediction_confidence_adjustment"]) if not v6.empty else pd.NA,
                "baseline_primary_risk": first_available(b, ["accuracy_primary_risk", "pick_primary_risk"]) if not b.empty else pd.NA,
                "candidate_v2_primary_risk": first_available(v2, ["accuracy_primary_risk", "pick_primary_risk"]) if not v2.empty else pd.NA,
                "candidate_v6_primary_risk": first_available(v6, ["accuracy_primary_risk", "pick_primary_risk"]) if not v6.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=COMPARISON_COLUMNS)


def action_counts(df: pd.DataFrame) -> dict[str, int]:
    actions = df.get("api_prediction_benchmark_action", pd.Series(dtype=object)).map(norm_upper)
    return {
        "prediction_adjusted_rows": int(actions.ne(NOT_APPLIED).sum()) if len(actions) else 0,
        "prediction_strengthened_rows": int(actions.eq(ALIGNED_STRENGTHEN).sum()) if len(actions) else 0,
        "prediction_weakened_rows": int(actions.eq(DISAGREEMENT_WEAKEN).sum()) if len(actions) else 0,
        "prediction_secondary_rows": int(actions.eq(DISAGREEMENT_SECONDARY).sum()) if len(actions) else 0,
    }


def write_v6_report(path: Path, all_rows: pd.DataFrame, shortlist: pd.DataFrame, top: pd.DataFrame, counters: dict[str, int]) -> None:
    actions = all_rows.get("api_prediction_benchmark_action", pd.Series(dtype=object)).map(norm_upper)
    lines = [
        "vSIGMA SHADOW CANDIDATE V6",
        "",
        "Layer: candidate v2 + API Predictions Benchmark.",
        "Status: experimental shadow; API predictions never create picks.",
        "",
        f"Candidate v2 input rows: {len(all_rows)}",
        f"Candidate v6 competition shortlist rows: {len(shortlist)}",
        f"Candidate v6 competition top rows: {len(top)}",
        f"API prediction available rows: {counters.get('available_rows', 0)}",
        f"API prediction aligned rows: {counters.get('aligned_rows', 0)}",
        f"API prediction disagreement rows: {counters.get('disagreement_rows', 0)}",
        f"API calls: {counters.get('api_calls_made', 0)} | cache hits: {counters.get('cache_hits', 0)} | errors: {counters.get('api_errors', 0)}",
        "",
        "API Predictions Benchmark action mix",
        actions.value_counts().to_string() if len(actions) else "No rows.",
        "",
        "Candidate v6 Top",
    ]
    if top.empty:
        lines.append("No v6 competition top picks survived.")
    else:
        cols = [
            "accuracy_mode_rank",
            "fixture_id",
            "league",
            "home_team",
            "away_team",
            "market_primary",
            "competition_calibrated_prob",
            "accuracy_confidence_score",
            "api_prediction_alignment_flag",
            "api_prediction_benchmark_action",
        ]
        lines.append(top[[c for c in cols if c in top.columns]].to_string(index=False))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_comparison_report(path: Path, baseline: pd.DataFrame, v2: pd.DataFrame, v6: pd.DataFrame, comparison: pd.DataFrame) -> None:
    counts = action_counts(v6)
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V6",
        "",
        "Baseline: official frozen Competition Accuracy Mode + Probability Calibration.",
        "Candidate v2: shadow schedule-strength + anomaly-cleaning layer.",
        "Candidate v6: candidate v2 + API Predictions Benchmark.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(v2)}",
        f"Candidate v6 shadow picks: {len(v6)}",
        f"Candidate v6 adjusted top rows: {counts['prediction_adjusted_rows']}",
        "",
        "Side-by-side picks",
        comparison.to_string(index=False) if not comparison.empty else "No compared rows.",
        "",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(norm_text(row.get(col)).replace("|", "\\|") for col in cols) + " |")
    return "\n".join(lines)


def write_pre_journal(path: Path, match_date: str, timezone_name: str, top: pd.DataFrame, all_rows: pd.DataFrame, counters: dict[str, int]) -> None:
    lines = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v6 Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_name}",
        "- Mode: SHADOW / experimental / non-official",
        "- Layer: candidate v2 + API Predictions Benchmark",
        "",
        "## API Predictions Benchmark",
        "",
        f"- Available rows: {counters.get('available_rows', 0)}",
        f"- Aligned rows: {counters.get('aligned_rows', 0)}",
        f"- Disagreement rows: {counters.get('disagreement_rows', 0)}",
        f"- API calls: {counters.get('api_calls_made', 0)}",
        "",
    ]
    cols = [
        "fixture_id",
        "home_team",
        "away_team",
        "market_primary",
        "api_prediction_quality_flag",
        "api_prediction_alignment_flag",
        "api_prediction_confidence_adjustment",
        "api_prediction_benchmark_action",
        "api_prediction_benchmark_changed_inclusion_flag",
    ]
    lines.append(markdown_table(all_rows[[c for c in cols if c in all_rows.columns]]) if not all_rows.empty else "_No candidate v2 rows to benchmark._")
    lines.extend(["", "## Candidate v6 Shadow Top", ""])
    top_cols = ["accuracy_mode_rank", "home_team", "away_team", "market_primary", "api_prediction_alignment_flag", "api_prediction_benchmark_action"]
    lines.append(markdown_table(top[[c for c in top_cols if c in top.columns]]) if not top.empty else "_No top picks survived._")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_shadow_run_report(
    path: Path,
    match_date: str,
    timezone_name: str,
    baseline_top: pd.DataFrame,
    candidate_v2_top: pd.DataFrame,
    candidate_v6_top: pd.DataFrame,
    all_rows: pd.DataFrame,
    counters: dict[str, int],
) -> None:
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "mode": V6_MODE_NAME,
                "baseline_competition_rows": int(len(baseline_top)),
                "candidate_v2_competition_rows": int(len(candidate_v2_top)),
                "candidate_v6_competition_rows": int(len(candidate_v6_top)),
                **counters,
                **action_counts(all_rows),
                "official_baseline_preserved": 1,
                "candidate_v2_preserved": 1,
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(path, index=False)


def build_candidate_v6_outputs(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    match_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
    *,
    use_api: bool = True,
    payload_by_fixture: dict[int, dict[str, Any]] | None = None,
) -> dict[str, Path]:
    match_date = match_date or date.today().isoformat()
    snapshot_dir = today_dir / match_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    baseline_top = read_csv_optional(processed_dir / BASELINE_TOP_CSV)
    candidate_v2_shortlist = read_csv_optional(processed_dir / CANDIDATE_V2_SHORTLIST_CSV)
    candidate_v2_top = read_csv_optional(processed_dir / CANDIDATE_V2_TOP_CSV)

    if candidate_v2_shortlist.empty:
        all_rows = empty_v6_frame(candidate_v2_top)
        shortlist = empty_v6_frame(candidate_v2_top)
        top = empty_v6_frame(candidate_v2_top)
        counters = {
            "rows_processed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "api_calls_made": 0,
            "api_errors": 0,
            "plan_limit_errors": 0,
            "available_rows": 0,
            "aligned_rows": 0,
            "disagreement_rows": 0,
        }
    else:
        all_rows, shortlist, top, counters = apply_api_predictions_benchmark_layer(
            candidate_v2_shortlist,
            use_api=use_api,
            payload_by_fixture=payload_by_fixture,
        )

    shortlist_path = processed_dir / CANDIDATE_V6_SHORTLIST_CSV
    top_path = processed_dir / CANDIDATE_V6_TOP_CSV
    report_path = processed_dir / CANDIDATE_V6_REPORT_TXT
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    shadow_report_path = processed_dir / SHADOW_RUN_REPORT

    shortlist.to_csv(shortlist_path, index=False)
    top.to_csv(top_path, index=False)
    write_v6_report(report_path, all_rows, shortlist, top, counters)
    comparison = build_three_way_comparison(baseline_top, candidate_v2_top, top)
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_top, candidate_v2_top, top, comparison)
    write_shadow_run_report(shadow_report_path, match_date, timezone_name, baseline_top, candidate_v2_top, top, all_rows, counters)

    for path in [shortlist_path, top_path, report_path, comparison_path, comparison_report_path, shadow_report_path]:
        copy_if_exists(path, snapshot_dir)
    pre_journal_path = snapshot_dir / PRE_JOURNAL
    write_pre_journal(pre_journal_path, match_date, timezone_name, top, all_rows, counters)

    return {
        "candidate_v6_shortlist": shortlist_path,
        "candidate_v6_top": top_path,
        "candidate_v6_report": report_path,
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": shadow_report_path,
        "shadow_pre_journal": pre_journal_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build candidate v6 shadow outputs from candidate v2 plus API predictions benchmark.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--cache-only", action="store_true", help="Do not fetch missing predictions from the API.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v6_outputs(
        PROCESSED_DIR,
        TODAY_DIR,
        match_date,
        args.timezone,
        use_api=not args.cache_only,
    )
    print("\n=== TODAY SHADOW CANDIDATE V6 COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print("Official baseline and candidate v2 files preserved; v6 wrote separate outputs only.")


if __name__ == "__main__":
    main()
