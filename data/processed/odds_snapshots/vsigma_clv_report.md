# vSIGMA CLV Calibration Report

- Target date: 2026-07-26
- Rows: 17
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 964
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-30, 2026-05-31, 2026-06-06, 2026-06-07, 2026-06-09, 2026-06-10, 2026-06-14, 2026-06-20, 2026-07-03, 2026-07-04, 2026-07-05, 2026-07-06, 2026-07-07, 2026-07-08, 2026-07-11, 2026-07-14, 2026-07-15, 2026-07-19
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 17 |
| backfilled_rows | 0 |
| calibration_usable_rows | 5 |
| audit_only_rows | 12 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 12 |
| CLV_FLAT | 5 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-26 | 1492303 | Serie A | Cruzeiro | Botafogo | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.87 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1492306 | Serie A | Palmeiras | Atletico-MG | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.7 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1492307 | Serie A | Remo | Vitoria | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1492307 | Serie A | Remo | Vitoria | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.37 |  | 1.37 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | WIN | 0.37 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.5 |  | 1.5 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.5 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494217 | Allsvenskan | IF Brommapojkarna | Hammarby FF | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_RESULTS | 1.5 |  | 1.5 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494222 | Allsvenskan | Malmo FF | IF Elfsborg | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.73 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494709 | Eliteserien | Aalesund | Viking | AWAY_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.54 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494709 | Eliteserien | Aalesund | Viking | AWAY_WIN | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.54 |  | 1.54 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494711 | Eliteserien | KFUM Oslo | Molde | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.72 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1494711 | Eliteserien | KFUM Oslo | Molde | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.72 |  | 1.72 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | WIN | 0.72 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1507015 | K League 1 | FC Seoul | Ulsan Hyundai FC | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.85 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1548976 | Superliga | Sonderjyske | FC Midtjylland | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.53 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1548979 | Superliga | FC Copenhagen | Lyngby | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.58 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1555351 | Super League | FC Lugano | FC Vaduz | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.67 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-26 | 1555352 | Super League | FC ST. Gallen | FC Zurich | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.45 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
