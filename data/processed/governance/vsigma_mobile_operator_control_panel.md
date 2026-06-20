# vSIGMA Mobile Operator Control Panel - 2026-06-20

## Top Verdict
- mobile_status: LIVE_WAIT
- betting_permission: MANUAL_ONLY
- next_action: Wait/use live validator before any manual live decision.
- auto_apply: NO
- production_change: NO

## At a Glance
- action_level: LIVE
- final_decision: WAIT_LIVE_WINDOW
- alert_route: LOCAL_ONLY
- operator_sanity: PASS
- hard_guard: WARN | commit_allowed=YES
- learning_sanity: WARN
- shadow_active: 0 | high=0 | metrics=none
- promotion_candidates: 0 | decisions=none

## Cards
- MOBILE_STATUS | status=LIVE_WAIT | betting_permission=MANUAL_ONLY; final_decision=WAIT_LIVE_WINDOW; action_level=LIVE; alert_route=LOCAL_ONLY | next=Wait/use live validator before any manual live decision.
- OPERATOR | status=LIVE | final_decision=WAIT_LIVE_WINDOW; alert_route=LOCAL_ONLY; sanity=PASS | next=Read operator brief only if status is REVIEW_NOW/LIVE/STOP.
- LEARNING_GUARD | status=WARN | commit_allowed=YES; decisions=WARN_ONLY=7 | next=If BLOCK_COMMIT, rerun/fix learning chain before trusting outputs.
- LEARNING_SANITY | status=WARN | sanity=EMPTY_NO_FALLBACK=7; severity=WARN=7 | next=Review warnings before calibration decisions.
- SHADOW_QUEUE | status=INACTIVE_OR_STABLE | active=0; high=0; metrics=none; decisions=none | next=Shadow only; no production change.
- PROMOTION_READINESS | status=NO_PROMOTION | promotion_candidates=0; decisions=none | next=Manual review only if promotion candidate appears.

## Mobile Sources
- operator: data/processed/today/2026-06-20/vsigma_operator_brief.csv
- shadow_queue: data/processed/governance/vsigma_calibration_shadow_patch_queue.csv
- promotion_readiness: data/processed/governance/vsigma_shadow_patch_promotion_readiness.csv
- learning_sanity: data/processed/today/2026-06-20/vsigma_learning_chain_output_sanity.csv
- hard_guard: data/processed/today/2026-06-20/vsigma_learning_chain_empty_output_guard.csv

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
- ab_quality_source: data/processed/today/2026-06-20/vsigma_shadow_ab_quality_gate.csv
- auto_apply: NO
- production_change: NO
