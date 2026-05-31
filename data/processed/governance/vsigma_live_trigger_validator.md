# vSIGMA Live Trigger Validator - 2026-05-31

## Summary
- rows_validated: 4
- window_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- live_trigger_counts: TOO_EARLY=2; MATCH_FINISHED=1; TOO_LATE=1
- auto_apply: NO
- production_change: NO

## Rows
- #1 | window=TOO_EARLY | decision=TOO_EARLY | Cordoba vs Huesca | market=OVER_1_5_SUPPORTED | status=NS | min=0 | mtko=633.49 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window
- #2 | window=MATCH_FINISHED | decision=MATCH_FINISHED | RB Bragantino vs Internacional | market=OVER_1_5_SUPPORTED | status=FT | min=90.0 | mtko=333.43 | score=3-1 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=match already final
- #3 | window=TOO_LATE | decision=TOO_LATE | Almeria vs Valladolid | market=OVER_1_5_SUPPORTED | status=2H | min=56.0 | mtko=483.51 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=live window passed
- #4 | window=TOO_EARLY | decision=TOO_EARLY | Vasco DA Gama vs Atletico-MG | market=BTTS_YES_REVIEW | status=NS | min=0 | mtko=633.42 | score=0-0 | shots=0 | SoT=0 | corners=0 | signal=0 | reason=outside useful live window

## Guardrails
- Diagnostic only; no execution.
- Manual review required for any action.
