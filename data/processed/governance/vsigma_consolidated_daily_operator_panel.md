# vSIGMA Consolidated Daily Operator Panel - 2026-06-17

## First Read
- panel_status: NONE
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=ATTENTION; board_rows=7
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=7
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: ATTENTION
- board_rows: 7
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
- #2 | NO_BET | HJK Helsinki vs Inter Turku | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #3 | NO_BET | Ilves vs FF Jaro | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #4 | NO_BET | SJK vs VPS | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #5 | NO_BET | Turku PS vs KuPS | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #6 | NO_BET | Hegelmann Litauen vs Džiugas Telšiai | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #7 | NO_BET | Kauno Žalgiris vs Banga | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=7
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=7
- execution_permission_counts: NO=7
- avg_coverage_score: 18.6
- forecast_warning_counts: PARTIAL_RECENT_STATS=7; SHOT_SAMPLE_WEAK=7; CORNER_SAMPLE_WEAK=7; CARD_SAMPLE_WEAK=7
- missing_data_counts: recent_stats_coverage=NONE=7; lineup_coverage=NONE=7; injuries_coverage=NONE=7; standings_coverage=NONE=7; odds_coverage=NONE=7; league_coverage=PARTIAL=2


## API-Enriched Review Board
- source: data/processed/today/2026-06-17/vsigma_api_enriched_review_board.csv
- review_rows_written: 67
- ready_for_manual_review_rows: 67
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=34; P1_MANUAL_REVIEW=33
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=67
- pick_permission_counts: NO_PICK_PERMISSION=67
- stake_permission_counts: NO_STAKE_PERMISSION=67
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P2_MANUAL_REVIEW | Vermont Green vs Seacoast United Phantoms | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Vermont Green | pred_total_home_away=69.4/30.6
- P2_MANUAL_REVIEW | Eagle FC vs Lehigh Valley United | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Lehigh Valley United | pred_total_home_away=22.7/77.3
- P2_MANUAL_REVIEW | Houston Sur vs GFI | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=GFI | pred_total_home_away=21.8/78.3
- P2_MANUAL_REVIEW | La Fama vs Britannia | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Britannia | pred_total_home_away=32.7/67.3
- P1_MANUAL_REVIEW | Central Stallions vs Ulaanbaatar | status=API_ENRICHED_REVIEW_READY | score=97 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Ulaanbaatar | pred_total_home_away=36.0/64.0 | 1x2=5.00/4.50/1.42 | ou2.5=1.44/2.62
- P2_MANUAL_REVIEW | Khoromkhon vs Ulaangom City | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Khoromkhon | pred_total_home_away=70.2/29.8
- P2_MANUAL_REVIEW | Simba vs Vita Club | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Vita Club | pred_total_home_away=24.2/75.8
- P2_MANUAL_REVIEW | Arsenal Tula vs Volga Ulyanovsk | status=API_ENRICHED_REVIEW_READY | score=57 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Volga Ulyanovsk | pred_total_home_away=39.3/60.7
- P2_MANUAL_REVIEW | Singida Black Stars vs Dodoma Jiji | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Singida Black Stars | pred_total_home_away=69.3/31.0
- P1_MANUAL_REVIEW | Gareji vs Shturmi | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Gareji | pred_total_home_away=65.7/34.3 | 1x2=2.30/2.90/2.80 | ou2.5=8.00/1.06

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-17/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-17/vsigma_probable_lineup_consensus.csv: rows=7
- data/processed/governance/official_lineup_sources.csv: rows=44
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-17/official_lineup_sources.csv: rows=44
- data/processed/today/2026-06-17/vsigma_probable_lineup_consensus.csv: rows=7
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
- status_counts: OK=6; MISSING=1; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-17; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-17T13:04:55+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-17; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-17T13:04:55+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-17; reason=normalize_prelock_recheck_date; triggered_at=2026-06-17T13:04:55+01:00

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
- forecast_rows: 7
- translator_rows: 7
- board_rows: 7
- next_action: Build missing required upstream component first: real_objective_context_gate.

