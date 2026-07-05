# vSIGMA Promotion Input Bridge - 2026-07-05

## Summary
- source_rows_reviewed: 2
- bridge_rows_written: 2
- promotion_ready_review_only_rows: 2
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=2
- signal_band_counts: HIGH_SIGNAL_REVIEW=2
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Degerfors IF vs Malmo FF | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Malmo FF | pred_total_home_away=34.3/65.7 | 1x2=3.10/3.45/2.20 | ou2.5=1.85/1.95 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Jeonbuk Motors vs Gangwon FC | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=81 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Jeonbuk Motors | pred_total_home_away=58.8/41.2 | 1x2=2.25/3.00/3.35 | ou2.5=2.35/1.57 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
