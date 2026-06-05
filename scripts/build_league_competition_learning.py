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
    "competition_key",
    "country",
    "league",
    "sample_rows_total",
    "sample_rows_real",
    "diagnostic_rows",
    "pending_rows",
    "no_pick_rows",
    "green_rows",
    "red_rows",
    "void_rows",
    "no_bet_rows",
    "no_bet_protection_candidate_rows",
    "no_bet_too_conservative_candidate_rows",
    "high_event_rows",
    "low_event_rows",
    "manual_review_rows",
    "market_family_counts",
    "top_market_family",
    "observed_green_rate",
    "red_rate_real_sample",
    "sample_gate",
    "data_coverage_status",
    "volatility_status",
    "competition_learning_status",
    "recommended_downstream_use",
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


def load_rows(processed: Path, day: str, names: list[str]) -> list[dict[str, str]]:
    path = first_existing(processed, day, names)
    if not path:
        return []
    return read_csv(path)


def by_key(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = norm(row.get("ledger_key"))
        if key:
            out[key] = row
    return out


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


def compact_counts(counter: Counter[str]) -> str:
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["fixture_id", "home_team", "away_team", "decision_bucket", "ledger_status", "quality_class"]
    )
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text


def is_pending(row: dict[str, str]) -> bool:
    text = " ".join(up(row.get(name)) for name in ["pick_outcome", "quality_class", "learning_action"])
    return "PENDING" in text or "WAIT_FOR" in text


def competition_key(row: dict[str, str]) -> tuple[str, str, str]:
    if is_diagnostic(row):
        return "DIAGNOSTIC", "DIAGNOSTIC_NO_COMPETITION", "DIAGNOSTIC|DIAGNOSTIC_NO_COMPETITION"
    country = norm(row.get("country"), "UNKNOWN_COUNTRY")
    league = norm(row.get("league"), "UNKNOWN_LEAGUE")
    return country, league, f"{country}|{league}"


def merge_inputs(processed: Path, day: str) -> list[dict[str, str]]:
    ledger = load_rows(processed, day, ["vsigma_official_pick_ledger.csv", "vsigma_official_pick_ledger_daily.csv"])
    quality = by_key(load_rows(processed, day, ["vsigma_pick_quality_classification.csv", "vsigma_pick_quality_classification_daily.csv"]))
    translation = by_key(load_rows(processed, day, ["vsigma_market_translation_audit.csv", "vsigma_market_translation_audit_daily.csv"]))
    no_bet = by_key(load_rows(processed, day, ["vsigma_no_bet_audit.csv", "vsigma_no_bet_audit_daily.csv"]))

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
        for source in [quality.get(key, {}), translation.get(key, {}), no_bet.get(key, {})]:
            for field, value in source.items():
                if field in {"target_date", "generated_at"}:
                    continue
                if field in {"country", "league"} and norm(row.get(field)):
                    continue
                if norm(value):
                    row[field] = value
        merged.append(row)
    return merged


