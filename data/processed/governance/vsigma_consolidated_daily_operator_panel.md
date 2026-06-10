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


## API-Enriched Review Board
- source: data/processed/today/2026-06-10/vsigma_api_enriched_review_board.csv
- review_rows_written: 32
- ready_for_manual_review_rows: 32
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=23; P1_MANUAL_REVIEW=9
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=32
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P1_MANUAL_REVIEW | Neptūną Klaipėda vs Transinvest 2 | status=API_ENRICHED_REVIEW_READY | score=90 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Neptūną Klaipėda | pred_total_home_away=71.0/29.0 | 1x2=1.15/5.75/13.00
- P2_MANUAL_REVIEW | Fjardabyggd / Leiknir vs Fjolnir | status=API_ENRICHED_REVIEW_READY | score=61 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Fjardabyggd / Leiknir | pred_total_home_away=55.5/44.5 | 1x2=2.25/3.95/2.38
- P1_MANUAL_REVIEW | Haukar vs Kormákur / Hvöt | status=API_ENRICHED_REVIEW_READY | score=84 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Haukar | pred_total_home_away=63.2/36.8 | 1x2=1.44/4.33/5.40
- P2_MANUAL_REVIEW | Thróttur Vogar vs Vikingur Olafsiik | status=API_ENRICHED_REVIEW_READY | score=71 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Thróttur Vogar | pred_total_home_away=58.8/41.2 | 1x2=1.73/3.90/3.55
- P1_MANUAL_REVIEW | Damash Gilanian vs Mes Shahr-e Babak | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Mes Shahr-e Babak | pred_total_home_away=29.3/70.7 | 1x2=6.00/3.30/1.55 | ou2.5=2.50/1.50
- P2_MANUAL_REVIEW | Naft Bandar Abbas vs Shahrdari Noshahr | status=API_ENRICHED_REVIEW_READY | score=61 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Naft Bandar Abbas | pred_total_home_away=48.0/52.2 | 1x2=2.32/2.75/3.40 | ou2.5=2.67/1.36
- P2_MANUAL_REVIEW | Blumenau vs Jaraguá | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Blumenau | pred_total_home_away=89.7/10.3
- P2_MANUAL_REVIEW | Dikaki vs Cercle Mbéri | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Cercle Mbéri | pred_total_home_away=27.4/72.6
- P2_MANUAL_REVIEW | Mangasport vs Bouenguidi | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Mangasport | pred_total_home_away=75.3/24.7
- P2_MANUAL_REVIEW | Stade Mandji vs Lozo | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Stade Mandji | pred_total_home_away=66.4/34.0

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-10/official_lineup_sources.csv: rows=40
- data/processed/today/2026-06-10/vsigma_probable_lineup_consensus.csv: rows=2
- data/processed/governance/official_lineup_sources.csv: rows=40
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-10/official_lineup_sources.csv: rows=40
- data/processed/today/2026-06-10/vsigma_probable_lineup_consensus.csv: rows=2
- data/processed/governance/official_lineup_sources.csv: rows=40
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
- root_scored_same_day_rows: 2
- real_shortlist_rows: 2
- real_bet_rows: 1
- proxy_rows: 0
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1630
- accepted_rows: 122
- rejected_rows: 429
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
- blocked_rows: 1
- quarantine_rows: 93
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=93; NOT_TRUSTED_NO_PROMOTION=27; PROMOTED_TO_SCORING_INPUT=1; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=1
- next_action: Promoted rows may feed normal scoring gates only.

