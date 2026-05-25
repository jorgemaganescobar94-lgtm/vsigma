# vSIGMA Threshold Governance Report

This report recommends review actions only. It never edits threshold configuration.

- CLV sufficiency: CLV_DATA_SUFFICIENT_FOR_REVIEW: usable=12, available_direction_rows=12; advice remains reporting-only.

## Threshold Recommendations
| market_family | failure_mode | experiment_id | drift_status | clv_direction | settled_rows | hit_rate | profit_units | roi_percent | threshold_recommendation | threshold_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | WATCH_PATTERN | CLV_UNAVAILABLE | 6 | 100.0 | 0.96 | 16.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | WATCH_PATTERN |  | 4 | 50.0 | -1.05 | -26.25 | SAMPLE_TOO_SMALL | Only 4 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V4_O25_FIREWALL | WATCH_PATTERN |  | 4 | 50.0 | -1.05 | -26.25 | SAMPLE_TOO_SMALL | Only 4 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | WATCH_PATTERN |  | 4 | 50.0 | -1.05 | -26.25 | SAMPLE_TOO_SMALL | Only 4 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | WATCH_PATTERN |  | 4 | 50.0 | -1.05 | -26.25 | SAMPLE_TOO_SMALL | Only 4 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | OFFICIAL_BASELINE | WATCH_PATTERN |  | 4 | 50.0 | -1.05 | -26.25 | SAMPLE_TOO_SMALL | Only 4 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | WATCH_PATTERN | CLV_FLAT | 3 | 100.0 | 0.96 | 32.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | WATCH_PATTERN | CLV_POSITIVE | 2 |  | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | NO_DRIFT | CLV_FLAT | 2 |  | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | NO_DRIFT | CLV_POSITIVE | 1 |  | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | NO_DRIFT | CLV_UNAVAILABLE | 1 |  | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | OFFICIAL_BASELINE | NO_DRIFT |  | 1 | 100.0 | 0.52 | 52.0 | SAMPLE_TOO_SMALL | Only 1 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | WATCH_PATTERN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V4_O25_FIREWALL | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_1_5 | UNSPECIFIED | CANDIDATE_V6_API_PREDICTIONS | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V2_SCHEDULE_ANOMALY | NO_DRIFT |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V5_PLAYER_IMPACT | NO_DRIFT |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V6_API_PREDICTIONS | NO_DRIFT |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | LOW_CONVERSION | CANDIDATE_V7_PRICE_DISCIPLINE | NO_DRIFT |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V2_SCHEDULE_ANOMALY | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V5_PLAYER_IMPACT | UNKNOWN |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
| OVER_2_5 | UNSPECIFIED | CANDIDATE_V7_PRICE_DISCIPLINE | NO_DRIFT |  | 0 |  | 0.0 |  | SAMPLE_TOO_SMALL | Only 0 settled rows; minimum threshold-review sample is 10. |
