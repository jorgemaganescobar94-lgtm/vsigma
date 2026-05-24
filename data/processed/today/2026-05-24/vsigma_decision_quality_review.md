# vSIGMA Decision Quality Review - 2026-05-24

## Executive Summary
- generated_at: 2026-05-24T21:18:30+01:00
- daily_classification: EXECUTION_OK
- no_bet_classification: EXECUTION_ACTIONABLE_PRESENT
- operational_verdict: EXECUTION_AVAILABLE
- predictive_failure: UNKNOWN
- rows reviewed: 8
- actionable rows: 1
- non-actionable rows: 7
- resolved rows: 1
- unresolved rows: 7
- good decisions: 0
- bad decisions: 1
- neutral/unresolved: 7
- top improvement signal: WAIT_FOR_POST_RESULTS (3)
- current recommendation: Do not recalibrate; collect more labeled outcomes.
- operational note: At least one row was executable at decision time.

## Daily Operational Classification
- classification: EXECUTION_OK
- no_bet_validity: EXECUTION_ACTIONABLE_PRESENT
- current_operational_verdict: EXECUTION_AVAILABLE
- explanation: At least one row was executable at decision time.

## Decision Quality Table
| fixture | market_primary | official_action | final_block_reason | result_status | decision_quality_label | quality_bucket | improvement_signal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Flamengo vs Palmeiras | OVER_1_5 | EXECUTABLE | NONE | UNRESOLVED | ACTIONABLE_UNRESOLVED | NEEDS_MORE_DATA | IMPROVE_POST_RESULT_LABELING |
| Tokyo Verdy vs Yokohama F. Marinos | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | WIN | WAIT_MISSED_WIN | BAD_DECISION | REVIEW_NON_ACTIONABLE_BLOCK |
| Sporting Gijon vs Almeria | OVER_2_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Catanzaro vs Monza | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Remo vs Atletico Paranaense | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Sporting Gijon vs Almeria | OVER_2_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |
| Catanzaro vs Monza | OVER_1_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |
| Remo vs Atletico Paranaense | OVER_1_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |

## Block Quality Review
- NO_BET_MISSED_WIN count: 0
- NO_BET_CORRECT_AVOIDED_LOSS count: 0
- WAIT_MISSED_WIN count: 1
- WAIT_CORRECT_AVOIDED_LOSS count: 0
- EXPIRED_PRELOCK rows: 3
- PRELOCK_NOT_AVAILABLE rows: 0
- KICKOFF_ALREADY_PASSED rows: 3

## Market Quality Review
| market_primary | rows | wins | losses | no_bet_missed_win | no_bet_correct_avoided_loss | unresolved | recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | 6 | 1 | 0 | 0 | 0 | 5 | MONITOR |
| OVER_2_5 | 2 | 0 | 0 | 0 | 0 | 2 | WAIT_FOR_POST_RESULTS |

## System Recommendations
| priority | category | title | reason | apply_now |
| --- | --- | --- | --- | --- |
| P3 | sample | Do not recalibrate from quality sample yet | resolved_rows=1 is below minimum 30. | NO |
| P3 | post_results | Wait for POST results or improve labeling | unresolved_rows=7; resolved_rows=1. | NO |

## Guardrails
- automatic scoring changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
