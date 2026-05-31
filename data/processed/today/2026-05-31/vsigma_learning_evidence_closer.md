# vSIGMA Learning Evidence Closer - 2026-05-31

## Executive Evidence Summary
- generated_at: 2026-05-31T11:00:43+01:00
- executive_status: POST_RESULT_LABELING_REQUIRED
- close_items: 15
- severity_counts: P2=9; P3=6
- issue_counts: PRELOCK_OPEN_ITEM=4; OPEN_RESULT_STATUS=3; NO_SIGNAL=2; UNKNOWN_FAMILY=2; UNKNOWN_RISK=2; MISSING_IDENTITY=1; MISSING_RESULT_FILE=1
- auto_fix: NO
- production_change: NO

## Close Plan
- #1 | P2 | MISSING_IDENTITY | fixture=N/A | market=UNKNOWN | field=fixture_id | state=NEEDS_SOURCE_IDENTITY | next=REBUILD_FROM_EXECUTION_AND_RESULT_SOURCES | reason=Learning row is missing fixture_id or market_primary.
- #2 | P2 | MISSING_RESULT_FILE | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_RESULTS_PIPELINE | reason=No dated market result file exists yet.
- #3 | P2 | OPEN_RESULT_STATUS | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #4 | P2 | OPEN_RESULT_STATUS | fixture=1392226 | market=OVER_1_5 | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #5 | P2 | OPEN_RESULT_STATUS | fixture=1492282 | market=OVER_1_5 | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_THEN_REBUILD_LEARNING | reason=Outcome cannot close until post-result labeling is available.
- #6 | P2 | PRELOCK_OPEN_ITEM | fixture=1392217 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #7 | P2 | PRELOCK_OPEN_ITEM | fixture=1392220 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #8 | P2 | PRELOCK_OPEN_ITEM | fixture=1492282 | market=OVER_1_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #9 | P2 | PRELOCK_OPEN_ITEM | fixture=1492289 | market=OVER_1_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #10 | P3 | NO_SIGNAL | fixture=N/A | market=UNKNOWN | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #11 | P3 | NO_SIGNAL | fixture=1392226 | market=OVER_1_5 | field=improvement_signal | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=improvement_signal is empty or unresolved.
- #12 | P3 | UNKNOWN_FAMILY | fixture=N/A | market=UNKNOWN | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #13 | P3 | UNKNOWN_FAMILY | fixture=1392226 | market=OVER_1_5 | field=learning_family | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=learning_family is empty or unresolved.
- #14 | P3 | UNKNOWN_RISK | fixture=N/A | market=UNKNOWN | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.
- #15 | P3 | UNKNOWN_RISK | fixture=1392226 | market=OVER_1_5 | field=accuracy_primary_risk | state=ENRICH_AFTER_POST | next=REBUILD_LEARNING_AFTER_POST | reason=accuracy_primary_risk is empty or unresolved.

## Guardrails
- No ledger rows are changed by this report.
- No production behavior is changed.
- Safe closing requires POST first, then learning rebuild, then readiness review.