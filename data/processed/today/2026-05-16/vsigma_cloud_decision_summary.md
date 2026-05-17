# vSIGMA Cloud Decision Summary - 2026-05-16

## Status
- Auto status: TECHNICAL_WARNING
- PRE refreshed: NO
- Candidates reviewed: 3
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 0
- Data problem picks: 0
- Next automatic action: REVIEW_AUTO_TECHNICAL_WARNINGS

## Executable Picks
_No rows._

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1388609 | Bundesliga | SC Freiburg | RB Leipzig | OVER_2_5 | 2026-05-16T14:30+01:00 | -1854.83 | TECHNICAL_WARNING | KICKOFF_ALREADY_PASSED | REVIEW_AUTO_TECHNICAL_WARNINGS |
| 1392194 | Segunda División | Granada CF | Burgos | OVER_1_5 | 2026-05-16T17:30+01:00 | -1674.83 | TECHNICAL_WARNING | KICKOFF_ALREADY_PASSED | REVIEW_AUTO_TECHNICAL_WARNINGS |
| 1544949 | Serie B | Juve Stabia | Monza | OVER_1_5 | 2026-05-16T19:00+01:00 | -1584.83 | TECHNICAL_WARNING | KICKOFF_ALREADY_PASSED | REVIEW_AUTO_TECHNICAL_WARNINGS |

## Technical Warnings
- healthcheck_status: BROKEN
- pre_refresh_attempted: NO
- pre_refresh_failed: NO
- pre_refresh_skipped_reason: PAST_TARGET_DATE
- pre_refresh_error: none
- prelock_failed: NO
- prelock_error: none
- audit_failed: NO
- audit_error: none

## Technical Notes
- Timezone: Atlantic/Canary
- Window minutes: 90
- PRE refreshed by auto controller: NO
- PRE refresh reasons: global candidate top includes rows outside target date: vsigma_today_candidate_v2_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v4_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v5_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v6_competition_top.csv; global official top includes rows outside target date
- PRELOCK retained no rows: YES
- PRELOCK unavailable rows: 0
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/vsigma_prelock_exclusion_audit.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-16/vsigma_cloud_decision_summary.csv
