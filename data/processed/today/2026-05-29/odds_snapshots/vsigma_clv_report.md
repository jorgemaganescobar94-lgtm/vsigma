# vSIGMA CLV Calibration Report

- Target date: 2026-05-29
- Rows: 12
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 743
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 12 |
| backfilled_rows | 0 |
| calibration_usable_rows | 3 |
| audit_only_rows | 9 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 9 |
| CLV_FLAT | 3 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-29 | 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.45 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.45 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535218 | CONMEBOL Sudamericana | America de Cali | Macara | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK | 1.45 | 1.45 | 1.45 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.37 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535314 | CONMEBOL Libertadores | Boca Juniors | U. Catolica | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK | 1.37 | 1.37 | 1.37 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1535318 | CONMEBOL Libertadores | Cruzeiro | Barcelona SC | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.55 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2 | 1.52 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.52 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1545409 | Ligue 1 | Nice | Saint Etienne | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK | 1.52 | 1.52 | 1.52 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1545797 | Serie B | Monza | Catanzaro | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.83 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-29 | 1545797 | Serie B | Monza | Catanzaro | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST | 1.83 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
