from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = [
    "target_date", "generated_at", "portfolio_verdict", "premium_count", "review_count",
    "shadow_risk_count", "downgraded_count", "wait_count", "no_bet_count",
    "recommended_stance", "top_available_pick", "top_available_market", "top_available_status",
    "stake_guidance", "auto_apply", "production_change", "guardrail_status"
]
DETAIL_FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team", "market_primary",
    "adjusted_final_status", "stake_band", "portfolio_role", "portfolio_reason"
]


def norm(v: object) -> str:
    return "" if v is None else str(v).strip()


def up(v: object) -> str:
    return norm(v).upper()


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


def source_path(processed: Path, target_date: str) -> Path:
    p = processed / "today" / target_date / "vsigma_context_adjusted_final_picks.csv"
    if p.exists():
        return p
    return processed / "governance" / "vsigma_context_adjusted_final_picks.csv"


def role_for(status: str) -> tuple[str, str]:
    s = up(status)
    if s == "BET_KEEP":
        return "PREMIUM_CANDIDATE", "clean context-adjusted keep"
    if s == "BET_REVIEW":
        return "REVIEW_SINGLE", "positive but not premium"
    if s == "SHADOW_RISK_ONLY":
        return "LOW_STAKE_OR_LIVE_ONLY", "shadow-risk row, do not place in serious slip"
    if s == "WAIT_PRELOCK":
        return "WAIT_ONLY", "needs prelock confirmation"
    if s == "BET_DOWNGRADED_TO_REVIEW":
        return "DOWNGRADED_NO_PREMIUM", "base BET downgraded by context or availability"
    return "NO_BET", "not eligible for execution"


def build_details(target_date: str, generated_at: str, rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for i, row in enumerate(rows, start=1):
        role, reason = role_for(row.get("adjusted_final_status"))
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": norm(row.get("final_rank")) or i,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "market_primary": up(row.get("market_primary")),
            "adjusted_final_status": up(row.get("adjusted_final_status")),
            "stake_band": up(row.get("stake_band")),
            "portfolio_role": role,
            "portfolio_reason": reason,
        })
    return out


def count_status(rows: list[dict[str, str]], *statuses: str) -> int:
    wanted = {up(s) for s in statuses}
    return sum(1 for r in rows if up(r.get("adjusted_final_status")) in wanted)


def portfolio_summary(target_date: str, generated_at: str, rows: list[dict[str, str]], details: list[dict[str, object]]) -> dict[str, object]:
    premium = count_status(rows, "BET_KEEP")
    review = count_status(rows, "BET_REVIEW")
    shadow = count_status(rows, "SHADOW_RISK_ONLY")
    downgraded = count_status(rows, "BET_DOWNGRADED_TO_REVIEW")
    wait = count_status(rows, "WAIT_PRELOCK")
    no_bet = count_status(rows, "NO_BET_CONTEXT", "NO_BET_BASE")

    if premium > 0:
        verdict = "PREMIUM_AVAILABLE"
        stance = "Use only premium candidates, after normal prelock checks."
        stake = "NORMAL_IF_PRELOCK_OK"
    elif review > 0:
        verdict = "REVIEW_ONLY"
        stance = "No premium; manual review only."
        stake = "LOW"
    elif shadow > 0:
        verdict = "LOW_STAKE_OR_LIVE_ONLY"
        stance = "No premium; only low/symbolic stake or live confirmation."
        stake = "LOW_OR_SYMBOLIC"
    elif wait > 0:
        verdict = "WAIT_PRELOCK_ONLY"
        stance = "No prematch execution; wait for prelock."
        stake = "NO_PREMATCH_STAKE"
    else:
        verdict = "NO_PREMIUM_NO_BET"
        stance = "No serious bet from the adjusted portfolio."
        stake = "NO_STAKE"

    eligible = [d for d in details if d["portfolio_role"] in {"PREMIUM_CANDIDATE", "REVIEW_SINGLE", "LOW_STAKE_OR_LIVE_ONLY"}]
    top = eligible[0] if eligible else {}
    top_pick = f"{top.get('home_team', '')} vs {top.get('away_team', '')}" if top else "NONE"

    return {
        "target_date": target_date,
        "generated_at": generated_at,
        "portfolio_verdict": verdict,
        "premium_count": premium,
        "review_count": review,
        "shadow_risk_count": shadow,
        "downgraded_count": downgraded,
        "wait_count": wait,
        "no_bet_count": no_bet,
        "recommended_stance": stance,
        "top_available_pick": top_pick,
        "top_available_market": top.get("market_primary", "NONE"),
        "top_available_status": top.get("adjusted_final_status", "NONE"),
        "stake_guidance": stake,
        "auto_apply": "NO",
        "production_change": "NO",
        "guardrail_status": "FINAL_PORTFOLIO_VERDICT_REPORT_ONLY",
    }


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, summary: dict[str, object], details: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Final Portfolio Verdict - {target_date}",
        "",
        "## Executive Verdict",
        f"- portfolio_verdict: {summary['portfolio_verdict']}",
        f"- recommended_stance: {summary['recommended_stance']}",
        f"- stake_guidance: {summary['stake_guidance']}",
        f"- top_available_pick: {summary['top_available_pick']} — {summary['top_available_market']} ({summary['top_available_status']})",
        f"- role_counts: {counts(details, 'portfolio_role')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Portfolio Rows",
    ]
    if not details:
        lines.append("- none")
    for d in details:
        lines.append(f"- #{d['rank']} | {d['portfolio_role']} | {d['home_team']} vs {d['away_team']} | market={d['market_primary']} | adjusted={d['adjusted_final_status']} | stake={d['stake_band']} | reason={d['portfolio_reason']}")
    lines += ["", "## Guardrails", "- This report does not place bets or alter production outputs.", "- It is the final operator-facing portfolio interpretation after context and availability gates."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    rows = read_rows(source_path(processed, target_date))
    details = build_details(target_date, generated_at, rows)
    summary = portfolio_summary(target_date, generated_at, rows, details)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_final_portfolio_verdict.csv", [summary], FIELDS)
        write_rows(base / "vsigma_final_portfolio_verdict_details.csv", details, DETAIL_FIELDS)
        (base / "vsigma_final_portfolio_verdict.md").write_text(md(target_date, summary, details), encoding="utf-8")
    print("=== VSIGMA FINAL PORTFOLIO VERDICT ===")
    print(f"portfolio_verdict={summary['portfolio_verdict']}")
    print(f"role_counts={counts(details, 'portfolio_role')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
