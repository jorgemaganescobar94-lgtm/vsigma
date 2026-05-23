from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
OVERRIDES = Path("data/context/manual_objective_overrides.csv")
FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "league", "home_team", "away_team",
    "market_primary", "base_recommendation", "objective_override_status", "home_objective_status",
    "away_objective_status", "objective_edge", "context_gate_decision", "context_gate_reason",
    "recommended_action", "home_urgency_score", "away_urgency_score", "home_rank", "away_rank",
    "auto_apply", "production_change", "guardrail_status"
]

SIDE_HOME = {"HOME_WIN", "HOME_DNB", "HOME_TEAM_TOTAL", "HOME_OVER_0_5", "HOME_OVER_1_5"}
SIDE_AWAY = {"AWAY_WIN", "AWAY_DNB", "AWAY_TEAM_TOTAL", "AWAY_OVER_0_5", "AWAY_OVER_1_5"}
GOALS = {"OVER_1_5", "OVER_2_5", "BTTS_YES"}


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


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def picks_path(processed: Path, target_date: str) -> Path:
    p = processed / "today" / target_date / "vsigma_today_execution_bets_only.csv"
    return p if p.exists() else processed / "vsigma_today_execution_bets_only.csv"


def override_index(root: Path) -> dict[tuple[str, str], dict[str, str]]:
    rows = read_rows(root / OVERRIDES)
    out: dict[tuple[str, str], dict[str, str]] = {}
    for r in rows:
        key = (norm(r.get("target_date"))[:10], norm(r.get("fixture_id")).replace(".0", ""))
        if key[0] and key[1]:
            out[key] = r
    return out


def side(market: str) -> str:
    m = up(market)
    if m in SIDE_HOME:
        return "HOME"
    if m in SIDE_AWAY:
        return "AWAY"
    if m in GOALS:
        return "BOTH"
    return "UNKNOWN"


def proxy_objective(row: dict[str, str]) -> tuple[str, str, str, str]:
    h = num(row.get("home_urgency_score"), 0)
    a = num(row.get("away_urgency_score"), 0)
    s = side(row.get("market_primary"))
    if s == "HOME" and h > a:
        return "PROXY_ONLY", "TABLE_PROXY_HOME_EDGE", "HOME", "table proxy supports home side"
    if s == "HOME" and a > h:
        return "PROXY_ONLY", "TABLE_PROXY_CONFLICT", "AWAY", "table proxy favors away side"
    if s == "AWAY" and a > h:
        return "PROXY_ONLY", "TABLE_PROXY_AWAY_EDGE", "AWAY", "table proxy supports away side"
    if s == "AWAY" and h > a:
        return "PROXY_ONLY", "TABLE_PROXY_CONFLICT", "HOME", "table proxy favors home side"
    if s == "BOTH" and (h > 0 or a > 0):
        return "PROXY_ONLY", "TABLE_PROXY_TEMPO", "TEMPO", "table proxy supports tempo"
    return "PROXY_ONLY", "OBJECTIVE_NEUTRAL_OR_UNKNOWN", "NEUTRAL", "no strong objective proxy"


