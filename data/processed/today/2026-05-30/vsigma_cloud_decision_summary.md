# vSIGMA Cloud Decision Summary - 2026-05-30

## Status
- Auto status: EXECUTABLE
- PRE refreshed: NO
- Candidates reviewed: 3
- Executable picks: 1
- Waiting picks: 0
- Blocked picks: 1
- Data problem picks: 0
- Next automatic action: EXECUTE_GOVERNED_PICK
- OFFICIAL_ACTION_SUMMARY: NO_BET

## Executable Picks
| fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | official_action | executable_now | prelock_decision | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | 0.830325 | NO_BET | NO | PRELOCK_NO_CHANGE | EXECUTE_GOVERNED_PICK |

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | 2026-05-30T21:30+01:00 | 11.89 | NO_BET | NO | PRELOCK_GOVERNANCE_NOT_RETAINED | NO |  | IN_WINDOW_BUT_BLOCKED | IN_WINDOW_BUT_NOT_RETAINED | CHECK_ODDS_LINEUPS_AVAILABILITY_OR_V7_GOVERNANCE |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | 2026-05-30T17:00+01:00 | -258.11 | NO_BET | NO | KICKOFF_ALREADY_PASSED | NO |  | POST_PENDING | KICKOFF_ALREADY_PASSED | WAIT_FOR_POST_RESULTS |

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
