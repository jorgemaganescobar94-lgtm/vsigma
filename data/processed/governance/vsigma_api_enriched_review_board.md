# vSIGMA API-Enriched Review Board - 2026-06-05

## Summary
- source_rows_reviewed: 2
- review_rows_written: 2
- ready_for_manual_review_rows: 2
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=1; P2_MANUAL_REVIEW=1
- review_board_status_counts: API_ENRICHED_REVIEW_READY=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Review Rows
- P1_MANUAL_REVIEW | Castellón vs Almeria | status=API_ENRICHED_REVIEW_READY | score=75 | summary=prediction_winner=Castellón | pred_total_home_away=56.8/43.2 | 1x2=1.81/3.75/4.00 | ou2.5=1.62/2.25 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P2_MANUAL_REVIEW | HK Kopavogur vs Afturelding | status=API_ENRICHED_REVIEW_READY | score=73 | summary=prediction_winner=Afturelding | pred_total_home_away=43.8/56.2 | 1x2=2.90/4.00/2.00 | ou2.5=2.40/1.50 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
