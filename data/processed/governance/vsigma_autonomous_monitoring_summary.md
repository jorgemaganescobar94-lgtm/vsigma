# vSIGMA Autonomous Monitoring Summary - 2026-06-14

## Executive Status
- generated_at: 2026-06-14T11:50:43+01:00
- mode: pre
- daily_classification: WAITING_FOR_PRELOCK
- operational_verdict: WAITING_FOR_PRELOCK
- action_level: REVIEW_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/27496468851

## Operator Action
- Wait for next scheduled AUTO/PRELOCK run or rerun prelock manually if timing is critical.

## Explanation
- At least one candidate is waiting for the configured PRELOCK window or retry slot.

## Source Coverage
- decision_quality_review: present
- system_review: present
- healthcheck_report: present
- cloud_decision_summary: present
- prelock_decision_resolver: present
- decision_outcome_ledger_rows: 1

## Classification Contract
- EXECUTION_OK: at least one executable decision exists.
- NO_BET_VALID: no executable row and no higher-severity block.
- EXPIRED_PRELOCK: candidate expired before execution; not predictive failure.
- WAITING_FOR_PRELOCK: candidate waiting for configured execution window.
- DATA_BLOCKED: provider/odds/lineup/data gap blocked execution.
- TECHNICAL_WARNING: healthcheck or partial evidence requires inspection.
- BROKEN: required monitoring evidence is missing or inconsistent.
