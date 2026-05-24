from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
DETAIL_FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team", "market_primary",
    "base_result", "base_profit_units", "adjusted_status", "stake_band", "audit_label",
    "audit_effect_units", "audit_reason", "auto_apply", "production_change"
]
SUMMARY_FIELDS = [
    "target_date", "generated_at", "base_bets", "base_wins", "base_losses", "base_profit_units",
    "adjusted_counted_bets", "adjusted_wins", "adjusted_losses", "adjusted_profit_units",
    "avoided_loss_units", "missed_win_units", "kept_win_units", "net_adjustment_delta_units",
    "audit_verdict", "auto_apply", "production_change"
]
COUNTED_ADJUSTED = {"BET_KEEP", "BET_REVIEW", "SHADOW_RISK_ONLY"}
DOWNGRADED = {"BET_DOWNGRADED_TO_REVIEW", "NO_BET_CONTEXT", "NO_BET_BASE", "WAIT_PRELOCK"}


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


def num(v: object, default: float = 0.0) -> float:
    try:
        text = norm(v)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_rows(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({field: r.get(field, "") for field in fields})


def file_for(processed: Path, target_date: str, filename: str) -> Path:
    p = processed / "today" / target_date / filename
    if p.exists():
        return p
    return processed / "governance" / filename


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for r in rows:
        fid = norm(r.get("fixture_id")).replace(".0", "")
        if fid and fid not in out:
            out[fid] = r
    return out


def label(adjusted: str, result: str, profit: float) -> tuple[str, float, str]:
    a = up(adjusted)
    r = up(result)
    if a in COUNTED_ADJUSTED and r == "WIN":
        return "KEPT_WIN", profit, "adjusted portfolio kept a winning candidate"
    if a in COUNTED_ADJUSTED and r == "LOSS":
        return "KEPT_LOSS", profit, "adjusted portfolio kept a losing candidate"
    if a in DOWNGRADED and r == "LOSS":
        return "AVOIDED_LOSS", abs(profit), "adjusted portfolio would have avoided a base loss"
    if a in DOWNGRADED and r == "WIN":
        return "MISSED_WIN", -profit, "adjusted portfolio would have missed a base win"
    if a in DOWNGRADED:
        return "DOWNGRADED_OTHER", 0.0, "adjusted portfolio downgraded a non-win/loss result"
    return "UNCLASSIFIED", 0.0, "no audit classification"


def build(target_date: str, timezone: str, processed: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    result_rows = read_rows(file_for(processed, target_date, "vsigma_execution_shortlist_results_ledger.csv"))
    adjusted_rows = read_rows(file_for(processed, target_date, "vsigma_context_adjusted_final_picks.csv"))
    adjusted = index_by_fixture(adjusted_rows)

    details: list[dict[str, object]] = []
    for i, row in enumerate(result_rows, start=1):
        fid = norm(row.get("fixture_id")).replace(".0", "")
        adj = adjusted.get(fid, {})
        result = up(row.get("actionable_result")) or up(row.get("primary_result"))
        profit = num(row.get("actionable_profit_units"), num(row.get("primary_profit_units"), 0))
        adjusted_status = up(adj.get("adjusted_final_status")) or "NO_ADJUSTED_ROW"
        audit_label, effect, reason = label(adjusted_status, result, profit)
        details.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": i,
            "fixture_id": fid,
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "market_primary": up(row.get("market_primary")),
            "base_result": result,
            "base_profit_units": profit,
            "adjusted_status": adjusted_status,
            "stake_band": up(adj.get("stake_band")),
            "audit_label": audit_label,
            "audit_effect_units": round(effect, 6),
            "audit_reason": reason,
            "auto_apply": "NO",
            "production_change": "NO",
        })

    base_bets = len(details)
    base_wins = sum(1 for d in details if d["base_result"] == "WIN")
    base_losses = sum(1 for d in details if d["base_result"] == "LOSS")
    base_profit = round(sum(float(d["base_profit_units"]) for d in details), 6)
    counted = [d for d in details if d["adjusted_status"] in COUNTED_ADJUSTED]
    adjusted_wins = sum(1 for d in counted if d["base_result"] == "WIN")
    adjusted_losses = sum(1 for d in counted if d["base_result"] == "LOSS")
    adjusted_profit = round(sum(float(d["base_profit_units"]) for d in counted), 6)
    avoided = round(sum(float(d["audit_effect_units"]) for d in details if d["audit_label"] == "AVOIDED_LOSS"), 6)
    missed = round(-sum(float(d["audit_effect_units"]) for d in details if d["audit_label"] == "MISSED_WIN"), 6)
    kept = round(sum(float(d["base_profit_units"]) for d in details if d["audit_label"] == "KEPT_WIN"), 6)
    delta = round(adjusted_profit - base_profit, 6)

    if adjusted_profit > base_profit and avoided >= missed:
        verdict = "CONTEXT_FILTER_IMPROVED_DAY"
    elif adjusted_profit < base_profit and missed > avoided:
        verdict = "CONTEXT_FILTER_TOO_CONSERVATIVE"
    else:
        verdict = "CONTEXT_FILTER_MIXED"

    summary = {
        "target_date": target_date,
        "generated_at": generated_at,
        "base_bets": base_bets,
        "base_wins": base_wins,
        "base_losses": base_losses,
        "base_profit_units": base_profit,
        "adjusted_counted_bets": len(counted),
        "adjusted_wins": adjusted_wins,
        "adjusted_losses": adjusted_losses,
        "adjusted_profit_units": adjusted_profit,
        "avoided_loss_units": avoided,
        "missed_win_units": missed,
        "kept_win_units": kept,
        "net_adjustment_delta_units": delta,
        "audit_verdict": verdict,
        "auto_apply": "NO",
        "production_change": "NO",
    }
    return summary, details


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, summary: dict[str, object], details: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Context Adjustment Result Auditor - {target_date}",
        "",
        "## Executive Audit",
        f"- audit_verdict: {summary['audit_verdict']}",
        f"- base: {summary['base_wins']}W-{summary['base_losses']}L, profit={summary['base_profit_units']}u",
        f"- adjusted counted: {summary['adjusted_wins']}W-{summary['adjusted_losses']}L, profit={summary['adjusted_profit_units']}u",
        f"- avoided_loss_units: {summary['avoided_loss_units']}",
        f"- missed_win_units: {summary['missed_win_units']}",
        f"- net_adjustment_delta_units: {summary['net_adjustment_delta_units']}",
        f"- audit_label_counts: {counts(details, 'audit_label')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Detail Rows",
    ]
    for d in details:
        lines.append(f"- #{d['rank']} | {d['audit_label']} | {d['home_team']} vs {d['away_team']} | market={d['market_primary']} | base={d['base_result']} {d['base_profit_units']}u | adjusted={d['adjusted_status']} | effect={d['audit_effect_units']}u")
    lines += ["", "## Guardrails", "- This audit does not rewrite historical results.", "- Use repeated audits before changing thresholds or context rules."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    summary, details = build(target_date, timezone, processed)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_context_adjustment_result_auditor.csv", [summary], SUMMARY_FIELDS)
        write_rows(base / "vsigma_context_adjustment_result_auditor_details.csv", details, DETAIL_FIELDS)
        (base / "vsigma_context_adjustment_result_auditor.md").write_text(md(target_date, summary, details), encoding="utf-8")
    print("=== VSIGMA CONTEXT ADJUSTMENT RESULT AUDITOR ===")
    print(f"audit_verdict={summary['audit_verdict']}")
    print(f"net_adjustment_delta_units={summary['net_adjustment_delta_units']}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
