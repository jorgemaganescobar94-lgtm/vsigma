# vSIGMA Date Coherence Guard - 2026-06-01

## Summary
- overall_status: PARTIAL_OUTPUTS
- board_status: daily_board_md=OK; daily_board_csv=DATE_UNKNOWN
- mismatch_count: 0
- missing_core_count: 1
- trigger_date_counts: 2026-06-01=2
- next_action: Build missing core reports before market discussion.
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_board_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_daily_execution_board.md | detail=date coherent
- daily_board_csv | status=DATE_UNKNOWN | observed=UNKNOWN | path=data/processed/today/2026-06-01/vsigma_daily_execution_board.csv | detail=artifact exists but date could not be parsed
- operator_brief_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_operator_brief.md | detail=date coherent
- automation_health_md | status=MISSING_CORE | observed=MISSING | path=data/processed/today/2026-06-01/vsigma_automation_health.md | detail=required daily artifact is missing
- prelock_live_recheck_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_prelock_live_recheck.md | detail=date coherent
- live_trigger_validator_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_live_trigger_validator.md | detail=date coherent
- consolidated_panel_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_consolidated_daily_operator_panel.md | detail=date coherent
- source_reliability_governor_md | status=OK | observed=2026-06-01 | path=data/processed/today/2026-06-01/vsigma_probable_lineup_source_reliability_governor.md | detail=date coherent
- daily_chain_trigger | status=OK | observed=2026-06-01 | path=.vsigma/triggers/daily_decision_chain_v2.trigger | detail=date coherent
- prelock_recheck_trigger | status=OK | observed=2026-06-01 | path=.vsigma/triggers/prelock_official_lineup_recheck.trigger | detail=date coherent

## Guardrails
- Date mismatches block market interpretation until the daily chain is coherent.
- Missing daily board blocks prelock/live/operator outputs from becoming pick permission.
- This guard is diagnostic only and does not execute bets.
