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
- review_rows_written: 28
- ready_for_manual_review_rows: 28
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=14; P1_MANUAL_REVIEW=14
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=28
- pick_permission_counts: NO_PICK_PERMISSION=28
- stake_permission_counts: NO_STAKE_PERMISSION=28
- panel_note: API review board is parallel-only and cannot create picks, stake, or canonical board permission.

### API Review Rows
- P2_MANUAL_REVIEW | Dainava vs Garliava | status=API_ENRICHED_REVIEW_READY | score=67 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Dainava | pred_total_home_away=54.0/46.0 | 1x2=2.05/3.45/2.95 | ou2.5=1.60/2.05
- P1_MANUAL_REVIEW | FUS Rabat vs Difaa EL Jadida | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=FUS Rabat | pred_total_home_away=65.7/34.3 | 1x2=1.77/3.25/4.40 | ou2.5=2.20/1.62
- P2_MANUAL_REVIEW | Olympique Dcheïra vs Hassania Agadir | status=API_ENRICHED_REVIEW_READY | score=55 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Olympique Dcheïra | pred_total_home_away=49.8/50.2 | 1x2=3.20/2.85/2.33 | ou2.5=2.35/1.55
- P1_MANUAL_REVIEW | Renaissance Berkane vs Ittihad Tanger | status=API_ENRICHED_REVIEW_READY | score=90 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Renaissance Berkane | pred_total_home_away=61.8/38.2 | 1x2=1.65/3.30/5.20 | ou2.5=2.20/1.62
- P1_MANUAL_REVIEW | Wydad AC vs Olympique Safi | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Wydad AC | pred_total_home_away=66.3/33.7 | 1x2=1.45/3.75/6.75 | ou2.5=1.93/1.80
- P2_MANUAL_REVIEW | Uni Souza vs Barcelona RJ | status=API_ENRICHED_REVIEW_READY | score=61 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Uni Souza | pred_total_home_away=52.0/48.0 | 1x2=1.53/3.80/4.80 | ou2.5=1.55/2.15
- P1_MANUAL_REVIEW | Monsoon vs Santa Cruz RS | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Santa Cruz RS | pred_total_home_away=24.2/76.2 | 1x2=2.25/3.20/3.00 | ou2.5=2.15/1.65
- P1_MANUAL_REVIEW | 3 de Noviembre vs General Caballero | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=General Caballero | pred_total_home_away=33.0/67.0 | 1x2=3.75/3.20/1.85 | ou2.5=1.90/1.73
- P1_MANUAL_REVIEW | Encarnación vs SOL DE America | status=API_ENRICHED_REVIEW_READY | score=100 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=SOL DE America | pred_total_home_away=25.7/74.3 | 1x2=2.62/3.00/2.50 | ou2.5=2.10/1.57
- P2_MANUAL_REVIEW | Jeunes Fauves vs Aigle Royal de Moungo | status=API_ENRICHED_REVIEW_READY | score=70 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | summary=prediction_winner=Aigle Royal de Moungo | pred_total_home_away=28.3/71.8

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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-08; reason=normalize_daily_chain_self_heal_date; triggered_at=2026-06-08T21:11:57+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-08; reason=normalize_daily_decision_chain_v2_date; triggered_at=2026-06-08T21:11:57+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-08; reason=normalize_prelock_recheck_date; triggered_at=2026-06-08T21:11:57+01:00

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
- files_scanned: 1490
- accepted_rows: 70
- rejected_rows: 282
- next_action: Review accepted rows, then feed normal scoring gates.

## Raw Candidate Trust Gate
- rows_reviewed: 70
- trusted_rows: 43
- quarantine_rows: 27
- blocked_rows: 0
- trust_status_counts: TRUSTED_RAW_SOURCE=43; QUARANTINE_REVIEW=27
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.

## Trusted Raw Candidate Promotion Gate
- rows_reviewed: 70
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 43
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=43; NOT_TRUSTED_NO_PROMOTION=27
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.

## Scoring Gap Explainer
- rows_reviewed: 70
- missing_scored_rows: 43
- no_data_blocked_rows: 0
- not_trusted_rows: 27
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=43; NOT_TRUSTED_SKIPPED=27
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.

## Trusted Raw Scoring Queue
- queue_rows: 43
- priority_counts: P1_TRUSTED_MISSING_SCORING=39; P2_LOW_COVERAGE_SCORING=4
- scoring_needed_counts: YES=43
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.

