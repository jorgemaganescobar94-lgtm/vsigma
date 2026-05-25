# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-25
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
| 1 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | OVER_1_5 | BET | PREMIUM_CORE | 122.036 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.185; market_fit=SAFE_OK |
| 2 | IF Elfsborg vs BK Hacken | Allsvenskan | OVER_2_5 | BET | PREMIUM_CORE | 122.294 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.235; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 SC Paderborn 07 vs VfL Wolfsburg
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.3; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 2.1-2.8; away 1.5-2.2; total 3.7-4.8
- Shots: home 13-17; away 9-13; SOT 4-6 vs 4-6
- Corners / possession: 8-12; home 48-56% / away 44-52%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 IF Elfsborg vs BK Hacken
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.2; stats=FULL.
- Scoreline: main 2-2; alt 2-1
- xG: home 1.7-2.4; away 1.8-2.5; total 3.7-4.8
- Shots: home 10-14; away 11-15; SOT 3-5 vs 3-5
- Corners / possession: 8-12; home 43-51% / away 49-57%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | IF Elfsborg vs BK Hacken | 2 | 2 | OVER_2_5 | OVER_2_5 | 0.822 | 0.808 | 131.523 | 129.461 |
| BOTH | SC Paderborn 07 vs VfL Wolfsburg | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.855 | 0.858 | 155.046 | 155.854 |
