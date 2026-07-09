# vSIGMA Promotion Input Bridge - 2026-07-09

## Summary
- source_rows_reviewed: 2
- bridge_rows_written: 2
- promotion_ready_review_only_rows: 1
- blocked_rows: 1
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=1; BLOCKED_NOT_SCORING_READY=1
- signal_band_counts: LOW_SIGNAL_REVIEW=1; WEAK_SIGNAL=1
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=1; NO_PROMOTION_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Bridge Rows
- ML Vitebsk vs Universitatea Craiova | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=40 band=LOW_SIGNAL_REVIEW | summary=pred_total_home_away=0/0 | 1x2=5.50/3.55/1.60 | ou2.5=2.10/1.70 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Petrocub vs Egnatia Rrogozhinë | bridge=BLOCKED_NOT_SCORING_READY | score=10 band=WEAK_SIGNAL | summary= | promotion=NO_PROMOTION_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
