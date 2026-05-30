# vSIGMA Mobile Operator Control Panel - 2026-05-30

## Top Verdict
- mobile_status: STOP
- betting_permission: NO
- next_action: Fix blocking guard/operator issue before trusting outputs.
- auto_apply: NO
- production_change: NO

## At a Glance
- action_level: BROKEN
- final_decision: SYSTEM_FIX_REQUIRED
- alert_route: CRITICAL_STOP
- operator_sanity: PASS
- hard_guard: PASS | commit_allowed=YES
- learning_sanity: PASS
- shadow_active: 4 | high=4 | metrics=total_corners,total_fouls,total_goals,total_sot
- promotion_candidates: 0 | decisions=KEEP_SHADOW_TEST=4; NO_PROMOTION_STABLE=2

## Cards
- MOBILE_STATUS | status=STOP | betting_permission=NO; final_decision=SYSTEM_FIX_REQUIRED; action_level=BROKEN; alert_route=CRITICAL_STOP | next=Fix blocking guard/operator issue before trusting outputs.
- OPERATOR | status=BROKEN | final_decision=SYSTEM_FIX_REQUIRED; alert_route=CRITICAL_STOP; sanity=PASS | next=Read operator brief only if status is REVIEW_NOW/LIVE/STOP.
- LEARNING_GUARD | status=PASS | commit_allowed=YES; decisions=PASS=7 | next=If BLOCK_COMMIT, rerun/fix learning chain before trusting outputs.
- LEARNING_SANITY | status=PASS | sanity=PASS=7; severity=OK=7 | next=Review warnings before calibration decisions.
- SHADOW_QUEUE | status=ACTIVE | active=4; high=4; metrics=total_corners,total_fouls,total_goals,total_sot; decisions=PROMOTE_TO_SHADOW_TEST=4; NO_PATCH_STABLE=2 | next=Shadow only; no production change.
- PROMOTION_READINESS | status=KEEP_SHADOW_TEST | promotion_candidates=0; decisions=KEEP_SHADOW_TEST=4; NO_PROMOTION_STABLE=2 | next=Manual review only if promotion candidate appears.

## Mobile Sources
- operator: data/processed/today/2026-05-30/vsigma_operator_brief.csv
- shadow_queue: data/processed/governance/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/governance/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/governance/vsigma_learning_chain_output_sanity.csv
- hard_guard: data/processed/governance/vsigma_learning_chain_empty_output_guard.csv

## Guardrails
- This panel is read-only governance.
- It does not execute bets.
- It does not edit forecast formulas.
- It does not enable production changes.

## Shadow Forecast A/B
- ab_status: SHADOW_EDGE
- ab_metrics: total_goals,total_sot,total_corners,total_fouls
- ab_verdicts: SHADOW_BETTER_ON_SAMPLE=3; NO_CLEAR_AB_EDGE=1
- ab_source: data/processed/governance/vsigma_shadow_forecast_ab_summary.csv
- auto_apply: NO
- production_change: NO

## Shadow A/B Quality Gate
- ab_quality_status: PROMOTION_BLOCKED
- quality_gates: NO_CLEAR_AB_EDGE=2; PROMOTION_BLOCKED=2
- quality_priorities: LOW=2; MEDIUM=2
- usable_metrics: none
- bad_metrics: none
- blocked_metrics: total_corners,total_fouls
- ab_quality_source: data/processed/governance/vsigma_shadow_ab_quality_gate.csv
- auto_apply: NO
- production_change: NO
