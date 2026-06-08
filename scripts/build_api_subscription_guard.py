from __future__ import annotations

import argparse
import csv
import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

PROCESSED = Path("data/processed")
STATUS_URL = "https://v3.football.api-sports.io/status"

FIELDS = [
    "target_date",
    "generated_at",
    "api_status",
    "subscription_plan",
    "subscription_active",
    "subscription_end",
    "requests_current",
    "requests_limit_day",
    "requests_remaining",
    "api_calls_allowed",
    "executor_mode",
    "recommended_executor_limit",
    "guard_reason",
    "auto_apply",
    "production_change",
]

def get_key() -> str:
    for name in (
        "API_FOOTBALL_KEY",
        "APISPORTS_KEY",
        "API_SPORTS_KEY",
        "APIFOOTBALL_KEY",
        "API_FOOTBALL_API_KEY",
    ):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""

def as_int(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default

def decide(plan: str, active: bool, current: int, limit_day: int) -> tuple[str, str, int, str]:
    remaining = max(limit_day - current, 0)
    plan_up = (plan or "").upper()

    if not active:
        return "NO", "SKIP_API_EXECUTION", 0, "subscription not active"

    if limit_day <= 0:
        return "NO", "SKIP_API_EXECUTION", 0, "no daily request limit available"

    if remaining <= 20:
        return "NO", "SKIP_API_EXECUTION", 0, f"only {remaining} requests remaining; reserve protected"

    if "FREE" in plan_up or limit_day <= 100:
        safe_rows = max(1, min(2, (remaining - 20) // 6))
        if safe_rows <= 0:
            return "NO", "SKIP_API_EXECUTION", 0, f"free plan remaining={remaining}; not enough reserve"
        return "YES", "FREE_SAFE_EXECUTION", safe_rows, f"free plan detected; limit executor to {safe_rows} fixtures"

    if "PRO" in plan_up or (limit_day >= 7500 and limit_day < 50000):
        # 250 fixtures × ~6 endpoints = ~1500 requests/run, leaving large reserve.
        safe_rows = max(1, min(250, (remaining - 500) // 6))
        if safe_rows <= 0:
            return "NO", "SKIP_API_EXECUTION", 0, f"pro plan remaining={remaining}; not enough reserve"
        return "YES", "PRO_CONTROLLED_EXECUTION", safe_rows, f"pro plan detected; limit executor to {safe_rows} fixtures"

    if "ULTRA" in plan_up or limit_day >= 50000:
        return "YES", "MAX_COVERAGE_EXECUTION", 0, f"high-capacity plan detected; remaining={remaining}"

    safe_rows = max(1, min(50, (remaining - 100) // 6))
    if safe_rows <= 0:
        return "NO", "SKIP_API_EXECUTION", 0, f"remaining={remaining}; not enough safe reserve"
    return "YES", "LIMITED_EXECUTION", safe_rows, f"unknown active plan; conservative limit={safe_rows}"

def fetch_status() -> tuple[dict, str, str | None]:
    key = get_key()
    if not key:
        return {}, "MISSING_KEY", "No API key found in environment"

    try:
        response = requests.get(
            STATUS_URL,
            headers={"x-apisports-key": key},
            timeout=30,
        )
    except Exception as exc:
        return {}, "HTTP_ERROR", str(exc)

    if response.status_code != 200:
        return {}, f"HTTP_{response.status_code}", response.text[:500]

    try:
        return response.json(), "OK", None
    except Exception as exc:
        return {}, "BAD_JSON", str(exc)

def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in FIELDS} for row in rows])

def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA API Subscription Guard - {row['target_date']}",
        "",
        "## Summary",
        f"- api_status: {row['api_status']}",
        f"- subscription_plan: {row['subscription_plan']}",
        f"- subscription_active: {row['subscription_active']}",
        f"- subscription_end: {row['subscription_end']}",
        f"- requests_current: {row['requests_current']}",
        f"- requests_limit_day: {row['requests_limit_day']}",
        f"- requests_remaining: {row['requests_remaining']}",
        f"- api_calls_allowed: {row['api_calls_allowed']}",
        f"- executor_mode: {row['executor_mode']}",
        f"- recommended_executor_limit: {row['recommended_executor_limit']}",
        f"- guard_reason: {row['guard_reason']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Guardrails",
        "- This guard never creates picks, stake, or market recommendations.",
        "- Free/Pro execution is capped to avoid exhausting daily quota.",
        "- Expired, forbidden, missing-key, or low-remaining quota states skip real API execution.",
        "- Account personal details from the API status response are intentionally not written.",
        "",
    ]) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")

    payload, api_status, error = fetch_status()
    response = payload.get("response", {}) if isinstance(payload, dict) else {}
    subscription = response.get("subscription", {}) if isinstance(response, dict) else {}
    requests_obj = response.get("requests", {}) if isinstance(response, dict) else {}

    plan = str(subscription.get("plan", "") or "")
    active = bool(subscription.get("active", False))
    end = str(subscription.get("end", "") or "")
    current = as_int(requests_obj.get("current"), 0)
    limit_day = as_int(requests_obj.get("limit_day"), 0)
    remaining = max(limit_day - current, 0)

    if api_status == "OK":
        allowed, mode, recommended_limit, reason = decide(plan, active, current, limit_day)
    else:
        allowed, mode, recommended_limit, reason = "NO", "SKIP_API_EXECUTION", 0, error or api_status

    row = {
        "target_date": day,
        "generated_at": generated,
        "api_status": api_status,
        "subscription_plan": plan or "UNKNOWN",
        "subscription_active": "YES" if active else "NO",
        "subscription_end": end,
        "requests_current": current,
        "requests_limit_day": limit_day,
        "requests_remaining": remaining,
        "api_calls_allowed": allowed,
        "executor_mode": mode,
        "recommended_executor_limit": recommended_limit,
        "guard_reason": reason,
        "auto_apply": "NO",
        "production_change": "NO",
    }

    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_subscription_guard.csv", [row])
        (base / "vsigma_api_subscription_guard.md").write_text(md(row), encoding="utf-8")

    print("=== VSIGMA API SUBSCRIPTION GUARD ===")
    print(f"api_status={row['api_status']}")
    print(f"subscription_plan={row['subscription_plan']}")
    print(f"requests_remaining={row['requests_remaining']}")
    print(f"api_calls_allowed={row['api_calls_allowed']}")
    print(f"executor_mode={row['executor_mode']}")
    print(f"recommended_executor_limit={row['recommended_executor_limit']}")
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
