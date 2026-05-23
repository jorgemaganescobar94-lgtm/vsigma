# vSIGMA System Review - 2026-05-23

## Executive Status
- Cloud AUTO status: WAITING_OR_BLOCKED
- Candidates reviewed: 2
- Executable picks: 0
- Waiting picks: 1
- Blocked picks: 1
- Official action summary: MIXED
- Healthcheck status: WARNING
- Ledger rows total: 97
- Ledger rows for target date: 13
- Decision outcome ledger rows total: 19
- Decision outcome ledger actionable rows: 3
- Decision outcome ledger non-actionable rows: 16
- Decision outcome ledger no bet rows: 10
- Decision outcome ledger expired rows: 8
- Decision outcome ledger waiting rows: 6
- Decision outcome ledger blocked rows: 2
- Decision outcome ledger technical review rows: 0
- Current operational verdict: NO_EXECUTION_BLOCKED_BY_PRELOCK_OR_DATA

## Decision Quality Review
- status: AVAILABLE
- rows reviewed: 2
- good decisions: 0
- bad decisions: 0
- unresolved: 2
- top improvement signal: WAIT_FOR_POST_RESULTS (2)
- recalibration_allowed_from_quality: NO

## Current Picks / Decisions
| fixture_id | league | home_team | away_team | market_primary | official_action | executable_now | final_block_reason | retry_allowed | next_retry_time | data_gap_flags | execution_family_status | decision_state | exclusion_reason | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1504822 | J1 League | Kashima | FC Tokyo | OVER_1_5 | NO_BET | NO | ODDS_NOT_AVAILABLE;LINEUPS_NOT_AVAILABLE;AVAILABILITY_NOT_AVAILABLE | NO |  | ODDS_MISSING;LINEUPS_MISSING;AVAILABILITY_MISSING | DATA_GAP_BLOCKED |  | PRELOCK_NOT_AVAILABLE |  |
| 1494182 | Allsvenskan | Kalmar FF | Degerfors IF | OVER_1_5 | WAIT | NO | OUTSIDE_PRELOCK_WINDOW | YES | 2026-05-23T13:00+01:00 |  | WAITING_FOR_WINDOW |  | OUTSIDE_90_MIN_PRELOCK_WINDOW |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 13; COVERAGE_PARTIAL: 2
- odds coverage: 15/15
- fixture stats coverage: 13/15
- injuries coverage: 9/15
- lineups coverage: 15/15
- predictions coverage: 15/15
- odds structure depth: target_fixtures: 28; OK: 28; RICH_COHERENT: 23; RICH_MIXED: 5; BROAD_GOALS: 12
- API gaps detected: fixture_stats, injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 88; OVER_2_5: 13; BTTS_YES: 3; AWAY_WIN: 2; UNDER_3_5: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 162; LOW_CONVERSION: 81
- OVER_1_5: appearances=88; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=13; calibration_sample=2; status=needs more sample
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
| P1 | execution | Keep actionable and non-actionable buckets separated | The current day has waiting or blocked decisions. | Keeps ledger/backtest interpretation aligned with execution reality. | Low; reporting-only validation. | Continue reporting all rows, actionable only, non-actionable, and graded bets separately. | YES | blocked=1; waiting=1; auto_status=WAITING_OR_BLOCKED |
| P1 | odds | Improve in-window odds refresh | Decision outcome ledger has NO_BET rows blocked by missing odds. | Improves executable pick retention when model selection is already available. | Medium; API quota and cache growth must remain bounded. | Refresh odds for candidate fixtures inside the PRELOCK window before resolving final action. | YES | no_bet_odds_not_available=1 |
| P2 | api_data | Fetch candidate lineups in-window | Decision outcome ledger has NO_BET rows blocked by missing lineups. | Improves PRELOCK evidence for candidate fixtures without broad calendar enrichment. | Medium; lineup availability varies by league and kickoff timing. | Target lineup fetches to candidate fixtures inside the PRELOCK window. | YES | no_bet_lineups_not_available=1 |
| P2 | api_data | Target API enrichment to candidate fixtures only | Coverage gaps are present, but broad calendar enrichment would add cost and repo churn. | Improves prelock evidence where it matters without expanding data volume unnecessarily. | Medium; API quotas and cache growth must be controlled. | Fetch lineups only for candidate picks in-window, injuries only for reliable leagues, and fixture statistics only for TOP candidates; keep cache bounds. | YES | data_gap_flags=ODDS_MISSING;LINEUPS_MISSING;AVAILABILITY_MISSING: 1; prelock_lineup_state=LINEUPS_NOT_AVAILABLE: 1; prelock_odds_state=ODDS_NOT_AVAILABLE: 1; prelock_availability_state=AVAILABILITY_NOT_AVAILABLE: 1 |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=7; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-23T08:50:08+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
