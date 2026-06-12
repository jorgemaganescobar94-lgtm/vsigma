from __future__ import annotations

import argparse
import csv
import re
import unicodedata
from pathlib import Path

BASE = Path("data/processed")


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


def write_csv(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(row.keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def verdict(governance: dict[str, str], price_rows: list[dict[str, str]]) -> dict[str, object]:
    builder_permission = str(governance.get("builder_permission", ""))
    monitor_required = str(governance.get("monitor_required", "NO"))
    veto_flags = str(governance.get("veto_flags", ""))

    if not price_rows:
        return {
            "final_execution_verdict": "NO_EXECUTION_NO_PRICE_CHECK",
            "selected_market": "",
            "selected_odds": "",
            "selected_expected_roi": "",
            "selected_edge_prob": "",
            "final_note": "No price survival file exists. Cannot execute.",
        }

    ok_rows = [r for r in price_rows if str(r.get("price_label")) == "PRICE_OK"]
    thin_rows = [r for r in price_rows if str(r.get("price_label")) == "PRICE_THIN"]

    if not ok_rows:
        if thin_rows:
            return {
                "final_execution_verdict": "NO_EXECUTION_PRICE_THIN",
                "selected_market": thin_rows[0].get("normalized_market", ""),
                "selected_odds": thin_rows[0].get("offered_odds", ""),
                "selected_expected_roi": thin_rows[0].get("expected_roi", ""),
                "selected_edge_prob": thin_rows[0].get("edge_prob", ""),
                "final_note": "Price is positive but too thin for execution.",
            }
        return {
            "final_execution_verdict": "NO_EXECUTION_PRICE_FAIL",
            "selected_market": price_rows[0].get("normalized_market", ""),
            "selected_odds": price_rows[0].get("offered_odds", ""),
            "selected_expected_roi": price_rows[0].get("expected_roi", ""),
            "selected_edge_prob": price_rows[0].get("edge_prob", ""),
            "final_note": "No checked market survives price.",
        }

    ok_rows.sort(key=lambda r: fnum(r.get("expected_roi")), reverse=True)
    best = ok_rows[0]

    if "LOW_AGREEMENT" in veto_flags:
        final = "EXECUTION_HOLD_LOW_AGREEMENT"
        note = "Price survives, but agreement layer demands manual review."
    elif monitor_required == "YES" or "MONITOR_REQUIRED" in veto_flags:
        final = "EXECUTION_HOLD_MONITOR"
        note = "Price survives, but monitor-required gate is active. Needs extra tactical/lineup confirmation."
    elif builder_permission in {"", "NO"}:
        final = "EXECUTION_HOLD_CONTEXT_WEAK"
        note = "Price survives, but governance did not grant builder permission."
    else:
        final = "EXECUTABLE_SHADOW"
        note = "Price and governance survive. Still no auto-bet: final tactical/lineup/portfolio confirmation required."

    return {
        "final_execution_verdict": final,
        "selected_market": best.get("normalized_market", ""),
        "selected_odds": best.get("offered_odds", ""),
        "selected_expected_roi": best.get("expected_roi", ""),
        "selected_edge_prob": best.get("edge_prob", ""),
        "final_note": note,
    }


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA Final Execution Lock - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- final_execution_verdict: {row.get('final_execution_verdict')}",
        f"- selected_market: {row.get('selected_market')}",
        f"- selected_odds: {row.get('selected_odds')}",
        f"- selected_expected_roi: {row.get('selected_expected_roi')}",
        f"- selected_edge_prob: {row.get('selected_edge_prob')}",
        "",
        "## Governance context",
        f"- market_governance_label: {row.get('market_governance_label')}",
        f"- builder_permission: {row.get('builder_permission')}",
        f"- monitor_required: {row.get('monitor_required')}",
        f"- veto_flags: {row.get('veto_flags')}",
        "",
        "## Final note",
        f"- {row.get('final_note')}",
        "",
        "## Hard rules",
        "- auto_bet: NO",
        "- production_change: NO",
        "- EXECUTABLE_SHADOW is not automatic execution.",
        "- Final human/tactical/lineup/portfolio confirmation is still required.",
    ]) + "\n"


def run(day: str, home: str, away: str, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    today = base / "today" / day

    governance = read_one(today / f"vsigma_market_governance_summary_{slug}.csv")
    price_rows = []
    for path in today.glob(f"vsigma_price_survival_{slug}_*.csv"):
        price_rows.extend(read_rows(path))

    decision = verdict(governance, price_rows)

    row = {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "home_team": home,
        "away_team": away,
        "market_governance_label": governance.get("market_governance_label", "MISSING"),
        "builder_permission": governance.get("builder_permission", ""),
        "monitor_required": governance.get("monitor_required", "NO"),
        "veto_flags": governance.get("veto_flags", ""),
        "price_checks_found": len(price_rows),
        "auto_bet": "NO",
        "production_change": "NO",
        **decision,
    }

    for folder in [today, base / "governance"]:
        write_csv(folder / f"vsigma_final_execution_lock_{slug}.csv", row)
        (folder / f"vsigma_final_execution_lock_{slug}.md").write_text(md(row), encoding="utf-8")

    print(f"Final execution lock: {row['final_execution_verdict']} market={row['selected_market']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    args = parser.parse_args()

    run(args.date, args.home, args.away, args.processed_dir)
