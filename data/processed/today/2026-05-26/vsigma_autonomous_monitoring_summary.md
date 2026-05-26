# vSIGMA Autonomous Monitoring Summary - 2026-05-26

## Executive Status
- generated_at: 2026-05-26T19:11:50+01:00
- mode: pre
- daily_classification: BROKEN
- operational_verdict: BROKEN
- action_level: ACTION_REQUIRED
- predictive_failure: UNKNOWN
- evidence_basis: missing_sources
- run_url: https://github.com/jorgemaganescobar94-lgtm/vsigma/actions/runs/26466350566

## Operator Action
- Inspect workflow logs and required daily reports; monitoring evidence is incomplete.

## Explanation
- Classification inferred from missing_sources; health_status=UNKNOWN; official_summary=UNKNOWN.

## Source Coverage
- decision_quality_review: missing
- system_review: missing
- healthcheck_report: missing
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
