# vSIGMA Trusted Raw Scoring Queue - 2026-07-16

## Summary
- queue_rows: 3
- priority_counts: P1_TRUSTED_MISSING_SCORING=3
- scoring_needed_counts: YES=3
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Malisheva vs Vllaznia Shkodër | league=UEFA Europa Conference League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Atert Bissen vs KI Klaksvik | league=UEFA Champions League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Universitatea Craiova vs ML Vitebsk | league=UEFA Champions League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
