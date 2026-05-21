# vSIGMA System Review - 2026-05-21

## Executive Status
- Cloud AUTO status: NO_BET
- Candidates reviewed: 0
- Executable picks: 0
- Waiting picks: 0
- Blocked picks: 0
- Official action summary: NO_BET
- Healthcheck status: WARNING
- Ledger rows total: 94
- Ledger rows for target date: 23
- Decision outcome ledger rows total: 14
- Decision outcome ledger actionable rows: 2
- Decision outcome ledger non-actionable rows: 12
- Decision outcome ledger no bet rows: 7
- Decision outcome ledger expired rows: 6
- Decision outcome ledger waiting rows: 5
- Decision outcome ledger blocked rows: 1
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_BET

## Decision Quality Review
- status: AVAILABLE
- rows reviewed: 4
- good decisions: 0
- bad decisions: 0
- unresolved: 2
- top improvement signal: REVIEW_AUTO_TIMING (3)
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | NO_BET | NO | NO_CANDIDATES | NO |  |  | NO_CANDIDATES |  |  |  |

## Data Coverage Review
- coverage rich / partial / weak: none
- odds coverage: UNKNOWN
- fixture stats coverage: UNKNOWN
- injuries coverage: UNKNOWN
- lineups coverage: UNKNOWN
- predictions coverage: UNKNOWN
- odds structure depth: target_fixtures: 0
- API gaps detected: none detected in available coverage inputs

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 70; OVER_2_5: 16; UNDER_3_5: 8; BTTS_YES: 3; AWAY_WIN: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 144; LOW_CONVERSION: 72; FAILURE_MODE_AVALANCHE_RISK: 12
- OVER_1_5: appearances=70; calibration_sample=0; status=needs more sample
- OVER_2_5: appearances=16; calibration_sample=0; status=needs more sample
- sides / DNB / 1X / X2: appearances=2; calibration_sample=0; status=needs more sample
- mercados con buena senal: none yet by sample rule
- mercados que necesitan mas muestra: none detected

## Calibration Review
- closed picks available: 7
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
| P1 | execution | Improve prelock timing schedule | Decision outcome ledger includes expired or prelock unavailable decisions. | Reduces non-actionable PRELOCK outcomes caused by late or missing execution windows. | Low if limited to scheduling and reporting diagnostics. | Review AUTO/PRELOCK timing so resolver runs before kickoff and captures a useful in-window slot. | YES | prelock_not_available=0; expired=3 |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=2 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=7; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-21T23:51:46+01:00
- timezone: Atlantic/Canary
- missing optional inputs: vsigma_probability_calibration_report.txt, vsigma_probability_calibration_table.csv
