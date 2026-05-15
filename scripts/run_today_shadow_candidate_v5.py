from __future__ import annotations

import argparse
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

try:
    from build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates
    from enrich_player_impact import PLAYER_IMPACT_COLUMNS, add_player_impact_fields
except ModuleNotFoundError:
    from scripts.build_competition_accuracy_mode import select_competition_top, sort_accuracy_candidates
    from scripts.enrich_player_impact import PLAYER_IMPACT_COLUMNS, add_player_impact_fields


ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
TODAY_DIR = PROCESSED_DIR / "today"

BASELINE_SHORTLIST_CSV = "vsigma_today_competition_shortlist.csv"
BASELINE_TOP_CSV = "vsigma_today_competition_top.csv"
CANDIDATE_V2_SHORTLIST_CSV = "vsigma_today_candidate_v2_competition_shortlist.csv"
CANDIDATE_V2_TOP_CSV = "vsigma_today_candidate_v2_competition_top.csv"

CANDIDATE_V5_SHORTLIST_CSV = "vsigma_today_candidate_v5_competition_shortlist.csv"
CANDIDATE_V5_TOP_CSV = "vsigma_today_candidate_v5_competition_top.csv"
CANDIDATE_V5_REPORT_TXT = "vsigma_today_candidate_v5_competition_report.txt"
COMPARISON_CSV = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv"
COMPARISON_REPORT = "vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5_report.txt"
SHADOW_RUN_REPORT = "today_shadow_candidate_v5_report.csv"

V5_MODE_NAME = "SHADOW_CANDIDATE_V5_PLAYER_IMPACT"
NOT_APPLIED = "NOT_APPLIED"
STRENGTHEN = "PLAYER_IMPACT_STRENGTHEN"
DOWNGRADE_GOALS = "PLAYER_IMPACT_DOWNGRADE_GOALS"
BLOCK_MARKET = "PLAYER_IMPACT_BLOCK_MARKET"
SIDE_RISK_FLAG = "PLAYER_IMPACT_SIDE_RISK_FLAG"

V5_COLUMNS = [
    "player_impact_adjustment_action",
    "player_impact_adjustment_reason",
    "player_impact_original_market",
    "player_impact_recommended_market",
    "player_impact_confidence_delta",
    "player_impact_probability_delta",
    *PLAYER_IMPACT_COLUMNS,
]

EMPTY_V5_COLUMNS = [
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
    *V5_COLUMNS,
]

