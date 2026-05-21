# vSIGMA Daily Competition Master Report - 2026-05-21

## Daily Status
PRE_LOCK_REVIEWED

## Official Baseline Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 0.801325 | 137.736 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8157 | 125.862 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8613 | 111.027 | FAILURE_MODE_AVALANCHE_RISK |

## Candidate v2 Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | 137.416 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | 126.307 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8583 | 110.922 | FAILURE_MODE_AVALANCHE_RISK |

## Candidate v4/v5/v6 Top Picks
### Candidate v4
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_1_5 | 0.84996 | 156.544 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | 126.307 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8583 | 110.922 | FAILURE_MODE_AVALANCHE_RISK |

### Candidate v5
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | 137.416 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | 126.307 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8583 | 110.922 | FAILURE_MODE_AVALANCHE_RISK |

### Candidate v6
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 0.8181 | 126.307 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8643 | 112.422 | FAILURE_MODE_AVALANCHE_RISK |

### Candidate v7
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 0.797325 | 137.416 | FAILURE_MODE_LOW_CONVERSION | PRICE_OK |
| 2 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 0.8583 | 110.922 | FAILURE_MODE_AVALANCHE_RISK | PRICE_OK |

## Match Script Forecasts
| forecast_rank | fixture_id | league | home_team | away_team | market_primary | predicted_match_script | predicted_score_main | predicted_score_alt | predicted_home_xg_range | predicted_away_xg_range | predicted_home_shots_range | predicted_away_shots_range | predicted_home_sot_range | predicted_away_sot_range | predicted_total_corners_range | predicted_possession_split | predicted_pick_path | predicted_pick_breaker | predicted_total_goals_range | predicted_first_goal_side | predicted_state_gravity | forecast_confidence_band | forecast_inputs_used | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.2; stats=FULL. | 1-3 | 1-2 | 1.1-1.8 | 2.4-3.1 | 13-17 | 12-16 | 4-6 | 4-6 | 8-12 | home 47-55% / away 45-53% | Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 3.6-4.7 | Away slight lean | open exchange | HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| 2 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.8; stats=FULL. | 2-2 | 1-2 | 2.0-2.7 | 1.2-1.9 | 12-16 | 11-15 | 5-7 | 4-6 | 7-11 | home 48-56% / away 44-52% | Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 3.3-4.4 | Home slight lean | open exchange | MEDIUM_HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| 3 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | Controlled script with enough structure to avoid a four-goal game; the breaker is an early goal that opens the match too far. Total-goal lean: 1.7; stats=PARTIAL. | 1-0 | 2-0 | 0.9-1.6 | 0.1-0.8 | 11-15 | 10-14 | 2-4 | 2-4 | 5-9 | home 51-59% / away 41-49% | Pick wins if game state stays structured and neither side turns the match into repeated transition attacks. | An early goal or transition chain breaks the controlled script and creates too many goals. | 1.1-2.2 | Home slight lean | controlled low-volatility state | MEDIUM_HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

## Baseline vs Candidate Comparison
### Candidate v2
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | baseline_market | candidate_v2_market | baseline_raw_prob | candidate_v2_raw_prob | baseline_calibrated_prob | candidate_v2_calibrated_prob | baseline_confidence_score | candidate_v2_confidence_score | baseline_bucket | candidate_v2_bucket | baseline_main_reason | candidate_v2_main_reason | baseline_primary_risk | candidate_v2_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOTH | 1535208 | Gremio vs Palestino | CONMEBOL Sudamericana | 3 | 3 | UNDER_3_5 | UNDER_3_5 | 0.9113 | 0.9083 | 0.8613 | 0.8583 | 111.027 | 110.922 | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BOTH | 1535302 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | 2 | 2 | OVER_1_5 | OVER_1_5 | 0.8957 | 0.8981 | 0.8157 | 0.8181 | 125.862 | 126.307 | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BOTH | 1545410 | Brondby vs FC Copenhagen | Superliga | 1 | 1 | OVER_2_5 | OVER_2_5 | 0.7842 | 0.7802 | 0.801325 | 0.797325 | 137.736 | 137.416 | ACCURACY_CORE | ACCURACY_CORE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

