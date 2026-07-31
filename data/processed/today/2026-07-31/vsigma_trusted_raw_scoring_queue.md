# vSIGMA Trusted Raw Scoring Queue - 2026-07-31

## Summary
- queue_rows: 4
- priority_counts: P1_TRUSTED_MISSING_SCORING=4
- scoring_needed_counts: YES=4
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | IF Brommapojkarna vs Hammarby FF | league=Allsvenskan | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | KFUM Oslo vs Molde | league=Eliteserien | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Remo vs Vitoria | league=Serie A | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | Aalesund vs Viking | league=Eliteserien | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
