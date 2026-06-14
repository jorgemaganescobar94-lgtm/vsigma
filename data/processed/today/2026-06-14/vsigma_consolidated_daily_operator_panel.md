# vSIGMA Consolidated Daily Operator Panel - 2026-06-14

## First Read
- panel_status: PARTIAL_OUTPUTS
- operator_detail: action=BROKEN; final=SYSTEM_FIX_REQUIRED; risk=HIGH; health=BROKEN; board_rows=0
- executable_prematch: NO_BOARD
- live_only: NONE
- watchlist: NONE
- no_bet: NONE
- health_status: BROKEN
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: BROKEN
- compact_final_decision: SYSTEM_FIX_REQUIRED
- risk_label: HIGH
- health_status: BROKEN
- board_rows: 0
- panel_status: PARTIAL_OUTPUTS
- next_action: Daily execution board is missing; do not use operator/prelock/live outputs as pick permission. Run daily chain first.

## Executable Prematch
- none

## Live Only
- none

## Watchlist
- none

## No Bet
- none

## API Coverage
- no daily board rows available

## Official / Probable Lineups
- data/processed/governance/official_lineup_sources.csv: rows=42
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/governance/official_lineup_sources.csv: rows=42
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: BROKEN
- components_checked: 11
- severity_counts: BROKEN=1; WARN=1; OK=5; INFO=4
- status_counts: MISSING=2; OK=5; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-10; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-13T16:18:14+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-10; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-13T16:18:14+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-10; reason=normalize_prelock_recheck_date; triggered_at=2026-06-13T16:18:14+01:00

## Key Files
- data/processed/today/2026-06-14/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-14/vsigma_operator_brief.md
- data/processed/today/2026-06-14/vsigma_daily_execution_board.md
- data/processed/today/2026-06-14/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-14/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-14/vsigma_automation_health.md
- data/processed/today/2026-06-14/vsigma_probable_lineup_source_reliability_governor.md

## Guardrails
- Panel is diagnostic only; it does not execute bets.
- auto_apply=NO and production_change=NO are hardcoded.
- No Bet, Watch, Live Only, Learning Only and Quarantine are valid successful outcomes.
- Source Reliability Governor remains advisory-only and cannot change weights by itself.
- If the daily board is missing, prelock/live files cannot be used as pick permission.

## Date Coherence Guard
- overall_status: DATE_MISMATCH_BLOCK
- board_status: daily_board_md=MISSING_CORE; daily_board_csv=MISSING_CORE
- mismatch_count: 2
- missing_core_count: 2
- trigger_date_counts: 2026-06-10=2
- next_action: Fix trigger/artifact date mismatch before using market signals.

## Upstream Board Input Diagnostic
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: real_objective_context_gate
- missing_required_count: 8
- empty_required_count: 0
- date_issue_count: 0
- forecast_rows: 0
- translator_rows: 0
- board_rows: 0
- next_action: Build missing required upstream component first: real_objective_context_gate.

## Real Shortlist Recovery Diagnostic
- overall_status: REAL_CANDIDATES_AVAILABLE
- root_cause: real shortlist or bets rows exist
- root_scored_same_day_rows: 13
- real_shortlist_rows: 1
- real_bet_rows: 1
- proxy_rows: 0
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1736
- accepted_rows: 410
- rejected_rows: 85
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 410
- trusted_rows: 13
- quarantine_rows: 0
- blocked_rows: 397
- trust_status_counts: REJECTED_SOURCE_BLOCK=397; TRUSTED_RAW_SOURCE=13
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 410
- promoted_rows: 1
- blocked_rows: 12
- quarantine_rows: 0
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=397; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=12; PROMOTED_TO_SCORING_INPUT=1
- next_action: Promoted rows may feed normal scoring gates only.

## Scoring Gap Explainer
- rows_reviewed: 410
- missing_scored_rows: 0
- no_data_blocked_rows: 12
- not_trusted_rows: 397
- promoted_rows: 1
- gap_status_counts: NOT_TRUSTED_SKIPPED=397; SCORED_ROW_NO_DATA_BLOCKED=12; PROMOTED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 0
- priority_counts: none
- scoring_needed_counts: none
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 0
- dry_run_decision_counts: none
- risk_label_counts: none
- priority_counts: none
- total_estimated_call_units: 0
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: NO_ENRICHMENT_NEEDED
- rows_planned: 0
- estimated_call_units: 0
- approval_required: NO
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: NO_ACTION

## Daily Board Self-Heal
- self_heal_status: NO_ACTION
- promotion_rows_reviewed: 410
- promoted_rows: 1
- blocked_rows: 12
- quarantine_rows: 0
- board_rows_written: 0
- reason: promoted rows exist; normal scoring/translator should build board
