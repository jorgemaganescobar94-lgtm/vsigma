# vSIGMA Trusted Raw Scoring Queue - 2026-07-13

## Summary
- queue_rows: 2
- priority_counts: P1_TRUSTED_MISSING_SCORING=2
- scoring_needed_counts: YES=2
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Ulsan Hyundai FC vs Jeonbuk Motors | league=K League 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Gwangju FC vs Pohang Steelers | league=K League 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
