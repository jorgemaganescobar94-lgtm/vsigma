# vSIGMA Scoring Gap Explainer - 2026-08-06

## Summary
- rows_reviewed: 1
- missing_scored_rows: 1
- no_data_blocked_rows: 0
- not_trusted_rows: 0
- promoted_rows: 0
- gap_status_counts: MISSING_SCORED_ROW=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.
- auto_apply: NO
- production_change: NO

## Gap Rows
- Dundee Utd vs Rangers | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
