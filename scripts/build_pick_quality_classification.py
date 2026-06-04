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
    "final_decision",
    "decision_bucket",
    "audit_status",
    "pick_outcome",
    "market_grade_status",
    "result_source_status",
    "actual_total_goals",
    "actual_total_xg",
    "actual_total_sot",
    "actual_total_big",
    "quality_class",
    "quality_score",
    "error_family",
    "learning_action",
    "confidence_adjustment",
    "no_bet_quality_label",
    "manual_review_required",
    "classification_note",
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


def load_audit_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_postmatch_pick_audit_daily.csv", "vsigma_postmatch_pick_audit.csv"])
    if not path:
        return []
    rows = read_csv(path)
    if path.name == "vsigma_postmatch_pick_audit.csv":
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows


def as_float(value: object) -> float | None:
    text = norm(value)
    if not text or text.lower() == "nan":
        return None
    try:
        return float(text)
    except ValueError:
        return None


def metric_pressure(row: dict[str, str]) -> str:
    total_xg = as_float(row.get("actual_total_xg"))
    total_sot = as_float(row.get("actual_total_sot"))
    total_big = as_float(row.get("actual_total_big"))

    high_flags = 0
    low_flags = 0
    known = 0

    if total_xg is not None:
        known += 1
        if total_xg >= 3.0:
            high_flags += 1
        if total_xg <= 1.6:
            low_flags += 1
    if total_sot is not None:
        known += 1
        if total_sot >= 10:
            high_flags += 1
        if total_sot <= 5:
            low_flags += 1
    if total_big is not None:
        known += 1
        if total_big >= 4:
            high_flags += 1
        if total_big <= 1:
            low_flags += 1

    if known == 0:
        return "UNKNOWN_PRESSURE"
    if high_flags >= 2:
        return "HIGH_PRESSURE"
    if low_flags >= 2:
        return "LOW_PRESSURE"
    return "MEDIUM_PRESSURE"


