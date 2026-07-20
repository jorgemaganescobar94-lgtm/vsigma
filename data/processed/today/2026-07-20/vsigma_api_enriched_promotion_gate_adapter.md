# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-20

## Summary
- source_rows_reviewed: 3
- adapter_rows_written: 3
- adapter_promoted_review_only_rows: 3
- adapter_blocked_rows: 0
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=3
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Hammarby FF vs Degerfors IF | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Hammarby FF | pred_total_home_away=70.3/29.7 | 1x2=1.22/5.75/13.00 | ou2.5=1.50/2.60 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Halmstad vs BK Hacken | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=BK Hacken | pred_total_home_away=33.7/66.5 | 1x2=5.20/4.33/1.55 | ou2.5=1.50/2.62 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- FC Anyang vs Gwangju FC | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=FC Anyang | pred_total_home_away=65.8/34.2 | 1x2=1.55/3.75/6.25 | ou2.5=2.00/1.80 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
