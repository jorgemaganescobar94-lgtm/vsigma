# vSIGMA API-Enriched Scored Candidates - 2026-07-08

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
- Vikingur Reykjavik vs Gyori ETO FC | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=pred_total_home_away=0/0 | 1x2=2.45/3.40/2.50 | ou2.5=3.10/1.33 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Lincoln Red Imps FC vs Inter Club d'Escaldes | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=pred_total_home_away=0/0 | 1x2=2.15/3.35/3.05 | ou2.5=1.90/1.85 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
