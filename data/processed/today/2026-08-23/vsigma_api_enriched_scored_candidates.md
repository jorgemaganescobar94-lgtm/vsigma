# vSIGMA API-Enriched Scored Candidates - 2026-08-23

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
- Fenerbahçe vs Lyon | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Fenerbahçe | pred_total_home_away=62.5/37.5 | 1x2=1.99/3.60/3.45 | ou2.5=1.80/2.00 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Dinamo Zagreb vs Viking | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=pred_total_home_away=0/0 | 1x2=1.64/4.10/4.65 | ou2.5=1.57/2.35 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Independ. Rivadavia vs Fluminense | status=API_ENRICHED_SCORING_READY_PENDING_GATES | fixture=YES pred=YES odds=YES | summary=prediction_winner=Independ. Rivadavia | pred_total_home_away=65.2/34.8 | 1x2=2.62/2.82/3.00 | ou2.5=7.00/1.07 | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- These are scored-candidate inputs only; they do not create picks or stake permission.
- Every row still requires normal scoring, promotion, market translation, and operator gates.
- API enrichment alone is never enough to recommend a market.
- auto_apply=NO and production_change=NO are hardcoded.
