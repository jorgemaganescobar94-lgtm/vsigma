# vSIGMA Cloud Decision Summary - 2026-05-21

## Status
- Auto status: WAITING_OR_BLOCKED
- PRE refreshed: YES
- Candidates reviewed: 3
- Executable picks: 0
- Waiting picks: 1
- Blocked picks: 2
- Data problem picks: 0
- Next automatic action: WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW
- OFFICIAL_ACTION_SUMMARY: MIXED

## Executable Picks
_No rows._

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 2026-05-21T17:30+01:00 | 1046.7 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-21T16:00+01:00 | WAITING_FOR_PRELOCK_WINDOW | OUTSIDE_90_MIN_PRELOCK_WINDOW | WAIT_UNTIL_2026-05-21T16:00+01:00 |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2026-05-21T01:30+01:00 | 86.7 | NO_BET | NO | ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE | NO |  | PRELOCK_BLOCKED | PRELOCK_NOT_AVAILABLE | WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 2026-05-21T01:00+01:00 | 56.7 | NO_BET | NO | ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE | NO |  | PRELOCK_BLOCKED | PRELOCK_NOT_AVAILABLE | WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW |

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
- PRE refresh reasons: candidate_output:CANDIDATE_V2 | WARNING: only stale rows found for 2026-05-20; candidate_output:CANDIDATE_V4 | WARNING: only stale rows found for 2026-05-20; candidate_output:CANDIDATE_V5 | WARNING: only stale rows found for 2026-05-20; candidate_output:CANDIDATE_V6 | WARNING: only stale rows found for 2026-05-20; candidate_output:CANDIDATE_V7_SHORTLIST | WARNING: only stale rows found for 2026-05-20; global candidate top includes rows outside target date: vsigma_today_candidate_v2_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v4_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v5_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v6_competition_top.csv; global official top includes rows outside target date; health summary reports ledger has no rows for target date; health summary reports only stale rows found; missing snapshot official top: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_competition_top.csv; official_baseline_output | WARNING: only stale rows found for 2026-05-20; text trigger: ledger has no rows for target date; text trigger: official_baseline_output | WARNING; text trigger: only stale rows found
- PRELOCK retained no rows: NO
- PRELOCK unavailable rows: 2
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_prelock_exclusion_audit.csv
- PRELOCK resolver source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_prelock_decision_resolver.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_cloud_decision_summary.csv
