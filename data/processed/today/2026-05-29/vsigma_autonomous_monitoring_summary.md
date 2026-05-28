# vSIGMA Autonomous Monitoring Summary - 2026-05-29

## Executive Status
- generated_at: 2026-05-29T00:06:01+01:00
- mode: auto
- daily_classification: DATA_BLOCKED
- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- action_level: ACTION_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/26607428973

## Operator Action
- Check provider/API coverage, odds availability, lineups, and data-gap flags before executing.

## Explanation
- Execution was blocked by data or prelock availability, not by a scored market losing.

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
