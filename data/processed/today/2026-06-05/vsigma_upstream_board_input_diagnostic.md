# vSIGMA Upstream Board Input Diagnostic - 2026-06-05

## Summary
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: real_objective_context_gate
- missing_required_count: 7
- empty_required_count: 1
- date_issue_count: 0
- forecast_rows: 0
- translator_rows: 0
- board_rows: 0
- next_action: Build missing required upstream component first: real_objective_context_gate.
- auto_apply: NO
- production_change: NO

## Component Rows
- real_objective_context_gate | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_real_objective_context_gate.csv | detail=required upstream file is missing
- objective_availability_gate | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_objective_availability_gate.csv | detail=required upstream file is missing
- context_adjusted_final_picks | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_context_adjusted_final_picks.csv | detail=required upstream file is missing
- context_matrix | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_context_matrix.csv | detail=required upstream file is missing
- context_matrix_portfolio | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_context_matrix_portfolio.csv | detail=required upstream file is missing
- match_stat_forecasts | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_match_stat_forecasts.csv | detail=required upstream file is missing
- forecast_market_translator | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_forecast_market_translator.csv | detail=required upstream file is missing
- daily_execution_board | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-05/vsigma_daily_execution_board.csv | detail=required upstream file exists but has zero rows
- fixture_api_coverage_matrix | status=MISSING_OPTIONAL | rows=0 | date=MISSING | path=data/processed/today/2026-06-05/vsigma_fixture_api_coverage_matrix_v3.csv | detail=optional upstream file is missing
- probable_lineup_consensus | status=EMPTY_OPTIONAL | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-05/vsigma_probable_lineup_consensus.csv | detail=optional upstream file has zero rows

## Guardrails
- Diagnostic only; this does not execute bets or alter stake permission.
- Empty board is not a pick signal; it is a No Bet / upstream diagnostic state.
- Use this file to locate where the daily chain loses candidates before the board.
