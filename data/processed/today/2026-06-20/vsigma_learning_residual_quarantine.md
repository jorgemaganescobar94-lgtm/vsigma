# vSIGMA Learning Residual Quarantine - 2026-06-20

## Summary
- rows_reviewed: 4
- usable_closed_samples: 0
- model_blocking_rows: 0
- bucket_counts: OPEN_RESULT_QUARANTINE=2; IDENTITY_QUARANTINE=2
- auto_fix: NO
- production_change: NO

## Rows
- #1 | OPEN_RESULT_QUARANTINE | counts=NO | fixture=1551272 | market=OVER_2_5 | result=UNRESOLVED | reason=Result is not closed; monitor but do not block usable closed samples.
- #2 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #3 | OPEN_RESULT_QUARANTINE | counts=NO | fixture=1551272 | market=OVER_1_5 | result=PENDING | reason=Result is not closed; monitor but do not block usable closed samples.
- #4 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.

## Guardrails
- No data is deleted.
- No model behavior changes.
- Quarantined rows remain auditable but should not block usable closed samples.