### Candidate v4
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1535208 | Gremio vs Palestino | CONMEBOL Sudamericana | 3 | 3 | 3 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1535302 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | 2 | 2 | 2 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1545410 | Brondby vs FC Copenhagen | Superliga | 1 | 1 | 1 | OVER_2_5 | OVER_2_5 | OVER_1_5 | OVER_2_5 | DEGRADE_TO_OVER_1_5 | 8.5 | MARKET_DOWNGRADED_TO_OVER_1_5 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

### Candidate v5
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v5_rank | baseline_market | candidate_v2_market | candidate_v5_market | candidate_v5_original_market | candidate_v5_action | candidate_v5_hint | baseline_primary_risk | candidate_v2_primary_risk | candidate_v5_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1535208 | Gremio vs Palestino | CONMEBOL Sudamericana | 3 | 3 | 3 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1535302 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | 2 | 2 | 2 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1545410 | Brondby vs FC Copenhagen | Superliga | 1 | 1 | 1 | OVER_2_5 | OVER_2_5 | OVER_2_5 | OVER_2_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

### Candidate v6
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v6_rank | baseline_market | candidate_v2_market | candidate_v6_market | candidate_v6_action | candidate_v6_alignment | candidate_v6_confidence_adjustment | baseline_primary_risk | candidate_v2_primary_risk | candidate_v6_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V6 | 1535208 | Gremio vs Palestino | CONMEBOL Sudamericana | 3 | 3 | 2.0 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | API_PREDICTION_ALIGNED_STRENGTHEN | ALIGNED | 1.5 | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | FAILURE_MODE_AVALANCHE_RISK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V6 | 1535302 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | 2 | 2 | 1.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | NEUTRAL | 0.0 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2 | 1545410 | Brondby vs FC Copenhagen | Superliga | 1 | 1 |  | OVER_2_5 | OVER_2_5 |  |  |  |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |  | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

### Candidate v7
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v7_rank | baseline_market | candidate_v2_market | candidate_v7_market | candidate_v7_decision | candidate_v7_required_edge | candidate_v7_actual_edge | candidate_v7_drift_status | candidate_v7_clv_direction | candidate_v7_execution_status | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V7 | 1535208 | Gremio vs Palestino | CONMEBOL Sudamericana | 3 | 3 | 2.0 | UNDER_3_5 | UNDER_3_5 | UNDER_3_5 | PRICE_OK | 0.055 | 0.173006 | UNKNOWN | CLV_FLAT | PRICE_OK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2 | 1535302 | Flamengo vs Estudiantes L.P. | CONMEBOL Libertadores | 2 | 2 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  |  |  | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V7 | 1545410 | Brondby vs FC Copenhagen | Superliga | 1 | 1 | 1.0 | OVER_2_5 | OVER_2_5 | OVER_2_5 | PRICE_OK | 0.155 | 0.248285 | NO_DRIFT | CLV_FLAT | PRICE_OK | 2026-05-21 | 2026-05-20T23:52:46+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-21-20260520T235245Z |

## Price Discipline / CLV / Drift Execution Guard
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | price_discipline_min_edge_required | price_discipline_actual_edge | price_discipline_edge_surplus | price_discipline_drift_status | candidate_v7_prelock_status | candidate_v7_execution_status | clv_direction | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | PRICE_OK | 0.155 | 0.248285 | 0.093285 | NO_DRIFT |  | PRICE_OK | CLV_FLAT | Price cleared configured minimum edge and probability requirements. |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | 0.143 | 0.193875 | 0.050875 | WATCH_PATTERN | V7_PRELOCK_UNAVAILABLE | V7_PRELOCK_UNAVAILABLE | CLV_FLAT | Fresh pre-lock review is unavailable; v7 cannot confirm execution. |
| 1535208 | Gremio | Palestino | UNDER_3_5 | PRICE_OK | 0.055 | 0.173006 | 0.118006 | UNKNOWN |  | PRICE_OK | CLV_FLAT | Price cleared configured minimum edge and probability requirements. |

