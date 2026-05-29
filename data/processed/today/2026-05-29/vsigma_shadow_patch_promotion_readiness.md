# vSIGMA Shadow Patch Promotion Readiness - 2026-05-29

## Summary
- rows_reviewed: 6
- readiness_decisions: KEEP_SHADOW_TEST=4; NO_PROMOTION_STABLE=2
- readiness_priorities: MEDIUM=3; NONE=2; HIGH=1
- manual_review_required: NO=6
- input_source_path: data/processed/today/2026-05-29/vsigma_calibration_shadow_patch_queue.csv
- auto_apply: NO
- production_change: NO

## Readiness Queue
- total_cards | decision=NO_PROMOTION_STABLE | priority=NONE | manual_review=NO | current=NO_PATCH_STABLE | history_days=3 | latest_rows=6 | bias_consistency=0.667 | status_consistency=1.000 | reason=Current queue is stable; no promotion path.
- total_corners | decision=KEEP_SHADOW_TEST | priority=MEDIUM | manual_review=NO | current=PROMOTE_TO_SHADOW_TEST | history_days=3 | latest_rows=8 | bias_consistency=0.000 | status_consistency=0.000 | reason=Bias signal is not consistent enough across recent history.
- total_fouls | decision=KEEP_SHADOW_TEST | priority=MEDIUM | manual_review=NO | current=PROMOTE_TO_SHADOW_TEST | history_days=3 | latest_rows=9 | bias_consistency=0.333 | status_consistency=0.333 | reason=Bias signal is not consistent enough across recent history.
- total_goals | decision=KEEP_SHADOW_TEST | priority=HIGH | manual_review=NO | current=PROMOTE_TO_SHADOW_TEST | history_days=3 | latest_rows=9 | bias_consistency=1.000 | status_consistency=1.000 | reason=Signal is consistent but sample is still below manual-promotion threshold.
- total_shots | decision=NO_PROMOTION_STABLE | priority=NONE | manual_review=NO | current=NO_PATCH_STABLE | history_days=3 | latest_rows=9 | bias_consistency=0.000 | status_consistency=0.667 | reason=Current queue is stable; no promotion path.
- total_sot | decision=KEEP_SHADOW_TEST | priority=MEDIUM | manual_review=NO | current=PROMOTE_TO_SHADOW_TEST | history_days=3 | latest_rows=8 | bias_consistency=0.333 | status_consistency=0.333 | reason=Bias signal is not consistent enough across recent history.

## Guardrails
- Promotion readiness is advisory only.
- No production change is allowed from this script.
- PROMOTION_CANDIDATE_MANUAL_REVIEW still requires explicit human approval.
