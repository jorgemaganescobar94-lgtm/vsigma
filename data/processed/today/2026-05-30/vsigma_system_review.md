# vSIGMA System Review - 2026-05-30

## Executive Status
- Cloud AUTO status: EXECUTABLE
- Candidates reviewed: 3
- Executable picks: 1
- Waiting picks: 2
- Blocked picks: 0
- Official action summary: MIXED
- Healthcheck status: WARNING
- Ledger rows total: 161
- Ledger rows for target date: 15
- Decision outcome ledger rows total: 49
- Decision outcome ledger actionable rows: 8
- Decision outcome ledger non-actionable rows: 41
- Decision outcome ledger no bet rows: 23
- Decision outcome ledger expired rows: 16
- Decision outcome ledger waiting rows: 18
- Decision outcome ledger blocked rows: 7
- Decision outcome ledger technical review rows: 0
- Current operational verdict: EXECUTION_AVAILABLE_UNDER_GOVERNANCE

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
| 1494185 | Allsvenskan | AIK Stockholm | Sirius | OVER_2_5 | EXECUTABLE | YES | NONE | NO |  | ODDS_MISSING;LINEUPS_MISSING | PRELOCK_CONFIRMED |  | PRELOCK_NO_CHANGE |  |
| 1492281 | Serie A | Bahia | Botafogo | OVER_2_5 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-30T20:00+01:00 |  | WAITING_FOR_WINDOW |  | OUTSIDE_90_MIN_PRELOCK_WINDOW |  |
| 1544371 | UEFA Champions League | Paris Saint Germain | Arsenal | OVER_1_5 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-30T16:00+01:00 |  | WAITING_FOR_WINDOW |  | OUTSIDE_90_MIN_PRELOCK_WINDOW |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 8; COVERAGE_PARTIAL: 2
- odds coverage: 10/10
- fixture stats coverage: 8/10
- injuries coverage: 6/10
- lineups coverage: 10/10
- predictions coverage: 10/10
- odds structure depth: target_fixtures: 12; OK: 12; RICH_COHERENT: 7; RICH_MIXED: 5; BROAD_GOALS: 7
- API gaps detected: fixture_stats, injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 125; OVER_2_5: 28; BTTS_YES: 3; UNDER_3_5: 3; AWAY_WIN: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 208; LOW_CONVERSION: 104; FAILURE_MODE_AVALANCHE_RISK: 2
- OVER_1_5: appearances=125; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=28; calibration_sample=2; status=needs more sample
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
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=0; waiting=2; auto_status=EXECUTABLE |
| P2 | api_data | Target API enrichment to candidate fixtures only | Coverage gaps are present, but broad calendar enrichment would add cost and repo churn. | Improves prelock evidence where it matters without expanding data volume unnecessarily. | Medium; API quotas and cache growth must be controlled. | Fetch lineups only for candidate picks in-window, injuries only for reliable leagues, and fixture statistics only for TOP candidates; keep cache bounds. | YES | data_gap_flags=ODDS_MISSING;LINEUPS_MISSING: 1; prelock_lineup_state=LINEUPS_NOT_AVAILABLE: 1; prelock_odds_state=ODDS_NOT_AVAILABLE: 1 |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=8; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-30T13:50:40+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