## Real Shortlist Recovery Diagnostic
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 7
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1892
- accepted_rows: 149
- rejected_rows: 59
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 149
- trusted_rows: 126
- quarantine_rows: 21
- blocked_rows: 2
- trust_status_counts: TRUSTED_RAW_SOURCE=126; QUARANTINE_REVIEW=21; REJECTED_SOURCE_BLOCK=2
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 149
- promoted_rows: 0
- blocked_rows: 7
- quarantine_rows: 119
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=119; NOT_TRUSTED_NO_PROMOTION=23; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=7
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 149
- missing_scored_rows: 119
- no_data_blocked_rows: 7
- not_trusted_rows: 23
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=119; NOT_TRUSTED_SKIPPED=23; SCORED_ROW_NO_DATA_BLOCKED=7
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 119
- priority_counts: P1_TRUSTED_MISSING_SCORING=119
- scoring_needed_counts: YES=119
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 119
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=119
- risk_label_counts: MEDIUM=119
- priority_counts: P1_TRUSTED_MISSING_SCORING=119
- total_estimated_call_units: 595
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 119
- estimated_call_units: 595
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
- rows_reviewed: 119
- p1_rows: 119
- p2_rows: 0
- p1_estimated_units: 595
- p2_estimated_units: 0
- auto_units_reserved: 595
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=119
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: REVIEW_EMPTY_DIAGNOSTIC_BOARD
- operator_state: EMPTY_REVIEW_REQUIRED
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 119
- diagnostic_no_bet_rows: 0
- next_action: Review date guard and board diagnostics before market discussion.
## Rejected Source Block Audit
- rows_reviewed: 2
- correct_reject_rows: 0
- manual_review_rows: 2
- whitelist_candidate_rows: 1
- audit_bucket_counts: REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=1; MANUAL_REVIEW_POSSIBLE_WHITELIST=1
- review_priority_counts: P2_REVIEW_LOW_CONFIDENCE=1; P1_REVIEW_CANDIDATE=1
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
## Manual Whitelist Review Board
- review_rows: 1
- p1_review_rows: 1
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=1
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=1
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=1
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=1
- scoring_permission_counts: NO_SCORING_PERMISSION=1
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
## Max-Coverage API Enrichment Policy
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 119
- rows_allowed: 119
- full_scoring_enrichment_rows: 89
- coverage_probe_rows: 0
- diagnostic_only_rows: 30
- blocked_rows: 0
- estimated_call_units: 595
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=89; DIAGNOSTIC_ONLY_NO_SCORING=30
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 89
- coverage_probe_rows: 0
- diagnostic_only_rows: 30
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 67
- bucket_counts: P3_REVIEW_LOW_SIGNAL=34; P1_REVIEW_STRONG_SIGNAL=33
- risk_label_counts: LOW=34; MEDIUM=33
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=67
- pick_permission_counts: NO_PICK_PERMISSION=67
- stake_permission_counts: NO_STAKE_PERMISSION=67
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 67
- api_calls_planned: 67
- api_calls_executed: 67
- finished_rows: 6
- pending_rows: 61
- refresh_status_counts: OK=67
- provider_counts: API-SPORTS_DIRECT=67
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 67
- finished_rows: 6
- pending_rows: 61
- accuracy_bucket_counts: PENDING_RESULT=61; PARTIAL_SIGNAL_VALIDATED=3; STRONG_SIGNAL_VALIDATED=2; SIGNAL_FAILED=1
- api_1x2_counts: PENDING_RESULT=61; MISS=4; HIT=2
- api_double_chance_counts: PENDING_RESULT=61; HIT=4; MISS=2
- api_dnb_counts: PENDING_RESULT=61; VOID=2; HIT=2; MISS=2
- over_1_5_counts: PENDING_RESULT=61; HIT=5; MISS=1
- over_2_5_counts: PENDING_RESULT=61; HIT=5; MISS=1
- under_3_5_counts: PENDING_RESULT=61; MISS=5; HIT=1
- btts_counts: PENDING_RESULT=61; HIT=5; MISS=1
- pick_permission_counts: NO_PICK_PERMISSION=67
- stake_permission_counts: NO_STAKE_PERMISSION=67
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 196
- finished_rows: 98
- pending_rows: 98
- summary_rows: 77
- top_market_by_hit_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DOUBLE_CHANCE | hit_rate_pct=82.1 | evaluated=28
- top_market_by_hit_or_void_rate: SCORE_BUCKET=SCORE_90_PLUS | API_DNB | hit_or_void_rate_pct=82.1 | evaluated=28
- sample_warning_counts: LOW_SAMPLE_UNDER_50=42; MEDIUM_SAMPLE_UNDER_100=28; INSUFFICIENT_SAMPLE_UNDER_20=7
- calibration_status_counts: CALIBRATION_NEUTRAL=21; CALIBRATION_WEAK_OR_NEGATIVE=20; CALIBRATION_MEDIUM_OBSERVED_EDGE=18; CALIBRATION_OBSERVE_ONLY=7; CALIBRATION_MEDIUM_PROTECTED_MARKET=4; CALIBRATION_STRONG_OBSERVED_EDGE=4; CALIBRATION_STRONG_PROTECTED_MARKET=3
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 19
- block_rows: 26
- observe_rows: 32
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=26; RULE_OBSERVE_ONLY_SEGMENT=22; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=9; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=7; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=6; RULE_CANDIDATE_TOTAL_MARKET=4; RULE_NEUTRAL_OBSERVE_MORE=3
- rule_decision_counts: OBSERVE_MORE_SEGMENT=22; WATCH_ONLY_COLLECT_TO_50_SAMPLE=15; BLOCK_ML_PROMOTION=9; BLOCK_OVER_2_5_PROMOTION=9; BLOCK_BTTS_YES_PROMOTION=8; COLLECT_MORE_SAMPLE=7; FUTURE_RULE_REVIEW_ONLY=4; OBSERVE_MORE_GLOBAL_MARKET=3
- future_rule_candidate_counts: NO_BLOCKED_MARKET=26; NO_SEGMENT_SAMPLE_TOO_SMALL=22; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=15; NO_SAMPLE_TOO_SMALL=7; YES_REVIEW_ONLY=4; NO_OBSERVE_MORE=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
