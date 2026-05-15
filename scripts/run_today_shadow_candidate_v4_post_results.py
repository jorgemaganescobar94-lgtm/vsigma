from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

try:
    from run_today_shadow_candidate_v2_post_results import (
        evaluate_competition_picks,
        summarize_ledger,
    )
    from run_today_shadow_candidate_v4 import (
        DEGRADE,
        KEEP,
        REMOVE,
        SECONDARY,
        V4_MODE_NAME,
        empty_v4_frame,
        first_available,
        norm_text,
        norm_upper,
    )
except ModuleNotFoundError:
    from scripts.run_today_shadow_candidate_v2_post_results import (
        evaluate_competition_picks,
        summarize_ledger,
    )
    from scripts.run_today_shadow_candidate_v4 import (
        DEGRADE,
        KEEP,
        REMOVE,
        SECONDARY,
        V4_MODE_NAME,
        empty_v4_frame,
        first_available,
        norm_text,
        norm_upper,
    )


ROOT = Path(__file__).resolve().parents[1]
RAW_MATCHES_CSV = ROOT / "data" / "raw" / "matches.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"
CANDIDATE_V4_TOP_CSV = "vsigma_today_candidate_v4_competition_top.csv"
CANDIDATE_V4_LEDGER_CSV = "vsigma_today_candidate_v4_results_ledger.csv"
CANDIDATE_V4_SUMMARY_CSV = "vsigma_today_candidate_v4_results_summary.csv"
RESULT_COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_results.csv"
RESULT_COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4_results_report.txt"
SHADOW_POST_REPORT = "today_shadow_candidate_v4_post_report.csv"
POST_JOURNAL = "daily_post_shadow_candidate_v4.md"

EMPTY_LEDGER_COLUMNS = [
    "comparison_mode",
    "competition_pick_rank",
    "fixture_id",
    "league",
    "home_team",
    "away_team",
    "market_primary",
    "resolved_home_goals",
    "resolved_away_goals",
    "ledger_result_status",
    "actionable_result",
    "actionable_profit_units",
    "primary_result",
    "primary_profit_units",
]

RESULT_COMPARISON_COLUMNS = [
    "comparison_status",
    "fixture_id",
    "fixture",
    "league",
    "baseline_rank",
    "candidate_v2_rank",
    "candidate_v4_rank",
    "baseline_market",
    "candidate_v2_market",
    "candidate_v4_market",
    "candidate_v4_original_market",
    "candidate_v4_firewall_decision",
    "baseline_result",
    "candidate_v2_result",
    "candidate_v4_result",
    "baseline_profit_units",
    "candidate_v2_profit_units",
    "candidate_v4_profit_units",
]


def read_csv_required(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return pd.read_csv(path)


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def empty_ledger() -> pd.DataFrame:
    return pd.DataFrame(columns=EMPTY_LEDGER_COLUMNS)


def safe_evaluate_competition_picks(picks: pd.DataFrame, raw: pd.DataFrame, mode: str) -> pd.DataFrame:
    if picks.empty:
        return empty_ledger()
    if raw.empty:
        out = picks.copy()
        for col in EMPTY_LEDGER_COLUMNS:
            if col not in out.columns:
                out[col] = pd.NA
        out["comparison_mode"] = mode
        out["ledger_result_status"] = "UNMATCHED"
        out["actionable_result"] = "UNMATCHED"
        return out
    return evaluate_competition_picks(picks, raw, mode)


def copy_if_exists(src: Path, dest_dir: Path) -> None:
    if src.exists():
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest_dir / src.name)


def compare_key(df: pd.DataFrame) -> pd.Series:
    return df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()


