# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-07-06

## Summary
- rows_reviewed: 2
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 2
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=2
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.
- auto_apply: NO
- production_change: NO

## Rows
- Degerfors IF vs Malmo FF | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_match_stat_forecasts.csv
- Jeonbuk Motors vs Gangwon FC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_match_stat_forecasts.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