def classify_green(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    pressure = metric_pressure(row)
    if pressure == "LOW_PRESSURE":
        return (
            "GREEN_CLEAN_CANDIDATE",
            "82",
            "NONE",
            "REINFORCE_LIGHT_AFTER_CAUSAL_REVIEW",
            "+SMALL_AFTER_SAMPLE",
            "Green result with low event pressure; candidate for clean-green confirmation.",
        )
    if pressure == "HIGH_PRESSURE":
        return (
            "GREEN_FRAGILE_OR_LUCKY_CANDIDATE",
            "55",
            "GREEN_FRAGILITY_REVIEW",
            "DO_NOT_REINFORCE_WITHOUT_CAUSAL_REVIEW",
            "NONE",
            "Green result but underlying pressure was high; avoid strengthening this pattern blindly.",
        )
    return (
        "GREEN_STANDARD_REVIEW",
        "70",
        "NONE",
        "REINFORCE_ONLY_AFTER_SAMPLE",
        "NONE",
        "Green result with medium/unknown pressure; keep for sample-based learning.",
    )


def classify_red(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    pressure = metric_pressure(row)
    if pressure == "LOW_PRESSURE":
        return (
            "RED_VARIANCE_CANDIDATE",
            "58",
            "VARIANCE_OR_CONVERSION_NOISE",
            "DO_NOT_DOWNGRADE_UNTIL_REVIEW",
            "NONE",
            "Red result despite low event pressure; review for variance before penalizing model.",
        )
    if pressure == "HIGH_PRESSURE":
        return (
            "RED_BAD_READ_CANDIDATE",
            "25",
            "BAD_READ_OR_BAD_MARKET",
            "DOWNGRADE_PATTERN_AFTER_CAUSAL_REVIEW",
            "-SMALL_AFTER_SAMPLE",
            "Red result with high underlying pressure; likely structural error unless explained by market family.",
        )
    return (
        "RED_STANDARD_CAUSAL_REVIEW",
        "40",
        "PENDING_CAUSAL_CLASSIFICATION",
        "REVIEW_BEFORE_MODEL_CHANGE",
        "NONE",
        "Red result needs causal review before assigning market/read/variance blame.",
    )


def classify_no_bet(row: dict[str, str]) -> tuple[str, str, str, str, str, str, str]:
    audit_status = up(row.get("audit_status"))
    if audit_status == "NO_BET_AUDIT_READY":
        return (
            "NO_BET_CAUSAL_REVIEW_REQUIRED",
            "",
            "NO_BET_REVIEW",
            "REVIEW_NO_BET_CORRECTNESS",
            "NONE",
            "PENDING_NO_BET_CORRECTNESS_REVIEW",
            "Real fixture no-bet has final actuals; classify as correct protection or too conservative.",
        )
    return (
        "NO_BET_PENDING_OR_DIAGNOSTIC",
        "",
        "NONE",
        "NO_MODEL_CHANGE",
        "NONE",
        "NOT_APPLICABLE_OR_PENDING",
        "No Bet is not ready for correctness classification in v1.",
    )


def classify(row: dict[str, str]) -> dict[str, str]:
    outcome = up(row.get("pick_outcome"))
    audit_status = up(row.get("audit_status"))
    decision_bucket = up(row.get("decision_bucket"))

    if "DIAGNOSTIC" in audit_status or "DIAGNOSTIC" in decision_bucket:
        qclass, qscore, err, action, adj, nb, manual, note = (
            "DIAGNOSTIC_NO_LEARNING",
            "",
            "NONE",
            "NO_MODEL_CHANGE",
            "NONE",
            "DIAGNOSTIC_NOT_A_REAL_NO_BET",
            "NO",
            "Diagnostic row; not a fixture-level pick/no-bet and must not train the model.",
        )
    elif audit_status.startswith("PENDING") or outcome == "PENDING":
        qclass, qscore, err, action, adj, nb, manual, note = (
            "PENDING_FINAL_ACTUALS",
            "",
            "PENDING",
            "WAIT_FOR_POSTMATCH_DATA",
            "NONE",
            "PENDING",
            "NO",
            "Waiting for final actuals before classifying quality.",
        )
    elif decision_bucket == "NO_BET" or audit_status == "NO_BET_AUDIT_READY":
        qclass, qscore, err, action, adj, nb, note = classify_no_bet(row)
        manual = "YES"
    elif outcome == "GREEN":
        qclass, qscore, err, action, adj, note = classify_green(row)
        nb = "NOT_APPLICABLE"
        manual = "YES"
    elif outcome == "RED":
        qclass, qscore, err, action, adj, note = classify_red(row)
        nb = "NOT_APPLICABLE"
        manual = "YES"
    elif outcome == "VOID":
        qclass, qscore, err, action, adj, nb, manual, note = (
            "VOID_NO_REINFORCEMENT",
            "50",
            "NONE",
            "NO_MODEL_CHANGE",
            "NONE",
            "NOT_APPLICABLE",
            "NO",
            "Void/push result; keep record but do not reinforce or downgrade.",
        )
    else:
        qclass, qscore, err, action, adj, nb, manual, note = (
            "MANUAL_CLASSIFICATION_REQUIRED",
            "",
            "UNKNOWN_MARKET_OR_OUTCOME",
            "MANUAL_REVIEW_REQUIRED",
            "NONE",
            "NOT_APPLICABLE",
            "YES",
            "Outcome/market was not safely classifiable by v1.",
        )

    return {
        "quality_class": qclass,
        "quality_score": qscore,
        "error_family": err,
        "learning_action": action,
        "confidence_adjustment": adj,
        "no_bet_quality_label": nb,
        "manual_review_required": manual,
        "classification_note": note,
    }


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    audit_rows = load_audit_rows(processed, day)
    if not audit_rows:
        audit_rows = [{
            "target_date": day,
            "ledger_key": f"{day}|NO_POSTMATCH_AUDIT",
            "fixture_id": "DIAGNOSTIC_NO_POSTMATCH_AUDIT",
            "home_team": "NO_POSTMATCH_AUDIT",
            "away_team": "NO_POSTMATCH_AUDIT",
            "primary_market": "NO_MARKET",
            "final_decision": "NO_BET",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "audit_status": "AUDIT_NOT_AVAILABLE",
            "pick_outcome": "NO_PICK",
            "market_grade_status": "NO_MARKET_GRADING",
            "result_source_status": "NO_AUDIT_FILE_FOUND",
        }]

    out: list[dict[str, object]] = []
    for row in audit_rows:
        cls = classify(row)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "ledger_key": norm(row.get("ledger_key")),
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "primary_market": norm(row.get("primary_market"), "NO_MARKET"),
            "final_decision": norm(row.get("final_decision")),
            "decision_bucket": norm(row.get("decision_bucket")),
            "audit_status": norm(row.get("audit_status")),
            "pick_outcome": norm(row.get("pick_outcome")),
            "market_grade_status": norm(row.get("market_grade_status")),
            "result_source_status": norm(row.get("result_source_status")),
            "actual_total_goals": norm(row.get("actual_total_goals")),
            "actual_total_xg": norm(row.get("actual_total_xg")),
            "actual_total_sot": norm(row.get("actual_total_sot")),
            "actual_total_big": norm(row.get("actual_total_big")),
            **cls,
            "source_guard": "PICK_QUALITY_CLASSIFICATION_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def update_historical(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    path = processed / "governance" / "vsigma_pick_quality_classification.csv"
    existing = read_csv(path)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(path, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Pick Quality Classification - {day}",
        "",
        "## Summary",
        f"- classification_rows: {len(rows)}",
        f"- quality_class_counts: {fmt_counts(rows, 'quality_class')}",
        f"- error_family_counts: {fmt_counts(rows, 'error_family')}",
        f"- learning_action_counts: {fmt_counts(rows, 'learning_action')}",
        f"- manual_review_required_counts: {fmt_counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Classification Rows",
    ]
    for row in rows[:80]:
        lines.append(
            "- "
            f"{row.get('quality_class', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"market={row.get('primary_market', '')} | outcome={row.get('pick_outcome', '')} | "
            f"error={row.get('error_family', '')} | action={row.get('learning_action', '')} | "
            f"manual={row.get('manual_review_required', '')} | note={row.get('classification_note', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This classifier labels audit rows; it does not change model weights or picks.",
        "- GREEN/RED labels are candidates until causal review confirms the lesson.",
        "- NO_BET correctness requires real fixture context and manual/causal review.",
        "- Diagnostic rows must not train the model.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_pick_quality_classification_daily.csv", rows, FIELDS)
        (base / "vsigma_pick_quality_classification.md").write_text(markdown(day, rows), encoding="utf-8")
    update_historical(processed, day, rows)

    print("=== VSIGMA PICK QUALITY CLASSIFICATION ===")
    print(f"classification_rows={len(rows)}")
    print(f"quality_class_counts={fmt_counts(rows, 'quality_class')}")
    print(f"learning_action_counts={fmt_counts(rows, 'learning_action')}")
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
