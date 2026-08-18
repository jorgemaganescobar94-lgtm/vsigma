# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-08-18
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
| 1 | Independ. Rivadavia vs Fluminense | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_CORE | 141.776 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK |
| 2 | Dinamo Zagreb vs Viking | UEFA Champions League | OVER_2_5 | BET | PREMIUM_CORE | 122.709 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.244; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Independ. Rivadavia vs Fluminense
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.6; stats=FULL.
- Scoreline: main 2-1; alt 1-1
- xG: home 2.1-2.8; away 0.8-1.5; total 3.1-4.2
- Shots: home 12-16; away 10-14; SOT 4-6 vs 3-5
- Corners / possession: 6-10; home 41-49% / away 51-59%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Dinamo Zagreb vs Viking
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.7; stats=PARTIAL.
- Scoreline: main 2-2; alt 2-1
- xG: home 1.9-2.6; away 2.1-2.8; total 4.2-5.2
- Shots: home 17-21; away 10-14; SOT 4-6 vs 4-6
- Corners / possession: 10-14; home 52-60% / away 40-48%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Independ. Rivadavia vs Fluminense | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.811 | 0.809 | 160.288 | 160.144 |
| BOTH | Dinamo Zagreb vs Viking | 2 | 2 | OVER_2_5 | OVER_2_5 | 0.879 | 0.864 | 135.230 | 133.806 |
