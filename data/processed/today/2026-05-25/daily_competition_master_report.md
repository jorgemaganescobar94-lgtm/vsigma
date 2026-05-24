# vSIGMA Daily Competition Master Report - 2026-05-25

## Daily Status
PRE_LOCK_PENDING

## Official Baseline Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 0.81736 | 154.173 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | 0.807425 | 133.361 | FAILURE_MODE_LOW_CONVERSION |

## Candidate v2 Top Picks
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 0.80906 | 152.696 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | 0.813825 | 134.423 | FAILURE_MODE_LOW_CONVERSION |

## Candidate v4/v5/v6 Top Picks
### Candidate v4
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | 0.85776 | 153.446 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 0.80906 | 152.696 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v5
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 0.80906 | 152.696 | FAILURE_MODE_LOW_CONVERSION |
| 2 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | 0.813825 | 134.423 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v6
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 0.80906 | 152.696 | FAILURE_MODE_LOW_CONVERSION |

### Candidate v7
| accuracy_mode_rank | fixture_id | league | home_team | away_team | market_primary | competition_calibrated_prob | accuracy_confidence_score | accuracy_primary_risk | price_discipline_decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | 0.813825 | 134.423 | FAILURE_MODE_LOW_CONVERSION | PRICE_OK |

## Match Script Forecasts
| forecast_rank | fixture_id | league | home_team | away_team | market_primary | predicted_match_script | predicted_score_main | predicted_score_alt | predicted_home_xg_range | predicted_away_xg_range | predicted_home_shots_range | predicted_away_shots_range | predicted_home_sot_range | predicted_away_sot_range | predicted_total_corners_range | predicted_possession_split | predicted_pick_path | predicted_pick_breaker | predicted_total_goals_range | predicted_first_goal_side | predicted_state_gravity | forecast_confidence_band | forecast_inputs_used | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | Moderately open game where two goals can arrive through sustained chance volume; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 3.7; stats=FULL. | 1-3 | 0-3 | 0.8-1.5 | 2.2-2.9 | 14-18 | 12-16 | 4-6 | 5-7 | 8-12 | home 45-53% / away 47-55% | Pick wins if either favorite pressure creates a second goal or both sides trade enough chances for a 1-1/2-0 type path. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 3.2-4.3 | Away slight lean | open exchange | HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| 2 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | Open, active match with both penalty boxes reached often; shot volume is expected, but finishing drag is the main volatility point. Total-goal lean: 4.2; stats=FULL. | 2-2 | 2-1 | 2.0-2.7 | 1.5-2.2 | 13-17 | 9-13 | 4-6 | 4-6 | 8-12 | home 48-56% / away 44-52% | Pick wins if the projected chance volume turns into three goals, usually via early tempo or both teams contributing. | Good territory without conversion: shots arrive but finish quality or goalkeeper variance drags the score under the market. | 3.7-4.8 | Home slight lean | open exchange | HIGH_FORECAST_CONFIDENCE | market+projected_goals+competition_probability+pick_risk+recent_stats+league_coverage | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | FORECAST | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

## Baseline vs Candidate Comparison
### Candidate v2
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | baseline_market | candidate_v2_market | baseline_raw_prob | candidate_v2_raw_prob | baseline_calibrated_prob | candidate_v2_calibrated_prob | baseline_confidence_score | candidate_v2_confidence_score | baseline_bucket | candidate_v2_bucket | baseline_main_reason | candidate_v2_main_reason | baseline_primary_risk | candidate_v2_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BOTH | 1494179 | IFK Goteborg vs Mjallby AIF | Allsvenskan | 1 | 1 | OVER_1_5 | OVER_1_5 | 0.885 | 0.8767 | 0.81736 | 0.80906 | 154.173 | 152.696 | ACCURACY_CORE | ACCURACY_CORE | ACCURACY_CORE_PRIORITY;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_CORE_PRIORITY;ACCURACY_MARKET_STABLE;ACCURACY_OVER_CONFIRMED;ACCURACY_MODEL_PROB_HIGH;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| BOTH | 1545418 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | 2 | 2 | OVER_2_5 | OVER_2_5 | 0.7903 | 0.7967 | 0.807425 | 0.813825 | 133.361 | 134.423 | ACCURACY_CORE | ACCURACY_CORE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | ACCURACY_CORE_PRIORITY;ACCURACY_OVER_CONFIRMED;ACCURACY_FAILURE_MODE_ACCEPTABLE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

