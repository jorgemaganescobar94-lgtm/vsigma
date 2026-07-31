# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-31

## Summary
- source_rows_reviewed: 4
- adapter_rows_written: 4
- adapter_promoted_review_only_rows: 4
- adapter_blocked_rows: 0
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=4
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- auto_apply: NO
- production_change: NO

## Adapter Rows
- IF Brommapojkarna vs Hammarby FF | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Hammarby FF | pred_total_home_away=34.2/65.8 | 1x2=6.80/4.60/1.40 | ou2.5=1.50/2.60 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- KFUM Oslo vs Molde | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=61 | summary=prediction_winner=Molde | pred_total_home_away=47.8/52.2 | 1x2=3.00/3.60/2.20 | ou2.5=1.67/2.15 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Remo vs Vitoria | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=70 | summary=prediction_winner=Remo | pred_total_home_away=55.3/44.7 | 1x2=2.20/3.40/3.15 | ou2.5=4.75/1.15 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Aalesund vs Viking | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Viking | pred_total_home_away=34.8/65.2 | 1x2=5.80/4.50/1.48 | ou2.5=1.40/2.88 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
