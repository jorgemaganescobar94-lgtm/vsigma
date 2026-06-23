# vSIGMA Consolidated Daily Operator Panel - 2026-06-23

## First Read
- panel_status: NONE
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=UNKNOWN; board_rows=1
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=1
- health_status: MISSING
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: UNKNOWN
- board_rows: 1
- panel_status: NONE
- next_action: Follow operator brief and panel categories; no automatic execution.

## Executable Prematch
- none

## Live Only
- none

## Watchlist
- none

## No Bet
- #0 | NO_BET | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | market=NO_MARKET | stake=NO_STAKE | permission=NO_BET | score=0

## API Coverage
- board_rows=1
- source_guard_counts: PROMOTION_GATE_DIAGNOSTIC_ONLY=1
- execution_permission_counts: NO_BET=1
- avg_coverage_score: UNKNOWN
- forecast_warning_counts: no promoted raw candidates=1
- missing_data_counts: none

## Official / Probable Lineups
- data/processed/governance/official_lineup_sources.csv: rows=62
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/governance/official_lineup_sources.csv: rows=62
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: MISSING
- components_checked: UNKNOWN
- severity_counts: UNKNOWN
- status_counts: UNKNOWN

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-21; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-21T16:27:52+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-21; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-21T16:27:52+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-21; reason=normalize_prelock_recheck_date; triggered_at=2026-06-21T16:27:52+01:00

## Key Files
- data/processed/today/2026-06-23/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-23/vsigma_operator_brief.md
- data/processed/today/2026-06-23/vsigma_daily_execution_board.md
- data/processed/today/2026-06-23/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-23/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-23/vsigma_automation_health.md
- data/processed/today/2026-06-23/vsigma_probable_lineup_source_reliability_governor.md

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
- missing_core_count: 3
- trigger_date_counts: 2026-06-21=2
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
- overall_status: SCORING_SOURCE_EMPTY_FOR_DATE
- root_cause: scored source exists but has no rows for target date
- root_scored_same_day_rows: 0
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Refresh/fix scoring source date coverage.

## Local Raw Fixture Discovery
- overall_status: NO_LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 2118
- accepted_rows: 0
- rejected_rows: 0
- next_action: No local source can build raw candidates; upstream fetch/filter producer is still required.

## Raw Candidate Trust Gate
- rows_reviewed: 0
- trusted_rows: 0
- quarantine_rows: 0
- blocked_rows: 0
- trust_status_counts: none
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 0
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- promotion_status_counts: none
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 0
- missing_scored_rows: 0
- no_data_blocked_rows: 0
- not_trusted_rows: 0
- promoted_rows: 0
- gap_status_counts: none
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
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 0
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
