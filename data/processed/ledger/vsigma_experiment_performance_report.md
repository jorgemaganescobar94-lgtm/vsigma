# vSIGMA Experiment Performance Report

- Generated for ledger: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- Registry: /home/runner/work/vsigma/vsigma/config/vsigma_experiment_registry.json

## Official Baseline
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | vSIGMA Competition Accuracy Mode + Probability Calibration | OFFICIAL | official_selector | True | 4 | 4 | 0 | 8 | 5 | 3 | 2 | 0 | 0 | 60.0 | -0.53 | -10.6 | 0.798793 | 0.296723 | 0.0 | OVER_1_5:7; OVER_2_5:1 | FAILURE_MODE_LOW_CONVERSION:16; market_fit=SAFE_OK:8; LOW_CONVERSION:8; market=OVER_1_5:7; edge=0.202:2; edge=0.136:1; edge=0.141:1; edge=0.240:1; market=OVER_2_5:1; edge=0.123:1; edge=0.188:1; edge=0.167:1 | FROZEN_OFFICIAL_BASELINE |

## Shadow / Audit Experiments
| experiment_id | display_name | status | selection_role | allowed_to_select_officially | total_days_observed | pick_days | no_bet_days | picks_total | settled_picks | wins | losses | pushes | voids | hit_rate | profit_units | roi_percent | average_calibrated_probability | brier_score | max_drawdown | market_mix | failure_mode_mix | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | Candidate v2 Schedule Strength + Anomaly Cleaning | SHADOW | shadow_selector | False | 4 | 4 | 0 | 7 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.79734 | 0.352548 | -0.45 | OVER_1_5:7 | FAILURE_MODE_LOW_CONVERSION:14; market=OVER_1_5:7; market_fit=SAFE_OK:7; LOW_CONVERSION:7; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | Candidate v3 Odds Structure Depth | NOT_PROMOTED | audit_layer | False | 4 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  |  |  | 0.0 |  |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | Candidate v4 O2.5 Low Conversion Firewall | SHADOW | shadow_selector | False | 4 | 4 | 0 | 7 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.79734 | 0.352548 | -0.45 | OVER_1_5:7 | FAILURE_MODE_LOW_CONVERSION:14; market=OVER_1_5:7; market_fit=SAFE_OK:7; LOW_CONVERSION:7; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | Candidate v5 Player Impact Layer | SHADOW | shadow_selector | False | 4 | 4 | 0 | 7 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.79734 | 0.352548 | -0.45 | OVER_1_5:7 | FAILURE_MODE_LOW_CONVERSION:14; market=OVER_1_5:7; market_fit=SAFE_OK:7; LOW_CONVERSION:7; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | Candidate v6 API Predictions Benchmark | AUDIT_ONLY | audit_layer | False | 4 | 4 | 0 | 7 | 4 | 2 | 2 | 0 | 0 | 50.0 | -1.05 | -26.25 | 0.79734 | 0.352548 | -0.45 | OVER_1_5:7 | FAILURE_MODE_LOW_CONVERSION:14; market=OVER_1_5:7; market_fit=SAFE_OK:7; LOW_CONVERSION:7; edge=0.135:1; edge=0.136:1; edge=0.201:1; edge=0.222:1; edge=0.199:1; edge=0.190:1; edge=0.169:1 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | Candidate v7 Price Discipline + CLV + Drift Execution Guard | SHADOW | shadow_selector | False | 4 | 3 | 1 | 4 | 0 | 0 | 0 | 0 | 0 |  | 0.0 |  | 0.80384 |  | 0.0 | OVER_1_5:4 | FAILURE_MODE_LOW_CONVERSION:8; market=OVER_1_5:4; market_fit=SAFE_OK:4; LOW_CONVERSION:4; edge=0.201:1; edge=0.222:1; edge=0.190:1; edge=0.169:1 | PRICE_DISCIPLINE_UNTESTED |

## Official vs Shadow Comparison
| experiment_id | status | picks_total | settled_picks | wins | losses | profit_units | roi_percent | current_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | 8 | 5 | 3 | 2 | -0.53 | -10.6 | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | 7 | 4 | 2 | 2 | -1.05 | -26.25 | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | 0 | 0 | 0 | 0 | 0.0 |  | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | 7 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | 7 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | 7 | 4 | 2 | 2 | -1.05 | -26.25 | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | 4 | 0 | 0 | 0 | 0.0 |  | PRICE_DISCIPLINE_UNTESTED |

Interpretation note: registry and ledger reporting never promote a candidate and never changes official selection logic.
