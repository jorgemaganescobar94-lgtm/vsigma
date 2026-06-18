# vSIGMA Consolidated Daily Operator Panel - 2026-06-18

## First Read
- panel_status: NONE
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=ATTENTION; board_rows=1
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=1
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: ATTENTION
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
- #1 | NO_BET | AC Oulu vs Mariehamn | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=1
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=1
- execution_permission_counts: NO=1
- avg_coverage_score: 20.0
- forecast_warning_counts: PARTIAL_RECENT_STATS=1; SHOT_SAMPLE_WEAK=1; CORNER_SAMPLE_WEAK=1; CARD_SAMPLE_WEAK=1
- missing_data_counts: recent_stats_coverage=NONE=1; lineup_coverage=NONE=1; injuries_coverage=NONE=1; standings_coverage=NONE=1; odds_coverage=NONE=1

## Official / Probable Lineups
- data/processed/today/2026-06-18/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=48
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-18/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=48
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=6; WARN=1; INFO=4
- status_counts: OK=6; MISSING=1; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-18; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-18T12:36:00+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-18; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-18T12:36:00+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-18; reason=normalize_prelock_recheck_date; triggered_at=2026-06-18T12:36:00+01:00

## Key Files
- data/processed/today/2026-06-18/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-18/vsigma_operator_brief.md
- data/processed/today/2026-06-18/vsigma_daily_execution_board.md
- data/processed/today/2026-06-18/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-18/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-18/vsigma_automation_health.md
- data/processed/today/2026-06-18/vsigma_probable_lineup_source_reliability_governor.md

## Guardrails
- Panel is diagnostic only; it does not execute bets.
- auto_apply=NO and production_change=NO are hardcoded.
- No Bet, Watch, Live Only, Learning Only and Quarantine are valid successful outcomes.
- Source Reliability Governor remains advisory-only and cannot change weights by itself.
- If the daily board is missing, prelock/live files cannot be used as pick permission.

## Date Coherence Guard
- overall_status: OK
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- missing_core_count: 0
- trigger_date_counts: 2026-06-18=2
- next_action: All dated artifacts/triggers reviewed by guard are coherent.

## Upstream Board Input Diagnostic
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: real_objective_context_gate
- missing_required_count: 2
- empty_required_count: 3
- date_issue_count: 0
- forecast_rows: 1
- translator_rows: 1
- board_rows: 1
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
- files_scanned: 1953
- accepted_rows: 132
- rejected_rows: 800
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 132
- trusted_rows: 121
- quarantine_rows: 8
- blocked_rows: 3
- trust_status_counts: TRUSTED_RAW_SOURCE=121; QUARANTINE_REVIEW=8; REJECTED_SOURCE_BLOCK=3
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 132
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 121
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=121; NOT_TRUSTED_NO_PROMOTION=11
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 132
- missing_scored_rows: 121
- no_data_blocked_rows: 0
- not_trusted_rows: 11
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=121; NOT_TRUSTED_SKIPPED=11
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 121
- priority_counts: P1_TRUSTED_MISSING_SCORING=106; P2_LOW_COVERAGE_SCORING=15
- scoring_needed_counts: YES=121
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 121
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=121
- risk_label_counts: MEDIUM=104; HIGH_LOW_COVERAGE=15; HIGH_CONTEXT_VOLATILITY=2
- priority_counts: P1_TRUSTED_MISSING_SCORING=106; P2_LOW_COVERAGE_SCORING=15
- total_estimated_call_units: 592
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 121
- estimated_call_units: 592
- approval_required: YES
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: WAIT_FOR_MANUAL_APPROVAL

## Daily Board Self-Heal
- self_heal_status: NO_ACTION
- promotion_rows_reviewed: 0
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- board_rows_written: 0
- reason: daily board already has rows
## Forced API Board Fixture Lineups Refresh
- fixtures_reviewed: 1
- api_calls_executed: 1
- lineup_fixtures_found: 1
- lineup_fixtures_missing: 0
- starting_xi_rows: 22
- substitute_rows: 14
- api_status_counts: OK=36
- pick_permission: NO_PICK_PERMISSION
- stake_permission: NO_STAKE_PERMISSION
- next_action: Use direct board fixture_id API lineups as a prelock input only. No automatic pick or stake permission.
