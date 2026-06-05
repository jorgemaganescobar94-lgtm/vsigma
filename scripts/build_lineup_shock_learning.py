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
    "league",
    "country",
    "decision_bucket",
    "pick_outcome",
    "quality_class",
    "market_family",
    "official_lineup_rows",
    "probable_lineup_rows",
    "probable_imported_rows",
    "probable_learning_only_rows",
    "probable_unknown_rows",
    "lineup_data_status",
    "lineup_shock_status",
    "lineup_learning_label",
    "shock_evidence_level",
    "manual_review_required",
    "recommended_action",
    "lineup_note",
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

def load_rows(processed: Path, day: str, names: list[str]) -> list[dict[str, str]]:
    path = first_existing(processed, day, names)
    return read_csv(path) if path else []

def by_key(rows: list[dict[str, str]], field: str) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = norm(row.get(field))
        if key:
            out[key] = row
    return out

def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")

def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["fixture_id", "home_team", "away_team", "decision_bucket", "ledger_status", "quality_class"]
    )
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text

def merge_inputs(processed: Path, day: str) -> list[dict[str, str]]:
    ledger = load_rows(processed, day, ["vsigma_official_pick_ledger.csv", "vsigma_official_pick_ledger_daily.csv"])
    quality_by_key = by_key(
        load_rows(processed, day, ["vsigma_pick_quality_classification.csv", "vsigma_pick_quality_classification_daily.csv"]),
        "ledger_key",
    )
    translation_by_key = by_key(
        load_rows(processed, day, ["vsigma_market_translation_audit.csv", "vsigma_market_translation_audit_daily.csv"]),
        "ledger_key",
    )

    if not ledger:
        ledger = [{
            "target_date": day,
            "ledger_key": f"{day}|DIAGNOSTIC_NO_OFFICIAL_LEDGER",
            "fixture_id": "DIAGNOSTIC_NO_OFFICIAL_LEDGER",
            "home_team": "NO_OFFICIAL_LEDGER",
            "away_team": "NO_OFFICIAL_LEDGER",
            "league": "DIAGNOSTIC_NO_COMPETITION",
            "country": "DIAGNOSTIC",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "final_decision": "NO_BET",
        }]

    merged: list[dict[str, str]] = []
    for base in ledger:
        key = norm(base.get("ledger_key"))
        row = dict(base)
        for source in [quality_by_key.get(key, {}), translation_by_key.get(key, {})]:
            for field, value in source.items():
                if field in {"target_date", "generated_at"}:
                    continue
                if norm(value):
                    row[field] = value
        merged.append(row)
    return merged

