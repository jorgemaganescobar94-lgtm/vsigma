# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 11 | 10 | 1 | 19 | 7 | 4 | 3 | 0 | 0 | 57.142857 | -1.18 | -16.857143 | 0.807941 | 0.311373 | -0.65 | OVER_1_5:15; OVER_2_5:3; UNDER_3_5:1 | FAILURE_MODE_LOW_CONVERSION:36; market_fit=SAFE_OK:19; LOW_CONVERSION:18; market=OVER_1_5:15; market=OVER_2_5:3; edge=0.202:2; FAILURE_MODE_AVALANCHE_RISK:2; edge=0.136:1; edge=0.141:1; edge=0.240:1; edge=0.123:1; edge=0.188:1; edge=0.167:1; edge=0.126:1; edge=0.259:1; edge=0.160:1; edge=0.170:1; edge=0.182:1; edge=0.249:1; market=UNDER_3_5:1; edge=0.116:1; AVALANCHE_RISK:1; edge=0.191:1; edge=0.220:1; edge=0.151:1; edge=0.189:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 15 | 13 | 2 | 23 | 6 | 3 | 3 | 0 | 0 | 50.0 | -1.7 | -28.333333 | 0.80837 | 0.347087 | -1.1 | OVER_1_5:20; OVER_2_5:3 | FAILURE_MODE_LOW_CONVERSION:34; market_fit=SAFE_OK:17; LOW_CONVERSION:17; market=OVER_1_5:15; market=OVER_2_5:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.147:1; edge=0.186:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 16 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 15 | 13 | 2 | 22 | 6 | 4 | 2 | 0 | 0 | 66.666667 | -0.45 | -7.5 | 0.807981 | 0.24192 | -0.45 | OVER_1_5:22 | FAILURE_MODE_LOW_CONVERSION:32; market_fit=SAFE_OK:16; LOW_CONVERSION:16; market=OVER_1_5:15; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; market=OVER_2_5:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.147:1; edge=0.186:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 15 | 13 | 2 | 23 | 6 | 4 | 2 | 0 | 0 | 66.666667 | -0.45 | -7.5 | 0.807958 | 0.245579 | -0.45 | OVER_1_5:21; OVER_2_5:2 | FAILURE_MODE_LOW_CONVERSION:34; market_fit=SAFE_OK:17; LOW_CONVERSION:17; market=OVER_1_5:15; market=OVER_2_5:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.147:1; edge=0.186:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 15 | 13 | 2 | 21 | 5 | 3 | 2 | 0 | 0 | 60.0 | -0.7 | -14.0 | 0.808798 | 0.286085 | -0.45 | OVER_1_5:20; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:32; market_fit=SAFE_OK:16; LOW_CONVERSION:16; market=OVER_1_5:15; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.196:1; edge=0.219:1; edge=0.147:1; edge=0.186:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 12 | 9 | 4 | 13 | 1 | 0 | 1 | 0 | 0 | 0.0 | -1.0 | -100.0 | 0.808546 | 0.652097 | 0.0 | OVER_1_5:10; OVER_2_5:3 | FAILURE_MODE_LOW_CONVERSION:24; market_fit=SAFE_OK:12; LOW_CONVERSION:12; market=OVER_1_5:10; market=OVER_2_5:2; edge=0.201:1; edge=0.222:1; edge=0.190:1; edge=0.169:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.147:1; edge=0.186:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 19 | 7 | 4 | 3 | -1.18 | -16.857143 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 23 | 6 | 3 | 3 | -1.7 | -28.333333 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 22 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 23 | 6 | 4 | 2 | -0.45 | -7.5 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 21 | 5 | 3 | 2 | -0.7 | -14.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 13 | 1 | 0 | 1 | -1.0 | -100.0 | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
