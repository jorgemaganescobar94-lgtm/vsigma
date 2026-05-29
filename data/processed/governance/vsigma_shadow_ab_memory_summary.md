# vSIGMA Shadow A/B Historical Memory - 2026-05-29

## Summary
- metrics_reviewed: 4
- memory_verdicts: MEMORY_PROMOTION_BLOCKED_SAMPLE=2; MEMORY_NO_CLEAR_SIGNAL=2
- auto_apply: NO
- production_change: NO

## Metric Memory
- total_corners | verdict=MEMORY_PROMOTION_BLOCKED_SAMPLE | latest=PROMOTION_BLOCKED | days=1 | usable=0 | bad=0 | blocked=1 | delta_mean=0.333 | reason=Improvement exists but recent history remains sample-blocked.
- total_fouls | verdict=MEMORY_PROMOTION_BLOCKED_SAMPLE | latest=PROMOTION_BLOCKED | days=1 | usable=0 | bad=0 | blocked=1 | delta_mean=0.433 | reason=Improvement exists but recent history remains sample-blocked.
- total_goals | verdict=MEMORY_NO_CLEAR_SIGNAL | latest=NO_CLEAR_AB_EDGE | days=1 | usable=0 | bad=0 | blocked=0 | delta_mean=0.006 | reason=Recent history does not show a decisive A/B direction.
- total_sot | verdict=MEMORY_NO_CLEAR_SIGNAL | latest=NO_CLEAR_AB_EDGE | days=1 | usable=0 | bad=0 | blocked=0 | delta_mean=0.000 | reason=Recent history does not show a decisive A/B direction.

## Guardrails
- Historical memory is advisory only.
- No forecast formula changes are made.
- No official pick changes are made.
- Manual review is required before any promotion.
