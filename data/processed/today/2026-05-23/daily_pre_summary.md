# vSIGMA Daily Decision Journal - Pre

- Date: 2026-05-23
- Timezone: Atlantic/Canary

## Pipeline Counts

| Bucket | Rows |
| --- | ---: |
| Approved premium | 11 |
| Approved standard | 0 |
| Downgraded | 15 |
| Blocked | 1 |
| Watch | 1 |

## SAFE Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Bologna vs Inter | Serie A | AWAY_WIN | BET | PREMIUM_CORE | 155.008 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_DRAW_LIVE; market=AWAY_WIN; edge=0.341; market_fit=SAFE_OK |
| 2 | Kashima vs FC Tokyo | J1 League | OVER_1_5 | BET | PREMIUM_EXTENDED | 101.721 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.156; market_fit=SAFE_OK |

## BALANCED Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Bologna vs Inter | Serie A | AWAY_WIN | BET | PREMIUM_CORE | 155.008 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_DRAW_LIVE; market=AWAY_WIN; edge=0.341; market_fit=SAFE_OK |
| 2 | Lazio vs Pisa | Serie A | HOME_WIN | BET | PREMIUM_CORE | 144.052 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_DRAW_LIVE; market=HOME_WIN; edge=0.274; market_fit=SAFE_OK |
| 3 | Kashima vs FC Tokyo | J1 League | OVER_1_5 | BET | PREMIUM_EXTENDED | 101.721 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.156; market_fit=SAFE_OK |
| 4 | Kalmar FF vs Degerfors IF | Allsvenskan | OVER_1_5 | BET | PREMIUM_EXTENDED | 98.471 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.149; market_fit=SAFE_OK |

## Execution Shortlist

### #1 Bologna vs Inter
- League: Serie A
- Market: AWAY_WIN
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 155.008
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_DRAW_LIVE; market=AWAY_WIN; edge=0.341; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=1; phase=PREMIUM_CORE; execution_score=155.008; selection_score=101.940; primary_edge=0.341; primary_model_prob=0.799; shortlist_rank=2; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

### #2 Lazio vs Pisa
- League: Serie A
- Market: HOME_WIN
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 144.052
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_DRAW_LIVE; market=HOME_WIN; edge=0.274; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=2; phase=PREMIUM_CORE; execution_score=144.052; selection_score=97.690; primary_edge=0.274; primary_model_prob=0.842; shortlist_rank=4; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

### #3 Kashima vs FC Tokyo
- League: J1 League
- Market: OVER_1_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 101.721
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.156; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=3; phase=PREMIUM_EXTENDED; execution_score=101.721; selection_score=81.130; primary_edge=0.156; primary_model_prob=0.870; shortlist_rank=21; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #4 Kalmar FF vs Degerfors IF
- League: Allsvenskan
- Market: OVER_1_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 98.471
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.149; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=4; phase=PREMIUM_EXTENDED; execution_score=98.471; selection_score=78.610; primary_edge=0.149; primary_model_prob=0.863; shortlist_rank=22; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

## Match Script Forecasts

### #1 Kashima vs FC Tokyo
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.6; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.4-2.1; away 1.4-2.1; total 3.0-4.1
- Shots: home 10-14; away 12-16; SOT 2-4 vs 4-6
- Corners / possession: 7-11; home 51-59% / away 41-49%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Kalmar FF vs Degerfors IF
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.5; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.2-1.9; away 1.6-2.3; total 2.9-4.0
- Shots: home 9-13; away 10-14; SOT 3-5 vs 4-6
- Corners / possession: 6-10; home 43-51% / away 49-57%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.
