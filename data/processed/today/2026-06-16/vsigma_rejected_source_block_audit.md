# vSIGMA Rejected Source Block Audit - 2026-06-16

## Summary
- rows_reviewed: 3
- rejected_rows: 3
- correct_reject_rows: 1
- manual_review_rows: 2
- whitelist_candidate_rows: 2
- audit_bucket_counts: MANUAL_REVIEW_POSSIBLE_WHITELIST=2; CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=1
- review_priority_counts: P1_REVIEW_CANDIDATE=2; P3_CORRECT_REJECT=1
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Al Qadsia vs Al Salmiyah | league=Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Barki Tajik vs Parvoz | league=Vysshaya Liga | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
