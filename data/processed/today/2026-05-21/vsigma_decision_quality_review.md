# vSIGMA Decision Quality Review - 2026-05-21

## Executive Summary
- generated_at: 2026-05-21T18:39:09+01:00
- daily_classification: EXPIRED_PRELOCK
- no_bet_classification: NO_BET_VALID
- operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- predictive_failure: NO
- rows reviewed: 4
- actionable rows: 0
- non-actionable rows: 4
- resolved rows: 2
- unresolved rows: 2
- good decisions: 0
- bad decisions: 0
- neutral/unresolved: 4
- top improvement signal: REVIEW_AUTO_TIMING (3)
- current recommendation: Do not recalibrate; collect more labeled outcomes.
- operational note: The candidate expired before execution, so the operational issue is AUTO/PRELOCK timing. This is not a predictive failure and must not be counted in predictive hit-rate metrics.

## Daily Operational Classification
- classification: EXPIRED_PRELOCK
- no_bet_validity: NO_BET_VALID
- current_operational_verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA
- explanation: The candidate expired before execution, so the operational issue is AUTO/PRELOCK timing. This is not a predictive failure and must not be counted in predictive hit-rate metrics.

## Decision Quality Table
| fixture | market_primary | official_action | final_block_reason | result_status | decision_quality_label | quality_bucket | improvement_signal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Brondby vs FC Copenhagen | OVER_2_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Brondby vs FC Copenhagen | OVER_2_5 | NO_BET | KICKOFF_ALREADY_PASSED | UNRESOLVED | EXPIRED_PRELOCK_UNRESOLVED | NEEDS_MORE_DATA | REVIEW_AUTO_TIMING |
| Flamengo vs Estudiantes L.P. | OVER_1_5 | NO_BET | KICKOFF_ALREADY_PASSED | LOSS | EXPIRED_PRELOCK_RESULT_LOSS | NEUTRAL_OR_UNRESOLVED | REVIEW_AUTO_TIMING |
| Gremio vs Palestino | UNDER_3_5 | NO_BET | KICKOFF_ALREADY_PASSED | WIN | EXPIRED_PRELOCK_RESULT_WIN | NEUTRAL_OR_UNRESOLVED | REVIEW_AUTO_TIMING |

## Block Quality Review
- NO_BET_MISSED_WIN count: 0
- NO_BET_CORRECT_AVOIDED_LOSS count: 0
- WAIT_MISSED_WIN count: 0
- WAIT_CORRECT_AVOIDED_LOSS count: 0
- EXPIRED_PRELOCK rows: 3
- PRELOCK_NOT_AVAILABLE rows: 0
- KICKOFF_ALREADY_PASSED rows: 3

## Market Quality Review
| market_primary | rows | wins | losses | no_bet_missed_win | no_bet_correct_avoided_loss | unresolved | recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | 1 | 0 | 1 | 0 | 0 | 0 | MONITOR |
| OVER_2_5 | 2 | 0 | 0 | 0 | 0 | 2 | WAIT_FOR_POST_RESULTS |
| UNDER_3_5 | 1 | 1 | 0 | 0 | 0 | 0 | MONITOR |

## System Recommendations
| priority | category | title | reason | apply_now |
| --- | --- | --- | --- | --- |
| P3 | sample | Do not recalibrate from quality sample yet | resolved_rows=2 is below minimum 30. | NO |

## Guardrails
- automatic scoring changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
