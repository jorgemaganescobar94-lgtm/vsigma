from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

BASE = Path("data/processed")


def clean(v: object) -> str:
    t = unicodedata.normalize("NFKD", str(v or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")


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


def run_step(label: str, args: list[str]) -> None:
    print(f"\n==> {label}")
    print(" ".join(args))
    subprocess.run(args, check=True)


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA Full Shadow Pipeline - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- pipeline_final_verdict: {row.get('pipeline_final_verdict')}",
        f"- selected_market: {row.get('selected_market')}",
        f"- selected_odds: {row.get('selected_odds')}",
        f"- selected_expected_roi: {row.get('selected_expected_roi')}",
        f"- selected_edge_prob: {row.get('selected_edge_prob')}",
        f"- stake_cap_pct_bankroll: {row.get('stake_cap_pct_bankroll')}",
        "",
        "## Inputs",
        f"- requested_market_family: {row.get('requested_market_family')}",
        f"- requested_odds: {row.get('requested_odds')}",
        f"- lineups_confirmed: {row.get('lineups_confirmed')}",
        f"- tactical_confirmed: {row.get('tactical_confirmed')}",
        f"- price_live: {row.get('price_live')}",
        f"- portfolio_ok: {row.get('portfolio_ok')}",
        f"- monitor_confirmed: {row.get('monitor_confirmed')}",
        "",
        "## Layer results",
        f"- u35_gate_label: {row.get('u35_gate_label')}",
        f"- u35_market_action_hint: {row.get('u35_market_action_hint')}",
        f"- team_total_strong_markets: {row.get('team_total_strong_markets')}",
        f"- market_governance_label: {row.get('market_governance_label')}",
        f"- builder_permission: {row.get('builder_permission')}",
        f"- monitor_required: {row.get('monitor_required')}",
        f"- veto_flags: {row.get('veto_flags')}",
        f"- price_label: {row.get('price_label')}",
        f"- final_execution_verdict: {row.get('final_execution_verdict')}",
        f"- confirmation_verdict: {row.get('confirmation_verdict')}",
        "",
        "## Notes",
        f"- final_lock_note: {row.get('final_lock_note')}",
        f"- confirmation_note: {row.get('confirmation_note')}",
        f"- user_notes: {row.get('user_notes')}",
        "",
        "## Hard rules",
        "- auto_bet: NO",
        "- production_change: NO",
        "- This pipeline never sends or places bets.",
        "- Any executable verdict still means small-stake/manual execution only.",
    ]) + "\n"


def build_pipeline_row(
    day: str,
    home: str,
    away: str,
    market_family: str,
    odds: float,
    processed_dir: Path,
    skip_confirmation: bool,
    stake_cap_pct_bankroll: float,
    user_notes: str,
) -> dict[str, object]:
    slug = clean(f"{home}_vs_{away}")
    safe_market = clean(market_family)
    today = processed_dir / "today" / day

    u35_gate = read_one(today / f"vsigma_under35_shadow_gate_{slug}.csv")
    u35_action = read_one(today / f"vsigma_u35_market_action_hint_{slug}.csv")
    tt_gate_rows = read_rows(today / f"vsigma_team_total_gate_{slug}.csv")
    governance = read_one(today / f"vsigma_market_governance_summary_{slug}.csv")
    price = read_one(today / f"vsigma_price_survival_{slug}_{safe_market}.csv")
    final_lock = read_one(today / f"vsigma_final_execution_lock_{slug}.csv")
    confirmation = {} if skip_confirmation else read_one(today / f"vsigma_execution_confirmation_check_{slug}.csv")

    team_total_strong = ";".join([
        f"{r.get('market_family')}:{r.get('team_total_gate_label')}@{r.get('model_prob')}"
        for r in tt_gate_rows
        if str(r.get("team_total_gate_label")) == "TEAM_TOTAL_STRONG"
    ])

    if confirmation:
        pipeline_final = confirmation.get("confirmation_verdict", "MISSING_CONFIRMATION_VERDICT")
        selected_market = confirmation.get("selected_market", "")
        selected_odds = confirmation.get("selected_odds", "")
        selected_roi = confirmation.get("selected_expected_roi", "")
        selected_edge = confirmation.get("selected_edge_prob", "")
        confirmation_note = confirmation.get("confirmation_note", "")
    else:
        pipeline_final = final_lock.get("final_execution_verdict", "MISSING_FINAL_LOCK")
        selected_market = final_lock.get("selected_market", "")
        selected_odds = final_lock.get("selected_odds", "")
        selected_roi = final_lock.get("selected_expected_roi", "")
        selected_edge = final_lock.get("selected_edge_prob", "")
        confirmation_note = "SKIPPED" if skip_confirmation else "MISSING"

    return {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "home_team": home,
        "away_team": away,
        "requested_market_family": market_family,
        "requested_odds": odds,
        "pipeline_final_verdict": pipeline_final,
        "selected_market": selected_market,
        "selected_odds": selected_odds,
        "selected_expected_roi": selected_roi,
        "selected_edge_prob": selected_edge,
        "stake_cap_pct_bankroll": stake_cap_pct_bankroll,
        "lineups_confirmed": confirmation.get("lineups_confirmed", "SKIPPED" if skip_confirmation else ""),
        "tactical_confirmed": confirmation.get("tactical_confirmed", "SKIPPED" if skip_confirmation else ""),
        "price_live": confirmation.get("price_live", "SKIPPED" if skip_confirmation else ""),
        "portfolio_ok": confirmation.get("portfolio_ok", "SKIPPED" if skip_confirmation else ""),
        "monitor_confirmed": confirmation.get("monitor_confirmed", "SKIPPED" if skip_confirmation else ""),
        "u35_gate_label": u35_gate.get("u35_gate_label", "MISSING"),
        "u35_market_action_hint": u35_action.get("u35_market_action_hint", "MISSING"),
        "team_total_strong_markets": team_total_strong,
        "market_governance_label": governance.get("market_governance_label", "MISSING"),
        "builder_permission": governance.get("builder_permission", ""),
        "monitor_required": governance.get("monitor_required", "NO"),
        "veto_flags": governance.get("veto_flags", ""),
        "price_label": price.get("price_label", "MISSING"),
        "price_execution_permission": price.get("execution_permission", ""),
        "final_execution_verdict": final_lock.get("final_execution_verdict", "MISSING"),
        "final_lock_note": final_lock.get("final_note", ""),
        "confirmation_verdict": confirmation.get("confirmation_verdict", "SKIPPED" if skip_confirmation else "MISSING"),
        "confirmation_note": confirmation_note,
        "user_notes": user_notes,
        "auto_bet": "NO",
        "production_change": "NO",
    }


