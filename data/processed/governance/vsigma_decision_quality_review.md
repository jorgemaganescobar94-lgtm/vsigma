# vSIGMA Decision Quality Review - 2026-05-20

## Executive Summary
- generated_at: 2026-05-20T18:59:25+01:00
- daily_classification: EXECUTION_OK
- no_bet_classification: EXECUTION_ACTIONABLE_PRESENT
- operational_verdict: EXECUTION_AVAILABLE
- predictive_failure: UNKNOWN
- rows reviewed: 4
- actionable rows: 1
- non-actionable rows: 3
- resolved rows: 1
- unresolved rows: 3
- good decisions: 1
- bad decisions: 0
- neutral/unresolved: 3
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
| Santa Fe vs Platense | OVER_1_5 | EXECUTABLE | NONE | WIN | ACTIONABLE_WIN | GOOD_DECISION | MONITOR_DECISION_QUALITY |
| Gais vs Hammarby FF | OVER_2_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| SC Freiburg vs Aston Villa | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| SC Freiburg vs Aston Villa | OVER_1_5 | NO_BET | PRELOCK_GOVERNANCE_NOT_RETAINED | UNRESOLVED | NO_BET_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |

## Block Quality Review
- NO_BET_MISSED_WIN count: 0
- NO_BET_CORRECT_AVOIDED_LOSS count: 0
- WAIT_MISSED_WIN count: 0
- WAIT_CORRECT_AVOIDED_LOSS count: 0
- EXPIRED_PRELOCK rows: 0
- PRELOCK_NOT_AVAILABLE rows: 0
- KICKOFF_ALREADY_PASSED rows: 0

## Market Quality Review
| market_primary | rows | wins | losses | no_bet_missed_win | no_bet_correct_avoided_loss | unresolved | recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | 3 | 1 | 0 | 0 | 0 | 2 | MONITOR |
| OVER_2_5 | 1 | 0 | 0 | 0 | 0 | 1 | WAIT_FOR_POST_RESULTS |

## System Recommendations
| priority | category | title | reason | apply_now |
| --- | --- | --- | --- | --- |
| P3 | sample | Do not recalibrate from quality sample yet | resolved_rows=1 is below minimum 30. | NO |
| P3 | post_results | Wait for POST results or improve labeling | unresolved_rows=3; resolved_rows=1. | NO |

## Guardrails
- automatic scoring changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