### Candidate v4
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1494179 | IFK Goteborg vs Mjallby AIF | Allsvenskan | 1 | 1 | 2 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1545418 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | 2 | 2 | 1 | OVER_2_5 | OVER_2_5 | OVER_1_5 | OVER_2_5 | DEGRADE_TO_OVER_1_5 | 8.5 | MARKET_DOWNGRADED_TO_OVER_1_5 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

### Candidate v5
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v5_rank | baseline_market | candidate_v2_market | candidate_v5_market | candidate_v5_original_market | candidate_v5_action | candidate_v5_hint | baseline_primary_risk | candidate_v2_primary_risk | candidate_v5_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1494179 | IFK Goteborg vs Mjallby AIF | Allsvenskan | 1 | 1 | 1 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V5 | 1545418 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | 2 | 2 | 2 | OVER_2_5 | OVER_2_5 | OVER_2_5 | OVER_2_5 | NOT_APPLIED | PLAYER_IMPACT_NEUTRAL_NO_RELIABLE_COVERAGE | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

### Candidate v6
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v6_rank | baseline_market | candidate_v2_market | candidate_v6_market | candidate_v6_action | candidate_v6_alignment | candidate_v6_confidence_adjustment | baseline_primary_risk | candidate_v2_primary_risk | candidate_v6_primary_risk | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2+CANDIDATE_V6 | 1494179 | IFK Goteborg vs Mjallby AIF | Allsvenskan | 1 | 1 | 1.0 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | NEUTRAL | 0.0 | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| BASELINE+CANDIDATE_V2 | 1545418 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | 2 | 2 |  | OVER_2_5 | OVER_2_5 |  |  |  |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |  | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

### Candidate v7
| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v7_rank | baseline_market | candidate_v2_market | candidate_v7_market | candidate_v7_decision | candidate_v7_required_edge | candidate_v7_actual_edge | candidate_v7_drift_status | candidate_v7_clv_direction | candidate_v7_execution_status | target_date | generated_at | pipeline_mode | candidate_version | source_file_date_check | run_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2 | 1494179 | IFK Goteborg vs Mjallby AIF | Allsvenskan | 1 | 1 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  |  |  | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |
| BASELINE+CANDIDATE_V2+CANDIDATE_V7 | 1545418 | SC Paderborn 07 vs VfL Wolfsburg | Bundesliga | 2 | 2 | 1.0 | OVER_2_5 | OVER_2_5 | OVER_2_5 | PRICE_OK | 0.155 | 0.270384 | NO_DRIFT | CLV_UNAVAILABLE | PRICE_OK | 2026-05-25 | 2026-05-24T23:47:28+00:00 | PRE | COMPARISON | NO_DATE_COLUMN | 2026-05-25-20260524T234728Z |

## Price Discipline / CLV / Drift Execution Guard
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | price_discipline_min_edge_required | price_discipline_actual_edge | price_discipline_edge_surplus | price_discipline_drift_status | candidate_v7_prelock_status | candidate_v7_execution_status | clv_direction | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRICE_THIN_SECONDARY_ONLY | 0.143 | 0.12482 | -0.01818 | WATCH_PATTERN | V7_WAITING_FOR_PRELOCK | V7_WAITING_FOR_PRELOCK | CLV_UNAVAILABLE | Actual edge 0.125 below required edge 0.143. |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRICE_OK | 0.155 | 0.270384 | 0.115384 | NO_DRIFT |  | PRICE_OK | CLV_UNAVAILABLE | Price cleared configured minimum edge and probability requirements. |

## Pre-Lock Execution Status
- Pre-lock data fresh: YES
- Stale pre-lock excluded: NO
- Execution allowed by v7: 1

### Official Baseline Picks
| fixture_id | league | home_team | away_team | market_primary | accuracy_mode_rank | competition_calibrated_prob |
| --- | --- | --- | --- | --- | --- | --- |
| 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | 1 | 0.81736 |
| 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | 2 | 0.807425 |

