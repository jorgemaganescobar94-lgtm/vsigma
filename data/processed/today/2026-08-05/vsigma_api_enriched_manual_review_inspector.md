# vSIGMA API-Enriched Manual Review Inspector - 2026-08-05

## Summary
- review_rows: 1
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=1
- risk_label_counts: MEDIUM=1
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
- auto_apply: NO
- production_change: NO

## Inspector Rows
- #1 | Dundee Utd vs Rangers | priority=P1_MANUAL_REVIEW | signal_score=100 | signal_band=HIGH_SIGNAL_REVIEW | bucket=P1_REVIEW_STRONG_SIGNAL | risk=MEDIUM | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.

## Guardrails
- This inspector is triage-only.
- It does not promote to canonical board.
- It does not create picks or stake permission.
- All rows remain NO_CANONICAL_BOARD_PERMISSION, NO_PICK_PERMISSION, NO_STAKE_PERMISSION.
