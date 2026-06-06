# vSIGMA Candidate v7 Calibration Advisor

- Target date context: 2026-06-06
- Advisory only: this report never edits config/vsigma_price_discipline_config.json.
- CLV tracking status: CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING

## Recommendation Mix
| recommendation | rows |
| --- | --- |
| SAMPLE_TOO_SMALL | 1 |

## Advice
| market_family | failure_mode | drift_status | clv_direction | league | n | wins | losses | profit_units | roi_percent | avg_clv_delta | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_2_5 | LOW_CONVERSION | NO_DRIFT | CLV_UNAVAILABLE | ALL | 4 | 0 | 0 | 0.0 | 0.0 |  | SAMPLE_TOO_SMALL | Fewer than 10 settled rows; collect more snapshots before changing thresholds. |

## Date Validation

- LEDGER: CLV_DATE_MISMATCH; excluded_rows=162; mismatched_dates=2026-05-14, 2026-05-15, 2026-05-16, 2026-05-17, 2026-05-18, 2026-05-19, 2026-05-20, 2026-05-21, 2026-05-22, 2026-05-23, 2026-05-24, 2026-05-25, 2026-05-26, 2026-05-27, 2026-05-28, 2026-05-29, 2026-05-30, 2026-05-31
- CLV: PASS; excluded_rows=0; mismatched_dates=None
