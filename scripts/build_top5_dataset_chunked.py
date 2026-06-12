from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

DEFAULT_LEAGUE_SEASONS = [
    "39:2025", "39:2024", "39:2023",
    "140:2025", "140:2024", "140:2023",
    "135:2025", "135:2024", "135:2023",
    "78:2025", "78:2024", "78:2023",
    "61:2025", "61:2024", "61:2023",
]


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({key for row in rows for key in row.keys()})
    core = ["fixture_id", "fixture_date", "league_id", "season", "home_team", "away_team", "target_home_goals", "target_away_goals", "target_result_class"]
    fields = core + [f for f in fields if f not in core]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def merge_chunks(chunk_dir: Path, out_path: Path) -> int:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(chunk_dir.glob("*.csv")):
        if path.name.endswith("_summary.csv"):
            continue
        for row in read_rows(path):
            fid = str(row.get("fixture_id", ""))
            key = fid or f"{row.get('league_id')}|{row.get('season')}|{row.get('home_team')}|{row.get('away_team')}|{row.get('fixture_date')}"
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
    rows.sort(key=lambda r: str(r.get("fixture_date", "")))
    write_rows(out_path, rows)
    return len(rows)


def run_chunk(league_season: str, chunk_dir: Path, window: int, sleep: float, include_odds: bool, max_fixtures_per_chunk: int, force: bool) -> bool:
    safe_name = league_season.replace(":", "_")
    out = chunk_dir / f"vsigma_historical_{safe_name}.csv"
    if out.exists() and not force:
        print(f"SKIP existing chunk {league_season}: {out}")
        return True
    cmd = [
        sys.executable,
        "scripts/build_vsigma_historical_dataset.py",
        "--league-season", league_season,
        "--out", str(out),
        "--window", str(window),
        "--sleep", str(sleep),
    ]
    if include_odds:
        cmd.append("--include-odds")
    if max_fixtures_per_chunk > 0:
        cmd.extend(["--max-fixtures", str(max_fixtures_per_chunk)])
    print("RUN", " ".join(cmd))
    completed = subprocess.run(cmd, text=True)
    if completed.returncode != 0:
        print(f"STOP chunk failed for {league_season}. Keep completed chunks and rerun later.")
        return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--league-season", action="append", default=[])
    parser.add_argument("--chunk-dir", type=Path, default=Path("data/modeling/chunks/top5_current"))
    parser.add_argument("--out", type=Path, default=Path("data/modeling/vsigma_historical_dataset_top5_current.csv"))
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--sleep", type=float, default=0.8)
    parser.add_argument("--include-odds", action="store_true", help="Use only if API actually returns historical odds. Otherwise it wastes quota.")
    parser.add_argument("--max-fixtures-per-chunk", type=int, default=0)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    league_seasons = args.league_season or DEFAULT_LEAGUE_SEASONS
    args.chunk_dir.mkdir(parents=True, exist_ok=True)
    for item in league_seasons:
        ok = run_chunk(item, args.chunk_dir, args.window, args.sleep, args.include_odds, args.max_fixtures_per_chunk, args.force)
        rows = merge_chunks(args.chunk_dir, args.out)
        print(f"MERGED rows={rows} out={args.out}")
        if not ok:
            raise SystemExit(1)
    rows = merge_chunks(args.chunk_dir, args.out)
    print(f"DONE top5 chunks merged rows={rows} out={args.out}")


if __name__ == "__main__":
    main()
