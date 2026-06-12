from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

BASE = Path("data/processed")
DEFAULT_OUT_DIR = Path("data/processed/governance")

REQUIRED_COLUMNS = ["date", "home", "away", "market_family", "odds"]

VERDICT_PRIORITY = {
    "EXECUTE_SMALL_STAKE": 100,
    "EXECUTE_SMALL_STAKE_MONITOR": 90,
    "EXECUTABLE_SHADOW": 80,
    "EXECUTION_HOLD_MONITOR": 70,
    "EXECUTION_HOLD_LINEUPS": 65,
    "EXECUTION_HOLD_TACTICAL": 60,
    "EXECUTION_HOLD_PRICE_RECHECK": 55,
    "EXECUTION_HOLD_PORTFOLIO": 50,
    "EXECUTION_HOLD_MANUAL_REVIEW": 45,
    "EXECUTION_HOLD_LOW_AGREEMENT": 40,
    "NO_EXECUTION_PRICE_THIN": 25,
    "NO_EXECUTION_PRICE_FAIL": 20,
    "NO_EXECUTION_NO_PRICE_CHECK": 15,
    "PIPELINE_ERROR": 0,
}


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


def fnum(v: object, default: float = 0.0) -> float:
    try:
        return float(str(v).replace("%", "").strip())
    except Exception:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_one(path: Path) -> dict[str, str]:
    rows = read_rows(path)
    return rows[0] if rows else {}


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def yn(value: object, default: str = "PENDING") -> str:
    text = str(value or "").strip()
    return text if text else default


def optional_float_arg(cmd: list[str], flag: str, value: object) -> None:
    text = str(value or "").strip()
    if text:
        cmd.extend([flag, text])


def load_pipeline_result(processed_dir: Path, row: dict[str, str]) -> dict[str, str]:
    day = row.get("date", "")
    home = row.get("home", "")
    away = row.get("away", "")
    market = row.get("market_family", "")
    slug = clean(f"{home}_vs_{away}")
    safe_market = clean(market)
    path = processed_dir / "today" / day / f"vsigma_full_shadow_pipeline_{slug}_{safe_market}.csv"
    return read_one(path)


def run_full_pipeline(input_row: dict[str, str], processed_dir: Path, skip_confirmation: bool) -> tuple[dict[str, str], str, str]:
    day = input_row.get("date", "").strip()
    home = input_row.get("home", "").strip()
    away = input_row.get("away", "").strip()
    market = input_row.get("market_family", "").strip()
    odds = input_row.get("odds", "").strip()

    cmd = [
        sys.executable,
        "scripts/run_vsigma_full_shadow_pipeline.py",
        "--date", day,
        "--home", home,
        "--away", away,
        "--market-family", market,
        "--odds", odds,
        "--processed-dir", str(processed_dir),
        "--lineups-confirmed", yn(input_row.get("lineups_confirmed")),
        "--tactical-confirmed", yn(input_row.get("tactical_confirmed")),
        "--price-live", yn(input_row.get("price_live")),
        "--portfolio-ok", yn(input_row.get("portfolio_ok")),
        "--monitor-confirmed", yn(input_row.get("monitor_confirmed")),
        "--stake-cap-pct-bankroll", str(input_row.get("stake_cap_pct_bankroll") or "0.25"),
        "--notes", str(input_row.get("notes") or ""),
    ]

    optional_float_arg(cmd, "--market-under25-prob", input_row.get("market_under25_prob"))
    optional_float_arg(cmd, "--market-over25-prob", input_row.get("market_over25_prob"))
    optional_float_arg(cmd, "--min-edge", input_row.get("min_edge"))
    optional_float_arg(cmd, "--min-ev", input_row.get("min_ev"))

    if skip_confirmation:
        cmd.append("--skip-confirmation")

    proc = subprocess.run(cmd, text=True, capture_output=True)
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        return {}, stdout, stderr or f"returncode={proc.returncode}"
    return load_pipeline_result(processed_dir, input_row), stdout, stderr


def normalize_result(input_row: dict[str, str], pipeline_row: dict[str, str], index: int, stdout: str, stderr: str) -> dict[str, object]:
    if not pipeline_row:
        verdict = "PIPELINE_ERROR"
        return {
            "rank": "",
            "input_index": index,
            "date": input_row.get("date", ""),
            "fixture": clean(f"{input_row.get('home', '')}_vs_{input_row.get('away', '')}").replace("_", " "),
            "home": input_row.get("home", ""),
            "away": input_row.get("away", ""),
            "market_family": input_row.get("market_family", ""),
            "odds": input_row.get("odds", ""),
            "pipeline_final_verdict": verdict,
            "selected_market": "",
            "selected_odds": "",
            "selected_expected_roi": "",
            "selected_edge_prob": "",
            "monitor_required": "",
            "price_label": "",
            "builder_permission": "",
            "veto_flags": "",
            "stake_cap_pct_bankroll": input_row.get("stake_cap_pct_bankroll", ""),
            "priority_score": VERDICT_PRIORITY[verdict],
            "error": stderr,
            "stdout_tail": stdout[-600:],
            "auto_bet": "NO",
            "production_change": "NO",
        }

    verdict = pipeline_row.get("pipeline_final_verdict", "MISSING")
    priority = VERDICT_PRIORITY.get(verdict, 10)
    return {
        "rank": "",
        "input_index": index,
        "date": input_row.get("date", ""),
        "fixture": pipeline_row.get("fixture", ""),
        "home": input_row.get("home", ""),
        "away": input_row.get("away", ""),
        "market_family": input_row.get("market_family", ""),
        "odds": input_row.get("odds", ""),
        "pipeline_final_verdict": verdict,
        "selected_market": pipeline_row.get("selected_market", ""),
        "selected_odds": pipeline_row.get("selected_odds", ""),
        "selected_expected_roi": pipeline_row.get("selected_expected_roi", ""),
        "selected_edge_prob": pipeline_row.get("selected_edge_prob", ""),
        "monitor_required": pipeline_row.get("monitor_required", ""),
        "price_label": pipeline_row.get("price_label", ""),
        "builder_permission": pipeline_row.get("builder_permission", ""),
        "veto_flags": pipeline_row.get("veto_flags", ""),
        "stake_cap_pct_bankroll": pipeline_row.get("stake_cap_pct_bankroll", input_row.get("stake_cap_pct_bankroll", "")),
        "priority_score": priority,
        "error": stderr,
        "stdout_tail": stdout[-600:],
        "report_hint": f"data/processed/today/{input_row.get('date','')}/vsigma_full_shadow_pipeline_{clean(f'{input_row.get('home','')}_vs_{input_row.get('away','')}')}_{clean(input_row.get('market_family',''))}.md",
        "auto_bet": "NO",
        "production_change": "NO",
    }


