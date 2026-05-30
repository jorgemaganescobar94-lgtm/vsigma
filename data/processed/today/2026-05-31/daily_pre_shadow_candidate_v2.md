# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-31
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 2
- Candidate v2 competition rows: 2
- Overlap rows: 1
- Baseline-only rows: 1
- Candidate-only rows: 1

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Leganes vs Mirandes | Segunda División | OVER_1_5 | BET | PREMIUM_EXTENDED | 107.544 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.139; market_fit=SAFE_OK |
| 2 | RB Bragantino vs Internacional | Serie A | OVER_1_5 | BET | PREMIUM_EXTENDED | 104.786 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.163; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Leganes vs Mirandes
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.9; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.4-2.1; away 1.8-2.5; total 3.4-4.5
- Shots: home 13-17; away 12-16; SOT 4-6 vs 5-7
- Corners / possession: 9-13; home 46-54% / away 46-54%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 RB Bragantino vs Internacional
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.7; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.9-2.6; away 1.2-1.9; total 3.2-4.3
- Shots: home 10-14; away 11-15; SOT 4-6 vs 4-6
- Corners / possession: 6-10; home 46-54% / away 46-54%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| CANDIDATE_V2_ONLY | Leganes vs Mirandes | NA | 1.0 | NA | OVER_1_5 | NA | 0.822 | NA | 120.390 |
| BOTH | RB Bragantino vs Internacional | 1.0 | 2.0 | OVER_1_5 | OVER_1_5 | 0.805 | 0.807 | 116.500 | 117.003 |
| BASELINE_ONLY | Vasco DA Gama vs Atletico-MG | 2.0 | NA | OVER_1_5 | NA | 0.776 | NA | 109.988 | NA |
