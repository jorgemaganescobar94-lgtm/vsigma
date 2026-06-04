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
    "final_decision",
    "decision_bucket",
    "ledger_status",
    "official_pick_permission",
    "postmatch_audit_required",
    "result_source_status",
    "actual_home_goals",
    "actual_away_goals",
    "actual_total_goals",
    "actual_total_xg",
    "actual_total_sot",
    "actual_total_big",
    "audit_status",
    "pick_outcome",
    "market_grade_status",
    "postmatch_quality_label",
    "postmatch_quality_score",
    "error_family",
    "no_bet_audit_label",
    "learning_signal",
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


def load_ledger(processed: Path, day: str) -> list[dict[str, str]]:
    path = first_existing(processed, day, ["vsigma_official_pick_ledger_daily.csv", "vsigma_official_pick_ledger.csv"])
    if not path:
        return []
    rows = read_csv(path)
    if path.name == "vsigma_official_pick_ledger.csv":
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


def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")


def goals(actual: dict[str, str]) -> tuple[int | None, int | None, int | None]:
    hg = as_int(actual.get("actual_home_goals"))
    ag = as_int(actual.get("actual_away_goals"))
    tg = as_int(actual.get("actual_total_goals"))
    if tg is None and hg is not None and ag is not None:
        tg = hg + ag
    return hg, ag, tg


