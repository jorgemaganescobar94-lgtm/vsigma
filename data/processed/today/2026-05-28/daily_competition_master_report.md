# vSIGMA Daily Competition Master Report - 2026-05-28

## Daily Status
NO_BET

## Official Baseline Top Picks

Official baseline: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


## Candidate v2 Top Picks

Candidate v2: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


## Candidate v4/v5/v6 Top Picks
### Candidate v4

Candidate v4: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


### Candidate v5

Candidate v5: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


### Candidate v6

Candidate v6: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


### Candidate v7

Candidate v7: NO_BET. Empty output is valid when no pick clears the frozen competition filters.


## Match Script Forecasts
_No rows._

## Baseline vs Candidate Comparison
### Candidate v2
_No rows._

### Candidate v4
_No rows._

### Candidate v5
_No rows._

### Candidate v6
_No rows._

### Candidate v7
_No rows._

## Price Discipline / CLV / Drift Execution Guard
_No rows._

## Pre-Lock Execution Status
- Pre-lock data fresh: NO_CURRENT_PRELOCK_ROWS
- Stale pre-lock excluded: NO
- Execution allowed by v7: 0

### Official Baseline Picks
_No rows._

### Candidate v7 Pre-Lock Status
_No rows._

### Active Pre-Lock Decisions
_No rows._

### Stale Pre-Lock Warning
_No stale pre-lock rows excluded._

## Odds Snapshot / CLV Calibration
### CLV Summary
| fixture_id | home_team | away_team | market_primary | experiment_id | pre_price | prelock_price | close_proxy_price | clv_delta | clv_direction | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535220 | RB Bragantino | Carabobo FC | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 2.38 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535228 | River Plate | Blooming | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 2.5 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535315 | Bolívar | Independ. Rivadavia | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.85 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535315 | Bolívar | Independ. Rivadavia | OVER_2_5 | OFFICIAL_BASELINE | 1.85 |  | 1.85 | 0.0 | CLV_FLAT |  |  |
| 1535327 | Palmeiras | Junior | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 2.3 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535327 | Palmeiras | Junior | BTTS_YES | OFFICIAL_BASELINE | 2.3 |  | 2.3 | 0.0 | CLV_FLAT | WIN | 1.3 |
| 1535328 | Penarol | Santa Fe | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.44 |  |  |  | CLV_UNAVAILABLE |  |  |

### Candidate v7 Calibration Advice
_No rows._

## Post-Results Summary
| mode | pick_count | wins | losses | profit_units | roi_percent | pending_rows | candidate_version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_EXECUTION_SHORTLIST | 1.0 | 1.0 | 0.0 | 1.3 | 130.0 | 0.0 | OFFICIAL_RESULTS |
| SHADOW_CANDIDATE_V2 | 2.0 | 0.0 | 0.0 | 0.0 |  | 0.0 | CANDIDATE_V2_RESULTS |
| SHADOW_CANDIDATE_V4_O25_LOW_CONVERSION_FIREWALL | 2.0 | 0.0 | 0.0 | 0.0 |  | 0.0 | CANDIDATE_V4_RESULTS |
| SHADOW_CANDIDATE_V5_PLAYER_IMPACT | 2.0 | 0.0 | 0.0 | 0.0 |  | 0.0 | CANDIDATE_V5_RESULTS |
| SHADOW_CANDIDATE_V6_API_PREDICTIONS_BENCHMARK | 2.0 | 0.0 | 0.0 | 0.0 |  | 0.0 | CANDIDATE_V6_RESULTS |
| SHADOW_CANDIDATE_V7_PRICE_DISCIPLINE_CLV_DRIFT_GUARD | 0.0 | 0.0 | 0.0 | 0.0 |  | 0.0 | CANDIDATE_V7_RESULTS |

## Pre-Lock Status
_No rows._

## Drift Monitor Status
| pattern | settled_rows | wins | losses | profit_units | drift_status |
| --- | --- | --- | --- | --- | --- |
| OVER_2_5 + FAILURE_MODE_LOW_CONVERSION | 6 | 6 | 0 | 4.26 | NO_DRIFT |
| OVER_1_5 + FAILURE_MODE_LOW_CONVERSION | 26 | 16 | 10 | -3.39 | WATCH_PATTERN |
| BTTS_YES + FAILURE_MODE_BTTS_BREAK | 0 | 0 | 0 | 0.0 | SAMPLE_TOO_SMALL |
| HOME/AWAY_WIN + FAILURE_MODE_DRAW_LIVE | 5 | 5 | 0 | 5.0 | NO_DRIFT |
| candidate v2 vs baseline daily winner | 8 | 6 | 2 | 1.67 | NO_DRIFT |
| candidate v4 firewall performance | 6 | 4 | 2 | 0.25 | NO_DRIFT |
| candidate v5 player-impact adjusted subset | 8 | 6 | 2 | 1.67 | NO_DRIFT |
| candidate v6 API-prediction aligned subset | 1 | 1 | 0 | 1.0 | SAMPLE_TOO_SMALL |
| candidate v6 API-prediction disagreement subset | 0 | 0 | 0 | 0.0 | SAMPLE_TOO_SMALL |

