# vSIGMA Promotion Input Bridge - 2026-06-05

## Summary
- source_rows_reviewed: 2
- bridge_rows_written: 2
- promotion_ready_review_only_rows: 2
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=2
- signal_band_counts: HIGH_SIGNAL_REVIEW=1; MEDIUM_SIGNAL_REVIEW=1
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Castellón vs Almeria | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=75 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Castellón | pred_total_home_away=56.8/43.2 | 1x2=1.81/3.75/4.00 | ou2.5=1.62/2.25 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- HK Kopavogur vs Afturelding | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=73 band=MEDIUM_SIGNAL_REVIEW | summary=prediction_winner=Afturelding | pred_total_home_away=43.8/56.2 | 1x2=2.90/4.00/2.00 | ou2.5=2.40/1.50 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
