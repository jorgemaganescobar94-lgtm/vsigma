# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-06-26

## Summary
- rows_reviewed: 0
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 0
- promotion_status_counts: none
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.
- auto_apply: NO
- production_change: NO

## Rows
- none. No raw trust gate rows found.

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
