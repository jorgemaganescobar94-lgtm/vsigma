# vSIGMA Daily Decision Journal - Pre

- Date: 2026-05-21
- Timezone: Atlantic/Canary

## Pipeline Counts

| Bucket | Rows |
| --- | ---: |
| Approved premium | 14 |
| Approved standard | 0 |
| Downgraded | 6 |
| Blocked | 0 |
| Watch | 1 |

## SAFE Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Deportivo La Guaira vs Independ. Rivadavia | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_CORE | 137.453 | CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE;COVERAGE_RICH_SUPPORT | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.203; market_fit=SAFE_OK |
| 2 | Brondby vs FC Copenhagen | Superliga | OVER_2_5 | BET | PREMIUM_CORE | 141.179 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.252; market_fit=SAFE_OK |
| 3 | Independiente Petrolero vs Botafogo | CONMEBOL Sudamericana | BTTS_YES | BET | PREMIUM_CORE | 141.640 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.257; market_fit=SAFE_OK |

## BALANCED Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Brondby vs FC Copenhagen | Superliga | OVER_2_5 | BET | PREMIUM_CORE | 141.179 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.252; market_fit=SAFE_OK |
| 2 | Independiente Petrolero vs Botafogo | CONMEBOL Sudamericana | BTTS_YES | BET | PREMIUM_CORE | 141.640 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.257; market_fit=SAFE_OK |
| 3 | Deportivo La Guaira vs Independ. Rivadavia | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_CORE | 137.453 | CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE;COVERAGE_RICH_SUPPORT | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.203; market_fit=SAFE_OK |
| 4 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | OVER_1_5 | BET | PREMIUM_EXTENDED | 117.357 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.191; market_fit=SAFE_OK |
| 5 | Gremio vs Palestino | CONMEBOL Sudamericana | UNDER_3_5 | BET | PREMIUM_EXTENDED | 99.671 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.176; market_fit=SAFE_OK |

## Execution Shortlist

### #1 Independiente Petrolero vs Botafogo
- League: CONMEBOL Sudamericana
- Market: BTTS_YES
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 141.640
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.257; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=1; phase=PREMIUM_CORE; execution_score=141.640; selection_score=96.940; primary_edge=0.257; primary_model_prob=0.757; shortlist_rank=5; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #2 Brondby vs FC Copenhagen
- League: Superliga
- Market: OVER_2_5
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 141.179
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.252; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=2; phase=PREMIUM_CORE; execution_score=141.179; selection_score=96.950; primary_edge=0.252; primary_model_prob=0.784; shortlist_rank=4; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE

### #3 Deportivo La Guaira vs Independ. Rivadavia
- League: CONMEBOL Libertadores
- Market: OVER_1_5
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 137.453
- Main why: CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE;COVERAGE_RICH_SUPPORT
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.203; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=3; phase=PREMIUM_CORE; execution_score=137.453; selection_score=98.130; primary_edge=0.203; primary_model_prob=0.870; shortlist_rank=3; caps=league2_market2_fixture1
- Confirmation layers: ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #4 Flamengo vs Estudiantes L.P.
- League: CONMEBOL Libertadores
- Market: OVER_1_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 117.357
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.191; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=4; phase=PREMIUM_EXTENDED; execution_score=117.357; selection_score=93.210; primary_edge=0.191; primary_model_prob=0.896; shortlist_rank=9; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #5 Gremio vs Palestino
- League: CONMEBOL Sudamericana
- Market: UNDER_3_5
- Bucket: PREMIUM_EXTENDED
- Recommendation: BET
- Execution score: 99.671
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;EXTENDED_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.176; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_EXTENDED: EXTENDED_GATE_PASSED; EXTENDED_QUALITY_OK; edge>=0.08; prob>=0.82
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=5; phase=PREMIUM_EXTENDED; execution_score=99.671; selection_score=77.070; primary_edge=0.176; primary_model_prob=0.911; shortlist_rank=20; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

## Match Script Forecasts

### #1 Brondby vs FC Copenhagen
- Market: OVER_2_5
- Script: Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.2; stats=FULL.
- Scoreline: main 1-3; alt 1-2
- xG: home 1.1-1.8; away 2.4-3.1; total 3.6-4.7
- Shots: home 13-17; away 12-16; SOT 4-6 vs 4-6
- Corners / possession: 8-12; home 47-55% / away 45-53%
- Pick path: Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #2 Flamengo vs Estudiantes L.P.
- Market: OVER_1_5
- Script: Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL.
- Scoreline: main 2-2; alt 1-2
- xG: home 2.0-2.7; away 1.2-1.9; total 3.3-4.4
- Shots: home 12-16; away 11-15; SOT 5-7 vs 4-6
- Corners / possession: 7-11; home 48-56% / away 44-52%
- Pick path: Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path.
- Pick breaker: Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market.

### #3 Gremio vs Palestino
- Market: UNDER_3_5
- Script: Controlled script with enough structure to avoid a four-goal game; the breaker is an early goal that opens the match too far. Total-goal lean: 1.7; stats=PARTIAL.
- Scoreline: main 1-0; alt 2-0
- xG: home 0.9-1.6; away 0.1-0.8; total 1.1-2.2
- Shots: home 11-15; away 10-14; SOT 2-4 vs 2-4
- Corners / possession: 5-9; home 51-59% / away 41-49%
- Pick path: Pick wins if game state stays structured and neither side turns the match into repeated transition attacks.
- Pick breaker: An early goal or transition chain breaks the controlled script and creates too many goals.
