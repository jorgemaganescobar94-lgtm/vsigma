from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PROCESSED = Path("data/processed")
REGISTRY_PATH = PROCESSED / "governance" / "vsigma_api_shadow_rule_oos_rule_registry.csv"
HISTORY_PATH = PROCESSED / "governance" / "vsigma_api_shadow_rule_oos_tracker_history.csv"

REGISTRY_FIELDS = [
    "rule_signature", "first_seen_date", "first_seen_at", "rule_id", "rule_group_type",
    "rule_group_value", "rule_market", "rule_decision", "rule_bucket", "future_rule_candidate",
    "paper_trade_permission", "activation_permission", "pick_permission", "stake_permission",
]

ROW_FIELDS = [
    "target_date", "generated_at", "oos_id", "rule_signature", "rule_first_seen_date",
    "oos_class", "shadow_id", "rule_id", "fixture_id", "home_team", "away_team", "league", "country",
    "result_status", "home_goals", "away_goals", "prediction_winner", "predicted_side",
    "candidate_signal_score", "candidate_signal_band", "review_priority", "rule_group_type",
    "rule_group_value", "rule_market", "rule_decision", "rule_bucket", "future_rule_candidate",
    "shadow_outcome", "shadow_status", "oos_outcome", "oos_status", "oos_note",
    "paper_trade_permission", "activation_permission", "canonical_board_permission", "pick_permission",
    "stake_permission", "auto_apply", "production_change",
]

SUMMARY_FIELDS = [
    "target_date", "generated_at", "registry_rules", "rows_reviewed", "in_sample_rows",
    "out_of_sample_rows", "pending_rows", "evaluated_rows", "oos_evaluated_rows", "oos_hit_rows",
    "oos_miss_rows", "oos_void_rows", "oos_hit_rate_pct", "oos_hit_or_void_rate_pct",
    "oos_class_counts", "oos_outcome_counts", "rule_market_counts", "activation_permission_counts",
    "pick_permission_counts", "stake_permission_counts", "next_action", "auto_apply", "production_change",
]


def norm(value: object) -> str:
    return "" if value is None else str(value).strip()


def up(value: object) -> str:
    return norm(value).upper()


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


def pct(num: int, den: int) -> str:
    if den <= 0:
        return ""
    return f"{100.0 * num / den:.1f}"


def load_shadow_rows(processed: Path, day: str) -> list[dict[str, str]]:
    rows = read_rows(processed / "today" / day / "vsigma_api_shadow_rule_outcome_ledger.csv")
    if not rows:
        rows = read_rows(processed / "governance" / "vsigma_api_shadow_rule_outcome_ledger.csv")
    return rows


def rule_signature(row: dict[str, str]) -> str:
    parts = [
        up(row.get("rule_group_type")),
        up(row.get("rule_group_value")),
        up(row.get("rule_market")),
        up(row.get("rule_decision")),
        up(row.get("rule_bucket")),
    ]
    return "|".join(parts)


def load_registry() -> dict[str, dict[str, str]]:
    return {norm(row.get("rule_signature")): row for row in read_rows(REGISTRY_PATH) if norm(row.get("rule_signature"))}


def update_registry(registry: dict[str, dict[str, str]], rows: list[dict[str, str]], day: str, generated: str) -> dict[str, dict[str, str]]:
    for row in rows:
        sig = rule_signature(row)
        if not sig or sig in registry:
            continue
        registry[sig] = {
            "rule_signature": sig,
            "first_seen_date": day,
            "first_seen_at": generated,
            "rule_id": norm(row.get("rule_id")),
            "rule_group_type": norm(row.get("rule_group_type")),
            "rule_group_value": norm(row.get("rule_group_value")),
            "rule_market": norm(row.get("rule_market")),
            "rule_decision": norm(row.get("rule_decision")),
            "rule_bucket": norm(row.get("rule_bucket")),
            "future_rule_candidate": norm(row.get("future_rule_candidate")),
            "paper_trade_permission": norm(row.get("paper_trade_permission")) or "SHADOW_ONLY",
            "activation_permission": "NO_RULE_ACTIVATION_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
        }
    return registry


