# vSIGMA API-Enriched Review Board - 2026-08-01

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
- P1_MANUAL_REVIEW | Dundee Utd vs Rangers | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Rangers | pred_total_home_away=25.5/74.5 | 1x2=5.00/3.90/1.64 | ou2.5=3.40/1.28 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
