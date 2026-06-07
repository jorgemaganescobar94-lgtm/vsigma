# vSIGMA Learning Residual Quarantine - 2026-06-07

## Summary
- rows_reviewed: 2
- usable_closed_samples: 0
- model_blocking_rows: 0
- bucket_counts: OPEN_RESULT_QUARANTINE=1; IDENTITY_QUARANTINE=1
- auto_fix: NO
- production_change: NO

## Rows
- #1 | OPEN_RESULT_QUARANTINE | counts=NO | fixture=1548053 | market=OVER_1_5 | result=UNRESOLVED | reason=Result is not closed; monitor but do not block usable closed samples.
- #2 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.

## Guardrails
- No data is deleted.
- No model behavior changes.
- Quarantined rows remain auditable but should not block usable closed samples.
