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
    "cluster_type",
    "cluster_key",
    "sample_rows_total",
    "sample_rows_real",
    "diagnostic_rows",
    "pending_rows",
    "no_pick_rows",
    "green_rows",
    "red_rows",
    "void_rows",
    "no_bet_rows",
    "manual_review_rows",
    "correlated_failure_rows",
    "correlated_green_rows",
    "concentration_ratio",
    "green_rate_real_sample",
    "red_rate_real_sample",
    "portfolio_correlation_status",
    "correlation_risk_label",
    "recommended_action",
    "source_window",
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
    if not path:
        return []
    rows = read_csv(path)
    if path.parent.name == "governance" and not path.name.endswith("_daily.csv"):
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def by_key(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = norm(row.get("ledger_key"))
        if key:
            out[key] = row
    return out

def parse_confidence(value: object) -> str:
    text = norm(value)
    if not text:
        return "NO_CONFIDENCE"
    match = re.search(r"\d+(?:\.\d+)?", text.replace(",", "."))
    if not match:
        return "NO_CONFIDENCE"
    val = float(match.group(0))
    if 0 <= val <= 1:
        val *= 100
    if val < 50:
        return "CONF_LT_50"
    if val < 60:
        return "CONF_50_59"
    if val < 65:
        return "CONF_60_64"
    if val < 70:
        return "CONF_65_69"
    if val < 75:
        return "CONF_70_74"
    if val < 80:
        return "CONF_75_79"
    if val < 85:
        return "CONF_80_84"
    if val < 90:
        return "CONF_85_89"
    return "CONF_90_PLUS"

def is_diagnostic(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in [
            "fixture_id",
            "home_team",
            "away_team",
            "decision_bucket",
            "ledger_status",
            "quality_class",
            "market_family",
        ]
    )
    return "DIAGNOSTIC" in text or "NO_PROMOTED_RAW_CANDIDATES" in text

def is_pending(row: dict[str, str]) -> bool:
    text = " ".join(
        up(row.get(name))
        for name in ["pick_outcome", "quality_class", "learning_action", "result_status"]
    )
    return "PENDING" in text or "WAIT_FOR" in text

def merge_inputs(processed: Path, day: str) -> list[dict[str, str]]:
    ledger = load_rows(processed, day, ["vsigma_official_pick_ledger.csv", "vsigma_official_pick_ledger_daily.csv"])

    sources = [
        by_key(load_rows(processed, day, ["vsigma_pick_quality_classification.csv", "vsigma_pick_quality_classification_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_market_translation_audit.csv", "vsigma_market_translation_audit_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_no_bet_audit.csv", "vsigma_no_bet_audit_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_lineup_shock_learning.csv", "vsigma_lineup_shock_learning_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_goal_timing_learning.csv", "vsigma_goal_timing_learning_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_scoreline_neighbor_stress.csv", "vsigma_scoreline_neighbor_stress_daily.csv"])),
        by_key(load_rows(processed, day, ["vsigma_league_competition_learning.csv", "vsigma_league_competition_learning_daily.csv"])),
    ]

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
            "pick_outcome": "NO_PICK",
        }]

    merged: list[dict[str, str]] = []
    for base in ledger:
        key = norm(base.get("ledger_key"))
        row = dict(base)
        for source_map in sources:
            for field, value in source_map.get(key, {}).items():
                if field in {"target_date", "generated_at"}:
                    continue
                if field in {"country", "league"} and norm(row.get(field)):
                    continue
                if norm(value):
                    row[field] = value
        row["confidence_bucket"] = parse_confidence(row.get("forecast_confidence"))
        merged.append(row)
    return merged

def pct(num: int, den: int) -> str:
    if den <= 0:
        return ""
    return f"{(num / den) * 100:.1f}%"

