# vSIGMA System Review - 2026-06-13

## Executive Status
- Cloud AUTO status: NO_BET
- Candidates reviewed: 0
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 0
- Official action summary: NO_BET
- Healthcheck status: WARNING
- Ledger rows total: 174
- Ledger rows for target date: 0
- Decision outcome ledger rows total: 71
- Decision outcome ledger actionable rows: 8
- Decision outcome ledger non-actionable rows: 63
- Decision outcome ledger no bet rows: 40
- Decision outcome ledger expired rows: 24
- Decision outcome ledger waiting rows: 23
- Decision outcome ledger blocked rows: 16
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_BET

## Decision Quality Review
- status: NOT_AVAILABLE
- good decisions: 0
- bad decisions: 0
- unresolved: 0
- top improvement signal: NONE
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | NO_BET | NO | NO_CANDIDATES | NO |  |  | NO_CANDIDATES |  |  |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_PARTIAL: 1; COVERAGE_RICH: 1
- odds coverage: 2/2
- fixture stats coverage: 1/2
- injuries coverage: 0/2
- lineups coverage: 2/2
- predictions coverage: 2/2
- odds structure depth: target_fixtures: 0
- API gaps detected: fixture_stats, injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 132; OVER_2_5: 26; BTTS_YES: 3; UNDER_3_5: 3; AWAY_WIN: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 208; LOW_CONVERSION: 104; FAILURE_MODE_AVALANCHE_RISK: 2
- OVER_1_5: appearances=132; calibration_sample=0; status=needs more sample
- OVER_2_5: appearances=26; calibration_sample=0; status=needs more sample
- sides / DNB / 1X / X2: appearances=2; calibration_sample=0; status=needs more sample
- mercados con buena senal: none yet by sample rule
- mercados que necesitan mas muestra: none detected

## Calibration Review
- closed picks available: 8
- enough_sample: NO
- recalibration_allowed: NO
- recommendation: Do not recalibrate; keep collecting closed picks.
- calibration report present: NO
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
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=8; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-06-13T14:01:22+01:00
- timezone: Atlantic/Canary
- missing optional inputs: vsigma_today_competition_top.csv, vsigma_probability_calibration_report.txt, vsigma_probability_calibration_table.csv
