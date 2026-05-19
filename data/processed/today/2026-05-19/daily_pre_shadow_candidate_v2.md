# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-19
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
| 1 | Monza vs Juve Stabia | Serie B | OVER_1_5 | BET | PREMIUM_CORE | 131.327 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.139; market_fit=SAFE_OK |
| 2 | Coquimbo Unido vs Deportes Tolima | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_EXTENDED | 110.097 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.163; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Monza vs Juve Stabia
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.3; stats=FULL.
- Scoreline: main 2-1; alt 1-1
- xG: home 1.6-2.3; away 1.0-1.7; total 2.8-3.9
- Shots: home 14-18; away 10-14; SOT 4-6 vs 3-5
- Corners / possession: 7-11; home 46-54% / away 46-54%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Coquimbo Unido vs Deportes Tolima
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.5; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.4-2.1; away 1.5-2.1; total 3.0-4.1
- Shots: home 8-12; away 12-16; SOT 3-5 vs 4-6
- Corners / possession: 6-10; home 37-45% / away 55-63%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Coquimbo Unido vs Deportes Tolima | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.784 | 0.787 | 118.597 | 119.377 |
| BOTH | Monza vs Juve Stabia | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.780 | 0.776 | 153.514 | 149.854 |
