# vSIGMA Source Reliability Learning - 2026-08-18

## Summary
- source_rows: 15
- sample_gate_counts: INSUFFICIENT_SAMPLE=14; OBSERVE_ONLY_SAMPLE=1
- source_learning_status_counts: HOLD_SAMPLE=14; OBSERVE_ONLY=1
- recommended_weight_action_counts: NO_WEIGHT_CHANGE=15
- manual_review_required_counts: NO=15
- auto_apply: NO
- production_change: NO

## Source Rows
- club_official_hint | status=REVIEW_ONLY | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- footballtransfers | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- gffn | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- guardian_predicted | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- lequipe | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- local_media_generic | status=REVIEW_ONLY | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- madeinfoot | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- maxifoot | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- ninetymin | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- rotowire | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- sports_gambler | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- sportskeeda | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- sportsmole | status=ACTIVE | eval=16 promoted=8 learning=7 | avg=0.614 | gate=OBSERVE_ONLY_SAMPLE | signal=OBSERVE_ONLY | action=NO_WEIGHT_CHANGE | manual=NO
- standard_sport | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO
- whoscored | status=ACTIVE | eval=0 promoted=0 learning=0 | avg=0.000 | gate=INSUFFICIENT_SAMPLE | signal=HOLD_SAMPLE | action=NO_WEIGHT_CHANGE | manual=NO

## Guardrails
- This source learning report is advisory only and never edits source registry or weights.
- Parser failures alone cannot downgrade a source; parser/mapping review comes first.
- Upweight/downweight candidates require sufficient sample and manual confirmation.
- No picks, stakes, production changes, or whitelist changes are created here.
