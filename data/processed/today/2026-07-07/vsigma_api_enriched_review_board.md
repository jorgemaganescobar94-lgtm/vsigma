# vSIGMA API-Enriched Review Board - 2026-07-07

## Summary
- source_rows_reviewed: 1
- review_rows_written: 1
- ready_for_manual_review_rows: 1
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=1
- review_board_status_counts: API_ENRICHED_REVIEW_READY=1
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- auto_apply: NO
- production_change: NO

## Review Rows
- P1_MANUAL_REVIEW | BK Hacken vs Djurgardens IF | status=API_ENRICHED_REVIEW_READY | score=82 | summary=prediction_winner=Djurgardens IF | pred_total_home_away=41.0/59.0 | 1x2=2.45/3.75/2.55 | ou2.5=1.50/2.60 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
