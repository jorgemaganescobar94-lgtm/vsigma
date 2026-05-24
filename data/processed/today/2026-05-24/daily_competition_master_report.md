# vSIGMA Daily Competition Master Report - 2026-05-24

## Daily Status
PRE_LOCK_PENDING

## Official Baseline Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 0.841525 | 142.388 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 0.819 | 124.626 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | 112.99 | FAILURE_MODE_LOW_CONVERSION |

## Candidate v2 Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 0.802125 | 139.809 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 0.8149 | 123.878 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | 113.275 | FAILURE_MODE_LOW_CONVERSION |

## Candidate v4/v5/v6 Top Picks
### Candidate v4
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392205 | Segunda División | Huesca | Castellón | OVER_1_5 | 0.85236 | 158.115 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 0.8149 | 123.878 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v5
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 0.802125 | 139.809 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 0.8149 | 123.878 | FAILURE_MODE_LOW_CONVERSION |
| 3 | 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | 113.275 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v6
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 0.8149 | 123.878 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | 113.275 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v7
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392205 | Segunda División | Huesca | Castellón | OVER_2_5 | 0.802125 | 139.809 | FAILURE_MODE_LOW_CONVERSION | PRICE_OK |

## Match Script Forecasts
| forecast_rank | fixture_id | league | home_team | away_team | market_primary | predicted_match_script | predicted_score_main | predicted_score_alt | predicted_home_xg_range | predicted_away_xg_range | predicted_home_shots_range | predicted_away_shots_range | predicted_home_sot_range | predicted_away_sot_range | predicted_total_corners_range | predicted_possession_split | predicted_pick_path | predicted_pick_breaker | predicted_total_goals_range | predicted_first_goal_side | predicted_state_gravity | forecast_confidence_band | forecast_inputs_used | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.5; stats=FULL. | 2-3 | 1-2 | 1.2-1.9 | 2.6-3.3 | 11-15 | 12-16 | 4-6 | 4-6 | 6-10 | home 44-52% / away 48-56% | Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 4.0-5.0 | Away slight lean | open exchange | HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| 2 | 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.9; stats=FULL. | 2-2 | 1-2 | 1.3-2.0 | 1.9-2.6 | 11-15 | 11-15 | 5-7 | 4-6 | 7-11 | home 50-58% / away 42-50% | Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 3.3-4.4 | Away slight lean | open exchange | MEDIUM_HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| 3 | 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.4; stats=FULL. | 2-2 | 1-2 | 1.4-2.1 | 1.3-2.0 | 10-14 | 7-11 | 3-5 | 2-4 | 6-10 | home 39-47% / away 53-61% | Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 2.8-3.9 | Either side | open exchange | MEDIUM_HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

## Baseline vs Candidate Comparison
### Candidate v2
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | baseline_market | candidate_v2_market | baseline_raw_prob | candidate_v2_raw_prob | baseline_calibrated_prob | candidate_v2_calibrated_prob | baseline_confidence_score | candidate_v2_confidence_score | baseline_bucket | candidate_v2_bucket | baseline_main_reason | candidate_v2_main_reason | baseline_primary_risk | candidate_v2_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOTH | 1392205 | Huesca vs Castellón | Segunda División | 2 | 1 | OVER_2_5 | OVER_2_5 | 0.7926 | 0.785 | 0.809725 | 0.802125 | 137.759 | 139.809 | ACCURACY_CORE | ACCURACY_CORE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BOTH | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1 | 2 | OVER_2_5 | OVER_2_5 | 0.8244 | 0.7998 | 0.841525 | 0.816925 | 142.388 | 136.313 | ACCURACY_CORE | ACCURACY_CORE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BOTH | 1504827 | Tokyo Verdy vs Yokohama F. Marinos | J1 League | 4 | 4 | OVER_1_5 | OVER_1_5 | 0.8519 | 0.8519 | 0.7719 | 0.7719 | 112.99 | 113.275 | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BOTH | 1545796 | Catanzaro vs Monza | Serie B | 3 | 3 | OVER_1_5 | OVER_1_5 | 0.899 | 0.8949 | 0.819 | 0.8149 | 124.626 | 123.878 | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_STRONG | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_EXTENDED_REVIEW;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

