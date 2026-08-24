# vSIGMA Probable Lineup Source Reliability Governor - 2026-08-24

## Summary
- sources_reviewed: 15
- sample_gate_counts: INSUFFICIENT_SAMPLE=14; MATURE_SAMPLE=1
- verdict_counts: HOLD_SAMPLE=14; LEARNING_ONLY_SOURCE=1
- recommended_action_counts: KEEP_ACTIVE_COLLECT_MORE_DATA=14; KEEP_ACTIVE_BUT_REQUIRE_PROMOTION_GATE=1
- auto_apply: NO
- production_change: NO

## Source Verdicts
- club_official_hint | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- footballtransfers | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- gffn | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- guardian_predicted | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- lequipe | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- local_media_generic | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- madeinfoot | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- maxifoot | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- ninetymin | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- rotowire | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- sports_gambler | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- sportskeeda | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- sportsmole | verdict=LEARNING_ONLY_SOURCE | gate=MATURE_SAMPLE | evaluated=16 | promoted=8 | learning=7 | avg=0.614 | action=KEEP_ACTIVE_BUT_REQUIRE_PROMOTION_GATE | weight=NO_WEIGHT_CHANGE
- standard_sport | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE
- whoscored | verdict=HOLD_SAMPLE | gate=INSUFFICIENT_SAMPLE | evaluated=0 | promoted=0 | learning=0 | avg=0.000 | action=KEEP_ACTIVE_COLLECT_MORE_DATA | weight=NO_WEIGHT_CHANGE

## Guardrails
- Governor is advisory only and never edits the registry automatically.
- No source is downweighted from parser/extraction failures alone.
- Upweight recommendations require larger samples and manual confirmation.
- No picks, stakes, or production decisions are changed here.
