# vSIGMA Consolidated Daily Operator Panel - 2026-08-24

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


## API-Enriched Review Board
- source: data/processed/today/2026-08-24/vsigma_api_enriched_review_board.csv
- review_rows_written: 2
- ready_for_manual_review_rows: 2
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P1_MANUAL_REVIEW | Fenerbahçe vs Lyon | status=API_ENRICHED_REVIEW_READY | score=92 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Fenerbahçe | pred_total_home_away=62.5/37.5 | 1x2=1.99/3.60/3.45 | ou2.5=1.80/2.00
- P1_MANUAL_REVIEW | Independ. Rivadavia vs Fluminense | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Independ. Rivadavia | pred_total_home_away=65.2/34.8 | 1x2=2.62/2.82/3.00 | ou2.5=7.00/1.07

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-08-24/official_lineup_sources.csv: rows=462
- data/processed/today/2026-08-24/vsigma_probable_lineup_consensus.csv: rows=3
- data/processed/governance/official_lineup_sources.csv: rows=462
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=27; probable_status=UNKNOWN=1; LEARNING_ONLY=7; IMPORTED=19

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-08-24/official_lineup_sources.csv: rows=462
- data/processed/today/2026-08-24/vsigma_probable_lineup_consensus.csv: rows=3
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-08-24; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-08-24T09:10:55+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-08-24; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-08-24T09:10:55+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-08-24; reason=normalize_prelock_recheck_date; triggered_at=2026-08-24T09:10:55+01:00

## Key Files
- data/processed/today/2026-08-24/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-08-24/vsigma_operator_brief.md
- data/processed/today/2026-08-24/vsigma_daily_execution_board.md
- data/processed/today/2026-08-24/vsigma_prelock_live_recheck.md
- data/processed/today/2026-08-24/vsigma_live_trigger_validator.md
- data/processed/today/2026-08-24/vsigma_automation_health.md
- data/processed/today/2026-08-24/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-08-24=2
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
- files_scanned: 4044
- accepted_rows: 3
- rejected_rows: 6
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
## API Quota-Aware Enrichment Gate
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 3
- p1_rows: 3
- p2_rows: 0
- p1_estimated_units: 15
- p2_estimated_units: 0
- auto_units_reserved: 15
- max_auto_units_per_day: 5000
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=3
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: REVIEW_EMPTY_DIAGNOSTIC_BOARD
- operator_state: EMPTY_REVIEW_REQUIRED
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 3
- diagnostic_no_bet_rows: 0
- next_action: Review date guard and board diagnostics before market discussion.
## Rejected Source Block Audit
- rows_reviewed: 0
- correct_reject_rows: 0
- manual_review_rows: 0
- whitelist_candidate_rows: 0
- audit_bucket_counts: none
- review_priority_counts: none
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
## Manual Whitelist Review Board
- review_rows: 0
- p1_review_rows: 0
- p2_review_rows: 0
- manual_review_status_counts: none
- risk_label_counts: none
- whitelist_permission_counts: none
- canonical_board_permission_counts: none
- scoring_permission_counts: none
- api_enrichment_permission_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
## Max-Coverage API Enrichment Policy
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 3
- rows_allowed: 3
- full_scoring_enrichment_rows: 3
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- estimated_call_units: 15
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=3
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 3
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 2
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=2
- risk_label_counts: MEDIUM=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 2
- api_calls_planned: 2
- api_calls_executed: 2
- finished_rows: 2
- pending_rows: 0
- refresh_status_counts: OK=2
- provider_counts: API-SPORTS_DIRECT=2
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 2
- finished_rows: 2
- pending_rows: 0
- accuracy_bucket_counts: PARTIAL_SIGNAL_VALIDATED=2
- api_1x2_counts: MISS=2
- api_double_chance_counts: HIT=2
- api_dnb_counts: VOID=2
- over_1_5_counts: HIT=2
- over_2_5_counts: MISS=2
- under_3_5_counts: HIT=2
- btts_counts: HIT=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 709
- finished_rows: 355
- pending_rows: 354
- summary_rows: 84
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=87.4 | evaluated=135
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=87.4 | evaluated=135
- sample_warning_counts: SAMPLE_OK_100_PLUS=63; INSUFFICIENT_SAMPLE_UNDER_20=7; MEDIUM_SAMPLE_UNDER_100=7; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_NEUTRAL=31; CALIBRATION_STRONG_OBSERVED_EDGE=16; CALIBRATION_MEDIUM_OBSERVED_EDGE=10; CALIBRATION_WEAK_OR_NEGATIVE=10; CALIBRATION_STRONG_PROTECTED_MARKET=7; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 84
- candidate_rows: 28
- block_rows: 21
- observe_rows: 35
- rule_bucket_counts: RULE_OBSERVE_ONLY_SEGMENT=26; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=21; RULE_CANDIDATE_PROTECTED_MARKET=14; RULE_CANDIDATE_TOTAL_MARKET=14; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_NEUTRAL_OBSERVE_MORE=2
- rule_decision_counts: FUTURE_RULE_REVIEW_ONLY=28; OBSERVE_MORE_SEGMENT=26; BLOCK_ML_PROMOTION=11; BLOCK_OVER_2_5_PROMOTION=7; COLLECT_MORE_SAMPLE=7; BLOCK_BTTS_YES_PROMOTION=3; OBSERVE_MORE_GLOBAL_MARKET=2
- future_rule_candidate_counts: YES_REVIEW_ONLY=28; NO_SEGMENT_SAMPLE_TOO_SMALL=26; NO_BLOCKED_MARKET=21; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=2
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=84
- pick_permission_counts: NO_PICK_PERMISSION=84
- stake_permission_counts: NO_STAKE_PERMISSION=84
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
