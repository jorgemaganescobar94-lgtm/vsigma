# vSIGMA API-Enriched Review Board - 2026-08-23

## Summary
- source_rows_reviewed: 2
- review_rows_written: 2
- ready_for_manual_review_rows: 2
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=2
- review_board_status_counts: API_ENRICHED_REVIEW_READY=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Review Rows
- P1_MANUAL_REVIEW | Fenerbahçe vs Lyon | status=API_ENRICHED_REVIEW_READY | score=92 | summary=prediction_winner=Fenerbahçe | pred_total_home_away=62.5/37.5 | 1x2=1.99/3.60/3.45 | ou2.5=1.80/2.00 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Independ. Rivadavia vs Fluminense | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Independ. Rivadavia | pred_total_home_away=65.2/34.8 | 1x2=2.62/2.82/3.00 | ou2.5=7.00/1.07 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
