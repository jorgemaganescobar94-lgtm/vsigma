# vSIGMA API-Enriched Review Board - 2026-07-13

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
- P1_MANUAL_REVIEW | Ulsan Hyundai FC vs Jeonbuk Motors | status=API_ENRICHED_REVIEW_READY | score=94 | summary=prediction_winner=Jeonbuk Motors | pred_total_home_away=37.0/63.2 | 1x2=2.75/3.30/2.45 | ou2.5=1.95/1.83 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Gwangju FC vs Pohang Steelers | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Pohang Steelers | pred_total_home_away=29.2/71.0 | 1x2=5.80/3.50/1.64 | ou2.5=2.25/1.62 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
