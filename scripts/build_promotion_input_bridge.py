from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

ROW_FIELDS = [
    "target_date",
    "generated_at",
    "fixture_id",
    "home_team",
    "away_team",
    "league",
    "country",
    "fixture_date_utc",
    "fixture_status",
    "downstream_use",
    "scored_candidate_status",
    "fixture_detail_available",
    "predictions_available",
    "odds_available",
    "prediction_winner_name",
    "pred_home_total_pct",
    "pred_away_total_pct",
    "match_winner_home_odd",
    "match_winner_draw_odd",
    "match_winner_away_odd",
    "over_2_5_odd",
    "under_2_5_odd",
    "market_signal_summary",
    "candidate_signal_score",
    "candidate_signal_band",
    "promotion_input_status",
    "promotion_input_reason",
    "promotion_permission",
    "pick_permission",
    "stake_permission",
    "source_guard",
    "auto_apply",
    "production_change",
]

SUMMARY_FIELDS = [
    "target_date",
    "generated_at",
    "source_rows_reviewed",
    "bridge_rows_written",
    "promotion_ready_review_only_rows",
    "blocked_rows",
    "status_counts",
    "signal_band_counts",
    "promotion_permission_counts",
    "pick_permission_counts",
    "stake_permission_counts",
    "auto_apply",
    "production_change",
]

def norm(value: object, default: str = "") -> str:
    text = "" if value is None else str(value).strip()
    return text if text else default

def as_float(value: object) -> float | None:
    text = norm(value)
    if not text:
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None

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
    for name in names:
        for path in [processed / "today" / day / name, processed / "governance" / name]:
            if path.exists():
                return path
    return None

