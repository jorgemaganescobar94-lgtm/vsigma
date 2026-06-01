# vSIGMA Objective Context Execution Bridge - 2026-06-01

## Summary
- rows_bridged: 4
- source: vsigma_real_objective_context_gate.csv
- output: vsigma_today_execution_shortlist.csv
- bridge_mode: BASE_PROXY_FROM_OBJECTIVE_GATE
- auto_apply: NO
- production_change: NO

## Bridge Rows
- #1 | Cordoba vs Huesca | market=OVER_2_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_TEMPO
- #2 | Almeria vs Valladolid | market=OVER_2_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_TEMPO
- #3 | RB Bragantino vs Internacional | market=OVER_1_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_TEMPO
- #4 | Vasco DA Gama vs Atletico-MG | market=OVER_1_5 | recommendation=BET | guard=BASE_PROXY_FROM_OBJECTIVE_GATE_TEMPO

## Guardrails
- This bridge creates diagnostic/proxy shortlist rows only; it does not create stake permission.
- Downstream gates still control objective availability, forecast confidence, translator, board and No Bet states.
- Proxy rows keep lineups inactive and reliability moderate so execution cannot become premium from this bridge alone.
