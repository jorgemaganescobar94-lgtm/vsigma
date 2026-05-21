# vSIGMA CLV Calibration Report

- Target date: 2026-05-20
- Rows: 19
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 344
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-21
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 19 |
| backfilled_rows | 0 |
| calibration_usable_rows | 8 |
| audit_only_rows | 11 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 11 |
| CLV_FLAT | 6 |
| CLV_NEGATIVE | 2 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-20 | 1494229 | Allsvenskan | Gais | Hammarby FF | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.86 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1494229 | Allsvenskan | Gais | Hammarby FF | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.86 |  | 1.86 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535203 | CONMEBOL Sudamericana | America de Cali | Tigre | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.53 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535212 | CONMEBOL Sudamericana | Olimpia | Vasco DA Gama | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.47 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535299 | CONMEBOL Libertadores | Boca Juniors | Cruzeiro | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.57 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535304 | CONMEBOL Libertadores | Independiente del Valle | Libertad Asuncion | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.02 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535304 | CONMEBOL Libertadores | Independiente del Valle | Libertad Asuncion | BTTS_YES | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 2.02 |  | 2.02 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535308 | CONMEBOL Libertadores | Club Nacional | Universitario | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.4 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535308 | CONMEBOL Libertadores | Club Nacional | Universitario | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.4 |  | 1.4 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. | LOSS | -1.0 | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.6 |  | 1.6 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.6 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1535312 | CONMEBOL Libertadores | Santa Fe | Platense | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.6 | 1.6 | 1.6 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.35 |  | 1.38 | 0.03 | -2.222222 | CLV_NEGATIVE | Price drifted higher after PRE; market moved against vSIGMA. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.35 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1544596 | UEFA Europa League | SC Freiburg | Aston Villa | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.35 | 1.35 | 1.38 | 0.03 | -2.222222 | CLV_NEGATIVE | Price drifted higher after PRE; market moved against vSIGMA. | WIN | 0.35 | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1544952 | Serie B | Palermo | Catanzaro | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.75 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1544952 | Serie B | Palermo | Catanzaro | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.75 |  | 1.75 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1545403 | Primeira Liga | Torreense | Casa Pia | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.5 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-20 | 1545424 | Eerste Divisie | Willem II | FC Volendam | HOME_WIN | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.2 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
