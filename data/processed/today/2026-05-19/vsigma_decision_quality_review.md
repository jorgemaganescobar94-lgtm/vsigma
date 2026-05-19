# vSIGMA Decision Quality Review - 2026-05-19

## Executive Summary
- generated_at: 2026-05-19T11:50:03+01:00
- rows reviewed: 2
- actionable rows: 0
- non-actionable rows: 2
- resolved rows: 0
- unresolved rows: 2
- good decisions: 0
- bad decisions: 0
- neutral/unresolved: 2
- top improvement signal: WAIT_FOR_POST_RESULTS (2)
- current recommendation: Do not recalibrate; collect more labeled outcomes.

## Decision Quality Table
| fixture | market_primary | official_action | final_block_reason | result_status | decision_quality_label | quality_bucket | improvement_signal |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Monza vs Juve Stabia | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |
| Coquimbo Unido vs Deportes Tolima | OVER_1_5 | WAIT | OUTSIDE_PRELOCK_WINDOW | UNRESOLVED | WAIT_UNRESOLVED | NEEDS_MORE_DATA | WAIT_FOR_POST_RESULTS |

## Block Quality Review
- NO_BET_MISSED_WIN count: 0
- NO_BET_CORRECT_AVOIDED_LOSS count: 0
- WAIT_MISSED_WIN count: 0
- WAIT_CORRECT_AVOIDED_LOSS count: 0
- PRELOCK_NOT_AVAILABLE rows: 0
- KICKOFF_ALREADY_PASSED rows: 0

## Market Quality Review
| market_primary | rows | wins | losses | no_bet_missed_win | no_bet_correct_avoided_loss | unresolved | recommendation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | 2 | 0 | 0 | 0 | 0 | 2 | WAIT_FOR_POST_RESULTS |

## System Recommendations
| priority | category | title | reason | apply_now |
| --- | --- | --- | --- | --- |
| P3 | sample | Do not recalibrate from quality sample yet | resolved_rows=0 is below minimum 30. | NO |
| P3 | post_results | Wait for POST results or improve labeling | unresolved_rows=2; resolved_rows=0. | NO |

## Guardrails
- automatic scoring changes applied: NO
- threshold changes applied: NO
- calibration changes applied: NO
