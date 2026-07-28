# vSIGMA API-Enriched Manual Review Inspector - 2026-07-28

## Summary
- review_rows: 4
- bucket_counts: P1_REVIEW_STRONG_SIGNAL=2; P3_REVIEW_LOW_SIGNAL=2
- risk_label_counts: MEDIUM=2; LOW=2
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- next_action: Use this inspector only for human triage. It cannot promote, create picks, or create stake permission.
- auto_apply: NO
- production_change: NO

## Inspector Rows
- #1 | IF Brommapojkarna vs Hammarby FF | priority=P1_MANUAL_REVIEW | signal_score=100 | signal_band=HIGH_SIGNAL_REVIEW | bucket=P1_REVIEW_STRONG_SIGNAL | risk=MEDIUM | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.
- #2 | KFUM Oslo vs Molde | priority=P2_MANUAL_REVIEW | signal_score=61 | signal_band=MEDIUM_SIGNAL_REVIEW | bucket=P3_REVIEW_LOW_SIGNAL | risk=LOW | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Low/medium review signal. Keep as low-priority manual inspection only.
- #3 | Remo vs Vitoria | priority=P2_MANUAL_REVIEW | signal_score=70 | signal_band=MEDIUM_SIGNAL_REVIEW | bucket=P3_REVIEW_LOW_SIGNAL | risk=LOW | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Low/medium review signal. Keep as low-priority manual inspection only.
- #4 | Aalesund vs Viking | priority=P1_MANUAL_REVIEW | signal_score=100 | signal_band=HIGH_SIGNAL_REVIEW | bucket=P1_REVIEW_STRONG_SIGNAL | risk=MEDIUM | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=Strong API-enriched review signal. Human review may inspect first, but no promotion is allowed.

## Guardrails
- This inspector is triage-only.
- It does not promote to canonical board.
- It does not create picks or stake permission.
- All rows remain NO_CANONICAL_BOARD_PERMISSION, NO_PICK_PERMISSION, NO_STAKE_PERMISSION.