def classify_oos(day: str, first_seen_date: str, shadow_status: str) -> str:
    if up(shadow_status) != "SHADOW_EVALUATED":
        return "PENDING_RESULT"
    if not first_seen_date:
        return "UNKNOWN_RULE_FIRST_SEEN"
    if day == first_seen_date:
        return "IN_SAMPLE_BOOTSTRAP"
    if day > first_seen_date:
        return "OUT_OF_SAMPLE"
    return "PRE_REGISTRY_BACKFILL"


def oos_outcome(row: dict[str, str], oos_class: str) -> tuple[str, str]:
    outcome = up(row.get("shadow_outcome")) or "NOT_EVALUATED"
    if oos_class == "PENDING_RESULT":
        return "PENDING_RESULT", "PENDING"
    if outcome in {"HIT", "MISS", "VOID"}:
        return outcome, "EVALUATED"
    return "NOT_EVALUATED", "NOT_EVALUATED"


def build(day: str, tz: str, processed: Path):
    generated = datetime.now(ZoneInfo(tz)).isoformat(timespec="seconds")
    shadow_rows = load_shadow_rows(processed, day)
    registry = update_registry(load_registry(), shadow_rows, day, generated)
    out: list[dict[str, object]] = []

    for idx, row in enumerate(shadow_rows, start=1):
        sig = rule_signature(row)
        reg = registry.get(sig, {})
        first_seen = norm(reg.get("first_seen_date"))
        oos_class = classify_oos(day, first_seen, norm(row.get("shadow_status")))
        outcome, status = oos_outcome(row, oos_class)
        out.append({
            "target_date": day,
            "generated_at": generated,
            "oos_id": f"API_OOS_{idx:05d}",
            "rule_signature": sig,
            "rule_first_seen_date": first_seen,
            "oos_class": oos_class,
            "shadow_id": norm(row.get("shadow_id")),
            "rule_id": norm(row.get("rule_id")),
            "fixture_id": norm(row.get("fixture_id")),
            "home_team": norm(row.get("home_team")),
            "away_team": norm(row.get("away_team")),
            "league": norm(row.get("league")),
            "country": norm(row.get("country")),
            "result_status": norm(row.get("result_status")),
            "home_goals": norm(row.get("home_goals")),
            "away_goals": norm(row.get("away_goals")),
            "prediction_winner": norm(row.get("prediction_winner")),
            "predicted_side": norm(row.get("predicted_side")),
            "candidate_signal_score": norm(row.get("candidate_signal_score")),
            "candidate_signal_band": norm(row.get("candidate_signal_band")),
            "review_priority": norm(row.get("review_priority")),
            "rule_group_type": norm(row.get("rule_group_type")),
            "rule_group_value": norm(row.get("rule_group_value")),
            "rule_market": norm(row.get("rule_market")),
            "rule_decision": norm(row.get("rule_decision")),
            "rule_bucket": norm(row.get("rule_bucket")),
            "future_rule_candidate": norm(row.get("future_rule_candidate")),
            "shadow_outcome": norm(row.get("shadow_outcome")),
            "shadow_status": norm(row.get("shadow_status")),
            "oos_outcome": outcome,
            "oos_status": status,
            "oos_note": "Out-of-sample tracker only. Same first_seen_date rows are bootstrap/in-sample and cannot validate future promotion.",
            "paper_trade_permission": "SHADOW_ONLY",
            "activation_permission": "NO_RULE_ACTIVATION_PERMISSION",
            "canonical_board_permission": "NO_CANONICAL_BOARD_PERMISSION",
            "pick_permission": "NO_PICK_PERMISSION",
            "stake_permission": "NO_STAKE_PERMISSION",
            "auto_apply": "NO",
            "production_change": "NO",
        })

    evaluated = [r for r in out if r["oos_status"] == "EVALUATED"]
    oos_eval = [r for r in evaluated if r["oos_class"] == "OUT_OF_SAMPLE"]
    oos_hit = sum(1 for r in oos_eval if r["oos_outcome"] == "HIT")
    oos_miss = sum(1 for r in oos_eval if r["oos_outcome"] == "MISS")
    oos_void = sum(1 for r in oos_eval if r["oos_outcome"] == "VOID")

    summary = [{
        "target_date": day,
        "generated_at": generated,
        "registry_rules": len(registry),
        "rows_reviewed": len(out),
        "in_sample_rows": sum(1 for r in out if r["oos_class"] == "IN_SAMPLE_BOOTSTRAP"),
        "out_of_sample_rows": sum(1 for r in out if r["oos_class"] == "OUT_OF_SAMPLE"),
        "pending_rows": sum(1 for r in out if r["oos_class"] == "PENDING_RESULT"),
        "evaluated_rows": len(evaluated),
        "oos_evaluated_rows": len(oos_eval),
        "oos_hit_rows": oos_hit,
        "oos_miss_rows": oos_miss,
        "oos_void_rows": oos_void,
        "oos_hit_rate_pct": pct(oos_hit, len(oos_eval)),
        "oos_hit_or_void_rate_pct": pct(oos_hit + oos_void, len(oos_eval)),
        "oos_class_counts": counts(out, "oos_class"),
        "oos_outcome_counts": counts(out, "oos_outcome"),
        "rule_market_counts": counts(out, "rule_market"),
        "activation_permission_counts": counts(out, "activation_permission"),
        "pick_permission_counts": counts(out, "pick_permission"),
        "stake_permission_counts": counts(out, "stake_permission"),
        "next_action": "Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.",
        "auto_apply": "NO",
        "production_change": "NO",
    }]
    return out, summary, registry, markdown(day, out, summary[0])