### Candidate v7 Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | price_discipline_decision | candidate_v7_prelock_status | candidate_v7_execution_status | candidate_v7_execution_allowed_flag | price_discipline_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRICE_THIN_SECONDARY_ONLY | V7_WAITING_FOR_PRELOCK | V7_WAITING_FOR_PRELOCK | 0 | Actual edge 0.125 below required edge 0.143. |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRICE_OK |  | PRICE_OK | 1 | Price cleared configured minimum edge and probability requirements. |

### Active Pre-Lock Decisions
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 1033.63 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 1123.64 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

### Stale Pre-Lock Warning
_No stale pre-lock rows excluded._

## Odds Snapshot / CLV Calibration
### CLV Summary
| fixture_id | home_team | away_team | market_primary | experiment_id | pre_price | prelock_price | close_proxy_price | clv_delta | clv_direction | result | profit_units |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1494178 | IF Elfsborg | BK Hacken | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.88 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.33 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | 1.33 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | OFFICIAL_BASELINE | 1.33 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1494669 | Ham-Kam | Lillestrom | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.71 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | 1.9 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | 1.9 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | 1.9 |  |  |  | CLV_UNAVAILABLE |  |  |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | OFFICIAL_BASELINE | 1.9 |  |  |  | CLV_UNAVAILABLE |  |  |

### Candidate v7 Calibration Advice
| market_family | failure_mode | drift_status | clv_direction | n | profit_units | roi_percent | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_UNAVAILABLE | 6 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_UNAVAILABLE | 4 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Post-Results Summary
_No rows._

## Pre-Lock Status
| fixture_id | home_team | away_team | market_primary | prelock_status | prelock_minutes_to_kickoff | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1494179 | IFK Goteborg | Mjallby AIF | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | 1033.63 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| 1545418 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | 1123.64 | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

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
- Official picks registered: 2
- Shadow picks registered: 8
- No-bet records: 1
- Ledger report: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_ledger_daily_report.md

## Daily Controller Status
- Next recommended action: CHECK_STALE_OUTPUTS
- Pre-lock due time: 2026-05-25T15:31:05.800000+00:00
- Status path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/daily_controller_status.md

## Daily Supervisor
- Supervisor latest status: SUPERVISOR_STATUS_NOT_AVAILABLE
- Last run mode/time: NOT_AVAILABLE / NOT_AVAILABLE
- Next recommended action: CHECK_STALE_OUTPUTS
- Scheduled automation status: REGISTRATION_SCRIPT_AVAILABLE_STATUS_NOT_QUERIED
- Logs path: C:\vsigma\automation_logs\supervisor
- Report path: NOT_AVAILABLE

## Healthcheck
- Global health status: WARNING
- Critical warnings: official_baseline_output: WARNING - only stale rows found for 2026-05-24
- Recovery command: `.\.venv\Scripts\python.exe scripts\run_daily_competition_controller.py --date 2026-05-25 --timezone Atlantic/Canary --mode pre`
- Report path: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_healthcheck_report.md

### Current Experiment Daily Summary
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_decision | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1494179.0 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1494179.0 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V3_ODDS_DEPTH |  |  |  |  |  |  |  | NO_BET_RECORD |
| CANDIDATE_V4_O25_FIREWALL | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 |  | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1494179.0 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1494179.0 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1494179.0 | IFK Goteborg | Mjallby AIF | OVER_1_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545418.0 | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | PRELOCK_NOT_AVAILABLE | PENDING |  | PRELOCK_UPDATED |

### Experiment Performance Summary
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 18 | 6 | 4 | 2 | -0.05 | -0.833333 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 21 | 5 | 3 | 2 | -0.57 | -11.4 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 19 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 21 | 5 | 3 | 2 | -0.57 | -11.4 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 18 | 5 | 3 | 2 | -0.57 | -11.4 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 10 | 0 | 0 | 0 | 0.0 |  | PRICE_DISCIPLINE_UNTESTED |

## Promotion & Threshold Governance
- Official baseline status: KEEP_OFFICIAL_BASELINE
- Governance dashboard: /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_governance_dashboard.md

