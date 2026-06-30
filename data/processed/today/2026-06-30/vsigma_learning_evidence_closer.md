# vSIGMA Learning Evidence Closer - 2026-06-30

## Executive Evidence Summary
- generated_at: 2026-06-30T05:36:13+01:00
- executive_status: POST_RESULT_LABELING_REQUIRED
- close_items: 2
- severity_counts: P2=2
- issue_counts: MISSING_RESULT_FILE=1; PRELOCK_OPEN_ITEM=1
- auto_fix: NO
- production_change: NO

## Close Plan
- #1 | P2 | MISSING_RESULT_FILE | fixture=N/A | market=UNKNOWN | field=result_status | state=WAIT_POST_RESULT_LABELING | next=RUN_POST_RESULTS_PIPELINE | reason=No dated market result file exists yet.
- #2 | P2 | PRELOCK_OPEN_ITEM | fixture=1548054 | market=OVER_2_5 | field=lineup_activation_state | state=WAIT_PRELOCK | next=RUN_PRELOCK_IN_WINDOW | reason=BET row still needs prelock/lineup timing confirmation.

## Guardrails
- No ledger rows are changed by this report.
- No production behavior is changed.
- Safe closing requires POST first, then learning rebuild, then readiness review.