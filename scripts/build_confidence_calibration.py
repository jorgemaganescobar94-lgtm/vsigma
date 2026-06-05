from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

FIELDS = [
    "target_date",
    "generated_at",
    "confidence_bucket",
    "expected_confidence_midpoint",
    "sample_rows_total",
    "sample_rows_real",
    "diagnostic_rows",
    "pending_rows",
    "no_confidence_rows",
    "green_rows",
    "red_rows",
    "void_rows",
    "no_pick_rows",
    "manual_review_rows",
    "observed_green_rate",
    "calibration_gap_pct_points",
    "sample_gate",
    "calibration_status",
    "confidence_bias_signal",
    "recommended_action",
    "source_window",
    "source_guard",
    "auto_apply",
    "production_change",
]

MIN_OBSERVE_SAMPLE = 10
MIN_SOFT_SIGNAL_SAMPLE = 30
MIN_STRONG_SIGNAL_SAMPLE = 75

BUCKETS = [
    (0, 49, "CONF_00_49", 25.0),
    (50, 59, "CONF_50_59", 55.0),
    (60, 64, "CONF_60_64", 62.0),
    (65, 69, "CONF_65_69", 67.0),
    (70, 74, "CONF_70_74", 72.0),
    (75, 79, "CONF_75_79", 77.0),
    (80, 84, "CONF_80_84", 82.0),
    (85, 89, "CONF_85_89", 87.0),
    (90, 100, "CONF_90_100", 95.0),
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
        candidates.append(processed / "governance" / name)
        candidates.append(processed / "today" / day / name)
    for path in candidates:
        if path.exists():
            return path
    return None


def load_rows(processed: Path, day: str, names: list[str]) -> list[dict[str, str]]:
    path = first_existing(processed, day, names)
    if not path:
        return []
    rows = read_csv(path)
    # Cumulative governance files may contain multiple days; daily files may not.
    if path.name.endswith(".csv") and not path.name.endswith("_daily.csv"):
        rows = [row for row in rows if norm(row.get("target_date")) == day or not norm(row.get("target_date"))]
    return rows


def parse_confidence(value: object) -> float | None:
    text = norm(value)
    if not text:
        return None
    upper = text.upper()
    # Map coarse labels only when no numeric confidence is present.
    coarse = {
        "VERY_HIGH": 85.0,
        "HIGH": 75.0,
        "MEDIUM_HIGH": 68.0,
        "MEDIUM": 62.0,
        "LOW_MEDIUM": 55.0,
        "LOW": 45.0,
    }
    if upper in coarse:
        return coarse[upper]
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", "."))
    if not match:
        return None
    val = float(match.group(0))
    if 0 <= val <= 1:
        val *= 100.0
    if val < 0 or val > 100:
        return None
    return val


def confidence_bucket(value: object) -> tuple[str, str, float | None]:
    conf = parse_confidence(value)
    if conf is None:
        return "NO_CONFIDENCE", "", None
    for low, high, label, midpoint in BUCKETS:
        if low <= conf <= high:
            return label, f"{midpoint:.1f}%", midpoint
    return "NO_CONFIDENCE", "", None


def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["ledger_status", "decision_bucket", "quality_class", "fixture_id", "home_team", "away_team"]
    )
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text


def is_pending(row: dict[str, str]) -> bool:
    text = " ".join(up(row.get(name)) for name in ["pick_outcome", "quality_class", "learning_action"])
    return "PENDING" in text or "WAIT_FOR" in text


