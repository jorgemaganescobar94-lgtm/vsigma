from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

LEDGER_FIELDS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "home_team",
    "away_team",
    "market",
    "candidate_origin",
    "market_direction_source",
    "max_execution_permission",
    "real_data_strength",
    "proxy_reason",
    "allowed_downstream_use",
    "source_files",
    "auto_apply",
    "production_change",
]

PERMISSION_RANK = {
    "NO_BET": 0,
    "NO_BET_OR_WATCH": 1,
    "STAT_WATCH_ONLY": 2,
    "LIVE_ONLY": 3,
    "REVIEW_ONLY": 4,
    "REVIEW_LOW_STAKE": 5,
    "PRELOCK_REVIEW_LOW_STAKE": 5,
}


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def num(value: object, default: float = 0.0) -> float:
    try:
        text = norm(value)
        if not text or text.lower() == "nan":
            return default
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_rows(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def day_rows(rows: list[dict[str, str]], target_date: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        row_day = norm(row.get("target_date") or row.get("date"))[:10]
        if row_day in {"", target_date}:
            out.append(row)
    return out


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = fixture_id(row)
        if fid and fid not in out:
            out[fid] = row
    return out


def market_direction(market: str) -> str:
    m = up(market)
    if m.startswith("OVER") or "TEMPO" in m:
        return "OVER_TEMPO"
    if m.startswith("UNDER") or "NO_GOALS" in m:
        return "UNDER_CONTROL"
    if "BTTS" in m:
        return "BTTS"
    if "CORNERS" in m:
        return "CORNERS"
    if "CARDS" in m:
        return "CARDS"
    if "WIN" in m or "DNB" in m:
        return "SIDE_WIN"
    return "UNKNOWN"


def origin_and_reason(short: dict[str, str] | None, real: dict[str, str] | None, translator: dict[str, str] | None) -> tuple[str, str, str]:
    marker = ""
    if short:
        marker = up(short.get("bridge_source")) + " " + up(short.get("guardrail_status"))
    if "BASE_PROXY_FROM_OBJECTIVE_GATE" in marker or "VSIGMA_REAL_OBJECTIVE_CONTEXT_GATE" in marker:
        return "OBJECTIVE_PROXY", "objective context bridge created diagnostic shortlist row", "vsigma_real_objective_context_gate.csv; vsigma_today_execution_shortlist.csv"
    if short and up(short.get("final_recommendation")) == "BET":
        return "REAL_SHORTLIST", "dated shortlist row marked BET", "vsigma_today_execution_shortlist.csv"
    if translator:
        return "TRANSLATOR_ONLY", "translator row exists without identifiable shortlist origin", "vsigma_forecast_market_translator.csv"
    if real:
        return "DIAGNOSTIC_PROXY", "real objective context row exists but no shortlist/translator origin", "vsigma_real_objective_context_gate.csv"
    return "UNKNOWN_ORIGIN", "no source provenance found", "unknown"


def max_permission(origin: str, real_strength: int) -> str:
    if origin in {"OBJECTIVE_PROXY", "DIAGNOSTIC_PROXY"}:
        return "NO_BET"
    if origin == "REAL_SHORTLIST" and real_strength >= 75:
        return "REVIEW_LOW_STAKE"
    if origin == "REAL_SHORTLIST" and real_strength >= 60:
        return "LIVE_ONLY"
    if origin == "REAL_SHORTLIST":
        return "STAT_WATCH_ONLY"
    return "NO_BET"


def real_data_strength(short: dict[str, str] | None, forecast: dict[str, str] | None, portfolio: dict[str, str] | None, objective: dict[str, str] | None) -> int:
    score = 0
    if short:
        score += 12
        if up(short.get("guardrail_status")).startswith("BASE_PROXY"):
            score -= 10
        if up(short.get("recent_stats_quality_flag")) == "FULL":
            score += 18
        elif up(short.get("recent_stats_quality_flag")) == "PROXY":
            score += 3
        if num(short.get("odds_bookmaker_support_count"), 0) >= 4:
            score += 12
        if up(short.get("lineup_quality_flag")) in {"FULL", "LINEUPS_CONFIRMED"}:
            score += 12
        if up(short.get("lineup_activation_state")) == "INACTIVE":
            score -= 8
    if forecast:
        score += 12
        conf = up(forecast.get("forecast_confidence"))
        if conf == "HIGH":
            score += 18
        elif conf == "MEDIUM":
            score += 10
        elif conf == "LOW":
            score -= 4
    if portfolio:
        score += 12
        level = up(portfolio.get("context_level"))
        if level in {"L1_LOCK", "L2_SUPPORT", "L3_OK", "L4_CAUTION"}:
            score += 12
        elif level in {"L8_HARD_DOWN", "L9_MAX_BLOCK"}:
            score -= 18
    if objective:
        score += 8
        if up(objective.get("objective_override_status")) == "PROXY_ONLY":
            score -= 4
    return max(0, min(100, int(round(score))))


def allowed_use(origin: str, max_perm: str, strength: int) -> str:
    if origin in {"OBJECTIVE_PROXY", "DIAGNOSTIC_PROXY"}:
        return "DIAGNOSTIC_ONLY_NO_MARKET_PERMISSION"
    if max_perm == "NO_BET":
        return "NO_BET_ONLY"
    if max_perm == "STAT_WATCH_ONLY":
        return "WATCH_ONLY_NO_STAKE"
    if max_perm == "LIVE_ONLY":
        return "LIVE_CONFIRMATION_REQUIRED"
    return "MANUAL_PRELOCK_REVIEW_REQUIRED"


def build(target_date: str, timezone: str, processed: Path) -> list[dict[str, object]]:
    generated_at = datetime.now(ZoneInfo(timezone)).isoformat(timespec="seconds")
    base = processed / "today" / target_date
    short = index_by_fixture(day_rows(read_rows(base / "vsigma_today_execution_shortlist.csv"), target_date))
    real = index_by_fixture(day_rows(read_rows(base / "vsigma_real_objective_context_gate.csv"), target_date))
    translator = index_by_fixture(day_rows(read_rows(base / "vsigma_forecast_market_translator.csv"), target_date))
    forecast = index_by_fixture(day_rows(read_rows(base / "vsigma_match_stat_forecasts.csv"), target_date))
    portfolio = index_by_fixture(day_rows(read_rows(base / "vsigma_context_matrix_portfolio_v2_details.csv"), target_date))
    fixture_ids = sorted(set(short) | set(real) | set(translator) | set(forecast) | set(portfolio))
    rows: list[dict[str, object]] = []
    for fid in fixture_ids:
        source = short.get(fid) or translator.get(fid) or real.get(fid) or forecast.get(fid) or portfolio.get(fid) or {}
        market = norm((translator.get(fid) or {}).get("primary_stat_market")) or norm((short.get(fid) or real.get(fid) or {}).get("market_primary")) or "UNKNOWN"
        origin, reason, source_files = origin_and_reason(short.get(fid), real.get(fid), translator.get(fid))
        strength = real_data_strength(short.get(fid), forecast.get(fid), portfolio.get(fid), real.get(fid))
        ceiling = max_permission(origin, strength)
        rows.append(
            {
                "target_date": target_date,
                "generated_at": generated_at,
                "fixture_id": fid,
                "home_team": norm(source.get("home_team")),
                "away_team": norm(source.get("away_team")),
                "market": market,
                "candidate_origin": origin,
                "market_direction_source": market_direction(market),
                "max_execution_permission": ceiling,
                "real_data_strength": strength,
                "proxy_reason": reason,
                "allowed_downstream_use": allowed_use(origin, ceiling, strength),
                "source_files": source_files,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )
    return rows


def counts(rows: list[dict[str, object]], field: str) -> str:
    c = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in c.most_common()) if c else "none"


def md(target_date: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Candidate Provenance Ledger - {target_date}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- candidate_origin_counts: {counts(rows, 'candidate_origin')}",
        f"- max_execution_permission_counts: {counts(rows, 'max_execution_permission')}",
        f"- allowed_downstream_use_counts: {counts(rows, 'allowed_downstream_use')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Candidate Rows",
    ]
    if not rows:
        lines.append("- none. No candidate rows found across shortlist/objective/translator/forecast sources.")
    for row in rows:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | origin={row['candidate_origin']} | market={row['market']} | "
            f"direction={row['market_direction_source']} | max_permission={row['max_execution_permission']} | "
            f"strength={row['real_data_strength']} | allowed={row['allowed_downstream_use']} | reason={row['proxy_reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Provenance ledger is diagnostic and ceiling-only; it never upgrades candidates.",
        "- OBJECTIVE_PROXY and DIAGNOSTIC_PROXY rows are capped at NO_BET.",
        "- Real shortlist rows still require downstream gates, price, lineups and manual review.",
    ]
    return "\n".join(lines) + "\n"


def run(target_date: str, timezone: str, processed: Path) -> None:
    target_date = date.fromisoformat(target_date).isoformat()
    rows = build(target_date, timezone, processed)
    for out_base in [processed / "today" / target_date, processed / "governance"]:
        write_rows(out_base / "vsigma_candidate_provenance_ledger.csv", rows, LEDGER_FIELDS)
        (out_base / "vsigma_candidate_provenance_ledger.md").write_text(md(target_date, rows), encoding="utf-8")
    print("=== VSIGMA CANDIDATE PROVENANCE LEDGER ===")
    print(f"rows_reviewed={len(rows)}")
    print(f"candidate_origin_counts={counts(rows, 'candidate_origin')}")
    print(f"max_execution_permission_counts={counts(rows, 'max_execution_permission')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
