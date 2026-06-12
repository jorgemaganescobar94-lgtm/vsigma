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


def read_one(path: Path) -> dict[str, str]:
    if not path.exists():
        raise RuntimeError(f"Missing file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise RuntimeError(f"Empty file: {path}")
    return dict(rows[0])


def read_optional(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return dict(rows[0]) if rows else {}


def top_result(h: float, d: float, a: float) -> str:
    return max({"HOME": h, "DRAW": d, "AWAY": a}, key={"HOME": h, "DRAW": d, "AWAY": a}.get)


def score(v: dict[str, str], m: dict[str, str]) -> dict[str, object]:
    points = 0
    reasons = []
    vres = top_result(fnum(v.get("home_prob")), fnum(v.get("draw_prob")), fnum(v.get("away_prob")))
    mres = str(m.get("ml_result_forecast", ""))
    if vres == mres:
        points += 35; reasons.append("RESULT_AGREE")
    else:
        reasons.append(f"RESULT_DIVERGE:{vres}_vs_{mres}")
    prob_l1 = abs(fnum(v.get("home_prob"))-fnum(m.get("ml_home_prob"))) + abs(fnum(v.get("draw_prob"))-fnum(m.get("ml_draw_prob"))) + abs(fnum(v.get("away_prob"))-fnum(m.get("ml_away_prob")))
    if prob_l1 <= 0.25:
        points += 15; reasons.append("PROB_CLOSE")
    elif prob_l1 <= 0.50:
        points += 8; reasons.append("PROB_PARTIAL")
    else:
        reasons.append("PROB_DIVERGE")
    vxg = fnum(v.get("home_xg")) + fnum(v.get("away_xg"))
    mg = fnum(m.get("ml_total_goals"), -1)
    if mg >= 0:
        diff = abs(vxg - mg)
        if diff <= 0.45:
            points += 20; reasons.append("GOALS_CLOSE")
        elif diff <= 0.85:
            points += 10; reasons.append("GOALS_PARTIAL")
        else:
            reasons.append("GOALS_DIVERGE")
    vshots = fnum(v.get("home_shots")) + fnum(v.get("away_shots"))
    mshots = fnum(m.get("ml_home_shots"), -1) + fnum(m.get("ml_away_shots"), -1)
    if mshots >= 0:
        diff = abs(vshots - mshots)
        if diff <= 4:
            points += 10; reasons.append("SHOTS_CLOSE")
        elif diff <= 8:
            points += 5; reasons.append("SHOTS_PARTIAL")
        else:
            reasons.append("SHOTS_DIVERGE")
    vcorners = fnum(v.get("home_corners")) + fnum(v.get("away_corners"))
    mcorners = fnum(m.get("ml_home_corners"), -1) + fnum(m.get("ml_away_corners"), -1)
    if mcorners >= 0:
        diff = abs(vcorners - mcorners)
        if diff <= 2:
            points += 10; reasons.append("CORNERS_CLOSE")
        elif diff <= 4:
            points += 5; reasons.append("CORNERS_PARTIAL")
        else:
            reasons.append("CORNERS_DIVERGE")
    if str(m.get("ml_probability_sanity")) == "OK" and str(m.get("ml_regression_sanity")) == "OK":
        points += 10; reasons.append("SANITY_OK")
    else:
        reasons.append("SANITY_WARNING")
    label = "HIGH_AGREEMENT" if points >= 80 else ("MEDIUM_AGREEMENT" if points >= 55 else "LOW_AGREEMENT")
    return {"agreement_score": points, "agreement_label": label, "agreement_reasons": ";".join(reasons), "vsigma_result": vres, "ml_result": mres}


def u35_context(v: dict[str, str], u35: dict[str, str]) -> dict[str, object]:
    if not u35:
        return {
            "u35_gate_label": "U35_GATE_MISSING",
            "u35_context": "NO_U35_GATE_FILE",
            "u35_can_validate_under35": "NO",
            "u35_can_veto_over_btts_builder": "NO",
            "u35_model_under35_prob": "",
            "u35_market_under25_prob": "",
        }

    label = str(u35.get("u35_gate_label", ""))
    can_validate = str(u35.get("can_validate_under35", "NO"))
    can_veto = str(u35.get("can_veto_over_btts_builder", "NO"))
    p_under35 = fnum(u35.get("model_under35_prob"))
    market_u25 = fnum(u35.get("market_under25_prob"))
    vxg = fnum(v.get("home_xg")) + fnum(v.get("away_xg"))

    if label in {"ELITE", "STRONG_CLEAN", "STRONG"}:
        if vxg and vxg <= 3.05:
            context = "U35_GATE_ALIGNED_LOW_TOTAL"
        elif vxg >= 3.40:
            context = "U35_GATE_CONFLICTS_WITH_VSIGMA_GOALS"
        else:
            context = "U35_GATE_ACTIVE_NEEDS_TACTICAL_CONFIRMATION"
    elif label == "SUPPORT":
        context = "U35_GATE_SECONDARY_SUPPORT"
    elif label == "NO_PREMIUM_ZONE":
        context = "U35_GATE_NO_PREMIUM_ZONE"
    elif label == "OUT_OF_SCOPE_NOT_TOP5":
        context = "U35_GATE_OUT_OF_SCOPE"
    else:
        context = "U35_GATE_INACTIVE"

    return {
        "u35_gate_label": label,
        "u35_context": context,
        "u35_can_validate_under35": can_validate,
        "u35_can_veto_over_btts_builder": can_veto,
        "u35_model_under35_prob": p_under35,
        "u35_market_under25_prob": market_u25,
    }


def write_outputs(day: str, slug: str, row: dict[str, object], base: Path) -> None:
    fields = [
        "target_date", "fixture",
        "agreement_score", "agreement_label", "agreement_reasons",
        "vsigma_result", "ml_result",
        "u35_gate_label", "u35_context",
        "u35_can_validate_under35", "u35_can_veto_over_btts_builder",
        "u35_model_under35_prob", "u35_market_under25_prob",
        "auto_apply", "production_change"
    ]
    out = {"target_date": day, "fixture": slug.replace("_", " "), "auto_apply": "NO", "production_change": "NO", **row}
    for folder in [base / "today" / day, base / "governance"]:
        folder.mkdir(parents=True, exist_ok=True)
        csv_path = folder / f"vsigma_ml_agreement_{slug}.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader(); writer.writerow({k: out.get(k, "") for k in fields})
        md_path = folder / f"vsigma_ml_agreement_{slug}.md"
        md_path.write_text("\n".join([
            f"# vSIGMA ML Agreement - {day}", "",
            f"- fixture: {out['fixture']}",
            f"- agreement_score: {out['agreement_score']}",
            f"- agreement_label: {out['agreement_label']}",
            f"- agreement_reasons: {out['agreement_reasons']}",
            f"- vsigma_result: {out['vsigma_result']}",
            f"- ml_result: {out['ml_result']}",
            "",
            "## U35 Shadow Gate",
            f"- u35_gate_label: {out.get('u35_gate_label', '')}",
            f"- u35_context: {out.get('u35_context', '')}",
            f"- u35_can_validate_under35: {out.get('u35_can_validate_under35', '')}",
            f"- u35_can_veto_over_btts_builder: {out.get('u35_can_veto_over_btts_builder', '')}",
            f"- u35_model_under35_prob: {out.get('u35_model_under35_prob', '')}",
            f"- u35_market_under25_prob: {out.get('u35_market_under25_prob', '')}",
            "",
            "- auto_apply: NO",
            "- production_change: NO",
            "",
            "## Interpretation",
            "- HIGH_AGREEMENT: ML can reinforce vSIGMA, still shadow-only unless model is promoted.",
            "- MEDIUM_AGREEMENT: use as context; avoid aggressive escalation.",
            "- LOW_AGREEMENT: disagreement alert; prefer manual review/protected/live markets.",
        ]) + "\n", encoding="utf-8")


def run(day: str, home: str, away: str, base: Path) -> None:
    slug = clean(f"{home}_vs_{away}")
    v = read_one(base / "today" / day / f"vsigma_adhoc_match_stat_forecast_{slug}.csv")
    m = read_one(base / "today" / day / f"vsigma_ml_shadow_forecast_{slug}.csv")
    u35 = read_optional(base / "today" / day / f"vsigma_under35_shadow_gate_{slug}.csv")
    row = score(v, m)
    u35_row = u35_context(v, u35)
    row.update(u35_row)
    if u35_row.get("u35_gate_label") not in {"", "U35_GATE_MISSING"}:
        row["agreement_reasons"] = str(row.get("agreement_reasons", "")) + ";U35_GATE:" + str(u35_row.get("u35_gate_label"))
    write_outputs(day, slug, row, base)
    print(f"agreement={row['agreement_label']} score={row['agreement_score']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--home", required=True)
    ap.add_argument("--away", required=True)
    ap.add_argument("--processed-dir", type=Path, default=BASE)
    args = ap.parse_args()
    run(args.date, args.home, args.away, args.processed_dir)
