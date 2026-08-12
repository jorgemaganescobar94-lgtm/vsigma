# vSIGMA API-Enriched Manual Review Inspector - 2026-08-12

## Summary
- review_rows: 1
- bucket_counts: P3_REVIEW_LOW_SIGNAL=1
- risk_label_counts: LOW=1
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
- auto_apply: NO
- production_change: NO

## Inspector Rows
- #1 | Kairat Almaty vs Levski Sofia | priority=P2_MANUAL_REVIEW | signal_score=61 | signal_band=MEDIUM_SIGNAL_REVIEW | bucket=P3_REVIEW_LOW_SIGNAL | risk=LOW | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Low/medium review signal. Keep as low-priority manual inspection only.

## Guardrails
- This inspector is triage-only.
- It does not promote to canonical board.
- It does not create picks or stake permission.
- All rows remain NO_CANONICAL_BOARD_PERMISSION, NO_PICK_PERMISSION, NO_STAKE_PERMISSION.
