# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-13
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
| 1 | Lens vs Paris Saint Germain | Ligue 1 | OVER_2_5 | BET | PREMIUM_CORE | 132.513 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.158; market_fit=SAFE_OK |
| 2 | Stockport County vs Stevenage | League One | OVER_1_5 | BET | PREMIUM_EXTENDED | 100.886 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.164; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Lens vs Paris Saint Germain
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.6; stats=FULL.
- Scoreline: main 2-3; alt 1-2
- xG: home 1.6-2.4; away 2.3-3.0; total 4.1-5.2
- Shots: home 14-18; away 10-14; SOT 5-7 vs 4-6
- Corners / possession: 8-12; home 49-57% / away 43-51%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Stockport County vs Stevenage
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.5; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.5-2.2; away 1.3-2.0; total 2.9-4.0
- Shots: home 14-18; away 8-12; SOT 5-7 vs 4-6
- Corners / possession: 8-12; home 56-64% / away 36-44%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Lens vs Paris Saint Germain | 2 | 1.0 | OVER_2_5 | OVER_2_5 | 0.875 | 0.856 | 141.471 | 138.566 |
| BASELINE_ONLY | Alaves vs Barcelona | 1 | NA | OVER_2_5 | NA | 0.848 | NA | 143.319 | NA |
| BOTH | Stockport County vs Stevenage | 3 | 2.0 | OVER_1_5 | OVER_1_5 | 0.794 | 0.779 | 115.299 | 111.781 |
