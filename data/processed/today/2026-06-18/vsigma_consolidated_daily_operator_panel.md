# vSIGMA Consolidated Daily Operator Panel - 2026-06-18

## First Read
- panel_status: OK_EMPTY_BY_PROMOTION_GATE
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
- panel_status: OK_EMPTY_BY_PROMOTION_GATE
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


## API-Enriched Review Board
- source: data/processed/today/2026-06-18/vsigma_api_enriched_review_board.csv
- review_rows_written: 35
- ready_for_manual_review_rows: 35
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=18; P2_MANUAL_REVIEW=17
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=35
- pick_permission_counts: NO_PICK_PERMISSION=35
- stake_permission_counts: NO_STAKE_PERMISSION=35
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P1_MANUAL_REVIEW | Indy Eleven vs Brooklyn | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Indy Eleven | pred_total_home_away=71.3/28.8 | 1x2=1.64/3.80/4.50 | ou2.5=1.65/2.15
- P1_MANUAL_REVIEW | FC Tulsa vs Monterey Bay | status=API_ENRICHED_REVIEW_READY | score=97 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=FC Tulsa | pred_total_home_away=64.2/35.8 | 1x2=1.80/3.45/3.90 | ou2.5=1.80/1.93
- P2_MANUAL_REVIEW | Forward Madison vs Fort Wayne | status=API_ENRICHED_REVIEW_READY | score=66 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Forward Madison | pred_total_home_away=53.8/46.3 | 1x2=1.80/3.25/4.10 | ou2.5=2.05/1.70
- P1_MANUAL_REVIEW | Khovd Western vs Khangarid | status=API_ENRICHED_REVIEW_READY | score=96 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Khangarid | pred_total_home_away=36.3/63.8 | 1x2=23.00/9.60/1.03 | ou2.5=1.70/1.90
- P1_MANUAL_REVIEW | Khovd vs Deren | status=API_ENRICHED_REVIEW_READY | score=90 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Deren | pred_total_home_away=24.8/75.2 | 1x2=41.00/9.50/1.01
- P2_MANUAL_REVIEW | Akademiya Ontustik vs Yelimay Semey 2 | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Akademiya Ontustik | pred_total_home_away=76.0/24.0
- P2_MANUAL_REVIEW | JKT Tanzania vs Tanzania Prisons | status=API_ENRICHED_REVIEW_READY | score=64 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=JKT Tanzania | pred_total_home_away=53.0/47.0 | 1x2=2.10/3.20/3.00 | ou2.5=2.25/1.50
- P1_MANUAL_REVIEW | Pamba Jiji vs Mtibwa Sugar | status=API_ENRICHED_REVIEW_READY | score=76 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Mtibwa Sugar | pred_total_home_away=57.3/42.8 | 1x2=1.60/3.35/5.10 | ou2.5=2.00/1.65
- P1_MANUAL_REVIEW | Fountain Gate vs Young Africans | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Young Africans | pred_total_home_away=29.3/70.8 | 1x2=13.00/5.80/1.14 | ou2.5=1.67/1.95
- P2_MANUAL_REVIEW | Arys vs Kaspij Aktau 2 | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Kaspij Aktau 2 | pred_total_home_away=34.3/65.8

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-18/official_lineup_sources.csv: rows=50
- data/processed/governance/official_lineup_sources.csv: rows=50
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-18/official_lineup_sources.csv: rows=50
- data/processed/governance/official_lineup_sources.csv: rows=50
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-18; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-18T17:45:48+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-18; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-18T17:45:48+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-18; reason=normalize_prelock_recheck_date; triggered_at=2026-06-18T17:45:48+01:00

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
- empty_required_count: 6
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
- files_scanned: 1957
- accepted_rows: 131
- rejected_rows: 871
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 131
- trusted_rows: 121
- quarantine_rows: 8
- blocked_rows: 2
- trust_status_counts: TRUSTED_RAW_SOURCE=121; QUARANTINE_REVIEW=8; REJECTED_SOURCE_BLOCK=2
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 131
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 121
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=121; NOT_TRUSTED_NO_PROMOTION=10
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 131
- missing_scored_rows: 121
- no_data_blocked_rows: 0
- not_trusted_rows: 10
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=121; NOT_TRUSTED_SKIPPED=10
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
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 131
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 121
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
## API Quota-Aware Enrichment Gate
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 121
- p1_rows: 106
- p2_rows: 15
- p1_estimated_units: 532
- p2_estimated_units: 60
- auto_units_reserved: 535
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=104; COVERAGE_PROBE_ALLOWED_P2=15; MANUAL_REVIEW_REQUIRED=2
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: OK_EMPTY_BY_PROMOTION_GATE
- operator_state: HEALTHY_EMPTY_NO_ACTION
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 121
- diagnostic_no_bet_rows: 1
- next_action: No picks. System is coherent and empty because zero candidates were promoted. Wait for future data or improved trusted source coverage.
## Rejected Source Block Audit
- rows_reviewed: 2
- correct_reject_rows: 2
- manual_review_rows: 0
- whitelist_candidate_rows: 0
- audit_bucket_counts: CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=2
- review_priority_counts: P3_CORRECT_REJECT=2
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
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 121
- rows_allowed: 121
- full_scoring_enrichment_rows: 51
- coverage_probe_rows: 15
- diagnostic_only_rows: 55
- blocked_rows: 0
- estimated_call_units: 592
- downstream_use_counts: DIAGNOSTIC_ONLY_NO_SCORING=55; SCORING_ALLOWED_WITH_NORMAL_GATES=51; COVERAGE_GATE_ONLY=15
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 51
- coverage_probe_rows: 15
- diagnostic_only_rows: 55
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 35
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=18; P3_REVIEW_LOW_SIGNAL=17
- risk_label_counts: MEDIUM=18; LOW=17
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=35
- pick_permission_counts: NO_PICK_PERMISSION=35
- stake_permission_counts: NO_STAKE_PERMISSION=35
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 35
- api_calls_planned: 35
- api_calls_executed: 35
- finished_rows: 17
- pending_rows: 18
- refresh_status_counts: OK=35
- provider_counts: API-SPORTS_DIRECT=35
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 35
- finished_rows: 17
- pending_rows: 18
- accuracy_bucket_counts: PENDING_RESULT=18; PARTIAL_SIGNAL_VALIDATED=8; STRONG_SIGNAL_VALIDATED=6; SIGNAL_FAILED=3
- api_1x2_counts: PENDING_RESULT=18; MISS=11; HIT=6
- api_double_chance_counts: PENDING_RESULT=18; HIT=13; MISS=4
- api_dnb_counts: PENDING_RESULT=18; VOID=7; HIT=6; MISS=4
- over_1_5_counts: PENDING_RESULT=18; HIT=15; MISS=2
- over_2_5_counts: PENDING_RESULT=18; MISS=10; HIT=7
- under_3_5_counts: PENDING_RESULT=18; HIT=15; MISS=2
- btts_counts: PENDING_RESULT=18; HIT=11; MISS=6
- pick_permission_counts: NO_PICK_PERMISSION=35
- stake_permission_counts: NO_STAKE_PERMISSION=35
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 273
- finished_rows: 141
- pending_rows: 132
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=85.4 | evaluated=41
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=85.4 | evaluated=41
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=49; LOW_SAMPLE_UNDER_50=14; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=21; CALIBRATION_WEAK_OR_NEGATIVE=16; CALIBRATION_MEDIUM_OBSERVED_EDGE=16; CALIBRATION_STRONG_OBSERVED_EDGE=8; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=5; CALIBRATION_STRONG_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 21
- block_rows: 25
- observe_rows: 31
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=25; RULE_OBSERVE_ONLY_SEGMENT=21; RULE_CANDIDATE_TOTAL_MARKET=10; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_PROTECTED_MARKET=6; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2
- rule_decision_counts: OBSERVE_MORE_SEGMENT=21; FUTURE_RULE_REVIEW_ONLY=16; BLOCK_BTTS_YES_PROMOTION=10; BLOCK_ML_PROMOTION=9; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; WATCH_ONLY_COLLECT_TO_50_SAMPLE=5; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=25; NO_SEGMENT_SAMPLE_TOO_SMALL=21; YES_REVIEW_ONLY=16; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=5; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
## API Shadow Rule Outcome Ledger
- candidate_rules_applied: 21
- shadow_rows: 357
- finished_shadow_rows: 181
- pending_shadow_rows: 176
- shadow_outcome_counts: PENDING_RESULT=176; HIT=147; MISS=22; VOID=12
- rule_market_counts: OVER_1_5=163; API_DNB=66; API_DOUBLE_CHANCE=66; UNDER_3_5=62
- paper_trade_permission_counts: SHADOW_ONLY=357
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=357
- pick_permission_counts: NO_PICK_PERMISSION=357
- stake_permission_counts: NO_STAKE_PERMISSION=357
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
## API Shadow Rule Out-of-Sample Tracker
- registry_rules: 48
- rows_reviewed: 357
- in_sample_rows: 104
- out_of_sample_rows: 77
- pending_rows: 176
- oos_evaluated_rows: 77
- oos_class_counts: PENDING_RESULT=176; IN_SAMPLE_BOOTSTRAP=104; OUT_OF_SAMPLE=77
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=357
- pick_permission_counts: NO_PICK_PERMISSION=357
- stake_permission_counts: NO_STAKE_PERMISSION=357
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
