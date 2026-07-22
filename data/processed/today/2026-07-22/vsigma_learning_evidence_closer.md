# vSIGMA Learning Evidence Closer - 2026-07-22

## Executive Evidence Summary
- generated_at: 2026-07-22T04:50:25+01:00
- executive_status: POST_RESULT_LABELING_REQUIRED
- close_items: 4
- severity_counts: P2=4
- issue_counts: PRELOCK_OPEN_ITEM=3; MISSING_RESULT_FILE=1
- auto_fix: NO
- production_change: NO

## Close Plan
- #1 | P2 | MISSING_RESULT_FILE | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_RESULTS_PIPELINE | reason=No dated market result file exists yet.
- #2 | P2 | PRELOCK_OPEN_ITEM | fixture=1494212 | market=AWAY_WIN | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #3 | P2 | PRELOCK_OPEN_ITEM | fixture=1494213 | market=BTTS_YES | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.
- #4 | P2 | PRELOCK_OPEN_ITEM | fixture=1507002 | market=HOME_WIN | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.

## Guardrails
- No ledger rows are changed by this report.
- No production behavior is changed.
- Safe closing requires POST first, then learning rebuild, then readiness review.