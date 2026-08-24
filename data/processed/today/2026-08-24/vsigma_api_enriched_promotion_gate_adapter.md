# vSIGMA API-Enriched Promotion Gate Adapter - 2026-08-24

## Summary
- source_rows_reviewed: 3
- adapter_rows_written: 3
- adapter_promoted_review_only_rows: 2
- adapter_blocked_rows: 1
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=2; ADAPTER_BLOCKED_WEAK_SIGNAL=1
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=2; NO_DOWNSTREAM_USE=1
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Fenerbahçe vs Lyon | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=92 | summary=prediction_winner=Fenerbahçe | pred_total_home_away=62.5/37.5 | 1x2=1.99/3.60/3.45 | ou2.5=1.80/2.00 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Dinamo Zagreb vs Viking | adapter=ADAPTER_BLOCKED_WEAK_SIGNAL | allowed=NO_DOWNSTREAM_USE | score=40 | summary=pred_total_home_away=0/0 | 1x2=1.64/4.10/4.65 | ou2.5=1.57/2.35 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Independ. Rivadavia vs Fluminense | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Independ. Rivadavia | pred_total_home_away=65.2/34.8 | 1x2=2.62/2.82/3.00 | ou2.5=7.00/1.07 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
