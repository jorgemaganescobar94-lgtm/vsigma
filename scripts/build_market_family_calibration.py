from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "market_family",
    "sample_rows_total",
    "sample_rows_real",
    "diagnostic_rows",
    "pending_rows",
    "green_rows",
    "red_rows",
    "void_rows",
    "no_pick_rows",
    "manual_review_rows",
    "clean_green_rows",
    "fragile_green_rows",
    "bad_read_or_bad_market_rows",
    "variance_candidate_rows",
    "translation_failure_rows",
    "no_bet_review_rows",
    "odds_escalation_allowed_rows",
    "odds_escalation_blocked_rows",
    "green_rate_real_sample",
    "red_rate_real_sample",
    "sample_gate",
    "calibration_status",
    "confidence_signal",
    "recommended_action",
    "source_window",
    "source_guard",
    "auto_apply",
    "production_change",
]

MIN_OBSERVE_SAMPLE = 10
MIN_SOFT_SIGNAL_SAMPLE = 30
MIN_STRONG_SIGNAL_SAMPLE = 75


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
        candidates.append(processed / "governance" / name)
        candidates.append(processed / "today" / day / name)
    for path in candidates:
        if path.exists():
            return path
    return None


def load_translation_rows(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_market_translation_audit.csv", "vsigma_market_translation_audit_daily.csv"])
    if not path:
        return []
    return read_csv(path)


def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in [
            "decision_bucket",
            "translation_audit_status",
            "translation_quality_label",
            "translation_error_family",
            "fixture_id",
        ]
    )
    return "DIAGNOSTIC" in text


def is_pending(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["translation_audit_status", "translation_quality_label", "pick_outcome"]
    )
    return "PENDING" in text


def is_real_pick_sample(row: dict[str, str]) -> bool:
    if is_diagnostic(row) or is_pending(row):
        return False
    outcome = up(row.get("pick_outcome"))
    return outcome in {"GREEN", "RED", "VOID"}


def pct(num: int, den: int) -> str:
    if den <= 0:
        return ""
    return f"{(num / den) * 100:.1f}%"


def sample_gate(real_sample: int) -> str:
    if real_sample >= MIN_STRONG_SIGNAL_SAMPLE:
        return "STRONG_SAMPLE"
    if real_sample >= MIN_SOFT_SIGNAL_SAMPLE:
        return "SOFT_SIGNAL_SAMPLE"
    if real_sample >= MIN_OBSERVE_SAMPLE:
        return "OBSERVE_ONLY_SAMPLE"
    return "INSUFFICIENT_SAMPLE"


def calibration_status(real_sample: int, green: int, red: int, fragile: int, failures: int) -> tuple[str, str, str]:
    gate = sample_gate(real_sample)
    if gate == "INSUFFICIENT_SAMPLE":
        return (
            "HOLD_SAMPLE",
            "NO_WEIGHT_CHANGE",
            "Collect more market-family samples before changing confidence.",
        )

    green_rate = green / real_sample if real_sample else 0.0
    red_rate = red / real_sample if real_sample else 0.0
    fragility_rate = fragile / real_sample if real_sample else 0.0
    failure_rate = failures / real_sample if real_sample else 0.0

    if gate == "OBSERVE_ONLY_SAMPLE":
        return (
            "OBSERVE_ONLY",
            "NO_WEIGHT_CHANGE",
            "Sample is observable but still too small for calibration movement.",
        )

    if green_rate >= 0.68 and fragility_rate <= 0.15 and failure_rate <= 0.20:
        return (
            "POSITIVE_CALIBRATION_CANDIDATE",
            "UPGRADE_CANDIDATE_REQUIRES_REVIEW",
            "Family is performing well in sample; require causal review before any upgrade.",
        )
    if red_rate >= 0.42 or failure_rate >= 0.30:
        return (
            "NEGATIVE_CALIBRATION_CANDIDATE",
            "DOWNGRADE_CANDIDATE_REQUIRES_REVIEW",
            "Family shows elevated red/failure rate; require causal review before downgrade.",
        )
    return (
        "NEUTRAL_CALIBRATION",
        "KEEP_CURRENT_WEIGHT",
        "No strong family-level signal; keep collecting samples.",
    )


