# vSIGMA Daily Command Center - 2026-06-07

## Executive Command
- generated_at: 2026-06-07T09:40:46+01:00
- mode: auto
- command_center_status: REVIEW_HOLD
- daily_classification: WAITING_FOR_PRELOCK
- action_level: REVIEW_REQUIRED
- operational_verdict: WAITING_FOR_PRELOCK
- predictive_failure: NO
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/27087595351

## Next Operator Action
- Wait for next scheduled AUTO/PRELOCK run or rerun prelock manually if timing is critical.

## Decision Snapshot
- decision_outcome_rows: 1
- official_action_counts: WAIT=1
- execution_family_status_counts: WAITING_FOR_WINDOW=1

## Quality Snapshot
- decision_quality_rows: 1
- decision_quality_labels: WAIT_UNRESOLVED=1
- quality_buckets: NEEDS_MORE_DATA=1

## Source Coverage
- monitoring_summary: present — `data/processed/today/2026-06-07/vsigma_autonomous_monitoring_summary.md`
- decision_quality_review: present — `data/processed/today/2026-06-07/vsigma_decision_quality_review.md`
- system_review: present — `data/processed/today/2026-06-07/vsigma_system_review.md`
- prelock_resolver: present — `data/processed/today/2026-06-07/vsigma_prelock_decision_resolver.md`
- cloud_decision_summary: present — `data/processed/today/2026-06-07/vsigma_cloud_decision_summary.md`
- decision_outcome_ledger: present — `data/processed/today/2026-06-07/vsigma_decision_outcome_ledger.csv`

## Operating Rules
- ACTION_REQUIRED: inspect before trusting the day.
- REVIEW_HOLD: no urgent alert, but follow the next state transition.
- EXECUTION_READY: executable decision exists; review execution and post-result later.
- NO_ACTION_REQUIRED: no execution needed.
- No predictive formulas, thresholds, calibration, or market logic are changed by this command center.
