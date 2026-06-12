# vSIGMA Learning Residual Quarantine - 2026-06-12

## Summary
- rows_reviewed: 2
- usable_closed_samples: 0
- model_blocking_rows: 0
- bucket_counts: IDENTITY_QUARANTINE=2
- auto_fix: NO
- production_change: NO

## Rows
- #1 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #2 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.

## Guardrails
- No data is deleted.
- No model behavior changes.
- Quarantined rows remain auditable but should not block usable closed samples.
