# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 10 | 9 | 1 | 17 | 7 | 4 | 3 | 0 | 0 | 57.142857 | -1.18 | -16.857143 | 0.80816 | 0.311373 | -0.65 | OVER_1_5:13; OVER_2_5:3; UNDER_3_5:1 | FAILURE_MODE_LOW_CONVERSION:32; market_fit=SAFE_OK:17; LOW_CONVERSION:16; market=OVER_1_5:13; market=OVER_2_5:3; edge=0.202:2; FAILURE_MODE_AVALANCHE_RISK:2; edge=0.136:1; edge=0.141:1; edge=0.240:1; edge=0.123:1; edge=0.188:1; edge=0.167:1; edge=0.126:1; edge=0.259:1; edge=0.160:1; edge=0.170:1; edge=0.182:1; edge=0.249:1; market=UNDER_3_5:1; edge=0.116:1; AVALANCHE_RISK:1; edge=0.191:1; edge=0.220:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 14 | 12 | 2 | 21 | 6 | 3 | 3 | 0 | 0 | 50.0 | -1.7 | -28.333333 | 0.809122 | 0.347087 | -1.1 | OVER_1_5:18; OVER_2_5:3 | FAILURE_MODE_LOW_CONVERSION:30; market_fit=SAFE_OK:15; LOW_CONVERSION:15; market=OVER_1_5:13; market=OVER_2_5:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 15 | 0 | 15 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 14 | 12 | 2 | 20 | 6 | 4 | 2 | 0 | 0 | 66.666667 | -0.45 | -7.5 | 0.808731 | 0.24192 | -0.45 | OVER_1_5:20 | FAILURE_MODE_LOW_CONVERSION:28; market_fit=SAFE_OK:14; LOW_CONVERSION:14; market=OVER_1_5:13; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; market=OVER_2_5:1; edge=0.235:1; edge=0.196:1; edge=0.219:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 14 | 12 | 2 | 21 | 6 | 4 | 2 | 0 | 0 | 66.666667 | -0.45 | -7.5 | 0.808655 | 0.245579 | -0.45 | OVER_1_5:19; OVER_2_5:2 | FAILURE_MODE_LOW_CONVERSION:30; market_fit=SAFE_OK:15; LOW_CONVERSION:15; market=OVER_1_5:13; market=OVER_2_5:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 14 | 12 | 2 | 19 | 5 | 3 | 2 | 0 | 0 | 60.0 | -0.7 | -14.0 | 0.809665 | 0.286085 | -0.45 | OVER_1_5:18; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:28; market_fit=SAFE_OK:14; LOW_CONVERSION:14; market=OVER_1_5:13; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.196:1; edge=0.219:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 11 | 8 | 4 | 11 | 1 | 0 | 1 | 0 | 0 | 0.0 | -1.0 | -100.0 | 0.809709 | 0.652097 | 0.0 | OVER_1_5:8; OVER_2_5:3 | FAILURE_MODE_LOW_CONVERSION:20; market_fit=SAFE_OK:10; LOW_CONVERSION:10; market=OVER_1_5:8; market=OVER_2_5:2; edge=0.201:1; edge=0.222:1; edge=0.190:1; edge=0.169:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.235:1; edge=0.196:1; edge=0.219:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 17 | 7 | 4 | 3 | -1.18 | -16.857143 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 21 | 6 | 3 | 3 | -1.7 | -28.333333 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 20 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 21 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 19 | 5 | 3 | 2 | -0.7 | -14.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 11 | 1 | 0 | 1 | -1.0 | -100.0 | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
