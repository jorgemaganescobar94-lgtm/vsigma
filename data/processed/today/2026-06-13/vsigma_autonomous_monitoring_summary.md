# vSIGMA Autonomous Monitoring Summary - 2026-06-13

## Executive Status
- generated_at: 2026-06-13T00:14:41+01:00
- mode: auto
- daily_classification: NO_BET_VALID
- operational_verdict: NO_EXECUTION_NO_BET_VALID
- action_level: NO_ACTION_REQUIRED
- predictive_failure: NO
- evidence_basis: decision_quality_review
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/27448455973

## Operator Action
- No manual execution needed; keep collecting no-bet evidence.

## Explanation
- The day resolved to no-bet with no executable row and no expired candidate.

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
