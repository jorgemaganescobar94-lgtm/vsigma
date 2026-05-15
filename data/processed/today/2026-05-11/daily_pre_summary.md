# vSIGMA Daily Decision Journal - Pre

- Date: 2026-05-11
- Timezone: Atlantic/Canary

## Pipeline Counts

| Bucket | Rows |
| --- | ---: |
| Approved premium | 3 |
| Approved standard | 0 |
| Downgraded | 6 |
| Blocked | 2 |
| Watch | 1 |

## SAFE Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Benfica vs SC Braga | Primeira Liga | BTTS_YES | BET | PREMIUM_CORE | 143.104 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.241; market_fit=SAFE_OK |
| 2 | Napoli vs Bologna | Serie A | HOME_WIN | BET | PREMIUM_CORE | 131.948 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_DRAW_LIVE; market=HOME_WIN; edge=0.155; market_fit=SAFE_OK |

## BALANCED Picks

| Rank | Fixture | League | Market | Rec | Bucket | Score | Why | Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | Benfica vs SC Braga | Primeira Liga | BTTS_YES | BET | PREMIUM_CORE | 143.104 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.241; market_fit=SAFE_OK |
| 2 | Napoli vs Bologna | Serie A | HOME_WIN | BET | PREMIUM_CORE | 131.948 | STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE | FAILURE_MODE_DRAW_LIVE; market=HOME_WIN; edge=0.155; market_fit=SAFE_OK |

## Execution Shortlist

### #1 Benfica vs SC Braga
- League: Primeira Liga
- Market: BTTS_YES
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 143.104
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_BTTS_BREAK; market=BTTS_YES; edge=0.241; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=1; phase=PREMIUM_CORE; execution_score=143.104; selection_score=100.000; primary_edge=0.241; primary_model_prob=0.765; shortlist_rank=2; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+LEAGUE_COVERAGE

### #2 Napoli vs Bologna
- League: Serie A
- Market: HOME_WIN
- Bucket: PREMIUM_CORE
- Recommendation: BET
- Execution score: 131.948
- Main why: STRONG_ROLLING_STATS;CLEAN_MARKET_FIT;CORE_GATE_PASSED;EDGE_ABOVE_THRESHOLD;MODEL_PROB_STRONG;BET_EXECUTABLE
- Primary risk: FAILURE_MODE_DRAW_LIVE; market=HOME_WIN; edge=0.155; market_fit=SAFE_OK
- Bucket rationale: PREMIUM_CORE: CORE_GATE_PASSED; APPROVED_PREMIUM; BET; SAFE_OK
- Rank rationale: EXECUTION_SHORTLIST_SORT: execution_rank=2; phase=PREMIUM_CORE; execution_score=131.948; selection_score=97.460; primary_edge=0.155; primary_model_prob=0.776; shortlist_rank=4; caps=league2_market2_fixture1
- Confirmation layers: STATS+ODDS+MARKET_TRANSLATION+FORM+ADVISORY_AVAILABILITY+LEAGUE_COVERAGE
