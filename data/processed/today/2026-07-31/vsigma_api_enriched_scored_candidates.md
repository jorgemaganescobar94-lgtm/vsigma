# vSIGMA API-Enriched Scored Candidates - 2026-07-31

## Summary
- source_rows_reviewed: 4
- candidate_rows_written: 4
- scoring_ready_pending_gates_rows: 4
- missing_required_rows: 0
- coverage_only_rows: 0
- diagnostic_only_rows: 0
- status_counts: API_ENRICHED_SCORING_READY_PENDING_GATES=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- auto_apply: NO
- production_change: NO

## Candidate Rows
- IF Brommapojkarna vs Hammarby FF | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Hammarby FF | pred_total_home_away=34.2/65.8 | 1x2=6.80/4.60/1.40 | ou2.5=1.50/2.60 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- KFUM Oslo vs Molde | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Molde | pred_total_home_away=47.8/52.2 | 1x2=3.00/3.60/2.20 | ou2.5=1.67/2.15 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Remo vs Vitoria | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Remo | pred_total_home_away=55.3/44.7 | 1x2=2.20/3.40/3.15 | ou2.5=4.75/1.15 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Aalesund vs Viking | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Viking | pred_total_home_away=34.8/65.2 | 1x2=5.80/4.50/1.48 | ou2.5=1.40/2.88 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
