# vSIGMA Real Shortlist Recovery Diagnostic - 2026-06-05

## Summary
- overall_status: SCORING_SOURCE_EMPTY_FOR_DATE
- root_cause: scored source exists but has no rows for target date
- root_scored_same_day_rows: 0
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Refresh/fix scoring source date coverage.
- auto_apply: NO
- production_change: NO

## Component Rows
- root_scored_matches | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/matches_vsigma_scored_v3.csv | detail=file exists but has no data rows
- dated_scored_matches | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/matches_vsigma_scored_v3.csv | detail=file exists but has no data rows
- today_execution_shortlist | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_today_execution_shortlist.csv | detail=file is not present
- today_execution_bets_only | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_today_execution_bets_only.csv | detail=file is not present
- context_adjusted_final_picks | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_context_adjusted_final_picks.csv | detail=file is not present
- real_objective_context_gate | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_real_objective_context_gate.csv | detail=file is not present
- objective_context_execution_bridge | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_objective_context_execution_bridge.csv | detail=file is not present
- candidate_provenance_ledger | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-05/vsigma_candidate_provenance_ledger.csv | detail=file is not present

## Guardrails
- This diagnostic never creates picks or stake permission.
- Real candidate recovery must come from scored/selection outputs, not from proxy bridge rows.
- Proxy-only availability remains NO_BET through provenance ceiling.
