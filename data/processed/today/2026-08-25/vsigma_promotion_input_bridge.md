# vSIGMA Promotion Input Bridge - 2026-08-25

## Summary
- source_rows_reviewed: 3
- bridge_rows_written: 3
- promotion_ready_review_only_rows: 3
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=3
- signal_band_counts: HIGH_SIGNAL_REVIEW=2; LOW_SIGNAL_REVIEW=1
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Fenerbahçe vs Lyon | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=92 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Fenerbahçe | pred_total_home_away=62.5/37.5 | 1x2=1.99/3.60/3.45 | ou2.5=1.80/2.00 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Dinamo Zagreb vs Viking | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=40 band=LOW_SIGNAL_REVIEW | summary=pred_total_home_away=0/0 | 1x2=1.64/4.10/4.65 | ou2.5=1.57/2.35 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Independ. Rivadavia vs Fluminense | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Independ. Rivadavia | pred_total_home_away=65.2/34.8 | 1x2=2.62/2.82/3.00 | ou2.5=7.00/1.07 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
