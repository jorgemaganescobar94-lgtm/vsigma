# vSIGMA Shadow A/B Result Quality Gate - 2026-05-29

## Summary
- rows_reviewed: 4
- quality_gates: NO_CLEAR_AB_EDGE=2; PROMOTION_BLOCKED=2
- priorities: LOW=2; MEDIUM=2
- manual_review_required: NO=4
- auto_apply: NO
- production_change: NO

## Metric Gates
- total_goals | gate=NO_CLEAR_AB_EDGE | priority=LOW | rows=7 | verdict=SHADOW_BETTER_ON_SAMPLE | delta=0.006 | manual_review=NO | reason=A/B result does not show a clear usable edge.
- total_sot | gate=NO_CLEAR_AB_EDGE | priority=LOW | rows=6 | verdict=NO_CLEAR_AB_EDGE | delta=0.000 | manual_review=NO | reason=A/B result does not show a clear usable edge.
- total_corners | gate=PROMOTION_BLOCKED | priority=MEDIUM | rows=6 | verdict=SHADOW_BETTER_ON_SAMPLE | delta=0.333 | manual_review=NO | reason=Shadow improves sample, but promotion is blocked until larger sample.
- total_fouls | gate=PROMOTION_BLOCKED | priority=MEDIUM | rows=6 | verdict=SHADOW_BETTER_ON_SAMPLE | delta=0.433 | manual_review=NO | reason=Shadow improves sample, but promotion is blocked until larger sample.

## Guardrails
- Quality gate is advisory only.
- No production change is allowed.
- No formula or pick changes are made.
- USABLE_SHADOW_SIGNAL still requires explicit manual review.