def build_result_comparison(
    baseline_ledger: pd.DataFrame,
    candidate_v2_ledger: pd.DataFrame,
    candidate_v4_ledger: pd.DataFrame,
) -> pd.DataFrame:
    frames = {
        "baseline": baseline_ledger.copy(),
        "candidate_v2": candidate_v2_ledger.copy(),
        "candidate_v4": candidate_v4_ledger.copy(),
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
        v4 = item.get("candidate_v4", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v4)
        rows.append(
            {
                "comparison_status": "+".join(
                    name.upper()
                    for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v4", v4)]
                    if not row.empty
                ),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["competition_pick_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["competition_pick_rank"]) if not v2.empty else pd.NA,
                "candidate_v4_rank": first_available(v4, ["competition_pick_rank"]) if not v4.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v4_market": first_available(v4, ["market_primary"]) if not v4.empty else pd.NA,
                "candidate_v4_original_market": first_available(v4, ["over25_low_conversion_original_market"]) if not v4.empty else pd.NA,
                "candidate_v4_firewall_decision": first_available(v4, ["over25_low_conversion_firewall_decision"]) if not v4.empty else pd.NA,
                "baseline_result": first_available(b, ["actionable_result"]) if not b.empty else pd.NA,
                "candidate_v2_result": first_available(v2, ["actionable_result"]) if not v2.empty else pd.NA,
                "candidate_v4_result": first_available(v4, ["actionable_result"]) if not v4.empty else pd.NA,
                "baseline_profit_units": first_available(b, ["actionable_profit_units"]) if not b.empty else pd.NA,
                "candidate_v2_profit_units": first_available(v2, ["actionable_profit_units"]) if not v2.empty else pd.NA,
                "candidate_v4_profit_units": first_available(v4, ["actionable_profit_units"]) if not v4.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=RESULT_COMPARISON_COLUMNS)


def write_result_report(
    path: Path,
    baseline_summary: dict[str, object],
    candidate_v2_summary: dict[str, object],
    candidate_v4_summary: dict[str, object],
    comparison: pd.DataFrame,
    candidate_v4_top: pd.DataFrame,
) -> None:
    decisions = candidate_v4_top.get("over25_low_conversion_firewall_decision", pd.Series(dtype=object))
    adjusted = int(decisions.isin([DEGRADE, REMOVE, SECONDARY]).sum()) if not candidate_v4_top.empty else 0
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V4 RESULTS",
        "",
    ]
    if int(candidate_v4_summary.get("pick_count", 0)) == 0:
        lines.extend(
            [
                "CANDIDATE_V4_NO_BET",
                "reason: candidate v4 top empty",
                "",
            ]
        )
    lines.extend(
        [
        "Mode summary",
        pd.DataFrame([baseline_summary, candidate_v2_summary, candidate_v4_summary]).to_string(index=False),
        "",
        f"Candidate v4 adjusted/downgraded top picks: {adjusted}",
        "",
        "Pick result comparison",
        comparison.to_string(index=False) if not comparison.empty else "No compared picks.",
        ]
    )
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


def write_post_journal(
    path: Path,
    match_date: str,
    timezone_name: str,
    candidate_v4_summary: dict[str, object],
    candidate_v4_ledger: pd.DataFrame,
    comparison: pd.DataFrame,
) -> None:
    lines = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v4 Post",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_name}",
        "- Mode: SHADOW / experimental / non-official",
        "",
        "## O2.5 Low Conversion Firewall",
        "",
    ]
    if candidate_v4_ledger.empty:
        lines.extend(["- CANDIDATE_V4_NO_BET", "- reason: candidate v4 top empty"])
        lines.append("- Candidate v4 ledger is empty.")
    else:
        checked = candidate_v4_ledger[
            candidate_v4_ledger.get("over25_low_conversion_firewall_flag", pd.Series(0, index=candidate_v4_ledger.index)).eq(1)
        ].copy()
        if checked.empty:
            lines.append("- Checked: 0")
        else:
            for _, row in checked.iterrows():
                lines.append(
                    f"- {row.get('home_team')} vs {row.get('away_team')}: "
                    f"{row.get('over25_low_conversion_original_market')} -> {row.get('market_primary')} | "
                    f"{row.get('over25_low_conversion_firewall_decision')} | "
                    f"{row.get('actionable_result')} | {row.get('actionable_profit_units')}"
                )
    lines.extend(
        [
            "",
            "## Candidate v4 Result Summary",
            "",
            f"- Pick count: {candidate_v4_summary['pick_count']}",
            f"- Wins/losses: {candidate_v4_summary['wins']} / {candidate_v4_summary['losses']}",
            f"- Profit/ROI: {candidate_v4_summary['profit_units']} / {candidate_v4_summary['roi_percent']}%",
            "",
            "## Result Comparison",
            "",
            markdown_table(comparison) if not comparison.empty else "_No comparison rows._",
        ]
    )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_candidate_v4_post_results(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    match_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
) -> dict[str, Path]:
    match_date = match_date or date.today().isoformat()
    raw = read_csv_optional(RAW_MATCHES_CSV)
    baseline_top = read_csv_optional(processed_dir / BASELINE_TOP_CSV)
    candidate_v2_top = read_csv_optional(processed_dir / CANDIDATE_V2_TOP_CSV)
    candidate_v4_top = read_csv_optional(processed_dir / CANDIDATE_V4_TOP_CSV)
    if candidate_v4_top.empty:
        candidate_v4_top = empty_v4_frame(candidate_v2_top)

    baseline_ledger = safe_evaluate_competition_picks(baseline_top, raw, "BASELINE_OFFICIAL")
    candidate_v2_ledger = safe_evaluate_competition_picks(candidate_v2_top, raw, "SHADOW_CANDIDATE_V2")
    candidate_v4_ledger = safe_evaluate_competition_picks(candidate_v4_top, raw, V4_MODE_NAME)
    baseline_summary = summarize_ledger(baseline_ledger, "BASELINE_OFFICIAL")
    candidate_v2_summary = summarize_ledger(candidate_v2_ledger, "SHADOW_CANDIDATE_V2")
    candidate_v4_summary = summarize_ledger(candidate_v4_ledger, V4_MODE_NAME)
    comparison = build_result_comparison(baseline_ledger, candidate_v2_ledger, candidate_v4_ledger)

    ledger_path = processed_dir / CANDIDATE_V4_LEDGER_CSV
    summary_path = processed_dir / CANDIDATE_V4_SUMMARY_CSV
    comparison_path = processed_dir / RESULT_COMPARISON_CSV
    comparison_report_path = processed_dir / RESULT_COMPARISON_REPORT
    shadow_post_path = processed_dir / SHADOW_POST_REPORT

    candidate_v4_ledger.to_csv(ledger_path, index=False)
    pd.DataFrame([candidate_v4_summary]).to_csv(summary_path, index=False)
    comparison.to_csv(comparison_path, index=False)
    write_result_report(
        comparison_report_path,
        baseline_summary,
        candidate_v2_summary,
        candidate_v4_summary,
        comparison,
        candidate_v4_top,
    )

    decisions = candidate_v4_top.get("over25_low_conversion_firewall_decision", pd.Series(dtype=object))
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "baseline_pick_count": baseline_summary["pick_count"],
                "candidate_v2_pick_count": candidate_v2_summary["pick_count"],
                "candidate_v4_pick_count": candidate_v4_summary["pick_count"],
                "overlap_three_way_picks": int(comparison["comparison_status"].eq("BASELINE+CANDIDATE_V2+CANDIDATE_V4").sum()) if not comparison.empty else 0,
                "candidate_v4_firewall_kept_rows": int(decisions.eq(KEEP).sum()) if not candidate_v4_top.empty else 0,
                "candidate_v4_firewall_downgraded_rows": int(decisions.eq(DEGRADE).sum()) if not candidate_v4_top.empty else 0,
                "candidate_v4_firewall_secondary_rows": int(decisions.eq(SECONDARY).sum()) if not candidate_v4_top.empty else 0,
                "candidate_v4_firewall_removed_rows": int(decisions.eq(REMOVE).sum()) if not candidate_v4_top.empty else 0,
                "baseline_wins": baseline_summary["wins"],
                "baseline_losses": baseline_summary["losses"],
                "baseline_profit_units": baseline_summary["profit_units"],
                "baseline_roi_percent": baseline_summary["roi_percent"],
                "candidate_v2_wins": candidate_v2_summary["wins"],
                "candidate_v2_losses": candidate_v2_summary["losses"],
                "candidate_v2_profit_units": candidate_v2_summary["profit_units"],
                "candidate_v2_roi_percent": candidate_v2_summary["roi_percent"],
                "candidate_v4_wins": candidate_v4_summary["wins"],
                "candidate_v4_losses": candidate_v4_summary["losses"],
                "candidate_v4_profit_units": candidate_v4_summary["profit_units"],
                "candidate_v4_roi_percent": candidate_v4_summary["roi_percent"],
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(shadow_post_path, index=False)

    snapshot_dir = today_dir / match_date
    for path in [ledger_path, summary_path, comparison_path, comparison_report_path, shadow_post_path]:
        copy_if_exists(path, snapshot_dir)
    post_journal_path = snapshot_dir / POST_JOURNAL
    write_post_journal(post_journal_path, match_date, timezone_name, candidate_v4_summary, candidate_v4_ledger, comparison)

    return {
        "candidate_v4_results_ledger": ledger_path,
        "candidate_v4_results_summary": summary_path,
        "result_comparison_csv": comparison_path,
        "result_comparison_report": comparison_report_path,
        "shadow_post_report": shadow_post_path,
        "shadow_post_journal": post_journal_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate candidate v4 shadow picks after today's official post-results refresh."
    )
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v4_post_results(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    print("\n=== TODAY SHADOW CANDIDATE V4 POST-RESULTS COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
