# vSIGMA Decision Quality Review - 2026-05-22

## Executive Summary
- generated_at: 2026-05-22T22:40:24+01:00
- daily_classification: EXECUTION_OK
- no_bet_classification: EXECUTION_ACTIONABLE_PRESENT
- operational_verdict: EXECUTION_AVAILABLE
- predictive_failure: UNKNOWN
- rows reviewed: 3
- actionable rows: 1
- non-actionable rows: 2
- resolved rows: 0
- unresolved rows: 3
- good decisions: 0
- bad decisions: 0
- neutral/unresolved: 3
- top improvement signal: REVIEW_AUTO_TIMING (2)
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
| Djurgardens IF vs IF Brommapojkarna | OVER_2_5 | EXECUTABLE | NONE | UNRESOLVED | ACTIONABLE_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Sudtirol vs Bari | OVER_1_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |
| Djurgardens IF vs IF Brommapojkarna | OVER_2_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |

## Block Quality Review
- NO_BET_MISSED_WIN count: 0
- NO_BET_CORRECT_AVOIDED_LOSS count: 0
- WAIT_MISSED_WIN count: 0
- WAIT_CORRECT_AVOIDED_LOSS count: 0
- EXPIRED_PRELOCK rows: 2
- PRELOCK_NOT_AVAILABLE rows: 0
- KICKOFF_ALREADY_PASSED rows: 2

## Market Quality Review
| market_primary | rows | wins | losses | no_bet_missed_win | no_bet_correct_avoided_loss | unresolved | recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | 1 | 0 | 0 | 0 | 0 | 1 | WAIT_FOR_POST_RESULTS |
| OVER_2_5 | 2 | 0 | 0 | 0 | 0 | 2 | WAIT_FOR_POST_RESULTS |

## System Recommendations
| priority | category | title | reason | apply_now |
| --- | --- | --- | --- | --- |
| P3 | sample | Do not recalibrate from quality sample yet | resolved_rows=0 is below minimum 30. | NO |
| P3 | post_results | Wait for POST results or improve labeling | unresolved_rows=3; resolved_rows=0. | NO |

## Guardrails
- automatic scoring changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
