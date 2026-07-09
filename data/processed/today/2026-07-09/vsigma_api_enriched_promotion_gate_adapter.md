# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-09

## Summary
- source_rows_reviewed: 2
- adapter_rows_written: 2
- adapter_promoted_review_only_rows: 0
- adapter_blocked_rows: 2
- adapter_status_counts: ADAPTER_BLOCKED_WEAK_SIGNAL=1; ADAPTER_BLOCKED_NOT_READY=1
- allowed_downstream_use_counts: NO_DOWNSTREAM_USE=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Adapter Rows
- ML Vitebsk vs Universitatea Craiova | adapter=ADAPTER_BLOCKED_WEAK_SIGNAL | allowed=NO_DOWNSTREAM_USE | score=40 | summary=pred_total_home_away=0/0 | 1x2=5.50/3.55/1.60 | ou2.5=2.10/1.70 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Petrocub vs Egnatia Rrogozhinë | adapter=ADAPTER_BLOCKED_NOT_READY | allowed=NO_DOWNSTREAM_USE | score=10 | summary= | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
