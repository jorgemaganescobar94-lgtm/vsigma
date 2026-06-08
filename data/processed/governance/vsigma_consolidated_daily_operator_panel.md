# vSIGMA Consolidated Daily Operator Panel - 2026-06-08

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
- source: data/processed/today/2026-06-08/vsigma_api_enriched_review_board.csv
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
- data/processed/today/2026-06-08/official_lineup_sources.csv: rows=32
- data/processed/governance/official_lineup_sources.csv: rows=32
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-08/official_lineup_sources.csv: rows=32
- data/processed/governance/official_lineup_sources.csv: rows=32
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: ATTENTION
- components_checked: 11
- severity_counts: OK=3; WARN=1; INFO=7
- status_counts: OK=4; WAITING_OR_NOT_RUN=3; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-08; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-08T20:26:31+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-08; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-08T20:26:31+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-08; reason=normalize_prelock_recheck_date; triggered_at=2026-06-08T20:26:31+01:00

## Key Files
- data/processed/today/2026-06-08/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-08/vsigma_operator_brief.md
- data/processed/today/2026-06-08/vsigma_daily_execution_board.md
- data/processed/today/2026-06-08/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-08/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-08/vsigma_automation_health.md
- data/processed/today/2026-06-08/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-08=2
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
- files_scanned: 1483
- accepted_rows: 70
- rejected_rows: 0
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 70
- trusted_rows: 0
- quarantine_rows: 0
- blocked_rows: 70
- trust_status_counts: REJECTED_SOURCE_BLOCK=70
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 70
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=70
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 70
- missing_scored_rows: 0
- no_data_blocked_rows: 0
- not_trusted_rows: 70
- promoted_rows: 0
- gap_status_counts: NOT_TRUSTED_SKIPPED=70
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
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 70
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
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
- normalized_status: OK_EMPTY_BY_PROMOTION_GATE
- operator_state: HEALTHY_EMPTY_NO_ACTION
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 0
- diagnostic_no_bet_rows: 1
- next_action: No picks. System is coherent and empty because zero candidates were promoted. Wait for future data or improved trusted source coverage.
## Rejected Source Block Audit
- rows_reviewed: 70
- correct_reject_rows: 34
- manual_review_rows: 36
- whitelist_candidate_rows: 13
- audit_bucket_counts: CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=30; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=23; MANUAL_REVIEW_POSSIBLE_WHITELIST=13; CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=3; CORRECT_REJECT_LOW_TIER_LOW_COVERAGE=1
- review_priority_counts: P3_CORRECT_REJECT=34; P2_REVIEW_LOW_CONFIDENCE=23; P1_REVIEW_CANDIDATE=13
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
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
