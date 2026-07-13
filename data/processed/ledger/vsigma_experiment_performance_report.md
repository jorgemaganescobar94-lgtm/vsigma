# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 36 | 13 | 23 | 23 | 10 | 7 | 3 | 0 | 0 | 70.0 | 0.61 | 6.1 | 0.809617 | 0.230559 | -0.65 | OVER_1_5:15; OVER_2_5:7; UNDER_3_5:1 | FAILURE_MODE_LOW_CONVERSION:44; market_fit=SAFE_OK:23; LOW_CONVERSION:22; market=OVER_1_5:15; market=OVER_2_5:7; edge=0.202:2; edge=0.167:2; FAILURE_MODE_AVALANCHE_RISK:2; edge=0.136:1; edge=0.141:1; edge=0.240:1; edge=0.123:1; edge=0.188:1; edge=0.126:1; edge=0.259:1; edge=0.160:1; edge=0.170:1; edge=0.182:1; edge=0.249:1; market=UNDER_3_5:1; edge=0.116:1; AVALANCHE_RISK:1; edge=0.191:1; edge=0.220:1; edge=0.131:1; edge=0.211:1; edge=0.254:1; edge=0.225:1; edge=0.207:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 43 | 19 | 24 | 31 | 9 | 6 | 3 | 0 | 0 | 66.666667 | 0.09 | 1.0 | 0.808014 | 0.246588 | -1.1 | OVER_1_5:24; OVER_2_5:7 | FAILURE_MODE_LOW_CONVERSION:42; market_fit=SAFE_OK:21; LOW_CONVERSION:21; market=OVER_1_5:15; market=OVER_2_5:6; edge=0.246:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.134:1; edge=0.207:1; edge=0.163:1; edge=0.209:1; edge=0.184:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 49 | 0 | 49 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 43 | 18 | 25 | 28 | 8 | 6 | 2 | 0 | 0 | 75.0 | 0.25 | 3.125 | 0.813593 | 0.193111 | -0.45 | OVER_1_5:28 | FAILURE_MODE_LOW_CONVERSION:36; market_fit=SAFE_OK:18; LOW_CONVERSION:18; market=OVER_1_5:14; market=OVER_2_5:4; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.134:1; edge=0.207:1; edge=0.246:1; edge=0.184:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 43 | 19 | 24 | 31 | 9 | 7 | 2 | 0 | 0 | 77.777778 | 1.34 | 14.888889 | 0.80768 | 0.178915 | -0.45 | OVER_1_5:25; OVER_2_5:6 | FAILURE_MODE_LOW_CONVERSION:42; market_fit=SAFE_OK:21; LOW_CONVERSION:21; market=OVER_1_5:15; market=OVER_2_5:6; edge=0.246:2; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.134:1; edge=0.207:1; edge=0.163:1; edge=0.209:1; edge=0.184:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 45 | 17 | 28 | 25 | 6 | 4 | 2 | 0 | 0 | 66.666667 | -0.18 | -3.0 | 0.803523 | 0.251104 | -0.45 | OVER_1_5:24; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:32; market_fit=SAFE_OK:16; LOW_CONVERSION:16; market=OVER_1_5:15; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1; edge=0.126:1; market=OVER_2_5:1; edge=0.246:1; edge=0.154:1; edge=0.173:1; edge=0.185:1; edge=0.196:1; edge=0.219:1; edge=0.134:1; edge=0.163:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 37 | 12 | 26 | 16 | 3 | 2 | 1 | 0 | 0 | 66.666667 | 0.27 | 9.0 | 0.808763 | 0.237555 | 0.0 | OVER_1_5:9; OVER_2_5:7 | FAILURE_MODE_LOW_CONVERSION:30; market_fit=SAFE_OK:15; LOW_CONVERSION:15; market=OVER_1_5:9; market=OVER_2_5:6; edge=0.246:2; edge=0.201:1; edge=0.222:1; edge=0.190:1; edge=0.169:1; edge=0.154:1; edge=0.173:1; edge=0.235:1; edge=0.196:1; edge=0.219:1; edge=0.134:1; edge=0.207:1; edge=0.209:1; edge=0.184:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 23 | 10 | 7 | 3 | 0.61 | 6.1 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 31 | 9 | 6 | 3 | 0.09 | 1.0 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 28 | 8 | 6 | 2 | 0.25 | 3.125 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 31 | 9 | 7 | 2 | 1.34 | 14.888889 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 25 | 6 | 4 | 2 | -0.18 | -3.0 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 16 | 3 | 2 | 1 | 0.27 | 9.0 | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
