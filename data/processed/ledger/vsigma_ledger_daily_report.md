# vSIGMA Immutable Ledger Daily Report - 2026-08-18

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 2
- Shadow picks registered: 8
- No-bet records: 1
- Pending records: 0
- Settled records: 10
- Daily winner: TIE

## Experiment Registry
| experiment_id | status | selection_role | allowed_to_select_officially | current_verdict |
| --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | OFFICIAL | official_selector | True | FROZEN_OFFICIAL_BASELINE |
| CANDIDATE_V2_SCHEDULE_ANOMALY | SHADOW | shadow_selector | False | MAIN_SHADOW_RETENDER_NOT_PROMOTED |
| CANDIDATE_V3_ODDS_DEPTH | NOT_PROMOTED | audit_layer | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V4_O25_FIREWALL | SHADOW | shadow_selector | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V5_PLAYER_IMPACT | SHADOW | shadow_selector | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V6_API_PREDICTIONS | AUDIT_ONLY | audit_layer | False | PARTIAL_NOT_PROMOTED |
| CANDIDATE_V7_PRICE_DISCIPLINE | SHADOW | shadow_selector | False | PRICE_DISCIPLINE_UNTESTED |

## Daily Summary By Experiment
| experiment_id | records | picks | no_bet_records | pending | settled | profit_units |
| --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 2 | 0 | 0 | 2 | 1.23 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1 | 0 | 0 | 1 | 0.57 |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 2 | 0 | 0 | 2 | 1.23 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 0 | 2 | 1.23 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1 | 0 | 0 | 1 | 0.66 |
| OFFICIAL_BASELINE | 2 | 2 | 0 | 0 | 2 | 1.23 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1547770 | Independ. Rivadavia | Fluminense | OVER_1_5 | 0.81096 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.242; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 2 | 1622620 | Dinamo Zagreb | Viking | OVER_2_5 | 0.879125 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.260; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1547770 | Independ. Rivadavia | Fluminense | OVER_1_5 | 0.80916 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1622620 | Dinamo Zagreb | Viking | OVER_2_5 | 0.863925 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.244; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1547770 | Independ. Rivadavia | Fluminense | OVER_1_5 | 0.80916 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1547770 | Independ. Rivadavia | Fluminense | OVER_1_5 | 0.80916 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1622620 | Dinamo Zagreb | Viking | OVER_2_5 | 0.863925 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.244; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1547770 | Independ. Rivadavia | Fluminense | OVER_1_5 | 0.80916 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.240; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1622620 | Dinamo Zagreb | Viking | OVER_2_5 | 0.863925 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.244; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1622620 | Dinamo Zagreb | Viking | OVER_2_5 | 0.863925 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.244; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
_No rows._

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1547770 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.57 | SETTLED |
| OFFICIAL_BASELINE | 1622620 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.66 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1547770 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.57 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1622620 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.66 | SETTLED |
| CANDIDATE_V4_O25_FIREWALL | 1547770 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.57 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1547770 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.57 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1622620 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.66 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1547770 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.57 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1622620 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.66 | SETTLED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1622620 | OVER_2_5 | RESULT_AVAILABLE | WIN | 0.66 | SETTLED |

## Freshness Warnings
| file_name | status | detail |
| --- | --- | --- |
| vsigma_today_prelock_competition_top.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| vsigma_today_prelock_comparison.csv | EMPTY_OK_NO_BET | empty output with headers is valid for a no-bet day |
| today_post_results_report.csv | WARNING_STALE_GLOBAL_FILE | snapshot context file not present yet |
