# vSIGMA API-Enriched Promotion Gate Adapter - 2026-08-06

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
- Dundee Utd vs Rangers | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Rangers | pred_total_home_away=25.5/74.5 | 1x2=5.00/3.90/1.64 | ou2.5=3.40/1.28 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
