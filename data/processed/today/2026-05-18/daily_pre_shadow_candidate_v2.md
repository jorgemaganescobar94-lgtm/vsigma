# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-18
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
| 1 | Leganes vs Huesca | Segunda División | OVER_1_5 | BET | PREMIUM_CORE | 121.042 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.132; market_fit=SAFE_OK |
| 2 | Djurgardens IF vs Sirius | Allsvenskan | OVER_2_5 | BET | PREMIUM_CORE | 132.080 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.246; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Leganes vs Huesca
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.7; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.6-2.3; away 1.4-2.1; total 3.2-4.2
- Shots: home 12-16; away 9-13; SOT 4-6 vs 4-6
- Corners / possession: 8-12; home 49-57% / away 43-51%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Djurgardens IF vs Sirius
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.7; stats=FULL.
- Scoreline: main 2-3; alt 1-2
- xG: home 1.8-2.5; away 2.2-2.9; total 4.1-5.2
- Shots: home 14-18; away 11-15; SOT 4-6 vs 3-5
- Corners / possession: 8-12; home 52-60% / away 40-48%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Leganes vs Huesca | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.816 | 0.816 | 152.218 | 152.061 |
| BOTH | Djurgardens IF vs Sirius | 2 | 2 | OVER_2_5 | OVER_2_5 | 0.875 | 0.862 | 141.827 | 140.591 |