def market_oos_summary(rows: list[dict[str, object]]) -> list[str]:
    lines = []
    markets = sorted({str(r.get("rule_market")) for r in rows if r.get("rule_market")})
    for market in markets:
        subset = [r for r in rows if r.get("rule_market") == market and r.get("oos_class") == "OUT_OF_SAMPLE" and r.get("oos_status") == "EVALUATED"]
        hit = sum(1 for r in subset if r.get("oos_outcome") == "HIT")
        miss = sum(1 for r in subset if r.get("oos_outcome") == "MISS")
        void = sum(1 for r in subset if r.get("oos_outcome") == "VOID")
        denom = len(subset)
        if denom == 0:
            lines.append(f"- {market} | oos_evaluated=0 | status=NO_OUT_OF_SAMPLE_YET")
        else:
            lines.append(f"- {market} | oos_evaluated={denom} | HIT={hit} | MISS={miss} | VOID={void} | hit_rate={pct(hit, denom)} | hit_or_void={pct(hit + void, denom)}")
    return lines


def markdown(day: str, rows: list[dict[str, object]], summary: dict[str, object]) -> str:
    lines = [
        f"# vSIGMA API Shadow Rule Out-of-Sample Tracker - {day}",
        "",
        "## Summary",
        f"- registry_rules: {summary['registry_rules']}",
        f"- rows_reviewed: {summary['rows_reviewed']}",
        f"- in_sample_rows: {summary['in_sample_rows']}",
        f"- out_of_sample_rows: {summary['out_of_sample_rows']}",
        f"- pending_rows: {summary['pending_rows']}",
        f"- evaluated_rows: {summary['evaluated_rows']}",
        f"- oos_evaluated_rows: {summary['oos_evaluated_rows']}",
        f"- oos_hit_rows: {summary['oos_hit_rows']}",
        f"- oos_miss_rows: {summary['oos_miss_rows']}",
        f"- oos_void_rows: {summary['oos_void_rows']}",
        f"- oos_hit_rate_pct: {summary['oos_hit_rate_pct']}",
        f"- oos_hit_or_void_rate_pct: {summary['oos_hit_or_void_rate_pct']}",
        f"- oos_class_counts: {summary['oos_class_counts']}",
        f"- oos_outcome_counts: {summary['oos_outcome_counts']}",
        f"- activation_permission_counts: {summary['activation_permission_counts']}",
        f"- pick_permission_counts: {summary['pick_permission_counts']}",
        f"- stake_permission_counts: {summary['stake_permission_counts']}",
        f"- next_action: {summary['next_action']}",
        "- auto_apply: NO",
        "- production_change: NO",
        "",
        "## Market Out-of-Sample Summary",
    ]
    lines.extend(market_oos_summary(rows) or ["- none."])
    lines += ["", "## OOS Rows"]
    for row in rows[:120]:
        score = f"{row.get('home_goals')}-{row.get('away_goals')}" if row.get("result_status") == "FINISHED_RESULT" else "pending"
        lines.append(
            f"- {row['oos_id']} | {row['oos_class']} | first_seen={row['rule_first_seen_date']} | {row['home_team']} vs {row['away_team']} | score={score} | market={row['rule_market']} | outcome={row['oos_outcome']} | pick={row['pick_permission']} | stake={row['stake_permission']}"
        )
    lines += [
        "",
        "## Guardrails",
        "- This tracker separates bootstrap/in-sample rows from future out-of-sample rows.",
        "- It does not activate rules, picks, stake, canonical board permission, whitelist permission, or execution permission.",
        "- Future promotion requires separate implementation after sufficient OUT_OF_SAMPLE evidence.",
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
    section = "## API Shadow Rule Out-of-Sample Tracker"
    lines = [
        section,
        f"- registry_rules: {summary.get('registry_rules', 'UNKNOWN')}",
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- in_sample_rows: {summary.get('in_sample_rows', 'UNKNOWN')}",
        f"- out_of_sample_rows: {summary.get('out_of_sample_rows', 'UNKNOWN')}",
        f"- pending_rows: {summary.get('pending_rows', 'UNKNOWN')}",
        f"- oos_evaluated_rows: {summary.get('oos_evaluated_rows', 'UNKNOWN')}",
        f"- oos_class_counts: {summary.get('oos_class_counts', 'UNKNOWN')}",
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


def update_history(rows: list[dict[str, object]]) -> None:
    existing = read_rows(HISTORY_PATH)
    merged: dict[tuple[str, str, str], dict[str, object]] = {}
    for row in existing:
        key = (norm(row.get("target_date")), norm(row.get("shadow_id")), norm(row.get("rule_signature")))
        if all(key):
            merged[key] = row
    for row in rows:
        key = (norm(row.get("target_date")), norm(row.get("shadow_id")), norm(row.get("rule_signature")))
        if all(key):
            merged[key] = row
    ordered = sorted(merged.values(), key=lambda r: (norm(r.get("target_date")), norm(r.get("rule_market")), norm(r.get("shadow_id"))))
    write_csv(HISTORY_PATH, ordered, ROW_FIELDS)


def run(day: str, tz: str, processed: Path) -> None:
    day = date.fromisoformat(day).isoformat()
    rows, summary, registry, md = build(day, tz, processed)
    for base in [processed / "today" / day, processed / "governance"]:
        write_csv(base / "vsigma_api_shadow_rule_oos_tracker.csv", rows, ROW_FIELDS)
        write_csv(base / "vsigma_api_shadow_rule_oos_tracker_summary.csv", summary, SUMMARY_FIELDS)
        (base / "vsigma_api_shadow_rule_oos_tracker.md").write_text(md, encoding="utf-8")
    write_csv(REGISTRY_PATH, sorted(registry.values(), key=lambda r: norm(r.get("rule_signature"))), REGISTRY_FIELDS)
    update_history(rows)
    append_panel(processed, day, summary[0])
    print("=== VSIGMA API SHADOW RULE OUT-OF-SAMPLE TRACKER ===")
    print(f"registry_rules={summary[0]['registry_rules']}")
    print(f"rows_reviewed={summary[0]['rows_reviewed']}")
    print(f"in_sample_rows={summary[0]['in_sample_rows']}")
    print(f"out_of_sample_rows={summary[0]['out_of_sample_rows']}")
    print(f"oos_evaluated_rows={summary[0]['oos_evaluated_rows']}")
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
