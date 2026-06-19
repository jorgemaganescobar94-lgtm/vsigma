# vSIGMA Consolidated Daily Operator Panel - 2026-06-19

## First Read
- panel_status: BROKEN
- operator_detail: action=BROKEN; final=SYSTEM_FIX_REQUIRED; risk=HIGH; health=BROKEN; board_rows=1
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=1
- health_status: BROKEN
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: BROKEN
- compact_final_decision: SYSTEM_FIX_REQUIRED
- risk_label: HIGH
- health_status: BROKEN
- board_rows: 1
- panel_status: BROKEN
- next_action: Fix workflow/input before market discussion.

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
- data/processed/governance/official_lineup_sources.csv: rows=50
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/governance/official_lineup_sources.csv: rows=50
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-18; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-18T17:45:48+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-18; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-18T17:45:48+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-18; reason=normalize_prelock_recheck_date; triggered_at=2026-06-18T17:45:48+01:00

## Key Files
- data/processed/today/2026-06-19/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-19/vsigma_operator_brief.md
- data/processed/today/2026-06-19/vsigma_daily_execution_board.md
- data/processed/today/2026-06-19/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-19/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-19/vsigma_automation_health.md
- data/processed/today/2026-06-19/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-18=2
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
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1998
- accepted_rows: 107
- rejected_rows: 3
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 107
- trusted_rows: 103
- quarantine_rows: 4
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=103; QUARANTINE_REVIEW=4
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 107
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 103
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=103; NOT_TRUSTED_NO_PROMOTION=4
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 107
- missing_scored_rows: 103
- no_data_blocked_rows: 0
- not_trusted_rows: 4
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=103; NOT_TRUSTED_SKIPPED=4
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 103
- priority_counts: P1_TRUSTED_MISSING_SCORING=103
- scoring_needed_counts: YES=103
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 103
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=103
- risk_label_counts: MEDIUM=103
- priority_counts: P1_TRUSTED_MISSING_SCORING=103
- total_estimated_call_units: 515
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 103
- estimated_call_units: 515
- approval_required: YES
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: WAIT_FOR_MANUAL_APPROVAL

## Daily Board Self-Heal
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 107
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 103
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
