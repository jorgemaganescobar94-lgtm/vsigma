# vSIGMA Date Coherence Guard - 2026-06-14

## Summary
- overall_status: DATE_MISMATCH_BLOCK
- board_status: daily_board_md=MISSING_CORE; daily_board_csv=MISSING_CORE
- mismatch_count: 2
- missing_core_count: 2
- trigger_date_counts: 2026-06-10=2
- next_action: Fix trigger/artifact date mismatch before using market signals.
- auto_apply: NO
- production_change: NO

## Component Rows
- daily_board_md | status=MISSING_CORE | observed=MISSING | path=data/processed/today/2026-06-14/vsigma_daily_execution_board.md | detail=required daily artifact is missing
- daily_board_csv | status=MISSING_CORE | observed=MISSING | path=data/processed/today/2026-06-14/vsigma_daily_execution_board.csv | detail=required daily artifact is missing
- operator_brief_md | status=OK | observed=2026-06-14 | path=data/processed/today/2026-06-14/vsigma_operator_brief.md | detail=date coherent
- automation_health_md | status=OK | observed=2026-06-14 | path=data/processed/today/2026-06-14/vsigma_automation_health.md | detail=date coherent
- prelock_live_recheck_md | status=MISSING_OPTIONAL | observed=MISSING | path=data/processed/today/2026-06-14/vsigma_prelock_live_recheck.md | detail=optional artifact not found
- live_trigger_validator_md | status=OK | observed=2026-06-14 | path=data/processed/today/2026-06-14/vsigma_live_trigger_validator.md | detail=date coherent
- consolidated_panel_md | status=MISSING_OPTIONAL | observed=MISSING | path=data/processed/today/2026-06-14/vsigma_consolidated_daily_operator_panel.md | detail=optional artifact not found
- source_reliability_governor_md | status=MISSING_OPTIONAL | observed=MISSING | path=data/processed/today/2026-06-14/vsigma_probable_lineup_source_reliability_governor.md | detail=optional artifact not found
- daily_chain_trigger | status=DATE_MISMATCH | observed=2026-06-10 | path=.vsigma/triggers/daily_decision_chain_v2.trigger | detail=observed 2026-06-10 != target 2026-06-14
- prelock_recheck_trigger | status=DATE_MISMATCH | observed=2026-06-10 | path=.vsigma/triggers/prelock_official_lineup_recheck.trigger | detail=observed 2026-06-10 != target 2026-06-14

## Guardrails
- Date mismatches block market interpretation until the daily chain is coherent.
- Missing daily board blocks prelock/live/operator outputs from becoming pick permission.
- This guard is diagnostic only and does not execute bets.
