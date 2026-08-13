# vSIGMA API-Enriched Scored Candidates - 2026-08-13

## Summary
- source_rows_reviewed: 1
- candidate_rows_written: 1
- scoring_ready_pending_gates_rows: 1
- missing_required_rows: 0
- coverage_only_rows: 0
- diagnostic_only_rows: 0
- status_counts: API_ENRICHED_SCORING_READY_PENDING_GATES=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- auto_apply: NO
- production_change: NO

## Candidate Rows
- RB Bragantino vs Atletico-MG | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=RB Bragantino | pred_total_home_away=59.3/40.7 | 1x2=2.12/3.05/3.70 | ou2.5=6.00/1.09 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