## Pre-Lock Execution Status
- Pre-lock data fresh: YES
- Stale pre-lock excluded: NO
- Execution allowed by v7: 2

### Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | competition_calibrated_prob |
| --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | 1 | 0.801325 |
| 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | 2 | 0.8157 |
| 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | 3 | 0.8613 |

### Candidate v7 Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | candidate_v7_prelock_status | candidate_v7_execution_status | candidate_v7_execution_allowed_flag | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | PRICE_OK |  | PRICE_OK | 1 | Price cleared configured minimum edge and probability requirements. |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | V7_PRELOCK_UNAVAILABLE | V7_PRELOCK_UNAVAILABLE | 0 | Fresh pre-lock review is unavailable; v7 cannot confirm execution. |
| 1535208 | Gremio | Palestino | UNDER_3_5 | PRICE_OK |  | PRICE_OK | 1 | Price cleared configured minimum edge and probability requirements. |

### Active Pre-Lock Decisions
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 998.39 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | 38.5 | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | 8.43 | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |

### Stale Pre-Lock Warning
_No stale pre-lock rows excluded._

## Odds Snapshot / CLV Calibration
### CLV Summary
| fixture_id | home_team | away_team | market_primary | experiment_id | pre_price | prelock_price | close_proxy_price | clv_delta | clv_direction | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494228 | IF Elfsborg | Mjallby AIF | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.38 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535204 | Atletico-MG | Cienciano | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 2.38 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535208 | Gremio | Palestino | UNDER_3_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.36 |  | 1.36 | 0.0 | CLV_FLAT | WIN | 0.36 |
| 1535208 | Gremio | Palestino | UNDER_3_5 | CANDIDATE_V7_PRICE_DISCIPLINE | 1.36 |  | 1.36 | 0.0 | CLV_FLAT | WIN | 0.36 |
| 1535208 | Gremio | Palestino | UNDER_3_5 | DEEP_ANALYSIS_CANDIDATES | 1.36 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535208 | Gremio | Palestino | UNDER_3_5 | OFFICIAL_BASELINE | 1.36 | 1.36 | 1.36 | 0.0 | CLV_FLAT | WIN | 0.36 |
| 1535209 | Independiente Petrolero | Botafogo | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 2.0 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535209 | Independiente Petrolero | Botafogo | BTTS_YES | OFFICIAL_BASELINE | 2.0 |  | 2.0 | 0.0 | CLV_FLAT | LOSS | -1.0 |
| 1535213 | Puerto Cabello | Juventud | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.37 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535215 | River Plate | RB Bragantino | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.5 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535301 | Cusco | Independiente Medellin | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.95 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.42 |  | 1.42 | 0.0 | CLV_FLAT | LOSS | -1.0 |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.42 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | OFFICIAL_BASELINE | 1.42 | 1.42 | 1.42 | 0.0 | CLV_FLAT | LOSS | -1.0 |
| 1535305 | Junior | Sporting Cristal | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.34 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535306 | Deportivo La Guaira | Independ. Rivadavia | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.5 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1535306 | Deportivo La Guaira | Independ. Rivadavia | OVER_1_5 | OFFICIAL_BASELINE | 1.5 |  | 1.5 | 0.0 | CLV_FLAT | PENDING |  |
| 1535309 | Palmeiras | Cerro Porteno | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 3.0 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.88 |  | 1.88 | 0.0 | CLV_FLAT | PENDING |  |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | 1.88 |  | 1.88 | 0.0 | CLV_FLAT | PENDING |  |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.88 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OFFICIAL_BASELINE | 1.88 |  | 1.88 | 0.0 | CLV_FLAT | PENDING |  |
| 1545412 | Utrecht | Heerenveen | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.75 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545417 | VfL Wolfsburg | SC Paderborn 07 | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.82 |  |  |  | CLV_UNAVAILABLE |  |  |

