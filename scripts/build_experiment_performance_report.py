from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient
    from update_immutable_daily_ledger import LEDGER_CSV, LEDGER_DIR, REGISTRY_PATH, load_experiment_registry
except ModuleNotFoundError:
    from scripts.daily_hardening import PROCESSED_DIR, format_markdown_table, read_csv_lenient
    from scripts.update_immutable_daily_ledger import LEDGER_CSV, LEDGER_DIR, REGISTRY_PATH, load_experiment_registry


SUMMARY_CSV = LEDGER_DIR / "vsigma_experiment_performance_summary.csv"
REPORT_MD = LEDGER_DIR / "vsigma_experiment_performance_report.md"


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def counts_mix(series: pd.Series) -> str:
    values: list[str] = []
    for raw in series.dropna().astype(str):
        for part in raw.replace("|", ";").split(";"):
            item = part.strip()
            if item:
                values.append(item)
    if not values:
        return ""
    counts = pd.Series(values).value_counts()
    return "; ".join(f"{idx}:{int(value)}" for idx, value in counts.items())


def max_drawdown_by_date(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    work = df.copy()
    work["profit_num"] = numeric(work.get("profit_units", pd.Series(dtype=object))).fillna(0.0)
    daily = work.groupby("target_date", dropna=False)["profit_num"].sum().reset_index()
    daily = daily.sort_values("target_date")
    cumulative = daily["profit_num"].cumsum()
    drawdown = cumulative - cumulative.cummax()
    return round(float(drawdown.min()), 6) if not drawdown.empty else 0.0


def brier_score(df: pd.DataFrame) -> float | str:
    work = df.copy()
    work["prob"] = numeric(work.get("calibrated_probability", pd.Series(dtype=object)))
    result = work.get("result", pd.Series(dtype=object)).astype(str).str.upper()
    mask = work["prob"].notna() & result.isin(["WIN", "LOSS"])
    if not mask.any():
        return ""
    outcome = result[mask].map({"WIN": 1.0, "LOSS": 0.0})
    return round(float(((work.loc[mask, "prob"] - outcome) ** 2).mean()), 6)


def summarize_experiment(experiment: dict[str, Any], ledger: pd.DataFrame) -> dict[str, object]:
    exp_id = experiment["experiment_id"]
    rows = ledger[ledger["experiment_id"].astype(str).eq(exp_id)].copy() if not ledger.empty else pd.DataFrame()
    pick_rows = rows[~rows.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy() if not rows.empty else rows
    no_bet_rows = rows[rows.get("record_status", pd.Series(dtype=object)).astype(str).eq("NO_BET_RECORD")].copy() if not rows.empty else rows
    result = pick_rows.get("result", pd.Series(dtype=object)).astype(str).str.upper() if not pick_rows.empty else pd.Series(dtype=object)
    record_status = pick_rows.get("record_status", pd.Series(dtype=object)).astype(str).str.upper() if not pick_rows.empty else pd.Series(dtype=object)
    settled_mask = record_status.isin(["SETTLED", "VOID"]) | result.isin(["WIN", "LOSS", "PUSH", "VOID"])
    settled = pick_rows[settled_mask].copy() if not pick_rows.empty else pick_rows
    profit = numeric(settled.get("profit_units", pd.Series(dtype=object))).fillna(0.0) if not settled.empty else pd.Series(dtype=float)
    wins = int(result.eq("WIN").sum()) if not result.empty else 0
    losses = int(result.eq("LOSS").sum()) if not result.empty else 0
    pushes = int(result.eq("PUSH").sum()) if not result.empty else 0
    voids = int(result.eq("VOID").sum()) if not result.empty else 0
    decided = wins + losses
    profit_units = round(float(profit.sum()), 6) if not profit.empty else 0.0
    roi = round((profit_units / len(settled)) * 100.0, 6) if len(settled) else ""
    avg_prob = numeric(pick_rows.get("calibrated_probability", pd.Series(dtype=object))).mean() if not pick_rows.empty else pd.NA
    return {
        "experiment_id": exp_id,
        "display_name": experiment.get("display_name", exp_id),
        "status": experiment.get("status", ""),
        "selection_role": experiment.get("selection_role", ""),
        "allowed_to_select_officially": experiment.get("allowed_to_select_officially", False),
        "total_days_observed": int(rows["target_date"].nunique()) if not rows.empty and "target_date" in rows.columns else 0,
        "pick_days": int(pick_rows["target_date"].nunique()) if not pick_rows.empty and "target_date" in pick_rows.columns else 0,
        "no_bet_days": int(no_bet_rows["target_date"].nunique()) if not no_bet_rows.empty and "target_date" in no_bet_rows.columns else 0,
        "picks_total": int(len(pick_rows)),
        "settled_picks": int(len(settled)),
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "voids": voids,
        "hit_rate": round((wins / decided) * 100.0, 6) if decided else "",
        "profit_units": profit_units,
        "roi_percent": roi,
        "average_calibrated_probability": round(float(avg_prob), 6) if not pd.isna(avg_prob) else "",
        "brier_score": brier_score(settled),
        "max_drawdown": max_drawdown_by_date(settled),
        "market_mix": counts_mix(pick_rows.get("market_primary", pd.Series(dtype=object))) if not pick_rows.empty else "",
        "failure_mode_mix": counts_mix(pick_rows.get("risk_tags", pd.Series(dtype=object))) if not pick_rows.empty else "",
        "current_verdict": experiment.get("current_verdict", ""),
    }


def build_performance_report(
    processed_dir: Path = PROCESSED_DIR,
    ledger_path: Path = LEDGER_CSV,
    registry_path: Path = REGISTRY_PATH,
) -> dict[str, Path]:
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    registry = load_experiment_registry(registry_path)
    ledger = read_csv_lenient(ledger_path)
    summary = pd.DataFrame([summarize_experiment(exp, ledger) for exp in registry.values()])
    summary.to_csv(SUMMARY_CSV, index=False)

    official = summary[summary["experiment_id"].astype(str).eq("OFFICIAL_BASELINE")]
    shadows = summary[~summary["experiment_id"].astype(str).eq("OFFICIAL_BASELINE")]
    lines = [
        "# vSIGMA Experiment Performance Report",
        "",
        f"- Generated for ledger: {ledger_path}",
        f"- Registry: {registry_path}",
        "",
        "## Official Baseline",
        format_markdown_table(official, max_rows=10),
        "",
        "## Shadow / Audit Experiments",
        format_markdown_table(shadows, max_rows=20),
        "",
        "## Official vs Shadow Comparison",
        format_markdown_table(summary, ["experiment_id", "status", "picks_total", "settled_picks", "wins", "losses", "profit_units", "roi_percent", "current_verdict"], max_rows=20),
        "",
        "Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    return {"summary": SUMMARY_CSV, "report": REPORT_MD}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build vSIGMA experiment performance from the immutable daily ledger.")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED_DIR)
    parser.add_argument("--ledger-path", type=Path, default=LEDGER_CSV)
    parser.add_argument("--registry-path", type=Path, default=REGISTRY_PATH)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = build_performance_report(args.processed_dir, args.ledger_path, args.registry_path)
    print("\n=== EXPERIMENT PERFORMANCE REPORT COMPLETADO ===")
    for label, path in paths.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
