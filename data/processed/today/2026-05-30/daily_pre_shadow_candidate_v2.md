# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-30
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Lab layers: schedule strength + anomaly cleaning

## Shadow Counts

- Baseline official competition rows: 3
- Candidate v2 competition rows: 3
- Overlap rows: 3
- Baseline-only rows: 0
- Candidate-only rows: 0

## Candidate v2 Shadow Top

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | AIK Stockholm vs Sirius | Allsvenskan | OVER_2_5 | BET | PREMIUM_CORE | 135.539 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.207; market_fit=SAFE_OK |
| 2 | Bahia vs Botafogo | Serie A | OVER_2_5 | BET | PREMIUM_CORE | 130.962 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.246; market_fit=SAFE_OK |
| 3 | Paris Saint Germain vs Arsenal | UEFA Champions League | OVER_1_5 | BET | PREMIUM_EXTENDED | 106.091 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.163; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 AIK Stockholm vs Sirius
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.4; stats=FULL.
- Scoreline: main 2-3; alt 1-2
- xG: home 1.2-1.9; away 2.4-3.1; total 3.8-4.9
- Shots: home 11-15; away 12-16; SOT 4-6 vs 3-5
- Corners / possession: 9-13; home 50-58% / away 42-50%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Bahia vs Botafogo
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.4; stats=FULL.
- Scoreline: main 2-3; alt 1-2
- xG: home 1.4-2.1; away 2.3-3.0; total 3.9-5.0
- Shots: home 10-14; away 15-19; SOT 4-6 vs 6-8
- Corners / possession: 10-14; home 47-55% / away 45-53%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #3 Paris Saint Germain vs Arsenal
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.6; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.4-2.1; away 1.5-2.2; total 3.1-4.2
- Shots: home 13-17; away 9-13; SOT 4-6 vs 3-5
- Corners / possession: 8-12; home 50-58% / away 42-50%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Bahia vs Botafogo | 2 | 2 | OVER_2_5 | OVER_2_5 | 0.839 | 0.831 | 137.999 | 137.291 |
| BOTH | AIK Stockholm vs Sirius | 1 | 1 | OVER_2_5 | OVER_2_5 | 0.830 | 0.827 | 142.542 | 142.104 |
| BOTH | Paris Saint Germain vs Arsenal | 3 | 3 | OVER_1_5 | OVER_1_5 | 0.801 | 0.797 | 118.005 | 117.173 |
