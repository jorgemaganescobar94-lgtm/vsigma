from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path("data/processed")
LEDGER = ROOT / "ledger" / "vsigma_alert_state.csv"
STATE_FIELDS = ["target_date", "title", "severity", "alert_hash"]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def meta(text: str, key: str) -> str:
    m = re.search(rf"-\s*{re.escape(key)}:\s*([^\n]+)", text)
    return m.group(1).strip() if m else "UNKNOWN"


def signal_lines(text: str) -> list[str]:
    keys = [
        "BROKEN", "READY_LOW_STAKE_REVIEW", "LIVE_ONLY_WAIT_TRIGGER",
        "LIVE_TRIGGER_CONFIRMED", "LIVE_TRIGGER_REJECTED", "TOO_LATE",
        "MATCH_FINISHED", "PATCH_CANDIDATE_REVIEW", "API_CREDENTIALS_MISSING",
        "REFRESH_SKIPPED_NO_API_CREDENTIALS",
    ]
    lines = [line.strip() for line in text.splitlines() if any(k in line for k in keys)]
    return sorted(set(lines))


def read_state() -> list[dict[str, str]]:
    if not LEDGER.exists():
        return []
    with LEDGER.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def previous_hash(day: str) -> str:
    rows = read_state()
    for row in reversed(rows):
        if row.get("target_date") == day:
            return row.get("alert_hash", "")
    return ""


def write_state(day: str, title: str, severity: str, alert_hash: str) -> None:
    rows = [r for r in read_state() if r.get("target_date") != day]
    rows.append({"target_date": day, "title": title, "severity": severity, "alert_hash": alert_hash})
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=STATE_FIELDS)
        w.writeheader()
        w.writerows(rows)


def stable_hash(day: str, status: str, severity: str, signals: list[str], health: str, live: str) -> str:
    snapshot = {
        "target_date": day,
        "system_status": status,
        "severity": severity,
        "signals": signals,
        "health_components": [line for line in health.splitlines() if line.startswith("- ")],
        "live_rows": [line for line in live.splitlines() if line.startswith("- #") or "live_trigger_counts" in line or "window_counts" in line],
    }
    raw = json.dumps(snapshot, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def build(day: str) -> dict[str, str]:
    folder = ROOT / "today" / day
    health = read(folder / "vsigma_automation_health.md")
    board = read(folder / "vsigma_daily_execution_board.md")
    prelock = read(folder / "vsigma_prelock_live_recheck.md")
    live = read(folder / "vsigma_live_trigger_validator.md")
    memory = read(folder / "vsigma_calibration_memory_ledger.md")

    status = meta(health, "system_status")
    combined = "\n".join([health, board, prelock, live, memory])
    signals = signal_lines(combined)
    required = status == "BROKEN" or bool(signals)
    severity = "BROKEN" if status == "BROKEN" else "ATTENTION" if required else "OK"
    title = f"[vSIGMA ALERT] {day} - {severity}"
    ahash = stable_hash(day, status, severity, signals, health, live)
    prev = previous_hash(day)
    notify = required and (prev != ahash)

    body = [
        f"# vSIGMA Alert - {day}", "",
        f"System status: **{status}**",
        f"Alert required: **{'YES' if required else 'NO'}**",
        f"Notify required: **{'YES' if notify else 'NO'}**",
        f"Alert hash: `{ahash}`",
        "", "## Signals",
    ]
    body += [f"- {line}" for line in signals[:40]] if signals else ["- none"]
    body += [
        "", "## Health Snapshot", "```", health[:6000] if health else "missing health report", "```",
        "", "## Live Trigger Snapshot", "```", live[:4000] if live else "missing live trigger report", "```",
        "", "## Guardrails", "- This issue is an alert only.", "- Manual review is required before any action.",
    ]
    return {"required": str(required).lower(), "notify": str(notify).lower(), "title": title, "body": "\n".join(body) + "\n", "severity": severity, "hash": ahash, "previous_hash": prev}


def run(day: str) -> None:
    day = date.fromisoformat(day).isoformat()
    payload = build(day)
    write_state(day, payload["title"], payload["severity"], payload["hash"])
    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write(base / "vsigma_issue_alert_required.txt", payload["required"] + "\n")
        write(base / "vsigma_issue_alert_notify_required.txt", payload["notify"] + "\n")
        write(base / "vsigma_issue_alert_title.txt", payload["title"] + "\n")
        write(base / "vsigma_issue_alert_hash.txt", payload["hash"] + "\n")
        write(base / "vsigma_issue_alert_body.md", payload["body"])
        write(base / "vsigma_issue_alert_status.md", f"# vSIGMA Issue Alert Status - {day}\n\n- required: {payload['required']}\n- notify_required: {payload['notify']}\n- severity: {payload['severity']}\n- title: {payload['title']}\n- alert_hash: {payload['hash']}\n- previous_hash: {payload['previous_hash'] or 'none'}\n")
    print(f"alert_required={payload['required']}")
    print(f"notify_required={payload['notify']}")
    print(f"title={payload['title']}")
    print(f"alert_hash={payload['hash']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date)


if __name__ == "__main__":
    main()
