# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-27
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 2
- Candidate v2 competition rows: 2
- Overlap rows: 2
- Baseline-only rows: 0
- Candidate-only rows: 0

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Crystal Palace vs Rayo Vallecano | UEFA Europa Conference League | OVER_1_5 | BET | PREMIUM_CORE | 128.997 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.196; market_fit=SAFE_OK |
| 2 | Independiente del Valle vs Rosario Central | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_CORE | 126.943 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.219; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Crystal Palace vs Rayo Vallecano
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.7; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.2-1.9; away 1.8-2.5; total 3.1-4.2
- Shots: home 10-14; away 13-17; SOT 3-5 vs 4-6
- Corners / possession: 7-11; home 43-51% / away 49-57%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Independiente del Valle vs Rosario Central
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.9; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.5-2.2; away 1.7-2.4; total 3.3-4.4
- Shots: home 12-16; away 11-15; SOT 3-5 vs 4-6
- Corners / possession: 8-12; home 47-55% / away 45-53%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Independiente del Valle vs Rosario Central | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.832 | 0.831 | 154.531 | 154.283 |
| BOTH | Crystal Palace vs Rayo Vallecano | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.808 | 0.813 | 156.432 | 157.482 |
