# vSIGMA Rejected Source Block Audit - 2026-06-21

## Summary
- rows_reviewed: 1
- rejected_rows: 1
- correct_reject_rows: 0
- manual_review_rows: 1
- whitelist_candidate_rows: 0
- audit_bucket_counts: REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=1
- review_priority_counts: P2_REVIEW_LOW_CONFIDENCE=1
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- The Town vs Ventura County | league=MLS Next Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
