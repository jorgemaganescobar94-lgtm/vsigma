# vSIGMA Mobile Operator Control Panel - 2026-06-11

## Top Verdict
- mobile_status: OK
- betting_permission: NO
- next_action: No operator action required.
- auto_apply: NO
- production_change: NO

## At a Glance
- action_level: NONE
- final_decision: NO_OPERATOR_ACTION
- alert_route: LOCAL_ONLY
- operator_sanity: PASS
- hard_guard: PASS | commit_allowed=YES
- learning_sanity: PASS
- shadow_active: 0 | high=0 | metrics=none
- promotion_candidates: 0 | decisions=WAIT_MORE_SAMPLE=1

## Cards
- MOBILE_STATUS | status=OK | betting_permission=NO; final_decision=NO_OPERATOR_ACTION; action_level=NONE; alert_route=LOCAL_ONLY | next=No operator action required.
- OPERATOR | status=NONE | final_decision=NO_OPERATOR_ACTION; alert_route=LOCAL_ONLY; sanity=PASS | next=Read operator brief only if status is REVIEW_NOW/LIVE/STOP.
- LEARNING_GUARD | status=PASS | commit_allowed=YES; decisions=PASS=7 | next=If BLOCK_COMMIT, rerun/fix learning chain before trusting outputs.
- LEARNING_SANITY | status=PASS | sanity=PASS=7; severity=OK=7 | next=Review warnings before calibration decisions.
- SHADOW_QUEUE | status=INACTIVE_OR_STABLE | active=0; high=0; metrics=none; decisions=REJECT_LOW_SAMPLE=1 | next=Shadow only; no production change.
- PROMOTION_READINESS | status=NO_PROMOTION | promotion_candidates=0; decisions=WAIT_MORE_SAMPLE=1 | next=Manual review only if promotion candidate appears.

## Mobile Sources
- operator: data/processed/today/2026-06-11/vsigma_operator_brief.csv
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
- ab_quality_source: data/processed/governance/vsigma_shadow_ab_quality_gate.csv
- auto_apply: NO
- production_change: NO
