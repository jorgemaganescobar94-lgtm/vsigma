# vSIGMA Immutable Ledger Daily Report - 2026-05-29

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 3
- Shadow picks registered: 15
- No-bet records: 1
- Pending records: 18
- Settled records: 0
- Daily winner: NO_SETTLED_RESULTS

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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 3 | 3 | 0 | 3 | 0 | 0.0 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 3 | 3 | 0 | 3 | 0 | 0.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 3 | 3 | 0 | 3 | 0 | 0.0 |
| CANDIDATE_V6_API_PREDICTIONS | 3 | 3 | 0 | 3 | 0 | 0.0 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 3 | 3 | 0 | 3 | 0 | 0.0 |
| OFFICIAL_BASELINE | 3 | 3 | 0 | 3 | 0 | 0.0 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.81316 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.151; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.799 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.189; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72086 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.131; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.80936 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.7961 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.186; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.80936 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.7961 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.186; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.80936 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.7961 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.186; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.80936 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.7961 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.186; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | 0.80936 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.147; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 2 | 1535218 | America de Cali | Macara | OVER_1_5 | 0.7961 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.186; market_fit=SAFE_OK; LOW_CONVERSION | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72396 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.134; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72396 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.134; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72396 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.134; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72396 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.134; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1545409 | Nice | Saint Etienne | OVER_1_5 | 0.72396 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.134; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| OFFICIAL_BASELINE | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V4_O25_FIREWALL | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V4_O25_FIREWALL | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V5_PLAYER_IMPACT | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V5_PLAYER_IMPACT | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V6_API_PREDICTIONS | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V6_API_PREDICTIONS | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535314 | Boca Juniors | U. Catolica | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535218 | America de Cali | Macara | OVER_1_5 | IN_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | no reliable pre-lock data available; missing data is neutral |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V4_O25_FIREWALL | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V5_PLAYER_IMPACT | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V6_API_PREDICTIONS | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535314 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1535218 | OVER_1_5 | PENDING | PENDING |  | PRELOCK_UPDATED |
| OFFICIAL_BASELINE | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1545409 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |

## Freshness Warnings
_No rows._
