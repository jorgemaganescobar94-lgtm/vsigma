# vSIGMA Daily Decision Journal - Shadow Candidate v2 Pre

- Date: 2026-05-14
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
| 1 | Valencia vs Rayo Vallecano | La Liga | OVER_1_5 | BET | PREMIUM_CORE | 121.951 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.135; market_fit=SAFE_OK |
| 2 | Bradford vs Bolton | League One | OVER_1_5 | BET | PREMIUM_CORE | 113.472 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.136; market_fit=SAFE_OK |

## Candidate v2 Match Script Forecasts

### #1 Valencia vs Rayo Vallecano
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.4; stats=FULL.
- Scoreline: main 1-2; alt 0-2
- xG: home 1.0-1.7; away 1.7-2.4; total 2.8-3.9
- Shots: home 12-16; away 13-17; SOT 3-5 vs 5-7
- Corners / possession: 7-11; home 43-51% / away 49-57%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Bradford vs Bolton
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.6-2.3; away 1.5-2.2; total 3.2-4.3
- Shots: home 11-15; away 13-17; SOT 3-5 vs 4-6
- Corners / possession: 8-12; home 45-53% / away 47-55%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

## Baseline vs Candidate v2

| Status | Fixture | Base Rank | Cand Rank | Base Market | Cand Market | Base Prob | Cand Prob | Base Score | Cand Score |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: |
| BOTH | Valencia vs Rayo Vallecano | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.783 | 0.782 | 147.275 | 149.998 |
| BOTH | Bradford vs Bolton | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.825 | 0.820 | 144.711 | 143.721 |
