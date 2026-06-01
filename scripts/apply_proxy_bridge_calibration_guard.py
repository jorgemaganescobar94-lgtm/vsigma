from __future__ import annotations

import argparse
import csv
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
    "target_date", "generated_at", "fixture_id", "home_team", "away_team", "market_hint",
    "before_primary", "after_primary", "before_permission", "after_permission", "guard_action",
    "reason", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def num(value: object, default: int = 0) -> int:
    try:
        return int(float(norm(value)))
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_rows(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def proxy_fixtures(base: Path, day: str) -> set[str]:
    path = base / "today" / day / "vsigma_today_execution_shortlist.csv"
    out: set[str] = set()
    for row in read_rows(path):
        marker = up(row.get("bridge_source")) + " " + up(row.get("guardrail_status"))
        if "VSIGMA_REAL_OBJECTIVE_CONTEXT_GATE" in marker or "BASE_PROXY_FROM_OBJECTIVE_GATE" in marker:
            fid = fixture_id(row)
            if fid:
                out.add(fid)
    return out


def is_tempo_or_over_hint(row: dict[str, str]) -> bool:
    hint = up(row.get("market_hint"))
    return hint.startswith("OVER") or hint.startswith("BTTS") or "TEMPO" in hint


def is_inversion(row: dict[str, str]) -> bool:
    primary = up(row.get("primary_stat_market"))
    secondary = up(row.get("secondary_stat_market"))
    return primary.startswith("UNDER") or primary in {"NO_GOALS_AGGRESSION"} or secondary == "NO_GOALS_AGGRESSION"


def apply_guard(day: str, tz: str, base: Path) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    translator_path = base / "today" / day / "vsigma_forecast_market_translator.csv"
    rows = read_rows(translator_path)
    proxy_ids = proxy_fixtures(base, day)
    report: list[dict[str, str]] = []

    for row in rows:
        fid = fixture_id(row)
        before_primary = up(row.get("primary_stat_market"))
        before_permission = up(row.get("execution_permission"))
        if fid in proxy_ids and is_tempo_or_over_hint(row) and is_inversion(row):
            row["primary_stat_market"] = "NO_CLEAR_STAT_MARKET"
            row["secondary_stat_market"] = "NONE"
            row["execution_permission"] = "NO_BET"
            row["stake_band"] = "NO_STAKE"
            row["translation_score"] = str(min(num(row.get("translation_score"), -34), -34))
            row["kill_switch"] = "PROXY_BRIDGE_INVERSION_BLOCK"
            row["translation_reason"] = (
                norm(row.get("translation_reason"))
                + "; proxy_bridge_calibration_guard=blocked inversion from tempo/over proxy into under/no-goals market"
            ).strip("; ")
            source_guard = up(row.get("source_guard"))
            row["source_guard"] = (source_guard + "; PROXY_BRIDGE_CALIBRATION_GUARD").strip("; ")
            action = "BLOCKED_INVERSION"
            reason = "proxy objective-context tempo/over source cannot be inverted into under/no-goals market"
        else:
            action = "NO_CHANGE"
            reason = "not a proxy inversion"

        report.append(
            {
                "target_date": day,
                "generated_at": generated_at,
                "fixture_id": fid,
                "home_team": norm(row.get("home_team")),
                "away_team": norm(row.get("away_team")),
                "market_hint": up(row.get("market_hint")),
                "before_primary": before_primary,
                "after_primary": up(row.get("primary_stat_market")),
                "before_permission": before_permission,
                "after_permission": up(row.get("execution_permission")),
                "guard_action": action,
                "reason": reason,
                "auto_apply": "NO",
                "production_change": "NO",
            }
        )

    return rows, report


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter: dict[str, int] = {}
    for row in rows:
        key = norm(row.get(field)) or "UNKNOWN"
        counter[key] = counter.get(key, 0) + 1
    return "; ".join(f"{key}={value}" for key, value in counter.items()) if counter else "none"


def translator_md(day: str, rows: list[dict[str, str]]) -> str:
    lines = [
        f"# vSIGMA Forecast-to-Market Translator - {day}",
        "",
        "## Summary",
        f"- rows_translated: {len(rows)}",
        f"- execution_permission_counts: {counts(rows, 'execution_permission')}",
        f"- primary_market_counts: {counts(rows, 'primary_stat_market')}",
        "- calibration_note: v68.1 blocks proxy-bridge inversion from tempo/over source into under/no-goals market.",
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
        "- Proxy bridge rows can support diagnostics only; they cannot invert tempo/over thesis into under/no-goals markets.",
        "- Final execution still requires price/prelock/live confirmation.",
    ]
    return "\n".join(lines) + "\n"


def guard_md(day: str, report: list[dict[str, str]]) -> str:
    lines = [
        f"# vSIGMA Proxy Bridge Calibration Guard - {day}",
        "",
        "## Summary",
        f"- rows_reviewed: {len(report)}",
        f"- guard_action_counts: {counts(report, 'guard_action')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guard Rows",
    ]
    if not report:
        lines.append("- none. Translator rows missing or no proxy rows detected.")
    for row in report:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | action={row['guard_action']} | "
            f"market_hint={row['market_hint']} | before={row['before_primary']} -> after={row['after_primary']} | "
            f"permission={row['before_permission']} -> {row['after_permission']} | reason={row['reason']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- Diagnostic/post-processing only; no stake permission is added.",
        "- The guard can only downgrade or preserve rows, never upgrade them.",
        "- It specifically blocks under/no-goals inversion created from objective-context proxy tempo/over rows.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, report = apply_guard(day, tz, base)
    for out_base in [base / "today" / day, base / "governance"]:
        write_rows(out_base / "vsigma_forecast_market_translator.csv", rows, TRANSLATOR_FIELDS)
        (out_base / "vsigma_forecast_market_translator.md").write_text(translator_md(day, rows), encoding="utf-8")
        write_rows(out_base / "vsigma_proxy_bridge_calibration_guard.csv", report, REPORT_FIELDS)
        (out_base / "vsigma_proxy_bridge_calibration_guard.md").write_text(guard_md(day, report), encoding="utf-8")
    print("=== VSIGMA PROXY BRIDGE CALIBRATION GUARD ===")
    print(f"rows_reviewed={len(report)}")
    print(f"guard_action_counts={counts(report, 'guard_action')}")
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
