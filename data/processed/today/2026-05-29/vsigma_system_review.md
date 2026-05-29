# vSIGMA System Review - 2026-05-29

## Executive Status
- Cloud AUTO status: EXECUTABLE
- Candidates reviewed: 1
- Executable picks: 1
- Waiting picks: 0
- Blocked picks: 0
- Official action summary: EXECUTABLE
- Healthcheck status: WARNING
- Ledger rows total: 158
- Ledger rows for target date: 19
- Decision outcome ledger rows total: 45
- Decision outcome ledger actionable rows: 7
- Decision outcome ledger non-actionable rows: 38
- Decision outcome ledger no bet rows: 22
- Decision outcome ledger expired rows: 15
- Decision outcome ledger waiting rows: 16
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
| 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | EXECUTABLE | YES | NONE | NO |  | ODDS_MISSING;LINEUPS_MISSING | PRELOCK_CONFIRMED |  | PRELOCK_NO_CHANGE |  |

## Data Coverage Review
- coverage rich / partial / weak: COVERAGE_RICH: 1; COVERAGE_PARTIAL: 1
- odds coverage: 2/2
- fixture stats coverage: 1/2
- injuries coverage: 1/2
- lineups coverage: 2/2
- predictions coverage: 2/2
- odds structure depth: target_fixtures: 1; OK: 1; RICH_MIXED: 1; LOW_GOALS: 1; PREFER_MILDER_TOTAL: 1
- API gaps detected: fixture_stats, injuries

## Model / Market Review
- markets appearing in current/historical inputs: OVER_1_5: 131; OVER_2_5: 18; BTTS_YES: 3; UNDER_3_5: 3; AWAY_WIN: 2
- failure modes principales: FAILURE_MODE_LOW_CONVERSION: 204; LOW_CONVERSION: 102; FAILURE_MODE_AVALANCHE_RISK: 2
- OVER_1_5: appearances=131; calibration_sample=7; status=needs more sample
- OVER_2_5: appearances=18; calibration_sample=2; status=needs more sample
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
| P1 | odds | Improve in-window odds refresh | Decision outcome ledger has NO_BET rows blocked by missing odds. | Improves executable pick retention when model selection is already available. | Medium; API quota and cache growth must remain bounded. | Refresh odds for candidate fixtures inside the PRELOCK window before resolving final action. | YES | no_bet_odds_not_available=2 |
| P2 | api_data | Fetch candidate lineups in-window | Decision outcome ledger has NO_BET rows blocked by missing lineups. | Improves PRELOCK evidence for candidate fixtures without broad calendar enrichment. | Medium; lineup availability varies by league and kickoff timing. | Target lineup fetches to candidate fixtures inside the PRELOCK window. | YES | no_bet_lineups_not_available=2 |
| P2 | api_data | Target API enrichment to candidate fixtures only | Coverage gaps are present, but broad calendar enrichment would add cost and repo churn. | Improves prelock evidence where it matters without expanding data volume unnecessarily. | Medium; API quotas and cache growth must be controlled. | Fetch lineups only for candidate picks in-window, injuries only for reliable leagues, and fixture statistics only for TOP candidates; keep cache bounds. | YES | data_gap_flags=ODDS_MISSING;LINEUPS_MISSING: 1; prelock_lineup_state=LINEUPS_NOT_AVAILABLE: 1; prelock_odds_state=ODDS_NOT_AVAILABLE: 1 |
| P3 | decision_quality | Collect more closed decision quality outcomes | Decision Quality Review has fewer than 30 resolved rows. | Avoids premature recalibration or execution-rule changes from a thin sample. | Low; reporting only. | Keep building the quality review after POST labels are available. | NO | resolved_quality_rows=0 |
| P3 | model_calibration | Defer recalibration until minimum closed-pick sample | Fewer than 30 closed picks are available. | Avoids fitting thresholds or probability adjustments to noise. | Low; no predictive change is applied. | Keep calibration reporting active and wait for at least 30 closed picks before suggestions. | NO | closed_picks=7; enough_sample=NO; recalibration_allowed=NO |

## Input Inventory
- generated_at: 2026-05-29T19:23:13+01:00
- timezone: Atlantic/Canary
- missing optional inputs: none
