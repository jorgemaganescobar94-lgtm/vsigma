# vSIGMA System Review - 2026-05-22

## Executive Status
- Cloud AUTO status: EXECUTABLE
- Candidates reviewed: 2
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 2
- Official action summary: NO_BET
- Healthcheck status: WARNING
- Ledger rows total: 84
- Ledger rows for target date: 8
- Decision outcome ledger rows total: 17
- Decision outcome ledger actionable rows: 3
- Decision outcome ledger non-actionable rows: 14
- Decision outcome ledger no bet rows: 9
- Decision outcome ledger expired rows: 8
- Decision outcome ledger waiting rows: 5
- Decision outcome ledger blocked rows: 1
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA

## Decision Quality Review
- status: AVAILABLE
- rows reviewed: 3
- good decisions: 0
- bad decisions: 0
- unresolved: 3
- top improvement signal: REVIEW_AUTO_TIMING (2)
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1544652 | Serie B | Sudtirol | Bari | OVER_1_5 | NO_BET | NO | KICKOFF_ALREADY_PASSED | NO |  |  | EXPIRED |  | PRELOCK_NOT_AVAILABLE |  |
| 1494177 | Allsvenskan | Djurgardens IF | IF Brommapojkarna | OVER_2_5 | NO_BET | NO | KICKOFF_ALREADY_PASSED | NO |  |  | EXPIRED |  | PRELOCK_CONFIRMED |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 7; COVERAGE_PARTIAL: 1
- odds coverage: 8/8
- fixture stats coverage: 7/8
- injuries coverage: 5/8
- lineups coverage: 8/8
- predictions coverage: 8/8
- odds structure depth: target_fixtures: 5; OK: 5; RICH_COHERENT: 5; BROAD_GOALS: 3; MILD_GOALS: 2
- API gaps detected: fixture_stats, injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 75; OVER_2_5: 14; BTTS_YES: 3; AWAY_WIN: 2; UNDER_3_5: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 138; LOW_CONVERSION: 69
- OVER_1_5: appearances=75; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=14; calibration_sample=2; status=needs more sample
- sides / DNB / 1X / X2: appearances=2; calibration_sample=1; status=needs more sample
- mercados con buena senal: none yet by sample rule
- mercados que necesitan mas muestra: AWAY_WIN (1), OVER_1_5 (7), OVER_2_5 (2)

## Calibration Review
- closed picks available: 7
- enough_sample: NO
- recalibration_allowed: NO
- recommendation: Do not recalibrate; keep collecting closed picks.
- calibration report present: YES
- action applied: NO

## API Data Improvement Recommendations
- Fetch lineups only for candidate picks inside the relevant prelock window.
- Fetch injuries only for leagues with reliable coverage and candidate exposure.
- Fetch fixture statistics only for TOP candidates where the data can change execution review.
- Do not enrich the full calendar without a specific diagnostic or execution need.
- Keep API cache bounded and monitor repository size.

## System Improvement Queue
| priority | category | title | reason | expected_impact | risk | recommended_action | apply_now | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | execution | Improve prelock timing schedule | Decision outcome ledger includes expired or prelock unavailable decisions. | Reduces non-actionable PRELOCK outcomes caused by late or missing execution windows. | Low if limited to scheduling and reporting diagnostics. | Review AUTO/PRELOCK timing so resolver runs before kickoff and captures a useful in-window slot. | YES | prelock_not_available=0; expired=2 |
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=2; waiting=0; auto_status=EXECUTABLE |
| P2 | api_data | Target API enrichment to candidate fixtures only | Coverage gaps are present, but broad calendar enrichment would add cost and repo churn. | Improves prelock evidence where it matters without expanding data volume unnecessarily. | Medium; API quotas and cache growth must be controlled. | Fetch lineups only for candidate picks in-window, injuries only for reliable leagues, and fixture statistics only for TOP candidates; keep cache bounds. | YES | prelock_lineup_state=LINEUPS_NOT_AVAILABLE: 1; LINEUPS_CONFIRMED: 1; prelock_odds_state=ODDS_NOT_AVAILABLE: 2; prelock_availability_state=AVAILABILITY_NOT_AVAILABLE: 1; AVAILABILITY_CONFIRMED: 1 |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=7; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-22T22:40:24+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
