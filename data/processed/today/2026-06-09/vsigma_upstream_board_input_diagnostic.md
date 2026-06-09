# vSIGMA Upstream Board Input Diagnostic - 2026-06-09

## Summary
- overall_status: UPSTREAM_MISSING
- first_empty_required_component: context_matrix
- missing_required_count: 2
- empty_required_count: 0
- date_issue_count: 0
- forecast_rows: 3
- translator_rows: 3
- board_rows: 3
- next_action: Build missing required upstream component first: context_matrix.
- auto_apply: NO
- production_change: NO

## Component Rows
- real_objective_context_gate | status=OK | rows=1 | date=OK | path=data/processed/today/2026-06-09/vsigma_real_objective_context_gate.csv | detail=file has rows and passed basic diagnostic checks
- objective_availability_gate | status=OK | rows=1 | date=OK | path=data/processed/today/2026-06-09/vsigma_objective_availability_gate.csv | detail=file has rows and passed basic diagnostic checks
- context_adjusted_final_picks | status=OK | rows=1 | date=OK | path=data/processed/today/2026-06-09/vsigma_context_adjusted_final_picks.csv | detail=file has rows and passed basic diagnostic checks
- context_matrix | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-09/vsigma_context_matrix.csv | detail=required upstream file is missing
- context_matrix_portfolio | status=MISSING_REQUIRED | rows=0 | date=MISSING | path=data/processed/today/2026-06-09/vsigma_context_matrix_portfolio.csv | detail=required upstream file is missing
- match_stat_forecasts | status=OK | rows=3 | date=OK | path=data/processed/today/2026-06-09/vsigma_match_stat_forecasts.csv | detail=file has rows and passed basic diagnostic checks
- forecast_market_translator | status=OK | rows=3 | date=OK | path=data/processed/today/2026-06-09/vsigma_forecast_market_translator.csv | detail=file has rows and passed basic diagnostic checks
- daily_execution_board | status=OK | rows=3 | date=OK | path=data/processed/today/2026-06-09/vsigma_daily_execution_board.csv | detail=file has rows and passed basic diagnostic checks
- fixture_api_coverage_matrix | status=MISSING_OPTIONAL | rows=0 | date=MISSING | path=data/processed/today/2026-06-09/vsigma_fixture_api_coverage_matrix_v3.csv | detail=optional upstream file is missing
- probable_lineup_consensus | status=OK | rows=3 | date=OK | path=data/processed/today/2026-06-09/vsigma_probable_lineup_consensus.csv | detail=file has rows and passed basic diagnostic checks

## Guardrails
- Diagnostic only; this does not execute bets or alter stake permission.
- Empty board is not a pick signal; it is a No Bet / upstream diagnostic state.
- Use this file to locate where the daily chain loses candidates before the board.
