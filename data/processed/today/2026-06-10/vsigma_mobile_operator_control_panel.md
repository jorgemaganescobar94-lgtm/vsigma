# vSIGMA Mobile Operator Control Panel - 2026-06-10

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
- hard_guard: WARN | commit_allowed=YES
- learning_sanity: WARN
- shadow_active: 0 | high=0 | metrics=none
- promotion_candidates: 0 | decisions=none

## Cards
- MOBILE_STATUS | status=STOP | betting_permission=NO; final_decision=SYSTEM_FIX_REQUIRED; action_level=BROKEN; alert_route=CRITICAL_STOP | next=Fix blocking guard/operator issue before trusting outputs.
- OPERATOR | status=BROKEN | final_decision=SYSTEM_FIX_REQUIRED; alert_route=CRITICAL_STOP; sanity=PASS | next=Read operator brief only if status is REVIEW_NOW/LIVE/STOP.
- LEARNING_GUARD | status=WARN | commit_allowed=YES; decisions=WARN_ONLY=7 | next=If BLOCK_COMMIT, rerun/fix learning chain before trusting outputs.
- LEARNING_SANITY | status=WARN | sanity=EMPTY_NO_FALLBACK=7; severity=WARN=7 | next=Review warnings before calibration decisions.
- SHADOW_QUEUE | status=INACTIVE_OR_STABLE | active=0; high=0; metrics=none; decisions=none | next=Shadow only; no production change.
- PROMOTION_READINESS | status=NO_PROMOTION | promotion_candidates=0; decisions=none | next=Manual review only if promotion candidate appears.

## Mobile Sources
- operator: data/processed/today/2026-06-10/vsigma_operator_brief.csv
- shadow_queue: data/processed/governance/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/governance/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-10/vsigma_learning_chain_output_sanity.csv
- hard_guard: data/processed/today/2026-06-10/vsigma_learning_chain_empty_output_guard.csv

## Guardrails
- This panel is read-only governance.
- It does not execute bets.
- It does not edit forecast formulas.
- It does not enable production changes.

## Shadow Forecast A/B
- ab_status: UNAVAILABLE
- ab_metrics: none
- ab_verdicts: none
- ab_source: data/processed/governance/vsigma_shadow_forecast_ab_summary.csv
- auto_apply: NO
- production_change: NO

## Shadow A/B Quality Gate
- ab_quality_status: NO_DATA
- quality_gates: NO_DATA=1
- quality_priorities: NONE=1
- usable_metrics: none
- bad_metrics: none
- blocked_metrics: none
- ab_quality_source: data/processed/today/2026-06-10/vsigma_shadow_ab_quality_gate.csv
- auto_apply: NO
- production_change: NO