## Baseline vs Candidate Trend
| mode | rows | settled_rows | wins | losses | profit_units | roi_percent | max_drawdown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE_OFFICIAL | 9 | 9 | 7 | 2 | 2.03 | 22.555556 | -1.67 |
| SHADOW_CANDIDATE_V2 | 8 | 8 | 6 | 2 | 1.67 | 20.875 | -2.0 |
| SHADOW_CANDIDATE_V4_O25_LOW_CONVERSION_FIREWALL | 6 | 6 | 4 | 2 | 0.25 | 4.166667 | -1.0 |
| SHADOW_CANDIDATE_V5_PLAYER_IMPACT | 8 | 8 | 6 | 2 | 1.67 | 20.875 | -2.0 |
| SHADOW_CANDIDATE_V6_API_PREDICTIONS_BENCHMARK | 6 | 6 | 4 | 2 | 0.25 | 4.166667 | -1.0 |

## Immutable Ledger / Experiment Registry
- Ledger update status: AVAILABLE
- Official picks registered: 0
- Shadow picks registered: 8
- No-bet records: 1
- Ledger report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_ledger_daily_report.md

## Daily Controller Status
- Next recommended action: NO_BET_DAY
- Pre-lock due time: NOT_AVAILABLE
- Status path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/daily_controller_status.md

## Daily Supervisor
- Supervisor latest status: SUPERVISOR_STATUS_NOT_AVAILABLE
- Last run mode/time: NOT_AVAILABLE / NOT_AVAILABLE
- Next recommended action: NO_BET_DAY
- Scheduled automation status: REGISTRATION_SCRIPT_AVAILABLE_STATUS_NOT_QUERIED
- Logs path: C:\vsigma\automation_logs\supervisor
- Report path: NOT_AVAILABLE

## Healthcheck
- Global health status: WARNING
- Critical warnings: freshness_report: WARNING - validation report contains warning rows
- Recovery command: `.\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-29`
- Report path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_healthcheck_report.md

### Current Experiment Daily Summary
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_decision | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535218.0 | America de Cali | Macara | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V4_O25_FIREWALL | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V4_O25_FIREWALL | 1535218.0 | America de Cali | Macara | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V5_PLAYER_IMPACT | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V5_PLAYER_IMPACT | 1535218.0 | America de Cali | Macara | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V6_API_PREDICTIONS | 1535314.0 | Boca Juniors | U. Catolica | OVER_1_5 |  | UNMATCHED |  | PENDING |
| CANDIDATE_V6_API_PREDICTIONS | 1535218.0 | America de Cali | Macara | OVER_1_5 |  | UNMATCHED |  | PENDING |

### Experiment Performance Summary
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 19 | 7 | 4 | 3 | -1.18 | -16.857143 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 25 | 6 | 3 | 3 | -1.7 | -28.333333 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 24 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 25 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 23 | 5 | 3 | 2 | -0.7 | -14.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 13 | 1 | 0 | 1 | -1.0 | -100.0 | PRICE_DISCIPLINE_UNTESTED |

## Promotion & Threshold Governance
- Official baseline status: KEEP_OFFICIAL_BASELINE
- Governance dashboard: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_governance_dashboard.md

### Candidate Promotion Recommendations
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 7 | -16.857143 | 0.311373 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 6 | -28.333333 | 0.347087 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 6 | -7.5 | 0.24192 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 6 | -7.5 | 0.245579 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 5 | -14.0 | 0.286085 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | -100.0 | 0.652097 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

### Threshold Recommendations
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 6 | -7.5 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 6 | -7.5 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 5 | -14.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 5 | -14.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 5 | -14.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 2 | -24.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | -100.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | -100.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V4_O25_FIREWALL | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | OFFICIAL_BASELINE | 0 |  |  | SAMPLE_TOO_SMALL |

- CLV data sufficiency: INSUFFICIENT_CLV_DATA
- Drift alerts: 0

## Failure Mode Summary
_No rows._

