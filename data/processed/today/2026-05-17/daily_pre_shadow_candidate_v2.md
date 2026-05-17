# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-17
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
| 1 | Catanzaro vs Palermo | Serie B | OVER_1_5 | BET | PREMIUM_EXTENDED | 121.648 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.190; market_fit=SAFE_OK |
| 2 | Atletico Paranaense vs Flamengo | Serie A | OVER_1_5 | BET | PREMIUM_EXTENDED | 116.881 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.169; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Catanzaro vs Palermo
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.0; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.4-2.1; away 1.9-2.6; total 3.5-4.6
- Shots: home 11-15; away 10-14; SOT 5-7 vs 4-6
- Corners / possession: 7-11; home 52-60% / away 40-48%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Atletico Paranaense vs Flamengo
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.7; stats=FULL.
- Scoreline: main 1-3; alt 0-3
- xG: home 0.8-1.5; away 2.2-2.9; total 3.1-4.2
- Shots: home 12-16; away 9-13; SOT 4-6 vs 3-5
- Corners / possession: 6-10; home 48-56% / away 44-52%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Atletico Paranaense vs Flamengo | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.801 | 0.803 | 123.472 | 123.740 |
| BOTH | Catanzaro vs Palermo | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.827 | 0.830 | 127.553 | 127.988 |