### Candidate v4
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2+CANDIDATE_V4 | 1392205 | Huesca vs Castellón | Segunda División |  | 1.0 | 1.0 |  | OVER_2_5 | OVER_1_5 | OVER_2_5 | DEGRADE_TO_OVER_1_5 | 8.5 | MARKET_DOWNGRADED_TO_OVER_1_5 |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1.0 |  |  | OVER_2_5 |  |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2 | 1504827 | Tokyo Verdy vs Yokohama F. Marinos | J1 League | 3.0 | 3.0 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1545796 | Catanzaro vs Monza | Serie B | 2.0 | 2.0 | 2.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

### Candidate v5
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v5_rank | baseline_market | candidate_v2_market | candidate_v5_market | candidate_v5_original_market | candidate_v5_action | candidate_v5_hint | baseline_primary_risk | candidate_v2_primary_risk | candidate_v5_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2+CANDIDATE_V5 | 1392205 | Huesca vs Castellón | Segunda División |  | 1.0 | 1.0 |  | OVER_2_5 | OVER_2_5 | OVER_2_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1.0 |  |  | OVER_2_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1504827 | Tokyo Verdy vs Yokohama F. Marinos | J1 League | 3.0 | 3.0 | 3.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1545796 | Catanzaro vs Monza | Serie B | 2.0 | 2.0 | 2.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

### Candidate v6
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v6_rank | baseline_market | candidate_v2_market | candidate_v6_market | candidate_v6_action | candidate_v6_alignment | candidate_v6_confidence_adjustment | baseline_primary_risk | candidate_v2_primary_risk | candidate_v6_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2 | 1392205 | Huesca vs Castellón | Segunda División |  | 1.0 |  |  | OVER_2_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1.0 |  |  | OVER_2_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V6 | 1504827 | Tokyo Verdy vs Yokohama F. Marinos | J1 League | 3.0 | 3.0 | 2.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | NEUTRAL | 0.0 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V6 | 1545796 | Catanzaro vs Monza | Serie B | 2.0 | 2.0 | 1.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | NEUTRAL | 0.0 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

### Candidate v7
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v7_rank | baseline_market | candidate_v2_market | candidate_v7_market | candidate_v7_decision | candidate_v7_required_edge | candidate_v7_actual_edge | candidate_v7_drift_status | candidate_v7_clv_direction | candidate_v7_execution_status | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2+CANDIDATE_V7 | 1392205 | Huesca vs Castellón | Segunda División |  | 1.0 | 1.0 |  | OVER_2_5 | OVER_2_5 | PRICE_OK | 0.155 | 0.200205 | NO_DRIFT | CLV_UNAVAILABLE | PRICE_OK | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1.0 |  |  | OVER_2_5 |  |  |  |  |  |  |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2 | 1504827 | Tokyo Verdy vs Yokohama F. Marinos | J1 League | 3.0 | 3.0 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |
| BASELINE+CANDIDATE_V2 | 1545796 | Catanzaro vs Monza | Serie B | 2.0 | 2.0 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  |  |  | 2026-05-24 | 2026-05-24T00:22:01+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-24-20260524T002200Z |

## Price Discipline / CLV / Drift Execution Guard
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | price_discipline_min_edge_required | price_discipline_actual_edge | price_discipline_edge_surplus | price_discipline_drift_status | candidate_v7_prelock_status | candidate_v7_execution_status | clv_direction | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392205 | Huesca | Castellón | OVER_2_5 | PRICE_OK | 0.155 | 0.200205 | 0.045205 | NO_DRIFT |  | PRICE_OK | CLV_UNAVAILABLE | Price cleared configured minimum edge and probability requirements. |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | PRICE_OK | 0.155 | 0.162857 | 0.007857 | NO_DRIFT |  | PRICE_OK | CLV_FLAT | Price cleared configured minimum edge and probability requirements. |
| 1545796 | Catanzaro | Monza | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | 0.143 | 0.14302 | 2e-05 | WATCH_PATTERN | V7_PRELOCK_UNAVAILABLE | V7_PRELOCK_UNAVAILABLE | CLV_FLAT | Fresh pre-lock review is unavailable; v7 cannot confirm execution. |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | 0.143 | 0.176224 | 0.033224 | WATCH_PATTERN | V7_WAITING_FOR_PRELOCK | V7_WAITING_FOR_PRELOCK | CLV_UNAVAILABLE | Watch-pattern drift requires explicit pre-lock confirmation before execution. |

