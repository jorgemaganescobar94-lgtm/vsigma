# vSIGMA Learning Evidence Closer - 2026-05-22

## Executive Evidence Summary
- generated_at: 2026-05-22T15:42:04+01:00
- executive_status: POST_RESULT_LABELING_REQUIRED
- close_items: 18
- severity_counts: P3=10; P2=8
- issue_counts: OPEN_RESULT_STATUS=3; PRELOCK_OPEN_ITEM=3; NO_SIGNAL=3; UNKNOWN_FAMILY=3; UNKNOWN_RISK=3; MISSING_IDENTITY=1; MISSING_RESULT_FILE=1; DUPLICATE_LEARNING_ROW=1
- auto_fix: NO
- production_change: NO

## Close Plan
- #1 | P2 | MISSING_IDENTITY | fixture=N/A | market=UNKNOWN | field=fixture_id | state=NEEDS_SOURCE_IDENTITY | next=REBUILD_FROM_EXECUTION_AND_RESULT_SOURCES | reason=Learning row is missing fixture_id or market_primary.
- #2 | P2 | MISSING_RESULT_FILE | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_RESULTS_PIPELINE | reason=No dated market result file exists yet.
- #3 | P2 | OPEN_RESULT_STATUS | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #4 | P2 | OPEN_RESULT_STATUS | fixture=1494177 | market=OVER_2_5 | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #5 | P2 | OPEN_RESULT_STATUS | fixture=1544652 | market=OVER_1_5 | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #6 | P2 | PRELOCK_OPEN_ITEM | fixture=1494177 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #7 | P2 | PRELOCK_OPEN_ITEM | fixture=1544652 | market=OVER_1_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #8 | P2 | PRELOCK_OPEN_ITEM | fixture=1545405 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #9 | P3 | DUPLICATE_LEARNING_ROW | fixture=1544652 | market=OVER_1_5 | field=sample_key | state=DEDUP_REVIEW | next=DEDUPLICATE_REBUILT_LEDGER | reason=Multiple learning rows share fixture, market and result status.
- #10 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #11 | P3 | NO_SIGNAL | fixture=1494177 | market=OVER_2_5 | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #12 | P3 | NO_SIGNAL | fixture=1544652 | market=OVER_1_5 | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #13 | P3 | UNKNOWN_FAMILY | fixture=N/A | market=UNKNOWN | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #14 | P3 | UNKNOWN_FAMILY | fixture=1494177 | market=OVER_2_5 | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #15 | P3 | UNKNOWN_FAMILY | fixture=1544652 | market=OVER_1_5 | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #16 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.
- #17 | P3 | UNKNOWN_RISK | fixture=1494177 | market=OVER_2_5 | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.
- #18 | P3 | UNKNOWN_RISK | fixture=1544652 | market=OVER_1_5 | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.

## Guardrails
- No ledger rows are changed by this report.
- No production behavior is changed.
- Safe closing requires POST first, then learning rebuild, then readiness review.