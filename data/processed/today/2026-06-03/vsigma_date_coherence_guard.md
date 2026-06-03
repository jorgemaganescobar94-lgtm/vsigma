# vSIGMA Date Coherence Guard - 2026-06-03

## Summary
- overall_status: MISSING_DAILY_BOARD
- board_status: daily_board_md=MISSING_CORE; daily_board_csv=DATE_UNKNOWN
- mismatch_count: 0
- missing_core_count: 2
- trigger_date_counts: 2026-06-03=2
- next_action: Run daily decision chain for target date before using prelock/live/operator outputs.
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_board_md | status=MISSING_CORE | observed=MISSING | path=data/processed/today/2026-06-03/vsigma_daily_execution_board.md | detail=required daily artifact is missing
- daily_board_csv | status=DATE_UNKNOWN | observed=UNKNOWN | path=data/processed/today/2026-06-03/vsigma_daily_execution_board.csv | detail=artifact exists but date could not be parsed
- operator_brief_md | status=OK | observed=2026-06-03 | path=data/processed/today/2026-06-03/vsigma_operator_brief.md | detail=date coherent
- automation_health_md | status=MISSING_CORE | observed=MISSING | path=data/processed/today/2026-06-03/vsigma_automation_health.md | detail=required daily artifact is missing
- prelock_live_recheck_md | status=OK | observed=2026-06-03 | path=data/processed/today/2026-06-03/vsigma_prelock_live_recheck.md | detail=date coherent
- live_trigger_validator_md | status=OK | observed=2026-06-03 | path=data/processed/today/2026-06-03/vsigma_live_trigger_validator.md | detail=date coherent
- consolidated_panel_md | status=MISSING_OPTIONAL | observed=MISSING | path=data/processed/today/2026-06-03/vsigma_consolidated_daily_operator_panel.md | detail=optional artifact not found
- source_reliability_governor_md | status=OK | observed=2026-06-03 | path=data/processed/today/2026-06-03/vsigma_probable_lineup_source_reliability_governor.md | detail=date coherent
- daily_chain_trigger | status=OK | observed=2026-06-03 | path=.vsigma/triggers/daily_decision_chain_v2.trigger | detail=date coherent
- prelock_recheck_trigger | status=OK | observed=2026-06-03 | path=.vsigma/triggers/prelock_official_lineup_recheck.trigger | detail=date coherent

## Guardrails
- Date mismatches block market interpretation until the daily chain is coherent.
- Missing daily board blocks prelock/live/operator outputs from becoming pick permission.
- This guard is diagnostic only and does not execute bets.
