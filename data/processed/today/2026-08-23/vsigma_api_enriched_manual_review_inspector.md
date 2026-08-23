# vSIGMA API-Enriched Manual Review Inspector - 2026-08-23

## Summary
- review_rows: 2
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=2
- risk_label_counts: MEDIUM=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
- auto_apply: NO
- production_change: NO

## Inspector Rows
- #1 | Fenerbahçe vs Lyon | priority=P1_MANUAL_REVIEW | signal_score=92 | signal_band=HIGH_SIGNAL_REVIEW | bucket=P1_REVIEW_STRONG_SIGNAL | risk=MEDIUM | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.
- #2 | Independ. Rivadavia vs Fluminense | priority=P1_MANUAL_REVIEW | signal_score=100 | signal_band=HIGH_SIGNAL_REVIEW | bucket=P1_REVIEW_STRONG_SIGNAL | risk=MEDIUM | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.

## Guardrails
- This inspector is triage-only.
- It does not promote to canonical board.
- It does not create picks or stake permission.
- All rows remain NO_CANONICAL_BOARD_PERMISSION, NO_PICK_PERMISSION, NO_STAKE_PERMISSION.
