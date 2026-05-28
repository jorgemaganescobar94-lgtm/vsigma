# vSIGMA Learning Residual Quarantine - 2026-05-28

## Summary
- rows_reviewed: 10
- usable_closed_samples: 1
- model_blocking_rows: 0
- bucket_counts: IDENTITY_QUARANTINE=9; USABLE_CLOSED_SAMPLE=1
- auto_fix: NO
- production_change: NO

## Rows
- #1 | USABLE_CLOSED_SAMPLE | counts=YES | fixture=1535315 | market=OVER_2_5 | result=WIN | reason=Resolved actionable sample; eligible for pattern counting.
- #2 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #3 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #4 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #5 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #6 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #7 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #8 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #9 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #10 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.

## Guardrails
- No data is deleted.
- No model behavior changes.
- Quarantined rows remain auditable but should not block usable closed samples.
