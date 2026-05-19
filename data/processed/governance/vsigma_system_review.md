# vSIGMA System Review - 2026-05-19

## Executive Status
- Cloud AUTO status: WAITING_OR_BLOCKED
- Candidates reviewed: 1
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 1
- Official action summary: NO_BET
- Healthcheck status: WARNING
- Ledger rows total: 70
- Ledger rows for target date: 13
- Decision outcome ledger rows total: 4
- Decision outcome ledger actionable rows: 0
- Decision outcome ledger non-actionable rows: 4
- Decision outcome ledger no bet rows: 2
- Decision outcome ledger expired rows: 1
- Decision outcome ledger waiting rows: 2
- Decision outcome ledger blocked rows: 1
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA

## Decision Quality Review
- status: AVAILABLE
- rows reviewed: 3
- good decisions: 0
- bad decisions: 0
- unresolved: 3
- top improvement signal: WAIT_FOR_POST_RESULTS (3)
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535300 | CONMEBOL Libertadores | Coquimbo Unido | Deportes Tolima | OVER_1_5 | NO_BET | NO | PRELOCK_GOVERNANCE_NOT_RETAINED | YES | 2026-05-19T22:00+01:00 |  | PRELOCK_NOT_RETAINED |  | IN_WINDOW_BUT_NOT_RETAINED |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 5
- odds coverage: 4/5
- fixture stats coverage: 5/5
- injuries coverage: 3/5
- lineups coverage: 5/5
- predictions coverage: 5/5
- odds structure depth: target_fixtures: 11; OK: 11; RICH_MIXED: 6; RICH_COHERENT: 4; RICH_NOISY: 1
- API gaps detected: injuries, odds

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 63; OVER_2_5: 10; AWAY_WIN: 1; BTTS_YES: 1; UNDER_3_5: 1
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 124; LOW_CONVERSION: 62
- OVER_1_5: appearances=63; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=10; calibration_sample=2; status=needs more sample
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
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=1; waiting=0; auto_status=WAITING_OR_BLOCKED |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=5; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-19T21:32:00+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
