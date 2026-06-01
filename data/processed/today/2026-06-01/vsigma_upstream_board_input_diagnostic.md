# vSIGMA Upstream Board Input Diagnostic - 2026-06-01

## Summary
- overall_status: FORECAST_EMPTY
- first_empty_required_component: objective_availability_gate
- missing_required_count: 2
- empty_required_count: 4
- date_issue_count: 0
- forecast_rows: 0
- translator_rows: 0
- board_rows: 0
- next_action: Investigate why objective availability, context-adjusted picks, match stat forecasts and forecast market translator are empty before market discussion.
- auto_apply: NO
- production_change: NO

## Component Rows
- real_objective_context_gate | status=OK | rows=4 | date=OK | path=data/processed/today/2026-06-01/vsigma_real_objective_context_gate.csv | detail=objective context proxy rows exist
- objective_availability_gate | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-01/vsigma_objective_availability_gate.csv | detail=required upstream file exists but has zero rows
- context_adjusted_final_picks | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-01/vsigma_context_adjusted_final_picks.csv | detail=required upstream file exists but has zero rows
- context_matrix | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-01/vsigma_context_matrix.csv | detail=required upstream file is missing
- context_matrix_portfolio | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-01/vsigma_context_matrix_portfolio.csv | detail=required upstream file is missing
- match_stat_forecasts | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-01/vsigma_match_stat_forecasts.csv | detail=required upstream file exists but has zero rows
- forecast_market_translator | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-01/vsigma_forecast_market_translator.csv | detail=required upstream file exists but has zero rows
- daily_execution_board | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-01/vsigma_daily_execution_board.csv | detail=board exists but has zero rows

## Diagnosis
The board is empty because the chain loses candidates before market translation. The first healthy upstream artifact is real_objective_context_gate with 4 rows, but objective_availability_gate, context_adjusted_final_picks, match_stat_forecasts and forecast_market_translator are empty. Context matrix artifacts are missing.

## Guardrails
- Diagnostic only; this does not execute bets or alter stake permission.
- Empty board is not a pick signal; it is a No Bet / upstream diagnostic state.
- Use this file to locate where the daily chain loses candidates before the board.
