# vSIGMA Consolidated Daily Operator Panel - 2026-06-10

## First Read
- panel_status: WATCH
- operator_detail: action=WATCH; final=WATCH_ONLY_NO_STAKE; risk=LOW_ALERT; health=ATTENTION; board_rows=2
- executable_prematch: NONE
- live_only: ROWS=1
- watchlist: NONE
- no_bet: ROWS=1
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: WATCH
- compact_final_decision: WATCH_ONLY_NO_STAKE
- risk_label: LOW_ALERT
- health_status: ATTENTION
- board_rows: 2
- panel_status: WATCH
- next_action: Follow operator brief and panel categories; no automatic execution.

## Executable Prematch
- none

## Live Only
- #1 | LIVE_ONLY | Malaga vs Las Palmas | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | permission=NO_PREMATCH | conf=MEDIUM | score=17

## Watchlist
- none

## No Bet
- #2 | NO_BET | Cape Town City vs Magesi | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=2
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=2
- execution_permission_counts: NO_PREMATCH=1; NO=1
- avg_coverage_score: 50.0
- forecast_warning_counts: LINEUPS_INACTIVE=1; API_EARLY_LOW_SUPPORT=1; PARTIAL_RECENT_STATS=1; SHOT_SAMPLE_WEAK=1; CORNER_SAMPLE_WEAK=1; CARD_SAMPLE_WEAK=1
- missing_data_counts: lineup_coverage=NOT_DUE_YET=1; injuries_coverage=NONE=2; recent_stats_coverage=NONE=1; lineup_coverage=NONE=1; standings_coverage=NONE=1; odds_coverage=NONE=1

## Official / Probable Lineups
- data/processed/today/2026-06-10/vsigma_probable_lineup_consensus.csv: rows=2
- data/processed/governance/official_lineup_sources.csv: rows=38
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-10/vsigma_probable_lineup_consensus.csv: rows=2
- data/processed/governance/official_lineup_sources.csv: rows=38
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: ATTENTION
- components_checked: 11
- severity_counts: WARN=2; OK=5; INFO=4
- status_counts: OK=7; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-10; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-10T19:13:01+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-10; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-10T19:13:01+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-10; reason=normalize_prelock_recheck_date; triggered_at=2026-06-10T19:13:01+01:00

## Key Files
- data/processed/today/2026-06-10/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-10/vsigma_operator_brief.md
- data/processed/today/2026-06-10/vsigma_daily_execution_board.md
- data/processed/today/2026-06-10/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-10/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-10/vsigma_automation_health.md
- data/processed/today/2026-06-10/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-10=2
- next_action: All dated artifacts/triggers reviewed by guard are coherent.

## Upstream Board Input Diagnostic
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: context_matrix
- missing_required_count: 2
- empty_required_count: 0
- date_issue_count: 0
- forecast_rows: 2
- translator_rows: 2
- board_rows: 2
- next_action: Build missing required upstream component first: context_matrix.

## Real Shortlist Recovery Diagnostic
- overall_status: REAL_CANDIDATES_AVAILABLE
- root_cause: real shortlist or bets rows exist
- root_scored_same_day_rows: 1
- real_shortlist_rows: 2
- real_bet_rows: 1
- proxy_rows: 0
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1625
- accepted_rows: 122
- rejected_rows: 668
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 122
- trusted_rows: 95
- quarantine_rows: 27
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=95; QUARANTINE_REVIEW=27
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 122
- promoted_rows: 1
- blocked_rows: 0
- quarantine_rows: 94
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=94; NOT_TRUSTED_NO_PROMOTION=27; PROMOTED_TO_SCORING_INPUT=1
- next_action: Promoted rows may feed normal scoring gates only.

## Scoring Gap Explainer
- rows_reviewed: 122
- missing_scored_rows: 94
- no_data_blocked_rows: 0
- not_trusted_rows: 27
- promoted_rows: 1
- gap_status_counts: MISSING_SCORED_ROW=94; NOT_TRUSTED_SKIPPED=27; PROMOTED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 94
- priority_counts: P1_TRUSTED_MISSING_SCORING=80; P2_LOW_COVERAGE_SCORING=14
- scoring_needed_counts: YES=94
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 94
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=94
- risk_label_counts: MEDIUM=60; HIGH_CONTEXT_VOLATILITY=20; HIGH_LOW_COVERAGE=14
- priority_counts: P1_TRUSTED_MISSING_SCORING=80; P2_LOW_COVERAGE_SCORING=14
- total_estimated_call_units: 480
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 94
- estimated_call_units: 480
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
## API Shadow Rule Outcome Ledger
- candidate_rules_applied: 10
- shadow_rows: 242
- finished_shadow_rows: 92
- pending_shadow_rows: 150
- shadow_outcome_counts: PENDING_RESULT=150; HIT=60; MISS=20; VOID=12
- rule_market_counts: API_DNB=96; API_DOUBLE_CHANCE=96; OVER_1_5=32; UNDER_3_5=18
- paper_trade_permission_counts: SHADOW_ONLY=242
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=242
- pick_permission_counts: NO_PICK_PERMISSION=242
- stake_permission_counts: NO_STAKE_PERMISSION=242
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
## API Shadow Rule Out-of-Sample Tracker
- registry_rules: 11
- rows_reviewed: 242
- in_sample_rows: 53
- out_of_sample_rows: 39
- pending_rows: 150
- oos_evaluated_rows: 39
- oos_class_counts: PENDING_RESULT=150; IN_SAMPLE_BOOTSTRAP=53; OUT_OF_SAMPLE=39
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=242
- pick_permission_counts: NO_PICK_PERMISSION=242
- stake_permission_counts: NO_STAKE_PERMISSION=242
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
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
