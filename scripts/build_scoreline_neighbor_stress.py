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
    "actual_home_goals",
    "actual_away_goals",
    "actual_total_goals",
    "actual_scoreline",
    "goal_margin",
    "scoreline_neighbor_bucket",
    "draw_neighbor_flag",
    "one_goal_margin_flag",
    "low_score_flag",
    "high_score_flag",
    "scoreline_data_status",
    "scoreline_stress_status",
    "scoreline_learning_label",
    "stress_evidence_level",
    "manual_review_required",
    "recommended_action",
    "scoreline_note",
    "source_guard",
    "auto_apply",
    "production_change",
]

NEIGHBOR_SCORELINES = {
    "0-0": "NIL_NIL",
    "1-0": "HOME_1_0",
    "0-1": "AWAY_0_1",
    "1-1": "DRAW_1_1",
    "2-1": "HOME_2_1",
    "1-2": "AWAY_1_2",
    "2-0": "HOME_2_0",
    "0-2": "AWAY_0_2",
}

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

def by_fixture(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        fid = norm(row.get("fixture_id")).replace(".0", "")
        if fid:
            out[fid] = row
    return out

def fixture_id(row: dict[str, str]) -> str:
    return norm(row.get("fixture_id")).replace(".0", "")

def as_int(value: object) -> int | None:
    text = norm(value)
    if not text or text.lower() == "nan":
        return None
    try:
        return int(round(float(text)))
    except ValueError:
        return None

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

def load_actuals(processed: Path, day: str) -> dict[str, dict[str, str]]:
    actual_rows = load_rows(processed, day, ["vsigma_post_match_stat_actuals.csv", "matches.csv"])
    return by_fixture(actual_rows)

def actual_goals(row: dict[str, str], actual: dict[str, str]) -> tuple[int | None, int | None, int | None]:
    hg = (
        as_int(actual.get("actual_home_goals"))
        or as_int(actual.get("home_goals"))
        or as_int(actual.get("goals_home"))
        or as_int(row.get("actual_home_goals"))
    )
    ag = (
        as_int(actual.get("actual_away_goals"))
        or as_int(actual.get("away_goals"))
        or as_int(actual.get("goals_away"))
        or as_int(row.get("actual_away_goals"))
    )
    tg = (
        as_int(actual.get("actual_total_goals"))
        or as_int(actual.get("total_goals"))
        or as_int(row.get("actual_total_goals"))
    )
    if tg is None and hg is not None and ag is not None:
        tg = hg + ag
    return hg, ag, tg

def scoreline_bucket(home_goals: int | None, away_goals: int | None, total_goals: int | None) -> tuple[str, str, int | None]:
    if home_goals is None or away_goals is None:
        return "NO_SCORELINE", "NO_SCORELINE", None

    scoreline = f"{home_goals}-{away_goals}"
    margin = home_goals - away_goals
    if scoreline in NEIGHBOR_SCORELINES:
        return scoreline, NEIGHBOR_SCORELINES[scoreline], margin

    if home_goals == away_goals:
        return scoreline, "OTHER_DRAW", margin
    if abs(margin) == 1:
        return scoreline, "OTHER_ONE_GOAL_MARGIN", margin
    if total_goals is not None and total_goals >= 4:
        return scoreline, "HIGH_SCORELINE", margin
    if total_goals is not None and total_goals <= 1:
        return scoreline, "LOW_SCORELINE", margin
    return scoreline, "OTHER_SCORELINE", margin

def classify_stress(row: dict[str, str], home_goals: int | None, away_goals: int | None, total_goals: int | None, bucket: str) -> tuple[str, str, str, str, str, str]:
    if is_diagnostic(row):
        return (
            "DIAGNOSTIC_NO_SCORELINE_STRESS",
            "DIAGNOSTIC_NOT_REAL_FIXTURE",
            "NONE",
            "NO",
            "NO_MODEL_CHANGE",
            "Diagnostic row; no scoreline neighbor stress can be evaluated.",
        )

    if home_goals is None or away_goals is None:
        return (
            "SCORELINE_DATA_MISSING",
            "NO_SCORELINE_SIGNAL",
            "LOW",
            "NO",
            "COLLECT_FINAL_SCORELINE_DATA",
            "No usable final scoreline found for this fixture.",
        )

    outcome = up(row.get("pick_outcome"))
    market_family = up(row.get("market_family"))
    decision_bucket = up(row.get("decision_bucket"))
    is_draw = home_goals == away_goals
    one_goal_margin = abs(home_goals - away_goals) == 1
    low_score = (total_goals or 0) <= 1
    high_score = (total_goals or 0) >= 4

    if decision_bucket == "NO_BET":
        if bucket in {"NIL_NIL", "DRAW_1_1", "LOW_SCORELINE", "OTHER_DRAW"}:
            return (
                "NO_BET_SCORELINE_REVIEW",
                "NO_BET_TOO_CONSERVATIVE_SCORELINE_CANDIDATE",
                "MEDIUM",
                "YES",
                "REVIEW_IF_SAFE_LOW_EVENT_MARKET_WAS_MISSED",
                "No Bet landed on low/draw neighbor; review whether protection was correct or too conservative.",
            )
        return (
            "NO_BET_SCORELINE_CONTEXT",
            "NO_BET_PROTECTION_OR_NEUTRAL_SCORELINE",
            "LOW",
            "YES",
            "REVIEW_NO_BET_CONTEXT_ONLY",
            "No Bet with final scoreline available; review manually before learning.",
        )

    if outcome == "RED":
        if market_family in {"MATCH_WINNER", "DNB_AH0", "HANDICAP"} and is_draw:
            return (
                "DRAW_NEIGHBOR_FAILURE_REVIEW",
                "SIDE_MARKET_DRAW_FRAGILITY",
                "HIGH",
                "YES",
                "REVIEW_DRAW_SURVIVAL_AND_PROTECTED_MARKET",
                "Side/protected market failed or suffered around a draw neighbor.",
            )
        if market_family in {"MATCH_WINNER", "HANDICAP"} and one_goal_margin:
            return (
                "ONE_GOAL_MARGIN_FAILURE_REVIEW",
                "SIDE_MARKET_THIN_MARGIN_FRAGILITY",
                "HIGH",
                "YES",
                "REVIEW_MARGIN_DEPENDENCY_AND_SAFER_FAMILY",
                "Market appears exposed to a one-goal neighbor scoreline.",
            )
        if market_family == "TOTAL_GOALS" and (low_score or high_score):
            return (
                "TOTALS_SCORELINE_FAILURE_REVIEW",
                "TOTALS_LINE_WIDTH_OR_STATE_FAILURE",
                "HIGH",
                "YES",
                "REVIEW_TOTAL_LINE_WIDTH_AND_STATE_SURVIVAL",
                "Total-goals market failed around low/high scoreline stress.",
            )
        return (
            "RED_SCORELINE_CAUSAL_REVIEW",
            "SCORELINE_NEIGHBOR_FAILURE_REVIEW",
            "MEDIUM",
            "YES",
            "REVIEW_SCORELINE_NEIGHBOR_FAILURE",
            "Red result requires scoreline-neighbor causal review.",
        )

    if outcome == "GREEN":
        if bucket in NEIGHBOR_SCORELINES.values():
            return (
                "GREEN_NEIGHBOR_SURVIVAL_REVIEW",
                "MARKET_SURVIVED_MODAL_NEIGHBOR",
                "MEDIUM",
                "YES",
                "REVIEW_IF_GREEN_WAS_ROBUST_OR_LUCKY",
                "Green result landed on a common neighboring scoreline; review robustness.",
            )
        return (
            "GREEN_STANDARD_SCORELINE_REVIEW",
            "MARKET_SURVIVED_SCORELINE",
            "LOW",
            "NO",
            "KEEP_COLLECTING_SAMPLE",
            "Green result with no obvious scoreline-neighbor stress.",
        )

    if outcome == "VOID":
        return (
            "VOID_SCORELINE_REVIEW",
            "PUSH_NEIGHBOR_NO_REINFORCEMENT",
            "LOW",
            "NO",
            "NO_MODEL_CHANGE",
            "Void/push result; record but do not reinforce.",
        )

    return (
        "SCORELINE_CONTEXT_ONLY",
        "NO_SAFE_SCORELINE_LEARNING",
        "LOW",
        "NO",
        "KEEP_COLLECTING_SAMPLE",
        "Final scoreline exists but no safe scoreline stress label is available.",
    )

def build(day: str, tz: str, processed: Path) -> list[dict[str, object]]:
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    base_rows = merge_inputs(processed, day)
    actuals = load_actuals(processed, day)

    out: list[dict[str, object]] = []
    for row in base_rows:
        fid = fixture_id(row)
        actual = actuals.get(fid, {})
        hg, ag, tg = actual_goals(row, actual)
        scoreline, bucket, margin = scoreline_bucket(hg, ag, tg)
        stress_status, label, evidence, manual, action, note = classify_stress(row, hg, ag, tg, bucket)

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
            "actual_home_goals": "" if hg is None else hg,
            "actual_away_goals": "" if ag is None else ag,
            "actual_total_goals": "" if tg is None else tg,
            "actual_scoreline": "" if scoreline == "NO_SCORELINE" else scoreline,
            "goal_margin": "" if margin is None else margin,
            "scoreline_neighbor_bucket": bucket,
            "draw_neighbor_flag": "YES" if hg is not None and ag is not None and hg == ag else "NO",
            "one_goal_margin_flag": "YES" if margin is not None and abs(margin) == 1 else "NO",
            "low_score_flag": "YES" if tg is not None and tg <= 1 else "NO",
            "high_score_flag": "YES" if tg is not None and tg >= 4 else "NO",
            "scoreline_data_status": "HAS_FINAL_SCORELINE" if hg is not None and ag is not None else "NO_SCORELINE_DATA",
            "scoreline_stress_status": stress_status,
            "scoreline_learning_label": label,
            "stress_evidence_level": evidence,
            "manual_review_required": manual,
            "recommended_action": action,
            "scoreline_note": note,
            "source_guard": "SCORELINE_NEIGHBOR_STRESS_V1_NO_AUTO_APPLY",
            "auto_apply": "NO",
            "production_change": "NO",
        })
    return out

