from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path

import build_consolidated_daily_operator_panel_v2 as panel_v2
import build_date_coherence_guard as date_guard
import build_upstream_board_input_diagnostic as upstream_diag
import build_real_shortlist_recovery_diagnostic as real_shortlist_diag
import build_local_raw_fixture_discovery as local_raw_discovery
import apply_raw_candidate_trust_gate as raw_trust_gate
import apply_trusted_raw_candidate_promotion_gate as raw_promotion_gate
import build_scoring_gap_explainer as scoring_gap
import build_trusted_raw_scoring_queue as scoring_queue
import build_queue_to_enrichment_dry_run_planner as enrichment_dry_run
import build_enrichment_cost_approval_gate as enrichment_approval_gate
import build_daily_board_self_heal_from_promotion_gate as board_self_heal

ROOT = Path("data/processed")
TODAY = ROOT / "today"
GOVERNANCE = ROOT / "governance"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def append_panel_section(day: str, section_title: str, section_key: str, summary: dict[str, str], lines: list[str], status_field: str, detail_builder) -> None:
    for base in [TODAY / day, GOVERNANCE]:
        md_path = base / "vsigma_consolidated_daily_operator_panel.md"
        csv_path = base / "vsigma_consolidated_daily_operator_panel.csv"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8", errors="replace")
            block = "\n".join(["", f"## {section_title}", *lines]) + "\n"
            if f"## {section_title}" not in text:
                md_path.write_text(text + block, encoding="utf-8")
        rows = read_csv(csv_path)
        if rows:
            fields = list(rows[0].keys())
            existing = {row.get("section") for row in rows}
            if section_key not in existing:
                rows.append({
                    "target_date": day,
                    "generated_at": summary.get("generated_at", ""),
                    "section": section_key,
                    "status": summary.get(status_field, "UNKNOWN"),
                    "detail": detail_builder(summary),
                    "next_action": summary.get("next_action", "UNKNOWN"),
                    "auto_apply": "NO",
                    "production_change": "NO",
                })
                write_csv(csv_path, rows, fields)


def append_date_guard_to_panel(day: str, guard_summary: dict[str, str]) -> None:
    append_panel_section(day, "Date Coherence Guard", "date_coherence_guard", guard_summary, [
        f"- overall_status: {guard_summary.get('overall_status', 'UNKNOWN')}",
        f"- board_status: {guard_summary.get('board_status', 'UNKNOWN')}",
        f"- mismatch_count: {guard_summary.get('mismatch_count', 'UNKNOWN')}",
        f"- missing_core_count: {guard_summary.get('missing_core_count', 'UNKNOWN')}",
        f"- trigger_date_counts: {guard_summary.get('trigger_date_counts', 'UNKNOWN')}",
        f"- next_action: {guard_summary.get('next_action', 'UNKNOWN')}",
    ], "overall_status", lambda s: f"board_status={s.get('board_status', 'UNKNOWN')}; mismatch_count={s.get('mismatch_count', 'UNKNOWN')}; missing_core_count={s.get('missing_core_count', 'UNKNOWN')}; trigger_date_counts={s.get('trigger_date_counts', 'UNKNOWN')}")


def append_upstream_diag_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Upstream Board Input Diagnostic", "upstream_board_input_diagnostic", summary, [
        f"- overall_status: {summary.get('overall_status', 'UNKNOWN')}",
        f"- first_empty_required_component: {summary.get('first_empty_required_component', 'UNKNOWN')}",
        f"- missing_required_count: {summary.get('missing_required_count', 'UNKNOWN')}",
        f"- empty_required_count: {summary.get('empty_required_count', 'UNKNOWN')}",
        f"- date_issue_count: {summary.get('date_issue_count', 'UNKNOWN')}",
        f"- forecast_rows: {summary.get('forecast_rows', 'UNKNOWN')}",
        f"- translator_rows: {summary.get('translator_rows', 'UNKNOWN')}",
        f"- board_rows: {summary.get('board_rows', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "overall_status", lambda s: f"first_empty_required_component={s.get('first_empty_required_component', 'UNKNOWN')}; forecast_rows={s.get('forecast_rows', 'UNKNOWN')}; translator_rows={s.get('translator_rows', 'UNKNOWN')}; board_rows={s.get('board_rows', 'UNKNOWN')}")


