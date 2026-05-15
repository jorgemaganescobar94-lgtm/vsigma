# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 2 | 2 | 0 | 3 | 2 | 1 | 1 | 0 | 0 | 50.0 | -0.6 | -30.0 | 0.794373 | 0.363646 | 0.0 | OVER_1_5:3 | FAILURE_MODE_LOW_CONVERSION:6; market=OVER_1_5:3; market_fit=SAFE_OK:3; LOW_CONVERSION:3; edge=0.136:1; edge=0.141:1; edge=0.202:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 2 | 2 | 0 | 3 | 2 | 1 | 1 | 0 | 0 | 50.0 | -0.6 | -30.0 | 0.79626 | 0.36037 | 0.0 | OVER_1_5:3 | FAILURE_MODE_LOW_CONVERSION:6; market=OVER_1_5:3; market_fit=SAFE_OK:3; LOW_CONVERSION:3; edge=0.135:1; edge=0.136:1; edge=0.201:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 2 | 2 | 0 | 3 | 2 | 1 | 1 | 0 | 0 | 50.0 | -0.6 | -30.0 | 0.79626 | 0.36037 | 0.0 | OVER_1_5:3 | FAILURE_MODE_LOW_CONVERSION:6; market=OVER_1_5:3; market_fit=SAFE_OK:3; LOW_CONVERSION:3; edge=0.135:1; edge=0.136:1; edge=0.201:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 2 | 2 | 0 | 3 | 2 | 1 | 1 | 0 | 0 | 50.0 | -0.6 | -30.0 | 0.79626 | 0.36037 | 0.0 | OVER_1_5:3 | FAILURE_MODE_LOW_CONVERSION:6; market=OVER_1_5:3; market_fit=SAFE_OK:3; LOW_CONVERSION:3; edge=0.135:1; edge=0.136:1; edge=0.201:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 2 | 2 | 0 | 3 | 2 | 1 | 1 | 0 | 0 | 50.0 | -0.6 | -30.0 | 0.79626 | 0.36037 | 0.0 | OVER_1_5:3 | FAILURE_MODE_LOW_CONVERSION:6; market=OVER_1_5:3; market_fit=SAFE_OK:3; LOW_CONVERSION:3; edge=0.135:1; edge=0.136:1; edge=0.201:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 2 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  | 0.78646 |  | 0.0 | OVER_1_5:1 | FAILURE_MODE_LOW_CONVERSION:2; market=OVER_1_5:1; edge=0.201:1; market_fit=SAFE_OK:1; LOW_CONVERSION:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 3 | 2 | 1 | 1 | -0.6 | -30.0 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 3 | 2 | 1 | 1 | -0.6 | -30.0 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 3 | 2 | 1 | 1 | -0.6 | -30.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 3 | 2 | 1 | 1 | -0.6 | -30.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 3 | 2 | 1 | 1 | -0.6 | -30.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 1 | 0 | 0 | 0 | 0.0 |  | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
