# vSIGMA Promotion Input Bridge - 2026-07-31

## Summary
- source_rows_reviewed: 4
- bridge_rows_written: 4
- promotion_ready_review_only_rows: 4
- blocked_rows: 0
- status_counts: PROMOTION_INPUT_READY_REVIEW_ONLY=4
- signal_band_counts: HIGH_SIGNAL_REVIEW=2; MEDIUM_SIGNAL_REVIEW=2
- promotion_permission_counts: REVIEW_ONLY_PROMOTION_INPUT=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- auto_apply: NO
- production_change: NO

## Bridge Rows
- IF Brommapojkarna vs Hammarby FF | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Hammarby FF | pred_total_home_away=34.2/65.8 | 1x2=6.80/4.60/1.40 | ou2.5=1.50/2.60 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- KFUM Oslo vs Molde | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=61 band=MEDIUM_SIGNAL_REVIEW | summary=prediction_winner=Molde | pred_total_home_away=47.8/52.2 | 1x2=3.00/3.60/2.20 | ou2.5=1.67/2.15 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Remo vs Vitoria | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=70 band=MEDIUM_SIGNAL_REVIEW | summary=prediction_winner=Remo | pred_total_home_away=55.3/44.7 | 1x2=2.20/3.40/3.15 | ou2.5=4.75/1.15 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Aalesund vs Viking | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Viking | pred_total_home_away=34.8/65.2 | 1x2=5.80/4.50/1.48 | ou2.5=1.40/2.88 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