def classify_competition(real: int, green: int, red: int, diagnostic: int, pending: int, high_event: int, low_event: int) -> tuple[str, str, str, str]:
    gate = sample_gate(real)
    if real <= 0:
        if diagnostic > 0 and pending == 0:
            return (
                "DIAGNOSTIC_ONLY_NO_REAL_SAMPLE",
                "UNKNOWN_VOLATILITY",
                "DIAGNOSTIC_ONLY_NO_SCORING",
                "No real audited sample for this competition; keep diagnostic/collection only.",
            )
        return (
            "HOLD_NO_REAL_SAMPLE",
            "UNKNOWN_VOLATILITY",
            "COVERAGE_GATE_ONLY",
            "No real green/red/void sample; collect more before scoring confidence.",
        )

    green_rate = green / real
    red_rate = red / real
    high_rate = high_event / real
    low_rate = low_event / real

    if high_rate >= 0.35:
        volatility = "HIGH_VOLATILITY"
    elif low_rate >= 0.45:
        volatility = "LOW_EVENT_TENDENCY"
    else:
        volatility = "MIXED_VOLATILITY"

    if gate == "INSUFFICIENT_SAMPLE":
        return (
            "HOLD_SAMPLE",
            volatility,
            "COVERAGE_GATE_ONLY",
            "Sample below minimum; do not allow competition-level scoring changes.",
        )
    if gate == "OBSERVE_ONLY_SAMPLE":
        return (
            "OBSERVE_ONLY",
            volatility,
            "COVERAGE_GATE_ONLY",
            "Competition has observable sample but still too small for scoring confidence movement.",
        )
    if green_rate >= 0.66 and red_rate <= 0.28 and volatility != "HIGH_VOLATILITY":
        return (
            "POSITIVE_COMPETITION_SIGNAL_CANDIDATE",
            volatility,
            "SCORING_ALLOWED_WITH_NORMAL_GATES_CANDIDATE",
            "Competition sample is positive; require causal review before stronger scoring use.",
        )
    if red_rate >= 0.42 or volatility == "HIGH_VOLATILITY":
        return (
            "NEGATIVE_OR_VOLATILE_COMPETITION_SIGNAL",
            volatility,
            "COVERAGE_GATE_ONLY_OR_DIAGNOSTIC_REVIEW",
            "Competition shows elevated red rate or volatility; review before scoring use.",
        )
    return (
        "NEUTRAL_COMPETITION_SIGNAL",
        volatility,
        "COVERAGE_GATE_ONLY",
        "No strong competition-level signal; keep normal collection and review.",
    )


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = merge_inputs(processed, day)
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    meta: dict[str, tuple[str, str]] = {}

    for row in rows:
        country, league, key = competition_key(row)
        groups[key].append(row)
        meta[key] = (country, league)

    out: list[dict[str, object]] = []
    for key, comp_rows in sorted(groups.items()):
        country, league = meta[key]
        diagnostic = sum(1 for row in comp_rows if is_diagnostic(row))
        pending = sum(1 for row in comp_rows if is_pending(row))
        real_rows = [
            row for row in comp_rows
            if not is_diagnostic(row) and not is_pending(row) and up(row.get("pick_outcome")) in {"GREEN", "RED", "VOID"}
        ]

        real = len(real_rows)
        green = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "GREEN")
        red = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "RED")
        void = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "VOID")
        no_pick = sum(1 for row in comp_rows if up(row.get("pick_outcome")) in {"NO_PICK", ""})
        no_bet_rows = sum(1 for row in comp_rows if up(row.get("decision_bucket")) == "NO_BET" or "NO_BET" in up(row.get("no_bet_audit_status")))
        no_bet_protect = sum(1 for row in comp_rows if "PROTECTION" in up(row.get("no_bet_quality_label")))
        no_bet_conservative = sum(1 for row in comp_rows if "TOO_CONSERVATIVE" in up(row.get("no_bet_quality_label")))
        high_event = sum(1 for row in comp_rows if "HIGH" in up(row.get("no_bet_evidence_profile")) or "HIGH" in up(row.get("translation_quality_label")))
        low_event = sum(1 for row in comp_rows if "LOW_EVENT" in up(row.get("no_bet_evidence_profile")))
        manual = sum(1 for row in comp_rows if up(row.get("manual_review_required")) == "YES")

        family_counter = Counter(norm(row.get("market_family"), "UNKNOWN_FAMILY") for row in comp_rows)
        top_family = family_counter.most_common(1)[0][0] if family_counter else "UNKNOWN_FAMILY"

        status, volatility, downstream, action = classify_competition(real, green, red, diagnostic, pending, high_event, low_event)
        data_coverage = "HAS_REAL_SAMPLE" if real > 0 else ("DIAGNOSTIC_ONLY" if diagnostic else "NO_REAL_SAMPLE")

        out.append({
            "target_date": day,
            "generated_at": generated,
            "competition_key": key,
            "country": country,
            "league": league,
            "sample_rows_total": len(comp_rows),
            "sample_rows_real": real,
            "diagnostic_rows": diagnostic,
            "pending_rows": pending,
            "no_pick_rows": no_pick,
            "green_rows": green,
            "red_rows": red,
            "void_rows": void,
            "no_bet_rows": no_bet_rows,
            "no_bet_protection_candidate_rows": no_bet_protect,
            "no_bet_too_conservative_candidate_rows": no_bet_conservative,
            "high_event_rows": high_event,
            "low_event_rows": low_event,
            "manual_review_rows": manual,
            "market_family_counts": compact_counts(family_counter),
            "top_market_family": top_family,
            "observed_green_rate": pct(green, real),
            "red_rate_real_sample": pct(red, real),
            "sample_gate": sample_gate(real),
            "data_coverage_status": data_coverage,
            "volatility_status": volatility,
            "competition_learning_status": status,
            "recommended_downstream_use": downstream,
            "recommended_action": action,
            "source_window": "GOVERNANCE_CUMULATIVE_WITH_DAILY_FALLBACK",
            "source_guard": "LEAGUE_COMPETITION_LEARNING_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out


def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_league_competition_learning_daily.csv", rows, FIELDS)
        (base / "vsigma_league_competition_learning.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_league_competition_learning.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA League / Competition Learning - {day}",
        "",
        "## Summary",
        f"- competition_rows: {len(rows)}",
        f"- sample_gate_counts: {fmt_counts(rows, 'sample_gate')}",
        f"- data_coverage_status_counts: {fmt_counts(rows, 'data_coverage_status')}",
        f"- volatility_status_counts: {fmt_counts(rows, 'volatility_status')}",
        f"- competition_learning_status_counts: {fmt_counts(rows, 'competition_learning_status')}",
        f"- recommended_downstream_use_counts: {fmt_counts(rows, 'recommended_downstream_use')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Competition Rows",
    ]

    for row in rows[:120]:
        lines.append(
            "- "
            f"{row.get('competition_key', '')} | real={row.get('sample_rows_real', '')}/{row.get('sample_rows_total', '')} | "
            f"green={row.get('green_rows', '')} red={row.get('red_rows', '')} void={row.get('void_rows', '')} | "
            f"no_bet={row.get('no_bet_rows', '')} | top_family={row.get('top_market_family', '')} | "
            f"gate={row.get('sample_gate', '')} | volatility={row.get('volatility_status', '')} | "
            f"status={row.get('competition_learning_status', '')} | downstream={row.get('recommended_downstream_use', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This competition learning report is advisory only and never changes league scoring permissions.",
        "- Diagnostic and pending rows do not count as real hit-rate samples.",
        "- SCORING_ALLOWED recommendations are candidates only and require causal/manual review.",
        "- No picks, stakes, production changes, or automatic downstream changes are created here.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA LEAGUE / COMPETITION LEARNING ===")
    print(f"competition_rows={len(rows)}")
    print(f"sample_gate_counts={fmt_counts(rows, 'sample_gate')}")
    print(f"competition_learning_status_counts={fmt_counts(rows, 'competition_learning_status')}")
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