## Queue-to-Enrichment Dry Run Planner
- rows_planned: 43
- dry_run_decision_counts: DRY_RUN_ONLY_NO_API_CALLS=43
- risk_label_counts: MEDIUM=37; HIGH_LOW_COVERAGE=4; HIGH_CONTEXT_VOLATILITY=2
- priority_counts: P1_TRUSTED_MISSING_SCORING=39; P2_LOW_COVERAGE_SCORING=4
- total_estimated_call_units: 216
- api_calls_planned: NO
- api_calls_executed: NO
- next_action: Review dry-run plan and explicitly approve any future enrichment/API stage. No calls executed here.

## Enrichment Cost & Approval Gate
- approval_gate_status: WAIT_FOR_MANUAL_APPROVAL
- rows_planned: 43
- estimated_call_units: 216
- approval_required: YES
- max_allowed_without_manual_approval: 0
- api_calls_allowed: NO
- api_calls_planned: NO
- api_calls_executed: NO
- recommended_action: WAIT_FOR_MANUAL_APPROVAL

## Daily Board Self-Heal
- self_heal_status: EMPTY_BY_PROMOTION_GATE
- promotion_rows_reviewed: 70
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 43
- board_rows_written: 1_DIAGNOSTIC_ROW
- reason: 0 promoted raw candidates; no scoring-safe rows available
## API Quota-Aware Enrichment Gate
- quota_gate_status: AUTO_ENRICHMENT_ALLOWED_LIMITED
- api_plan_name: API-Football Pro
- plan_requests_per_day: 7500
- rows_reviewed: 43
- p1_rows: 39
- p2_rows: 4
- p1_estimated_units: 197
- p2_estimated_units: 19
- auto_units_reserved: 189
- max_auto_units_per_day: 1500
- max_auto_units_per_run: 1500
- quota_decision_counts: AUTO_ENRICHMENT_ALLOWED_P1=37; COVERAGE_PROBE_ALLOWED_P2=4; MANUAL_REVIEW_REQUIRED=2
- api_calls_allowed: YES_LIMITED
- api_calls_executed: NO
- recommended_action: Run a separate enrichment executor only for allowlisted rows; do not create picks from enrichment alone.
## Empty Diagnostic Board State Normalizer
- normalized_status: OK_EMPTY_BY_PROMOTION_GATE
- operator_state: HEALTHY_EMPTY_NO_ACTION
- board_status: daily_board_md=OK; daily_board_csv=OK
- mismatch_count: 0
- promoted_rows: 0
- queue_rows: 43
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
- rows_reviewed: 43
- rows_allowed: 43
- full_scoring_enrichment_rows: 34
- coverage_probe_rows: 4
- diagnostic_only_rows: 5
- blocked_rows: 0
- estimated_call_units: 216
- downstream_use_counts: SCORING_ALLOWED_WITH_NORMAL_GATES=34; DIAGNOSTIC_ONLY_NO_SCORING=5; COVERAGE_GATE_ONLY=4
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- next_action: Use max-coverage policy through the subscription guard and logged API executor only. Enrichment can be broad; scoring remains restricted by downstream_use and normal gates.
## Active API Policy
- active_api_policy: MAX_COVERAGE
- policy_source: vsigma_max_coverage_api_enrichment_policy
- external_calls_allowed: YES_MAX_COVERAGE_POLICY
- external_calls_executed: NO
- scoring_allowed_rows: 34
- coverage_probe_rows: 4
- diagnostic_only_rows: 5
- blocked_rows: 0
- legacy_cost_gate_status: LEGACY_INFORMATIONAL_ONLY:WAIT_FOR_MANUAL_APPROVAL
- legacy_quota_gate_status: LEGACY_SECONDARY_ONLY:AUTO_ENRICHMENT_ALLOWED_LIMITED
- legacy_allowlist_status: LEGACY_SECONDARY_ONLY:ALLOWLIST_DRY_RUN_READY
- operator_note: MAX_COVERAGE is the active API policy. Legacy cost/quota/allowlist gates are informational and cannot override the active policy. No external calls are executed by this integration.
## API-Enriched Manual Review Inspector
- review_rows: 28
- bucket_counts: BLOCKED_INSUFFICIENT_CONTEXT=28
- risk_label_counts: HIGH=28
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=28
- pick_permission_counts: NO_PICK_PERMISSION=28
- stake_permission_counts: NO_STAKE_PERMISSION=28
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
