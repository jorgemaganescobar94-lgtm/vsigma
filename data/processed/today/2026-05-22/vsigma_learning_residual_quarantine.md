# vSIGMA Learning Residual Quarantine - 2026-05-22

## Summary
- rows_reviewed: 6
- usable_closed_samples: 3
- model_blocking_rows: 0
- bucket_counts: USABLE_CLOSED_SAMPLE=3; LOW_INFORMATION_QUARANTINE=2; IDENTITY_QUARANTINE=1
- auto_fix: NO
- production_change: NO

## Rows
- #1 | USABLE_CLOSED_SAMPLE | counts=YES | fixture=1494177 | market=OVER_2_5 | result=WIN | reason=Resolved actionable sample; eligible for pattern counting.
- #2 | USABLE_CLOSED_SAMPLE | counts=YES | fixture=1544652 | market=OVER_1_5 | result=LOSS | reason=Resolved actionable sample; eligible for pattern counting.
- #3 | USABLE_CLOSED_SAMPLE | counts=YES | fixture=1545405 | market=OVER_2_5 | result=LOSS | reason=Resolved actionable sample; eligible for pattern counting.
- #4 | IDENTITY_QUARANTINE | counts=NO | fixture=N/A | market=UNKNOWN | result=UNRESOLVED | reason=Missing fixture or market identity; keep out of model readiness gates.
- #5 | LOW_INFORMATION_QUARANTINE | counts=NO | fixture=1504822 | market=OVER_1_5 | result=UNMATCHED | reason=Low-information row; monitor separately from usable evidence.
- #6 | LOW_INFORMATION_QUARANTINE | counts=NO | fixture=1494182 | market=OVER_1_5 | result=UNMATCHED | reason=Low-information row; monitor separately from usable evidence.

## Guardrails
- No data is deleted.
- No model behavior changes.
- Quarantined rows remain auditable but should not block usable closed samples.
