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


def top_result(row: dict[str, str]) -> str:
    probs = {
        "HOME": fnum(row.get("home_prob") or row.get("raw_home_prob")),
        "DRAW": fnum(row.get("draw_prob") or row.get("raw_draw_prob")),
        "AWAY": fnum(row.get("away_prob") or row.get("raw_away_prob")),
    }
    if not any(probs.values()):
        return ""
    return max(probs, key=probs.get)


def compact_markets(rows: list[dict[str, str]], label_set: set[str]) -> list[str]:
    out: list[str] = []
    for row in rows:
        if str(row.get("team_total_gate_label")) in label_set:
            out.append(f"{row.get('market_family')}:{row.get('team_total_gate_label')}@{row.get('model_prob')}")
    return out


def governance_decision(
    agreement: dict[str, str],
    u35_action: dict[str, str],
    tt_rows: list[dict[str, str]],
) -> dict[str, object]:
    agreement_label = str(agreement.get("agreement_label", ""))
    agreement_score = fnum(agreement.get("agreement_score"), 0.0)
    u35_hint = str(u35_action.get("u35_market_action_hint", ""))
    u35_veto = str(u35_action.get("u35_builder_veto_hint", ""))

    tt_strong = [r for r in tt_rows if str(r.get("team_total_gate_label")) == "TEAM_TOTAL_STRONG"]
    tt_support = [r for r in tt_rows if str(r.get("team_total_gate_label")) == "TEAM_TOTAL_SUPPORT"]
    tt_veto = [r for r in tt_rows if str(r.get("can_veto_overstretch")) == "YES"]

    u35_validates = u35_hint in {
        "U35_VALIDATE_UNDER35",
        "U35_STRONG_CLEAN_VALIDATE_UNDER35",
        "U35_ELITE_VALIDATE_UNDER35",
    }
    u35_support = u35_hint == "U35_SUPPORT_ONLY"
    low_agreement = agreement_label == "LOW_AGREEMENT" or (agreement_score and agreement_score < 55)

    veto_flags: list[str] = []
    if u35_veto == "YES":
        veto_flags.append("U35_VETO_OVER_BTTS_BUILDER")
    if tt_veto:
        veto_flags.append("TT_UNDER15_VETO_OVERSTRETCH")
    if low_agreement:
        veto_flags.append("LOW_AGREEMENT_MANUAL_REVIEW")

    approved: list[str] = []
    if u35_validates:
        approved.append("UNDER35_PROTECTED_LOW_TOTAL")
    elif u35_support:
        approved.append("UNDER35_SECONDARY_SUPPORT")

    for row in tt_strong:
        approved.append(str(row.get("market_family")))
    for row in tt_support:
        approved.append(str(row.get("market_family")) + "_SECONDARY")

    if low_agreement:
        label = "MANUAL_REVIEW_LOW_AGREEMENT"
        builder_permission = "NO"
        note = "ML agreement is low. Do not build combo without manual review."
    elif u35_validates and tt_strong:
        label = "PROTECTED_BUILDER_CANDIDATE"
        builder_permission = "YES_PROTECTED_ONLY_WITH_PRICE_CHECK"
        note = "U35 and strong team-total gate align. Builder can be considered only if tactical read, lineup and price survive."
    elif u35_validates:
        label = "LOW_TOTAL_GATE_ACTIVE"
        builder_permission = "SECONDARY_ONLY"
        note = "U35 validates low-total structure, but team-total support is not strong enough for a protected builder alone."
    elif tt_strong:
        label = "TEAM_TOTAL_GATE_ACTIVE"
        builder_permission = "YES_WITH_PRICE_CHECK"
        note = "Strong team-total gate exists. Use as support/validation, not automatic standalone."
    elif u35_support or tt_support:
        label = "SECONDARY_SUPPORT_ONLY"
        builder_permission = "SECONDARY_ONLY"
        note = "Only secondary support exists. Do not upgrade market without tactical and price confirmation."
    else:
        label = "NO_GATE_SUPPORT"
        builder_permission = "NO"
        note = "No promoted gate supports this fixture. Prefer base vSIGMA/manual review."

    return {
        "market_governance_label": label,
        "builder_permission": builder_permission,
        "approved_market_families": ";".join([a for a in approved if a]),
        "veto_flags": ";".join(veto_flags),
        "team_total_strong_count": len(tt_strong),
        "team_total_support_count": len(tt_support),
        "team_total_veto_count": len(tt_veto),
        "team_total_strong_markets": ";".join(compact_markets(tt_strong, {"TEAM_TOTAL_STRONG"})),
        "team_total_support_markets": ";".join(compact_markets(tt_support, {"TEAM_TOTAL_SUPPORT"})),
        "decision_note": note,
    }


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA Market Governance Summary - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- vsigma_result: {row.get('vsigma_result')}",
        f"- agreement_label: {row.get('agreement_label')}",
        f"- agreement_score: {row.get('agreement_score')}",
        f"- market_governance_label: {row.get('market_governance_label')}",
        f"- builder_permission: {row.get('builder_permission')}",
        f"- approved_market_families: {row.get('approved_market_families')}",
        f"- veto_flags: {row.get('veto_flags')}",
        "",
        "## U35 layer",
        f"- u35_gate_label: {row.get('u35_gate_label')}",
        f"- u35_market_action_hint: {row.get('u35_market_action_hint')}",
        f"- u35_builder_veto_hint: {row.get('u35_builder_veto_hint')}",
        "",
        "## Team-total layer",
        f"- strong_count: {row.get('team_total_strong_count')}",
        f"- support_count: {row.get('team_total_support_count')}",
        f"- veto_count: {row.get('team_total_veto_count')}",
        f"- strong_markets: {row.get('team_total_strong_markets')}",
        f"- support_markets: {row.get('team_total_support_markets')}",
        "",
        "## Decision note",
        f"- {row.get('decision_note')}",
        "",
        "## Governance",
        "- auto_bet: NO",
        "- production_change: NO",
        "- This summary coordinates gates only; final execution still requires tactical read, lineups and price survival.",
    ]) + "\n"