### Candidate Promotion Recommendations
| experiment_id | settled_picks | roi_percent | brier_score | promotion_recommendation | required_next_evidence |
| --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 6 | -0.833333 | 0.255941 | KEEP_OFFICIAL_BASELINE | Continue accumulating official settled outcomes and compare challengers against it. |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 5 | -11.4 | 0.292445 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V3_ODDS_DEPTH | 0 |  |  | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V4_O25_FIREWALL | 4 | -26.25 | 0.352548 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V5_PLAYER_IMPACT | 5 | -11.4 | 0.292445 | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |
| CANDIDATE_V6_API_PREDICTIONS | 5 | -11.4 | 0.292445 | AUDIT_ONLY | Keep as an audit comparator unless registry governance explicitly changes its role. |
| CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL | Continue shadow tracking with immutable ledger outcomes. |

### Threshold Recommendations
| market_family | failure_mode | experiment_id | settled_rows | roi_percent | clv_direction | threshold_recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 6 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | 5 | -11.4 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | 5 | -11.4 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | 5 | -11.4 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | 5 | -11.4 |  | SAMPLE_TOO_SMALL |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | 4 | -26.25 |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | 4 | 0.0 | CLV_UNAVAILABLE | SAMPLE_TOO_SMALL |
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
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | 0 |  |  | SAMPLE_TOO_SMALL |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V7_PRICE_DISCIPLINE | 0 |  |  | SAMPLE_TOO_SMALL |

- CLV data sufficiency: INSUFFICIENT_CLV_DATA
- Drift alerts: 0

## Failure Mode Summary
| failure_mode | rows |
| --- | --- |
| FAILURE_MODE_LOW_CONVERSION | 10 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.125; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.270; market_fit=SAFE_OK | 4 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.133; market_fit=SAFE_OK | 1 |
| FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.264; market_fit=SAFE_OK | 1 |

## Freshness Validation
| file_name | candidate_version | status | detail | rows |
| --- | --- | --- | --- | --- |
| vsigma_today_competition_shortlist.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 2 |
| vsigma_today_competition_top.csv | OFFICIAL_BASELINE | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v2_competition_shortlist.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v2_competition_top.csv | CANDIDATE_V2 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v4_competition_shortlist.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v4_competition_top.csv | CANDIDATE_V4 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v5_competition_shortlist.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v5_competition_top.csv | CANDIDATE_V5 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v6_competition_shortlist.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v6_competition_top.csv | CANDIDATE_V6 | PASS | output is fresh for requested target date | 1 |
| vsigma_today_candidate_v7_competition_shortlist.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v7_competition_top.csv | CANDIDATE_V7 | PASS | output is fresh for requested target date | 1 |
| vsigma_today_baseline_vs_candidate_v2.csv | COMPARISON | PASS | output is fresh for requested target date | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v4.csv | COMPARISON | PASS | output is fresh for requested target date | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v5.csv | COMPARISON | PASS | output is fresh for requested target date | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v6.csv | COMPARISON | PASS | output is fresh for requested target date | 2 |
| vsigma_today_baseline_vs_candidate_v2_vs_candidate_v7.csv | COMPARISON | PASS | output is fresh for requested target date | 2 |
| vsigma_today_match_script_forecasts.csv | FORECAST | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v2_match_script_forecasts.csv | FORECAST_CANDIDATE_V2 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_candidate_v4_match_script_forecasts.csv | FORECAST_CANDIDATE_V4 | PASS | output is fresh for requested target date | 2 |
| vsigma_today_prelock_competition_top.csv | OFFICIAL_BASELINE_PRELOCK | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day | 0 |
| vsigma_today_prelock_comparison.csv | PRELOCK_COMPARISON | WARNING_STALE_GLOBAL_FILE | metadata target_date=['2026-05-24'] does not match 2026-05-25 | 3 |
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
| snapshot_contains_expected_file | vsigma_today_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v2_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_candidate_v2_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v4_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_candidate_v4_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v5_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_candidate_v5_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v6_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_candidate_v6_competition_top.csv |
| snapshot_contains_expected_file | vsigma_today_candidate_v7_competition_top.csv | PASS | /home/runner/work/vsigma/vsigma/data/processed/today/2026-05-25/vsigma_today_candidate_v7_competition_top.csv |

## Pre-Lock
PRE_LOCK_ACTIVE: pre-lock review writes separate PRELOCK outputs and never overwrites the frozen morning official baseline.
