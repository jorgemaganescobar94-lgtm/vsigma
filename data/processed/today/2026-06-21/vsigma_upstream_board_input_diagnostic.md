# vSIGMA Upstream Board Input Diagnostic - 2026-06-21

## Summary
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: real_objective_context_gate
- missing_required_count: 2
- empty_required_count: 3
- date_issue_count: 0
- forecast_rows: 11
- translator_rows: 11
- board_rows: 11
- next_action: Build missing required upstream component first: real_objective_context_gate.
- auto_apply: NO
- production_change: NO

## Component Rows
- real_objective_context_gate | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-21/vsigma_real_objective_context_gate.csv | detail=required upstream file exists but has zero rows
- objective_availability_gate | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-21/vsigma_objective_availability_gate.csv | detail=required upstream file exists but has zero rows
- context_adjusted_final_picks | status=EMPTY_REQUIRED | rows=0 | date=NO_ROWS | path=data/processed/today/2026-06-21/vsigma_context_adjusted_final_picks.csv | detail=required upstream file exists but has zero rows
- context_matrix | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-21/vsigma_context_matrix.csv | detail=required upstream file is missing
- context_matrix_portfolio | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-21/vsigma_context_matrix_portfolio.csv | detail=required upstream file is missing
- match_stat_forecasts | status=OK | rows=11 | date=OK | path=data/processed/today/2026-06-21/vsigma_match_stat_forecasts.csv | detail=file has rows and passed basic diagnostic checks
- forecast_market_translator | status=OK | rows=11 | date=OK | path=data/processed/today/2026-06-21/vsigma_forecast_market_translator.csv | detail=file has rows and passed basic diagnostic checks
- daily_execution_board | status=OK | rows=11 | date=OK | path=data/processed/today/2026-06-21/vsigma_daily_execution_board.csv | detail=file has rows and passed basic diagnostic checks
- fixture_api_coverage_matrix | status=MISSING_OPTIONAL | rows=0 | date=MISSING | path=data/processed/today/2026-06-21/vsigma_fixture_api_coverage_matrix_v3.csv | detail=optional upstream file is missing
- probable_lineup_consensus | status=OK | rows=11 | date=OK | path=data/processed/today/2026-06-21/vsigma_probable_lineup_consensus.csv | detail=file has rows and passed basic diagnostic checks

## Guardrails
- Diagnostic only; this does not execute bets or alter stake permission.
- Empty board is not a pick signal; it is a No Bet / upstream diagnostic state.
- Use this file to locate where the daily chain loses candidates before the board.
