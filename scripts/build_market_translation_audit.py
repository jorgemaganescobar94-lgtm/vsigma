from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "ledger_key",
    "fixture_id",
    "home_team",
    "away_team",
    "primary_market",
    "market_family",
    "final_decision",
    "decision_bucket",
    "pick_outcome",
    "quality_class",
    "error_family",
    "learning_action",
    "translation_audit_status",
    "translation_quality_label",
    "translation_error_family",
    "suggested_safer_family",
    "suggested_odds_escalation_status",
    "manual_review_required",
    "translation_note",
    "source_guard",
    "auto_apply",
    "production_change",
]


def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default


def up(value: object) -> str:
    return norm(value).upper()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def first_existing(processed: Path, day: str, names: list[str]) -> Path | None:
    candidates: list[Path] = []
    for name in names:
        candidates.append(processed / "today" / day / name)
        candidates.append(processed / "governance" / name)
    for path in candidates:
        if path.exists():
            return path
    return None


def load_quality_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_pick_quality_classification_daily.csv", "vsigma_pick_quality_classification.csv"])
    if not path:
        return []
    rows = read_csv(path)
    if path.name == "vsigma_pick_quality_classification.csv":
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows


def infer_market_family(market: str, decision: str = "") -> str:
    text = f"{up(market)} {up(decision)}"
    if not text.strip() or "NO_MARKET" in text:
        return "NO_MARKET"
    if any(token in text for token in ["BTTS", "BOTH TEAMS", "AMBOS"]):
        return "BTTS"
    if "TEAM TOTAL" in text or "TT " in text or "EQUIPO" in text:
        return "TEAM_TOTAL"
    if "CORNER" in text or "CÓRNER" in text or "CORNERS" in text:
        return "CORNERS"
    if "CARD" in text or "TARJ" in text:
        return "CARDS"
    if "UNDER" in text or "OVER" in text or re.search(r"\b[UO]\s*\d", text):
        return "TOTAL_GOALS"
    if "DNB" in text or "DRAW NO BET" in text or "+0" in text or "AH 0" in text:
        return "DNB_AH0"
    if "DOUBLE CHANCE" in text or "DOBLE" in text or "1X" in text or "X2" in text or "+0.5" in text:
        return "DOUBLE_CHANCE_AH_POSITIVE"
    if "HANDICAP" in text or " AH" in text or re.search(r"[+-]\d(?:\.\d)?", text):
        return "HANDICAP"
    if any(token in text for token in ["HOME WIN", "AWAY WIN", "LOCAL GANA", "VISITANTE GANA", " ML", "MONEYLINE", "WIN"]):
        return "MATCH_WINNER"
    return "UNKNOWN_FAMILY"


def safer_family(family: str, quality_class: str, outcome: str) -> str:
    q = up(quality_class)
    o = up(outcome)
    if family == "MATCH_WINNER":
        return "DNB_OR_DOUBLE_CHANCE_WHEN_DRAW_LIVES"
    if family == "HANDICAP":
        return "LOWER_HANDICAP_OR_DNB_IF_TWO_STRIKE_RISK"
    if family == "TOTAL_GOALS":
        if "FRAGILE" in q or o == "RED":
            return "WIDER_TOTAL_OR_LIVE_CONFIRMATION"
        return "SAME_TOTAL_FAMILY_REVIEW_LINE_WIDTH"
    if family == "BTTS":
        return "OVER_1_5_OR_TEAM_TOTAL_IF_ONE_SIDE_EDGE_DOMINATES"
    if family == "TEAM_TOTAL":
        return "TEAM_TOTAL_LOWER_LINE_OR_OVER_1_5_GAME"
    if family == "DNB_AH0":
        return "DOUBLE_CHANCE_IF_DRAW_SURVIVAL_IS_PRIORITY"
    if family == "DOUBLE_CHANCE_AH_POSITIVE":
        return "KEEP_PROTECTED_FAMILY_UNLESS_PRICE_TOO_LOW"
    if family == "NO_MARKET":
        return "NO_MARKET"
    return "MANUAL_FAMILY_REVIEW"


def odds_escalation_status(family: str, quality_class: str, outcome: str) -> str:
    q = up(quality_class)
    o = up(outcome)
    if family in {"NO_MARKET", "UNKNOWN_FAMILY"}:
        return "NOT_APPLICABLE"
    if "FRAGILE" in q or "LUCKY" in q:
        return "DO_NOT_ESCALATE_ODDS"
    if o == "RED":
        return "NO_ESCALATION_REVIEW_FAILURE_FIRST"
    if o == "VOID":
        return "NO_ESCALATION_VOID"
    if "GREEN_CLEAN" in q:
        return "ESCALATION_ALLOWED_ONLY_AFTER_SAMPLE_AND_PRICE_CHECK"
    if "GREEN" in q:
        return "ESCALATION_HOLD_UNTIL_CAUSAL_REVIEW"
    return "NO_ESCALATION_WITHOUT_MANUAL_REVIEW"


