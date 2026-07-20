# vSIGMA API-Enriched Review Board - 2026-07-20

## Summary
- source_rows_reviewed: 3
- review_rows_written: 3
- ready_for_manual_review_rows: 3
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=3
- review_board_status_counts: API_ENRICHED_REVIEW_READY=3
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Review Rows
- P1_MANUAL_REVIEW | Hammarby FF vs Degerfors IF | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Hammarby FF | pred_total_home_away=70.3/29.7 | 1x2=1.22/5.75/13.00 | ou2.5=1.50/2.60 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Halmstad vs BK Hacken | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=BK Hacken | pred_total_home_away=33.7/66.5 | 1x2=5.20/4.33/1.55 | ou2.5=1.50/2.62 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | FC Anyang vs Gwangju FC | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=FC Anyang | pred_total_home_away=65.8/34.2 | 1x2=1.55/3.75/6.25 | ou2.5=2.00/1.80 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