def write_outputs(processed: Path, day: str, rows: list[dict[str, object]]) -> None:
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_scoreline_neighbor_stress_daily.csv", rows, FIELDS)
        (base / "vsigma_scoreline_neighbor_stress.md").write_text(markdown(day, rows), encoding="utf-8")

    hist = processed / "governance" / "vsigma_scoreline_neighbor_stress.csv"
    existing = read_csv(hist)
    existing = [row for row in existing if norm(row.get("target_date")) != day]
    existing.extend({field: str(row.get(field, "")) for field in FIELDS} for row in rows)
    write_csv(hist, existing, FIELDS)

def fmt_counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"

def markdown(day: str, rows: list[dict[str, object]]) -> str:
    lines = [
        f"# vSIGMA Scoreline Neighbor Stress - {day}",
        "",
        "## Summary",
        f"- scoreline_rows: {len(rows)}",
        f"- scoreline_data_status_counts: {fmt_counts(rows, 'scoreline_data_status')}",
        f"- scoreline_neighbor_bucket_counts: {fmt_counts(rows, 'scoreline_neighbor_bucket')}",
        f"- scoreline_stress_status_counts: {fmt_counts(rows, 'scoreline_stress_status')}",
        f"- scoreline_learning_label_counts: {fmt_counts(rows, 'scoreline_learning_label')}",
        f"- stress_evidence_level_counts: {fmt_counts(rows, 'stress_evidence_level')}",
        f"- manual_review_required_counts: {fmt_counts(rows, 'manual_review_required')}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Scoreline Rows",
    ]

    for row in rows[:120]:
        lines.append(
            "- "
            f"{row.get('scoreline_stress_status', '')} | {row.get('home_team', '')} vs {row.get('away_team', '')} | "
            f"score={row.get('actual_scoreline', '') or 'NA'} bucket={row.get('scoreline_neighbor_bucket', '')} | "
            f"market={row.get('market_family', '')} outcome={row.get('pick_outcome', '')} | "
            f"label={row.get('scoreline_learning_label', '')} | manual={row.get('manual_review_required', '')} | "
            f"action={row.get('recommended_action', '')}"
        )

    lines += [
        "",
        "## Guardrails",
        "- This scoreline stress report is advisory only and never changes picks, stake, gates, or weights.",
        "- Neighbor labels are review candidates, not automatic truth.",
        "- Diagnostic and missing-scoreline rows must not train the model.",
        "- No automatic market-family, live, or production changes are created here.",
    ]
    return "\n".join(lines) + "\n"

def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows = build(day, tz, processed)
    write_outputs(processed, day, rows)
    print("=== VSIGMA SCORELINE NEIGHBOR STRESS ===")
    print(f"scoreline_rows={len(rows)}")
    print(f"scoreline_data_status_counts={fmt_counts(rows, 'scoreline_data_status')}")
    print(f"scoreline_stress_status_counts={fmt_counts(rows, 'scoreline_stress_status')}")
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
