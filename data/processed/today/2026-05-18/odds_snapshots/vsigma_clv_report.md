# vSIGMA CLV Calibration Report

- Target date: 2026-05-18
- Rows: 11
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 155
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 11 |
| backfilled_rows | 0 |
| calibration_usable_rows | 7 |
| audit_only_rows | 4 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 4 |
| CLV_FLAT | 4 |
| CLV_NEGATIVE | 2 |
| CLV_POSITIVE | 1 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-18 | 1392197 | Segunda División | Leganes | Huesca | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.32 |  | 1.33 | 0.01 | -0.757576 | CLV_NEGATIVE | Price drifted higher after PRE; market moved against vSIGMA. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1392197 | Segunda División | Leganes | Huesca | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.32 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1392197 | Segunda División | Leganes | Huesca | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.32 | 1.32 | 1.33 | 0.01 | -0.757576 | CLV_NEGATIVE | Price drifted higher after PRE; market moved against vSIGMA. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494170 | Allsvenskan | Djurgardens IF | Sirius | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.67 |  | 1.67 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494170 | Allsvenskan | Djurgardens IF | Sirius | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7;CANDIDATE_V7_RESULTS | 1.67 |  | 1.67 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494170 | Allsvenskan | Djurgardens IF | Sirius | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.67 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494170 | Allsvenskan | Djurgardens IF | Sirius | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.67 |  | 1.67 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494175 | Allsvenskan | Orgryte IS | IFK Goteborg | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.81 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1494175 | Allsvenskan | Orgryte IS | IFK Goteborg | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.81 |  | 1.81 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1545230 | Super League | FC Aarau | Grasshoppers | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.8 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-18 | 1545230 | Super League | FC Aarau | Grasshoppers | HOME_WIN | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 2.8 |  | 2.23 | -0.57 | 20.357143 | CLV_POSITIVE | Price shortened after PRE; vSIGMA beat the close proxy. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
