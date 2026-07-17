# vSIGMA API-Enriched Review Board - 2026-07-17

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
- P1_MANUAL_REVIEW | Malisheva vs Vllaznia Shkodër | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Vllaznia Shkodër | pred_total_home_away=33.0/67.0 | 1x2=1.73/3.70/4.00 | ou2.5=1.77/1.95 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Atert Bissen vs KI Klaksvik | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=KI Klaksvik | pred_total_home_away=33.0/67.0 | 1x2=2.14/3.50/2.96 | ou2.5=1.57/2.30 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Universitatea Craiova vs ML Vitebsk | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Universitatea Craiova | pred_total_home_away=80.0/20.0 | 1x2=1.27/5.00/9.60 | ou2.5=1.55/2.35 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
