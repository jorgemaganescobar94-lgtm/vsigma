# vSIGMA Cloud Decision Summary - 2026-06-09

## Status
- Auto status: WAITING_OR_BLOCKED
- PRE refreshed: YES
- Candidates reviewed: 1
- Executable picks: 0
- Waiting picks: 1
- Blocked picks: 0
- Data problem picks: 0
- Next automatic action: WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW
- OFFICIAL_ACTION_SUMMARY: WAIT

## Executable Picks
_No rows._

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1548054 | Segunda División | Almeria | Castellón | OVER_2_5 | 2026-06-09T20:00+01:00 | 494.12 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-06-09T19:00+01:00 | WAITING_FOR_PRELOCK_WINDOW | OUTSIDE_90_MIN_PRELOCK_WINDOW | WAIT_UNTIL_2026-06-09T19:00+01:00 |

## Technical Warnings
- healthcheck_status: WARNING
- pre_refresh_attempted: YES
- pre_refresh_failed: NO
- pre_refresh_skipped_reason: none
- pre_refresh_error: none
- prelock_failed: NO
- prelock_error: none
- audit_failed: NO
- audit_error: none

## Technical Notes
- Timezone: Atlantic/Canary
- Window minutes: 90
- PRE refreshed by auto controller: YES
- PRE refresh reasons: health summary reports ledger has no rows for target date; missing snapshot official top: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_today_competition_top.csv; text trigger: ledger has no rows for target date
- PRELOCK retained no rows: YES
- PRELOCK unavailable rows: 0
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_prelock_exclusion_audit.csv
- PRELOCK resolver source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_prelock_decision_resolver.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-06-09/vsigma_cloud_decision_summary.csv
