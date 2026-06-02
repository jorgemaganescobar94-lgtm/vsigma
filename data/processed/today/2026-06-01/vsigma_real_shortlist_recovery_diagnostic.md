# vSIGMA Real Shortlist Recovery Diagnostic - 2026-06-01

## Summary
- overall_status: FILTERS_TOO_STRICT_OR_SELECTOR_NOT_RUN
- root_cause: scoring has same-day rows but real shortlist/bets outputs are absent or empty
- root_scored_same_day_rows: 1
- real_shortlist_rows: 0
- real_bet_rows: 0
- proxy_rows: 0
- next_action: Run/repair real selection step from scored matches into shortlist/bets-only outputs.
- auto_apply: NO
- production_change: NO

## Component Rows
- root_scored_matches | status=HAS_REAL_ROWS | same_day=1 | real=1 | proxy=0 | bet_like=0 | path=data/processed/matches_vsigma_scored_v3.csv | detail=file has same-day rows
- dated_scored_matches | status=HAS_ROWS | same_day=1 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv | detail=file has same-day rows
- today_execution_shortlist | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_today_execution_shortlist.csv | detail=file exists but has no data rows
- today_execution_bets_only | status=MISSING | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_today_execution_bets_only.csv | detail=file is not present
- context_adjusted_final_picks | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_context_adjusted_final_picks.csv | detail=file exists but has no data rows
- real_objective_context_gate | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_real_objective_context_gate.csv | detail=file exists but has no data rows
- objective_context_execution_bridge | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_objective_context_execution_bridge.csv | detail=file exists but has no data rows
- candidate_provenance_ledger | status=EMPTY | same_day=0 | real=0 | proxy=0 | bet_like=0 | path=data/processed/today/2026-06-01/vsigma_candidate_provenance_ledger.csv | detail=file exists but has no data rows

## Guardrails
- This diagnostic never creates picks or stake permission.
- Real candidate recovery must come from scored/selection outputs, not from proxy bridge rows.
- Proxy-only availability remains NO_BET through provenance ceiling.
