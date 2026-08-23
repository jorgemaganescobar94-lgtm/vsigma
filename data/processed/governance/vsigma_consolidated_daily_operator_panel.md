# vSIGMA Consolidated Daily Operator Panel - 2026-08-23

## First Read
- panel_status: NONE
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=ATTENTION; board_rows=3
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=3
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: ATTENTION
- board_rows: 3
- panel_status: NONE
- next_action: Follow operator brief and panel categories; no automatic execution.

## Executable Prematch
- none

## Live Only
- none

## Watchlist
- none

## No Bet
- #1 | NO_BET | Fenerbahçe vs Lyon | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-34
- #2 | NO_BET | Dinamo Zagreb vs Viking | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-34
- #3 | NO_BET | Independ. Rivadavia vs Fluminense | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-34

## API Coverage
- board_rows=3
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=3
- execution_permission_counts: NO=3
- avg_coverage_score: UNKNOWN
- forecast_warning_counts: LINEUPS_INACTIVE=3; LOW_LEAGUE_RELIABILITY=3; PARTIAL_RECENT_STATS=3; API_COVERAGE_UNKNOWN=3
- missing_data_counts: unknown=3

## Official / Probable Lineups
- data/processed/today/2026-08-23/official_lineup_sources.csv: rows=462
- data/processed/today/2026-08-23/vsigma_probable_lineup_consensus.csv: rows=3
- data/processed/governance/official_lineup_sources.csv: rows=462
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=27; probable_status=UNKNOWN=1; LEARNING_ONLY=7; IMPORTED=19

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-08-23/official_lineup_sources.csv: rows=462
- data/processed/today/2026-08-23/vsigma_probable_lineup_consensus.csv: rows=3
- data/processed/governance/official_lineup_sources.csv: rows=462
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=27; probable_status=UNKNOWN=1; LEARNING_ONLY=7; IMPORTED=19

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=14; LEARNING_ONLY_SOURCE=1
- sample_gate_counts: INSUFFICIENT_SAMPLE=14; MATURE_SAMPLE=1
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=14; KEEP_ACTIVE_BUT_REQUIRE_PROMOTION_GATE=1

## Automation Health
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=2; WARN=1; INFO=8
- status_counts: OK=2; MISSING=1; WAITING_OR_NOT_RUN=4; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-08-23; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-08-23T08:56:37+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-08-23; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-08-23T08:56:37+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-08-23; reason=normalize_prelock_recheck_date; triggered_at=2026-08-23T08:56:37+01:00

## Key Files
- data/processed/today/2026-08-23/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-08-23/vsigma_operator_brief.md
- data/processed/today/2026-08-23/vsigma_daily_execution_board.md
- data/processed/today/2026-08-23/vsigma_prelock_live_recheck.md
- data/processed/today/2026-08-23/vsigma_live_trigger_validator.md
- data/processed/today/2026-08-23/vsigma_automation_health.md
- data/processed/today/2026-08-23/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-08-23=2
- next_action: All dated artifacts/triggers reviewed by guard are coherent.

## Upstream Board Input Diagnostic
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: context_matrix
- missing_required_count: 2
- empty_required_count: 0
- date_issue_count: 0
- forecast_rows: 3
- translator_rows: 3
- board_rows: 3
- next_action: Build missing required upstream component first: context_matrix.

## Real Shortlist Recovery Diagnostic
- overall_status: REAL_CANDIDATES_AVAILABLE
- root_cause: real shortlist or bets rows exist
- root_scored_same_day_rows: 0
- real_shortlist_rows: 3
- real_bet_rows: 0
- proxy_rows: 9
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 4042
- accepted_rows: 3
- rejected_rows: 190
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 3
- trusted_rows: 3
- quarantine_rows: 0
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=3
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 3
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 3
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=3
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 3
- missing_scored_rows: 3
- no_data_blocked_rows: 0
- not_trusted_rows: 0
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=3
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 3
- priority_counts: P1_TRUSTED_MISSING_SCORING=3
- scoring_needed_counts: YES=3
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 3
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=3
- risk_label_counts: MEDIUM=3
- priority_counts: P1_TRUSTED_MISSING_SCORING=3
- total_estimated_call_units: 15
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 3
- estimated_call_units: 15
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
