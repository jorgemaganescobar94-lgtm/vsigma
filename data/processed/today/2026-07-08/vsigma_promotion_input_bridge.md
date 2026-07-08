# vSIGMA Promotion Input Bridge - 2026-07-08

## Summary
- source_rows_reviewed: 2
- bridge_rows_written: 2
- promotion_ready_review_only_rows: 2
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=2
- signal_band_counts: LOW_SIGNAL_REVIEW=2
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Bridge Rows
- Vikingur Reykjavik vs Gyori ETO FC | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=40 band=LOW_SIGNAL_REVIEW | summary=pred_total_home_away=0/0 | 1x2=2.45/3.40/2.50 | ou2.5=3.10/1.33 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Lincoln Red Imps FC vs Inter Club d'Escaldes | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=40 band=LOW_SIGNAL_REVIEW | summary=pred_total_home_away=0/0 | 1x2=2.15/3.35/3.05 | ou2.5=1.90/1.85 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
