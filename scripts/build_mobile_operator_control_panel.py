from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
FIELDS = ["target_date", "generated_at", "card", "status", "detail", "next_action"]


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in FIELDS} for row in rows])


def day_path(day: str, filename: str) -> Path:
    return PROCESSED / "today" / day / filename


def gov_path(filename: str) -> Path:
    return PROCESSED / "governance" / filename


def source(day: str, filename: str) -> tuple[list[dict[str, str]], str]:
    today = day_path(day, filename)
    rows = read_csv(today)
    if rows:
        return rows, str(today)
    gov = gov_path(filename)
    return read_csv(gov), str(gov)


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter = Counter(n(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def section_status(rows: list[dict[str, str]], section: str) -> str:
    for row in rows:
        if row.get("section") == section:
            return n(row.get("status")) or "UNKNOWN"
    return "UNKNOWN"


def metric_list(rows: list[dict[str, str]], field: str, values: set[str]) -> str:
    metrics: list[str] = []
    for row in rows:
        if row.get(field) in values:
            metric = n(row.get("metric")) or "UNKNOWN"
            if metric not in metrics:
                metrics.append(metric)
    return ",".join(metrics) if metrics else "none"


def decide_panel_status(
    action_level: str,
    alert_route: str,
    guard_status: str,
    guard_allowed: str,
    learning_sanity: str,
    shadow_active_count: int,
    promotion_candidates: int,
) -> tuple[str, str, str]:
    if guard_allowed == "NO" or guard_status == "BLOCK_COMMIT" or alert_route == "CRITICAL_STOP" or action_level == "BROKEN":
        return "STOP", "NO", "Fix blocking guard/operator issue before trusting outputs."
    if action_level == "REVIEW_NOW":
        return "REVIEW_NOW", "MANUAL_ONLY", "Manual review required; no automatic execution."
    if action_level == "LIVE":
        return "LIVE_WAIT", "MANUAL_ONLY", "Wait/use live validator before any manual live decision."
    if promotion_candidates > 0:
        return "CALIBRATION_REVIEW", "NO", "Promotion candidate exists; manual calibration review only."
    if learning_sanity == "WARN" or guard_status == "WARN":
        return "WARN", "NO", "Review sanity/guard warnings before using learning outputs."
    if shadow_active_count > 0:
        return "WATCH_SHADOW", "NO", "Shadow tests active; no stake or production change."
    if action_level == "WATCH":
        return "WATCH_ONLY", "NO", "Watch-only day; no official stake."
    return "OK", "NO", "No operator action required."


def build(day: str, tz: str) -> tuple[list[dict[str, str]], dict[str, str]]:
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    operator_rows, operator_source = source(day, "vsigma_operator_brief.csv")
    shadow_rows, shadow_source = source(day, "vsigma_calibration_shadow_patch_queue.csv")
    readiness_rows, readiness_source = source(day, "vsigma_shadow_patch_promotion_readiness.csv")
    sanity_rows, sanity_source = source(day, "vsigma_learning_chain_output_sanity.csv")
    guard_rows, guard_source = source(day, "vsigma_learning_chain_empty_output_guard.csv")

    action_level = section_status(operator_rows, "operator_action_level")
    final_decision = section_status(operator_rows, "operator_compact_summary")
    alert_route = section_status(operator_rows, "operator_alert_route")
    operator_sanity = section_status(operator_rows, "operator_sanity_check")

    shadow_active = [row for row in shadow_rows if row.get("queue_decision") in {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}]
    shadow_high = [row for row in shadow_active if row.get("shadow_priority") == "HIGH"]
    promotion_candidates = [row for row in readiness_rows if row.get("readiness_decision") == "PROMOTION_CANDIDATE_MANUAL_REVIEW"]
    keep_shadow = [row for row in readiness_rows if row.get("readiness_decision") == "KEEP_SHADOW_TEST"]

    guard_status = "NO_GUARD"
    guard_allowed = "UNKNOWN"
    if guard_rows:
        if any(row.get("commit_allowed") == "NO" for row in guard_rows):
            guard_status = "BLOCK_COMMIT"
            guard_allowed = "NO"
        elif any(row.get("guard_decision") == "WARN_ONLY" for row in guard_rows):
            guard_status = "WARN"
            guard_allowed = "YES"
        else:
            guard_status = "PASS"
            guard_allowed = "YES"

    if any(row.get("severity") in {"WARN", "ERROR", "CRITICAL"} for row in sanity_rows):
        learning_sanity = "WARN"
    elif sanity_rows:
        learning_sanity = "PASS"
    else:
        learning_sanity = "UNAVAILABLE"

    panel_status, betting_permission, next_action = decide_panel_status(
        action_level,
        alert_route,
        guard_status,
        guard_allowed,
        learning_sanity,
        len(shadow_active),
        len(promotion_candidates),
    )

    rows = [
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "MOBILE_STATUS",
            "status": panel_status,
            "detail": f"betting_permission={betting_permission}; final_decision={final_decision}; action_level={action_level}; alert_route={alert_route}",
            "next_action": next_action,
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "OPERATOR",
            "status": action_level,
            "detail": f"final_decision={final_decision}; alert_route={alert_route}; sanity={operator_sanity}",
            "next_action": "Read operator brief only if status is REVIEW_NOW/LIVE/STOP.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "LEARNING_GUARD",
            "status": guard_status,
            "detail": f"commit_allowed={guard_allowed}; decisions={counts(guard_rows, 'guard_decision')}",
            "next_action": "If BLOCK_COMMIT, rerun/fix learning chain before trusting outputs.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "LEARNING_SANITY",
            "status": learning_sanity,
            "detail": f"sanity={counts(sanity_rows, 'sanity_status')}; severity={counts(sanity_rows, 'severity')}",
            "next_action": "Review warnings before calibration decisions.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "SHADOW_QUEUE",
            "status": "ACTIVE" if shadow_active else "INACTIVE_OR_STABLE",
            "detail": f"active={len(shadow_active)}; high={len(shadow_high)}; metrics={metric_list(shadow_rows, 'queue_decision', {'PROMOTE_TO_SHADOW_TEST', 'PATCH_CANDIDATE'})}; decisions={counts(shadow_rows, 'queue_decision')}",
            "next_action": "Shadow only; no production change.",
        },
        {
            "target_date": day,
            "generated_at": generated_at,
            "card": "PROMOTION_READINESS",
            "status": "MANUAL_REVIEW_CANDIDATE" if promotion_candidates else "KEEP_SHADOW_TEST" if keep_shadow else "NO_PROMOTION",
            "detail": f"promotion_candidates={len(promotion_candidates)}; decisions={counts(readiness_rows, 'readiness_decision')}",
            "next_action": "Manual review only if promotion candidate appears.",
        },
    ]

    meta = {
        "generated_at": generated_at,
        "panel_status": panel_status,
        "betting_permission": betting_permission,
        "next_action": next_action,
        "action_level": action_level,
        "final_decision": final_decision,
        "alert_route": alert_route,
        "operator_sanity": operator_sanity,
        "guard_status": guard_status,
        "guard_allowed": guard_allowed,
        "learning_sanity": learning_sanity,
        "shadow_active": str(len(shadow_active)),
        "shadow_high": str(len(shadow_high)),
        "shadow_metrics": metric_list(shadow_rows, "queue_decision", {"PROMOTE_TO_SHADOW_TEST", "PATCH_CANDIDATE"}),
        "promotion_candidates": str(len(promotion_candidates)),
        "promotion_decisions": counts(readiness_rows, "readiness_decision"),
        "operator_source": operator_source,
        "shadow_source": shadow_source,
        "readiness_source": readiness_source,
        "sanity_source": sanity_source,
        "guard_source": guard_source,
    }
    return rows, meta


def md(day: str, rows: list[dict[str, str]], meta: dict[str, str]) -> str:
    lines = [
        f"# vSIGMA Mobile Operator Control Panel - {day}",
        "",
        "## Top Verdict",
        f"- mobile_status: {meta['panel_status']}",
        f"- betting_permission: {meta['betting_permission']}",
        f"- next_action: {meta['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## At a Glance",
        f"- action_level: {meta['action_level']}",
        f"- final_decision: {meta['final_decision']}",
        f"- alert_route: {meta['alert_route']}",
        f"- operator_sanity: {meta['operator_sanity']}",
        f"- hard_guard: {meta['guard_status']} | commit_allowed={meta['guard_allowed']}",
        f"- learning_sanity: {meta['learning_sanity']}",
        f"- shadow_active: {meta['shadow_active']} | high={meta['shadow_high']} | metrics={meta['shadow_metrics']}",
        f"- promotion_candidates: {meta['promotion_candidates']} | decisions={meta['promotion_decisions']}",
        "",
        "## Cards",
    ]
    for row in rows:
        lines.append(f"- {row['card']} | status={row['status']} | {row['detail']} | next={row['next_action']}")
    lines += [
        "",
        "## Mobile Sources",
        f"- operator: {meta['operator_source']}",
        f"- shadow_queue: {meta['shadow_source']}",
        f"- promotion_readiness: {meta['readiness_source']}",
        f"- learning_sanity: {meta['sanity_source']}",
        f"- hard_guard: {meta['guard_source']}",
        "",
        "## Guardrails",
        "- This panel is read-only governance.",
        "- It does not execute bets.",
        "- It does not edit forecast formulas.",
        "- It does not enable production changes.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, meta = build(day, tz)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        write_csv(base / "vsigma_mobile_operator_control_panel.csv", rows)
        (base / "vsigma_mobile_operator_control_panel.md").write_text(md(day, rows, meta), encoding="utf-8")
    print("=== VSIGMA MOBILE OPERATOR CONTROL PANEL ===")
    print(f"mobile_status={meta['panel_status']}")
    print(f"betting_permission={meta['betting_permission']}")
    print(f"next_action={meta['next_action']}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
