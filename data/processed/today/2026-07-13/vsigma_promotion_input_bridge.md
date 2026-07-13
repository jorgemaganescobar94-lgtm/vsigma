# vSIGMA Promotion Input Bridge - 2026-07-13

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
- Ulsan Hyundai FC vs Jeonbuk Motors | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=94 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Jeonbuk Motors | pred_total_home_away=37.0/63.2 | 1x2=2.75/3.30/2.45 | ou2.5=1.95/1.83 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Gwangju FC vs Pohang Steelers | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Pohang Steelers | pred_total_home_away=29.2/71.0 | 1x2=5.80/3.50/1.64 | ou2.5=2.25/1.62 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
