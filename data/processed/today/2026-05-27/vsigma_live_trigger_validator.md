# vSIGMA Live Trigger Validator - 2026-05-27

## Summary
- rows_validated: 4
- window_counts: MATCH_FINISHED=2; TOO_EARLY=2
- live_trigger_counts: MATCH_FINISHED=2; TOO_EARLY=2
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.52 | score=3-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=10.53 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=TOO_EARLY | decision=TOO_EARLY | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1120.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=1300.47 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.