def run(day: str, home: str, away: str, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    today = base / "today" / day
    forecast = read_one(today / f"vsigma_adhoc_match_stat_forecast_{slug}.csv")
    agreement = read_one(today / f"vsigma_ml_agreement_{slug}.csv")
    u35_gate = read_one(today / f"vsigma_under35_shadow_gate_{slug}.csv")
    u35_action = read_one(today / f"vsigma_u35_market_action_hint_{slug}.csv")
    tt_rows = read_rows(today / f"vsigma_team_total_gate_{slug}.csv")

    if not forecast:
        raise RuntimeError(f"Missing forecast file for {slug} on {day}")

    decision = governance_decision(agreement, u35_action, tt_rows)
    row = {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "home_team": forecast.get("home_team", home),
        "away_team": forecast.get("away_team", away),
        "league_id": forecast.get("league_id", ""),
        "league_name": forecast.get("league_name", ""),
        "vsigma_result": top_result(forecast),
        "agreement_label": agreement.get("agreement_label", "MISSING"),
        "agreement_score": agreement.get("agreement_score", ""),
        "agreement_reasons": agreement.get("agreement_reasons", ""),
        "u35_gate_label": u35_gate.get("u35_gate_label", "MISSING"),
        "u35_market_action_hint": u35_action.get("u35_market_action_hint", "MISSING"),
        "u35_builder_veto_hint": u35_action.get("u35_builder_veto_hint", ""),
        "u35_market_family_hint": u35_action.get("u35_market_family_hint", ""),
        **decision,
        "auto_bet": "NO",
        "production_change": "NO",
    }

    for folder in [today, base / "governance"]:
        write_csv(folder / f"vsigma_market_governance_summary_{slug}.csv", row)
        (folder / f"vsigma_market_governance_summary_{slug}.md").write_text(md(row), encoding="utf-8")

    print(f"Market governance built for {home} vs {away}: {row['market_governance_label']} builder={row['builder_permission']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--home", required=True)
    parser.add_argument("--away", required=True)
    parser.add_argument("--processed-dir", type=Path, default=BASE)
    args = parser.parse_args()
    run(args.date, args.home, args.away, args.processed_dir)
