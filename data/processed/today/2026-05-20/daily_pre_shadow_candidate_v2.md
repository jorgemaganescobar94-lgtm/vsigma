# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-20
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 3
- Candidate v2 competition rows: 2
- Overlap rows: 2
- Baseline-only rows: 1
- Candidate-only rows: 0

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Santa Fe vs Platense | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_CORE | 139.010 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.246; market_fit=SAFE_OK |
| 2 | SC Freiburg vs Aston Villa | UEFA Europa League | OVER_1_5 | BET | PREMIUM_EXTENDED | 110.006 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.168; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Santa Fe vs Platense
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.6; stats=FULL.
- Scoreline: main 2-1; alt 1-1
- xG: home 1.8-2.5; away 1.1-1.8; total 3.0-4.1
- Shots: home 10-14; away 13-17; SOT 4-6 vs 4-6
- Corners / possession: 5-9; home 42-50% / away 50-58%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 SC Freiburg vs Aston Villa
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.3-2.0; away 1.8-2.5; total 3.2-4.3
- Shots: home 10-14; away 12-16; SOT 4-6 vs 4-6
- Corners / possession: 6-10; home 43-51% / away 49-57%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BASELINE_ONLY | Gais vs Hammarby FF | 2 | NA | OVER_2_5 | NA | 0.800 | NA | 137.648 | NA |
| BOTH | Santa Fe vs Platense | 1 | 1.0 | OVER_1_5 | OVER_1_5 | 0.800 | 0.803 | 156.448 | 156.688 |
| BOTH | SC Freiburg vs Aston Villa | 3 | 2.0 | OVER_1_5 | OVER_1_5 | 0.817 | 0.812 | 122.530 | 121.308 |
