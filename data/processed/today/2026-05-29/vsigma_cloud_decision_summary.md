# vSIGMA Cloud Decision Summary - 2026-05-29

## Status
- Auto status: WAITING_OR_BLOCKED
- PRE refreshed: YES
- Candidates reviewed: 2
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 2
- Data problem picks: 0
- Next automatic action: WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW
- OFFICIAL_ACTION_SUMMARY: NO_BET

## Executable Picks
_No rows._

## Waiting / Blocked Picks
| fixture_id | league | home_team | away_team | market_primary | fixture_datetime | minutes_to_kickoff | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | 2026-05-29T01:30+01:00 | 84.02 | NO_BET | NO | ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE | NO |  | PRELOCK_BLOCKED | PRELOCK_NOT_AVAILABLE | WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW |
| 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | 2026-05-29T01:30+01:00 | 84.02 | NO_BET | NO | ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE | NO |  | PRELOCK_BLOCKED | PRELOCK_NOT_AVAILABLE | WAIT_FOR_NEXT_AUTO_PRELOCK_OR_NO_BET_REVIEW |

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
- PRE refresh reasons: health summary reports ledger has no rows for target date; missing snapshot official top: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_today_competition_top.csv; text trigger: ledger has no rows for target date
- PRELOCK retained no rows: NO
- PRELOCK unavailable rows: 2
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_prelock_exclusion_audit.csv
- PRELOCK resolver source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_prelock_decision_resolver.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-29/vsigma_cloud_decision_summary.csv
