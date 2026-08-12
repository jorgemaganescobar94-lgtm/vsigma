# vSIGMA API-Enriched Promotion Gate Adapter - 2026-08-12

## Summary
- source_rows_reviewed: 1
- adapter_rows_written: 1
- adapter_promoted_review_only_rows: 1
- adapter_blocked_rows: 0
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=1
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Kairat Almaty vs Levski Sofia | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=61 | summary=prediction_winner=Levski Sofia | pred_total_home_away=52.0/48.0 | 1x2=2.62/3.10/2.76 | ou2.5=2.45/1.53 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
