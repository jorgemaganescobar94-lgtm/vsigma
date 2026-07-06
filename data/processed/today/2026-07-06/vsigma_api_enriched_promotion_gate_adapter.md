# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-06

## Summary
- source_rows_reviewed: 2
- adapter_rows_written: 2
- adapter_promoted_review_only_rows: 2
- adapter_blocked_rows: 0
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=2
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Degerfors IF vs Malmo FF | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Malmo FF | pred_total_home_away=34.3/65.7 | 1x2=3.10/3.45/2.20 | ou2.5=1.85/1.95 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Jeonbuk Motors vs Gangwon FC | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=81 | summary=prediction_winner=Jeonbuk Motors | pred_total_home_away=58.8/41.2 | 1x2=2.25/3.00/3.35 | ou2.5=2.35/1.57 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
