from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = ["target_date","generated_at","rank","fixture_id","home_team","away_team","market_primary","context_level","context_score","matrix_policy","audit_memory_level","final_portfolio_status","stake_guidance","operator_note","auto_apply","production_change"]
SUMMARY_FIELDS = ["target_date","generated_at","portfolio_verdict","rows_reviewed","status_counts","recommended_stance","top_pick","top_market","top_status","auto_apply","production_change"]


def n(v: object) -> str:
    return "" if v is None else str(v).strip()


def u(v: object) -> str:
    return n(v).upper()


def read(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as h:
        return [dict(r) for r in csv.DictReader(h)]


def write(path: Path, data: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        for r in data:
            w.writerow({k: r.get(k, "") for k in fields})


def dated_matrix_path(base: Path, day: str) -> Path:
    return base / "today" / day / "vsigma_context_level_matrix.csv"


def dated_adjusted_path(base: Path, day: str) -> Path:
    return base / "today" / day / "vsigma_context_adjusted_final_picks.csv"


def classify(row: dict[str, str]) -> tuple[str, str, str]:
    lvl = u(row.get("context_level"))
    mem = u(row.get("memory_level"))
    market = u(row.get("market_primary"))
    if lvl in {"L9_MAX_BLOCK", "L8_HARD_DOWN"}:
        if mem == "MEM_MISSED_WIN":
            return "NO_ACTION_SOFTEN_WATCH", "NO_STAKE", "No action now, but track as missed-win soften candidate."
        return "NO_ACTION_CONTEXT", "NO_STAKE", "Context matrix blocks this pick."
    if lvl == "L7_SOFT_DOWN":
        return "LIVE_ONLY_OR_SYMBOLIC", "SYMBOLIC_ONLY", "Soft downgrade; only live confirmation or symbolic stake."
    if lvl == "L6_REVIEW":
        return "REVIEW_ONLY", "LOW_IF_CONFIRMED", "Review only; low stake only with price/prelock/live confirmation."
    if lvl == "L5_EDGE_ONLY":
        return "EDGE_ONLY_REVIEW", "LOW", "No context edge; allow only if price/stat edge remains strong."
    if lvl in {"L4_CAUTION", "L3_OK"}:
        return "CONTEXT_OK_CANDIDATE", "NORMAL_IF_PRELOCK_OK", "Candidate survives context matrix."
    if lvl in {"L2_SUPPORT", "L1_LOCK"}:
        return "CONTEXT_SUPPORTED_CANDIDATE", "NORMAL_OR_PLUS_IF_ALL_GATES_OK", "Context supports the pick; still require normal gates."
    if market:
        return "MATRIX_UNKNOWN_REVIEW", "LOW", "Unknown matrix level; manual review."
    return "NO_ACTION", "NO_STAKE", "No actionable row."


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def empty_summary(day: str, gen: str, verdict: str, reason: str) -> dict[str, object]:
    return {
        "target_date": day,
        "generated_at": gen,
        "portfolio_verdict": verdict,
        "rows_reviewed": 0,
        "status_counts": "none",
        "recommended_stance": reason,
        "top_pick": "NONE",
        "top_market": "NONE",
        "top_status": "NONE",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, base: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    gen = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    adjusted_source = dated_adjusted_path(base, day)
    if not adjusted_source.exists():
        reason = f"No dated adjusted final picks found at {adjusted_source}; refusing portfolio build because matrix may be stale. Run vsigma_context_adjusted_final_picks first."
        return empty_summary(day, gen, "INPUT_MISSING_ADJUSTED_PICKS", reason), []

    matrix_source = dated_matrix_path(base, day)
    if not matrix_source.exists():
        reason = f"No dated context matrix found at {matrix_source}; refusing stale governance fallback. Run vsigma_context_level_matrix for this date first."
        return empty_summary(day, gen, "INPUT_MISSING_DATE_GUARD", reason), []

    matrix_all = read(matrix_source)
    matrix = [r for r in matrix_all if n(r.get("target_date"))[:10] in {"", day}]
    stale = [r for r in matrix_all if n(r.get("target_date"))[:10] not in {"", day}]
    if stale:
        reason = "Dated context matrix contains rows from another target_date; refusing mixed-date portfolio."
        return empty_summary(day, gen, "MIXED_DATE_MATRIX_BLOCKED", reason), []

    rows: list[dict[str, object]] = []
    for i, r in enumerate(matrix, start=1):
        status, stake, note = classify(r)
        rows.append({
            "target_date": day,
            "generated_at": gen,
            "rank": n(r.get("rank")) or i,
            "fixture_id": n(r.get("fixture_id")),
            "home_team": n(r.get("home_team")),
            "away_team": n(r.get("away_team")),
            "market_primary": u(r.get("market_primary")),
            "context_level": u(r.get("context_level")),
            "context_score": n(r.get("context_score")),
            "matrix_policy": n(r.get("policy")),
            "audit_memory_level": u(r.get("memory_level")),
            "final_portfolio_status": status,
            "stake_guidance": stake,
            "operator_note": note,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    order = {"CONTEXT_SUPPORTED_CANDIDATE":0,"CONTEXT_OK_CANDIDATE":1,"EDGE_ONLY_REVIEW":2,"REVIEW_ONLY":3,"LIVE_ONLY_OR_SYMBOLIC":4,"NO_ACTION_SOFTEN_WATCH":5,"NO_ACTION_CONTEXT":6,"NO_ACTION":7}
    rows.sort(key=lambda r: (order.get(str(r["final_portfolio_status"]), 99), int(r.get("rank") or 999)))
    active = [r for r in rows if r["final_portfolio_status"] not in {"NO_ACTION_CONTEXT","NO_ACTION_SOFTEN_WATCH","NO_ACTION"}]
    if any(r["final_portfolio_status"] in {"CONTEXT_SUPPORTED_CANDIDATE","CONTEXT_OK_CANDIDATE"} for r in active):
        verdict = "ACTIONABLE_CANDIDATE_AVAILABLE"
        stance = "Use only candidates that survive context matrix and normal prelock gates."
    elif any(r["final_portfolio_status"] == "REVIEW_ONLY" for r in active):
        verdict = "REVIEW_ONLY_PORTFOLIO"
        stance = "No premium; review/live/low stake only."
    elif any(r["final_portfolio_status"] == "LIVE_ONLY_OR_SYMBOLIC" for r in active):
        verdict = "LIVE_OR_SYMBOLIC_ONLY"
        stance = "No prematch serious bet. Live or symbolic only."
    elif not rows:
        verdict = "NO_MATRIX_ROWS"
        stance = "No context matrix rows found for the date."
    else:
        verdict = "NO_ACTION_PORTFOLIO"
        stance = "No serious action after context matrix."
    top = active[0] if active else {}
    summary = {"target_date": day,"generated_at": gen,"portfolio_verdict": verdict,"rows_reviewed": len(rows),"status_counts": counts(rows,"final_portfolio_status"),"recommended_stance": stance,"top_pick": (f"{top.get('home_team')} vs {top.get('away_team')}" if top else "NONE"),"top_market": top.get("market_primary","NONE"),"top_status": top.get("final_portfolio_status","NONE"),"auto_apply":"NO","production_change":"NO"}
    return summary, rows


def md(day: str, summary: dict[str, object], rows: list[dict[str, object]]) -> str:
    lines = [f"# vSIGMA Context Matrix Portfolio v2 - {day}","","## Executive Verdict",f"- portfolio_verdict: {summary['portfolio_verdict']}",f"- recommended_stance: {summary['recommended_stance']}",f"- top_pick: {summary['top_pick']} - {summary['top_market']} ({summary['top_status']})",f"- status_counts: {summary['status_counts']}","- auto_apply: NO","- production_change: NO","","## Portfolio Rows"]
    if not rows:
        lines.append("- none")
    for r in rows:
        lines.append(f"- #{r['rank']} | {r['final_portfolio_status']} | {r['home_team']} vs {r['away_team']} | market={r['market_primary']} | level={r['context_level']} | stake={r['stake_guidance']} | note={r['operator_note']}")
    lines += ["", "## Guardrails", "- This report refuses stale governance fallback when dated inputs are missing.", "- Run dated context adjusted final picks and dated context level matrix before this portfolio report."]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    summary, rows = build(day, tz, base)
    for b in [base / "today" / day, base / "governance"]:
        write(b / "vsigma_context_matrix_portfolio_v2.csv", [summary], SUMMARY_FIELDS)
        write(b / "vsigma_context_matrix_portfolio_v2_details.csv", rows, FIELDS)
        (b / "vsigma_context_matrix_portfolio_v2.md").write_text(md(day, summary, rows), encoding="utf-8")
    print("=== VSIGMA CONTEXT MATRIX PORTFOLIO V2 ===")
    print(f"portfolio_verdict={summary['portfolio_verdict']}")
    print(f"status_counts={summary['status_counts']}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir)


if __name__ == "__main__":
    main()
