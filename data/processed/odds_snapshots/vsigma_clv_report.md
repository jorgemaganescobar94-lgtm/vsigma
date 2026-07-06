# vSIGMA CLV Calibration Report

- Target date: 2026-07-05
- Rows: 2
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 907
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-30, 2026-05-31, 2026-06-06, 2026-06-07, 2026-06-09, 2026-06-10, 2026-06-14, 2026-06-20, 2026-07-03, 2026-07-04
- Missing PRE snapshot rows: 2
- CLV tracking status: CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 0 |
| backfilled_rows | 0 |
| calibration_usable_rows | 0 |
| audit_only_rows | 2 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 2 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-07-05 | 1494195 | Allsvenskan | IF Elfsborg | Hammarby FF | OVER_2_5 | OFFICIAL_BASELINE | OFFICIAL_RESULTS |  |  | 1.75 |  |  | CLV_UNAVAILABLE | CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING | WIN | 0.75 | CANONICAL_CAPTURED | 0 | 0 | POST | Captured by odds snapshot pipeline. |
| 2026-07-05 | 1494199 | Allsvenskan | Kalmar FF | Orgryte IS | BTTS_YES | OFFICIAL_BASELINE | OFFICIAL_RESULTS |  |  | 1.8 |  |  | CLV_UNAVAILABLE | CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING | LOSS | -1.0 | CANONICAL_CAPTURED | 0 | 0 | POST | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
