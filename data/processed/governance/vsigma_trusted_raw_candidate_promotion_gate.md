# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-08-21

## Summary
- rows_reviewed: 3
- promoted_rows: 0
- blocked_rows: 0
- quarantine_rows: 3
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=3
- next_action: No promotion unless TRUSTED_RAW_SOURCE has non-blocked scored data. Keep No Bet for blocked rows.
- auto_apply: NO
- production_change: NO

## Rows
- Fenerbahçe vs Lyon | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Independ. Rivadavia vs Fluminense | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Dinamo Zagreb vs Viking | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_match_stat_forecasts.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
