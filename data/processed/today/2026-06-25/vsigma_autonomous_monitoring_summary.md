# vSIGMA Autonomous Monitoring Summary - 2026-06-25

## Executive Status
- generated_at: 2026-06-26T11:29:08+01:00
- mode: post-yesterday
- daily_classification: TECHNICAL_WARNING
- operational_verdict: TECHNICAL_WARNING
- action_level: ACTION_REQUIRED
- predictive_failure: NO
- evidence_basis: partial_sources
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/28232416883

## Operator Action
- Inspect healthcheck, workflow logs, and artifacts before trusting the day.

## Explanation
- Classification inferred from partial_sources; health_status=UNKNOWN; official_summary=UNKNOWN.

## Source Coverage
- decision_quality_review: missing
- system_review: missing
- healthcheck_report: present
- cloud_decision_summary: missing
- prelock_decision_resolver: missing
- decision_outcome_ledger_rows: 0

## Classification Contract
- EXECUTION_OK: at least one executable decision exists.
- NO_BET_VALID: no executable row and no higher-severity block.
- EXPIRED_PRELOCK: candidate expired before execution; not predictive failure.
- WAITING_FOR_PRELOCK: candidate waiting for configured execution window.
- DATA_BLOCKED: provider/odds/lineup/data gap blocked execution.
- TECHNICAL_WARNING: healthcheck or partial evidence requires inspection.
- BROKEN: required monitoring evidence is missing or inconsistent.
