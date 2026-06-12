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


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return dict(rows[0]) if rows else {}


def write_csv(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(row.keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fields})


def market_action(u35: dict[str, str], agreement: dict[str, str]) -> dict[str, str]:
    label = str(u35.get("u35_gate_label", "U35_GATE_MISSING"))
    can_veto = str(u35.get("can_veto_over_btts_builder", "NO"))

    if label in {"", "U35_GATE_MISSING"}:
        return {
            "u35_market_action_hint": "NO_ACTION_NO_GATE",
            "u35_builder_veto_hint": "NO",
            "u35_market_family_hint": "NONE",
            "u35_execution_note": "U35 gate file missing. Do not use U35 layer.",
        }

    if label == "OUT_OF_SCOPE_NOT_TOP5":
        return {
            "u35_market_action_hint": "NO_ACTION_OUT_OF_SCOPE",
            "u35_builder_veto_hint": "NO",
            "u35_market_family_hint": "NONE",
            "u35_execution_note": "Fixture is outside trained top-5 league scope. Ignore U35 probability.",
        }

    if label == "NO_PREMIUM_ZONE":
        return {
            "u35_market_action_hint": "NO_PREMIUM_VALIDATION",
            "u35_builder_veto_hint": "NO",
            "u35_market_family_hint": "UNDER35_NOT_PREMIUM",
            "u35_execution_note": "p_under35 is in noisy 0.70-0.75 zone. Do not validate premium Under 3.5.",
        }

    if label == "SUPPORT":
        return {
            "u35_market_action_hint": "U35_SUPPORT_ONLY",
            "u35_builder_veto_hint": "WEAK_ONLY" if can_veto.startswith("YES") else "NO",
            "u35_market_family_hint": "UNDER35_SECONDARY_SUPPORT",
            "u35_execution_note": "Use only as secondary support if vSIGMA tactical read and market family agree.",
        }

    if label == "STRONG":
        return {
            "u35_market_action_hint": "U35_VALIDATE_UNDER35",
            "u35_builder_veto_hint": "YES" if can_veto == "YES" else "NO",
            "u35_market_family_hint": "UNDER35_OR_PROTECTED_BUILDER",
            "u35_execution_note": "Can validate Under 3.5/protected builder if tactical read agrees. Can veto overstretched Over/BTTS.",
        }

    if label == "STRONG_CLEAN":
        return {
            "u35_market_action_hint": "U35_STRONG_CLEAN_VALIDATE_UNDER35",
            "u35_builder_veto_hint": "YES",
            "u35_market_family_hint": "UNDER35_PRIMARY_GATE",
            "u35_execution_note": "Strong clean Under 3.5 gate. Prefer Under 3.5/protected low-total builders; avoid aggressive Over/BTTS.",
        }

    if label == "ELITE":
        return {
            "u35_market_action_hint": "U35_ELITE_VALIDATE_UNDER35",
            "u35_builder_veto_hint": "YES",
            "u35_market_family_hint": "UNDER35_ELITE_GATE",
            "u35_execution_note": "Elite U35 gate. Strong reinforcement only; still no auto-bet without tactical and lineup confirmation.",
        }

    return {
        "u35_market_action_hint": "NO_ACTION_UNKNOWN_LABEL",
        "u35_builder_veto_hint": "NO",
        "u35_market_family_hint": "UNKNOWN",
        "u35_execution_note": f"Unknown U35 label: {label}",
    }


def md(row: dict[str, object]) -> str:
    return "\n".join([
        f"# vSIGMA U35 Market Action Hint - {row.get('target_date')}",
        "",
        f"- fixture: {row.get('fixture')}",
        f"- agreement_label: {row.get('agreement_label')}",
        f"- u35_gate_label: {row.get('u35_gate_label')}",
        f"- u35_market_action_hint: {row.get('u35_market_action_hint')}",
        f"- u35_builder_veto_hint: {row.get('u35_builder_veto_hint')}",
        f"- u35_market_family_hint: {row.get('u35_market_family_hint')}",
        f"- note: {row.get('u35_execution_note')}",
        "",
        "## Governance",
        "- auto_bet: NO",
        "- production_change: NO",
        "- final decision still belongs to vSIGMA tactical + lineup + market survival.",
    ]) + "\n"


def run(day: str, home: str, away: str, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    u35 = read_one(base / "today" / day / f"vsigma_under35_shadow_gate_{slug}.csv")
    agreement = read_one(base / "today" / day / f"vsigma_ml_agreement_{slug}.csv")

    action = market_action(u35, agreement)
    row = {
        "target_date": day,
        "fixture": slug.replace("_", " "),
        "agreement_label": agreement.get("agreement_label", ""),
        "agreement_score": agreement.get("agreement_score", ""),
        "u35_gate_label": u35.get("u35_gate_label", "U35_GATE_MISSING"),
        "model_under35_prob": u35.get("model_under35_prob", ""),
        "market_under25_prob": u35.get("market_under25_prob", ""),
        "can_validate_under35": u35.get("can_validate_under35", ""),
        "can_veto_over_btts_builder": u35.get("can_veto_over_btts_builder", ""),
        **action,
        "auto_bet": "NO",
        "production_change": "NO",
    }

    for folder in [base / "today" / day, base / "governance"]:
        write_csv(folder / f"vsigma_u35_market_action_hint_{slug}.csv", row)
        (folder / f"vsigma_u35_market_action_hint_{slug}.md").write_text(md(row), encoding="utf-8")

    print(f"U35 market action hint built: {row['u35_market_action_hint']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--away", required=True)
    ap.add_argument("--processed-dir", type=Path, default=BASE)
    args = ap.parse_args()
    run(args.date, args.home, args.away, args.processed_dir)