def build_family_rows(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = load_translation_rows(processed, day)
    if not rows:
        rows = [{
            "target_date": day,
            "market_family": "NO_MARKET",
            "fixture_id": "DIAGNOSTIC_NO_MARKET_TRANSLATION_AUDIT",
            "translation_audit_status": "TRANSLATION_NOT_AVAILABLE",
            "translation_quality_label": "DIAGNOSTIC_NO_MARKET_LEARNING",
            "pick_outcome": "NO_PICK",
            "suggested_odds_escalation_status": "NOT_APPLICABLE",
        }]

    by_family: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        family = norm(row.get("market_family"), "UNKNOWN_FAMILY")
        by_family[family].append(row)

    out: list[dict[str, object]] = []
    for family, fam_rows in sorted(by_family.items()):
        total = len(fam_rows)
        diagnostic = sum(1 for row in fam_rows if is_diagnostic(row))
        pending = sum(1 for row in fam_rows if is_pending(row))
        real_rows = [row for row in fam_rows if is_real_pick_sample(row)]
        real = len(real_rows)
        outcomes = Counter(up(row.get("pick_outcome")) or "UNKNOWN" for row in fam_rows)
        qlabels = Counter(up(row.get("translation_quality_label")) or "UNKNOWN" for row in fam_rows)
        terrors = Counter(up(row.get("translation_error_family")) or "UNKNOWN" for row in fam_rows)
        odds = Counter(up(row.get("suggested_odds_escalation_status")) or "UNKNOWN" for row in fam_rows)
        manual = Counter(up(row.get("manual_review_required")) or "UNKNOWN" for row in fam_rows)

        green = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "GREEN")
        red = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "RED")
        void = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "VOID")
        fragile = sum(1 for row in fam_rows if "FRAGILE" in up(row.get("translation_quality_label")))
        bad_read_market = sum(
            1
            for row in fam_rows
            if "BAD_MARKET" in up(row.get("translation_error_family"))
            or "BAD_READ" in up(row.get("translation_error_family"))
        )
        variance = sum(1 for row in fam_rows if "VARIANCE" in up(row.get("translation_error_family")))
        translation_failure = sum(1 for row in fam_rows if "FAILURE" in up(row.get("translation_audit_status")))
        no_bet_review = sum(1 for row in fam_rows if "NO_BET" in up(row.get("translation_audit_status")))
        odds_allowed = sum(1 for row in fam_rows if "ALLOWED" in up(row.get("suggested_odds_escalation_status")))
        odds_blocked = sum(
            1
            for row in fam_rows
            if any(token in up(row.get("suggested_odds_escalation_status")) for token in ["DO_NOT", "NO_ESCALATION", "BLOCK"])
        )
        status, signal, action = calibration_status(real, green, red, fragile, translation_failure + bad_read_market)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "market_family": family,
            "sample_rows_total": total,
            "sample_rows_real": real,
            "diagnostic_rows": diagnostic,
            "pending_rows": pending,
            "green_rows": green,
            "red_rows": red,
            "void_rows": void,
            "no_pick_rows": outcomes.get("NO_PICK", 0),
            "manual_review_rows": manual.get("YES", 0),
            "clean_green_rows": qlabels.get("MARKET_FAMILY_WORKED_CLEANLY", 0),
            "fragile_green_rows": fragile,
            "bad_read_or_bad_market_rows": bad_read_market,
            "variance_candidate_rows": variance,
            "translation_failure_rows": translation_failure,
            "no_bet_review_rows": no_bet_review,
            "odds_escalation_allowed_rows": odds_allowed,
            "odds_escalation_blocked_rows": odds_blocked,
            "green_rate_real_sample": pct(green, real),
            "red_rate_real_sample": pct(red, real),
            "sample_gate": sample_gate(real),
            "calibration_status": status,
            "confidence_signal": signal,
            "recommended_action": action,
            "source_window": "GOVERNANCE_CUMULATIVE_WITH_DAILY_FALLBACK",
            "source_guard": "MARKET_FAMILY_CALIBRATION_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_market_family_calibration_daily.csv", rows, FIELDS)
        (base / "vsigma_market_family_calibration.md").write_text(markdown(day, rows), encoding="utf-8")
    # Historical snapshot uses one row per date+family; replace current day rows.
    hist = processed / "governance" / "vsigma_market_family_calibration.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Market Family Calibration - {day}",
        "",
        "## Summary",
        f"- family_rows: {len(rows)}",
        f"- sample_gate_counts: {fmt_counts(rows, 'sample_gate')}",
        f"- calibration_status_counts: {fmt_counts(rows, 'calibration_status')}",
        f"- confidence_signal_counts: {fmt_counts(rows, 'confidence_signal')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Family Rows",
    ]
    for row in rows[:100]:
        lines.append(
            "- "
            f"{row.get('market_family', '')} | real={row.get('sample_rows_real', '')}/{row.get('sample_rows_total', '')} | "
            f"green={row.get('green_rows', '')} red={row.get('red_rows', '')} void={row.get('void_rows', '')} | "
            f"gate={row.get('sample_gate', '')} | status={row.get('calibration_status', '')} | "
            f"signal={row.get('confidence_signal', '')} | action={row.get('recommended_action', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This calibration is family-level and advisory only; it does not change model weights.",
        "- Sample gates block upgrades/downgrades until enough real audited rows exist.",
        "- Diagnostic, pending and no-pick rows do not count as real market-family hit-rate sample.",
        "- Any upgrade/downgrade candidate requires causal review before a future manual patch.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build_family_rows(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA MARKET FAMILY CALIBRATION ===")
    print(f"family_rows={len(rows)}")
    print(f"sample_gate_counts={fmt_counts(rows, 'sample_gate')}")
    print(f"calibration_status_counts={fmt_counts(rows, 'calibration_status')}")
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
