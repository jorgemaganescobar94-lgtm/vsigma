# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-06-01

## Summary
- rows_reviewed: 1
- promoted_rows: 0
- blocked_rows: 1
- quarantine_rows: 0
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=1
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.
- auto_apply: NO
- production_change: NO

## Rows
- Ponte Preta vs Botafogo SP | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data\processed\matches_league_filtered.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
