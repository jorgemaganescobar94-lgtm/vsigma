# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-21
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 3
- Candidate v2 competition rows: 3
- Overlap rows: 3
- Baseline-only rows: 0
- Candidate-only rows: 0

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Brondby vs FC Copenhagen | Superliga | OVER_2_5 | BET | PREMIUM_CORE | 140.559 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK |
| 2 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_EXTENDED | 117.937 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK |
| 3 | Gremio vs Palestino | CONMEBOL Sudamericana | UNDER_3_5 | BET | PREMIUM_EXTENDED | 99.831 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Brondby vs FC Copenhagen
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.1; stats=FULL.
- Scoreline: main 1-3; alt 1-2
- xG: home 1.1-1.8; away 2.4-3.1; total 3.6-4.7
- Shots: home 13-17; away 12-16; SOT 4-6 vs 4-6
- Corners / possession: 8-12; home 47-55% / away 45-53%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Flamengo vs Estudiantes L.P.
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.9; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 2.0-2.7; away 1.2-1.9; total 3.3-4.4
- Shots: home 12-16; away 11-15; SOT 5-7 vs 4-6
- Corners / possession: 7-11; home 48-56% / away 44-52%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #3 Gremio vs Palestino
- Market: UNDER_3_5
- Script: Controlled script with enough structure to avoid a four-goal game; the breaker is an early goal that opens the match too far. Total-goal lean: 1.7; stats=PARTIAL.
- Scoreline: main 1-0; alt 2-0
- xG: home 0.9-1.6; away 0.1-0.8; total 1.1-2.2
- Shots: home 11-15; away 10-14; SOT 2-4 vs 2-4
- Corners / possession: 5-9; home 51-59% / away 41-49%
- Pick path: Pick wins if game state stays structured and neither side turns the match into repeated transition attacks.
- Pick breaker: An early goal or transition chain breaks the controlled script and creates too many goals.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Gremio vs Palestino | 3 | 3 | UNDER_3_5 | UNDER_3_5 | 0.861 | 0.858 | 111.027 | 110.922 |
| BOTH | Flamengo vs Estudiantes L.P. | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.816 | 0.818 | 125.862 | 126.307 |
| BOTH | Brondby vs FC Copenhagen | 1 | 1 | OVER_2_5 | OVER_2_5 | 0.801 | 0.797 | 137.736 | 137.416 |
