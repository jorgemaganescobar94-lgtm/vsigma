# vSIGMA Rejected Source Block Audit - 2026-06-18

## Summary
- rows_reviewed: 2
- rejected_rows: 2
- correct_reject_rows: 2
- manual_review_rows: 0
- whitelist_candidate_rows: 0
- audit_bucket_counts: CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=2
- review_priority_counts: P3_CORRECT_REJECT=2
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- none. All rejected rows were classified as correct rejects.

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
