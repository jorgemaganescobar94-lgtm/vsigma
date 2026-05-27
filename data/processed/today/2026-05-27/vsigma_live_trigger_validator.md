# vSIGMA Live Trigger Validator - 2026-05-27

## Summary
- rows_validated: 4
- live_trigger_counts: MATCH_FINISHED=2; MATCH_NOT_LIVE=2
- auto_apply: NO
- production_change: NO

## Rows
- #1 | MATCH_FINISHED | Flamengo vs Cusco | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | score=3-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #2 | MATCH_FINISHED | Club Nacional vs Coquimbo Unido | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | score=1-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | MATCH_NOT_LIVE | Crystal Palace vs Rayo Vallecano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=not live yet
- #4 | MATCH_NOT_LIVE | Olimpia vs A. Italiano | market=OVER_1_5_SUPPORTED | status=NS | min=0 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=not live yet

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.
