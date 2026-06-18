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


## API-Enriched Review Board
- source: data/processed/today/2026-06-18/vsigma_api_enriched_review_board.csv
- review_rows_written: 69
- ready_for_manual_review_rows: 69
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=42; P1_MANUAL_REVIEW=27
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=69
- pick_permission_counts: NO_PICK_PERMISSION=69
- stake_permission_counts: NO_STAKE_PERMISSION=69
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P1_MANUAL_REVIEW | Indy Eleven vs Brooklyn | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Indy Eleven | pred_total_home_away=71.3/28.8 | 1x2=1.64/3.80/4.50 | ou2.5=1.65/2.15
- P2_MANUAL_REVIEW | Lionsbridge vs Patuxent | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Lionsbridge | pred_total_home_away=85.7/14.3
- P2_MANUAL_REVIEW | Pittsburgh Riverhounds 2 vs Lorain County Leviathan | status=API_ENRICHED_REVIEW_READY | score=55 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Lorain County Leviathan | pred_total_home_away=40.0/60.0
- P1_MANUAL_REVIEW | Sporting Jax 2 vs Nona | status=API_ENRICHED_REVIEW_READY | score=90 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Nona | pred_total_home_away=38.2/61.8 | 1x2=5.25/3.60/1.53 | ou2.5=1.77/1.83
- P2_MANUAL_REVIEW | Tobacco Road vs Appalachian | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Appalachian | pred_total_home_away=28.3/71.8
- P2_MANUAL_REVIEW | Virginia Beach City vs Bethesda SC | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Virginia Beach City | pred_total_home_away=70.4/29.6
- P2_MANUAL_REVIEW | Virginia Marauders vs Charlottesville Blues | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Charlottesville Blues | pred_total_home_away=19.2/80.8
- P2_MANUAL_REVIEW | Jackson Boom vs Red River | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Red River | pred_total_home_away=32.5/67.5
- P2_MANUAL_REVIEW | Rockford Raptors vs Sueno | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Sueno | pred_total_home_away=28.6/71.4
- P2_MANUAL_REVIEW | Weston vs FC Miami City | status=API_ENRICHED_REVIEW_READY | score=64 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Weston | pred_total_home_away=63.2/37.0

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-18/official_lineup_sources.csv: rows=50
- data/processed/today/2026-06-18/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=50
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-18/official_lineup_sources.csv: rows=50
- data/processed/today/2026-06-18/vsigma_probable_lineup_consensus.csv: rows=1
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
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 1
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1944
- accepted_rows: 129
- rejected_rows: 14
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 129
- trusted_rows: 121
- quarantine_rows: 8
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=121; QUARANTINE_REVIEW=8
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 129
- promoted_rows: 0
- blocked_rows: 1
- quarantine_rows: 120
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=120; NOT_TRUSTED_NO_PROMOTION=8; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=1
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 129
- missing_scored_rows: 120
- no_data_blocked_rows: 1
- not_trusted_rows: 8
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=120; NOT_TRUSTED_SKIPPED=8; SCORED_ROW_NO_DATA_BLOCKED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 120
- priority_counts: P1_TRUSTED_MISSING_SCORING=120
- scoring_needed_counts: YES=120
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 120
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=120
- risk_label_counts: MEDIUM=120
- priority_counts: P1_TRUSTED_MISSING_SCORING=120
- total_estimated_call_units: 600
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 120
- estimated_call_units: 600
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
- rows_reviewed: 120
- p1_rows: 120
- p2_rows: 0
- p1_estimated_units: 600
- p2_estimated_units: 0
- auto_units_reserved: 600
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=120
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: REVIEW_EMPTY_DIAGNOSTIC_BOARD
- operator_state: EMPTY_REVIEW_REQUIRED
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 120
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
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 120
- rows_allowed: 120
- full_scoring_enrichment_rows: 86
- coverage_probe_rows: 0
- diagnostic_only_rows: 34
- blocked_rows: 0
- estimated_call_units: 600
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=86; DIAGNOSTIC_ONLY_NO_SCORING=34
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 86
- coverage_probe_rows: 0
- diagnostic_only_rows: 34
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 69
- bucket_counts: P3_REVIEW_LOW_SIGNAL=42; P1_REVIEW_STRONG_SIGNAL=27
- risk_label_counts: LOW=42; MEDIUM=27
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=69
- pick_permission_counts: NO_PICK_PERMISSION=69
- stake_permission_counts: NO_STAKE_PERMISSION=69
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 69
- api_calls_planned: 69
- api_calls_executed: 69
- finished_rows: 18
- pending_rows: 51
- refresh_status_counts: OK=69
- provider_counts: API-SPORTS_DIRECT=69
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 69
- finished_rows: 18
- pending_rows: 51
- accuracy_bucket_counts: PENDING_RESULT=51; STRONG_SIGNAL_VALIDATED=12; PARTIAL_SIGNAL_VALIDATED=5; SIGNAL_FAILED=1
- api_1x2_counts: PENDING_RESULT=51; HIT=13; MISS=5
- api_double_chance_counts: PENDING_RESULT=51; HIT=15; MISS=3
- api_dnb_counts: PENDING_RESULT=51; HIT=13; MISS=3; VOID=2
- over_1_5_counts: PENDING_RESULT=51; HIT=16; MISS=2
- over_2_5_counts: PENDING_RESULT=51; HIT=13; MISS=5
- under_3_5_counts: PENDING_RESULT=51; MISS=9; HIT=9
- btts_counts: PENDING_RESULT=51; MISS=10; HIT=8
- pick_permission_counts: NO_PICK_PERMISSION=69
- stake_permission_counts: NO_STAKE_PERMISSION=69
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 271
- finished_rows: 127
- pending_rows: 144
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=82.9 | evaluated=35
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=82.9 | evaluated=35
- sample_warning_counts: MEDIUM_SAMPLE_UNDER_100=35; LOW_SAMPLE_UNDER_50=28; SAMPLE_OK_100_PLUS=7; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=22; CALIBRATION_WEAK_OR_NEGATIVE=16; CALIBRATION_MEDIUM_OBSERVED_EDGE=15; CALIBRATION_STRONG_OBSERVED_EDGE=8; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_STRONG_PROTECTED_MARKET=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 22
- block_rows: 25
- observe_rows: 30
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=25; RULE_OBSERVE_ONLY_SEGMENT=20; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_TOTAL_MARKET=6; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=6; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=6; RULE_CANDIDATE_PROTECTED_MARKET=4; RULE_NEUTRAL_OBSERVE_MORE=3
- rule_decision_counts: OBSERVE_MORE_SEGMENT=20; WATCH_ONLY_COLLECT_TO_50_SAMPLE=12; BLOCK_BTTS_YES_PROMOTION=10; FUTURE_RULE_REVIEW_ONLY=10; BLOCK_ML_PROMOTION=9; COLLECT_MORE_SAMPLE=7; BLOCK_OVER_2_5_PROMOTION=6; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=25; NO_SEGMENT_SAMPLE_TOO_SMALL=20; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=12; YES_REVIEW_ONLY=10; NO_SAMPLE_TOO_SMALL=7; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
