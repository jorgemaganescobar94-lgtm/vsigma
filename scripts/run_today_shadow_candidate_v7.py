from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

try:
    from apply_price_discipline_guard import PRICE_DISCIPLINE_COLUMNS, apply_price_discipline_guard, empty_price_frame, norm_text, norm_upper
    from build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates
except ModuleNotFoundError:
    from scripts.apply_price_discipline_guard import PRICE_DISCIPLINE_COLUMNS, apply_price_discipline_guard, empty_price_frame, norm_text, norm_upper
    from scripts.build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_SHORTLIST_CSV = "vsigma_today_candidate_v2_competition_shortlist.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"
CANDIDATE_V7_SHORTLIST_CSV = "vsigma_today_candidate_v7_competition_shortlist.csv"
CANDIDATE_V7_TOP_CSV = "vsigma_today_candidate_v7_competition_top.csv"
CANDIDATE_V7_REPORT_TXT = "vsigma_today_candidate_v7_competition_report.txt"
COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv"
COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7_report.txt"
SHADOW_RUN_REPORT = "today_shadow_candidate_v7_report.csv"
PRE_JOURNAL = "daily_pre_shadow_candidate_v7.md"

V7_MODE_NAME = "SHADOW_CANDIDATE_V7_PRICE_DISCIPLINE_CLV_DRIFT_GUARD"


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


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def compare_key(df: pd.DataFrame) -> pd.Series:
    return df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join("---" for _ in cols) + " |"]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(norm_text(row.get(col)).replace("|", "\\|") for col in cols) + " |")
    return "\n".join(lines)


