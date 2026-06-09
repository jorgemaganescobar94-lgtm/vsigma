# vSIGMA System Review - 2026-06-10

## Executive Status
- Cloud AUTO status: WAITING_OR_BLOCKED
- Candidates reviewed: 1
- Executable picks: 0
- Waiting picks: 1
- Blocked picks: 0
- Official action summary: WAIT
- Healthcheck status: WARNING
- Ledger rows total: 182
- Ledger rows for target date: 7
- Decision outcome ledger rows total: 67
- Decision outcome ledger actionable rows: 8
- Decision outcome ledger non-actionable rows: 59
- Decision outcome ledger no bet rows: 36
- Decision outcome ledger expired rows: 23
- Decision outcome ledger waiting rows: 23
- Decision outcome ledger blocked rows: 13
- Decision outcome ledger technical review rows: 0
- Current operational verdict: WAIT_FOR_NEXT_PRELOCK_SLOT

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
| 1548055 | Segunda División | Malaga | Las Palmas | OVER_1_5 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-06-10T19:00+01:00 |  | WAITING_FOR_WINDOW |  | OUTSIDE_90_MIN_PRELOCK_WINDOW |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 2
- odds coverage: 2/2
- fixture stats coverage: 2/2
- injuries coverage: 2/2
- lineups coverage: 2/2
- predictions coverage: 2/2
- odds structure depth: target_fixtures: 1; OK: 1; RICH_MIXED: 1; MILD_GOALS: 1; PREFER_MILDER_TOTAL: 1
- API gaps detected: none detected in available coverage inputs

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 135; OVER_2_5: 30; BTTS_YES: 3; UNDER_3_5: 3; AWAY_WIN: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 228; LOW_CONVERSION: 114; FAILURE_MODE_AVALANCHE_RISK: 2
- OVER_1_5: appearances=135; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=30; calibration_sample=2; status=needs more sample
- sides / DNB / 1X / X2: appearances=2; calibration_sample=1; status=needs more sample
- mercados con buena senal: none yet by sample rule
- mercados que necesitan mas muestra: AWAY_WIN (1), OVER_1_5 (7), OVER_2_5 (2)

## Calibration Review
- closed picks available: 8
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
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=0; waiting=1; auto_status=WAITING_OR_BLOCKED |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=8; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-06-10T00:54:41+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
