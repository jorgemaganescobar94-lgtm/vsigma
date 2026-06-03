# [vSIGMA SAFE PR] 2026-06-03 - MEDIUM reporting/ops improvements

## Summary
- target_date: 2026-06-03
- safe_candidates: 1
- auto_merge: NO
- production_change: NO

## Allowed Scope
- Reporting/brief cleanup
- Workflow ordering/diagnostics
- Health/issue reporting

## Forbidden Scope
- Prediction formulas
- Stake logic
- Market selection
- Odds/price thresholds
- Calibration auto-apply

## Candidate Improvements
- MEDIUM | workflow_order | OPERATOR_BEFORE_HEALTH | evidence=operator brief health_status=UNKNOWN | recommendation=Schedule health monitor before operator brief.

## Review Instructions
- This PR is review-only.
- Do not merge if it changes prediction, stake, market or calibration logic.
- If the proposal is accepted, implement in a separate reviewed commit/PR unless the patch is purely reporting/formatting.
