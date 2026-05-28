# vSIGMA Dated Post-Match Results Refresh - 2026-05-28

## Summary
- rows_reported: 3
- status_counts: NS=3
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- Casa Pia vs Torreense | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Cerro Porteno vs Sporting Cristal | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at
- Palmeiras vs Junior | status=NS | goals=None-None | stats=NOT_FINAL | fields=fixture_status_short;fixture_status_long;results_last_refresh_at

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