def decide(row: dict[str, str], override: dict[str, str] | None) -> tuple[str, str, str, str, str, str, str]:
    market = up(row.get("market_primary"))
    if override:
        h_obj = up(override.get("home_objective_status"))
        a_obj = up(override.get("away_objective_status"))
        edge = up(override.get("objective_edge")) or "NEUTRAL"
        note = norm(override.get("objective_note"))
        if h_obj == "NO_STRONG_OBJECTIVE" and a_obj == "NO_STRONG_OBJECTIVE":
            if market in SIDE_HOME | SIDE_AWAY:
                return "REAL_OVERRIDE", h_obj, a_obj, edge, "CONTEXT_DOWNGRADE", note or "real context says no strong objective edge", "Downgrade side market; do not treat ranking proxy as motivation"
            return "REAL_OVERRIDE", h_obj, a_obj, edge, "CONTEXT_NEUTRAL_KEEP_MONITOR", note or "real context neutral", "Keep only if stats/market/live support remains strong"
        if edge == "HOME" and market in SIDE_HOME:
            return "REAL_OVERRIDE", h_obj, a_obj, edge, "OBJECTIVE_SUPPORTS_PICK", note, "Objective supports pick"
        if edge == "AWAY" and market in SIDE_AWAY:
            return "REAL_OVERRIDE", h_obj, a_obj, edge, "OBJECTIVE_SUPPORTS_PICK", note, "Objective supports pick"
        if edge in {"HOME", "AWAY"} and market in SIDE_HOME | SIDE_AWAY:
            return "REAL_OVERRIDE", h_obj, a_obj, edge, "OBJECTIVE_CONFLICT", note, "Manual context conflicts with side market"
        return "REAL_OVERRIDE", h_obj, a_obj, edge, "CONTEXT_REVIEW", note, "Manual context available; review market fit"
    mode, status, edge, reason = proxy_objective(row)
    return mode, "PROXY", "PROXY", edge, status, reason, "No real objective override available"


def build(target_date: str, timezone: str, processed: Path, root: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    overrides = override_index(root)
    rows = [r for r in read_rows(picks_path(processed, target_date)) if up(r.get("final_recommendation")) == "BET"]
    out: list[dict[str, object]] = []
    for r in rows:
        fid = norm(r.get("fixture_id")).replace(".0", "")
        o = overrides.get((target_date, fid))
        mode, h_obj, a_obj, edge, decision, reason, action = decide(r, o)
        out.append({
            "target_date": target_date,
            "generated_at": generated_at,
            "rank": norm(r.get("execution_rank")) or len(out) + 1,
            "fixture_id": fid,
            "league": norm(r.get("league")),
            "home_team": norm(r.get("home_team")),
            "away_team": norm(r.get("away_team")),
            "market_primary": up(r.get("market_primary")),
            "base_recommendation": up(r.get("final_recommendation")),
            "objective_override_status": mode,
            "home_objective_status": h_obj,
            "away_objective_status": a_obj,
            "objective_edge": edge,
            "context_gate_decision": decision,
            "context_gate_reason": reason,
            "recommended_action": action,
            "home_urgency_score": norm(r.get("home_urgency_score")),
            "away_urgency_score": norm(r.get("away_urgency_score")),
            "home_rank": norm(r.get("home_rank")),
            "away_rank": norm(r.get("away_rank")),
            "auto_apply": "NO",
            "production_change": "NO",
            "guardrail_status": "REAL_OBJECTIVE_CONTEXT_REPORT_ONLY",
        })
    return out


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(r.get(field) or "UNKNOWN") for r in rows)
    return "; ".join(f"{k}={v}" for k, v in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Real Objective Context Gate - {target_date}", "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- context_gate_decision_counts: {counts(rows, 'context_gate_decision')}",
        f"- objective_override_status_counts: {counts(rows, 'objective_override_status')}",
        "- auto_apply: NO",
        "- production_change: NO", "",
        "## Rows",
    ]
    for r in rows:
        lines.append(f"- #{r['rank']} | {r['context_gate_decision']} | {r['home_team']} vs {r['away_team']} | market={r['market_primary']} | override={r['objective_override_status']} | edge={r['objective_edge']} | action={r['recommended_action']}")
    lines += ["", "## Guardrails", "- Real context overrides ranking urgency proxy.", "- This report does not change production picks automatically."]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path, root: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed, root)
    for base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(base / "vsigma_real_objective_context_gate.csv", rows)
        (base / "vsigma_real_objective_context_gate.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA REAL OBJECTIVE CONTEXT GATE ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"context_gate_decision_counts={counts(rows, 'context_gate_decision')}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--date", required=True)
    p.add_argument("--timezone", default="Atlantic/Canary")
    p.add_argument("--processed-dir", type=Path, default=PROCESSED)
    p.add_argument("--root", type=Path, default=Path("."))
    a = p.parse_args()
    run(a.date, a.timezone, a.processed_dir, a.root)


if __name__ == "__main__":
    main()
