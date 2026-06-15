# vSIGMA Consolidated Daily Operator Panel - 2026-06-15

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
- #1 | NO_BET | Maringá vs Maranhão | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=1
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=1
- execution_permission_counts: NO=1
- avg_coverage_score: 15.0
- forecast_warning_counts: PARTIAL_RECENT_STATS=1; SHOT_SAMPLE_WEAK=1; CORNER_SAMPLE_WEAK=1; CARD_SAMPLE_WEAK=1
- missing_data_counts: league_coverage=PARTIAL=1; recent_stats_coverage=NONE=1; lineup_coverage=NONE=1; injuries_coverage=NONE=1; standings_coverage=NONE=1; odds_coverage=NONE=1


## API-Enriched Review Board
- source: data/processed/today/2026-06-15/vsigma_api_enriched_review_board.csv
- review_rows_written: 36
- ready_for_manual_review_rows: 36
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=23; P1_MANUAL_REVIEW=13
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=36
- pick_permission_counts: NO_PICK_PERMISSION=36
- stake_permission_counts: NO_STAKE_PERMISSION=36
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P1_MANUAL_REVIEW | Westchester SC vs Greenville Triumph | status=API_ENRICHED_REVIEW_READY | score=90 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Greenville Triumph | pred_total_home_away=38.3/61.8 | 1x2=2.75/3.55/2.20 | ou2.5=1.62/2.20
- P2_MANUAL_REVIEW | Bigfoot vs Oly Town | status=API_ENRICHED_REVIEW_READY | score=56 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Oly Town | pred_total_home_away=39.5/60.7
- P2_MANUAL_REVIEW | City SC vs Ventura County Fusion | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Ventura County Fusion | pred_total_home_away=30.3/69.8
- P2_MANUAL_REVIEW | Brazos Valley vs Hill Country Lobos | status=API_ENRICHED_REVIEW_READY | score=64 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Brazos Valley | pred_total_home_away=63.3/36.7
- P2_MANUAL_REVIEW | Snohomish United vs West Seattle Junction | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Snohomish United | pred_total_home_away=67.2/32.8
- P2_MANUAL_REVIEW | Sportivo San Juan vs Almaden | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Almaden | pred_total_home_away=28.0/72.0
- P2_MANUAL_REVIEW | Varketili vs Betlemi | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Varketili | pred_total_home_away=87.0/13.0
- P2_MANUAL_REVIEW | Negelle Arsi vs Awassa Kenema | status=API_ENRICHED_REVIEW_READY | score=69 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Negelle Arsi | pred_total_home_away=58.3/42.0 | 1x2=2.62/2.50/2.90
- P1_MANUAL_REVIEW | KMC vs Coastal Union | status=API_ENRICHED_REVIEW_READY | score=76 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Coastal Union | pred_total_home_away=43.0/57.0 | 1x2=4.10/3.70/1.64 | ou2.5=1.60/2.05
- P2_MANUAL_REVIEW | Gonio vs Margveti 2006 | status=API_ENRICHED_REVIEW_READY | score=64 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Gonio | pred_total_home_away=63.3/36.8

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-15/official_lineup_sources.csv: rows=42
- data/processed/today/2026-06-15/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=42
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-15/official_lineup_sources.csv: rows=42
- data/processed/today/2026-06-15/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=42
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-15; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-15T14:30:26+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-15; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-15T14:30:26+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-15; reason=normalize_prelock_recheck_date; triggered_at=2026-06-15T14:30:26+01:00

