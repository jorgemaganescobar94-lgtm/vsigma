# vSIGMA Consolidated Daily Operator Panel - 2026-06-01

## First Read
- panel_status: PARTIAL_OUTPUTS
- operator_detail: action=NONE; final=NO_OPERATOR_ACTION; risk=NONE; health=UNKNOWN; board_rows=0
- executable_prematch: NO_BOARD
- live_only: NONE
- watchlist: NONE
- no_bet: NONE
- health_status: MISSING
- auto_apply: NO
- production_change: NO

## Operator Gate
- action_level: NONE
- compact_final_decision: NO_OPERATOR_ACTION
- risk_label: NONE
- health_status: UNKNOWN
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
- data/processed/today/2026-06-01/official_lineup_sources.csv: rows=30
- data/processed/governance/official_lineup_sources.csv: rows=30
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Quarantine / Learning-Only / Import Status
- data/processed/today/2026-06-01/official_lineup_sources.csv: rows=30
- data/processed/governance/official_lineup_sources.csv: rows=30
- data/processed/governance/vsigma_probable_lineup_accuracy_ledger.csv: rows=8; probable_status=UNKNOWN=1; LEARNING_ONLY=1; IMPORTED=6

## Source Reliability Governor
- sources_reviewed: 15
- verdict_counts: HOLD_SAMPLE=15
- sample_gate_counts: INSUFFICIENT_SAMPLE=15
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=15

## Automation Health
- system_status: MISSING
- components_checked: UNKNOWN
- severity_counts: UNKNOWN
- status_counts: UNKNOWN

## Next Triggers / Rechecks
- .vsigma/triggers/daily_chain_self_heal.trigger: date=2026-06-01; reason=run_daily_chain_self_heal_v67_8_missing_board; triggered_at=2026-06-01T09:35:00+01:00
- .vsigma/triggers/daily_decision_chain_v2.trigger: date=2026-06-01; reason=run_daily_decision_chain_v2_v67_6_missing_board_self_heal; triggered_at=2026-06-01T09:22:00+01:00
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
- overall_status: PARTIAL_OUTPUTS
- board_status: daily_board_md=OK; daily_board_csv=DATE_UNKNOWN
- mismatch_count: 0
- missing_core_count: 1
- trigger_date_counts: 2026-06-01=2
- next_action: Build missing core reports before market discussion.
