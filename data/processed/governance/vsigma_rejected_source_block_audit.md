# vSIGMA Rejected Source Block Audit - 2026-06-20

## Summary
- rows_reviewed: 4
- rejected_rows: 4
- correct_reject_rows: 0
- manual_review_rows: 4
- whitelist_candidate_rows: 4
- audit_bucket_counts: MANUAL_REVIEW_POSSIBLE_WHITELIST=4
- review_priority_counts: P1_REVIEW_CANDIDATE=4
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Cheongju Showking vs Yangcheon TNT | league=FA Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Seogot vs Areum | league=FA Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Yangsan United vs Anseong | league=FA Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Yeonsu Songdo vs Ulsan FC | league=FA Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
