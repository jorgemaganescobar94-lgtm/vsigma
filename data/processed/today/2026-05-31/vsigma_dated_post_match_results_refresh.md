# vSIGMA Dated Post-Match Results Refresh - 2026-05-31

## Summary
- rows_reported: 4
- status_counts: NS=4
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- RB Bragantino vs Internacional | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Almeria vs Valladolid | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Cordoba vs Huesca | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Vasco DA Gama vs Atletico-MG | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
