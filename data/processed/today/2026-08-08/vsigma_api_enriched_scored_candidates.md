# vSIGMA API-Enriched Scored Candidates - 2026-08-08

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
- Dundee Utd vs Rangers | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=NO | summary=prediction_winner=Rangers | pred_total_home_away=25.5/74.5 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
