# vSIGMA Immutable Ledger Daily Report - 2026-05-24

## Ledger Update Status
- Ledger CSV: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.csv
- JSONL event log: /home/runner/work/vsigma/vsigma/data/processed/ledger/vsigma_immutable_daily_pick_ledger.jsonl
- Official picks registered: 4
- Shadow picks registered: 11
- No-bet records: 1
- Pending records: 11
- Settled records: 4
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
| CANDIDATE_V2_SCHEDULE_ANOMALY | 3 | 3 | 0 | 2 | 1 | 0.48 |
| CANDIDATE_V3_ODDS_DEPTH | 1 | 0 | 1 | 0 | 0 | 0.0 |
| CANDIDATE_V4_O25_FIREWALL | 2 | 2 | 0 | 2 | 0 | 0.0 |
| CANDIDATE_V5_PLAYER_IMPACT | 3 | 3 | 0 | 2 | 1 | 0.48 |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 2 | 0 | 1 | 1 | 0.48 |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1 | 0 | 1 | 0 | 0.0 |
| OFFICIAL_BASELINE | 4 | 4 | 0 | 3 | 1 | 0.48 |

## Official Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1 | 1392207 | Sporting Gijon | Almeria | OVER_2_5 | 0.841525 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.191; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| OFFICIAL_BASELINE | 2 | 1545796 | Catanzaro | Monza | OVER_1_5 | 0.819 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.164; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| OFFICIAL_BASELINE | 3 | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.176; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| OFFICIAL_BASELINE | 3 | 1492276 | Remo | Atletico Paranaense | OVER_1_5 | 0.7612 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.117; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |

## Shadow Picks
| experiment_id | rank | fixture_id | home_team | away_team | market_primary | calibrated_probability | risk_tags | record_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1 | 1392205 | Huesca | Castellón | OVER_2_5 | 0.802125 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 2 | 1545796 | Catanzaro | Monza | OVER_1_5 | 0.8149 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.160; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1 | 1392205 | Huesca | Castellón | OVER_1_5 | 0.85236 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 2 | 1545796 | Catanzaro | Monza | OVER_1_5 | 0.8149 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.160; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1 | 1392205 | Huesca | Castellón | OVER_2_5 | 0.802125 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 2 | 1545796 | Catanzaro | Monza | OVER_1_5 | 0.8149 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.160; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1 | 1545796 | Catanzaro | Monza | OVER_1_5 | 0.8149 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.160; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1 | 1392205 | Huesca | Castellón | OVER_2_5 | 0.802125 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_2_5; edge=0.200; market_fit=SAFE_OK; LOW_CONVERSION | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 3 | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.176; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 3 | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.176; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 2 | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | 0.7719 | FAILURE_MODE_LOW_CONVERSION; FAILURE_MODE_LOW_CONVERSION; market=OVER_1_5; edge=0.176; market_fit=SAFE_OK; LOW_CONVERSION | SETTLED |

## No-Bet Modes
| experiment_id | record_status | reason_tags | source_file |
| --- | --- | --- | --- |
| CANDIDATE_V3_ODDS_DEPTH | NO_BET_RECORD | NO_BET; SOURCE_FILE_MISSING_OR_NOT_AVAILABLE | vsigma_today_candidate_v3_competition_top.csv |

## Pre-Lock Changes
| experiment_id | fixture_id | home_team | away_team | market_primary | prelock_status | prelock_decision | prelock_decision_reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207 | Sporting Gijon | Almeria | OVER_2_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V4_O25_FIREWALL | 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1545796 | Catanzaro | Monza | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| OFFICIAL_BASELINE | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V5_PLAYER_IMPACT | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |
| CANDIDATE_V6_API_PREDICTIONS | 1504827 | Tokyo Verdy | Yokohama F. Marinos | OVER_1_5 | OUTSIDE_PRELOCK_WINDOW | PRELOCK_NOT_AVAILABLE | fixture is outside requested pre-lock window |

## Result State
| experiment_id | fixture_id | market_primary | result_status | result | profit_units | record_status |
| --- | --- | --- | --- | --- | --- | --- |
| OFFICIAL_BASELINE | 1392207 | OVER_2_5 | PENDING | PENDING |  | PRE_REGISTERED |
| OFFICIAL_BASELINE | 1545796 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1392205 | OVER_2_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1545796 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1392205 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V4_O25_FIREWALL | 1545796 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1392205 | OVER_2_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V5_PLAYER_IMPACT | 1545796 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V6_API_PREDICTIONS | 1545796 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |
| CANDIDATE_V7_PRICE_DISCIPLINE | 1392205 | OVER_2_5 | PENDING | PENDING |  | PRE_REGISTERED |
| OFFICIAL_BASELINE | 1504827 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.48 | SETTLED |
| CANDIDATE_V2_SCHEDULE_ANOMALY | 1504827 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.48 | SETTLED |
| CANDIDATE_V5_PLAYER_IMPACT | 1504827 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.48 | SETTLED |
| CANDIDATE_V6_API_PREDICTIONS | 1504827 | OVER_1_5 | RESULT_AVAILABLE | WIN | 0.48 | SETTLED |
| OFFICIAL_BASELINE | 1492276 | OVER_1_5 | PENDING | PENDING |  | PRE_REGISTERED |

## Freshness Warnings
_No rows._
