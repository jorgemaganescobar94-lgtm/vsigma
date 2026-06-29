# vSIGMA Scoring Gap Explainer - 2026-06-29

## Summary
- rows_reviewed: 0
- missing_scored_rows: 0
- no_data_blocked_rows: 0
- not_trusted_rows: 0
- promoted_rows: 0
- gap_status_counts: none
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.
- auto_apply: NO
- production_change: NO

## Gap Rows
- none. Promotion gate output missing or empty.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