def load_candidates(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_api_enriched_scored_candidates.csv"])
    rows = read_csv(path) if path else []
    if path and path.parent.name == "governance" and rows and "target_date" in rows[0]:
        rows = [row for row in rows if norm(row.get("target_date")) == day]
    return rows

def implied_prob(odd: object) -> float | None:
    value = as_float(odd)
    if value is None or value <= 1.0:
        return None
    return 100.0 / value

def signal_score(row: dict[str, str]) -> int:
    home_pct = as_float(row.get("pred_home_total_pct")) or 0.0
    away_pct = as_float(row.get("pred_away_total_pct")) or 0.0
    pred_edge = abs(home_pct - away_pct)

    has_1x2 = bool(norm(row.get("match_winner_home_odd")) and norm(row.get("match_winner_away_odd")))
    has_ou = bool(norm(row.get("over_2_5_odd")) and norm(row.get("under_2_5_odd")))
    has_winner = bool(norm(row.get("prediction_winner_name")))

    score = 0
    score += min(int(pred_edge * 1.5), 45)
    if has_winner:
        score += 15
    if has_1x2:
        score += 20
    if has_ou:
        score += 10
    if norm(row.get("fixture_detail_available")) == "YES":
        score += 10

    return max(0, min(score, 100))

def signal_band(score: int) -> str:
    if score >= 75:
        return "HIGH_SIGNAL_REVIEW"
    if score >= 55:
        return "MEDIUM_SIGNAL_REVIEW"
    if score >= 35:
        return "LOW_SIGNAL_REVIEW"
    return "WEAK_SIGNAL"

def classify(row: dict[str, str], score: int) -> tuple[str, str, str]:
    status = norm(row.get("scored_candidate_status"))
    downstream = norm(row.get("downstream_use"))
    fixture_ok = norm(row.get("fixture_detail_available")) == "YES"
    pred_ok = norm(row.get("predictions_available")) == "YES"
    odds_ok = norm(row.get("odds_available")) == "YES"

    if downstream != "SCORING_ALLOWED_WITH_NORMAL_GATES":
        return (
            "COVERAGE_ONLY_NO_PROMOTION",
            "Downstream use is not scoring-allowed.",
            "NO_PROMOTION_PERMISSION",
        )

    if status != "API_ENRICHED_SCORING_READY_PENDING_GATES":
        return (
            "BLOCKED_NOT_SCORING_READY",
            "API-enriched candidate is not scoring-ready pending gates.",
            "NO_PROMOTION_PERMISSION",
        )

    if not fixture_ok or not (pred_ok or odds_ok):
        return (
            "BLOCKED_NO_MARKET_SIGNAL",
            "Missing fixture detail or market/prediction signal.",
            "NO_PROMOTION_PERMISSION",
        )

    return (
        "PROMOTION_INPUT_READY_REVIEW_ONLY",
        "Candidate can be reviewed by normal scoring/promotion gates; no pick permission created.",
        "REVIEW_ONLY_PROMOTION_INPUT",
    )

def build(day: str, tz: str, processed: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], str]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    source_rows = load_candidates(processed, day)

    out: list[dict[str, object]] = []
    for row in source_rows:
        score = signal_score(row)
        band = signal_band(score)
        status, reason, promotion_permission = classify(row, score)

        out.append({
            "target_date": day,
            "generated_at": generated,
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "fixture_date_utc": norm(row.get("fixture_date_utc")),
            "fixture_status": norm(row.get("fixture_status")),
            "downstream_use": norm(row.get("downstream_use")),
            "scored_candidate_status": norm(row.get("scored_candidate_status")),
            "fixture_detail_available": norm(row.get("fixture_detail_available")),
            "predictions_available": norm(row.get("predictions_available")),
            "odds_available": norm(row.get("odds_available")),
            "prediction_winner_name": norm(row.get("prediction_winner_name")),
            "pred_home_total_pct": norm(row.get("pred_home_total_pct")),
            "pred_away_total_pct": norm(row.get("pred_away_total_pct")),
            "match_winner_home_odd": norm(row.get("match_winner_home_odd")),
            "match_winner_draw_odd": norm(row.get("match_winner_draw_odd")),
            "match_winner_away_odd": norm(row.get("match_winner_away_odd")),
            "over_2_5_odd": norm(row.get("over_2_5_odd")),
            "under_2_5_odd": norm(row.get("under_2_5_odd")),
            "market_signal_summary": norm(row.get("market_signal_summary")),
            "candidate_signal_score": score,
            "candidate_signal_band": band,
            "promotion_input_status": status,
            "promotion_input_reason": reason,
            "promotion_permission": promotion_permission,
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "source_guard": "PROMOTION_INPUT_BRIDGE_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "source_rows_reviewed": len(source_rows),
        "bridge_rows_written": len(out),
        "promotion_ready_review_only_rows": sum(1 for row in out if row["promotion_input_status"] == "PROMOTION_INPUT_READY_REVIEW_ONLY"),
        "blocked_rows": sum(1 for row in out if str(row["promotion_input_status"]).startswith("BLOCKED") or row["promotion_input_status"] == "COVERAGE_ONLY_NO_PROMOTION"),
        "status_counts": counts(out, "promotion_input_status"),
        "signal_band_counts": counts(out, "candidate_signal_band"),
        "promotion_permission_counts": counts(out, "promotion_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "auto_apply": "NO",
        "production_change": "NO",
    }]

    return out, summary, markdown(day, out, summary[0])

def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA Promotion Input Bridge - {day}",
        "",
        "## Summary",
        f"- source_rows_reviewed: {summary['source_rows_reviewed']}",
        f"- bridge_rows_written: {summary['bridge_rows_written']}",
        f"- promotion_ready_review_only_rows: {summary['promotion_ready_review_only_rows']}",
        f"- blocked_rows: {summary['blocked_rows']}",
        f"- status_counts: {summary['status_counts']}",
        f"- signal_band_counts: {summary['signal_band_counts']}",
        f"- promotion_permission_counts: {summary['promotion_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Bridge Rows",
    ]

    for row in rows[:120]:
        lines.append(
            f"- {row['home_team']} vs {row['away_team']} | bridge={row['promotion_input_status']} | "
            f"score={row['candidate_signal_score']} band={row['candidate_signal_band']} | "
            f"summary={row['market_signal_summary']} | promotion={row['promotion_permission']} | "
            f"pick={row['pick_permission']} | stake={row['stake_permission']}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This bridge only prepares review inputs for normal gates.",
        "- It does not create picks, stake permission, market recommendations, or execution permission.",
        "- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.",
        "- auto_apply=NO and production_change=NO are hardcoded.",
    ]
    return "\n".join(lines) + "\n"

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]], summary: list[dict[str, object]], md: str) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_promotion_input_bridge.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_promotion_input_bridge_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_promotion_input_bridge.md").write_text(md, encoding="utf-8")

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    write_outputs(processed, day, rows, summary, md)
    s = summary[0]
    print("=== VSIGMA PROMOTION INPUT BRIDGE ===")
    print(f"bridge_rows_written={s['bridge_rows_written']}")
    print(f"promotion_ready_review_only_rows={s['promotion_ready_review_only_rows']}")
    print(f"pick_permission_counts={s['pick_permission_counts']}")
    print(f"stake_permission_counts={s['stake_permission_counts']}")
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
