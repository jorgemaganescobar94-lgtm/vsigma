# vSIGMA Promotion Input Bridge - 2026-07-07

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
- BK Hacken vs Djurgardens IF | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=82 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Djurgardens IF | pred_total_home_away=41.0/59.0 | 1x2=2.45/3.75/2.55 | ou2.5=1.50/2.60 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
