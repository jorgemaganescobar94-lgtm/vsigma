# vSIGMA Rejected Source Block Audit - 2026-06-16

## Summary
- rows_reviewed: 5
- rejected_rows: 5
- correct_reject_rows: 0
- manual_review_rows: 5
- whitelist_candidate_rows: 5
- audit_bucket_counts: MANUAL_REVIEW_POSSIBLE_WHITELIST=5
- review_priority_counts: P1_REVIEW_CANDIDATE=5
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Fortune vs Real de Banjul | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- GPA vs Team Rhino | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Hart Acedemy vs Brikama United | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Medina United vs Dutch Lions | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Samger vs Bombada | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