def classify_translation(row: dict[str, str]) -> dict[str, str]:
    market = norm(row.get("primary_market"), "NO_MARKET")
    decision = norm(row.get("final_decision"))
    family = infer_market_family(market, decision)
    qclass = up(row.get("quality_class"))
    outcome = up(row.get("pick_outcome"))
    decision_bucket = up(row.get("decision_bucket"))
    error_family = up(row.get("error_family"))

    if "DIAGNOSTIC" in qclass or "DIAGNOSTIC" in decision_bucket:
        return {
            "market_family": family,
            "translation_audit_status": "TRANSLATION_NOT_REQUIRED_DIAGNOSTIC",
            "translation_quality_label": "DIAGNOSTIC_NO_MARKET_LEARNING",
            "translation_error_family": "NONE",
            "suggested_safer_family": "NO_MARKET",
            "suggested_odds_escalation_status": "NOT_APPLICABLE",
            "manual_review_required": "NO",
            "translation_note": "Diagnostic/non-fixture row; market translation must not train the model.",
        }

    if "PENDING" in qclass or outcome == "PENDING":
        return {
            "market_family": family,
            "translation_audit_status": "TRANSLATION_PENDING_RESULT_OR_CAUSAL_REVIEW",
            "translation_quality_label": "PENDING",
            "translation_error_family": "PENDING",
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": "NO_ESCALATION_PENDING",
            "manual_review_required": "NO",
            "translation_note": "Waiting for final actuals or causal review before judging market translation.",
        }

    if decision_bucket == "NO_BET" or "NO_BET" in qclass:
        return {
            "market_family": family,
            "translation_audit_status": "NO_BET_TRANSLATION_REVIEW_REQUIRED",
            "translation_quality_label": "NO_BET_MARKET_OPPORTUNITY_REVIEW",
            "translation_error_family": "NO_BET_CORRECTNESS_PENDING",
            "suggested_safer_family": "REVIEW_IF_ANY_MARKET_SHOULD_HAVE_EXISTED",
            "suggested_odds_escalation_status": "NOT_APPLICABLE",
            "manual_review_required": "YES",
            "translation_note": "Real fixture no-bet must be reviewed for correct protection vs excessive conservatism.",
        }

    if outcome == "GREEN" and "GREEN_CLEAN" in qclass:
        return {
            "market_family": family,
            "translation_audit_status": "MARKET_TRANSLATION_ACCEPTED_CANDIDATE",
            "translation_quality_label": "MARKET_FAMILY_WORKED_CLEANLY",
            "translation_error_family": "NONE",
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": odds_escalation_status(family, qclass, outcome),
            "manual_review_required": "YES",
            "translation_note": "Clean green candidate; confirm with sample before reinforcing market family.",
        }

    if outcome == "GREEN" and ("FRAGILE" in qclass or "LUCKY" in qclass):
        return {
            "market_family": family,
            "translation_audit_status": "MARKET_SURVIVED_BUT_FRAGILE_REVIEW",
            "translation_quality_label": "GREEN_BUT_MARKET_FRAGILITY",
            "translation_error_family": "FRAGILE_MARKET_SELECTION",
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": odds_escalation_status(family, qclass, outcome),
            "manual_review_required": "YES",
            "translation_note": "Green result was fragile; do not raise confidence or odds ladder without causal review.",
        }

    if outcome == "GREEN":
        return {
            "market_family": family,
            "translation_audit_status": "MARKET_TRANSLATION_STANDARD_REVIEW",
            "translation_quality_label": "GREEN_MARKET_REVIEW",
            "translation_error_family": "NONE",
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": odds_escalation_status(family, qclass, outcome),
            "manual_review_required": "YES",
            "translation_note": "Green result requires causal review before market-family reinforcement.",
        }

    if outcome == "RED":
        if "BAD_READ" in qclass or "BAD_MARKET" in error_family:
            translation_error = "BAD_MARKET_OR_BAD_READ_TRANSLATION"
        elif "VARIANCE" in qclass or "VARIANCE" in error_family:
            translation_error = "DO_NOT_BLAME_MARKET_BEFORE_VARIANCE_REVIEW"
        else:
            translation_error = "RED_MARKET_TRANSLATION_CAUSAL_REVIEW"
        return {
            "market_family": family,
            "translation_audit_status": "MARKET_TRANSLATION_FAILURE_REVIEW",
            "translation_quality_label": "RED_MARKET_REVIEW",
            "translation_error_family": translation_error,
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": odds_escalation_status(family, qclass, outcome),
            "manual_review_required": "YES",
            "translation_note": "Red result requires separation between bad read, bad market, bad price and variance.",
        }

    if outcome == "VOID":
        return {
            "market_family": family,
            "translation_audit_status": "VOID_NO_MARKET_REINFORCEMENT",
            "translation_quality_label": "VOID_NO_REINFORCEMENT",
            "translation_error_family": "NONE",
            "suggested_safer_family": safer_family(family, qclass, outcome),
            "suggested_odds_escalation_status": odds_escalation_status(family, qclass, outcome),
            "manual_review_required": "NO",
            "translation_note": "Void result; record but do not reinforce market family.",
        }

    return {
        "market_family": family,
        "translation_audit_status": "MANUAL_TRANSLATION_REVIEW_REQUIRED",
        "translation_quality_label": "UNKNOWN_TRANSLATION_STATE",
        "translation_error_family": "UNKNOWN",
        "suggested_safer_family": safer_family(family, qclass, outcome),
        "suggested_odds_escalation_status": "NO_ESCALATION_UNKNOWN",
        "manual_review_required": "YES",
        "translation_note": "Could not classify market translation safely in v1.",
    }


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    quality_rows = load_quality_rows(processed, day)
    if not quality_rows:
        quality_rows = [{
            "target_date": day,
            "ledger_key": f"{day}|NO_PICK_QUALITY_CLASSIFICATION",
            "fixture_id": "DIAGNOSTIC_NO_PICK_QUALITY_CLASSIFICATION",
            "home_team": "NO_PICK_QUALITY_CLASSIFICATION",
            "away_team": "NO_PICK_QUALITY_CLASSIFICATION",
            "primary_market": "NO_MARKET",
            "final_decision": "NO_BET",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "pick_outcome": "NO_PICK",
            "quality_class": "DIAGNOSTIC_NO_LEARNING",
            "error_family": "NONE",
            "learning_action": "NO_MODEL_CHANGE",
        }]

    out: list[dict[str, object]] = []
    for row in quality_rows:
        trans = classify_translation(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "ledger_key": norm(row.get("ledger_key")),
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "primary_market": norm(row.get("primary_market"), "NO_MARKET"),
            "market_family": trans["market_family"],
            "final_decision": norm(row.get("final_decision")),
            "decision_bucket": norm(row.get("decision_bucket")),
            "pick_outcome": norm(row.get("pick_outcome")),
            "quality_class": norm(row.get("quality_class")),
            "error_family": norm(row.get("error_family")),
            "learning_action": norm(row.get("learning_action")),
            "translation_audit_status": trans["translation_audit_status"],
            "translation_quality_label": trans["translation_quality_label"],
            "translation_error_family": trans["translation_error_family"],
            "suggested_safer_family": trans["suggested_safer_family"],
            "suggested_odds_escalation_status": trans["suggested_odds_escalation_status"],
            "manual_review_required": trans["manual_review_required"],
            "translation_note": trans["translation_note"],
            "source_guard": "MARKET_TRANSLATION_AUDIT_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def update_historical(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    path = processed / "governance" / "vsigma_market_translation_audit.csv"
    existing = read_csv(path)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(path, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Market Translation Audit - {day}",
        "",
        "## Summary",
        f"- audit_rows: {len(rows)}",
        f"- market_family_counts: {fmt_counts(rows, 'market_family')}",
        f"- translation_audit_status_counts: {fmt_counts(rows, 'translation_audit_status')}",
        f"- translation_quality_label_counts: {fmt_counts(rows, 'translation_quality_label')}",
        f"- translation_error_family_counts: {fmt_counts(rows, 'translation_error_family')}",
        f"- odds_escalation_counts: {fmt_counts(rows, 'suggested_odds_escalation_status')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Translation Rows",
    ]
    for row in rows[:80]:
        lines.append(
            "- "
            f"{row.get('translation_audit_status', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"family={row.get('market_family', '')} | market={row.get('primary_market', '')} | "
            f"quality={row.get('translation_quality_label', '')} | safer={row.get('suggested_safer_family', '')} | "
            f"odds={row.get('suggested_odds_escalation_status', '')} | note={row.get('translation_note', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This audit evaluates market translation only; it does not create picks or stake permission.",
        "- Suggested safer families are advisory and require manual/causal review.",
        "- Odds escalation is blocked by default unless sample and price checks later support it.",
        "- Diagnostic rows must not train the model.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_market_translation_audit_daily.csv", rows, FIELDS)
        (base / "vsigma_market_translation_audit.md").write_text(markdown(day, rows), encoding="utf-8")
    update_historical(processed, day, rows)

    print("=== VSIGMA MARKET TRANSLATION AUDIT ===")
    print(f"audit_rows={len(rows)}")
    print(f"translation_audit_status_counts={fmt_counts(rows, 'translation_audit_status')}")
    print(f"market_family_counts={fmt_counts(rows, 'market_family')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    parser.add_argument("--processed-dir", type=Path, default=PROCESSED)
    args = parser.parse_args()
    run(args.date, args.timezone, args.processed_dir)


if __name__ == "__main__":
    main()
