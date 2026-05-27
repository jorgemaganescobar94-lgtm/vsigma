from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path("data/processed")


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
        "BROKEN",
        "READY_LOW_STAKE_REVIEW",
        "LIVE_ONLY_WAIT_TRIGGER",
        "LIVE_TRIGGER_CONFIRMED",
        "LIVE_TRIGGER_REJECTED",
        "TOO_LATE",
        "MATCH_FINISHED",
        "PATCH_CANDIDATE_REVIEW",
        "API_CREDENTIALS_MISSING",
        "REFRESH_SKIPPED_NO_API_CREDENTIALS",
    ]
    return [line.strip() for line in text.splitlines() if any(k in line for k in keys)]


def build(day: str, tz: str) -> dict[str, str]:
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

    body = [
        f"# vSIGMA Alert - {day}",
        "",
        f"Generated: {datetime.now(ZoneInfo(tz)).isoformat(timespec='seconds')}",
        f"System status: **{status}**",
        f"Alert required: **{'YES' if required else 'NO'}**",
        "",
        "## Signals",
    ]

    if signals:
        body.extend(f"- {line}" for line in signals[:40])
    else:
        body.append("- none")

    body.extend([
        "",
        "## Health Snapshot",
        "```",
        health[:6000] if health else "missing health report",
        "```",
        "",
        "## Live Trigger Snapshot",
        "```",
        live[:4000] if live else "missing live trigger report",
        "```",
        "",
        "## Guardrails",
        "- This issue is an alert only.",
        "- Manual review is required before any action.",
    ])

    return {
        "required": str(required).lower(),
        "title": title,
        "body": "\n".join(body) + "\n",
        "severity": severity,
    }


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    payload = build(day, tz)

    for base in [ROOT / "today" / day, ROOT / "governance"]:
        write(base / "vsigma_issue_alert_required.txt", payload["required"] + "\n")
        write(base / "vsigma_issue_alert_title.txt", payload["title"] + "\n")
        write(base / "vsigma_issue_alert_body.md", payload["body"])
        write(
            base / "vsigma_issue_alert_status.md",
            f"# vSIGMA Issue Alert Status - {day}\n\n"
            f"- required: {payload['required']}\n"
            f"- severity: {payload['severity']}\n"
            f"- title: {payload['title']}\n",
        )

    print(f"alert_required={payload['required']}")
    print(f"title={payload['title']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
