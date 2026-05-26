# vSIGMA Daily Competition Master Report - 2026-05-26

## Daily Status
PRE_LOCK_PENDING

## Official Baseline Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1535324 | CONMEBOL Libertadores | LDU de Quito | Always Ready | UNDER_3_5 | 0.770525 | 127.772 | FAILURE_MODE_AVALANCHE_RISK |

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
| forecast_rank | fixture_id | league | home_team | away_team | market_primary | predicted_match_script | predicted_score_main | predicted_score_alt | predicted_home_xg_range | predicted_away_xg_range | predicted_home_shots_range | predicted_away_shots_range | predicted_home_sot_range | predicted_away_sot_range | predicted_total_corners_range | predicted_possession_split | predicted_pick_path | predicted_pick_breaker | predicted_total_goals_range | predicted_first_goal_side | predicted_state_gravity | forecast_confidence_band | forecast_inputs_used | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1535324 | CONMEBOL Libertadores | LDU de Quito | Always Ready | UNDER_3_5 | Controlled script with enough structure to avoid a four-goal game; the breaker is an early goal that opens the match too far. Total-goal lean: 2.5; stats=PARTIAL. | 1-1 | 2-1 | 0.9-1.6 | 0.9-1.6 | 10-14 | 13-17 | 3-5 | 4-6 | 9-13 | home 40-48% / away 52-60% | Pick wins if game state stays structured and neither side turns the match into repeated transition attacks. | An early goal or transition chain breaks the controlled script and creates too many goals. | 2.0-3.1 | Either side | controlled low-volatility state | MEDIUM_HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

## Baseline vs Candidate Comparison
### Candidate v2
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | baseline_market | candidate_v2_market | baseline_raw_prob | candidate_v2_raw_prob | baseline_calibrated_prob | candidate_v2_calibrated_prob | baseline_confidence_score | candidate_v2_confidence_score | baseline_bucket | candidate_v2_bucket | baseline_main_reason | candidate_v2_main_reason | baseline_primary_risk | candidate_v2_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE_ONLY | 1535324 | LDU de Quito vs Always Ready | CONMEBOL Libertadores | 1 |  | UNDER_3_5 |  | 0.7534 |  | 0.770525 |  | 127.772 |  | ACCURACY_CORE |  | ACCURACY_CORE_PRIORITY;ACCURACY_MARKET_STABLE;ACCURACY_FAILURE_MODE_ACCEPTABLE |  | FAILURE_MODE_AVALANCHE_RISK |  | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

### Candidate v4
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE | 1535324 | LDU de Quito vs Always Ready | CONMEBOL Libertadores | 1 |  |  | UNDER_3_5 |  |  |  |  |  |  | FAILURE_MODE_AVALANCHE_RISK |  |  | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

### Candidate v5
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v5_rank | baseline_market | candidate_v2_market | candidate_v5_market | candidate_v5_original_market | candidate_v5_action | candidate_v5_hint | baseline_primary_risk | candidate_v2_primary_risk | candidate_v5_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE | 1535324 | LDU de Quito vs Always Ready | CONMEBOL Libertadores | 1 |  |  | UNDER_3_5 |  |  |  |  |  | FAILURE_MODE_AVALANCHE_RISK |  |  | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

### Candidate v6
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v6_rank | baseline_market | candidate_v2_market | candidate_v6_market | candidate_v6_action | candidate_v6_alignment | candidate_v6_confidence_adjustment | baseline_primary_risk | candidate_v2_primary_risk | candidate_v6_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE | 1535324 | LDU de Quito vs Always Ready | CONMEBOL Libertadores | 1 |  |  | UNDER_3_5 |  |  |  |  |  | FAILURE_MODE_AVALANCHE_RISK |  |  | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

### Candidate v7
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v7_rank | baseline_market | candidate_v2_market | candidate_v7_market | candidate_v7_decision | candidate_v7_required_edge | candidate_v7_actual_edge | candidate_v7_drift_status | candidate_v7_clv_direction | candidate_v7_execution_status | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE | 1535324 | LDU de Quito vs Always Ready | CONMEBOL Libertadores | 1 |  |  | UNDER_3_5 |  |  |  |  |  |  |  |  | 2026-05-26 | 2026-05-26T19:32:48+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-26-20260526T193248Z |

## Price Discipline / CLV / Drift Execution Guard
_No rows._

## Pre-Lock Execution Status
- Pre-lock data fresh: YES
- Stale pre-lock excluded: NO
- Execution allowed by v7: 0

### Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | competition_calibrated_prob |
| --- | --- | --- | --- | --- | --- | --- |
| 1535324 | CONMEBOL Libertadores | LDU de Quito | Always Ready | UNDER_3_5 | 1 | 0.770525 |

### Candidate v7 Pre-Lock Status
_No rows._

### Active Pre-Lock Decisions
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1535324 | LDU de Quito | Always Ready | UNDER_3_5 | OUTSIDE_PRELOCK_WINDOW | 147.61 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

### Stale Pre-Lock Warning
_No stale pre-lock rows excluded._