def cluster_specs(row: dict[str, str]) -> list[tuple[str, str]]:
    country = norm(row.get("country"), "UNKNOWN_COUNTRY")
    league = norm(row.get("league"), "UNKNOWN_LEAGUE")
    specs = [
        ("DAILY_PORTFOLIO", "ALL"),
        ("MARKET_FAMILY", norm(row.get("market_family"), "UNKNOWN_FAMILY")),
        ("COUNTRY", country),
        ("LEAGUE", f"{country}|{league}"),
        ("DECISION_BUCKET", norm(row.get("decision_bucket"), "UNKNOWN_DECISION")),
        ("CONFIDENCE_BUCKET", norm(row.get("confidence_bucket"), "NO_CONFIDENCE")),
        ("QUALITY_CLASS", norm(row.get("quality_class"), "UNKNOWN_QUALITY")),
        ("ERROR_FAMILY", norm(row.get("error_family"), "UNKNOWN_ERROR")),
        ("LINEUP_SHOCK_STATUS", norm(row.get("lineup_shock_status"), "NO_LINEUP_STATUS")),
        ("GOAL_TIMING_PROFILE", norm(row.get("goal_timing_profile"), "NO_GOAL_TIMING_PROFILE")),
        ("SCORELINE_BUCKET", norm(row.get("scoreline_neighbor_bucket"), "NO_SCORELINE_BUCKET")),
        ("NO_BET_QUALITY", norm(row.get("no_bet_quality_label"), "NO_NO_BET_LABEL")),
    ]
    return [(kind, key) for kind, key in specs if key and key not in {"", "UNKNOWN", "NONE"}]

def classify_cluster(
    total: int,
    real: int,
    diagnostic: int,
    pending: int,
    green: int,
    red: int,
    void: int,
    no_bet: int,
    cluster_type: str,
    cluster_key: str,
) -> tuple[str, str, str]:
    if diagnostic == total:
        return (
            "DIAGNOSTIC_ONLY_NO_PORTFOLIO_LEARNING",
            "NONE",
            "Diagnostic-only cluster; do not learn portfolio correlation.",
        )

    if total < 2:
        return (
            "SINGLETON_NO_CORRELATION_SAMPLE",
            "LOW",
            "Only one row in cluster; no portfolio correlation can be inferred.",
        )

    if real == 0:
        if no_bet >= 2:
            return (
                "NO_BET_CONCENTRATION_REVIEW",
                "MEDIUM",
                "Multiple No Bet rows share this cluster; review whether the system is overblocking.",
            )
        return (
            "NO_REAL_RESULT_SAMPLE",
            "LOW",
            "Cluster has no real green/red/void sample yet.",
        )

    red_rate = red / real if real else 0.0
    green_rate = green / real if real else 0.0
    no_bet_rate = no_bet / total if total else 0.0

    if red >= 2 and red_rate >= 0.50:
        return (
            "CORRELATED_FAILURE_CANDIDATE",
            "HIGH",
            "Multiple red outcomes share this cluster; review hidden correlation before future portfolio exposure.",
        )

    if green >= 2 and green_rate >= 0.70:
        return (
            "POSITIVE_CLUSTER_CANDIDATE",
            "MEDIUM",
            "Multiple green outcomes share this cluster; review causally before reinforcing.",
        )

    if no_bet >= 2 and no_bet_rate >= 0.60:
        return (
            "NO_BET_CLUSTER_CONCENTRATION",
            "MEDIUM",
            "Cluster is dominated by No Bet decisions; review overconservatism vs protection.",
        )

    if total >= 3 and real <= 1:
        return (
            "CONCENTRATION_WITH_LOW_REAL_SAMPLE",
            "MEDIUM",
            "Cluster has repeated exposure but little real outcome sample.",
        )

    return (
        "NEUTRAL_OR_INSUFFICIENT_CORRELATION",
        "LOW",
        "No strong portfolio correlation signal yet.",
    )

