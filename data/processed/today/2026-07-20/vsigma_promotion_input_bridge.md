# vSIGMA Promotion Input Bridge - 2026-07-20

## Summary
- source_rows_reviewed: 3
- bridge_rows_written: 3
- promotion_ready_review_only_rows: 3
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=3
- signal_band_counts: HIGH_SIGNAL_REVIEW=3
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Hammarby FF vs Degerfors IF | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Hammarby FF | pred_total_home_away=70.3/29.7 | 1x2=1.22/5.75/13.00 | ou2.5=1.50/2.60 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Halmstad vs BK Hacken | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=BK Hacken | pred_total_home_away=33.7/66.5 | 1x2=5.20/4.33/1.55 | ou2.5=1.50/2.62 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- FC Anyang vs Gwangju FC | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=FC Anyang | pred_total_home_away=65.8/34.2 | 1x2=1.55/3.75/6.25 | ou2.5=2.00/1.80 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
