# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-24
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 4
- Candidate v2 competition rows: 3
- Overlap rows: 3
- Baseline-only rows: 1
- Candidate-only rows: 0

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Huesca vs Castellón | Segunda División | OVER_2_5 | BET | PREMIUM_CORE | 141.950 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK |
| 2 | Catanzaro vs Monza | Serie B | OVER_1_5 | BET | PREMIUM_EXTENDED | 120.061 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.160; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Huesca vs Castellón
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.2; stats=FULL.
- Scoreline: main 1-3; alt 1-2
- xG: home 0.9-1.6; away 2.5-3.2; total 3.6-4.7
- Shots: home 8-12; away 14-18; SOT 4-6 vs 5-7
- Corners / possession: 8-12; home 40-48% / away 52-60%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Catanzaro vs Monza
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.3-2.0; away 1.8-2.5; total 3.3-4.4
- Shots: home 11-15; away 11-15; SOT 5-7 vs 4-6
- Corners / possession: 7-11; home 50-58% / away 42-50%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Huesca vs Castellón | 2 | 1.0 | OVER_2_5 | OVER_2_5 | 0.810 | 0.802 | 137.759 | 139.809 |
| BOTH | Sporting Gijon vs Almeria | 1 | 2.0 | OVER_2_5 | OVER_2_5 | 0.842 | 0.817 | 142.569 | 136.494 |
| BASELINE_ONLY | Remo vs Atletico Paranaense | 4 | NA | OVER_1_5 | NA | 0.761 | NA | 110.058 | NA |
| BOTH | Catanzaro vs Monza | 3 | 3.0 | OVER_1_5 | OVER_1_5 | 0.819 | 0.815 | 125.787 | 125.039 |
