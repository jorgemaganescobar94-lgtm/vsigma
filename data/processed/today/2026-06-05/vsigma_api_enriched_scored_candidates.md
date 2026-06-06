# vSIGMA API-Enriched Scored Candidates - 2026-06-05

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
- Castellón vs Almeria | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Castellón | pred_total_home_away=56.8/43.2 | 1x2=1.81/3.75/4.00 | ou2.5=1.62/2.25 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- HK Kopavogur vs Afturelding | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Afturelding | pred_total_home_away=43.8/56.2 | 1x2=2.90/4.00/2.00 | ou2.5=2.40/1.50 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