### Candidate v7 Calibration Advice
| market_family | failure_mode | drift_status | clv_direction | n | profit_units | roi_percent | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_FLAT | 2 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_UNAVAILABLE | 4 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_FLAT | 3 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_UNAVAILABLE | 1 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| UNDER_3_5 | ANY | UNKNOWN | CLV_FLAT | 3 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| UNDER_3_5 | ANY | UNKNOWN | CLV_UNAVAILABLE | 3 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Post-Results Summary
| mode | pick_count | wins | losses | profit_units | roi_percent | pending_rows | candidate_version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_EXECUTION_SHORTLIST | 5.0 | 1.0 | 2.0 | -1.64 | -54.666667 | 2.0 | OFFICIAL_RESULTS |
| SHADOW_CANDIDATE_V2 | 3.0 | 1.0 | 1.0 | -0.64 | -32.0 | 1.0 | CANDIDATE_V2_RESULTS |
| SHADOW_CANDIDATE_V4_O25_LOW_CONVERSION_FIREWALL | 3.0 | 1.0 | 1.0 | -0.64 | -32.0 | 1.0 | CANDIDATE_V4_RESULTS |
| SHADOW_CANDIDATE_V5_PLAYER_IMPACT | 3.0 | 1.0 | 1.0 | -0.64 | -32.0 | 1.0 | CANDIDATE_V5_RESULTS |
| SHADOW_CANDIDATE_V6_API_PREDICTIONS_BENCHMARK | 2.0 | 1.0 | 1.0 | -0.64 | -32.0 | 0.0 | CANDIDATE_V6_RESULTS |
| SHADOW_CANDIDATE_V7_PRICE_DISCIPLINE_CLV_DRIFT_GUARD | 2.0 | 1.0 | 0.0 | 0.36 | 36.0 | 1.0 | CANDIDATE_V7_RESULTS |

## Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1545410 | Brondby | FC Copenhagen | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 998.39 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1535302 | Flamengo | Estudiantes L.P. | OVER_1_5 | IN_PRELOCK_WINDOW | 38.5 | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| 1535208 | Gremio | Palestino | UNDER_3_5 | IN_PRELOCK_WINDOW | 8.43 | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |

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
- Official picks registered: 3
- Shadow picks registered: 13
- No-bet records: 1
- Ledger report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_ledger_daily_report.md

## Daily Controller Status
- Next recommended action: RUN_POST_AFTER_FINISH
- Pre-lock due time: 2026-05-20T22:31:10.800000+00:00
- Status path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/daily_controller_status.md

## Daily Supervisor
- Supervisor latest status: SUPERVISOR_STATUS_NOT_AVAILABLE
- Last run mode/time: NOT_AVAILABLE / NOT_AVAILABLE
- Next recommended action: RUN_POST_AFTER_FINISH
- Scheduled automation status: REGISTRATION_SCRIPT_AVAILABLE_STATUS_NOT_QUERIED
- Logs path: C:\vsigma\automation_logs\supervisor
- Report path: NOT_AVAILABLE

## Healthcheck
- Global health status: WARNING
- Critical warnings: freshness_report: WARNING - validation report contains warning rows
- Recovery command: `.\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-21`
- Report path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_healthcheck_report.md

### Current Experiment Daily Summary
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_decision | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PENDING |
| OFFICIAL_BASELINE | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK_NOT_AVAILABLE | LOSS | -1.0 | SETTLED |
| OFFICIAL_BASELINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PENDING |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK_NOT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V4_O25_FIREWALL | 1545410.0 | Brondby | FC Copenhagen | OVER_1_5 |  | PENDING |  | PENDING |
| CANDIDATE_V4_O25_FIREWALL | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK_NOT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PENDING |
| CANDIDATE_V5_PLAYER_IMPACT | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK_NOT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1535302.0 | Flamengo | Estudiantes L.P. | OVER_1_5 | PRELOCK_NOT_AVAILABLE | LOSS | -1.0 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545410.0 | Brondby | FC Copenhagen | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PENDING |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535208.0 | Gremio | Palestino | UNDER_3_5 | PRELOCK_NOT_AVAILABLE | WIN | 0.36 | SETTLED |

