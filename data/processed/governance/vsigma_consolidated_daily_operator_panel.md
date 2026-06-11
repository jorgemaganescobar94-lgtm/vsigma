# vSIGMA Consolidated Daily Operator Panel - 2026-06-11

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
- severity_counts: BROKEN=1; WARN=1; OK=2; INFO=7
- status_counts: MISSING=1; OK=3; WAITING_OR_NOT_RUN=3; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-10; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-10T19:13:01+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-10; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-10T19:13:01+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-10; reason=normalize_prelock_recheck_date; triggered_at=2026-06-10T19:13:01+01:00

## Key Files
- data/processed/today/2026-06-11/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-11/vsigma_operator_brief.md
- data/processed/today/2026-06-11/vsigma_daily_execution_board.md
- data/processed/today/2026-06-11/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-11/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-11/vsigma_automation_health.md
- data/processed/today/2026-06-11/vsigma_probable_lineup_source_reliability_governor.md

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
- overall_status: SCORING_SOURCE_EMPTY_FOR_DATE
- root_cause: scored source exists but has no rows for target date
- root_scored_same_day_rows: 0
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Refresh/fix scoring source date coverage.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1616
- accepted_rows: 55
- rejected_rows: 0
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 55
- trusted_rows: 0
- quarantine_rows: 0
- blocked_rows: 55
- trust_status_counts: REJECTED_SOURCE_BLOCK=55
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 55
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=55
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 55
- missing_scored_rows: 0
- no_data_blocked_rows: 0
- not_trusted_rows: 55
- promoted_rows: 0
- gap_status_counts: NOT_TRUSTED_SKIPPED=55
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
- promotion_rows_reviewed: 55
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
## Prematch Calibration Rule Gate
- rows: 12
- candidate_rows: 0
- blocked_sample_rows: 6
- blocked_history_rows: 0
- hold_rows: 6
- next_action: No automatic rule changes; review candidates only after sample and history gates pass.

## Forced API Board Fixture Lineups Refresh
- fixtures_reviewed: 2
- api_calls_executed: 2
- lineup_fixtures_found: 2
- lineup_fixtures_missing: 0
- starting_xi_rows: 44
- substitute_rows: 42
- api_status_counts: OK=86
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- next_action: Use direct board fixture_id API lineups as a prelock input only. No automatic pick or stake permission.
## Forced API Lineup Bridge to Board
- board_rows_reviewed: 2
- lineup_confirmed_rows: 2
- lineup_missing_rows: 0
- board_rows_written: 2
- bridge_status_counts: LINEUPS_CONFIRMED_BY_FORCED_API=2
- bridge_action_counts: CLEAR_LINEUPS_INACTIVE_WARNING_KEEP_EXECUTION_LOCK=2
- canonical_board_permission: NO_CANONICAL_BOARD_PERMISSION
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- next_action: Use bridged copy for prelock review/repricing. Do not create picks or stake without separate governed promotion.
## Prematch Story Accuracy Ledger
- rows: 0
- finished_rows: 0
- pending_rows: 0
- result_family_counts: none
- score_neighbor_counts: none
- goal_profile_counts: none
- next_action: Track completed rows and calibrate prematch prediction families.

## Pending Prematch Prediction Finalizer
- pending_rows: 0
- api_calls: 0
- finalized_rows: 0
- still_pending_rows: 0
- next_action: Run accuracy ledger and rolling dashboard after this finalizer.
## Rolling Prematch Accuracy Dashboard
- finished_rows: 2
- pending_rows: 0
- result_family_hit_pct: 100.0
- neighbor_or_exact_pct: 100.0
- goal_profile_hit_pct: 50.0
- next_action: Use rolling accuracy to calibrate prematch prediction families.
## Prematch Prediction Calibration Advisor
- advice_rows: 12
- watch_rows: 4
- caution_rows: 2
- hold_rows: 6
- next_action: Review calibration advice only; keep auto_apply disabled until sample is large enough.
