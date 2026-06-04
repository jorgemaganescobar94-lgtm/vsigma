# vSIGMA Consolidated Daily Operator Panel - 2026-06-04

## First Read
- panel_status: BROKEN
- operator_detail: action=BROKEN; final=SYSTEM_FIX_REQUIRED; risk=HIGH; health=BROKEN; board_rows=1
- executable_prematch: NONE
- live_only: NONE
- watchlist: NONE
- no_bet: ROWS=1
- health_status: BROKEN
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: BROKEN
- compact_final_decision: SYSTEM_FIX_REQUIRED
- risk_label: HIGH
- health_status: BROKEN
- board_rows: 1
- panel_status: BROKEN
- next_action: Fix workflow/input before market discussion.

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

## Official / Probable Lineups
- data/processed/today/2026-06-04/official_lineup_sources.csv: rows=32
- data/processed/governance/official_lineup_sources.csv: rows=32
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-04/official_lineup_sources.csv: rows=32
- data/processed/governance/official_lineup_sources.csv: rows=32
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: BROKEN
- components_checked: 11
- severity_counts: BROKEN=1; WARN=1; OK=2; INFO=7
- status_counts: MISSING=1; OK=3; WAITING_OR_NOT_RUN=3; CONFIG_EXPECTED=4

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-04; reason=align_daily_chain_self_heal_today_v71_1; triggered_at=2026-06-04T17:05:43+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-04; reason=rerun_daily_decision_chain_v71_1_active_max_coverage_policy_fix; triggered_at=2026-06-04T17:11:18+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-04; reason=align_prelock_today_v71_1; triggered_at=2026-06-04T17:05:43+01:00

## Key Files
- data/processed/today/2026-06-04/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-04/vsigma_operator_brief.md
- data/processed/today/2026-06-04/vsigma_daily_execution_board.md
- data/processed/today/2026-06-04/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-04/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-04/vsigma_automation_health.md
- data/processed/today/2026-06-04/vsigma_probable_lineup_source_reliability_governor.md

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
- trigger_date_counts: 2026-06-04=2
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
- files_scanned: 1372
- accepted_rows: 108
- rejected_rows: 216
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 108
- trusted_rows: 72
- quarantine_rows: 36
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=72; QUARANTINE_REVIEW=36
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 108
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 72
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=72; NOT_TRUSTED_NO_PROMOTION=36
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 108
- missing_scored_rows: 72
- no_data_blocked_rows: 0
- not_trusted_rows: 36
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=72; NOT_TRUSTED_SKIPPED=36
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 72
- priority_counts: P1_TRUSTED_MISSING_SCORING=47; P2_LOW_COVERAGE_SCORING=25
- scoring_needed_counts: YES=72
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 72
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=72
- risk_label_counts: MEDIUM=45; HIGH_LOW_COVERAGE=25; HIGH_CONTEXT_VOLATILITY=2
- priority_counts: P1_TRUSTED_MISSING_SCORING=47; P2_LOW_COVERAGE_SCORING=25
- total_estimated_call_units: 350
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 72
- estimated_call_units: 350
- approval_required: YES
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: WAIT_FOR_MANUAL_APPROVAL

## Daily Board Self-Heal
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 108
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 72
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
## API Quota-Aware Enrichment Gate
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 72
- p1_rows: 47
- p2_rows: 25
- p1_estimated_units: 237
- p2_estimated_units: 113
- auto_units_reserved: 250
- max_auto_units_per_day: 5000
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=45; COVERAGE_PROBE_ALLOWED_P2=25; MANUAL_REVIEW_REQUIRED=2
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: OK_EMPTY_BY_PROMOTION_GATE
- operator_state: HEALTHY_EMPTY_NO_ACTION
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 72
- diagnostic_no_bet_rows: 1
- next_action: No picks. System is coherent and empty because zero candidates were promoted. Wait for future data or improved trusted source coverage.
## Rejected Source Block Audit
- rows_reviewed: 0
- correct_reject_rows: 0
- manual_review_rows: 0
- whitelist_candidate_rows: 0
- audit_bucket_counts: none
- review_priority_counts: none
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
## Max-Coverage API Enrichment Policy
- policy_status: MAX_COVERAGE_POLICY_READY
- api_plan_name: API-Football Ultra
- plan_requests_per_day: 75000
- rows_reviewed: 72
- rows_allowed: 72
- full_scoring_enrichment_rows: 41
- coverage_probe_rows: 22
- diagnostic_only_rows: 9
- blocked_rows: 0
- estimated_call_units: 350
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=41; COVERAGE_GATE_ONLY=22; DIAGNOSTIC_ONLY_NO_SCORING=9
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy for a separate logged API executor. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 41
- coverage_probe_rows: 22
- diagnostic_only_rows: 9
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
