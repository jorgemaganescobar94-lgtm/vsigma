# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 5 | 5 | 0 | 10 | 5 | 3 | 2 | 0 | 0 | 60.0 | -0.53 | -10.6 | 0.808083 | 0.296723 | 0.0 | OVER_1_5:8; OVER_2_5:2 | FAILURE_MODE_LOW_CONVERSION:20; market_fit=SAFE_OK:10; LOW_CONVERSION:10; market=OVER_1_5:8; edge=0.202:2; market=OVER_2_5:2; edge=0.136:1; edge=0.141:1; edge=0.240:1; edge=0.123:1; edge=0.188:1; edge=0.167:1; edge=0.126:1; edge=0.259:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 5 | 5 | 0 | 9 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.806574 | 0.352548 | -0.45 | OVER_1_5:8; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:18; market_fit=SAFE_OK:9; LOW_CONVERSION:9; market=OVER_1_5:8; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 5 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 5 | 5 | 0 | 8 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.799667 | 0.352548 | -0.45 | OVER_1_5:8 | FAILURE_MODE_LOW_CONVERSION:16; market=OVER_1_5:8; market_fit=SAFE_OK:8; LOW_CONVERSION:8; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 5 | 5 | 0 | 9 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.806574 | 0.352548 | -0.45 | OVER_1_5:8; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:18; market_fit=SAFE_OK:9; LOW_CONVERSION:9; market=OVER_1_5:8; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 5 | 5 | 0 | 9 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.807241 | 0.352548 | -0.45 | OVER_1_5:8; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:18; market_fit=SAFE_OK:9; LOW_CONVERSION:9; market=OVER_1_5:8; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 5 | 4 | 2 | 5 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  | 0.815437 |  | 0.0 | OVER_1_5:4; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:10; market_fit=SAFE_OK:5; LOW_CONVERSION:5; market=OVER_1_5:4; edge=0.201:1; edge=0.222:1; edge=0.190:1; edge=0.169:1; market=OVER_2_5:1; edge=0.246:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 10 | 5 | 3 | 2 | -0.53 | -10.6 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 9 | 4 | 2 | 2 | -1.05 | -26.25 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 8 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 9 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 9 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 5 | 0 | 0 | 0 | 0.0 |  | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
