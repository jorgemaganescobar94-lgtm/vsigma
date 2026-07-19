# vSIGMA API-Enriched Promotion Gate Adapter - 2026-07-19

## Summary
- source_rows_reviewed: 3
- adapter_rows_written: 3
- adapter_promoted_review_only_rows: 3
- adapter_blocked_rows: 0
- adapter_status_counts: API_ENRICHED_PROMOTION_REVIEW_READY=3
- allowed_downstream_use_counts: SCORING_REVIEW_ONLY_WITH_NORMAL_GATES=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Adapter Rows
- Malisheva vs Vllaznia Shkodër | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Vllaznia Shkodër | pred_total_home_away=33.0/67.0 | 1x2=1.73/3.70/4.00 | ou2.5=1.77/1.95 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Atert Bissen vs KI Klaksvik | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=KI Klaksvik | pred_total_home_away=33.0/67.0 | 1x2=2.14/3.50/2.96 | ou2.5=1.57/2.30 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Universitatea Craiova vs ML Vitebsk | adapter=API_ENRICHED_PROMOTION_REVIEW_READY | allowed=SCORING_REVIEW_ONLY_WITH_NORMAL_GATES | score=100 | summary=prediction_winner=Universitatea Craiova | pred_total_home_away=80.0/20.0 | 1x2=1.27/5.00/9.60 | ou2.5=1.55/2.35 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This adapter creates review-only promotion candidates, not picks.
- It does not write to the canonical daily execution board.
- It does not create stake permission, market recommendations, or execution permission.
- Normal scoring, promotion, market translation, and operator gates remain mandatory.
- auto_apply=NO and production_change=NO are hardcoded.
