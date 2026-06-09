from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")

MARKET_TO_LEDGER_FIELD = {
    "API_1X2": "api_1x2_result",
    "API_DOUBLE_CHANCE": "api_double_chance_result",
    "API_DNB": "api_dnb_result",
    "OVER_1_5": "over_1_5_result",
    "OVER_2_5": "over_2_5_result",
    "UNDER_3_5": "under_3_5_result",
    "BTTS_YES": "btts_result",
}

ROW_FIELDS = [
    "target_date", "generated_at", "shadow_id", "rule_id", "fixture_id", "home_team", "away_team",
    "league", "country", "result_status", "home_goals", "away_goals", "prediction_winner",
    "predicted_side", "candidate_signal_score", "candidate_signal_band", "review_priority",
    "rule_group_type", "rule_group_value", "rule_market", "rule_decision", "rule_bucket",
    "future_rule_candidate", "shadow_market_result", "shadow_outcome", "shadow_status",
    "shadow_reason", "paper_trade_permission", "activation_permission", "canonical_board_permission",
    "pick_permission", "stake_permission", "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "rules_available", "candidate_rules_applied", "shadow_rows",
    "finished_shadow_rows", "pending_shadow_rows", "hit_rows", "miss_rows", "void_rows",
    "not_evaluated_rows", "shadow_outcome_counts", "rule_market_counts", "rule_decision_counts",
    "paper_trade_permission_counts", "activation_permission_counts", "pick_permission_counts",
    "stake_permission_counts", "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


def as_int(value: object) -> int:
    try:
        text = norm(value)
        return int(float(text)) if text else 0
    except ValueError:
        return 0


def read_rows(path: Path) -> list[dict[str, str]]:
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


def counts(rows: list[dict[str, object]], field: str) -> str:
    counter = Counter(str(row.get(field) or "UNKNOWN") for row in rows)
    return "; ".join(f"{key}={value}" for key, value in counter.most_common()) if counter else "none"


def load_rule_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_calibration_rule_candidates.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_calibration_rule_candidates.csv")
    return rows


def load_ledger_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_enriched_postmatch_accuracy_ledger.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_enriched_postmatch_accuracy_ledger.csv")
    return rows


def score_bucket(row: dict[str, str]) -> str:
    score = as_int(row.get("candidate_signal_score"))
    if score >= 90:
        return "SCORE_90_PLUS"
    if score >= 80:
        return "SCORE_80_89"
    if score >= 70:
        return "SCORE_70_79"
    if score >= 55:
        return "SCORE_55_69"
    return "SCORE_BELOW_55"


def row_group_value(row: dict[str, str], group_type: str) -> str:
    group_type = up(group_type)
    if group_type == "ALL":
        return "ALL"
    if group_type == "SIGNAL_BAND":
        return norm(row.get("candidate_signal_band")) or "UNKNOWN_SIGNAL_BAND"
    if group_type == "REVIEW_PRIORITY":
        return norm(row.get("review_priority")) or "UNKNOWN_REVIEW_PRIORITY"
    if group_type == "PREDICTED_SIDE":
        return norm(row.get("predicted_side")) or "UNKNOWN_SIDE"
    if group_type == "SCORE_BUCKET":
        return score_bucket(row)
    return "UNKNOWN_GROUP_TYPE"


def rule_matches_fixture(rule: dict[str, str], fixture_row: dict[str, str]) -> bool:
    group_type = norm(rule.get("group_type"))
    group_value = norm(rule.get("group_value"))
    if up(group_type) == "ALL":
        return True
    return up(row_group_value(fixture_row, group_type)) == up(group_value)


def candidate_rules(rules: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for rule in rules:
        if not up(rule.get("future_rule_candidate")).startswith("YES"):
            continue
        if up(rule.get("activation_permission")) != "NO_RULE_ACTIVATION_PERMISSION":
            continue
        market = up(rule.get("market"))
        if market not in MARKET_TO_LEDGER_FIELD:
            continue
        out.append(rule)
    return out


def normalize_outcome(value: str) -> tuple[str, str]:
    value = up(value)
    if value in {"HIT", "MISS", "VOID", "PENDING_RESULT", "NOT_EVALUATED"}:
        return value, value
    if not value:
        return "NOT_EVALUATED", "NOT_EVALUATED"
    return "NOT_EVALUATED", value


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    all_rules = load_rule_rows(processed, day)
    rules = candidate_rules(all_rules)
    ledger_rows = load_ledger_rows(processed, day)
    out: list[dict[str, object]] = []

    shadow_n = 0
    for rule in rules:
        market = up(rule.get("market"))
        ledger_field = MARKET_TO_LEDGER_FIELD[market]
        for fixture_row in ledger_rows:
            if not rule_matches_fixture(rule, fixture_row):
                continue
            shadow_n += 1
            outcome, raw_result = normalize_outcome(norm(fixture_row.get(ledger_field)))
            result_status = up(fixture_row.get("result_status"))
            shadow_status = "SHADOW_PENDING" if outcome == "PENDING_RESULT" or result_status != "FINISHED_RESULT" else "SHADOW_EVALUATED"
            out.append({
                "target_date": day,
                "generated_at": generated,
                "shadow_id": f"API_SHADOW_{shadow_n:05d}",
                "rule_id": norm(rule.get("rule_id")),
                "fixture_id": norm(fixture_row.get("fixture_id")),
                "home_team": norm(fixture_row.get("home_team")),
                "away_team": norm(fixture_row.get("away_team")),
                "league": norm(fixture_row.get("league")),
                "country": norm(fixture_row.get("country")),
                "result_status": norm(fixture_row.get("result_status")),
                "home_goals": norm(fixture_row.get("home_goals")),
                "away_goals": norm(fixture_row.get("away_goals")),
                "prediction_winner": norm(fixture_row.get("prediction_winner")),
                "predicted_side": norm(fixture_row.get("predicted_side")),
                "candidate_signal_score": norm(fixture_row.get("candidate_signal_score")),
                "candidate_signal_band": norm(fixture_row.get("candidate_signal_band")),
                "review_priority": norm(fixture_row.get("review_priority")),
                "rule_group_type": norm(rule.get("group_type")),
                "rule_group_value": norm(rule.get("group_value")),
                "rule_market": market,
                "rule_decision": norm(rule.get("rule_decision")),
                "rule_bucket": norm(rule.get("rule_bucket")),
                "future_rule_candidate": norm(rule.get("future_rule_candidate")),
                "shadow_market_result": raw_result,
                "shadow_outcome": outcome,
                "shadow_status": shadow_status,
                "shadow_reason": "Paper-trading only. Candidate rule applied to historical/postmatch ledger row.",
                "paper_trade_permission": "SHADOW_ONLY",
                "activation_permission": "NO_RULE_ACTIVATION_PERMISSION",
                "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
                "pick_permission": "NO_PICK_PERMISSION",
                "stake_permission": "NO_STAKE_PERMISSION",
                "auto_apply": "NO",
                "production_change": "NO",
            })

    finished_rows = [row for row in out if row["shadow_status"] == "SHADOW_EVALUATED"]
    pending_rows = [row for row in out if row["shadow_status"] != "SHADOW_EVALUATED"]
    summary = [{
        "target_date": day,
        "generated_at": generated,
        "rules_available": len(all_rules),
        "candidate_rules_applied": len(rules),
        "shadow_rows": len(out),
        "finished_shadow_rows": len(finished_rows),
        "pending_shadow_rows": len(pending_rows),
        "hit_rows": sum(1 for row in out if row["shadow_outcome"] == "HIT"),
        "miss_rows": sum(1 for row in out if row["shadow_outcome"] == "MISS"),
        "void_rows": sum(1 for row in out if row["shadow_outcome"] == "VOID"),
        "not_evaluated_rows": sum(1 for row in out if row["shadow_outcome"] == "NOT_EVALUATED"),
        "shadow_outcome_counts": counts(out, "shadow_outcome"),
        "rule_market_counts": counts(out, "rule_market"),
        "rule_decision_counts": counts(out, "rule_decision"),
        "paper_trade_permission_counts": counts(out, "paper_trade_permission"),
        "activation_permission_counts": counts(out, "activation_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, markdown(day, out, summary[0])


def market_summary(rows: list[dict[str, object]]) -> list[str]:
    lines = []
    markets = sorted({str(row.get("rule_market")) for row in rows if row.get("rule_market")})
    for market in markets:
        subset = [row for row in rows if row.get("rule_market") == market]
        evaluated = [row for row in subset if row.get("shadow_status") == "SHADOW_EVALUATED"]
        hit = sum(1 for row in evaluated if row.get("shadow_outcome") == "HIT")
        miss = sum(1 for row in evaluated if row.get("shadow_outcome") == "MISS")
        void = sum(1 for row in evaluated if row.get("shadow_outcome") == "VOID")
        denom = len(evaluated)
        hit_rate = "" if denom == 0 else f"{100 * hit / denom:.1f}"
        hit_or_void = "" if denom == 0 else f"{100 * (hit + void) / denom:.1f}"
        lines.append(
            f"- {market} | evaluated={denom} | HIT={hit} | MISS={miss} | VOID={void} | hit_rate={hit_rate} | hit_or_void={hit_or_void}"
        )
    return lines


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Shadow Rule Outcome Ledger - {day}",
        "",
        "## Summary",
        f"- rules_available: {summary['rules_available']}",
        f"- candidate_rules_applied: {summary['candidate_rules_applied']}",
        f"- shadow_rows: {summary['shadow_rows']}",
        f"- finished_shadow_rows: {summary['finished_shadow_rows']}",
        f"- pending_shadow_rows: {summary['pending_shadow_rows']}",
        f"- shadow_outcome_counts: {summary['shadow_outcome_counts']}",
        f"- rule_market_counts: {summary['rule_market_counts']}",
        f"- paper_trade_permission_counts: {summary['paper_trade_permission_counts']}",
        f"- activation_permission_counts: {summary['activation_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Market Shadow Summary",
    ]
    ms = market_summary(rows)
    lines.extend(ms if ms else ["- none. No candidate rules applied."])
    lines += ["", "## Shadow Rows"]
    if not rows:
        lines.append("- none.")
    for row in rows[:120]:
        score = f"{row.get('home_goals')}-{row.get('away_goals')}" if row.get("result_status") == "FINISHED_RESULT" else "pending"
        lines.append(
            f"- {row['shadow_id']} | {row['rule_id']} | {row['home_team']} vs {row['away_team']} | score={score} | market={row['rule_market']} | outcome={row['shadow_outcome']} | status={row['shadow_status']} | paper={row['paper_trade_permission']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This ledger is shadow/paper-trading only.",
        "- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.",
        "- Any future promotion must be implemented separately after sufficient out-of-sample evidence exists.",
    ]
    return "\n".join(lines) + "\n"


def replace_or_append_section(text: str, section: str, block: str) -> str:
    if section not in text:
        return text.rstrip() + block
    before = text.split(section, 1)[0].rstrip()
    after = text.split(section, 1)[1]
    next_idx = after.find("\n## ")
    tail = after[next_idx:] if next_idx >= 0 else ""
    return before + block + tail


def append_panel(processed: Path, day: str, summary: dict[str, object]) -> None:
    section = "## API Shadow Rule Outcome Ledger"
    lines = [
        section,
        f"- candidate_rules_applied: {summary.get('candidate_rules_applied', 'UNKNOWN')}",
        f"- shadow_rows: {summary.get('shadow_rows', 'UNKNOWN')}",
        f"- finished_shadow_rows: {summary.get('finished_shadow_rows', 'UNKNOWN')}",
        f"- pending_shadow_rows: {summary.get('pending_shadow_rows', 'UNKNOWN')}",
        f"- shadow_outcome_counts: {summary.get('shadow_outcome_counts', 'UNKNOWN')}",
        f"- rule_market_counts: {summary.get('rule_market_counts', 'UNKNOWN')}",
        f"- paper_trade_permission_counts: {summary.get('paper_trade_permission_counts', 'UNKNOWN')}",
        f"- activation_permission_counts: {summary.get('activation_permission_counts', 'UNKNOWN')}",
        f"- pick_permission_counts: {summary.get('pick_permission_counts', 'UNKNOWN')}",
        f"- stake_permission_counts: {summary.get('stake_permission_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ]
    block = "\n" + "\n".join(lines) + "\n"
    for base in [processed / "today" / day, processed / "governance"]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            md_path.write_text(replace_or_append_section(text, section, block), encoding="utf-8")


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_shadow_rule_outcome_ledger.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_shadow_rule_outcome_ledger_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_shadow_rule_outcome_ledger.md").write_text(md, encoding="utf-8")
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API SHADOW RULE OUTCOME LEDGER ===")
    print(f"candidate_rules_applied={summary[0]['candidate_rules_applied']}")
    print(f"shadow_rows={summary[0]['shadow_rows']}")
    print(f"finished_shadow_rows={summary[0]['finished_shadow_rows']}")
    print(f"shadow_outcome_counts={summary[0]['shadow_outcome_counts']}")
    print(f"paper_trade_permission_counts={summary[0]['paper_trade_permission_counts']}")
    print(f"pick_permission_counts={summary[0]['pick_permission_counts']}")
    print(f"stake_permission_counts={summary[0]['stake_permission_counts']}")
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
