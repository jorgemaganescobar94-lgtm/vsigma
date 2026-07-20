# vSIGMA CLV Calibration Report

- Target date: 2026-07-19
- Rows: 7
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 954
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-30, 2026-05-31, 2026-06-06, 2026-06-07, 2026-06-09, 2026-06-10, 2026-06-14, 2026-06-20, 2026-07-03, 2026-07-04, 2026-07-05, 2026-07-06, 2026-07-07, 2026-07-08, 2026-07-11, 2026-07-14, 2026-07-15
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 7 |
| backfilled_rows | 0 |
| calibration_usable_rows | 3 |
| audit_only_rows | 4 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 4 |
| CLV_FLAT | 3 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-19 | 1494210 | Allsvenskan | IF Elfsborg | Sirius | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.62 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1494212 | Allsvenskan | Halmstad | BK Hacken | AWAY_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.6 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1494212 | Allsvenskan | Halmstad | BK Hacken | AWAY_WIN | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.6 |  | 1.6 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | WIN | 0.6 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1494213 | Allsvenskan | Hammarby FF | Degerfors IF | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.05 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1494213 | Allsvenskan | Hammarby FF | Degerfors IF | BTTS_YES | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 2.05 |  | 2.05 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1507002 | K League 1 | FC Anyang | Gwangju FC | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.65 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-07-19 | 1507002 | K League 1 | FC Anyang | Gwangju FC | HOME_WIN | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.65 |  | 1.65 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