## Odds Snapshot / CLV Calibration
### CLV Summary
| fixture_id | home_team | away_team | market_primary | experiment_id | pre_price | prelock_price | close_proxy_price | clv_delta | clv_direction | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1535324 | LDU de Quito | Always Ready | UNDER_3_5 | DEEP_ANALYSIS_CANDIDATES | 1.57 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535324 | LDU de Quito | Always Ready | UNDER_3_5 | OFFICIAL_BASELINE | 1.57 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545406 | SpVgg Greuther Fürth | Rot-Weiß Essen | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.7 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545406 | SpVgg Greuther Fürth | Rot-Weiß Essen | OVER_2_5 | OFFICIAL_BASELINE | 1.7 |  |  |  | CLV_UNAVAILABLE |  |  |

### Candidate v7 Calibration Advice
| market_family | failure_mode | drift_status | clv_direction | n | profit_units | roi_percent | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UNDER_3_5 | ANY | UNKNOWN | CLV_UNAVAILABLE | 1 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Post-Results Summary
_No rows._

## Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1535324 | LDU de Quito | Always Ready | UNDER_3_5 | OUTSIDE_PRELOCK_WINDOW | 147.61 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

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
- Official picks registered: 1
- Shadow picks registered: 0
- No-bet records: 6
- Ledger report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_ledger_daily_report.md

## Daily Controller Status
- Next recommended action: WAIT_FOR_PRELOCK
- Pre-lock due time: 2026-05-26T20:30:24.600000+00:00
- Status path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/daily_controller_status.md

## Daily Supervisor
- Supervisor latest status: SUPERVISOR_STATUS_NOT_AVAILABLE
- Last run mode/time: NOT_AVAILABLE / NOT_AVAILABLE
- Next recommended action: WAIT_FOR_PRELOCK
- Scheduled automation status: REGISTRATION_SCRIPT_AVAILABLE_STATUS_NOT_QUERIED
- Logs path: C:\vsigma\automation_logs\supervisor
- Report path: NOT_AVAILABLE

## Healthcheck
- Global health status: WARNING
- Critical warnings: freshness_report: WARNING - validation report contains warning rows
- Recovery command: `.\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-26`
- Report path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_healthcheck_report.md

### Current Experiment Daily Summary
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_decision | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V4_O25_FIREWALL |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V5_PLAYER_IMPACT |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V6_API_PREDICTIONS |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V7_PRICE_DISCIPLINE |  |  |  |  |  |  |  | NO_BET_RECORD |
| OFFICIAL_BASELINE | 1535324.0 | LDU de Quito | Always Ready | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |

### Experiment Performance Summary
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 15 | 7 | 4 | 3 | -1.18 | -16.857143 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 19 | 6 | 3 | 3 | -1.7 | -28.333333 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 18 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 19 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 17 | 5 | 3 | 2 | -0.7 | -14.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 9 | 1 | 0 | 1 | -1.0 | -100.0 | PRICE_DISCIPLINE_UNTESTED |

## Promotion & Threshold Governance
- Official baseline status: KEEP_OFFICIAL_BASELINE
- Governance dashboard: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_governance_dashboard.md

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
| UNDER_3_5 | ANY | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
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
| failure_mode | rows |
| --- | --- |
| FAILURE_MODE_AVALANCHE_RISK | 1 |
| FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.116; market_fit=SAFE_OK | 1 |

## Freshness Validation
| file_name | candidate_version | status | detail | rows |
| --- | --- | --- | --- | --- |
| vsigma_today_competition_shortlist.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 1 |
| vsigma_today_competition_top.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v2_competition_shortlist.csv | CANDIDATE_V2 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v2_competition_top.csv | CANDIDATE_V2 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v4_competition_shortlist.csv | CANDIDATE_V4 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v4_competition_top.csv | CANDIDATE_V4 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v5_competition_shortlist.csv | CANDIDATE_V5 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v5_competition_top.csv | CANDIDATE_V5 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v6_competition_shortlist.csv | CANDIDATE_V6 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v6_competition_top.csv | CANDIDATE_V6 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v7_competition_shortlist.csv | CANDIDATE_V7 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v7_competition_top.csv | CANDIDATE_V7 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_baseline_vs_candidate_v2.csv | COMPARISON | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | COMPARISON | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | COMPARISON | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | COMPARISON | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | COMPARISON | PASS | output is fresh for requested target date | 1 |
| vsigma_today_match_script_forecasts.csv | FORECAST | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v2_match_script_forecasts.csv | FORECAST_CANDIDATE_V2 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_candidate_v4_match_script_forecasts.csv | FORECAST_CANDIDATE_V4 | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_prelock_competition_top.csv | OFFICIAL_BASELINE_PRELOCK | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_prelock_comparison.csv | PRELOCK_COMPARISON | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| today_pipeline_report.csv | GLOBAL_LATEST_CONTEXT | PASS | snapshot context file present | 1 |
| today_post_results_report.csv | GLOBAL_LATEST_CONTEXT | WARNING_STALE_GLOBAL_FILE | snapshot context file not present yet | 0 |

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
| snapshot_contains_expected_file | vsigma_today_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v2_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_candidate_v2_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v4_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_candidate_v4_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v5_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_candidate_v5_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v6_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_candidate_v6_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v7_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-26/vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock
PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never overwrites the frozen morning official baseline.
