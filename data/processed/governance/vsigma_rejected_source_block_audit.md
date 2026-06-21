# vSIGMA Rejected Source Block Audit - 2026-06-21

## Summary
- rows_reviewed: 2
- rejected_rows: 2
- correct_reject_rows: 0
- manual_review_rows: 2
- whitelist_candidate_rows: 1
- audit_bucket_counts: MANUAL_REVIEW_POSSIBLE_WHITELIST=1; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=1
- review_priority_counts: P1_REVIEW_CANDIDATE=1; P2_REVIEW_LOW_CONFIDENCE=1
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Masters FC vs Creck | league=Super League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- 9 de Julio Rafaela vs El Linqueño | league=Torneo Federal A | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