COMPARISON_COLUMNS = [
    "comparison_status",
    "fixture_id",
    "fixture",
    "league",
    "baseline_rank",
    "candidate_v2_rank",
    "candidate_v5_rank",
    "baseline_market",
    "candidate_v2_market",
    "candidate_v5_market",
    "candidate_v5_original_market",
    "candidate_v5_action",
    "candidate_v5_hint",
    "baseline_primary_risk",
    "candidate_v2_primary_risk",
    "candidate_v5_primary_risk",
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


def empty_v5_frame(source: pd.DataFrame | None = None) -> pd.DataFrame:
    source_cols = list(source.columns) if source is not None and not source.empty else []
    columns = list(dict.fromkeys([*source_cols, *EMPTY_V5_COLUMNS]))
    return pd.DataFrame(columns=columns)


def first_available(row: pd.Series, columns: list[str]) -> object:
    for col in columns:
        if col in row.index and pd.notna(row.get(col)) and norm_text(row.get(col)):
            return row.get(col)
    return pd.NA


def compare_key(df: pd.DataFrame) -> pd.Series:
    return df.get("fixture_id", pd.Series("", index=df.index)).astype(str).str.strip()


def over15_available_clean(row: pd.Series) -> bool:
    if norm_upper(row.get("market_alt")) != "OVER_1_5":
        return False
    return bool(
        safe_float(row.get("alt_model_prob"), 0.0) >= 0.78
        and safe_float(row.get("alt_odds_used"), 0.0) > 1.0
        and safe_float(row.get("alt_edge"), -99.0) >= -0.01
    )


def swap_primary_alt_market(out: pd.DataFrame, idx: object, new_market: str) -> None:
    old_market = norm_upper(out.loc[idx, "market_primary"])
    old_alt = norm_upper(out.loc[idx, "market_alt"]) if "market_alt" in out.columns else ""
    out.loc[idx, "market_primary"] = new_market
    out.loc[idx, "market_alt"] = old_market or pd.NA
    if old_alt == new_market:
        for primary_col, alt_col in [
            ("primary_model_prob", "alt_model_prob"),
            ("primary_odds_used", "alt_odds_used"),
            ("primary_implied_prob", "alt_implied_prob"),
            ("primary_edge", "alt_edge"),
        ]:
            if primary_col in out.columns and alt_col in out.columns:
                old_primary = out.loc[idx, primary_col]
                out.loc[idx, primary_col] = out.loc[idx, alt_col]
                out.loc[idx, alt_col] = old_primary


def append_reason(value: object, tag: str) -> str:
    existing = norm_text(value)
    return (existing + ";" + tag).strip(";") if existing else tag


def player_impact_decision(row: pd.Series) -> dict[str, object]:
    quality = norm_upper(row.get("player_impact_quality_flag"))
    hint = norm_upper(row.get("player_impact_market_translation_hint"))
    market = norm_upper(row.get("market_primary"))
    original = market or pd.NA

    home_attack = safe_float(row.get("home_attacking_core_available_score"), 0.0)
    away_attack = safe_float(row.get("away_attacking_core_available_score"), 0.0)
    home_defense = safe_float(row.get("home_defensive_core_available_score"), 0.0)
    away_defense = safe_float(row.get("away_defensive_core_available_score"), 0.0)
    min_attack = min(home_attack, away_attack)
    avg_attack = (home_attack + away_attack) / 2.0
    weak_defense = min(home_defense, away_defense) <= -0.10
    gk_uncertain = norm_upper(row.get("home_goalkeeper_confidence_flag")) == "UNCERTAIN" or norm_upper(
        row.get("away_goalkeeper_confidence_flag")
    ) == "UNCERTAIN"

    base = {
        "player_impact_adjustment_action": NOT_APPLIED,
        "player_impact_adjustment_reason": "Player-impact coverage missing or neutral; no market movement.",
        "player_impact_original_market": original,
        "player_impact_recommended_market": market or pd.NA,
        "player_impact_confidence_delta": 0.0,
        "player_impact_probability_delta": 0.0,
    }
    if quality == "NONE":
        return base

    if market == "BTTS_YES" and min_attack <= -0.10:
        return {
            **base,
            "player_impact_adjustment_action": BLOCK_MARKET,
            "player_impact_adjustment_reason": "One attacking core is weakened; BTTS needs both scoring paths.",
            "player_impact_recommended_market": "NO_COMPETITION_PICK",
            "player_impact_confidence_delta": -10.0,
            "player_impact_probability_delta": -0.04,
        }

    if market == "OVER_2_5" and (min_attack <= -0.10 or avg_attack <= -0.07):
        if over15_available_clean(row):
            return {
                **base,
                "player_impact_adjustment_action": DOWNGRADE_GOALS,
                "player_impact_adjustment_reason": "Attacking-core weakness makes O2.5 too fine; clean O1.5 survival route exists.",
                "player_impact_recommended_market": "OVER_1_5",
                "player_impact_confidence_delta": -4.0,
                "player_impact_probability_delta": -0.015,
            }
        return {
            **base,
            "player_impact_adjustment_action": BLOCK_MARKET,
            "player_impact_adjustment_reason": "Attacking-core weakness makes O2.5 too fine and no clean O1.5 route exists.",
            "player_impact_recommended_market": "NO_COMPETITION_PICK",
            "player_impact_confidence_delta": -8.0,
            "player_impact_probability_delta": -0.03,
        }

    if market in {"OVER_1_5", "OVER_2_5", "BTTS_YES"} and (weak_defense or gk_uncertain):
        return {
            **base,
            "player_impact_adjustment_action": STRENGTHEN,
            "player_impact_adjustment_reason": "Defensive/GK uncertainty supports a goals thesis without creating a new pick.",
            "player_impact_confidence_delta": 2.0,
            "player_impact_probability_delta": 0.01,
        }

    if market in {"HOME_WIN", "HOME_DNB", "AWAY_WIN", "AWAY_DNB"} and (weak_defense or gk_uncertain):
        return {
            **base,
            "player_impact_adjustment_action": SIDE_RISK_FLAG,
            "player_impact_adjustment_reason": "Defensive/GK uncertainty flags side-market volatility; no hard veto.",
            "player_impact_confidence_delta": -2.0,
            "player_impact_probability_delta": -0.005,
        }

    if hint == "LINEUPS_CONFIRM_ATTACKING_THESIS" and market in {"OVER_1_5", "OVER_2_5"}:
        return {
            **base,
            "player_impact_adjustment_action": STRENGTHEN,
            "player_impact_adjustment_reason": "Lineup structure confirms attacking thesis.",
            "player_impact_confidence_delta": 1.5,
            "player_impact_probability_delta": 0.008,
        }

    return base


def apply_player_impact_layer(candidate_v2_shortlist: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source = add_player_impact_fields(candidate_v2_shortlist)
    if source.empty:
        for col in V5_COLUMNS:
            if col not in source.columns:
                source[col] = pd.Series(dtype=object)
        return source, source.copy(), source.copy()

    decisions = pd.DataFrame([player_impact_decision(row) for _, row in source.iterrows()], index=source.index)
    out = pd.concat([source, decisions], axis=1)

    for idx, row in out.iterrows():
        action = norm_upper(row.get("player_impact_adjustment_action"))
        if action == DOWNGRADE_GOALS and norm_upper(row.get("player_impact_recommended_market")) == "OVER_1_5":
            swap_primary_alt_market(out, idx, "OVER_1_5")
        elif action == BLOCK_MARKET:
            out.loc[idx, "accuracy_mode_eligible_flag"] = 0
            out.loc[idx, "accuracy_mode_bucket"] = "ACCURACY_REJECTED"
            out.loc[idx, "final_recommendation"] = "WATCH"

        prob_delta = safe_float(row.get("player_impact_probability_delta"), 0.0)
        conf_delta = safe_float(row.get("player_impact_confidence_delta"), 0.0)
        for col in ["primary_model_prob", "competition_raw_prob", "competition_calibrated_prob"]:
            if col in out.columns:
                out.loc[idx, col] = round(max(0.01, min(0.97, safe_float(out.loc[idx, col], 0.0) + prob_delta)), 6)
        if "accuracy_confidence_score" in out.columns:
            out.loc[idx, "accuracy_confidence_score"] = round(
                max(0.0, safe_float(out.loc[idx, "accuracy_confidence_score"], 0.0) + conf_delta),
                3,
            )
        if "accuracy_mode_reason" in out.columns and action != NOT_APPLIED:
            out.loc[idx, "accuracy_mode_reason"] = append_reason(out.loc[idx, "accuracy_mode_reason"], action)
        if "accuracy_primary_risk" in out.columns and action in {BLOCK_MARKET, SIDE_RISK_FLAG}:
            out.loc[idx, "accuracy_primary_risk"] = append_reason(out.loc[idx, "accuracy_primary_risk"], action)

    out["pick_mode"] = V5_MODE_NAME
    eligible = out[pd.to_numeric(out.get("accuracy_mode_eligible_flag", 0), errors="coerce").fillna(0).eq(1)].copy()
    shortlist = sort_accuracy_candidates(eligible) if not eligible.empty else empty_v5_frame(out)
    if not shortlist.empty:
        shortlist["accuracy_mode_rank"] = range(1, len(shortlist) + 1)
        shortlist["pick_mode"] = V5_MODE_NAME
    top = select_competition_top(shortlist) if not shortlist.empty else empty_v5_frame(out)
    if not top.empty:
        top["pick_mode"] = V5_MODE_NAME
    return out.reset_index(drop=True), shortlist.reset_index(drop=True), top.reset_index(drop=True)


def build_three_way_comparison(baseline: pd.DataFrame, candidate_v2: pd.DataFrame, candidate_v5: pd.DataFrame) -> pd.DataFrame:
    frames = {
        "baseline": baseline.copy(),
        "candidate_v2": candidate_v2.copy(),
        "candidate_v5": candidate_v5.copy(),
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
        v5 = item.get("candidate_v5", pd.Series(dtype=object))
        source = b if not b.empty else (v2 if not v2.empty else v5)
        rows.append(
            {
                "comparison_status": "+".join(
                    name.upper()
                    for name, row in [("baseline", b), ("candidate_v2", v2), ("candidate_v5", v5)]
                    if not row.empty
                ),
                "fixture_id": first_available(source, ["fixture_id"]),
                "fixture": f"{norm_text(first_available(source, ['home_team']))} vs {norm_text(first_available(source, ['away_team']))}",
                "league": first_available(source, ["league"]),
                "baseline_rank": first_available(b, ["accuracy_mode_rank", "execution_rank"]) if not b.empty else pd.NA,
                "candidate_v2_rank": first_available(v2, ["accuracy_mode_rank", "execution_rank"]) if not v2.empty else pd.NA,
                "candidate_v5_rank": first_available(v5, ["accuracy_mode_rank", "execution_rank"]) if not v5.empty else pd.NA,
                "baseline_market": first_available(b, ["market_primary"]) if not b.empty else pd.NA,
                "candidate_v2_market": first_available(v2, ["market_primary"]) if not v2.empty else pd.NA,
                "candidate_v5_market": first_available(v5, ["market_primary"]) if not v5.empty else pd.NA,
                "candidate_v5_original_market": first_available(v5, ["player_impact_original_market"]) if not v5.empty else pd.NA,
                "candidate_v5_action": first_available(v5, ["player_impact_adjustment_action"]) if not v5.empty else pd.NA,
                "candidate_v5_hint": first_available(v5, ["player_impact_market_translation_hint"]) if not v5.empty else pd.NA,
                "baseline_primary_risk": first_available(b, ["accuracy_primary_risk", "pick_primary_risk"]) if not b.empty else pd.NA,
                "candidate_v2_primary_risk": first_available(v2, ["accuracy_primary_risk", "pick_primary_risk"]) if not v2.empty else pd.NA,
                "candidate_v5_primary_risk": first_available(v5, ["accuracy_primary_risk", "pick_primary_risk"]) if not v5.empty else pd.NA,
            }
        )
    return pd.DataFrame(rows, columns=COMPARISON_COLUMNS)


def write_v5_report(path: Path, all_rows: pd.DataFrame, shortlist: pd.DataFrame, top: pd.DataFrame) -> None:
    actions = all_rows.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    lines = [
        "vSIGMA SHADOW CANDIDATE V5",
        "",
        "Layer: candidate v2 + conservative player impact.",
        "Status: experimental shadow; official baseline and candidate v2 outputs are not replaced.",
        "",
        f"Candidate v2 input rows: {len(all_rows)}",
        f"Candidate v5 competition shortlist rows: {len(shortlist)}",
        f"Candidate v5 competition top rows: {len(top)}",
        f"Player-impact adjustments made: {int(actions.ne(NOT_APPLIED).sum()) if len(actions) else 0}",
        "",
        "Player-impact action mix",
        actions.value_counts().to_string() if len(actions) else "No rows.",
        "",
        "Candidate v5 Top",
    ]
    if top.empty:
        lines.append("No v5 competition top picks survived.")
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
            "player_impact_adjustment_action",
            "player_impact_market_translation_hint",
        ]
        lines.append(top[[c for c in cols if c in top.columns]].to_string(index=False))
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_comparison_report(path: Path, baseline: pd.DataFrame, v2: pd.DataFrame, v5: pd.DataFrame, comparison: pd.DataFrame) -> None:
    actions = v5.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    lines = [
        "vSIGMA TODAY BASELINE VS CANDIDATE V2 VS CANDIDATE V5",
        "",
        "Baseline: official frozen Competition Accuracy Mode + Probability Calibration.",
        "Candidate v2: shadow schedule-strength + anomaly-cleaning layer.",
        "Candidate v5: candidate v2 + conservative player-impact layer.",
        "",
        f"Baseline official picks: {len(baseline)}",
        f"Candidate v2 shadow picks: {len(v2)}",
        f"Candidate v5 shadow picks: {len(v5)}",
        f"Candidate v5 player-impact adjustments in top: {int(actions.ne(NOT_APPLIED).sum()) if len(actions) else 0}",
        "",
        "Side-by-side picks",
        comparison.to_string(index=False) if not comparison.empty else "No compared rows.",
        "",
    ]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_shadow_run_report(
    path: Path,
    match_date: str,
    timezone_name: str,
    baseline_top: pd.DataFrame,
    candidate_v2_top: pd.DataFrame,
    candidate_v5_top: pd.DataFrame,
    all_rows: pd.DataFrame,
) -> None:
    actions = all_rows.get("player_impact_adjustment_action", pd.Series(dtype=object)).map(norm_upper)
    pd.DataFrame(
        [
            {
                "date": match_date,
                "timezone": timezone_name,
                "mode": V5_MODE_NAME,
                "baseline_competition_rows": int(len(baseline_top)),
                "candidate_v2_competition_rows": int(len(candidate_v2_top)),
                "candidate_v5_competition_rows": int(len(candidate_v5_top)),
                "player_impact_adjusted_rows": int(actions.ne(NOT_APPLIED).sum()) if len(actions) else 0,
                "player_impact_strengthened_rows": int(actions.eq(STRENGTHEN).sum()) if len(actions) else 0,
                "player_impact_downgraded_rows": int(actions.eq(DOWNGRADE_GOALS).sum()) if len(actions) else 0,
                "player_impact_blocked_rows": int(actions.eq(BLOCK_MARKET).sum()) if len(actions) else 0,
                "official_baseline_preserved": 1,
                "candidate_v2_preserved": 1,
                "run_finished_at": datetime.now(timezone.utc).isoformat(),
            }
        ]
    ).to_csv(path, index=False)


def build_candidate_v5_outputs(
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

    if candidate_v2_shortlist.empty:
        all_rows = empty_v5_frame(candidate_v2_top)
        shortlist = empty_v5_frame(candidate_v2_top)
        top = empty_v5_frame(candidate_v2_top)
    else:
        all_rows, shortlist, top = apply_player_impact_layer(candidate_v2_shortlist)

    shortlist_path = processed_dir / CANDIDATE_V5_SHORTLIST_CSV
    top_path = processed_dir / CANDIDATE_V5_TOP_CSV
    report_path = processed_dir / CANDIDATE_V5_REPORT_TXT
    comparison_path = processed_dir / COMPARISON_CSV
    comparison_report_path = processed_dir / COMPARISON_REPORT
    shadow_report_path = processed_dir / SHADOW_RUN_REPORT

    shortlist.to_csv(shortlist_path, index=False)
    top.to_csv(top_path, index=False)
    write_v5_report(report_path, all_rows, shortlist, top)
    comparison = build_three_way_comparison(baseline_top, candidate_v2_top, top)
    comparison.to_csv(comparison_path, index=False)
    write_comparison_report(comparison_report_path, baseline_top, candidate_v2_top, top, comparison)
    write_shadow_run_report(shadow_report_path, match_date, timezone_name, baseline_top, candidate_v2_top, top, all_rows)

    for path in [shortlist_path, top_path, report_path, comparison_path, comparison_report_path, shadow_report_path]:
        copy_if_exists(path, snapshot_dir)

    return {
        "candidate_v5_shortlist": shortlist_path,
        "candidate_v5_top": top_path,
        "candidate_v5_report": report_path,
        "comparison_csv": comparison_path,
        "comparison_report": comparison_report_path,
        "shadow_run_report": shadow_report_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build candidate v5 shadow outputs from candidate v2 plus player impact.")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--timezone", default="Atlantic/Canary")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    match_date = datetime.strptime(args.date, "%Y-%m-%d").date().isoformat()
    paths = build_candidate_v5_outputs(PROCESSED_DIR, TODAY_DIR, match_date, args.timezone)
    print("\n=== TODAY SHADOW CANDIDATE V5 COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")
    print("Official baseline and candidate v2 files preserved; v5 wrote separate outputs only.")


if __name__ == "__main__":
    main()