## Pre-Lock Execution Status
- Pre-lock data fresh: YES
- Stale pre-lock excluded: NO
- Execution allowed by v7: 2

### Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | competition_calibrated_prob |
| --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Segunda División | Sporting Gijon | Almeria | OVER_2_5 | 1 | 0.841525 |
| 1545796 | Serie B | Catanzaro | Monza | OVER_1_5 | 2 | 0.819 |
| 1504827 | J1 League | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 3 | 0.7719 |

### Candidate v7 Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | candidate_v7_prelock_status | candidate_v7_execution_status | candidate_v7_execution_allowed_flag | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1392205 | Huesca | Castellón | OVER_2_5 | PRICE_OK |  | PRICE_OK | 1 | Price cleared configured minimum edge and probability requirements. |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | PRICE_OK |  | PRICE_OK | 1 | Price cleared configured minimum edge and probability requirements. |
| 1545796 | Catanzaro | Monza | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | V7_PRELOCK_UNAVAILABLE | V7_PRELOCK_UNAVAILABLE | 0 | Fresh pre-lock review is unavailable; v7 cannot confirm execution. |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRICE_NEEDS_PRELOCK_CONFIRMATION | V7_WAITING_FOR_PRELOCK | V7_WAITING_FOR_PRELOCK | 0 | Watch-pattern drift requires explicit pre-lock confirmation before execution. |

### Active Pre-Lock Decisions
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 971.36 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 1061.3 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 281.24 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

### Stale Pre-Lock Warning
_No stale pre-lock rows excluded._

## Odds Snapshot / CLV Calibration
### CLV Summary
| fixture_id | home_team | away_team | market_primary | experiment_id | pre_price | prelock_price | close_proxy_price | clv_delta | clv_direction | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1379344 | Manchester City | Aston Villa | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 1.6 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1379344 | Manchester City | Aston Villa | BTTS_YES | OFFICIAL_BASELINE | 1.6 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1379347 | Tottenham | Everton | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.84 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392205 | Huesca | Castellón | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.71 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392205 | Huesca | Castellón | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | 1.71 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392205 | Huesca | Castellón | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.71 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392205 | Huesca | Castellón | OVER_2_5 | OFFICIAL_BASELINE | 1.71 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.57 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | OFFICIAL_BASELINE | 1.57 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392209 | Malaga | Racing Santander | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.4 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392210 | Mirandes | Granada CF | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.72 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392214 | Eibar | Cordoba | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.87 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1392215 | Albacete | Real Sociedad II | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | 1.92 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1490315 | Chicago Fire | Toronto FC | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.52 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1490319 | Colorado Rapids | FC Dallas | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.63 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1490322 | Columbus Crew | Atlanta United FC | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.58 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1492273 | Flamengo | Palmeiras | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.37 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1492273 | Flamengo | Palmeiras | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.37 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1492273 | Flamengo | Palmeiras | OVER_1_5 | OFFICIAL_BASELINE | 1.37 | 1.37 | 1.37 | 0.0 | CLV_FLAT |  |  |
| 1494181 | Hammarby FF | AIK Stockholm | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.66 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494183 | Malmo FF | Vasteras SK FK | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.75 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494184 | Sirius | Gais | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.73 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494668 | Bodo/Glimt | Brann | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | 1.53 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1504826 | Mito Hollyhock | Kawasaki Frontale | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.92 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.48 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.48 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OFFICIAL_BASELINE | 1.48 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1537006 | Union St. Gilloise | Anderlecht | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.82 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1537007 | Club Brugge KV | Gent | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | 1.73 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1537007 | Club Brugge KV | Gent | HOME_WIN | OFFICIAL_BASELINE | 1.73 |  |  |  | CLV_UNAVAILABLE |  |  |

### Candidate v7 Calibration Advice
| market_family | failure_mode | drift_status | clv_direction | n | profit_units | roi_percent | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_FLAT | 1 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_UNAVAILABLE | 13 | 0.0 | 0.0 | INSUFFICIENT_CLV_DATA | CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING; do not change thresholds. |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_UNAVAILABLE | 4 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Post-Results Summary
_No rows._

## Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1392207 | Sporting Gijon | Almeria | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 971.36 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 1061.3 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 281.24 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

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
- Official picks registered: 4
- Shadow picks registered: 14
- No-bet records: 1
- Ledger report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_ledger_daily_report.md