def sort_results(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    def key(row: dict[str, object]):
        return (
            fnum(row.get("priority_score")),
            fnum(row.get("selected_expected_roi")),
            fnum(row.get("selected_edge_prob")),
            0.0 if str(row.get("monitor_required")) == "YES" else 1.0,
        )
    out = sorted(rows, key=key, reverse=True)
    for i, row in enumerate(out, start=1):
        row["rank"] = i
    return out


def section(title: str, rows: list[dict[str, object]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not rows:
        lines.append("- None")
        lines.append("")
        return lines
    for row in rows:
        lines.append(
            f"{row.get('rank')}. {row.get('fixture')} — {row.get('selected_market') or row.get('market_family')} "
            f"@{row.get('selected_odds') or row.get('odds')} — {row.get('pipeline_final_verdict')} — "
            f"EV {row.get('selected_expected_roi')} — edge {row.get('selected_edge_prob')} — monitor {row.get('monitor_required')}"
        )
    lines.append("")
    return lines


def md(batch_name: str, rows: list[dict[str, object]]) -> str:
    executable = [r for r in rows if str(r.get("pipeline_final_verdict")).startswith("EXECUTE_SMALL_STAKE")]
    holds = [r for r in rows if str(r.get("pipeline_final_verdict")).startswith("EXECUTION_HOLD")]
    no_exec = [r for r in rows if str(r.get("pipeline_final_verdict")).startswith("NO_EXECUTION")]
    errors = [r for r in rows if str(r.get("pipeline_final_verdict")) == "PIPELINE_ERROR"]

    lines = [
        f"# vSIGMA Batch Shadow Pipeline — {batch_name}",
        "",
        f"- candidates: {len(rows)}",
        f"- executable: {len(executable)}",
        f"- holds: {len(holds)}",
        f"- no_execution: {len(no_exec)}",
        f"- errors: {len(errors)}",
        "- auto_bet: NO",
        "- production_change: NO",
        "",
    ]
    lines += section("TOP EXECUTABLES", executable)
    lines += section("HOLDS", holds)
    lines += section("NO EXECUTION", no_exec)
    lines += section("ERRORS", errors)
    lines += [
        "## Hard rules",
        "",
        "- This batch runner never sends or places bets.",
        "- EXECUTE_SMALL_STAKE means only that the local checks passed; execution remains manual.",
        "- Rank is operational, not a guarantee of outcome.",
        "",
    ]
    return "\n".join(lines)


def validate_input(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise RuntimeError("Input CSV has no rows")
    missing = [c for c in REQUIRED_COLUMNS if c not in rows[0]]
    if missing:
        raise RuntimeError(f"Input CSV missing required columns: {missing}")


def run(args: argparse.Namespace) -> None:
    input_csv = Path(args.input_csv)
    processed_dir = Path(args.processed_dir)
    out_dir = Path(args.out_dir)
    batch_name = args.batch_name or clean(input_csv.stem)

    rows = read_rows(input_csv)
    validate_input(rows)

    results: list[dict[str, object]] = []
    for idx, row in enumerate(rows, start=1):
        fixture = f"{row.get('home')} vs {row.get('away')}"
        market = row.get("market_family", "")
        print(f"\n### [{idx}/{len(rows)}] {fixture} — {market} @{row.get('odds')}")
        pipeline_row, stdout, stderr = run_full_pipeline(row, processed_dir, args.skip_confirmation)
        result = normalize_result(row, pipeline_row, idx, stdout, stderr)
        results.append(result)
        print(f"=> {result.get('pipeline_final_verdict')} EV={result.get('selected_expected_roi')} edge={result.get('selected_edge_prob')}")
        if stderr:
            print(f"stderr: {stderr[-300:]}")

    ranked = sort_results(results)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"vsigma_batch_shadow_pipeline_{batch_name}.csv"
    out_md = out_dir / f"vsigma_batch_shadow_pipeline_{batch_name}.md"
    write_csv(out_csv, ranked)
    out_md.write_text(md(batch_name, ranked), encoding="utf-8")

    print("\n=== vSIGMA BATCH SHADOW PIPELINE ===")
    print(f"BATCH: {batch_name}")
    print(f"CANDIDATES: {len(ranked)}")
    print(f"CSV: {out_csv}")
    print(f"MD: {out_md}")
    print("AUTO_BET: NO")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--batch-name", default="")
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--skip-confirmation", action="store_true")
    run(parser.parse_args())
