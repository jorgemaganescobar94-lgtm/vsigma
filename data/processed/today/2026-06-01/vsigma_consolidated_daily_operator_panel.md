# vSIGMA Consolidated Daily Operator Panel - 2026-06-01

## First Read
- panel_status: PARTIAL_OUTPUTS
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=ATTENTION; board_rows=0
- executable_prematch: NO_BOARD
- live_only: NONE
- watchlist: NONE
- no_bet: NONE
- health_status: ATTENTION
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: ATTENTION
- board_rows: 0
- panel_status: PARTIAL_OUTPUTS
- next_action: Daily execution board is missing; do not use operator/prelock/live outputs as pick permission. Run daily chain first.

## Executable Prematch
- none

## Live Only
- none

## Watchlist
- none

## No Bet
- none

## API Coverage
- no daily board rows available

## Official / Probable Lineups
- data/processed/today/2026-06-01/official_lineup_sources.csv: rows=32
- data/processed/today/2026-06-01/vsigma_probable_lineup_consensus.csv: rows=1
- data/processed/governance/official_lineup_sources.csv: rows=32
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-01/official_lineup_sources.csv: rows=32
- data/processed/today/2026-06-01/vsigma_probable_lineup_consensus.csv: rows=1
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
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-01; reason=run_daily_chain_self_heal_v68_0_objective_context_bridge; triggered_at=2026-06-01T10:12:00+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-02; reason=run_daily_decision_chain_v2_v67_6_missing_board_self_heal; triggered_at=2026-06-02T13:26:52+01:00
- .vsigma/triggers/prelock_official_lineup_recheck.trigger: date=2026-06-01; reason=run_prelock_recheck_v67_5_1_safe_consolidated_operator_panel; triggered_at=2026-06-01T09:05:00+01:00

## Key Files
- data/processed/today/2026-06-01/vsigma_consolidated_daily_operator_panel.md
- data/processed/today/2026-06-01/vsigma_operator_brief.md
- data/processed/today/2026-06-01/vsigma_daily_execution_board.md
- data/processed/today/2026-06-01/vsigma_prelock_live_recheck.md
- data/processed/today/2026-06-01/vsigma_live_trigger_validator.md
- data/processed/today/2026-06-01/vsigma_automation_health.md
- data/processed/today/2026-06-01/vsigma_probable_lineup_source_reliability_governor.md

## Guardrails
- Panel is diagnostic only; it does not execute bets.
- auto_apply=NO and production_change=NO are hardcoded.
- No Bet, Watch, Live Only, Learning Only and Quarantine are valid successful outcomes.
- Source Reliability Governor remains advisory-only and cannot change weights by itself.
- If the daily board is missing, prelock/live files cannot be used as pick permission.

## Date Coherence Guard
- overall_status: DATE_MISMATCH_BLOCK
- board_status: daily_board_md=OK; daily_board_csv=DATE_UNKNOWN
- mismatch_count: 1
- missing_core_count: 0
- trigger_date_counts: 2026-06-02=1; 2026-06-01=1
- next_action: Fix trigger/artifact date mismatch before using market signals.

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
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 1
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.