def append_real_shortlist_diag_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Real Shortlist Recovery Diagnostic", "real_shortlist_recovery_diagnostic", summary, [
        f"- overall_status: {summary.get('overall_status', 'UNKNOWN')}",
        f"- root_cause: {summary.get('root_cause', 'UNKNOWN')}",
        f"- root_scored_same_day_rows: {summary.get('root_scored_same_day_rows', 'UNKNOWN')}",
        f"- real_shortlist_rows: {summary.get('real_shortlist_rows', 'UNKNOWN')}",
        f"- real_bet_rows: {summary.get('real_bet_rows', 'UNKNOWN')}",
        f"- proxy_rows: {summary.get('proxy_rows', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "overall_status", lambda s: f"root_cause={s.get('root_cause', 'UNKNOWN')}; root_scored_same_day_rows={s.get('root_scored_same_day_rows', 'UNKNOWN')}; real_shortlist_rows={s.get('real_shortlist_rows', 'UNKNOWN')}; real_bet_rows={s.get('real_bet_rows', 'UNKNOWN')}; proxy_rows={s.get('proxy_rows', 'UNKNOWN')}")


def append_local_raw_discovery_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Local Raw Fixture Discovery", "local_raw_fixture_discovery", summary, [
        f"- overall_status: {summary.get('overall_status', 'UNKNOWN')}",
        f"- files_scanned: {summary.get('files_scanned', 'UNKNOWN')}",
        f"- accepted_rows: {summary.get('accepted_rows', 'UNKNOWN')}",
        f"- rejected_rows: {summary.get('rejected_rows', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "overall_status", lambda s: f"files_scanned={s.get('files_scanned', 'UNKNOWN')}; accepted_rows={s.get('accepted_rows', 'UNKNOWN')}; rejected_rows={s.get('rejected_rows', 'UNKNOWN')}")


def append_raw_trust_gate_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Raw Candidate Trust Gate", "raw_candidate_trust_gate", summary, [
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- trusted_rows: {summary.get('trusted_rows', 'UNKNOWN')}",
        f"- quarantine_rows: {summary.get('quarantine_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- trust_status_counts: {summary.get('trust_status_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "trust_status_counts", lambda s: f"rows_reviewed={s.get('rows_reviewed', 'UNKNOWN')}; trusted_rows={s.get('trusted_rows', 'UNKNOWN')}; blocked_rows={s.get('blocked_rows', 'UNKNOWN')}; quarantine_rows={s.get('quarantine_rows', 'UNKNOWN')}")


def append_raw_promotion_gate_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Trusted Raw Candidate Promotion Gate", "trusted_raw_candidate_promotion_gate", summary, [
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- promoted_rows: {summary.get('promoted_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- quarantine_rows: {summary.get('quarantine_rows', 'UNKNOWN')}",
        f"- promotion_status_counts: {summary.get('promotion_status_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "promotion_status_counts", lambda s: f"rows_reviewed={s.get('rows_reviewed', 'UNKNOWN')}; promoted_rows={s.get('promoted_rows', 'UNKNOWN')}; blocked_rows={s.get('blocked_rows', 'UNKNOWN')}; quarantine_rows={s.get('quarantine_rows', 'UNKNOWN')}")


def append_scoring_gap_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Scoring Gap Explainer", "scoring_gap_explainer", summary, [
        f"- rows_reviewed: {summary.get('rows_reviewed', 'UNKNOWN')}",
        f"- missing_scored_rows: {summary.get('missing_scored_rows', 'UNKNOWN')}",
        f"- no_data_blocked_rows: {summary.get('no_data_blocked_rows', 'UNKNOWN')}",
        f"- not_trusted_rows: {summary.get('not_trusted_rows', 'UNKNOWN')}",
        f"- promoted_rows: {summary.get('promoted_rows', 'UNKNOWN')}",
        f"- gap_status_counts: {summary.get('gap_status_counts', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "gap_status_counts", lambda s: f"missing_scored_rows={s.get('missing_scored_rows', 'UNKNOWN')}; no_data_blocked_rows={s.get('no_data_blocked_rows', 'UNKNOWN')}; not_trusted_rows={s.get('not_trusted_rows', 'UNKNOWN')}; promoted_rows={s.get('promoted_rows', 'UNKNOWN')}")


def append_scoring_queue_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Trusted Raw Scoring Queue", "trusted_raw_scoring_queue", summary, [
        f"- queue_rows: {summary.get('queue_rows', 'UNKNOWN')}",
        f"- priority_counts: {summary.get('priority_counts', 'UNKNOWN')}",
        f"- scoring_needed_counts: {summary.get('scoring_needed_counts', 'UNKNOWN')}",
        f"- source_gap_status: {summary.get('source_gap_status', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "priority_counts", lambda s: f"queue_rows={s.get('queue_rows', 'UNKNOWN')}; priority_counts={s.get('priority_counts', 'UNKNOWN')}; scoring_needed_counts={s.get('scoring_needed_counts', 'UNKNOWN')}")


def append_enrichment_dry_run_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Queue-to-Enrichment Dry Run Planner", "queue_to_enrichment_dry_run", summary, [
        f"- rows_planned: {summary.get('rows_planned', 'UNKNOWN')}",
        f"- dry_run_decision_counts: {summary.get('dry_run_decision_counts', 'UNKNOWN')}",
        f"- risk_label_counts: {summary.get('risk_label_counts', 'UNKNOWN')}",
        f"- priority_counts: {summary.get('priority_counts', 'UNKNOWN')}",
        f"- total_estimated_call_units: {summary.get('total_estimated_call_units', 'UNKNOWN')}",
        f"- api_calls_planned: {summary.get('api_calls_planned', 'UNKNOWN')}",
        f"- api_calls_executed: {summary.get('api_calls_executed', 'UNKNOWN')}",
        f"- next_action: {summary.get('next_action', 'UNKNOWN')}",
    ], "dry_run_decision_counts", lambda s: f"rows_planned={s.get('rows_planned', 'UNKNOWN')}; risk_label_counts={s.get('risk_label_counts', 'UNKNOWN')}; estimated_units={s.get('total_estimated_call_units', 'UNKNOWN')}; api_calls_executed={s.get('api_calls_executed', 'UNKNOWN')}")


