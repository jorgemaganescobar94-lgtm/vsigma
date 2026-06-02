# vSIGMA Date Coherence Guard - 2026-06-01

## Summary
- overall_status: DATE_UNKNOWN_REVIEW
- board_status: daily_board_md=OK; daily_board_csv=DATE_UNKNOWN
- mismatch_count: 0
- missing_core_count: 0
- trigger_date_counts: UNKNOWN=1; 2026-06-01=1
- next_action: Review artifacts with unparseable dates before trusting outputs.
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_board_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_daily_execution_board.md | detail=date coherent
- daily_board_csv | status=DATE_UNKNOWN | observed=UNKNOWN | path=data\processed\today\2026-06-01\vsigma_daily_execution_board.csv | detail=artifact exists but date could not be parsed
- operator_brief_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_operator_brief.md | detail=date coherent
- automation_health_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_automation_health.md | detail=date coherent
- prelock_live_recheck_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_prelock_live_recheck.md | detail=date coherent
- live_trigger_validator_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_live_trigger_validator.md | detail=date coherent
- consolidated_panel_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_consolidated_daily_operator_panel.md | detail=date coherent
- source_reliability_governor_md | status=OK | observed=2026-06-01 | path=data\processed\today\2026-06-01\vsigma_probable_lineup_source_reliability_governor.md | detail=date coherent
- daily_chain_trigger | status=DATE_UNKNOWN | observed=UNKNOWN | path=.vsigma\triggers\daily_decision_chain_v2.trigger | detail=artifact exists but date could not be parsed
- prelock_recheck_trigger | status=OK | observed=2026-06-01 | path=.vsigma\triggers\prelock_official_lineup_recheck.trigger | detail=date coherent

## Guardrails
- Date mismatches block market interpretation until the daily chain is coherent.
- Missing daily board blocks prelock/live/operator outputs from becoming pick permission.
- This guard is diagnostic only and does not execute bets.