## Freshness Validation
| file_name | candidate_version | status | detail | rows |
| --- | --- | --- | --- | --- |
| vsigma_today_competition_shortlist.csv | OFFICIAL_BASELINE | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_competition_top.csv | OFFICIAL_BASELINE | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v2_competition_shortlist.csv | CANDIDATE_V2 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v2_competition_top.csv | CANDIDATE_V2 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v4_competition_shortlist.csv | CANDIDATE_V4 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v4_competition_top.csv | CANDIDATE_V4 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v5_competition_shortlist.csv | CANDIDATE_V5 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v5_competition_top.csv | CANDIDATE_V5 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v6_competition_shortlist.csv | CANDIDATE_V6 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v6_competition_top.csv | CANDIDATE_V6 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v7_competition_shortlist.csv | CANDIDATE_V7 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v7_competition_top.csv | CANDIDATE_V7 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_baseline_vs_candidate_v2.csv | COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_match_script_forecasts.csv | FORECAST | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v2_match_script_forecasts.csv | FORECAST_CANDIDATE_V2 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_candidate_v4_match_script_forecasts.csv | FORECAST_CANDIDATE_V4 | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_prelock_competition_top.csv | OFFICIAL_BASELINE_PRELOCK | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_today_prelock_comparison.csv | PRELOCK_COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-29'] does not match 2026-05-28 | 2 |
| vsigma_execution_shortlist_results_ledger.csv | OFFICIAL_RESULTS | PASS | output is fresh for requested target date | 1 |
| vsigma_execution_shortlist_results_summary.csv | OFFICIAL_RESULTS | PASS | output is fresh for requested target date | 96 |
| vsigma_today_candidate_v2_results_ledger.csv | CANDIDATE_V2_RESULTS | WARNING_STALE_GLOBAL_FILE | metadata source_file_date_check reports DATE_MISMATCH | 2 |
| vsigma_today_candidate_v2_results_summary.csv | CANDIDATE_V2_RESULTS | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v4_results_ledger.csv | CANDIDATE_V4_RESULTS | WARNING_STALE_GLOBAL_FILE | metadata source_file_date_check reports DATE_MISMATCH | 2 |
| vsigma_today_candidate_v4_results_summary.csv | CANDIDATE_V4_RESULTS | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v5_results_ledger.csv | CANDIDATE_V5_RESULTS | WARNING_STALE_GLOBAL_FILE | metadata source_file_date_check reports DATE_MISMATCH | 2 |
| vsigma_today_candidate_v5_results_summary.csv | CANDIDATE_V5_RESULTS | PASS | output is fresh for requested target date | 1 |

## Candidate Isolation
| check_name | file_name | status | detail |
| --- | --- | --- | --- |
| official_baseline_exists | vsigma_today_competition_report.txt | PASS | baseline file present |
| official_baseline_exists | vsigma_today_competition_shortlist.csv | PASS | baseline file present |
| official_baseline_exists | vsigma_today_competition_top.csv | PASS | baseline file present |
| candidate_specific_name | vsigma_today_candidate_v2_competition_top.csv | PASS | candidate output uses candidate-specific name |
| candidate_file_present_or_optional | vsigma_today_candidate_v2_competition_top.csv | PASS | candidate file present |
| candidate_specific_name | vsigma_today_candidate_v4_competition_top.csv | PASS | candidate output uses candidate-specific name |
| candidate_file_present_or_optional | vsigma_today_candidate_v4_competition_top.csv | PASS | candidate file present |
| candidate_specific_name | vsigma_today_candidate_v5_competition_top.csv | PASS | candidate output uses candidate-specific name |
| candidate_file_present_or_optional | vsigma_today_candidate_v5_competition_top.csv | PASS | candidate file present |
| candidate_specific_name | vsigma_today_candidate_v6_competition_top.csv | PASS | candidate output uses candidate-specific name |
| candidate_file_present_or_optional | vsigma_today_candidate_v6_competition_top.csv | PASS | candidate file present |
| candidate_specific_name | vsigma_today_candidate_v7_competition_top.csv | PASS | candidate output uses candidate-specific name |
| candidate_file_present_or_optional | vsigma_today_candidate_v7_competition_top.csv | PASS | candidate file present |
| candidate_does_not_overwrite_baseline_path | vsigma_today_candidate_v2_competition_top.csv | PASS | candidate path is isolated from official baseline paths |
| candidate_does_not_overwrite_baseline_path | vsigma_today_candidate_v4_competition_top.csv | PASS | candidate path is isolated from official baseline paths |
| candidate_does_not_overwrite_baseline_path | vsigma_today_candidate_v5_competition_top.csv | PASS | candidate path is isolated from official baseline paths |
| candidate_does_not_overwrite_baseline_path | vsigma_today_candidate_v6_competition_top.csv | PASS | candidate path is isolated from official baseline paths |
| candidate_does_not_overwrite_baseline_path | vsigma_today_candidate_v7_competition_top.csv | PASS | candidate path is isolated from official baseline paths |
| snapshot_contains_expected_file | vsigma_today_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v2_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_candidate_v2_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v4_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_candidate_v4_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v5_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_candidate_v5_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v6_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_candidate_v6_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v7_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-28/vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock
PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never overwrites the frozen morning official baseline.
