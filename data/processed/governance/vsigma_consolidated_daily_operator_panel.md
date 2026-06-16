# vSIGMA Consolidated Daily Operator Panel - 2026-06-16

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
- #1 | NO_BET | TransINVEST Vilnius vs FK Trakai | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=1
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=1
- execution_permission_counts: NO=1
- avg_coverage_score: 15.0
- forecast_warning_counts: PARTIAL_RECENT_STATS=1; SHOT_SAMPLE_WEAK=1; CORNER_SAMPLE_WEAK=1; CARD_SAMPLE_WEAK=1
- missing_data_counts: league_coverage=PARTIAL=1; recent_stats_coverage=NONE=1; lineup_coverage=NONE=1; injuries_coverage=NONE=1; standings_coverage=NONE=1; odds_coverage=NONE=1

## Official / Probable Lineups
- data/processed/today/2026-06-16/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-16/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=44
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-16/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-16/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=44
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
- status_counts: OK=7; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-16; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-16T19:18:06+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-16; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-16T19:18:06+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-16; reason=normalize_prelock_recheck_date; triggered_at=2026-06-16T19:18:06+01:00

## Key Files
- data/processed/today/2026-06-16/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-16/vsigma_operator_brief.md
- data/processed/today/2026-06-16/vsigma_daily_execution_board.md
- data/processed/today/2026-06-16/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-16/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-16/vsigma_automation_health.md
- data/processed/today/2026-06-16/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-16=2
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
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 1
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1849
- accepted_rows: 65
- rejected_rows: 457
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 65
- trusted_rows: 54
- quarantine_rows: 11
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=54; QUARANTINE_REVIEW=11
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 65
- promoted_rows: 0
- blocked_rows: 1
- quarantine_rows: 53
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=53; NOT_TRUSTED_NO_PROMOTION=11; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=1
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 65
- missing_scored_rows: 53
- no_data_blocked_rows: 1
- not_trusted_rows: 11
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=53; NOT_TRUSTED_SKIPPED=11; SCORED_ROW_NO_DATA_BLOCKED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 53
- priority_counts: P1_TRUSTED_MISSING_SCORING=53
- scoring_needed_counts: YES=53
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 53
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=53
- risk_label_counts: MEDIUM=53
- priority_counts: P1_TRUSTED_MISSING_SCORING=53
- total_estimated_call_units: 265
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 53
- estimated_call_units: 265
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
