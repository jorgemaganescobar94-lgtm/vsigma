# vSIGMA API-Enriched Promotion Gate Adapter - 2026-06-05

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
- Castellón vs Almeria | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=75 | summary=prediction_winner=Castellón | pred_total_home_away=56.8/43.2 | 1x2=1.81/3.75/4.00 | ou2.5=1.62/2.25 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- HK Kopavogur vs Afturelding | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=73 | summary=prediction_winner=Afturelding | pred_total_home_away=43.8/56.2 | 1x2=2.90/4.00/2.00 | ou2.5=2.40/1.50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
