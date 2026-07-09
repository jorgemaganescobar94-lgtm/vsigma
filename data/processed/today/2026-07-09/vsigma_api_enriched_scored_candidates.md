# vSIGMA API-Enriched Scored Candidates - 2026-07-09

## Summary
- source_rows_reviewed: 2
- candidate_rows_written: 2
- scoring_ready_pending_gates_rows: 1
- missing_required_rows: 1
- coverage_only_rows: 0
- diagnostic_only_rows: 0
- status_counts: API_ENRICHED_SCORING_READY_PENDING_GATES=1; MISSING_REQUIRED_API_DATA=1
- pick_permission_counts: NO_PICK_PERMISSION=2
- stake_permission_counts: NO_STAKE_PERMISSION=2
- auto_apply: NO
- production_change: NO

## Candidate Rows
- ML Vitebsk vs Universitatea Craiova | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=pred_total_home_away=0/0 | 1x2=5.50/3.55/1.60 | ou2.5=2.10/1.70 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Petrocub vs Egnatia Rrogozhinë | status=MISSING_REQUIRED_API_DATA | fixture=YES pred=NO odds=NO | summary= | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