def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    rows = merge_inputs(processed, day)

    clusters: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        for spec in cluster_specs(row):
            clusters.setdefault(spec, []).append(row)

    out: list[dict[str, object]] = []
    portfolio_total = max(len(rows), 1)

    for (cluster_type, cluster_key), cluster_rows in sorted(clusters.items()):
        total = len(cluster_rows)
        diagnostic = sum(1 for row in cluster_rows if is_diagnostic(row))
        pending = sum(1 for row in cluster_rows if is_pending(row))
        real_rows = [
            row for row in cluster_rows
            if not is_diagnostic(row) and not is_pending(row) and up(row.get("pick_outcome")) in {"GREEN", "RED", "VOID"}
        ]
        real = len(real_rows)
        green = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "GREEN")
        red = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "RED")
        void = sum(1 for row in real_rows if up(row.get("pick_outcome")) == "VOID")
        no_pick = sum(1 for row in cluster_rows if up(row.get("pick_outcome")) in {"NO_PICK", ""})
        no_bet = sum(1 for row in cluster_rows if up(row.get("decision_bucket")) == "NO_BET" or "NO_BET" in up(row.get("no_bet_audit_status")))
        manual = sum(1 for row in cluster_rows if up(row.get("manual_review_required")) == "YES")
        status, risk, action = classify_cluster(total, real, diagnostic, pending, green, red, void, no_bet, cluster_type, cluster_key)

        out.append({
            "target_date": day,
            "generated_at": generated,
            "cluster_type": cluster_type,
            "cluster_key": cluster_key,
            "sample_rows_total": total,
            "sample_rows_real": real,
            "diagnostic_rows": diagnostic,
            "pending_rows": pending,
            "no_pick_rows": no_pick,
            "green_rows": green,
            "red_rows": red,
            "void_rows": void,
            "no_bet_rows": no_bet,
            "manual_review_rows": manual,
            "correlated_failure_rows": red if status == "CORRELATED_FAILURE_CANDIDATE" else 0,
            "correlated_green_rows": green if status == "POSITIVE_CLUSTER_CANDIDATE" else 0,
            "concentration_ratio": pct(total, portfolio_total),
            "green_rate_real_sample": pct(green, real),
            "red_rate_real_sample": pct(red, real),
            "portfolio_correlation_status": status,
            "correlation_risk_label": risk,
            "recommended_action": action,
            "source_window": "GOVERNANCE_CUMULATIVE_WITH_DAILY_FALLBACK",
            "source_guard": "PORTFOLIO_CORRELATION_LEARNING_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    return out

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_portfolio_correlation_learning_daily.csv", rows, FIELDS)
        (base / "vsigma_portfolio_correlation_learning.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_portfolio_correlation_learning.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)

def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Portfolio / Correlation Learning - {day}",
        "",
        "## Summary",
        f"- cluster_rows: {len(rows)}",
        f"- portfolio_correlation_status_counts: {fmt_counts(rows, 'portfolio_correlation_status')}",
        f"- correlation_risk_label_counts: {fmt_counts(rows, 'correlation_risk_label')}",
        f"- cluster_type_counts: {fmt_counts(rows, 'cluster_type')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Cluster Rows",
    ]

    for row in rows[:140]:
        lines.append(
            "- "
            f"{row.get('cluster_type', '')}:{row.get('cluster_key', '')} | "
            f"rows={row.get('sample_rows_total', '')} real={row.get('sample_rows_real', '')} | "
            f"green={row.get('green_rows', '')} red={row.get('red_rows', '')} no_bet={row.get('no_bet_rows', '')} | "
            f"status={row.get('portfolio_correlation_status', '')} | risk={row.get('correlation_risk_label', '')} | "
            f"action={row.get('recommended_action', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This portfolio correlation report is advisory only and never changes picks, stake, gates, or weights.",
        "- Correlation labels are review candidates, not automatic truth.",
        "- Diagnostic and single-row clusters must not train the model.",
        "- No automatic portfolio cap, market-family change, or production change is created here.",
    ]
    return "\n".join(lines) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA PORTFOLIO / CORRELATION LEARNING ===")
    print(f"cluster_rows={len(rows)}")
    print(f"portfolio_correlation_status_counts={fmt_counts(rows, 'portfolio_correlation_status')}")
    print(f"correlation_risk_label_counts={fmt_counts(rows, 'correlation_risk_label')}")
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
