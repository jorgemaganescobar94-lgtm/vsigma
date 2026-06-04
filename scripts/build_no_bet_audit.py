from __future__ import annotations

import argparse
import csv
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
    "decision_bucket",
    "translation_audit_status",
    "translation_quality_label",
    "market_family",
    "result_source_status",
    "actual_home_goals",
    "actual_away_goals",
    "actual_total_goals",
    "actual_total_xg",
    "actual_total_sot",
    "actual_total_big",
    "no_bet_audit_status",
    "no_bet_quality_label",
    "no_bet_evidence_profile",
    "missed_opportunity_risk",
    "protection_value_signal",
    "learning_action",
    "manual_review_required",
    "audit_note",
    "source_guard",
    "auto_apply",
    "production_change",
]


def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default


def up(value: object) -> str:
    return norm(value).upper()


def as_float(value: object) -> float | None:
    text = norm(value)
    if not text or text.lower() == "nan":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def as_int(value: object) -> int | None:
    val = as_float(value)
    if val is None:
        return None
    return int(round(val))


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


def load_translation_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_market_translation_audit_daily.csv", "vsigma_market_translation_audit.csv"])
    if not path:
        return []
    rows = read_csv(path)
    if path.name == "vsigma_market_translation_audit.csv":
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows


def load_actuals(processed: Path, day: str) -> dict[str, dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_post_match_stat_actuals.csv"])
    rows = read_csv(path) if path else []
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid:
            out[fid] = row
    return out


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def actual_by_translation_row(row: dict[str, str], actuals: dict[str, dict[str, str]]) -> dict[str, str]:
    fid = fixture_id(row)
    return actuals.get(fid, {}) if fid else {}


def value_from(row: dict[str, str], actual: dict[str, str], name: str) -> str:
    return norm(row.get(name)) or norm(actual.get(name))


def evidence_profile(row: dict[str, str], actual: dict[str, str]) -> str:
    total_goals = as_float(value_from(row, actual, "actual_total_goals"))
    total_xg = as_float(value_from(row, actual, "actual_total_xg"))
    total_sot = as_float(value_from(row, actual, "actual_total_sot"))
    total_big = as_float(value_from(row, actual, "actual_total_big"))

    known = 0
    high = 0
    low = 0

    if total_goals is not None:
        known += 1
        if total_goals >= 4:
            high += 1
        if total_goals <= 1:
            low += 1
    if total_xg is not None:
        known += 1
        if total_xg >= 3.0:
            high += 1
        if total_xg <= 1.5:
            low += 1
    if total_sot is not None:
        known += 1
        if total_sot >= 10:
            high += 1
        if total_sot <= 5:
            low += 1
    if total_big is not None:
        known += 1
        if total_big >= 4:
            high += 1
        if total_big <= 1:
            low += 1

    if known == 0:
        return "NO_POSTMATCH_PRESSURE_METRICS"
    if high >= 2:
        return "HIGH_VOLATILITY_OR_HIGH_EVENT_MATCH"
    if low >= 2:
        return "LOW_EVENT_MATCH"
    return "MIXED_OR_MEDIUM_EVENT_MATCH"


def classify_no_bet(row: dict[str, str], actual: dict[str, str]) -> dict[str, str]:
    decision_bucket = up(row.get("decision_bucket"))
    translation_status = up(row.get("translation_audit_status"))
    quality_label = up(row.get("translation_quality_label"))
    fid = fixture_id(row)
    has_actual = bool(actual) or norm(row.get("result_source_status")) == "FINAL_ACTUALS_FOUND"
    profile = evidence_profile(row, actual)

    is_diagnostic = (
        "DIAGNOSTIC" in decision_bucket
        or "DIAGNOSTIC" in translation_status
        or "DIAGNOSTIC" in quality_label
        or fid.startswith("DIAGNOSTIC")
    )
    is_no_bet = decision_bucket == "NO_BET" or "NO_BET" in translation_status or "NO_BET" in quality_label

    if is_diagnostic:
        return {
            "no_bet_audit_status": "NO_BET_AUDIT_NOT_REQUIRED_DIAGNOSTIC",
            "no_bet_quality_label": "DIAGNOSTIC_NOT_REAL_FIXTURE_NO_BET",
            "no_bet_evidence_profile": profile,
            "missed_opportunity_risk": "NOT_APPLICABLE",
            "protection_value_signal": "NOT_APPLICABLE",
            "learning_action": "NO_MODEL_CHANGE",
            "manual_review_required": "NO",
            "audit_note": "Diagnostic row; no fixture-level No Bet correctness can be evaluated.",
        }

    if not is_no_bet:
        return {
            "no_bet_audit_status": "NO_BET_AUDIT_NOT_APPLICABLE",
            "no_bet_quality_label": "NOT_A_NO_BET_ROW",
            "no_bet_evidence_profile": profile,
            "missed_opportunity_risk": "NOT_APPLICABLE",
            "protection_value_signal": "NOT_APPLICABLE",
            "learning_action": "NO_MODEL_CHANGE",
            "manual_review_required": "NO",
            "audit_note": "Row is not a No Bet decision; handled by pick quality/market translation audits.",
        }

    if not has_actual:
        return {
            "no_bet_audit_status": "NO_BET_AUDIT_PENDING_FINAL_ACTUALS",
            "no_bet_quality_label": "PENDING",
            "no_bet_evidence_profile": profile,
            "missed_opportunity_risk": "PENDING",
            "protection_value_signal": "PENDING",
            "learning_action": "WAIT_FOR_FINAL_ACTUALS",
            "manual_review_required": "NO",
            "audit_note": "Real No Bet row but final actuals are not available yet.",
        }

    if profile == "HIGH_VOLATILITY_OR_HIGH_EVENT_MATCH":
        return {
            "no_bet_audit_status": "NO_BET_CAUSAL_REVIEW_READY",
            "no_bet_quality_label": "NO_BET_PROTECTION_CANDIDATE",
            "no_bet_evidence_profile": profile,
            "missed_opportunity_risk": "LOW_TO_MEDIUM_PENDING_MARKET_REVIEW",
            "protection_value_signal": "HIGH",
            "learning_action": "REVIEW_FOR_NO_BET_CORRECTNESS_REINFORCEMENT",
            "manual_review_required": "YES",
            "audit_note": "Final match looked volatile/high-event; No Bet may have protected against fragile markets. Confirm against pre-match candidates.",
        }

    if profile == "LOW_EVENT_MATCH":
        return {
            "no_bet_audit_status": "NO_BET_CAUSAL_REVIEW_READY",
            "no_bet_quality_label": "NO_BET_TOO_CONSERVATIVE_CANDIDATE",
            "no_bet_evidence_profile": profile,
            "missed_opportunity_risk": "MEDIUM_TO_HIGH_PENDING_MARKET_REVIEW",
            "protection_value_signal": "LOW",
            "learning_action": "REVIEW_FOR_MISSED_SAFE_MARKET",
            "manual_review_required": "YES",
            "audit_note": "Final match looked low-event; review if a safe market was missed or if pre-match data correctly blocked it.",
        }

    return {
        "no_bet_audit_status": "NO_BET_CAUSAL_REVIEW_READY",
        "no_bet_quality_label": "NO_BET_NEUTRAL_REVIEW_REQUIRED",
        "no_bet_evidence_profile": profile,
        "missed_opportunity_risk": "UNKNOWN_PENDING_MARKET_REVIEW",
        "protection_value_signal": "MEDIUM_OR_UNKNOWN",
        "learning_action": "MANUAL_REVIEW_BEFORE_MODEL_CHANGE",
        "manual_review_required": "YES",
        "audit_note": "Final match evidence is mixed/medium; review with pre-match candidates before judging No Bet correctness.",
    }


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_translation_rows(processed, day)
    actuals = load_actuals(processed, day)
    if not rows:
        rows = [{
            "target_date": day,
            "ledger_key": f"{day}|NO_MARKET_TRANSLATION_AUDIT",
            "fixture_id": "DIAGNOSTIC_NO_MARKET_TRANSLATION_AUDIT",
            "home_team": "NO_MARKET_TRANSLATION_AUDIT",
            "away_team": "NO_MARKET_TRANSLATION_AUDIT",
            "primary_market": "NO_MARKET",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "translation_audit_status": "TRANSLATION_NOT_AVAILABLE",
            "translation_quality_label": "DIAGNOSTIC_NO_MARKET_LEARNING",
            "market_family": "NO_MARKET",
        }]

    out: list[dict[str, object]] = []
    for row in rows:
        actual = actual_by_translation_row(row, actuals)
        cls = classify_no_bet(row, actual)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "ledger_key": norm(row.get("ledger_key")),
            "fixture_id": fixture_id(row),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "primary_market": norm(row.get("primary_market"), "NO_MARKET"),
            "decision_bucket": norm(row.get("decision_bucket")),
            "translation_audit_status": norm(row.get("translation_audit_status")),
            "translation_quality_label": norm(row.get("translation_quality_label")),
            "market_family": norm(row.get("market_family"), "UNKNOWN_FAMILY"),
            "result_source_status": norm(row.get("result_source_status")) or ("FINAL_ACTUALS_FOUND" if actual else "NO_FINAL_ACTUALS_FOUND"),
            "actual_home_goals": norm(row.get("actual_home_goals")) or norm(actual.get("actual_home_goals")),
            "actual_away_goals": norm(row.get("actual_away_goals")) or norm(actual.get("actual_away_goals")),
            "actual_total_goals": norm(row.get("actual_total_goals")) or norm(actual.get("actual_total_goals")),
            "actual_total_xg": norm(row.get("actual_total_xg")) or norm(actual.get("actual_total_xg")),
            "actual_total_sot": norm(row.get("actual_total_sot")) or norm(actual.get("actual_total_sot")),
            "actual_total_big": norm(row.get("actual_total_big")) or norm(actual.get("actual_total_big")),
            **cls,
            "source_guard": "NO_BET_AUDIT_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def update_historical(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    path = processed / "governance" / "vsigma_no_bet_audit.csv"
    existing = read_csv(path)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(path, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA No Bet Audit - {day}",
        "",
        "## Summary",
        f"audit_rows: {len(rows)}",
        f"- no_bet_audit_status_counts: {fmt_counts(rows, 'no_bet_audit_status')}",
        f"- no_bet_quality_label_counts: {fmt_counts(rows, 'no_bet_quality_label')}",
        f"- evidence_profile_counts: {fmt_counts(rows, 'no_bet_evidence_profile')}",
        f"- missed_opportunity_risk_counts: {fmt_counts(rows, 'missed_opportunity_risk')}",
        f"- protection_value_signal_counts: {fmt_counts(rows, 'protection_value_signal')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Audit Rows",
    ]
    for row in rows[:100]:
        lines.append(
            "- "
            f"{row.get('no_bet_audit_status', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"quality={row.get('no_bet_quality_label', '')} | evidence={row.get('no_bet_evidence_profile', '')} | "
            f"missed={row.get('missed_opportunity_risk', '')} | protection={row.get('protection_value_signal', '')} | "
            f"manual={row.get('manual_review_required', '')} | note={row.get('audit_note', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This audit does not create picks, stake permission, or automatic model changes.",
        "- NO_BET_PROTECTION_CANDIDATE and NO_BET_TOO_CONSERVATIVE_CANDIDATE are review labels, not final truth.",
        "- A No Bet can only become a learning signal after causal review and sufficient sample size.",
        "- Diagnostic rows must not train the model.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_no_bet_audit_daily.csv", rows, FIELDS)
        (base / "vsigma_no_bet_audit.md").write_text(markdown(day, rows), encoding="utf-8")
    update_historical(processed, day, rows)

    print("=== VSIGMA NO BET AUDIT ===")
    print(f"audit_rows={len(rows)}")
    print(f"no_bet_audit_status_counts={fmt_counts(rows, 'no_bet_audit_status')}")
    print(f"no_bet_quality_label_counts={fmt_counts(rows, 'no_bet_quality_label')}")
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
