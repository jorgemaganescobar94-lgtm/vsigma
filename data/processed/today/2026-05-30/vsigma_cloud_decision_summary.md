# vSIGMA Cloud Decision Summary - 2026-05-30

## Status
- Auto status: EXECUTABLE
- PRE refreshed: NO
- Candidates reviewed: 3
- Executable picks: 1
- Waiting picks: 2
- Blocked picks: 0
- Data problem picks: 0
- Next automatic action: EXECUTE_GOVERNED_PICK
- OFFICIAL_ACTION_SUMMARY: MIXED

## Executable Picks
| fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | official_action | executable_now | prelock_decision | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | 0.830325 | EXECUTABLE | YES | PRELOCK_NO_CHANGE | EXECUTE_GOVERNED_PICK |

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | 2026-05-30T21:30+01:00 | 459.34 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-30T20:00+01:00 | WAITING_FOR_PRELOCK_WINDOW | OUTSIDE_90_MIN_PRELOCK_WINDOW | WAIT_UNTIL_2026-05-30T20:00+01:00 |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | 2026-05-30T17:00+01:00 | 189.34 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-30T16:00+01:00 | WAITING_FOR_PRELOCK_WINDOW | OUTSIDE_90_MIN_PRELOCK_WINDOW | WAIT_UNTIL_2026-05-30T16:00+01:00 |

## Technical Warnings
- healthcheck_status: WARNING
- pre_refresh_attempted: NO
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
- PRE refreshed by auto controller: NO
- PRE refresh reasons: none
- PRELOCK retained no rows: NO
- PRELOCK unavailable rows: 0
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_prelock_exclusion_audit.csv
- PRELOCK resolver source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_prelock_decision_resolver.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-30/vsigma_cloud_decision_summary.csv