## Key Files
- data/processed/today/2026-06-15/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-15/vsigma_operator_brief.md
- data/processed/today/2026-06-15/vsigma_daily_execution_board.md
- data/processed/today/2026-06-15/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-15/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-15/vsigma_automation_health.md
- data/processed/today/2026-06-15/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-15=2
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
- files_scanned: 1784
- accepted_rows: 72
- rejected_rows: 11
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 72
- trusted_rows: 67
- quarantine_rows: 5
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=67; QUARANTINE_REVIEW=5
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 72
- promoted_rows: 0
- blocked_rows: 1
- quarantine_rows: 66
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=66; NOT_TRUSTED_NO_PROMOTION=5; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=1
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 72
- missing_scored_rows: 66
- no_data_blocked_rows: 1
- not_trusted_rows: 5
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=66; NOT_TRUSTED_SKIPPED=5; SCORED_ROW_NO_DATA_BLOCKED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 66
- priority_counts: P1_TRUSTED_MISSING_SCORING=66
- scoring_needed_counts: YES=66
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 66
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=66
- risk_label_counts: MEDIUM=66
- priority_counts: P1_TRUSTED_MISSING_SCORING=66
- total_estimated_call_units: 330
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 66
- estimated_call_units: 330
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
- rows_reviewed: 66
- p1_rows: 66
- p2_rows: 0
- p1_estimated_units: 330
- p2_estimated_units: 0
- auto_units_reserved: 330
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=66
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: REVIEW_EMPTY_DIAGNOSTIC_BOARD
- operator_state: EMPTY_REVIEW_REQUIRED
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 66
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
- rows_reviewed: 66
- rows_allowed: 66
- full_scoring_enrichment_rows: 53
- coverage_probe_rows: 0
- diagnostic_only_rows: 13
- blocked_rows: 0
- estimated_call_units: 330
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=53; DIAGNOSTIC_ONLY_NO_SCORING=13
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 53
- coverage_probe_rows: 0
- diagnostic_only_rows: 13
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 36
- bucket_counts: P3_REVIEW_LOW_SIGNAL=23; P1_REVIEW_STRONG_SIGNAL=13
- risk_label_counts: LOW=23; MEDIUM=13
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=36
- pick_permission_counts: NO_PICK_PERMISSION=36
- stake_permission_counts: NO_STAKE_PERMISSION=36
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 36
- api_calls_planned: 36
- api_calls_executed: 36
- finished_rows: 8
- pending_rows: 28
- refresh_status_counts: OK=36
- provider_counts: API-SPORTS_DIRECT=36
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 36
- finished_rows: 8
- pending_rows: 28
- accuracy_bucket_counts: PENDING_RESULT=28; STRONG_SIGNAL_VALIDATED=5; SIGNAL_FAILED=2; PARTIAL_SIGNAL_VALIDATED=1
- api_1x2_counts: PENDING_RESULT=28; HIT=5; MISS=3
- api_double_chance_counts: PENDING_RESULT=28; HIT=6; MISS=2
- api_dnb_counts: PENDING_RESULT=28; HIT=5; MISS=2; VOID=1
- over_1_5_counts: PENDING_RESULT=28; HIT=7; MISS=1
- over_2_5_counts: PENDING_RESULT=28; HIT=6; MISS=2
- under_3_5_counts: PENDING_RESULT=28; MISS=4; HIT=4
- btts_counts: PENDING_RESULT=28; HIT=5; MISS=3
- pick_permission_counts: NO_PICK_PERMISSION=36
- stake_permission_counts: NO_STAKE_PERMISSION=36
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 99
- finished_rows: 64
- pending_rows: 35
- summary_rows: 77
- top_market_by_hit_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DOUBLE_CHANCE | hit_rate_pct=80.0 | evaluated=25
- top_market_by_hit_or_void_rate: REVIEW_PRIORITY=P1_MANUAL_REVIEW | API_DNB | hit_or_void_rate_pct=80.0 | evaluated=25
- sample_warning_counts: LOW_SAMPLE_UNDER_50=49; INSUFFICIENT_SAMPLE_UNDER_20=21; MEDIUM_SAMPLE_UNDER_100=7
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=21; CALIBRATION_WEAK_OR_NEGATIVE=20; CALIBRATION_NEUTRAL=20; CALIBRATION_STRONG_OBSERVED_EDGE=6; CALIBRATION_MEDIUM_OBSERVED_EDGE=5; CALIBRATION_MEDIUM_PROTECTED_MARKET=3; CALIBRATION_STRONG_PROTECTED_MARKET=2
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 9
- block_rows: 22
- observe_rows: 46
- rule_bucket_counts: RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=22; RULE_OBSERVE_ONLY_SEGMENT=22; RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=21; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=4; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=4; RULE_NEUTRAL_OBSERVE_MORE=3; RULE_CANDIDATE_TOTAL_MARKET=1
- rule_decision_counts: OBSERVE_MORE_SEGMENT=22; COLLECT_MORE_SAMPLE=21; BLOCK_ML_PROMOTION=8; WATCH_ONLY_COLLECT_TO_50_SAMPLE=8; BLOCK_BTTS_YES_PROMOTION=7; BLOCK_OVER_2_5_PROMOTION=7; OBSERVE_MORE_GLOBAL_MARKET=3; FUTURE_RULE_REVIEW_ONLY=1
- future_rule_candidate_counts: NO_BLOCKED_MARKET=22; NO_SEGMENT_SAMPLE_TOO_SMALL=22; NO_SAMPLE_TOO_SMALL=21; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=8; NO_OBSERVE_MORE=3; YES_REVIEW_ONLY=1
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
