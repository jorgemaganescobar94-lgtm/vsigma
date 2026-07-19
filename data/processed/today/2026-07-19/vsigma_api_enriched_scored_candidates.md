# vSIGMA API-Enriched Scored Candidates - 2026-07-19

## Summary
- source_rows_reviewed: 3
- candidate_rows_written: 3
- scoring_ready_pending_gates_rows: 3
- missing_required_rows: 0
- coverage_only_rows: 0
- diagnostic_only_rows: 0
- status_counts: API_ENRICHED_SCORING_READY_PENDING_GATES=3
- pick_permission_counts: NO_PICK_PERMISSION=3
- stake_permission_counts: NO_STAKE_PERMISSION=3
- auto_apply: NO
- production_change: NO

## Candidate Rows
- Malisheva vs Vllaznia Shkodër | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Vllaznia Shkodër | pred_total_home_away=33.0/67.0 | 1x2=1.73/3.70/4.00 | ou2.5=1.77/1.95 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Atert Bissen vs KI Klaksvik | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=KI Klaksvik | pred_total_home_away=33.0/67.0 | 1x2=2.14/3.50/2.96 | ou2.5=1.57/2.30 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Universitatea Craiova vs ML Vitebsk | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Universitatea Craiova | pred_total_home_away=80.0/20.0 | 1x2=1.27/5.00/9.60 | ou2.5=1.55/2.35 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
