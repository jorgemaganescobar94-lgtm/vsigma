# vSIGMA Consolidated Daily Operator Panel - 2026-06-17

## First Read
- panel_status: NONE
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=ATTENTION; board_rows=2
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=2
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: ATTENTION
- board_rows: 2
- panel_status: NONE
- next_action: Follow operator brief and panel categories; no automatic execution.

## Executable Prematch
- none

## Live Only
- none

## Watchlist
- none

## No Bet
- #1 | NO_BET | Gnistan vs Lahti | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #2 | NO_BET | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=2
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=2
- execution_permission_counts: NO=2
- avg_coverage_score: 20.0
- forecast_warning_counts: PARTIAL_RECENT_STATS=2; SHOT_SAMPLE_WEAK=2; CORNER_SAMPLE_WEAK=2; CARD_SAMPLE_WEAK=2
- missing_data_counts: recent_stats_coverage=NONE=2; lineup_coverage=NONE=2; injuries_coverage=NONE=2; standings_coverage=NONE=2; odds_coverage=NONE=2


## API-Enriched Review Board
- source: data/processed/today/2026-06-17/vsigma_api_enriched_review_board.csv
- review_rows_written: 57
- ready_for_manual_review_rows: 57
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=30; P2_MANUAL_REVIEW=27
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=57
- pick_permission_counts: NO_PICK_PERMISSION=57
- stake_permission_counts: NO_STAKE_PERMISSION=57
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P2_MANUAL_REVIEW | La Fama vs Britannia | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Britannia | pred_total_home_away=32.7/67.3
- P1_MANUAL_REVIEW | Central Stallions vs Ulaanbaatar | status=API_ENRICHED_REVIEW_READY | score=97 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Ulaanbaatar | pred_total_home_away=36.0/64.0 | 1x2=5.00/4.50/1.42 | ou2.5=1.44/2.62
- P2_MANUAL_REVIEW | Khoromkhon vs Ulaangom City | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Khoromkhon | pred_total_home_away=70.2/29.8
- P2_MANUAL_REVIEW | Simba vs Vita Club | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Vita Club | pred_total_home_away=24.2/75.8
- P2_MANUAL_REVIEW | Singida Black Stars vs Dodoma Jiji | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Singida Black Stars | pred_total_home_away=69.3/31.0
- P1_MANUAL_REVIEW | Gareji vs Shturmi | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Gareji | pred_total_home_away=65.7/34.3 | 1x2=2.15/2.90/3.20 | ou2.5=7.50/1.07
- P1_MANUAL_REVIEW | Merani Martvili vs Samtredia | status=API_ENRICHED_REVIEW_READY | score=81 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Merani Martvili | pred_total_home_away=59.0/41.2 | 1x2=1.57/3.50/4.80 | ou2.5=5.50/1.11
- P2_MANUAL_REVIEW | Don Bosco vs TP Mazembe | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=TP Mazembe | pred_total_home_away=31.2/68.8
- P2_MANUAL_REVIEW | Saint Eloi Lupopo vs Céleste | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Saint Eloi Lupopo | pred_total_home_away=70.6/29.4
- P1_MANUAL_REVIEW | Molodechno-DYuSSh 4 vs Bate Borisov | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Bate Borisov | pred_total_home_away=11.0/89.0 | 1x2=9.00/3.75/1.36 | ou2.5=1.83/1.86

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-17/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-17/vsigma_probable_lineup_consensus.csv: rows=2
- data/processed/governance/official_lineup_sources.csv: rows=44
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-17/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-17/vsigma_probable_lineup_consensus.csv: rows=2
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-17; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-17T17:47:12+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-17; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-17T17:47:12+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-17; reason=normalize_prelock_recheck_date; triggered_at=2026-06-17T17:47:12+01:00

## Key Files
- data/processed/today/2026-06-17/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-17/vsigma_operator_brief.md
- data/processed/today/2026-06-17/vsigma_daily_execution_board.md
- data/processed/today/2026-06-17/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-17/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-17/vsigma_automation_health.md
- data/processed/today/2026-06-17/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-17=2
- next_action: All dated artifacts/triggers reviewed by guard are coherent.

## Upstream Board Input Diagnostic
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: real_objective_context_gate
- missing_required_count: 2
- empty_required_count: 3
- date_issue_count: 0
- forecast_rows: 2
- translator_rows: 2
- board_rows: 2
- next_action: Build missing required upstream component first: real_objective_context_gate.

