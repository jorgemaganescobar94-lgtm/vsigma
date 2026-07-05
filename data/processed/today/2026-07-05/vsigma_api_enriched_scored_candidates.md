# vSIGMA API-Enriched Scored Candidates - 2026-07-05

## Summary
- source_rows_reviewed: 2
- candidate_rows_written: 2
- scoring_ready_pending_gates_rows: 2
- missing_required_rows: 0
- coverage_only_rows: 0
- diagnostic_only_rows: 0
- status_counts: API_ENRICHED_SCORING_READY_PENDING_GATES=2
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Degerfors IF vs Malmo FF | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Malmo FF | pred_total_home_away=34.3/65.7 | 1x2=3.10/3.45/2.20 | ou2.5=1.85/1.95 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Jeonbuk Motors vs Gangwon FC | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Jeonbuk Motors | pred_total_home_away=58.8/41.2 | 1x2=2.25/3.00/3.35 | ou2.5=2.35/1.57 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