def index_by_fixture(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid:
            out.setdefault(fid, []).append(row)
    return out

def probable_status_counts(rows: list[dict[str, str]]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in rows:
        status = up(row.get("probable_status")) or up(row.get("status")) or up(row.get("lineup_status")) or "UNKNOWN"
        counter[status] += 1
    return counter

def classify_lineup_shock(
    row: dict[str, str],
    official_rows: list[dict[str, str]],
    probable_rows: list[dict[str, str]],
) -> tuple[str, str, str, str, str, str]:
    if is_diagnostic(row):
        return (
            "DIAGNOSTIC_NO_LINEUP_LEARNING",
            "DIAGNOSTIC_NOT_REAL_FIXTURE",
            "NONE",
            "NO",
            "NO_MODEL_CHANGE",
            "Diagnostic row; no fixture-level lineup shock can be evaluated.",
        )

    outcome = up(row.get("pick_outcome"))
    quality = up(row.get("quality_class"))
    decision_bucket = up(row.get("decision_bucket"))
    official_count = len(official_rows)
    probable_count = len(probable_rows)
    status_counts = probable_status_counts(probable_rows)

    if official_count == 0 and probable_count == 0:
        return (
            "LINEUP_DATA_MISSING",
            "NO_LINEUP_SIGNAL",
            "LOW",
            "NO",
            "COLLECT_LINEUP_DATA",
            "No official/probable lineup rows found for this fixture.",
        )

    if official_count > 0 and probable_count == 0:
        if outcome == "RED":
            return (
                "OFFICIAL_LINEUP_AVAILABLE_RED_REVIEW",
                "LINEUP_SHOCK_REVIEW_CANDIDATE",
                "MEDIUM",
                "YES",
                "REVIEW_IF_OFFICIAL_LINEUP_CHANGED_THESIS",
                "Official lineup data exists and pick was red; review whether lineup information should have downgraded or cancelled.",
            )
        if decision_bucket == "NO_BET":
            return (
                "OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW",
                "NO_BET_LINEUP_REVIEW",
                "MEDIUM",
                "YES",
                "REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY",
                "Official lineup data exists for a No Bet; review whether lineup protected the system or was too conservative.",
            )
        return (
            "OFFICIAL_LINEUP_AVAILABLE_NEUTRAL",
            "LINEUP_CONTEXT_PRESENT",
            "LOW",
            "NO",
            "KEEP_COLLECTING_SAMPLE",
            "Official lineup data exists, but no shock inference is safe in v1.",
        )

    if probable_count > 0 and official_count == 0:
        if status_counts.get("UNKNOWN", 0) > 0 or status_counts.get("LEARNING_ONLY", 0) > 0:
            return (
                "PROBABLE_LINEUP_UNCONFIRMED",
                "PRELOCK_UNCERTAINTY_REVIEW",
                "MEDIUM",
                "YES" if outcome == "RED" else "NO",
                "KEEP_AS_PRELOCK_OR_LIVE_UNTIL_CONFIRMED",
                "Probable lineup data exists but official confirmation is missing/learning-only.",
            )
        return (
            "PROBABLE_LINEUP_AVAILABLE_NO_OFFICIAL",
            "PRELOCK_LINEUP_CONTEXT_ONLY",
            "LOW",
            "NO",
            "COLLECT_OFFICIAL_CONFIRMATION",
            "Probable lineup data exists but official lineup confirmation is missing.",
        )

    if official_count > 0 and probable_count > 0:
        if outcome == "RED" or "RED" in quality:
            return (
                "LINEUP_CONFIRMED_RED_CAUSAL_REVIEW",
                "LINEUP_SHOCK_OR_BAD_PRELOCK_REVIEW",
                "HIGH",
                "YES",
                "REVIEW_LINEUP_SHOCK_BEFORE_MODEL_CHANGE",
                "Probable and official lineup data exist and result was red; audit whether lineup shock was missed.",
            )
        if outcome == "GREEN":
            return (
                "LINEUP_CONFIRMED_GREEN_REVIEW",
                "LINEUP_SUPPORTED_OR_NEUTRAL",
                "MEDIUM",
                "YES",
                "REVIEW_IF_LINEUP_SIGNAL_VALIDATED_THESIS",
                "Probable and official lineup data exist and result was green; review if lineup confirmed the thesis.",
            )
        return (
            "LINEUP_CONFIRMED_CONTEXT_ONLY",
            "LINEUP_CONTEXT_PRESENT",
            "LOW",
            "NO",
            "KEEP_COLLECTING_SAMPLE",
            "Lineup data exists but outcome does not create a safe shock label.",
        )

    return (
        "LINEUP_REVIEW_UNKNOWN_STATE",
        "UNKNOWN_LINEUP_STATE",
        "LOW",
        "YES",
        "MANUAL_REVIEW_REQUIRED",
        "Could not classify lineup shock state safely in v1.",
    )

def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    base_rows = merge_inputs(processed, day)

    official_rows = load_rows(processed, day, ["official_lineup_sources.csv"])
    probable_rows = load_rows(processed, day, ["vsigma_probable_lineup_accuracy_ledger.csv"])

    official_by_fixture = index_by_fixture(official_rows)
    probable_by_fixture = index_by_fixture(probable_rows)

    out: list[dict[str, object]] = []
    for row in base_rows:
        fid = fixture_id(row)
        official_match = official_by_fixture.get(fid, [])
        probable_match = probable_by_fixture.get(fid, [])
        p_counts = probable_status_counts(probable_match)

        shock_status, label, evidence, manual, action, note = classify_lineup_shock(row, official_match, probable_match)

        out.append({
            "target_date": day,
            "generated_at": generated,
            "ledger_key": norm(row.get("ledger_key")),
            "fixture_id": fid,
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "decision_bucket": norm(row.get("decision_bucket")),
            "pick_outcome": norm(row.get("pick_outcome"), "NO_PICK"),
            "quality_class": norm(row.get("quality_class")),
            "market_family": norm(row.get("market_family"), "UNKNOWN_FAMILY"),
            "official_lineup_rows": len(official_match),
            "probable_lineup_rows": len(probable_match),
            "probable_imported_rows": p_counts.get("IMPORTED", 0),
            "probable_learning_only_rows": p_counts.get("LEARNING_ONLY", 0),
            "probable_unknown_rows": p_counts.get("UNKNOWN", 0),
            "lineup_data_status": "HAS_LINEUP_DATA" if official_match or probable_match else "NO_LINEUP_DATA",
            "lineup_shock_status": shock_status,
            "lineup_learning_label": label,
            "shock_evidence_level": evidence,
            "manual_review_required": manual,
            "recommended_action": action,
            "lineup_note": note,
            "source_guard": "LINEUP_SHOCK_LEARNING_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_lineup_shock_learning_daily.csv", rows, FIELDS)
        (base / "vsigma_lineup_shock_learning.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_lineup_shock_learning.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)

def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Lineup Shock Learning - {day}",
        "",
        "## Summary",
        f"- lineup_rows: {len(rows)}",
        f"- lineup_data_status_counts: {fmt_counts(rows, 'lineup_data_status')}",
        f"- lineup_shock_status_counts: {fmt_counts(rows, 'lineup_shock_status')}",
        f"- lineup_learning_label_counts: {fmt_counts(rows, 'lineup_learning_label')}",
        f"- shock_evidence_level_counts: {fmt_counts(rows, 'shock_evidence_level')}",
        f"- manual_review_required_counts: {fmt_counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Lineup Shock Rows",
    ]

    for row in rows[:120]:
        lines.append(
            "- "
            f"{row.get('lineup_shock_status', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"official={row.get('official_lineup_rows', '')} probable={row.get('probable_lineup_rows', '')} | "
            f"outcome={row.get('pick_outcome', '')} | label={row.get('lineup_learning_label', '')} | "
            f"evidence={row.get('shock_evidence_level', '')} | manual={row.get('manual_review_required', '')} | "
            f"action={row.get('recommended_action', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This lineup shock report is advisory only and never changes prelock, picks, stake, or weights.",
        "- Missing lineup data is not treated as source failure by itself.",
        "- Red/green labels require causal review before any model lesson is accepted.",
        "- No automatic lineup gate, source registry, or production changes are created here.",
    ]
    return "\n".join(lines) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA LINEUP SHOCK LEARNING ===")
    print(f"lineup_rows={len(rows)}")
    print(f"lineup_shock_status_counts={fmt_counts(rows, 'lineup_shock_status')}")
    print(f"lineup_data_status_counts={fmt_counts(rows, 'lineup_data_status')}")
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
