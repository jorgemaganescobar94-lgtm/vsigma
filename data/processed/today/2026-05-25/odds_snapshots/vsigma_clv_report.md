# vSIGMA CLV Calibration Report

- Target date: 2026-05-25
- Rows: 15
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 626
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 15 |
| backfilled_rows | 0 |
| calibration_usable_rows | 5 |
| audit_only_rows | 10 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 10 |
| CLV_FLAT | 5 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-25 | 1494178 | Allsvenskan | IF Elfsborg | BK Hacken | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.8 |  | 1.8 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494178 | Allsvenskan | IF Elfsborg | BK Hacken | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7;CANDIDATE_V7_RESULTS | 1.8 |  | 1.8 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494178 | Allsvenskan | IF Elfsborg | BK Hacken | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.8 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494178 | Allsvenskan | IF Elfsborg | BK Hacken | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.8 | 1.8 | 1.8 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.33 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.33 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494179 | Allsvenskan | IFK Goteborg | Mjallby AIF | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE | 1.33 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1494669 | Eliteserien | Ham-Kam | Lillestrom | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.7 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.35 |  | 1.35 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | WIN | 0.35 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.35 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.35 |  | 1.35 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | WIN | 0.35 | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.9 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7 | 1.9 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.9 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-25 | 1545418 | Bundesliga | SC Paderborn 07 | VfL Wolfsburg | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE | 1.9 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
