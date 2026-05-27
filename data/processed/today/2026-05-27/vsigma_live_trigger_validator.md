# vSIGMA Live Trigger Validator - 2026-05-27

## Summary
- rows_validated: 4
- window_counts: MATCH_FINISHED=1; TOO_LATE=3
- live_trigger_counts: MATCH_FINISHED=1; TOO_LATE=3
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=46.25 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #2 | window=TOO_LATE | decision=TOO_LATE | Libertad Asuncion vs UCV | market=OVER_1_5_SUPPORTED | status=HT | min=45.0 | mtko=226.25 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed
- #3 | window=TOO_LATE | decision=TOO_LATE | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | status=HT | min=45.0 | mtko=226.22 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed
- #4 | window=TOO_LATE | decision=TOO_LATE | Independiente del Valle vs Rosario Central | market=OVER_1_5_SUPPORTED | status=HT | min=45.0 | mtko=226.26 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.
