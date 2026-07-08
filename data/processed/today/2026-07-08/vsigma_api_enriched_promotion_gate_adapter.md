# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-08

## Summary
- source_rows_reviewed: 2
- adapter_rows_written: 2
- adapter_promoted_review_only_rows: 0
- adapter_blocked_rows: 2
- adapter_status_counts: ADAPTER_BLOCKED_WEAK_SIGNAL=2
- allowed_downstream_use_counts: NO_DOWNSTREAM_USE=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Vikingur Reykjavik vs Gyori ETO FC | adapter=ADAPTER_BLOCKED_WEAK_SIGNAL | allowed=NO_DOWNSTREAM_USE | score=40 | summary=pred_total_home_away=0/0 | 1x2=2.45/3.40/2.50 | ou2.5=3.10/1.33 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Lincoln Red Imps FC vs Inter Club d'Escaldes | adapter=ADAPTER_BLOCKED_WEAK_SIGNAL | allowed=NO_DOWNSTREAM_USE | score=40 | summary=pred_total_home_away=0/0 | 1x2=2.15/3.35/3.05 | ou2.5=1.90/1.85 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