## Real Shortlist Recovery Diagnostic
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 2
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1901
- accepted_rows: 151
- rejected_rows: 857
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 151
- trusted_rows: 127
- quarantine_rows: 22
- blocked_rows: 2
- trust_status_counts: TRUSTED_RAW_SOURCE=127; QUARANTINE_REVIEW=22; REJECTED_SOURCE_BLOCK=2
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 151
- promoted_rows: 0
- blocked_rows: 2
- quarantine_rows: 125
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=125; NOT_TRUSTED_NO_PROMOTION=24; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=2
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 151
- missing_scored_rows: 125
- no_data_blocked_rows: 2
- not_trusted_rows: 24
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=125; NOT_TRUSTED_SKIPPED=24; SCORED_ROW_NO_DATA_BLOCKED=2
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 125
- priority_counts: P1_TRUSTED_MISSING_SCORING=117; P2_LOW_COVERAGE_SCORING=8
- scoring_needed_counts: YES=125
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 125
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=125
- risk_label_counts: MEDIUM=116; HIGH_LOW_COVERAGE=8; HIGH_CONTEXT_VOLATILITY=1
- priority_counts: P1_TRUSTED_MISSING_SCORING=117; P2_LOW_COVERAGE_SCORING=8
- total_estimated_call_units: 619
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 125
- estimated_call_units: 619
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
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 125
- p1_rows: 117
- p2_rows: 8
- p1_estimated_units: 586
- p2_estimated_units: 33
- auto_units_reserved: 588
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=116; COVERAGE_PROBE_ALLOWED_P2=8; MANUAL_REVIEW_REQUIRED=1
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: REVIEW_EMPTY_DIAGNOSTIC_BOARD
- operator_state: EMPTY_REVIEW_REQUIRED
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 125
- diagnostic_no_bet_rows: 0
- next_action: Review date guard and board diagnostics before market discussion.
## Rejected Source Block Audit
- rows_reviewed: 2
- correct_reject_rows: 0
- manual_review_rows: 2
- whitelist_candidate_rows: 2
- audit_bucket_counts: MANUAL_REVIEW_POSSIBLE_WHITELIST=2
- review_priority_counts: P1_REVIEW_CANDIDATE=2
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
## Manual Whitelist Review Board
- review_rows: 2
- p1_review_rows: 2
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=2
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=2
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- scoring_permission_counts: NO_SCORING_PERMISSION=2
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
## Max-Coverage API Enrichment Policy
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 125
- rows_allowed: 125
- full_scoring_enrichment_rows: 79
- coverage_probe_rows: 8
- diagnostic_only_rows: 38
- blocked_rows: 0
- estimated_call_units: 619
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=79; DIAGNOSTIC_ONLY_NO_SCORING=38; COVERAGE_GATE_ONLY=8
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 79
- coverage_probe_rows: 8
- diagnostic_only_rows: 38
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 57
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=30; P3_REVIEW_LOW_SIGNAL=27
- risk_label_counts: MEDIUM=30; LOW=27
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=57
- pick_permission_counts: NO_PICK_PERMISSION=57
- stake_permission_counts: NO_STAKE_PERMISSION=57
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 57
- api_calls_planned: 57
- api_calls_executed: 57
- finished_rows: 14
- pending_rows: 43
- refresh_status_counts: OK=57
- provider_counts: API-SPORTS_DIRECT=57
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 57
- finished_rows: 14
- pending_rows: 43
- accuracy_bucket_counts: PENDING_RESULT=43; PARTIAL_SIGNAL_VALIDATED=5; STRONG_SIGNAL_VALIDATED=5; SIGNAL_FAILED=4
- api_1x2_counts: PENDING_RESULT=43; MISS=8; HIT=6
- api_double_chance_counts: PENDING_RESULT=43; HIT=10; MISS=4
- api_dnb_counts: PENDING_RESULT=43; HIT=6; VOID=4; MISS=4
- over_1_5_counts: PENDING_RESULT=43; HIT=10; MISS=4
- over_2_5_counts: PENDING_RESULT=43; HIT=8; MISS=6
- under_3_5_counts: PENDING_RESULT=43; HIT=10; MISS=4
- btts_counts: PENDING_RESULT=43; MISS=8; HIT=6
- pick_permission_counts: NO_PICK_PERMISSION=57
- stake_permission_counts: NO_STAKE_PERMISSION=57
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 202
- finished_rows: 109
- pending_rows: 93
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=81.2 | evaluated=32
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=81.2 | evaluated=32
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; MEDIUM_SAMPLE_UNDER_100=21; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_MEDIUM_OBSERVED_EDGE=20; CALIBRATION_WEAK_OR_NEGATIVE=18; CALIBRATION_NEUTRAL=18; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=5; CALIBRATION_STRONG_OBSERVED_EDGE=5; CALIBRATION_STRONG_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 21
- block_rows: 26
- observe_rows: 30
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=26; RULE_OBSERVE_ONLY_SEGMENT=20; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=9; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=8; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET=4; RULE_NEUTRAL_OBSERVE_MORE=3
- rule_decision_counts: OBSERVE_MORE_SEGMENT=20; WATCH_ONLY_COLLECT_TO_50_SAMPLE=17; BLOCK_ML_PROMOTION=10; BLOCK_BTTS_YES_PROMOTION=8; BLOCK_OVER_2_5_PROMOTION=8; COLLECT_MORE_SAMPLE=7; FUTURE_RULE_REVIEW_ONLY=4; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=26; NO_SEGMENT_SAMPLE_TOO_SMALL=20; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=17; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY=4; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
## API Shadow Rule Outcome Ledger
- candidate_rules_applied: 21
- shadow_rows: 547
- finished_shadow_rows: 140
- pending_shadow_rows: 407
- shadow_outcome_counts: PENDING_RESULT=407; HIT=96; MISS=39; VOID=5
- rule_market_counts: OVER_1_5=264; API_DNB=96; API_DOUBLE_CHANCE=96; UNDER_3_5=91
- paper_trade_permission_counts: SHADOW_ONLY=547
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=547
- pick_permission_counts: NO_PICK_PERMISSION=547
- stake_permission_counts: NO_STAKE_PERMISSION=547
- next_action: Track shadow outcomes over future runs. This ledger cannot activate rules, picks, or stake.
## API Shadow Rule Out-of-Sample Tracker
- registry_rules: 34
- rows_reviewed: 547
- in_sample_rows: 14
- out_of_sample_rows: 126
- pending_rows: 407
- oos_evaluated_rows: 126
- oos_class_counts: PENDING_RESULT=407; OUT_OF_SAMPLE=126; IN_SAMPLE_BOOTSTRAP=14
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=547
- pick_permission_counts: NO_PICK_PERMISSION=547
- stake_permission_counts: NO_STAKE_PERMISSION=547
- next_action: Collect future OUT_OF_SAMPLE rows. No rule activation before sufficient out-of-sample sample size.
