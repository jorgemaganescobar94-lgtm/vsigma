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


def model_probability_for_market(
    market_family: str,
    forecast: dict[str, str],
    u35_gate: dict[str, str],
    tt_rows: list[dict[str, str]],
) -> tuple[float, str, str]:
    market = market_family.upper().strip()

    if market in {"HOME", "1", "HOME_WIN"}:
        return fnum(forecast.get("home_prob") or forecast.get("raw_home_prob")), "forecast_1x2", "HOME"

    if market in {"DRAW", "X"}:
        return fnum(forecast.get("draw_prob") or forecast.get("raw_draw_prob")), "forecast_1x2", "DRAW"

    if market in {"AWAY", "2", "AWAY_WIN"}:
        return fnum(forecast.get("away_prob") or forecast.get("raw_away_prob")), "forecast_1x2", "AWAY"

    if market in {"UNDER35", "UNDER_3_5", "U35", "UNDER 3.5"}:
        return fnum(u35_gate.get("model_under35_prob")), "u35_gate", "UNDER_3_5"

    for row in tt_rows:
        if str(row.get("market_family", "")).upper() == market:
            return fnum(row.get("model_prob")), "team_total_gate", str(row.get("market_family"))

    return 0.0, "missing", market


def price_label(model_prob: float, odds: float, min_edge: float, min_ev: float) -> dict[str, object]:
    if model_prob <= 0 or odds <= 1.0:
        return {
            "price_label": "PRICE_INPUT_INVALID_OR_MODEL_MISSING",
            "implied_prob": "",
            "fair_odds": "",
            "edge_prob": "",
            "expected_roi": "",
            "price_ok": "NO",
        }

    implied = 1.0 / odds
    fair = 1.0 / model_prob
    edge = model_prob - implied
    ev = model_prob * odds - 1.0

    if edge >= min_edge and ev >= min_ev:
        label = "PRICE_OK"
        ok = "YES"
    elif edge >= 0 and ev >= 0:
        label = "PRICE_THIN"
        ok = "NO_THIN"
    else:
        label = "PRICE_FAIL"
        ok = "NO"

    return {
        "price_label": label,
        "implied_prob": round(implied, 5),
        "fair_odds": round(fair, 3),
        "edge_prob": round(edge, 5),
        "expected_roi": round(ev, 5),
        "price_ok": ok,
    }


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA Price Survival Check - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- market_family: {row.get('market_family')}",
        f"- normalized_market: {row.get('normalized_market')}",
        f"- probability_source: {row.get('probability_source')}",
        f"- model_prob: {row.get('model_prob')}",
        f"- offered_odds: {row.get('offered_odds')}",
        f"- implied_prob: {row.get('implied_prob')}",
        f"- fair_odds: {row.get('fair_odds')}",
        f"- edge_prob: {row.get('edge_prob')}",
        f"- expected_roi: {row.get('expected_roi')}",
        f"- price_label: {row.get('price_label')}",
        f"- execution_permission: {row.get('execution_permission')}",
        "",
        "## Gate context",
        f"- market_governance_label: {row.get('market_governance_label')}",
        f"- builder_permission: {row.get('builder_permission')}",
        f"- monitor_required: {row.get('monitor_required')}",
        f"- veto_flags: {row.get('veto_flags')}",
        "",
        "## Governance",
        "- auto_bet: NO",
        "- production_change: NO",
        "- PRICE_OK only means the price survives this mathematical check; tactical, lineup and portfolio checks still decide execution.",
    ]) + "\n"


def run(day: str, home: str, away: str, market_family: str, odds: float, base: Path, min_edge: float, min_ev: float) -> None:
    slug = clean(f"{home}_vs_{away}")
    today = base / "today" / day

    forecast = read_one(today / f"vsigma_adhoc_match_stat_forecast_{slug}.csv")
    u35_gate = read_one(today / f"vsigma_under35_shadow_gate_{slug}.csv")
    tt_rows = read_rows(today / f"vsigma_team_total_gate_{slug}.csv")
    governance = read_one(today / f"vsigma_market_governance_summary_{slug}.csv")

    if not forecast:
        raise RuntimeError(f"Missing forecast file for {slug} on {day}")

    model_prob, source, normalized = model_probability_for_market(market_family, forecast, u35_gate, tt_rows)
    price = price_label(model_prob, odds, min_edge, min_ev)

    veto_flags = str(governance.get("veto_flags", ""))
    builder_permission = str(governance.get("builder_permission", ""))
    monitor_required = str(governance.get("monitor_required", "NO"))
    market_governance_label = str(governance.get("market_governance_label", "MISSING"))
    price_ok = str(price.get("price_ok", "NO"))

    if price_ok == "YES" and builder_permission not in {"", "NO"}:
        if monitor_required == "YES":
            execution_permission = "PRICE_OK_WITH_MONITOR_GOVERNANCE_REVIEW_REQUIRED"
        else:
            execution_permission = "PRICE_OK_GOVERNANCE_REVIEW_REQUIRED"
    elif price_ok == "YES":
        execution_permission = "PRICE_OK_BUT_GATE_CONTEXT_WEAK_OR_MISSING"
    elif price_ok == "NO_THIN":
        execution_permission = "NO_EXECUTION_PRICE_THIN"
    else:
        execution_permission = "NO_EXECUTION_PRICE_FAIL"

    row = {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "home_team": forecast.get("home_team", home),
        "away_team": forecast.get("away_team", away),
        "market_family": market_family,
        "normalized_market": normalized,
        "probability_source": source,
        "model_prob": round(model_prob, 5) if model_prob else "",
        "offered_odds": odds,
        "min_edge": min_edge,
        "min_expected_roi": min_ev,
        **price,
        "market_governance_label": market_governance_label,
        "builder_permission": builder_permission,
        "monitor_required": monitor_required,
        "veto_flags": veto_flags,
        "execution_permission": execution_permission,
        "auto_bet": "NO",
        "production_change": "NO",
    }

    safe_market = clean(market_family)
    for folder in [today, base / "governance"]:
        write_csv(folder / f"vsigma_price_survival_{slug}_{safe_market}.csv", row)
        (folder / f"vsigma_price_survival_{slug}_{safe_market}.md").write_text(md(row), encoding="utf-8")

    print(f"Price survival built: {market_family} {row['price_label']} exec={execution_permission}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--market-family", required=True)
    parser.add_argument("--odds", type=float, required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    parser.add_argument("--min-edge", type=float, default=0.025)
    parser.add_argument("--min-ev", type=float, default=0.03)
    args = parser.parse_args()

    run(
        args.date,
        args.home,
        args.away,
        args.market_family,
        args.odds,
        args.processed_dir,
        args.min_edge,
        args.min_ev,
    )
