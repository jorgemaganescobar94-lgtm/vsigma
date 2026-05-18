# vSIGMA Cloud Decision Summary - 2026-05-18

## Status
- Auto status: TECHNICAL_WARNING
- PRE refreshed: YES
- Candidates reviewed: 2
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
| 1392197 | Segunda División | Leganes | Huesca | OVER_1_5 | 2026-05-18T19:30+01:00 | 1094.93 | TECHNICAL_WARNING | OUTSIDE_90_MIN_PRELOCK_WINDOW | REVIEW_AUTO_TECHNICAL_WARNINGS |
| 1494170 | Allsvenskan | Djurgardens IF | Sirius | OVER_2_5 | 2026-05-18T18:00+01:00 | 1004.93 | TECHNICAL_WARNING | OUTSIDE_90_MIN_PRELOCK_WINDOW | REVIEW_AUTO_TECHNICAL_WARNINGS |

## Technical Warnings
- healthcheck_status: BROKEN
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
- PRE refresh reasons: candidate_output:CANDIDATE_V2 | WARNING: only stale rows found for 2026-05-17; candidate_output:CANDIDATE_V4 | WARNING: only stale rows found for 2026-05-17; candidate_output:CANDIDATE_V5 | WARNING: only stale rows found for 2026-05-17; candidate_output:CANDIDATE_V6 | WARNING: only stale rows found for 2026-05-17; candidate_output:CANDIDATE_V7_SHORTLIST | WARNING: only stale rows found for 2026-05-17; global candidate top includes rows outside target date: vsigma_today_candidate_v2_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v4_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v5_competition_top.csv; global candidate top includes rows outside target date: vsigma_today_candidate_v6_competition_top.csv; global official top includes rows outside target date; health summary reports ledger has no rows for target date; health summary reports only stale rows found; missing snapshot official top: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_today_competition_top.csv; official_baseline_output | WARNING: only stale rows found for 2026-05-17; text trigger: ledger has no rows for target date; text trigger: official_baseline_output | WARNING; text trigger: only stale rows found
- PRELOCK retained no rows: YES
- PRELOCK unavailable rows: 0
- Candidate source used: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_today_competition_top.csv
- Global candidate fallback: /home/runner/work/vsigma/vsigma/data/processed/vsigma_today_competition_top.csv
- PRELOCK source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_today_prelock_competition_top.csv
- Audit source: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_prelock_exclusion_audit.csv
- PRELOCK report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_today_prelock_report.txt
- Summary CSV: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-18/vsigma_cloud_decision_summary.csv
