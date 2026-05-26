# vSIGMA Candidate v7 Calibration Advisor

- Target date context: 2026-05-25
- Advisory only: this report never edits config/vsigma_price_discipline_config.json.
- CLV tracking status: CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING

## Recommendation Mix
| recommendation | rows |
| --- | --- |
| SAMPLE_TOO_SMALL | 3 |

## Advice
| market_family | failure_mode | drift_status | clv_direction | league | n | wins | losses | profit_units | roi_percent | avg_clv_delta | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_FLAT | ALL | 2 | 0 | 0 | 0.0 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_UNAVAILABLE | ALL | 6 | 0 | 0 | 0.0 | 0.0 |  | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_FLAT | ALL | 3 | 0 | 0 | 0.0 | 0.0 | 0.0 | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Date Validation

- LEDGER: CLV_DATE_MISMATCH; excluded_rows=99; mismatched_dates=2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24
- CLV: PASS; excluded_rows=0; mismatched_dates=None
