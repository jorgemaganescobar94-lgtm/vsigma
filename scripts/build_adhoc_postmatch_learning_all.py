from __future__ import annotations

import argparse
import csv
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from build_adhoc_postmatch_learning_ledger import run as run_single

BASE = Path("data/processed")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def discover_forecasts(day: str, base: Path) -> list[tuple[str, str, str]]:
    folder = base / "today" / day
    matches: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    if not folder.exists():
        return matches
    for path in sorted(folder.glob("vsigma_adhoc_match_stat_forecast_*.csv")):
        if path.name.endswith("_summary.csv"):
            continue
        rows = read_csv(path)
        if not rows:
            continue
        row = rows[0]
        home = (row.get("home_team") or "").strip()
        away = (row.get("away_team") or "").strip()
        fixture_id = (row.get("fixture_id") or "").strip()
        key = fixture_id or f"{home}|{away}"
        if not home or not away or key in seen:
            continue
        seen.add(key)
        matches.append((home, away, fixture_id))
    return matches


def run(day: str, tz: str, base: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    now = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    matches = discover_forecasts(day, base)
    summary_rows: list[dict[str, str]] = []
    for home, away, fixture_id in matches:
        try:
            run_single(day, home, away, tz, base)
            status = "OK"
            error = ""
        except Exception as exc:  # keep batch alive; one fixture must not kill the whole ledger
            status = "ERROR"
            error = str(exc)[:500]
        summary_rows.append({
            "target_date": day,
            "generated_at": now,
            "home_team": home,
            "away_team": away,
            "fixture_id": fixture_id,
            "postmatch_status": status,
            "error": error,
            "auto_apply": "NO",
            "production_change": "NO",
        })
    fields = ["target_date","generated_at","home_team","away_team","fixture_id","postmatch_status","error","auto_apply","production_change"]
    for folder in [base / "today" / day, base / "governance"]:
        folder.mkdir(parents=True, exist_ok=True)
        out = folder / f"vsigma_adhoc_postmatch_learning_all_{day}.csv"
        with out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(summary_rows)
        md = folder / f"vsigma_adhoc_postmatch_learning_all_{day}.md"
        lines = [f"# vSIGMA Ad Hoc Post-Match Learning All - {day}", "", f"- generated_at: {now}", f"- forecasts_found: {len(matches)}", f"- ledgers_attempted: {len(summary_rows)}", "- auto_apply: NO", "- production_change: NO", "", "## Fixtures"]
        if not summary_rows:
            lines.append("- none. No ad hoc forecast files found for this date.")
        for row in summary_rows:
            label = f"{row['home_team']} vs {row['away_team']}"
            if row["postmatch_status"] == "OK":
                lines.append(f"- {label}: OK")
            else:
                lines.append(f"- {label}: ERROR | {row['error']}")
        md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Ad hoc postmatch learning all built forecasts_found={len(matches)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)