def join_quality_by_key(quality_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in quality_rows:
        key = norm(row.get("ledger_key"))
        if key:
            out[key] = row
    return out


def merge_ledger_quality(ledger_rows: list[dict[str, str]], quality_rows: list[dict[str, str]], day: str) -> list[dict[str, str]]:
    quality_by_key = join_quality_by_key(quality_rows)
    if not ledger_rows and quality_rows:
        return quality_rows
    merged: list[dict[str, str]] = []
    for ledger in ledger_rows:
        key = norm(ledger.get("ledger_key"))
        quality = quality_by_key.get(key, {})
        row = dict(ledger)
        for name, value in quality.items():
            if name not in row or not norm(row.get(name)):
                row[name] = value
        # Preserve outcome/quality fields from quality when present.
        for name in ["pick_outcome", "quality_class", "manual_review_required", "learning_action"]:
            if norm(quality.get(name)):
                row[name] = quality[name]
        merged.append(row)
    return merged


def sample_gate(real_sample: int) -> str:
    if real_sample >= MIN_STRONG_SIGNAL_SAMPLE:
        return "STRONG_SAMPLE"
    if real_sample >= MIN_SOFT_SIGNAL_SAMPLE:
        return "SOFT_SIGNAL_SAMPLE"
    if real_sample >= MIN_OBSERVE_SAMPLE:
        return "OBSERVE_ONLY_SAMPLE"
    return "INSUFFICIENT_SAMPLE"


def pct(num: int, den: int) -> str:
    if den <= 0:
        return ""
    return f"{(num / den) * 100:.1f}%"


def calibration_for(bucket_midpoint: float | None, real_sample: int, green: int) -> tuple[str, str, str, str]:
    gate = sample_gate(real_sample)
    if real_sample <= 0 or bucket_midpoint is None:
        return (
            gate,
            "HOLD_SAMPLE",
            "NO_CONFIDENCE_SIGNAL",
            "No real green/red sample or no numeric confidence; collect data only.",
        )
    observed = (green / real_sample) * 100.0
    gap = observed - bucket_midpoint

    if gate == "INSUFFICIENT_SAMPLE":
        return (
            gate,
            "HOLD_SAMPLE",
            "NO_WEIGHT_CHANGE",
            "Sample too small for confidence calibration movement.",
        )
    if gate == "OBSERVE_ONLY_SAMPLE":
        return (
            gate,
            "OBSERVE_ONLY",
            "NO_WEIGHT_CHANGE",
            "Observable sample, but not enough for weight movement.",
        )
    if gap <= -12.0:
        return (
            gate,
            "OVERCONFIDENCE_CANDIDATE",
            "DOWN_CALIBRATE_CONFIDENCE_REQUIRES_REVIEW",
            "Observed hit rate is materially below expected confidence; review before any downgrade.",
        )
    if gap >= 12.0:
        return (
            gate,
            "UNDERCONFIDENCE_CANDIDATE",
            "UP_CALIBRATE_CONFIDENCE_REQUIRES_REVIEW",
            "Observed hit rate is materially above expected confidence; review before any upgrade.",
        )
    return (
        gate,
        "CALIBRATED_OR_NEUTRAL",
        "KEEP_CURRENT_CONFIDENCE",
        "Observed hit rate is close enough to expected confidence for current sample.",
    )


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    ledger_rows = load_rows(processed, day, ["vsigma_official_pick_ledger.csv", "vsigma_official_pick_ledger_daily.csv"])
    quality_rows = load_rows(processed, day, ["vsigma_pick_quality_classification.csv", "vsigma_pick_quality_classification_daily.csv"])
    rows = merge_ledger_quality(ledger_rows, quality_rows, day)
    if not rows:
        rows = [{
            "target_date": day,
            "ledger_key": f"{day}|NO_CONFIDENCE_INPUTS",
            "fixture_id": "DIAGNOSTIC_NO_CONFIDENCE_INPUTS",
            "home_team": "NO_CONFIDENCE_INPUTS",
            "away_team": "NO_CONFIDENCE_INPUTS",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "forecast_confidence": "",
            "pick_outcome": "NO_PICK",
            "quality_class": "DIAGNOSTIC_NO_LEARNING",
        }]

    by_bucket: dict[str, list[dict[str, str]]] = defaultdict(list)
    bucket_midpoints: dict[str, float | None] = {}
    bucket_midpoint_text: dict[str, str] = {}
    for row in rows:
        bucket, midpoint_text, midpoint = confidence_bucket(row.get("forecast_confidence"))
        by_bucket[bucket].append(row)
        bucket_midpoints[bucket] = midpoint
        bucket_midpoint_text[bucket] = midpoint_text

    out: list[dict[str, object]] = []
    for bucket, bucket_rows in sorted(by_bucket.items()):
        total = len(bucket_rows)
        diagnostic = sum(1 for row in bucket_rows if is_diagnostic(row))
        pending = sum(1 for row in bucket_rows if is_pending(row))
        no_conf = sum(1 for row in bucket_rows if confidence_bucket(row.get("forecast_confidence"))[0] == "NO_CONFIDENCE")
        outcomes = Counter(up(row.get("pick_outcome")) or "UNKNOWN" for row in bucket_rows)
        manual = Counter(up(row.get("manual_review_required")) or "UNKNOWN" for row in bucket_rows)

        real_rows = [
            row for row in bucket_rows
            if not is_diagnostic(row) and not is_pending(row) and up(row.get("pick_outcome")) in {"GREEN", "RED", "VOID"}
        ]
        real = len(real_rows)
        green = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "GREEN")
        red = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "RED")
        void = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "VOID")
        gate, status, signal, action = calibration_for(bucket_midpoints.get(bucket), real, green)
        expected_mid = bucket_midpoint_text.get(bucket, "")
        gap = ""
        if real > 0 and bucket_midpoints.get(bucket) is not None:
            gap = f"{((green / real) * 100.0) - float(bucket_midpoints[bucket]):+.1f}pp"
        out.append({
            "target_date": day,
            "generated_at": generated,
            "confidence_bucket": bucket,
            "expected_confidence_midpoint": expected_mid,
            "sample_rows_total": total,
            "sample_rows_real": real,
            "diagnostic_rows": diagnostic,
            "pending_rows": pending,
            "no_confidence_rows": no_conf,
            "green_rows": green,
            "red_rows": red,
            "void_rows": void,
            "no_pick_rows": outcomes.get("NO_PICK", 0),
            "manual_review_rows": manual.get("YES", 0),
            "observed_green_rate": pct(green, real),
            "calibration_gap_pct_points": gap,
            "sample_gate": gate,
            "calibration_status": status,
            "confidence_bias_signal": signal,
            "recommended_action": action,
            "source_window": "GOVERNANCE_CUMULATIVE_WITH_DAILY_FALLBACK",
            "source_guard": "CONFIDENCE_CALIBRATION_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_confidence_calibration_daily.csv", rows, FIELDS)
        (base / "vsigma_confidence_calibration.md").write_text(markdown(day, rows), encoding="utf-8")
    hist = processed / "governance" / "vsigma_confidence_calibration.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Confidence Calibration - {day}",
        "",
        "## Summary",
        f"- confidence_bucket_rows: {len(rows)}",
        f"- sample_gate_counts: {fmt_counts(rows, 'sample_gate')}",
        f"- calibration_status_counts: {fmt_counts(rows, 'calibration_status')}",
        f"- confidence_bias_signal_counts: {fmt_counts(rows, 'confidence_bias_signal')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Confidence Rows",
    ]
    for row in rows[:100]:
        lines.append(
            "- "
            f"{row.get('confidence_bucket', '')} | expected={row.get('expected_confidence_midpoint', '') or 'NA'} | "
            f"real={row.get('sample_rows_real', '')}/{row.get('sample_rows_total', '')} | "
            f"green={row.get('green_rows', '')} red={row.get('red_rows', '')} void={row.get('void_rows', '')} | "
            f"observed={row.get('observed_green_rate', '') or 'NA'} | gap={row.get('calibration_gap_pct_points', '') or 'NA'} | "
            f"gate={row.get('sample_gate', '')} | status={row.get('calibration_status', '')} | signal={row.get('confidence_bias_signal', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This calibration is advisory only and does not change confidence weights.",
        "- Diagnostic, pending and no-pick rows do not count as real hit-rate sample.",
        "- Confidence upgrades/downgrades require sufficient sample and causal review.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA CONFIDENCE CALIBRATION ===")
    print(f"confidence_bucket_rows={len(rows)}")
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
