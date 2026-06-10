# vSIGMA CLV Calibration Report

- Target date: 2026-06-10
- Rows: 3
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 852
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-30, 2026-05-31, 2026-06-06, 2026-06-07, 2026-06-09
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 3 |
| backfilled_rows | 0 |
| calibration_usable_rows | 0 |
| audit_only_rows | 3 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 3 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-06-10 | 1548055 | Segunda División | Malaga | Las Palmas | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-06-10 | 1548055 | Segunda División | Malaga | Las Palmas | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-06-10 | 1548055 | Segunda División | Malaga | Las Palmas | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