def run_pipeline(args: argparse.Namespace) -> None:
    slug = clean(f"{args.home}_vs_{args.away}")
    safe_market = clean(args.market_family)
    processed_dir = Path(args.processed_dir)
    today = processed_dir / "today" / args.date
    if not (today / f"vsigma_adhoc_match_stat_forecast_{slug}.csv").exists():
        raise RuntimeError(f"Missing forecast file: {today / f'vsigma_adhoc_match_stat_forecast_{slug}.csv'}")

    py = sys.executable
    common = ["--date", args.date, "--home", args.home, "--away", args.away, "--processed-dir", str(processed_dir)]

    u35_cmd = [py, "scripts/apply_under35_shadow_gate.py", *common]
    if args.market_under25_prob is not None:
        u35_cmd += ["--market-under25-prob", str(args.market_under25_prob)]
    if args.market_over25_prob is not None:
        u35_cmd += ["--market-over25-prob", str(args.market_over25_prob)]

    steps = [
        ("U35 shadow gate", u35_cmd),
        ("U35 market action hint", [py, "scripts/build_u35_market_action_hint.py", *common]),
        ("Team total gate", [py, "scripts/apply_team_total_gate.py", *common]),
        ("Market governance summary", [py, "scripts/build_market_governance_summary.py", *common]),
        ("Price survival", [
            py,
            "scripts/build_price_survival_check.py",
            *common,
            "--market-family",
            args.market_family,
            "--odds",
            str(args.odds),
            "--min-edge",
            str(args.min_edge),
            "--min-ev",
            str(args.min_ev),
        ]),
        ("Final execution lock", [py, "scripts/build_final_execution_lock.py", *common]),
    ]

    if not args.skip_confirmation:
        steps.append(("Execution confirmation", [
            py,
            "scripts/build_execution_confirmation_check.py",
            *common,
            "--lineups-confirmed",
            args.lineups_confirmed,
            "--tactical-confirmed",
            args.tactical_confirmed,
            "--price-live",
            args.price_live,
            "--portfolio-ok",
            args.portfolio_ok,
            "--monitor-confirmed",
            args.monitor_confirmed,
            "--stake-cap-pct-bankroll",
            str(args.stake_cap_pct_bankroll),
            "--notes",
            args.notes,
        ]))

    for label, cmd in steps:
        run_step(label, cmd)

    row = build_pipeline_row(
        args.date,
        args.home,
        args.away,
        args.market_family,
        args.odds,
        processed_dir,
        args.skip_confirmation,
        args.stake_cap_pct_bankroll,
        args.notes,
    )

    for folder in [today, processed_dir / "governance"]:
        write_csv(folder / f"vsigma_full_shadow_pipeline_{slug}_{safe_market}.csv", row)
        (folder / f"vsigma_full_shadow_pipeline_{slug}_{safe_market}.md").write_text(md(row), encoding="utf-8")

    print("\n=== vSIGMA FULL SHADOW PIPELINE ===")
    print(f"FINAL: {row['pipeline_final_verdict']}")
    print(f"MARKET: {row['selected_market']}")
    print(f"ODDS: {row['selected_odds']}")
    print(f"EV: {row['selected_expected_roi']}")
    print(f"EDGE: {row['selected_edge_prob']}")
    print(f"STAKE CAP: {row['stake_cap_pct_bankroll']}%")
    print("AUTO_BET: NO")
    print(f"REPORT: {today / f'vsigma_full_shadow_pipeline_{slug}_{safe_market}.md'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--market-family", required=True)
    parser.add_argument("--odds", type=float, required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    parser.add_argument("--market-under25-prob", type=float, default=None)
    parser.add_argument("--market-over25-prob", type=float, default=None)
    parser.add_argument("--min-edge", type=float, default=0.025)
    parser.add_argument("--min-ev", type=float, default=0.03)
    parser.add_argument("--lineups-confirmed", default="PENDING")
    parser.add_argument("--tactical-confirmed", default="PENDING")
    parser.add_argument("--price-live", default="PENDING")
    parser.add_argument("--portfolio-ok", default="PENDING")
    parser.add_argument("--monitor-confirmed", default="PENDING")
    parser.add_argument("--stake-cap-pct-bankroll", type=float, default=0.25)
    parser.add_argument("--notes", default="")
    parser.add_argument("--skip-confirmation", action="store_true")
    run_pipeline(parser.parse_args())