## Daily Controller Status
- Next recommended action: WAIT_FOR_PRELOCK
- Pre-lock due time: 2026-05-24T03:33:14.400000+00:00
- Status path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/daily_controller_status.md

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
- Recovery command: `.\.venv\Scripts\python.exe scripts\validate_daily_output_freshness.py --date 2026-05-24`
- Report path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_healthcheck_report.md

### Current Experiment Daily Summary
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_decision | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207.0 | Sporting Gijon | Almeria | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRELOCK_CONFIRMED | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205.0 | Huesca | Castellón | OVER_2_5 |  | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRELOCK_CONFIRMED | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V4_O25_FIREWALL | 1392205.0 | Huesca | Castellón | OVER_1_5 |  | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205.0 | Huesca | Castellón | OVER_2_5 |  | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRELOCK_CONFIRMED | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1545796.0 | Catanzaro | Monza | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1492273.0 | Flamengo | Palmeiras | OVER_1_5 | PRELOCK_CONFIRMED | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205.0 | Huesca | Castellón | OVER_2_5 |  | PENDING |  | PRE_REGISTERED |
| OFFICIAL_BASELINE | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1504827.0 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |

### Experiment Performance Summary
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 18 | 5 | 3 | 2 | -0.53 | -10.6 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 20 | 4 | 2 | 2 | -1.05 | -26.25 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 17 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 20 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 19 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 10 | 0 | 0 | 0 | 0.0 |  | PRICE_DISCIPLINE_UNTESTED |

## Promotion & Threshold Governance
- Official baseline status: KEEP_OFFICIAL_BASELINE
- Governance dashboard: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_governance_dashboard.md

### Candidate Promotion Recommendations
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 5 | -10.6 | 0.296723 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 4 | -26.25 | 0.352548 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 4 | -26.25 | 0.352548 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 4 | -26.25 | 0.352548 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 4 | -26.25 | 0.352548 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

### Threshold Recommendations
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 13 | 0.0 | CLV_UNAVAILABLE | INSUFFICIENT_CLV_DATA |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 4 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 0.0 | CLV_FLAT | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 1 | 52.0 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V4_O25_FIREWALL | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |

- CLV data sufficiency: INSUFFICIENT_CLV_DATA
- Drift alerts: 0

## Failure Mode Summary
| failure_mode | rows |
| --- | --- |
| FAILURE_MODE_LOW_CONVERSION | 14 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.176; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.143; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.187; market_fit=SAFE_OK | 1 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK | 1 |

## Freshness Validation
| file_name | candidate_version | status | detail | rows |
| --- | --- | --- | --- | --- |
| vsigma_today_competition_shortlist.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 4 |
| vsigma_today_competition_top.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_competition_shortlist.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 4 |
| vsigma_today_candidate_v2_competition_top.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_competition_shortlist.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 4 |
| vsigma_today_candidate_v4_competition_top.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v5_competition_shortlist.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 4 |
| vsigma_today_candidate_v5_competition_top.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v6_competition_shortlist.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v6_competition_top.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v7_competition_shortlist.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 4 |
| vsigma_today_candidate_v7_competition_top.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2.csv | COMPARISON | PASS | output is fresh for requested target date | 4 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | COMPARISON | PASS | output is fresh for requested target date | 4 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | COMPARISON | PASS | output is fresh for requested target date | 4 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | COMPARISON | PASS | output is fresh for requested target date | 4 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | COMPARISON | PASS | output is fresh for requested target date | 4 |
| vsigma_today_match_script_forecasts.csv | FORECAST | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v2_match_script_forecasts.csv | FORECAST_CANDIDATE_V2 | PASS | output is fresh for requested target date | 3 |
| vsigma_today_candidate_v4_match_script_forecasts.csv | FORECAST_CANDIDATE_V4 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_prelock_competition_top.csv | OFFICIAL_BASELINE_PRELOCK | PASS | output is fresh for requested target date | 1 |
| vsigma_today_prelock_comparison.csv | PRELOCK_COMPARISON | PASS | output is fresh for requested target date | 3 |
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
| snapshot_contains_expected_file | vsigma_today_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v2_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_candidate_v2_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v4_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_candidate_v4_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v5_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_candidate_v5_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v6_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_candidate_v6_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v7_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-24/vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock
PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never overwrites the frozen morning official baseline.