### Experiment Performance Summary
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 18 | 8 | 5 | 3 | -0.57 | -7.125 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 16 | 7 | 4 | 3 | -1.09 | -15.571429 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 15 | 7 | 4 | 3 | -1.09 | -15.571429 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 16 | 7 | 4 | 3 | -1.09 | -15.571429 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 15 | 7 | 4 | 3 | -1.09 | -15.571429 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 11 | 1 | 1 | 0 | 0.36 | 36.0 | PRICE_DISCIPLINE_UNTESTED |

## Promotion & Threshold Governance
- Official baseline status: KEEP_OFFICIAL_BASELINE
- Governance dashboard: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_governance_dashboard.md

### Candidate Promotion Recommendations
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 8 | -7.125 | 0.276005 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 7 | -15.571429 | 0.305455 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 7 | -15.571429 | 0.305455 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 7 | -15.571429 | 0.305455 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 7 | -15.571429 | 0.305218 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 36.0 | 0.020079 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

### Threshold Recommendations
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 6 | -24.166667 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 6 | -24.166667 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 6 | -24.166667 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 6 | -24.166667 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 6 | -24.166667 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 4 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| UNDER_3_5 | ANY | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| UNDER_3_5 | ANY | CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V4_O25_FIREWALL | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V5_PLAYER_IMPACT | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V6_API_PREDICTIONS | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| UNDER_3_5 | AVALANCHE_RISK | OFFICIAL_BASELINE | 1 | 36.0 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 1 | 52.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |

- CLV data sufficiency: CLV_DATA_SUFFICIENT_FOR_REVIEW
- Drift alerts: 0

## Failure Mode Summary
| failure_mode | rows |
| --- | --- |
| FAILURE_MODE_LOW_CONVERSION | 10 |
| FAILURE_MODE_AVALANCHE_RISK | 6 |
| FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.173; market_fit=SAFE_OK | 5 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.248; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.194; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.252; market_fit=SAFE_OK | 1 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.191; market_fit=SAFE_OK | 1 |
| FAILURE_MODE_AVALANCHE_RISK; market=UNDER_3_5; edge=0.176; market_fit=SAFE_OK | 1 |

## Freshness Validation
| file_name | candidate_version | status | detail | rows |
| --- | --- | --- | --- | --- |
| vsigma_today_competition_shortlist.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 3 |
| vsigma_today_competition_top.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_competition_shortlist.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_competition_top.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_competition_shortlist.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_competition_top.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v5_competition_shortlist.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v5_competition_top.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v6_competition_shortlist.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v6_competition_top.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v7_competition_shortlist.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v7_competition_top.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_baseline_vs_candidate_v2.csv | COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_today_match_script_forecasts.csv | FORECAST | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_match_script_forecasts.csv | FORECAST_CANDIDATE_V2 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_match_script_forecasts.csv | FORECAST_CANDIDATE_V4 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_prelock_competition_top.csv | OFFICIAL_BASELINE_PRELOCK | PASS | output is fresh for requested target date | 2 |
| vsigma_today_prelock_comparison.csv | PRELOCK_COMPARISON | PASS | output is fresh for requested target date | 3 |
| vsigma_execution_shortlist_results_ledger.csv | OFFICIAL_RESULTS | PASS | output is fresh for requested target date | 5 |
| vsigma_execution_shortlist_results_summary.csv | OFFICIAL_RESULTS | PASS | output is fresh for requested target date | 192 |
| vsigma_today_candidate_v2_results_ledger.csv | CANDIDATE_V2_RESULTS | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_results_summary.csv | CANDIDATE_V2_RESULTS | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v4_results_ledger.csv | CANDIDATE_V4_RESULTS | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_results_summary.csv | CANDIDATE_V4_RESULTS | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v5_results_ledger.csv | CANDIDATE_V5_RESULTS | PASS | output is fresh for requested target date | 3 |
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
| snapshot_contains_expected_file | vsigma_today_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v2_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_candidate_v2_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v4_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_candidate_v4_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v5_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_candidate_v5_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v6_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_candidate_v6_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v7_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-21/vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock
PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never overwrites the frozen morning official baseline.
