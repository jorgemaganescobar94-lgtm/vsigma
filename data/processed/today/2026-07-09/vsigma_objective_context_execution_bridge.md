# vSIGMA Objective Context Execution Bridge - 2026-07-09

## Summary
- rows_bridged: 3
- source: vsigma_real_objective_context_gate.csv
- output: vsigma_today_execution_shortlist.csv only if no real shortlist exists
- bridge_mode: PROXY_BRIDGE_WRITTEN
- auto_apply: NO
- production_change: NO

## Bridge Rows
- #1 | ML Vitebsk vs Universitatea Craiova | market=OVER_2_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_NEUTRAL
- #2 | Zira vs Torpedo Kutaisi | market=OVER_1_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_NEUTRAL
- #3 | Petrocub vs Egnatia Rrogozhinë | market=OVER_1_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_NEUTRAL

## Guardrails
- This bridge creates diagnostic/proxy shortlist rows only; it does not create stake permission.
- If a real shortlist exists, proxy writing is skipped to preserve the real candidate path.
- Proxy rows keep lineups inactive and reliability moderate so execution cannot become premium from this bridge alone.
