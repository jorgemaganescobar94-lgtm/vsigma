from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

LAYER_FILES = [
    ("official_pick_ledger", "vsigma_official_pick_ledger_daily.csv", "vsigma_official_pick_ledger.csv"),
    ("postmatch_pick_audit", "vsigma_postmatch_pick_audit_daily.csv", "vsigma_postmatch_pick_audit.csv"),
    ("pick_quality_classification", "vsigma_pick_quality_classification_daily.csv", "vsigma_pick_quality_classification.csv"),
    ("market_translation_audit", "vsigma_market_translation_audit_daily.csv", "vsigma_market_translation_audit.csv"),
    ("no_bet_audit", "vsigma_no_bet_audit_daily.csv", "vsigma_no_bet_audit.csv"),
    ("market_family_calibration", "vsigma_market_family_calibration_daily.csv", "vsigma_market_family_calibration.csv"),
    ("confidence_calibration", "vsigma_confidence_calibration_daily.csv", "vsigma_confidence_calibration.csv"),
    ("source_reliability_learning", "vsigma_source_reliability_learning_daily.csv", "vsigma_source_reliability_learning.csv"),
    ("league_competition_learning", "vsigma_league_competition_learning_daily.csv", "vsigma_league_competition_learning.csv"),
    ("lineup_shock_learning", "vsigma_lineup_shock_learning_daily.csv", "vsigma_lineup_shock_learning.csv"),
    ("goal_timing_learning", "vsigma_goal_timing_learning_daily.csv", "vsigma_goal_timing_learning.csv"),
    ("scoreline_neighbor_stress", "vsigma_scoreline_neighbor_stress_daily.csv", "vsigma_scoreline_neighbor_stress.csv"),
    ("portfolio_correlation_learning", "vsigma_portfolio_correlation_learning_daily.csv", "vsigma_portfolio_correlation_learning.csv"),
]

