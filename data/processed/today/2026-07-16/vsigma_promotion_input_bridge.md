# vSIGMA Promotion Input Bridge - 2026-07-16

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
- Malisheva vs Vllaznia Shkodër | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Vllaznia Shkodër | pred_total_home_away=33.0/67.0 | 1x2=1.73/3.70/4.00 | ou2.5=1.77/1.95 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Atert Bissen vs KI Klaksvik | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=KI Klaksvik | pred_total_home_away=33.0/67.0 | 1x2=2.14/3.50/2.96 | ou2.5=1.57/2.30 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Universitatea Craiova vs ML Vitebsk | bridge=PROMOTION_INPUT_READY_REVIEW_ONLY | score=100 band=HIGH_SIGNAL_REVIEW | summary=prediction_winner=Universitatea Craiova | pred_total_home_away=80.0/20.0 | 1x2=1.27/5.00/9.60 | ou2.5=1.55/2.35 | promotion=REVIEW_ONLY_PROMOTION_INPUT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This bridge only prepares review inputs for normal gates.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Promotion permission is review-only and cannot bypass normal scoring/promotion/market/operator gates.
- auto_apply=NO and production_change=NO are hardcoded.
