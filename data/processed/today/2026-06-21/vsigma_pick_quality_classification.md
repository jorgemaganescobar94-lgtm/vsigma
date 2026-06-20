# vSIGMA Pick Quality Classification - 2026-06-21

## Summary
- classification_rows: 10
- quality_class_counts: PENDING_FINAL_ACTUALS=10
- error_family_counts: PENDING=10
- learning_action_counts: WAIT_FOR_POSTMATCH_DATA=10
- manual_review_required_counts: NO=10
- auto_apply: NO
- production_change: NO

## Classification Rows
- PENDING_FINAL_ACTUALS | Almeria vs Malaga | market=OVER_1_5_SUPPORTED | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Ceara vs Botafogo SP | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Londrina vs Athletic Club | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Vila Nova vs Nautico Recife | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Banga vs FK Zalgiris Vilnius | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Panevėžys vs Šiauliai | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | TransINVEST Vilnius vs Kauno Žalgiris | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Anápolis vs AO Itabaiana | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Botafogo PB vs Volta Redonda | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.
- PENDING_FINAL_ACTUALS | Santa Cruz vs Ypiranga-RS | market=NO_CLEAR_STAT_MARKET | outcome=PENDING | error=PENDING | action=WAIT_FOR_POSTMATCH_DATA | manual=NO | note=Waiting for final actuals before classifying quality.

## Guardrails
- This classifier labels audit rows; it does not change model weights or picks.
- GREEN/RED labels are candidates until causal review confirms the lesson.
- NO_BET correctness requires real fixture context and manual/causal review.
- Diagnostic rows must not train the model.