FIELDS = [
    "target_date",
    "generated_at",
    "layer_name",
    "source_file",
    "artifact_status",
    "rows_total",
    "diagnostic_rows",
    "pending_rows",
    "manual_review_rows",
    "sample_blocked_rows",
    "no_real_sample_rows",
    "positive_signal_rows",
    "negative_signal_rows",
    "neutral_signal_rows",
    "no_model_change_rows",
    "learning_candidate_rows",
    "action_counts",
    "status_counts",
    "synthesis_status",
    "synthesis_priority",
    "learning_permission",
    "synthesis_note",
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

def first_existing(processed: Path, day: str, daily_name: str, governance_name: str) -> Path | None:
    candidates = [
        processed / "today" / day / daily_name,
        processed / "governance" / daily_name,
        processed / "governance" / governance_name,
    ]
    for path in candidates:
        if path.exists():
            return path
    return None

def filter_day(rows: list[dict[str, str]], day: str, path: Path) -> list[dict[str, str]]:
    if path.name.endswith("_daily.csv"):
        return rows
    if not rows:
        return rows
    if "target_date" not in rows[0]:
        return rows
    return [row for row in rows if norm(row.get("target_date")) == day]

def row_text(row: dict[str, str]) -> str:
    return " ".join(up(value) for value in row.values())

def is_diagnostic(row: dict[str, str]) -> bool:
    text = row_text(row)
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text

def is_pending(row: dict[str, str]) -> bool:
    text = row_text(row)
    return "PENDING" in text or "WAIT_FOR" in text or "MISSING_FINAL" in text

def needs_manual(row: dict[str, str]) -> bool:
    text = row_text(row)
    return (
        up(row.get("manual_review_required")) == "YES"
        or "MANUAL_REVIEW" in text
        or "CAUSAL_REVIEW" in text
        or "REVIEW_REQUIRED" in text
    )

def is_sample_blocked(row: dict[str, str]) -> bool:
    text = row_text(row)
    return (
        "INSUFFICIENT_SAMPLE" in text
        or "HOLD_SAMPLE" in text
        or "OBSERVE_ONLY_SAMPLE" in text
        or "NO_REAL_SAMPLE" in text
    )

def no_real_sample(row: dict[str, str]) -> bool:
    text = row_text(row)
    return "NO_REAL_SAMPLE" in text or "NO_REAL_RESULT_SAMPLE" in text or "DIAGNOSTIC_ONLY_NO_REAL_SAMPLE" in text

def positive_signal(row: dict[str, str]) -> bool:
    text = row_text(row)
    return (
        "POSITIVE" in text
        or "GREEN_CLEAN" in text
        or "UPGRADE_CANDIDATE" in text
        or "UP_CALIBRATE" in text
        or "MARKET_FAMILY_WORKED_CLEANLY" in text
    )

def negative_signal(row: dict[str, str]) -> bool:
    text = row_text(row)
    return (
        "NEGATIVE" in text
        or "RED_BAD" in text
        or "DOWNGRADE_CANDIDATE" in text
        or "DOWN_CALIBRATE" in text
        or "FAILURE" in text
        or "OVERCONFIDENCE" in text
        or "CORRELATED_FAILURE" in text
    )

def neutral_signal(row: dict[str, str]) -> bool:
    text = row_text(row)
    return "NEUTRAL" in text or "KEEP_CURRENT" in text or "NO_WEIGHT_CHANGE" in text

def no_model_change(row: dict[str, str]) -> bool:
    text = row_text(row)
    return "NO_MODEL_CHANGE" in text or "NO_WEIGHT_CHANGE" in text or "NO_AUTOMATIC" in text

def learning_candidate(row: dict[str, str]) -> bool:
    text = row_text(row)
    return (
        "CANDIDATE" in text
        or "REVIEW" in text
        or "MANUAL" in text
    ) and not is_diagnostic(row)

def count_field_values(rows: list[dict[str, str]], possible_fields: list[str]) -> str:
    counter: Counter[str] = Counter()
    for row in rows:
        for field in possible_fields:
            value = norm(row.get(field))
            if value:
                counter[value] += 1
                break
    if not counter:
        return "none"
    return "; ".join(f"{key}={value}" for key, value in counter.most_common())

def classify_layer(
    rows_total: int,
    diagnostic_rows: int,
    pending_rows: int,
    manual_review_rows: int,
    sample_blocked_rows: int,
    no_real_sample_rows: int,
    positive_rows: int,
    negative_rows: int,
    candidate_rows: int,
) -> tuple[str, str, str, str]:
    if rows_total == 0:
        return (
            "MISSING_ARTIFACT",
            "HIGH",
            "NO_LEARNING",
            "Artifact missing or empty; cannot synthesize this layer.",
        )

    if diagnostic_rows == rows_total:
        return (
            "DIAGNOSTIC_ONLY",
            "NONE",
            "NO_LEARNING_DIAGNOSTIC_ONLY",
            "All rows are diagnostic; no learning is permitted.",
        )

    if pending_rows > 0 and pending_rows == rows_total:
        return (
            "PENDING_ONLY",
            "LOW",
            "WAIT_FOR_FINAL_DATA",
            "All rows are pending; wait for final data.",
        )

    if manual_review_rows > 0:
        return (
            "MANUAL_REVIEW_REQUIRED",
            "HIGH",
            "MANUAL_REVIEW_ONLY",
            "Layer contains review candidates; no automatic learning allowed.",
        )

    if negative_rows > 0:
        return (
            "NEGATIVE_SIGNAL_REVIEW",
            "HIGH",
            "MANUAL_REVIEW_ONLY",
            "Layer contains negative/failure signal; requires causal review.",
        )

    if positive_rows > 0:
        return (
            "POSITIVE_SIGNAL_REVIEW",
            "MEDIUM",
            "MANUAL_REVIEW_ONLY",
            "Layer contains positive signal; requires sample and causal review before reinforcement.",
        )

    if sample_blocked_rows > 0 or no_real_sample_rows > 0:
        return (
            "HOLD_SAMPLE",
            "LOW",
            "NO_LEARNING_SAMPLE_BLOCKED",
            "Layer is blocked by insufficient/no real sample.",
        )

    if candidate_rows > 0:
        return (
            "LEARNING_CANDIDATE_REVIEW",
            "MEDIUM",
            "MANUAL_REVIEW_ONLY",
            "Layer has learning candidates but needs manual confirmation.",
        )

    return (
        "NO_MODEL_CHANGE",
        "NONE",
        "NO_MODEL_CHANGE",
        "No actionable learning signal detected.",
    )

def build_layer_row(day: str, generated: str, layer_name: str, path: Path | None, rows: list[dict[str, str]]) -> dict[str, object]:
    rows_total = len(rows)
    diagnostic_rows = sum(1 for row in rows if is_diagnostic(row))
    pending_rows = sum(1 for row in rows if is_pending(row))
    manual_review_rows = sum(1 for row in rows if needs_manual(row))
    sample_blocked_rows = sum(1 for row in rows if is_sample_blocked(row))
    no_real_sample_rows = sum(1 for row in rows if no_real_sample(row))
    positive_rows = sum(1 for row in rows if positive_signal(row))
    negative_rows = sum(1 for row in rows if negative_signal(row))
    neutral_rows = sum(1 for row in rows if neutral_signal(row))
    no_model_change_rows = sum(1 for row in rows if no_model_change(row))
    candidate_rows = sum(1 for row in rows if learning_candidate(row))

    synthesis_status, priority, permission, note = classify_layer(
        rows_total,
        diagnostic_rows,
        pending_rows,
        manual_review_rows,
        sample_blocked_rows,
        no_real_sample_rows,
        positive_rows,
        negative_rows,
        candidate_rows,
    )

    return {
        "target_date": day,
        "generated_at": generated,
        "layer_name": layer_name,
        "source_file": path.as_posix() if path else "MISSING",
        "artifact_status": "FOUND" if path else "MISSING",
        "rows_total": rows_total,
        "diagnostic_rows": diagnostic_rows,
        "pending_rows": pending_rows,
        "manual_review_rows": manual_review_rows,
        "sample_blocked_rows": sample_blocked_rows,
        "no_real_sample_rows": no_real_sample_rows,
        "positive_signal_rows": positive_rows,
        "negative_signal_rows": negative_rows,
        "neutral_signal_rows": neutral_rows,
        "no_model_change_rows": no_model_change_rows,
        "learning_candidate_rows": candidate_rows,
        "action_counts": count_field_values(rows, ["recommended_action", "learning_action", "recommended_weight_action", "recommended_registry_action"]),
        "status_counts": count_field_values(rows, [
            "synthesis_status",
            "ledger_status",
            "audit_status",
            "quality_class",
            "translation_audit_status",
            "no_bet_audit_status",
            "calibration_status",
            "source_learning_status",
            "competition_learning_status",
            "lineup_shock_status",
            "goal_timing_profile",
            "scoreline_stress_status",
            "portfolio_correlation_status",
        ]),
        "synthesis_status": synthesis_status,
        "synthesis_priority": priority,
        "learning_permission": permission,
        "synthesis_note": note,
        "source_guard": "FINAL_LEARNING_SYNTHESIS_V1_NO_AUTO_APPLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }

def overall_row(day: str, generated: str, layer_rows: list[dict[str, object]]) -> dict[str, object]:
    total_layers = len(layer_rows)
    total_rows = sum(int(row.get("rows_total") or 0) for row in layer_rows)
    manual_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "MANUAL_REVIEW_REQUIRED")
    diagnostic_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "DIAGNOSTIC_ONLY")
    hold_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "HOLD_SAMPLE")
    missing_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "MISSING_ARTIFACT")
    negative_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "NEGATIVE_SIGNAL_REVIEW")
    positive_layers = sum(1 for row in layer_rows if row.get("synthesis_status") == "POSITIVE_SIGNAL_REVIEW")

    if missing_layers > 0:
        status = "SYNTHESIS_INCOMPLETE_MISSING_ARTIFACTS"
        priority = "HIGH"
        permission = "NO_LEARNING_MISSING_ARTIFACTS"
        note = "One or more learning artifacts are missing; fix workflow/output coverage before learning."
    elif manual_layers > 0 or negative_layers > 0 or positive_layers > 0:
        status = "SYNTHESIS_REVIEW_REQUIRED"
        priority = "HIGH"
        permission = "MANUAL_REVIEW_ONLY"
        note = "At least one layer has reviewable learning signal; no automatic update is allowed."
    elif diagnostic_layers == total_layers:
        status = "SYNTHESIS_DIAGNOSTIC_ONLY"
        priority = "NONE"
        permission = "NO_LEARNING_DIAGNOSTIC_ONLY"
        note = "All layers are diagnostic; no learning is permitted."
    elif hold_layers > 0:
        status = "SYNTHESIS_HOLD_SAMPLE"
        priority = "LOW"
        permission = "NO_LEARNING_SAMPLE_BLOCKED"
        note = "No reviewable signal; one or more layers are blocked by sample."
    else:
        status = "SYNTHESIS_NO_MODEL_CHANGE"
        priority = "NONE"
        permission = "NO_MODEL_CHANGE"
        note = "No actionable learning signal detected."

    return {
        "target_date": day,
        "generated_at": generated,
        "layer_name": "OVERALL_SYNTHESIS",
        "source_file": "ALL_LAYERS",
        "artifact_status": "AGGREGATED",
        "rows_total": total_rows,
        "diagnostic_rows": diagnostic_layers,
        "pending_rows": 0,
        "manual_review_rows": manual_layers,
        "sample_blocked_rows": hold_layers,
        "no_real_sample_rows": 0,
        "positive_signal_rows": positive_layers,
        "negative_signal_rows": negative_layers,
        "neutral_signal_rows": 0,
        "no_model_change_rows": sum(1 for row in layer_rows if row.get("synthesis_status") == "NO_MODEL_CHANGE"),
        "learning_candidate_rows": manual_layers + positive_layers + negative_layers,
        "action_counts": "none",
        "status_counts": "; ".join(f"{key}={value}" for key, value in Counter(str(row.get("synthesis_status")) for row in layer_rows).most_common()),
        "synthesis_status": status,
        "synthesis_priority": priority,
        "learning_permission": permission,
        "synthesis_note": note,
        "source_guard": "FINAL_LEARNING_SYNTHESIS_V1_NO_AUTO_APPLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }

def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    layer_rows: list[dict[str, object]] = []

    for layer_name, daily_name, governance_name in LAYER_FILES:
        path = first_existing(processed, day, daily_name, governance_name)
        raw_rows = filter_day(read_csv(path), day, path) if path else []
        layer_rows.append(build_layer_row(day, generated, layer_name, path, raw_rows))

    return [overall_row(day, generated, layer_rows)] + layer_rows

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_final_learning_synthesis_daily.csv", rows, FIELDS)
        (base / "vsigma_final_learning_synthesis.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_final_learning_synthesis.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)

def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]]) -> str:
    overall = rows[0] if rows else {}
    lines = [
        f"# vSIGMA Final Learning Synthesis - {day}",
        "",
        "## Overall",
        f"- synthesis_status: {overall.get('synthesis_status', 'UNKNOWN')}",
        f"- synthesis_priority: {overall.get('synthesis_priority', 'UNKNOWN')}",
        f"- learning_permission: {overall.get('learning_permission', 'UNKNOWN')}",
        f"- synthesis_note: {overall.get('synthesis_note', '')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Summary",
        f"- layer_rows: {max(len(rows) - 1, 0)}",
        f"- synthesis_status_counts: {fmt_counts(rows[1:], 'synthesis_status')}",
        f"- synthesis_priority_counts: {fmt_counts(rows[1:], 'synthesis_priority')}",
        f"- learning_permission_counts: {fmt_counts(rows[1:], 'learning_permission')}",
        "",
        "## Layer Rows",
    ]

    for row in rows[1:]:
        lines.append(
            "- "
            f"{row.get('layer_name', '')} | rows={row.get('rows_total', '')} | "
            f"diag={row.get('diagnostic_rows', '')} manual={row.get('manual_review_rows', '')} "
            f"sample_blocked={row.get('sample_blocked_rows', '')} pos={row.get('positive_signal_rows', '')} "
            f"neg={row.get('negative_signal_rows', '')} | status={row.get('synthesis_status', '')} | "
            f"permission={row.get('learning_permission', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This synthesis is advisory only and never changes model weights, gates, picks, stake, registry, or production.",
        "- Diagnostic-only days are valid and must not train the model.",
        "- Positive/negative/candidate signals require causal review before any future manual patch.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    overall = rows[0]
    print("=== VSIGMA FINAL LEARNING SYNTHESIS ===")
    print(f"synthesis_status={overall.get('synthesis_status')}")
    print(f"learning_permission={overall.get('learning_permission')}")
    print(f"layer_rows={len(rows) - 1}")
    print(f"synthesis_status_counts={fmt_counts(rows[1:], 'synthesis_status')}")
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