def build_v7_shortlist(candidate_v2_shortlist: pd.DataFrame, target_date: str | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    all_rows = apply_price_discipline_guard(candidate_v2_shortlist, target_date=target_date)
    if all_rows.empty:
        empty = empty_price_frame(candidate_v2_shortlist)
        return empty, empty.copy(), empty.copy()
    out = all_rows.copy()
    allowed = pd.to_numeric(out.get("price_discipline_execution_allowed_flag", 0), errors="coerce").fillna(0).eq(1)
    out.loc[~allowed, "accuracy_mode_eligible_flag"] = 0
    out.loc[~allowed, "accuracy_mode_bucket"] = "ACCURACY_REJECTED"
    if "accuracy_mode_reason" in out.columns:
        out.loc[~allowed, "accuracy_mode_reason"] = (
            out.loc[~allowed, "accuracy_mode_reason"].map(norm_text) + ";PRICE_DISCIPLINE_NOT_TOP"
        ).str.strip(";")
    out.loc[~allowed, "final_recommendation"] = "WATCH"
    eligible = out[allowed].copy()
    shortlist = sort_accuracy_candidates(eligible) if not eligible.empty else empty_price_frame(out)
    if not shortlist.empty:
        shortlist["accuracy_mode_rank"] = range(1, len(shortlist) + 1)
        shortlist["pick_mode"] = V7_MODE_NAME
    top = select_competition_top(shortlist) if not shortlist.empty else empty_price_frame(out)
    if not top.empty:
        top["pick_mode"] = V7_MODE_NAME
    out["pick_mode"] = V7_MODE_NAME
    return out.reset_index(drop=True), shortlist.reset_index(drop=True), top.reset_index(drop=True)


def build_three_way_comparison(baseline: pd.DataFrame, candidate_v2: pd.DataFrame, candidate_v7: pd.DataFrame) -> pd.DataFrame:
    frames = {"baseline": baseline.copy(), "candidate_v2": candidate_v2.copy(), "candidate_v7": candidate_v7.copy()}
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
        v7 = item.get("candidate_v7", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v7)
        rows.append(
            {
                "comparison_status": "+".join(name.upper() for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v7", v7)] if not row.empty),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["accuracy_mode_rank", "execution_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["accuracy_mode_rank", "execution_rank"]) if not v2.empty else pd.NA,
                "candidate_v7_rank": first_available(v7, ["accuracy_mode_rank", "execution_rank"]) if not v7.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v7_market": first_available(v7, ["market_primary"]) if not v7.empty else pd.NA,
                "candidate_v7_decision": first_available(v7, ["price_discipline_decision"]) if not v7.empty else pd.NA,
                "candidate_v7_required_edge": first_available(v7, ["price_discipline_min_edge_required"]) if not v7.empty else pd.NA,
                "candidate_v7_actual_edge": first_available(v7, ["price_discipline_actual_edge"]) if not v7.empty else pd.NA,
                "candidate_v7_drift_status": first_available(v7, ["price_discipline_drift_status"]) if not v7.empty else pd.NA,
                "candidate_v7_clv_direction": first_available(v7, ["clv_direction"]) if not v7.empty else pd.NA,
                "candidate_v7_execution_status": first_available(v7, ["candidate_v7_execution_status"]) if not v7.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows)


def write_v7_report(path: Path, all_rows: pd.DataFrame, shortlist: pd.DataFrame, top: pd.DataFrame) -> None:
    decisions = all_rows.get("price_discipline_decision", pd.Series(dtype=object)).map(norm_upper)
    lines = [
        "vSIGMA SHADOW CANDIDATE V7",
        "",
        "Layer: candidate v2 + price discipline + CLV tracking + drift execution guard.",
        "Status: shadow-only; official baseline and candidate v2 outputs are not replaced.",
        "",
        f"Candidate v2 input rows: {len(all_rows)}",
        f"Candidate v7 accepted shortlist rows: {len(shortlist)}",
        f"Candidate v7 competition top rows: {len(top)}",
        "",
        "Price discipline decision mix",
        decisions.value_counts().to_string() if len(decisions) else "No rows.",
        "",
        "Price Discipline / CLV / Drift Execution Guard",
    ]
    cols = [
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
    ]
    lines.append(all_rows[[c for c in cols if c in all_rows.columns]].to_string(index=False) if not all_rows.empty else "No candidate v2 rows.")
    lines.extend(["", "Candidate v7 Top"])
    lines.append(top[[c for c in cols if c in top.columns]].to_string(index=False) if not top.empty else "No v7 competition top picks survived.")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_comparison_report(path: Path, baseline: pd.DataFrame, v2: pd.DataFrame, v7: pd.DataFrame, comparison: pd.DataFrame) -> None:
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V7",
        "",
        "Baseline: official frozen Competition Accuracy Mode + Probability Calibration.",
        "Candidate v2: shadow schedule-strength + anomaly-cleaning layer.",
        "Candidate v7: candidate v2 + Price Discipline / CLV / Drift Execution Guard.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(v2)}",
        f"Candidate v7 shadow picks: {len(v7)}",
        "",
        "Side-by-side picks",
        comparison.to_string(index=False) if not comparison.empty else "No compared rows.",
        "",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_pre_journal(path: Path, match_date: str, timezone_name: str, all_rows: pd.DataFrame, top: pd.DataFrame) -> None:
    cols = [
        "fixture_id",
        "home_team",
        "away_team",
        "market_primary",
        "price_discipline_decision",
        "price_discipline_min_edge_required",
        "price_discipline_actual_edge",
        "price_discipline_drift_status",
        "clv_direction",
        "candidate_v7_prelock_status",
        "candidate_v7_execution_status",
    ]
    lines = [
        "# vSIGMA Daily Decision Journal - Shadow Candidate v7 Pre",
        "",
        f"- Date: {match_date}",
        f"- Timezone: {timezone_name}",
        "- Mode: SHADOW / experimental / non-official",
        "- Layer: candidate v2 + price discipline + CLV tracking + drift execution guard",
        "",
        "## Price Discipline / CLV / Drift Execution Guard",
        "",
        markdown_table(all_rows[[c for c in cols if c in all_rows.columns]]) if not all_rows.empty else "_No candidate v2 rows._",
        "",
        "## Candidate v7 Shadow Top",
        "",
        markdown_table(top[[c for c in cols if c in top.columns]]) if not top.empty else "_No top picks survived._",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def build_candidate_v7_outputs(
    processed_dir: Path = PROCESSED_DIR,
    today_dir: Path = TODAY_DIR,
    match_date: str | None = None,
    timezone_name: str = "Atlantic/Canary",
) -> dict[str, Path]:
    match_date = match_date or date.today().isoformat()
    snapshot_dir = today_dir / match_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    baseline_top = read_csv_optional(processed_dir / BASELINE_TOP_CSV)
    candidate_v2_shortlist = read_csv_optional(processed_dir / CANDIDATE_V2_SHORTLIST_CSV)
    candidate_v2_top = read_csv_optional(processed_dir / CANDIDATE_V2_TOP_CSV)

    all_rows, shortlist, top = build_v7_shortlist(candidate_v2_shortlist, target_date=match_date)
    shortlist_path = processed_dir / CANDIDATE_V7_SHORTLIST_CSV
    top_path = processed_dir / CANDIDATE_V7_TOP_CSV
    report_path = processed_dir / CANDIDATE_V7_REPORT_TXT
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    shadow_report_path = processed_dir / SHADOW_RUN_REPORT

    all_rows.to_csv(shortlist_path, index=False)
    top.to_csv(top_path, index=False)
    write_v7_report(report_path, all_rows, shortlist, top)
    comparison = build_three_way_comparison(baseline_top, candidate_v2_top, top)
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_top, candidate_v2_top, top, comparison)
    decisions = all_rows.get("price_discipline_decision", pd.Series(dtype=object)).map(norm_upper)
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "mode": V7_MODE_NAME,
                "baseline_competition_rows": int(len(baseline_top)),
                "candidate_v2_competition_rows": int(len(candidate_v2_top)),
                "candidate_v7_competition_rows": int(len(top)),
                "price_ok_rows": int(decisions.eq("PRICE_OK").sum()) if len(decisions) else 0,
                "price_thin_secondary_rows": int(decisions.eq("PRICE_THIN_SECONDARY_ONLY").sum()) if len(decisions) else 0,
                "price_rejected_rows": int(decisions.eq("PRICE_REJECTED").sum()) if len(decisions) else 0,
                "price_prelock_required_rows": int(decisions.eq("PRICE_NEEDS_PRELOCK_CONFIRMATION").sum()) if len(decisions) else 0,
                "v7_waiting_for_prelock_rows": int(all_rows.get("candidate_v7_execution_status", pd.Series(dtype=object)).map(norm_upper).eq("V7_WAITING_FOR_PRELOCK").sum()) if not all_rows.empty else 0,
                "v7_prelock_confirmed_rows": int(all_rows.get("candidate_v7_execution_status", pd.Series(dtype=object)).map(norm_upper).eq("V7_PRELOCK_CONFIRMED").sum()) if not all_rows.empty else 0,
                "v7_prelock_rejected_rows": int(all_rows.get("candidate_v7_execution_status", pd.Series(dtype=object)).map(norm_upper).isin(["V7_PRELOCK_REJECTED", "V7_SECONDARY_ONLY", "V7_PRICE_REJECTED"]).sum()) if not all_rows.empty else 0,
                "v7_prelock_unavailable_rows": int(all_rows.get("candidate_v7_execution_status", pd.Series(dtype=object)).map(norm_upper).eq("V7_PRELOCK_UNAVAILABLE").sum()) if not all_rows.empty else 0,
                "price_drift_penalized_rows": int(decisions.eq("PRICE_DRIFT_PENALIZED").sum()) if len(decisions) else 0,
                "official_baseline_preserved": 1,
                "candidate_v2_preserved": 1,
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(shadow_report_path, index=False)
    for path in [shortlist_path, top_path, report_path, comparison_path, comparison_report_path, shadow_report_path]:
        copy_if_exists(path, snapshot_dir)
    pre_journal_path = snapshot_dir / PRE_JOURNAL
    write_pre_journal(pre_journal_path, match_date, timezone_name, all_rows, top)
    return {
        "candidate_v7_shortlist": shortlist_path,
        "candidate_v7_top": top_path,
        "candidate_v7_report": report_path,
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": shadow_report_path,
        "shadow_pre_journal": pre_journal_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build candidate v7 shadow outputs from candidate v2 plus price discipline, CLV, and drift guard.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v7_outputs(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    print("\n=== TODAY SHADOW CANDIDATE V7 COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print("Official baseline and candidate v2 files preserved; v7 wrote separate outputs only.")


if __name__ == "__main__":
    main()
