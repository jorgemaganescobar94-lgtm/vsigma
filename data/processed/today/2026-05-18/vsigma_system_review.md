# vSIGMA System Review - 2026-05-18

## Executive Status
- Cloud AUTO status: WAITING_OR_BLOCKED
- Candidates reviewed: 1
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 1
- Official action summary: NO_BET
- Healthcheck status: WARNING
- Ledger rows total: 57
- Ledger rows for target date: 12
- Decision outcome ledger rows total: 1
- Decision outcome ledger actionable rows: 0
- Decision outcome ledger non-actionable rows: 1
- Decision outcome ledger no bet rows: 1
- Decision outcome ledger expired rows: 1
- Decision outcome ledger waiting rows: 0
- Decision outcome ledger blocked rows: 0
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA

## Decision Quality Review
- status: AVAILABLE
- rows reviewed: 1
- good decisions: 0
- bad decisions: 0
- unresolved: 1
- top improvement signal: WAIT_FOR_POST_RESULTS (1)
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392197 | Segunda División | Leganes | Huesca | OVER_1_5 | NO_BET | NO | KICKOFF_ALREADY_PASSED | NO |  |  | EXPIRED |  | PRELOCK_NOT_AVAILABLE |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 4
- odds coverage: 4/4
- fixture stats coverage: 4/4
- injuries coverage: 3/4
- lineups coverage: 4/4
- predictions coverage: 4/4
- odds structure depth: target_fixtures: 3; OK: 3; RICH_MIXED: 2; RICH_COHERENT: 1; BROAD_GOALS: 1
- API gaps detected: injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 46; OVER_2_5: 8; UNDER_3_5: 1; HOME_WIN: 1
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 100; LOW_CONVERSION: 50
- OVER_1_5: appearances=46; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=8; calibration_sample=2; status=needs more sample
- sides / DNB / 1X / X2: appearances=1; calibration_sample=1; status=needs more sample
- mercados con buena senal: none yet by sample rule
- mercados que necesitan mas muestra: AWAY_WIN (1), OVER_1_5 (7), OVER_2_5 (2)

## Calibration Review
- closed picks available: 5
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
| P1 | execution | Improve prelock timing schedule | Decision outcome ledger includes expired or prelock unavailable decisions. | Reduces non-actionable PRELOCK outcomes caused by late or missing execution windows. | Low if limited to scheduling and reporting diagnostics. | Review AUTO/PRELOCK timing so resolver runs before kickoff and captures a useful in-window slot. | YES | prelock_not_available=0; expired=1 |
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=1; waiting=0; auto_status=WAITING_OR_BLOCKED |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=5; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-18T22:55:11+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