def append_enrichment_approval_gate_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Enrichment Cost & Approval Gate", "enrichment_cost_approval_gate", summary, [
        f"- approval_gate_status: {summary.get('approval_gate_status', 'UNKNOWN')}",
        f"- rows_planned: {summary.get('rows_planned', 'UNKNOWN')}",
        f"- estimated_call_units: {summary.get('estimated_call_units', 'UNKNOWN')}",
        f"- approval_required: {summary.get('approval_required', 'UNKNOWN')}",
        f"- max_allowed_without_manual_approval: {summary.get('max_allowed_without_manual_approval', 'UNKNOWN')}",
        f"- api_calls_allowed: {summary.get('api_calls_allowed', 'UNKNOWN')}",
        f"- api_calls_planned: {summary.get('api_calls_planned', 'UNKNOWN')}",
        f"- api_calls_executed: {summary.get('api_calls_executed', 'UNKNOWN')}",
        f"- recommended_action: {summary.get('recommended_action', 'UNKNOWN')}",
    ], "approval_gate_status", lambda s: f"estimated_call_units={s.get('estimated_call_units', 'UNKNOWN')}; approval_required={s.get('approval_required', 'UNKNOWN')}; api_calls_allowed={s.get('api_calls_allowed', 'UNKNOWN')}; api_calls_executed={s.get('api_calls_executed', 'UNKNOWN')}")


def append_board_self_heal_to_panel(day: str, summary: dict[str, str]) -> None:
    append_panel_section(day, "Daily Board Self-Heal", "daily_board_self_heal", summary, [
        f"- self_heal_status: {summary.get('self_heal_status', 'UNKNOWN')}",
        f"- promotion_rows_reviewed: {summary.get('promotion_rows_reviewed', 'UNKNOWN')}",
        f"- promoted_rows: {summary.get('promoted_rows', 'UNKNOWN')}",
        f"- blocked_rows: {summary.get('blocked_rows', 'UNKNOWN')}",
        f"- quarantine_rows: {summary.get('quarantine_rows', 'UNKNOWN')}",
        f"- board_rows_written: {summary.get('board_rows_written', 'UNKNOWN')}",
        f"- reason: {summary.get('reason', 'UNKNOWN')}",
    ], "self_heal_status", lambda s: f"promoted_rows={s.get('promoted_rows', 'UNKNOWN')}; board_rows_written={s.get('board_rows_written', 'UNKNOWN')}; reason={s.get('reason', 'UNKNOWN')}")


