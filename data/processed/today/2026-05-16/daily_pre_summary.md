# vSIGMA Daily Decision Journal - Pre

- Date: 2026-05-16
- Timezone: Atlantic/Canary

## Pipeline Counts

| Bucket | Rows |
| --- | ---: |
| Approved premium | 19 |
| Approved standard | 0 |
| Downgraded | 25 |
| Blocked | 3 |
| Watch | 5 |

## SAFE Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Bayern München vs 1. FC Köln | Bundesliga | BTTS_YES | BET | PREMIUM_CORE | 138.163 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.150; market_fit=SAFE_OK |
| 2 | Granada CF vs Burgos | Segunda División | OVER_1_5 | BET | PREMIUM_EXTENDED | 122.671 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK |

## BALANCED Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Bayern München vs 1. FC Köln | Bundesliga | BTTS_YES | BET | PREMIUM_CORE | 138.163 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.150; market_fit=SAFE_OK |
| 2 | SC Freiburg vs RB Leipzig | Bundesliga | OVER_2_5 | BET | PREMIUM_CORE | 134.021 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.123; market_fit=SAFE_OK |
| 3 | Almeria vs Las Palmas | Segunda División | OVER_2_5 | BET | PREMIUM_EXTENDED | 127.697 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.284; market_fit=SAFE_OK |
| 4 | Granada CF vs Burgos | Segunda División | OVER_1_5 | BET | PREMIUM_EXTENDED | 122.671 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK |
| 5 | Juve Stabia vs Monza | Serie B | OVER_1_5 | BET | PREMIUM_EXTENDED | 124.124 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.202; market_fit=SAFE_OK |

## Execution Shortlist

### #1 Bayern München vs 1. FC Köln
- League: Bundesliga
- Market: BTTS_YES
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 138.163
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.150; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=1; phase=PREMIUM_CORE; execution_score=138.163; selection_score=104.180; primary_edge=0.150; primary_model_prob=0.817; shortlist_rank=1; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

### #2 SC Freiburg vs RB Leipzig
- League: Bundesliga
- Market: OVER_2_5
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 134.021
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.123; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=2; phase=PREMIUM_CORE; execution_score=134.021; selection_score=102.730; primary_edge=0.123; primary_model_prob=0.781; shortlist_rank=3; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

### #3 Almeria vs Las Palmas
- League: Segunda División
- Market: OVER_2_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 127.697
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.284; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=3; phase=PREMIUM_EXTENDED; execution_score=127.697; selection_score=94.300; primary_edge=0.284; primary_model_prob=0.855; shortlist_rank=21; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #4 Juve Stabia vs Monza
- League: Serie B
- Market: OVER_1_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 124.124
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.202; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=4; phase=PREMIUM_EXTENDED; execution_score=124.124; selection_score=98.920; primary_edge=0.202; primary_model_prob=0.847; shortlist_rank=11; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #5 Granada CF vs Burgos
- League: Segunda División
- Market: OVER_1_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 122.671
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=5; phase=PREMIUM_EXTENDED; execution_score=122.671; selection_score=93.710; primary_edge=0.240; primary_model_prob=0.893; shortlist_rank=22; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

## Match Script Forecasts

### #1 SC Freiburg vs RB Leipzig
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.1; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.3-2.0; away 2.1-2.8; total 3.6-4.7
- Shots: home 12-16; away 15-19; SOT 3-5 vs 5-7
- Corners / possession: 7-11; home 42-50% / away 50-58%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Granada CF vs Burgos
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 1.2-1.9; away 1.9-2.6; total 3.3-4.4
- Shots: home 9-13; away 8-12; SOT 3-5 vs 3-5
- Corners / possession: 6-10; home 50-58% / away 42-50%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #3 Juve Stabia vs Monza
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.3; stats=FULL.
- Scoreline: main 1-2; alt 0-2
- xG: home 1.0-1.7; away 1.6-2.3; total 2.8-3.9
- Shots: home 10-14; away 14-18; SOT 3-5 vs 4-6
- Corners / possession: 7-11; home 46-54% / away 46-54%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.
