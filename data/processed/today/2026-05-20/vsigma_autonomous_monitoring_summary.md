# vSIGMA Autonomous Monitoring Summary - 2026-05-20

## Executive Status
- generated_at: 2026-05-20T19:13:32+01:00
- mode: auto
- daily_classification: EXECUTION_OK
- operational_verdict: EXECUTION_AVAILABLE
- action_level: NO_ACTION_REQUIRED
- predictive_failure: UNKNOWN
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/26181175648

## Operator Action
- Review official executable picks and post-result quality once scores are labeled.

## Explanation
- At least one row was executable at decision time.

## Source Coverage
- decision_quality_review: present
- system_review: present
- healthcheck_report: present
- cloud_decision_summary: present
- prelock_decision_resolver: present
- decision_outcome_ledger_rows: 5

## Classification Contract
- EXECUTION_OK: at least one executable decision exists.
- NO_BET_VALID: no executable row and no higher-severity block.
- EXPIRED_PRELOCK: candidate expired before execution; not predictive failure.
- WAITING_FOR_PRELOCK: candidate waiting for configured execution window.
- DATA_BLOCKED: provider/odds/lineup/data gap blocked execution.
- TECHNICAL_WARNING: healthcheck or partial evidence requires inspection.
- BROKEN: required monitoring evidence is missing or inconsistent.
