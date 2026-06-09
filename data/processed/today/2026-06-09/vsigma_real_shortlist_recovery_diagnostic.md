# vSIGMA Real Shortlist Recovery Diagnostic - 2026-06-09

## Summary
- overall_status: REAL_CANDIDATES_AVAILABLE
- root_cause: real shortlist or bets rows exist
- root_scored_same_day_rows: 3
- real_shortlist_rows: 2
- real_bet_rows: 1
- proxy_rows: 0
- next_action: Use normal gates; do not rely on proxy bridge unless real rows fail downstream.
- auto_apply: NO
- production_change: NO

## Component Rows
- root_scored_matches | status=HAS_REAL_ROWS | same_day=3 | real=3 | proxy=0 | bet_like=0 | path=data/processed/matches_vsigma_scored_v3.csv | detail=file has same-day rows
- dated_scored_matches | status=HAS_ROWS | same_day=3 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-09/matches_vsigma_scored_v3.csv | detail=file has same-day rows
- today_execution_shortlist | status=HAS_REAL_ROWS | same_day=1 | real=1 | proxy=0 | bet_like=1 | path=data/processed/today/2026-06-09/vsigma_today_execution_shortlist.csv | detail=file has same-day rows
- today_execution_bets_only | status=HAS_REAL_ROWS | same_day=1 | real=1 | proxy=0 | bet_like=1 | path=data/processed/today/2026-06-09/vsigma_today_execution_bets_only.csv | detail=file has same-day rows
- context_adjusted_final_picks | status=HAS_REAL_ROWS | same_day=1 | real=1 | proxy=0 | bet_like=1 | path=data/processed/today/2026-06-09/vsigma_context_adjusted_final_picks.csv | detail=file has same-day rows
- real_objective_context_gate | status=HAS_ROWS | same_day=1 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-09/vsigma_real_objective_context_gate.csv | detail=file has same-day rows
- objective_context_execution_bridge | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-09/vsigma_objective_context_execution_bridge.csv | detail=file exists but has no data rows
- candidate_provenance_ledger | status=HAS_ROWS | same_day=3 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-09/vsigma_candidate_provenance_ledger.csv | detail=file has same-day rows

## Guardrails
- This diagnostic never creates picks or stake permission.
- Real candidate recovery must come from scored/selection outputs, not from proxy bridge rows.
- Proxy-only availability remains NO_BET through provenance ceiling.