def extract_goal_line(market: str, kind: str) -> float | None:
    patterns = [
        rf"\b{kind}\s*([0-9]+(?:\.[0-9]+)?)\b",
        rf"\b{kind[0]}\s*([0-9]+(?:\.[0-9]+)?)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, market)
        if match:
            return float(match.group(1))
    return None


def grade_total_goals(market: str, total_goals: int | None) -> tuple[str, str]:
    if total_goals is None:
        return "PENDING_RESULT", "No final goal total available."

    upper = up(market)
    under_line = extract_goal_line(upper, "UNDER")
    over_line = extract_goal_line(upper, "OVER")

    if under_line is not None:
        if abs(total_goals - under_line) < 1e-9:
            return "VOID", f"Total goals {total_goals} equals under line {under_line}."
        return ("GREEN" if total_goals < under_line else "RED", f"Total goals {total_goals} vs under line {under_line}.")
    if over_line is not None:
        if abs(total_goals - over_line) < 1e-9:
            return "VOID", f"Total goals {total_goals} equals over line {over_line}."
        return ("GREEN" if total_goals > over_line else "RED", f"Total goals {total_goals} vs over line {over_line}.")

    return "UNKNOWN_MARKET", "Market is not a recognized total-goals line."


def grade_btts(market: str, home_goals: int | None, away_goals: int | None) -> tuple[str, str]:
    if home_goals is None or away_goals is None:
        return "PENDING_RESULT", "No final team goals available."
    upper = up(market)
    both_scored = home_goals > 0 and away_goals > 0
    if "BTTS" in upper or "BOTH TEAMS" in upper or "AMBOS" in upper:
        if "NO" in upper:
            return ("GREEN" if not both_scored else "RED", f"BTTS No vs goals {home_goals}-{away_goals}.")
        if "YES" in upper or "SI" in upper or "SÍ" in upper:
            return ("GREEN" if both_scored else "RED", f"BTTS Yes vs goals {home_goals}-{away_goals}.")
    return "UNKNOWN_MARKET", "Market is not a recognized BTTS line."


def grade_market(market: str, actual: dict[str, str]) -> tuple[str, str, str]:
    hg, ag, tg = goals(actual)
    upper = up(market)
    if not upper or upper == "NO_MARKET":
        return "NO_MARKET", "NO_PICK", "No market to grade."

    if any(token in upper for token in ["UNDER", "OVER", " U", " O"]):
        outcome, note = grade_total_goals(upper, tg)
        return "AUTO_GRADED_TOTAL_GOALS", outcome, note

    if any(token in upper for token in ["BTTS", "BOTH TEAMS", "AMBOS"]):
        outcome, note = grade_btts(upper, hg, ag)
        return "AUTO_GRADED_BTTS", outcome, note

    return "NEEDS_MANUAL_MARKET_GRADING", "UNKNOWN", "Market family is not safely auto-gradable in v1."


def quality_from_outcome(outcome: str, actual: dict[str, str]) -> tuple[str, str, str]:
    total_xg = as_float(actual.get("actual_total_xg"))
    total_sot = as_float(actual.get("actual_total_sot"))
    total_big = as_float(actual.get("actual_total_big"))

    if outcome == "GREEN":
        score = 65
        if total_xg is not None and total_xg <= 2.0:
            score += 10
        if total_big is not None and total_big <= 3:
            score += 10
        if total_sot is not None and total_sot <= 8:
            score += 5
        return "GREEN_RESULT_PENDING_CAUSAL_REVIEW", str(min(score, 90)), "RESULT_GREEN_REVIEW_FOR_CLEANNESS"
    if outcome == "RED":
        score = 35
        if total_xg is not None and total_xg <= 1.4:
            score += 15
        if total_big is not None and total_big <= 2:
            score += 10
        return "RED_RESULT_PENDING_CAUSAL_AUDIT", str(min(score, 60)), "RESULT_RED_REVIEW_FOR_VARIANCE_OR_BAD_READ"
    if outcome == "VOID":
        return "VOID_RESULT", "50", "VOID_NO_MODEL_REINFORCEMENT"
    if outcome == "UNKNOWN":
        return "MANUAL_MARKET_GRADING_REQUIRED", "", "NO_AUTOMATIC_LEARNING"
    return "PENDING_RESULT", "", "WAIT_FOR_FINAL_ACTUALS"


def audit_row(row: dict[str, str], actuals_by_fixture: dict[str, dict[str, str]], generated: str, day: str) -> dict[str, object]:
    fid = fixture_id(row)
    actual = actuals_by_fixture.get(fid, {}) if fid else {}
    ledger_status = norm(row.get("ledger_status"), "UNKNOWN")
    decision_bucket = norm(row.get("decision_bucket"), "UNKNOWN")
    market = norm(row.get("primary_market"), "NO_MARKET")
    permission = norm(row.get("official_pick_permission"), "NO_PICK_NO_STAKE")
    audit_required = norm(row.get("postmatch_audit_required"), "NO")

    actual_status = "FINAL_ACTUALS_FOUND" if actual else "NO_FINAL_ACTUALS_FOUND"
    hg, ag, tg = goals(actual) if actual else (None, None, None)

    if ledger_status.startswith("DIAGNOSTIC") or decision_bucket == "DIAGNOSTIC_ONLY":
        audit_status = "AUDIT_NOT_REQUIRED_DIAGNOSTIC"
        pick_outcome = "NO_PICK"
        market_grade_status = "NO_MARKET_GRADING"
        quality_label = "DIAGNOSTIC_NO_PICK"
        quality_score = ""
        error_family = "NONE"
        no_bet_label = "DIAGNOSTIC_NOT_A_REAL_NO_BET"
        learning_signal = "NO_LEARNING_DIAGNOSTIC_ONLY"
        note = "Diagnostic row from empty/no-promotion board; not a fixture-level decision."
    elif audit_required != "YES":
        audit_status = "AUDIT_NOT_REQUIRED"
        pick_outcome = "NO_PICK"
        market_grade_status = "NO_MARKET_GRADING"
        quality_label = "NO_AUDIT_REQUIRED"
        quality_score = ""
        error_family = "NONE"
        no_bet_label = "NOT_APPLICABLE"
        learning_signal = "NO_LEARNING_NOT_REQUIRED"
        note = "Ledger row does not request postmatch audit."
    elif not actual:
        audit_status = "PENDING_FINAL_ACTUALS"
        pick_outcome = "PENDING"
        market_grade_status = "PENDING_RESULT"
        quality_label = "PENDING"
        quality_score = ""
        error_family = "PENDING"
        no_bet_label = "PENDING" if decision_bucket == "NO_BET" else "NOT_APPLICABLE"
        learning_signal = "WAIT_FOR_FINAL_ACTUALS"
        note = "No final actuals found for fixture yet."
    elif decision_bucket == "NO_BET":
        audit_status = "NO_BET_AUDIT_READY"
        pick_outcome = "NO_PICK"
        market_grade_status = "NO_MARKET_GRADING"
        quality_label = "NO_BET_PENDING_CAUSAL_REVIEW"
        quality_score = ""
        error_family = "NO_BET_REVIEW"
        no_bet_label = "PENDING_NO_BET_CORRECTNESS_REVIEW"
        learning_signal = "NO_BET_REVIEW_REQUIRED"
        note = "Final actuals found; review whether No Bet avoided risk or was too conservative."
    else:
        market_grade_status, pick_outcome, grade_note = grade_market(market, actual)
        quality_label, quality_score, learning_signal = quality_from_outcome(pick_outcome, actual)
        audit_status = "PICK_RESULT_AUTO_GRADED" if pick_outcome in {"GREEN", "RED", "VOID"} else "PICK_RESULT_NEEDS_MANUAL_GRADING"
        error_family = "PENDING_CAUSAL_CLASSIFICATION" if pick_outcome in {"GREEN", "RED"} else "NONE"
        no_bet_label = "NOT_APPLICABLE"
        note = grade_note

    return {
        "target_date": day,
        "generated_at": generated,
        "ledger_key": norm(row.get("ledger_key")),
        "fixture_id": fid,
        "home_team": norm(row.get("home_team")),
        "away_team": norm(row.get("away_team")),
        "primary_market": market,
        "final_decision": norm(row.get("final_decision")),
        "decision_bucket": decision_bucket,
        "ledger_status": ledger_status,
        "official_pick_permission": permission,
        "postmatch_audit_required": audit_required,
        "result_source_status": actual_status,
        "actual_home_goals": "" if hg is None else str(hg),
        "actual_away_goals": "" if ag is None else str(ag),
        "actual_total_goals": "" if tg is None else str(tg),
        "actual_total_xg": norm(actual.get("actual_total_xg")) if actual else "",
        "actual_total_sot": norm(actual.get("actual_total_sot")) if actual else "",
        "actual_total_big": norm(actual.get("actual_total_big")) if actual else "",
        "audit_status": audit_status,
        "pick_outcome": pick_outcome,
        "market_grade_status": market_grade_status,
        "postmatch_quality_label": quality_label,
        "postmatch_quality_score": quality_score,
        "error_family": error_family,
        "no_bet_audit_label": no_bet_label,
        "learning_signal": learning_signal,
        "audit_note": note,
        "source_guard": "POSTMATCH_PICK_AUDIT_V1_NO_AUTO_APPLY",
        "auto_apply": "NO",
        "production_change": "NO",
    }


def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    ledger_rows = load_ledger(processed, day)
    actuals = load_actuals(processed, day)
    if not ledger_rows:
        ledger_rows = [{
            "target_date": day,
            "ledger_key": f"{day}|NO_OFFICIAL_LEDGER",
            "fixture_id": "DIAGNOSTIC_NO_OFFICIAL_LEDGER",
            "home_team": "NO_OFFICIAL_LEDGER",
            "away_team": "NO_OFFICIAL_LEDGER",
            "primary_market": "NO_MARKET",
            "final_decision": "NO_BET",
            "decision_bucket": "DIAGNOSTIC_ONLY",
            "ledger_status": "DIAGNOSTIC_NO_LEDGER",
            "official_pick_permission": "NO_PICK_NO_STAKE",
            "postmatch_audit_required": "NO",
        }]
    return [audit_row(row, actuals, generated, day) for row in ledger_rows]


def update_historical(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    path = processed / "governance" / "vsigma_postmatch_pick_audit.csv"
    existing = read_csv(path)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(path, existing, FIELDS)


def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Postmatch Pick Audit - {day}",
        "",
        "## Summary",
        f"- audit_rows: {len(rows)}",
        f"- audit_status_counts: {fmt_counts(rows, 'audit_status')}",
        f"- pick_outcome_counts: {fmt_counts(rows, 'pick_outcome')}",
        f"- quality_label_counts: {fmt_counts(rows, 'postmatch_quality_label')}",
        f"- learning_signal_counts: {fmt_counts(rows, 'learning_signal')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Audit Rows",
    ]
    for row in rows[:80]:
        lines.append(
            "- "
            f"{row.get('audit_status', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"market={row.get('primary_market', '')} | outcome={row.get('pick_outcome', '')} | "
            f"quality={row.get('postmatch_quality_label', '')} | learning={row.get('learning_signal', '')} | "
            f"note={row.get('audit_note', '')}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This audit does not create picks, stake permission, or automatic model changes.",
        "- GREEN/RED results are not final learning by themselves; causal review is still required.",
        "- NO_BET rows require separate correctness review when tied to a real fixture.",
        "- Diagnostic rows do not train the model.",
    ]
    return "\n".join(lines) + "\n"


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_postmatch_pick_audit_daily.csv", rows, FIELDS)
        (base / "vsigma_postmatch_pick_audit.md").write_text(markdown(day, rows), encoding="utf-8")
    update_historical(processed, day, rows)

    print("=== VSIGMA POSTMATCH PICK AUDIT ===")
    print(f"audit_rows={len(rows)}")
    print(f"audit_status_counts={fmt_counts(rows, 'audit_status')}")
    print(f"pick_outcome_counts={fmt_counts(rows, 'pick_outcome')}")
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