def run(day: str, tz: str) -> None:
    day = date.fromisoformat(day).isoformat()
    date_guard.run(day, tz)
    upstream_diag.run(day, tz)
    real_shortlist_diag.run(day, tz, ROOT)
    local_raw_discovery.run(day, tz, Path('.'), ROOT)
    raw_trust_gate.run(day, tz, ROOT)
    raw_promotion_gate.run(day, tz, ROOT)
    scoring_gap.run(day, tz, ROOT)
    scoring_queue.run(day, tz, ROOT)
    enrichment_dry_run.run(day, tz, ROOT)
    enrichment_approval_gate.run(day, tz, ROOT)
    board_self_heal.run(day, tz, ROOT)
    panel_v2.run(day, tz)

    date_rows = read_csv(TODAY / day / "vsigma_date_coherence_guard_summary.csv") or read_csv(GOVERNANCE / "vsigma_date_coherence_guard_summary.csv")
    upstream_rows = read_csv(TODAY / day / "vsigma_upstream_board_input_diagnostic_summary.csv") or read_csv(GOVERNANCE / "vsigma_upstream_board_input_diagnostic_summary.csv")
    real_shortlist_rows = read_csv(TODAY / day / "vsigma_real_shortlist_recovery_diagnostic_summary.csv") or read_csv(GOVERNANCE / "vsigma_real_shortlist_recovery_diagnostic_summary.csv")
    local_raw_rows = read_csv(TODAY / day / "vsigma_local_raw_fixture_discovery_summary.csv") or read_csv(GOVERNANCE / "vsigma_local_raw_fixture_discovery_summary.csv")
    trust_rows = read_csv(TODAY / day / "vsigma_raw_candidate_trust_gate_summary.csv") or read_csv(GOVERNANCE / "vsigma_raw_candidate_trust_gate_summary.csv")
    promotion_rows = read_csv(TODAY / day / "vsigma_trusted_raw_candidate_promotion_summary.csv") or read_csv(GOVERNANCE / "vsigma_trusted_raw_candidate_promotion_summary.csv")
    scoring_gap_rows = read_csv(TODAY / day / "vsigma_scoring_gap_explainer_summary.csv") or read_csv(GOVERNANCE / "vsigma_scoring_gap_explainer_summary.csv")
    scoring_queue_rows = read_csv(TODAY / day / "vsigma_trusted_raw_scoring_queue_summary.csv") or read_csv(GOVERNANCE / "vsigma_trusted_raw_scoring_queue_summary.csv")
    enrichment_rows = read_csv(TODAY / day / "vsigma_queue_to_enrichment_dry_run_summary.csv") or read_csv(GOVERNANCE / "vsigma_queue_to_enrichment_dry_run_summary.csv")
    approval_rows = read_csv(TODAY / day / "vsigma_enrichment_cost_approval_gate_summary.csv") or read_csv(GOVERNANCE / "vsigma_enrichment_cost_approval_gate_summary.csv")
    self_heal_rows = read_csv(TODAY / day / "vsigma_daily_board_self_heal_summary.csv") or read_csv(GOVERNANCE / "vsigma_daily_board_self_heal_summary.csv")
    if date_rows:
        append_date_guard_to_panel(day, date_rows[0])
    if upstream_rows:
        append_upstream_diag_to_panel(day, upstream_rows[0])
    if real_shortlist_rows:
        append_real_shortlist_diag_to_panel(day, real_shortlist_rows[0])
    if local_raw_rows:
        append_local_raw_discovery_to_panel(day, local_raw_rows[0])
    if trust_rows:
        append_raw_trust_gate_to_panel(day, trust_rows[0])
    if promotion_rows:
        append_raw_promotion_gate_to_panel(day, promotion_rows[0])
    if scoring_gap_rows:
        append_scoring_gap_to_panel(day, scoring_gap_rows[0])
    if scoring_queue_rows:
        append_scoring_queue_to_panel(day, scoring_queue_rows[0])
    if enrichment_rows:
        append_enrichment_dry_run_to_panel(day, enrichment_rows[0])
    if approval_rows:
        append_enrichment_approval_gate_to_panel(day, approval_rows[0])
    if self_heal_rows:
        append_board_self_heal_to_panel(day, self_heal_rows[0])
    print("=== VSIGMA CONSOLIDATED DAILY OPERATOR PANEL V3 ===")
    if date_rows:
        print(f"date_guard={date_rows[0].get('overall_status', 'UNKNOWN')}")
    if upstream_rows:
        print(f"upstream_diag={upstream_rows[0].get('overall_status', 'UNKNOWN')}")
    if real_shortlist_rows:
        print(f"real_shortlist_diag={real_shortlist_rows[0].get('overall_status', 'UNKNOWN')}")
    if local_raw_rows:
        print(f"local_raw={local_raw_rows[0].get('overall_status', 'UNKNOWN')}")
    if trust_rows:
        print(f"raw_trust={trust_rows[0].get('trust_status_counts', 'UNKNOWN')}")
    if promotion_rows:
        print(f"raw_promotion={promotion_rows[0].get('promotion_status_counts', 'UNKNOWN')}")
    if scoring_gap_rows:
        print(f"scoring_gap={scoring_gap_rows[0].get('gap_status_counts', 'UNKNOWN')}")
    if scoring_queue_rows:
        print(f"scoring_queue={scoring_queue_rows[0].get('priority_counts', 'UNKNOWN')}")
    if enrichment_rows:
        print(f"enrichment_dry_run={enrichment_rows[0].get('risk_label_counts', 'UNKNOWN')}")
    if approval_rows:
        print(f"approval_gate={approval_rows[0].get('approval_gate_status', 'UNKNOWN')}")
    if self_heal_rows:
        print(f"board_self_heal={self_heal_rows[0].get('self_heal_status', 'UNKNOWN')}")
    print("auto_apply=NO")
    print("production_change=NO")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--timezone", default="Atlantic/Canary")
    args = parser.parse_args()
    run(args.date, args.timezone)


if __name__ == "__main__":
    main()
