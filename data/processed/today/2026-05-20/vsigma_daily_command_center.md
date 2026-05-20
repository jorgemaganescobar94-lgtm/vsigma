# vSIGMA Daily Command Center - 2026-05-20

## Executive Command
- generated_at: 2026-05-20T21:38:51+01:00
- mode: auto
- command_center_status: EXECUTION_READY
- daily_classification: EXECUTION_OK
- action_level: NO_ACTION_REQUIRED
- operational_verdict: EXECUTION_AVAILABLE
- predictive_failure: UNKNOWN
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/26188564975

## Next Operator Action
- Review official executable picks and post-result quality once scores are labeled.

## Decision Snapshot
- decision_outcome_rows: 5
- official_action_counts: EXECUTABLE=2; WAIT=2; NO_BET=1
- execution_family_status_counts: PRELOCK_CONFIRMED=2; WAITING_FOR_WINDOW=2; EXPIRED=1

## Quality Snapshot
- decision_quality_rows: 5
- decision_quality_labels: WAIT_UNRESOLVED=2; ACTIONABLE_WIN=1; ACTIONABLE_UNRESOLVED=1; EXPIRED_PRELOCK_UNRESOLVED=1
- quality_buckets: NEEDS_MORE_DATA=4; GOOD_DECISION=1

## Source Coverage
- monitoring_summary: present — `data/processed/today/2026-05-20/vsigma_autonomous_monitoring_summary.md`
- decision_quality_review: present — `data/processed/today/2026-05-20/vsigma_decision_quality_review.md`
- system_review: present — `data/processed/today/2026-05-20/vsigma_system_review.md`
- prelock_resolver: present — `data/processed/today/2026-05-20/vsigma_prelock_decision_resolver.md`
- cloud_decision_summary: present — `data/processed/today/2026-05-20/vsigma_cloud_decision_summary.md`
- decision_outcome_ledger: present — `data/processed/today/2026-05-20/vsigma_decision_outcome_ledger.csv`

## Operating Rules
- ACTION_REQUIRED: inspect before trusting the day.
- REVIEW_HOLD: no urgent alert, but follow the next state transition.
- EXECUTION_READY: executable decision exists; review execution and post-result later.
- NO_ACTION_REQUIRED: no execution needed.
- No predictive formulas, thresholds, calibration, or market logic are changed by this command center.
