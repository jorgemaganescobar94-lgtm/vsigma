# vSIGMA Cloud Decision Summary - 2026-05-17

## Status
- Auto status: WAITING_FOR_PRELOCK_WINDOW
- PRE refreshed: NO
- Candidates reviewed: 2
- Executable picks: 0
- Waiting picks: 1
- Blocked picks: 0
- Data problem picks: 0
- Next automatic action: WAIT_FOR_NEXT_PRELOCK_WINDOW

## Executable Picks
_No rows._

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544950 | Serie B | Catanzaro | Palermo | OVER_1_5 | 2026-05-17T19:00+01:00 | -132.61 | POST_PENDING | KICKOFF_ALREADY_PASSED | WAIT_FOR_POST_RESULTS |
| 1492260 | Serie A | Atletico Paranaense | Flamengo | OVER_1_5 | 2026-05-17T23:30+01:00 | 137.39 | WAITING_FOR_PRELOCK_WINDOW | OUTSIDE_90_MIN_PRELOCK_WINDOW | WAIT_UNTIL_2026-05-17T22:00+01:00 |

## Technical Notes
- Timezone: Atlantic/Canary
- Window minutes: 90
- PRE refreshed by auto controller: NO
- PRE refresh reasons: none
- PRELOCK retained no rows: YES
- PRELOCK unavailable rows: 0
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/vsigma_prelock_exclusion_audit.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-17/vsigma_cloud_decision_summary.csv
