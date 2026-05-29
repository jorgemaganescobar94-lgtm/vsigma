from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
PANEL_FIELDS = ["target_date", "generated_at", "card", "status", "detail", "next_action"]


def n(value: object) -> str:
    return "" if value is None else str(value).strip()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return [dict(row) for row in csv.DictReader(file)]


def write_panel_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=PANEL_FIELDS)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in PANEL_FIELDS} for row in rows])


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dated(day: str, name: str) -> Path:
    return PROCESSED / "today" / day / name


def governance(name: str) -> Path:
    return PROCESSED / "governance" / name


def source(day: str, filename: str) -> tuple[list[dict[str, str]], str]:
    today = dated(day, filename)
    rows = read_csv(today)
    if rows:
        return rows, str(today)
    gov = governance(filename)
    return read_csv(gov), str(gov)


def counts(rows: list[dict[str, str]], field: str) -> str:
    counter = Counter(n(row.get(field)) or "UNKNOWN" for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def metric_list(rows: list[dict[str, str]]) -> str:
    metrics: list[str] = []
    for row in rows:
        metric = n(row.get("metric")) or "UNKNOWN"
        if metric not in metrics:
            metrics.append(metric)
    return ",".join(metrics) if metrics else "none"


def ab_status(summary_rows: list[dict[str, str]]) -> tuple[str, str, str]:
    if not summary_rows:
        return "UNAVAILABLE", "No A/B summary rows yet.", "Generate shadow forecast A/B simulator."
    if any(row.get("shadow_verdict") == "SHADOW_WORSE_ON_SAMPLE" for row in summary_rows):
        return "WARN", "At least one shadow rule is worse on available sample.", "Keep shadow only; review before any promotion."
    if any(row.get("shadow_verdict") == "SHADOW_BETTER_ON_SAMPLE" for row in summary_rows):
        return "SHADOW_EDGE", "At least one shadow rule improves sample error.", "Continue shadow; require larger sample before promotion."
    if any(row.get("shadow_verdict") == "WAIT_MORE_DETAIL_SAMPLE" for row in summary_rows):
        return "WAIT_MORE_SAMPLE", "A/B has rows but insufficient detail sample.", "Accumulate more post-match detail rows."
    return "NO_CLEAR_EDGE", "No clear A/B edge yet.", "Continue monitoring only."


def strip_existing(text: str) -> str:
    marker = "\n## Shadow Forecast A/B\n"
    idx = text.find(marker)
    if idx == -1:
        return text.rstrip() + "\n"
    return text[:idx].rstrip() + "\n"


def addendum(summary_rows: list[dict[str, str]], source_path: str) -> tuple[str, str, str, str]:
    status, detail, action = ab_status(summary_rows)
    block = [
        "## Shadow Forecast A/B",
        f"- ab_status: {status}",
        f"- ab_metrics: {metric_list(summary_rows)}",
        f"- ab_verdicts: {counts(summary_rows, 'shadow_verdict')}",
        f"- ab_source: {source_path}",
        "- auto_apply: NO",
        "- production_change: NO",
    ]
    return status, detail, action, "\n".join(block) + "\n"


def update_panel_csv(path: Path, day: str, generated_at: str, status: str, detail: str, action: str, summary_rows: list[dict[str, str]]) -> None:
    rows = [row for row in read_csv(path) if row.get("card") != "SHADOW_AB"]
    rows.append({
        "target_date": day,
        "generated_at": generated_at,
        "card": "SHADOW_AB",
        "status": status,
        "detail": f"metrics={metric_list(summary_rows)}; verdicts={counts(summary_rows, 'shadow_verdict')}; {detail}",
        "next_action": action,
    })
    write_panel_csv(path, rows)


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    generated_at = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    summary_rows, source_path = source(day, "vsigma_shadow_forecast_ab_summary.csv")
    status, detail, action, block = addendum(summary_rows, source_path)
    for base in [PROCESSED / "today" / day, PROCESSED / "governance"]:
        md_path = base / "vsigma_mobile_operator_control_panel.md"
        csv_path = base / "vsigma_mobile_operator_control_panel.csv"
        text = strip_existing(read_text(md_path))
        write_text(md_path, text + "\n" + block)
        update_panel_csv(csv_path, day, generated_at, status, detail, action, summary_rows)
    print("=== VSIGMA MOBILE PANEL SHADOW AB ADDENDUM ===")
    print(f"ab_status={status}")
    print(f"ab_metrics={metric_list(summary_rows)}")
    print(f"ab_verdicts={counts(summary_rows, 'shadow_verdict')}")
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
