# vSIGMA CLV Calibration Report

- Target date: 2026-05-21
- Rows: 27
- Date validation status: CLV_DATE_MISMATCH
- Date-mismatched rows excluded: 297
- Mismatched target dates observed: 2026-05-09, 2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20
- Missing PRE snapshot rows: 0
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Snapshot Provenance
| metric | rows |
| --- | --- |
| true_pre_rows | 27 |
| backfilled_rows | 0 |
| calibration_usable_rows | 10 |
| audit_only_rows | 17 |

## CLV Direction Mix
| clv_direction | rows |
| --- | --- |
| CLV_UNAVAILABLE | 17 |
| CLV_FLAT | 9 |
| CLV_POSITIVE | 1 |

## CLV Rows
| target_date | fixture_id | league | home_team | away_team | market_primary | experiment_id | source_candidate_version | pre_price | prelock_price | close_proxy_price | clv_delta | clv_percent | clv_direction | clv_interpretation | result | profit_units | snapshot_rebuild_mode | true_pre_snapshot_available_flag | clv_usable_for_threshold_calibration_flag | source_snapshot_stage | source_snapshot_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-05-21 | 1494228 | Allsvenskan | IF Elfsborg | Mjallby AIF | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.38 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535204 | CONMEBOL Sudamericana | Atletico-MG | Cienciano | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.62 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535204 | CONMEBOL Sudamericana | Atletico-MG | Cienciano | BTTS_YES | OFFICIAL_BASELINE | EXECUTION_SHORTLIST | 2.62 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.36 |  | 1.36 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7;CANDIDATE_V7_RESULTS | 1.36 |  | 1.36 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.36 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535208 | CONMEBOL Sudamericana | Gremio | Palestino | UNDER_3_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.36 | 1.36 | 1.36 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535209 | CONMEBOL Sudamericana | Independiente Petrolero | Botafogo | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 2.0 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535209 | CONMEBOL Sudamericana | Independiente Petrolero | Botafogo | BTTS_YES | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 2.0 |  | 2.0 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535213 | CONMEBOL Sudamericana | Puerto Cabello | Juventud | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.4 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535213 | CONMEBOL Sudamericana | Puerto Cabello | Juventud | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST | 1.4 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535215 | CONMEBOL Sudamericana | River Plate | RB Bragantino | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.5 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535301 | CONMEBOL Libertadores | Cusco | Independiente Medellin | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.95 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.42 |  | 1.42 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.42 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535302 | CONMEBOL Libertadores | Flamengo | Estudiantes L.P. | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.42 | 1.42 | 1.42 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE;PRELOCK | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535305 | CONMEBOL Libertadores | Junior | Sporting Cristal | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.34 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535306 | CONMEBOL Libertadores | Deportivo La Guaira | Independ. Rivadavia | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.69 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535306 | CONMEBOL Libertadores | Deportivo La Guaira | Independ. Rivadavia | OVER_1_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_RESULTS | 1.69 |  | 1.5 | -0.19 | 11.242604 | CLV_POSITIVE | Price shortened after PRE; vSIGMA beat the close proxy. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1535309 | CONMEBOL Libertadores | Palmeiras | Cerro Porteno | BTTS_YES | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 3.0 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545231 | Super League | Grasshoppers | FC Aarau | OVER_1_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.5 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | CANDIDATE_V2_SCHEDULE_ANOMALY | CANDIDATE_V2;CANDIDATE_V2_RESULTS | 1.88 |  | 1.88 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | CANDIDATE_V7_PRICE_DISCIPLINE | CANDIDATE_V7;CANDIDATE_V7_RESULTS | 1.88 |  | 1.88 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.88 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545410 | Superliga | Brondby | FC Copenhagen | OVER_2_5 | OFFICIAL_BASELINE | EXECUTION_SHORTLIST;OFFICIAL_BASELINE;OFFICIAL_BASELINE_PRELOCK;OFFICIAL_RESULTS | 1.88 |  | 1.88 | 0.0 | 0.0 | CLV_FLAT | Price movement was flat within tolerance. |  |  | CANONICAL_CAPTURED | 1 | 1 | CLOSE_PROXY;POST;PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545412 | Eredivisie | Utrecht | Heerenveen | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.66 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |
| 2026-05-21 | 1545417 | Bundesliga | VfL Wolfsburg | SC Paderborn 07 | OVER_2_5 | DEEP_ANALYSIS_CANDIDATES | DEEP_ANALYSIS_BET | 1.82 |  |  |  |  | CLV_UNAVAILABLE | CLV unavailable: missing close-proxy price. |  |  | CANONICAL_CAPTURED | 1 | 0 | PRE | Captured by odds snapshot pipeline. |

Interpretation note: close_proxy_price may come from CLOSE_PROXY, POST, or PRELOCK snapshots. It is not treated as true closing odds unless that data exists.
