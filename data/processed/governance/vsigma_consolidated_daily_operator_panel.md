# vSIGMA Consolidated Daily Operator Panel - 2026-06-09

## First Read
- panel_status: WATCH
- operator_detail: action=WATCH; final=WATCH_ONLY_NO_STAKE; risk=LOW; health=ATTENTION; board_rows=3
- executable_prematch: NONE
- live_only: ROWS=1
- watchlist: NONE
- no_bet: ROWS=2
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: WATCH
- compact_final_decision: WATCH_ONLY_NO_STAKE
- risk_label: LOW
- health_status: ATTENTION
- board_rows: 3
- panel_status: WATCH
- next_action: Follow operator brief and panel categories; no automatic execution.

## Executable Prematch
- none

## Live Only
- #1 | LIVE_ONLY | Almeria vs Castellón | market=OVER_1_5_SUPPORTED | alt=OVER_2_5_REVIEW | stake=NO_STAKE_OR_SYMBOLIC | permission=NO_PREMATCH | conf=MEDIUM | score=28

## Watchlist
- none

## No Bet
- #2 | NO_BET | Nautico Recife vs Fortaleza EC | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42
- #3 | NO_BET | Ponte Preta vs Cuiaba | market=NO_CLEAR_STAT_MARKET | stake=NO_STAKE | permission=NO | conf=LOW | score=-42

## API Coverage
- board_rows=3
- source_guard_counts: DATED_INPUT_ONLY; API_COVERAGE_GATE_V2=3
- execution_permission_counts: NO_PREMATCH=1; NO=2
- avg_coverage_score: 40.0
- forecast_warning_counts: LINEUPS_INACTIVE=1; API_EARLY_LOW_SUPPORT=1; PARTIAL_RECENT_STATS=2; SHOT_SAMPLE_WEAK=2; CORNER_SAMPLE_WEAK=2; CARD_SAMPLE_WEAK=2
- missing_data_counts: lineup_coverage=NOT_DUE_YET=1; injuries_coverage=NONE=3; recent_stats_coverage=NONE=2; lineup_coverage=NONE=2; standings_coverage=NONE=2; odds_coverage=NONE=2


## API-Enriched Review Board
- source: data/processed/today/2026-06-09/vsigma_api_enriched_review_board.csv
- review_rows_written: 0
- ready_for_manual_review_rows: 0
- blocked_rows: 0
- review_priority_counts: none
- canonical_board_permission_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- none

### API Review Guardrails
- This section is informational only.
- It does not modify the canonical daily execution board.
- Manual review remains mandatory.
- auto_apply=NO and production_change=NO remain hardcoded.

## Official / Probable Lineups
- data/processed/today/2026-06-09/official_lineup_sources.csv: rows=34
- data/processed/today/2026-06-09/vsigma_probable_lineup_consensus.csv: rows=3
- data/processed/governance/official_lineup_sources.csv: rows=34
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-09/official_lineup_sources.csv: rows=34
- data/processed/today/2026-06-09/vsigma_probable_lineup_consensus.csv: rows=3
- data/processed/governance/official_lineup_sources.csv: rows=34
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-09; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-09T22:10:51+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-09; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-09T22:10:51+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-09; reason=normalize_prelock_recheck_date; triggered_at=2026-06-09T22:10:51+01:00

## Key Files
- data/processed/today/2026-06-09/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-09/vsigma_operator_brief.md
- data/processed/today/2026-06-09/vsigma_daily_execution_board.md
- data/processed/today/2026-06-09/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-09/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-09/vsigma_automation_health.md
- data/processed/today/2026-06-09/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-09=2
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
- root_scored_same_day_rows: 3
- real_shortlist_rows: 2
- real_bet_rows: 1
- proxy_rows: 0
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.

## Local Raw Fixture Discovery
- overall_status: LOCAL_RAW_CANDIDATES_FOUND
- files_scanned: 1559
- accepted_rows: 127
- rejected_rows: 29
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 127
- trusted_rows: 3
- quarantine_rows: 0
- blocked_rows: 124
- trust_status_counts: REJECTED_SOURCE_BLOCK=124; TRUSTED_RAW_SOURCE=3
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 127
- promoted_rows: 1
- blocked_rows: 2
- quarantine_rows: 0
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=124; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=2; PROMOTED_TO_SCORING_INPUT=1
- next_action: Promoted rows may feed normal scoring gates only.

## Scoring Gap Explainer
- rows_reviewed: 127
- missing_scored_rows: 0
- no_data_blocked_rows: 2
- not_trusted_rows: 124
- promoted_rows: 1
- gap_status_counts: NOT_TRUSTED_SKIPPED=124; SCORED_ROW_NO_DATA_BLOCKED=2; PROMOTED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 0
- priority_counts: none
- scoring_needed_counts: none
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 0
- dry_run_decision_counts: none
- risk_label_counts: none
- priority_counts: none
- total_estimated_call_units: 0
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: NO_ENRICHMENT_NEEDED
- rows_planned: 0
- estimated_call_units: 0
- approval_required: NO
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: NO_ACTION

