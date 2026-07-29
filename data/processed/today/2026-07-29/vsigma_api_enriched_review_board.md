# vSIGMA API-Enriched Review Board - 2026-07-29

## Summary
- source_rows_reviewed: 4
- review_rows_written: 4
- ready_for_manual_review_rows: 4
- blocked_rows: 0
- review_priority_counts: P1_MANUAL_REVIEW=2; P2_MANUAL_REVIEW=2
- review_board_status_counts: API_ENRICHED_REVIEW_READY=4
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- auto_apply: NO
- production_change: NO

## Review Rows
- P1_MANUAL_REVIEW | IF Brommapojkarna vs Hammarby FF | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Hammarby FF | pred_total_home_away=34.2/65.8 | 1x2=6.80/4.60/1.40 | ou2.5=1.50/2.60 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P2_MANUAL_REVIEW | KFUM Oslo vs Molde | status=API_ENRICHED_REVIEW_READY | score=61 | summary=prediction_winner=Molde | pred_total_home_away=47.8/52.2 | 1x2=3.00/3.60/2.20 | ou2.5=1.67/2.15 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P2_MANUAL_REVIEW | Remo vs Vitoria | status=API_ENRICHED_REVIEW_READY | score=70 | summary=prediction_winner=Remo | pred_total_home_away=55.3/44.7 | 1x2=2.20/3.40/3.15 | ou2.5=4.75/1.15 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- P1_MANUAL_REVIEW | Aalesund vs Viking | status=API_ENRICHED_REVIEW_READY | score=100 | summary=prediction_winner=Viking | pred_total_home_away=34.8/65.2 | 1x2=5.80/4.50/1.48 | ou2.5=1.40/2.88 | canonical=NO_CANONICAL_BOARD_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This review board is separate from the canonical daily execution board.
- It does not create picks, stake permission, market recommendations, or execution permission.
- Manual review is mandatory before any future scoring/promotion integration.
- auto_apply=NO and production_change=NO are hardcoded.
