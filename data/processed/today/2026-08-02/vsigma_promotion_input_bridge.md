# vSIGMA Promotion Input Bridge - 2026-08-02

## Summary
- source_rows_reviewed: 1
- bridge_rows_written: 1
- promotion_ready_review_only_rows: 1
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=1
- signal_band_counts: HIGH_SIGNAL_REVIEW=1
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Dundee Utd vs Rangers | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Rangers | pred_total_home_away=25.5/74.5 | 1x2=5.00/3.90/1.64 | ou2.5=3.40/1.28 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
