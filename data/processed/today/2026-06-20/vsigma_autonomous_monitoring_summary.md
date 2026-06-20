# vSIGMA Autonomous Monitoring Summary - 2026-06-20

## Executive Status
- generated_at: 2026-06-20T20:21:05+01:00
- mode: auto
- daily_classification: EXPIRED_PRELOCK
- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- action_level: REVIEW_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/27881324224

## Operator Action
- Review AUTO/PRELOCK timing; do not count the row as predictive hit-rate failure.

## Explanation
- The candidate expired before execution, so the operational issue is AUTO/PRELOCK timing. This is not a predictive failure and must not be counted in predictive hit-rate metrics.

## Source Coverage
- decision_quality_review: present
- system_review: present
- healthcheck_report: present
- cloud_decision_summary: present
- prelock_decision_resolver: present
- decision_outcome_ledger_rows: 2

## Classification Contract
- EXECUTION_OK: at least one executable decision exists.
- NO_BET_VALID: no executable row and no higher-severity block.
- EXPIRED_PRELOCK: candidate expired before execution; not predictive failure.
- WAITING_FOR_PRELOCK: candidate waiting for configured execution window.
- DATA_BLOCKED: provider/odds/lineup/data gap blocked execution.
- TECHNICAL_WARNING: healthcheck or partial evidence requires inspection.
- BROKEN: required monitoring evidence is missing or inconsistent.
