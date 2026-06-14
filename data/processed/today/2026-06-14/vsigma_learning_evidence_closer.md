# vSIGMA Learning Evidence Closer - 2026-06-14

## Executive Evidence Summary
- generated_at: 2026-06-14T06:11:13+01:00
- executive_status: POST_RESULT_LABELING_REQUIRED
- close_items: 8
- severity_counts: P2=5; P3=3
- issue_counts: OPEN_RESULT_STATUS=2; MISSING_IDENTITY=1; MISSING_RESULT_FILE=1; PRELOCK_OPEN_ITEM=1; NO_SIGNAL=1; UNKNOWN_FAMILY=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Close Plan
- #1 | P2 | MISSING_IDENTITY | fixture=N/A | market=UNKNOWN | field=fixture_id | state=NEEDS_SOURCE_IDENTITY | next=REBUILD_FROM_EXECUTION_AND_RESULT_SOURCES | reason=Learning row is missing fixture_id or market_primary.
- #2 | P2 | MISSING_RESULT_FILE | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_RESULTS_PIPELINE | reason=No dated market result file exists yet.
- #3 | P2 | OPEN_RESULT_STATUS | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #4 | P2 | OPEN_RESULT_STATUS | fixture=1551271 | market=OVER_2_5 | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #5 | P2 | PRELOCK_OPEN_ITEM | fixture=1551271 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #6 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #7 | P3 | UNKNOWN_FAMILY | fixture=N/A | market=UNKNOWN | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #8 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.

## Guardrails
- No ledger rows are changed by this report.
- No production behavior is changed.
- Safe closing requires POST first, then learning rebuild, then readiness review.