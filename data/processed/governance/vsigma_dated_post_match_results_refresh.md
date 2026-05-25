# vSIGMA Dated Post-Match Results Refresh - 2026-05-25

## Summary
- rows_reported: 1
- status_counts: REFRESH_SKIPPED_NO_API_CREDENTIALS=1
- source_guard: DATED_INPUT_ONLY
- auto_apply: NO
- production_change: NO

## Rows
- SYSTEM vs SYSTEM | status=REFRESH_SKIPPED_NO_API_CREDENTIALS | goals=NA | stats=Missing GitHub Actions secret API_FOOTBALL_KEY/APISPORTS_KEY or RAPIDAPI_KEY | fields=none

## Guardrails
- If API credentials are missing, this step writes a diagnostic report and exits successfully.
- This refresh only writes dated outputs and does not infer missing stats.