## Scoring Gap Explainer
- rows_reviewed: 122
- missing_scored_rows: 93
- no_data_blocked_rows: 1
- not_trusted_rows: 27
- promoted_rows: 1
- gap_status_counts: MISSING_SCORED_ROW=93; NOT_TRUSTED_SKIPPED=27; PROMOTED=1; SCORED_ROW_NO_DATA_BLOCKED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 93
- priority_counts: P1_TRUSTED_MISSING_SCORING=79; P2_LOW_COVERAGE_SCORING=14
- scoring_needed_counts: YES=93
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 93
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=93
- risk_label_counts: MEDIUM=59; HIGH_CONTEXT_VOLATILITY=20; HIGH_LOW_COVERAGE=14
- priority_counts: P1_TRUSTED_MISSING_SCORING=79; P2_LOW_COVERAGE_SCORING=14
- total_estimated_call_units: 475
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 93
- estimated_call_units: 475
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
- rows_reviewed: 93
- p1_rows: 79
- p2_rows: 14
- p1_estimated_units: 415
- p2_estimated_units: 60
- auto_units_reserved: 309
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=59; MANUAL_REVIEW_REQUIRED=20; COVERAGE_PROBE_ALLOWED_P2=14
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: NOT_EMPTY_OR_NOT_APPLICABLE
- operator_state: NORMAL_PIPELINE_REVIEW
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 1
- queue_rows: 93
- diagnostic_no_bet_rows: 0
- next_action: Continue normal panel interpretation.
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
- rows_reviewed: 93
- rows_allowed: 93
- full_scoring_enrichment_rows: 55
- coverage_probe_rows: 12
- diagnostic_only_rows: 26
- blocked_rows: 0
- estimated_call_units: 475
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=55; DIAGNOSTIC_ONLY_NO_SCORING=26; COVERAGE_GATE_ONLY=12
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 55
- coverage_probe_rows: 12
- diagnostic_only_rows: 26
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 32
- bucket_counts: P3_REVIEW_LOW_SIGNAL=23; P1_REVIEW_STRONG_SIGNAL=9
- risk_label_counts: LOW=23; MEDIUM=9
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=32
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 32
- api_calls_planned: 32
- api_calls_executed: 32
- finished_rows: 13
- pending_rows: 19
- refresh_status_counts: OK=32
- provider_counts: API-SPORTS_DIRECT=32
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 32
- finished_rows: 13
- pending_rows: 19
- accuracy_bucket_counts: PENDING_RESULT=19; STRONG_SIGNAL_VALIDATED=5; SIGNAL_FAILED=5; PARTIAL_SIGNAL_VALIDATED=3
- api_1x2_counts: PENDING_RESULT=19; MISS=7; HIT=6
- api_double_chance_counts: PENDING_RESULT=19; HIT=10; MISS=3
- api_dnb_counts: PENDING_RESULT=19; HIT=6; VOID=4; MISS=3
- over_1_5_counts: PENDING_RESULT=19; HIT=8; MISS=5
- over_2_5_counts: PENDING_RESULT=19; HIT=7; MISS=6
- under_3_5_counts: PENDING_RESULT=19; HIT=7; MISS=6
- btts_counts: PENDING_RESULT=19; MISS=8; HIT=5
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 61
- finished_rows: 40
- pending_rows: 21
- summary_rows: 77
- top_market_by_hit_rate: ALL=ALL | API_DOUBLE_CHANCE | hit_rate_pct=77.5 | evaluated=40
- top_market_by_hit_or_void_rate: ALL=ALL | API_DNB | hit_or_void_rate_pct=77.5 | evaluated=40
- sample_warning_counts: INSUFFICIENT_SAMPLE_UNDER_20=49; LOW_SAMPLE_UNDER_50=28
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=49; CALIBRATION_WEAK_OR_NEGATIVE=10; CALIBRATION_NEUTRAL=5; CALIBRATION_STRONG_OBSERVED_EDGE=5; CALIBRATION_STRONG_PROTECTED_MARKET=4; CALIBRATION_MEDIUM_OBSERVED_EDGE=4
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 10
- block_rows: 12
- observe_rows: 55
- rule_bucket_counts: RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=49; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=12; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=8; RULE_OBSERVE_ONLY_SEGMENT=5; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=2; RULE_NEUTRAL_OBSERVE_MORE=1
- rule_decision_counts: COLLECT_MORE_SAMPLE=49; WATCH_ONLY_COLLECT_TO_50_SAMPLE=10; OBSERVE_MORE_SEGMENT=5; BLOCK_ML_PROMOTION=4; BLOCK_BTTS_YES_PROMOTION=4; BLOCK_OVER_2_5_PROMOTION=4; OBSERVE_MORE_GLOBAL_MARKET=1
- future_rule_candidate_counts: NO_SAMPLE_TOO_SMALL=49; NO_BLOCKED_MARKET=12; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=10; NO_SEGMENT_SAMPLE_TOO_SMALL=5; NO_OBSERVE_MORE=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
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
