from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
TRANSLATOR_FIELDS = [
    "target_date", "generated_at", "rank", "fixture_id", "home_team", "away_team",
    "forecast_confidence", "forecast_warning", "portfolio_status", "context_level", "market_hint",
    "stat_profile", "primary_stat_market", "secondary_stat_market", "execution_permission",
    "stake_band", "translation_score", "translation_reason", "kill_switch", "source_guard",
    "auto_apply", "production_change",
]
REPORT_FIELDS = [
    "target_date", "generated_at", "fixture_id", "home_team", "away_team",
    "candidate_origin", "max_execution_permission", "before_permission", "after_permission",
    "before_stake", "after_stake", "ceiling_action", "reason", "auto_apply", "production_change",
]
PERMISSION_ORDER = {
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


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = fixture_id(row)
        if fid and fid not in out:
            out[fid] = row
    return out


def should_cap(current: str, maximum: str) -> bool:
    return PERMISSION_ORDER.get(up(current), 99) > PERMISSION_ORDER.get(up(maximum), 0)


def stake_for(permission: str) -> str:
    p = up(permission)
    if p == "NO_BET":
        return "NO_STAKE"
    if p in {"NO_BET_OR_WATCH", "STAT_WATCH_ONLY"}:
        return "NO_STAKE_OR_SYMBOLIC"
    if p == "LIVE_ONLY":
        return "SYMBOLIC_ONLY"
    return "LOW_IF_CONFIRMED"


def apply(day: str, tz: str, base: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    folder = base / "today" / day
    translator_rows = read_rows(folder / "vsigma_forecast_market_translator.csv")
    ledger = index_by_fixture(read_rows(folder / "vsigma_candidate_provenance_ledger.csv"))
    report: list[dict[str, str]] = []

    for row in translator_rows:
        fid = fixture_id(row)
        prov = ledger.get(fid, {})
        maximum = up(prov.get("max_execution_permission")) or "NO_BET"
        origin = up(prov.get("candidate_origin")) or "UNKNOWN_ORIGIN"
        before_permission = up(row.get("execution_permission"))
        before_stake = up(row.get("stake_band"))
        if prov and should_cap(before_permission, maximum):
            row["execution_permission"] = maximum
            row["stake_band"] = stake_for(maximum)
            if maximum == "NO_BET":
                row["primary_stat_market"] = "NO_CLEAR_STAT_MARKET"
                row["secondary_stat_market"] = "NONE"
                row["kill_switch"] = "CANDIDATE_PROVENANCE_CEILING"
                row["translation_score"] = str(min(int(float(norm(row.get("translation_score")) or -34)), -34))
            row["translation_reason"] = (
                norm(row.get("translation_reason"))
                + f"; candidate_provenance_ceiling=max_permission={maximum}; origin={origin}"
            ).strip("; ")
            row["source_guard"] = (up(row.get("source_guard")) + "; CANDIDATE_PROVENANCE_CEILING").strip("; ")
            action = "CAPPED"
            reason = f"permission {before_permission} exceeded provenance ceiling {maximum} from {origin}"
        else:
            action = "NO_CHANGE"
            reason = "permission already within provenance ceiling or ledger missing"

        report.append(
            {
                "target_date": day,
                "generated_at": generated_at,
                "fixture_id": fid,
                "home_team": norm(row.get("home_team")),
                "away_team": norm(row.get("away_team")),
                "candidate_origin": origin,
                "max_execution_permission": maximum,
                "before_permission": before_permission,
                "after_permission": up(row.get("execution_permission")),
                "before_stake": before_stake,
                "after_stake": up(row.get("stake_band")),
                "ceiling_action": action,
                "reason": reason,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )
    return translator_rows, report


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter = Counter(norm(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def translator_md(day: str, rows: list[dict[str, str]]) -> str:
    lines = [
        f"# vSIGMA Forecast-to-Market Translator - {day}",
        "",
        "## Summary",
        f"- rows_translated: {len(rows)}",
        f"- execution_permission_counts: {counts(rows, 'execution_permission')}",
        f"- primary_market_counts: {counts(rows, 'primary_stat_market')}",
        "- calibration_note: v68.2 candidate provenance ceiling applied after market translation.",
        "- source_guard: DATED_INPUT_ONLY",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Translated Rows",
    ]
    if not rows:
        lines.append("- none. Need dated match stat forecasts first.")
    for row in rows:
        lines.append(
            f"- #{row.get('rank')} | {row.get('execution_permission')} | {row.get('home_team')} vs {row.get('away_team')} | "
            f"primary={row.get('primary_stat_market')} | secondary={row.get('secondary_stat_market')} | "
            f"score={row.get('translation_score')} | stake={row.get('stake_band')} | kill={row.get('kill_switch')} | reason={row.get('translation_reason')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This translator does not execute bets.",
        "- Candidate provenance ceiling can only downgrade or preserve permissions.",
        "- Final execution still requires price/prelock/live confirmation.",
    ]
    return "\n".join(lines) + "\n"


def report_md(day: str, rows: list[dict[str, str]]) -> str:
    lines = [
        f"# vSIGMA Candidate Provenance Ceiling - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(rows)}",
        f"- ceiling_action_counts: {counts(rows, 'ceiling_action')}",
        f"- candidate_origin_counts: {counts(rows, 'candidate_origin')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Ceiling Rows",
    ]
    if not rows:
        lines.append("- none. Translator or provenance ledger rows missing.")
    for row in rows:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | origin={row['candidate_origin']} | max={row['max_execution_permission']} | "
            f"permission={row['before_permission']} -> {row['after_permission']} | stake={row['before_stake']} -> {row['after_stake']} | action={row['ceiling_action']} | reason={row['reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Ceiling enforcement is diagnostic/safety governance only.",
        "- It can never upgrade a candidate beyond its provenance ceiling.",
        "- Proxy-origin rows are capped at NO_BET unless future real-data recovery produces a real-source row.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    translator_rows, report_rows = apply(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write_rows(out_base / "vsigma_forecast_market_translator.csv", translator_rows, TRANSLATOR_FIELDS)
        (out_base / "vsigma_forecast_market_translator.md").write_text(translator_md(day, translator_rows), encoding="utf-8")
        write_rows(out_base / "vsigma_candidate_provenance_ceiling.csv", report_rows, REPORT_FIELDS)
        (out_base / "vsigma_candidate_provenance_ceiling.md").write_text(report_md(day, report_rows), encoding="utf-8")
    print("=== VSIGMA CANDIDATE PROVENANCE CEILING ===")
    print(f"rows_reviewed={len(report_rows)}")
    print(f"ceiling_action_counts={counts(report_rows, 'ceiling_action')}")
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
