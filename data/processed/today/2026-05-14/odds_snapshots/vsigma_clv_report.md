# vSIGMA CLV Calibration Report

- Target date: 2026-05-14
- Rows: 1
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 1
- Mismatched target dates observed: 2026-05-09
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 1 |
| backfilled_rows | 0 |
| calibration_usable_rows | 1 |
| audit_only_rows | 0 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_POSITIVE | 1 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-14 | 14 |  |  |  | OVER_1_5 | OFFICIAL_BASELINE |  | 1.4 |  | 1.35 | -0.05 | 3.571429 | CLV_POSITIVE | Price shortened after PRE; vSIGMA beat the close proxy. |  |  |  | 1 | 1 | CLOSE_PROXY;PRE |  |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
