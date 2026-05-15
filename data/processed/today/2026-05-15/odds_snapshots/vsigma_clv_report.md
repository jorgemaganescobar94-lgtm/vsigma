# vSIGMA CLV Calibration Report

- Target date: 2026-05-15
- Rows: 7
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 26
- Mismatched target dates observed: 2026-05-09, 2026-05-14
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 7 |
| backfilled_rows | 0 |
| calibration_usable_rows | 4 |
| audit_only_rows | 3 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_FLAT | 4 |
| CLV_UNAVAILABLE | 3 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-15 | 1379330 | Premier League | Aston Villa | Liverpool | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.81 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1379330 | Premier League | Aston Villa | Liverpool | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.81 |  | 1.81 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | PENDING |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1392200 | Segunda División | Cordoba | Albacete | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.61 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1392200 | Segunda División | Cordoba | Albacete | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.61 |  | 1.61 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | PENDING |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1544651 | Serie B | Bari | Sudtirol | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.53 |  | 1.53 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | PENDING |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1544651 | Serie B | Bari | Sudtirol | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.53 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-15 | 1544651 | Serie B | Bari | Sudtirol | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_RESULTS | 1.53 |  | 1.53 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | PENDING |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