## Daily Board Self-Heal
- self_heal_status: NO_ACTION
- promotion_rows_reviewed: 0
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- board_rows_written: 0
- reason: daily board already has rows
## API Quota-Aware Enrichment Gate
- quota_gate_status: NO_AUTO_ENRICHMENT_ALLOWED
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 0
- p1_rows: 0
- p2_rows: 0
- p1_estimated_units: 0
- p2_estimated_units: 0
- auto_units_reserved: 0
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: none
- api_calls_allowed: NO
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: NOT_EMPTY_OR_NOT_APPLICABLE
- operator_state: NORMAL_PIPELINE_REVIEW
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 1
- queue_rows: 0
- diagnostic_no_bet_rows: 0
- next_action: Continue normal panel interpretation.
## Rejected Source Block Audit
- rows_reviewed: 124
- correct_reject_rows: 80
- manual_review_rows: 44
- whitelist_candidate_rows: 32
- audit_bucket_counts: CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=63; MANUAL_REVIEW_POSSIBLE_WHITELIST=32; CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=16; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=12; CORRECT_REJECT_LOW_TIER_LOW_COVERAGE=1
- review_priority_counts: P3_CORRECT_REJECT=80; P1_REVIEW_CANDIDATE=32; P2_REVIEW_LOW_CONFIDENCE=12
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
## Manual Whitelist Review Board
- review_rows: 32
- p1_review_rows: 32
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=32
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=32
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=32
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=32
- scoring_permission_counts: NO_SCORING_PERMISSION=32
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=32
- pick_permission_counts: NO_PICK_PERMISSION=32
- stake_permission_counts: NO_STAKE_PERMISSION=32
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
## Max-Coverage API Enrichment Policy
- policy_status: NO_ROWS_TO_COVER
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 0
- rows_allowed: 0
- full_scoring_enrichment_rows: 0
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- estimated_call_units: 0
- downstream_use_counts: none
- external_calls_allowed: NO
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: NO
- external_calls_executed: NO
- scoring_allowed_rows: 0
- coverage_probe_rows: 0
- diagnostic_only_rows: 0
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:NO_ENRICHMENT_NEEDED
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:NO_AUTO_ENRICHMENT_ALLOWED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 0
- bucket_counts: none
- risk_label_counts: none
- canonical_board_permission_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
## API-Enriched Fixture Results Refresh
- rows_reviewed: 0
- api_calls_planned: 0
- api_calls_executed: 0
- finished_rows: 0
- pending_rows: 0
- refresh_status_counts: none
- provider_counts: none
- next_action: Re-run the postmatch accuracy ledger after this refresh. This output does not create picks or stake.
## API-Enriched Postmatch Accuracy Ledger
- rows_reviewed: 0
- finished_rows: 0
- pending_rows: 0
- accuracy_bucket_counts: none
- api_1x2_counts: none
- api_double_chance_counts: none
- api_dnb_counts: none
- over_1_5_counts: none
- over_2_5_counts: none
- under_3_5_counts: none
- btts_counts: none
- pick_permission_counts: none
- stake_permission_counts: none
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
## API Signal Calibration Summary
- source_rows: 29
- finished_rows: 27
- pending_rows: 2
- summary_rows: 77
- top_market_by_hit_rate: ALL=ALL | API_DOUBLE_CHANCE | hit_rate_pct=77.8 | evaluated=27
- top_market_by_hit_or_void_rate: ALL=ALL | API_DNB | hit_or_void_rate_pct=77.8 | evaluated=27
- sample_warning_counts: INSUFFICIENT_SAMPLE_UNDER_20=70; LOW_SAMPLE_UNDER_50=7
- calibration_status_counts: CALIBRATION_OBSERVE_ONLY=70; CALIBRATION_WEAK_OR_NEGATIVE=2; CALIBRATION_MEDIUM_OBSERVED_EDGE=2; CALIBRATION_NEUTRAL=1; CALIBRATION_STRONG_PROTECTED_MARKET=1; CALIBRATION_STRONG_OBSERVED_EDGE=1
- next_action: Use this summary to design future promotion rules only after enough sample size exists. It cannot create picks or stake.
## API Calibration Rule Candidates
- rows_reviewed: 77
- candidate_rows: 4
- block_rows: 3
- observe_rows: 70
- rule_bucket_counts: RULE_OBSERVE_ONLY_INSUFFICIENT_SAMPLE=70; RULE_BLOCK_NEGATIVE_OR_WEAK_MARKET=3; RULE_CANDIDATE_PROTECTED_MARKET_EARLY_SAMPLE=2; RULE_CANDIDATE_TOTAL_MARKET_EARLY_SAMPLE=2
- rule_decision_counts: COLLECT_MORE_SAMPLE=70; WATCH_ONLY_COLLECT_TO_50_SAMPLE=4; BLOCK_ML_PROMOTION=1; BLOCK_BTTS_YES_PROMOTION=1; BLOCK_OVER_2_5_PROMOTION=1
- future_rule_candidate_counts: NO_SAMPLE_TOO_SMALL=70; YES_REVIEW_ONLY_AFTER_SAMPLE_GROWS=4; NO_BLOCKED_MARKET=3
- activation_permission_counts: NO_RULE_ACTIVATION_PERMISSION=77
- pick_permission_counts: NO_PICK_PERMISSION=77
- stake_permission_counts: NO_STAKE_PERMISSION=77
- next_action: Review candidate rules only after sample grows. This board cannot activate rules, picks, or stake.
