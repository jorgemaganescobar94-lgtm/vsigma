# vSIGMA API-Enriched Review Board - 2026-06-05

## Summary
- source_rows_reviewed: 2
- review_rows_written: 2
- ready_for_manual_review_rows: 2
- blocked_rows: 0
- review_priority_counts: P2_MANUAL_REVIEW=1; P1_MANUAL_REVIEW=1
- review_board_status_counts: API_ENRICHED_REVIEW_READY=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Review Rows
- P2_MANUAL_REVIEW | Las Palmas vs Malaga | status=API_ENRICHED_REVIEW_READY | score=61 | summary=prediction_winner=Malaga | pred_total_home_away=47.7/52.3 | 1x2=2.22/3.05/3.40 | ou2.5=2.20/1.65 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Binga vs US Bougouba | status=API_ENRICHED_REVIEW_READY | score=82 | summary=prediction_winner=Binga | pred_total_home_away=59.2/41.0 | 1x2=1.70/2.88/5.00 | ou2.5=11.00/1.04 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
