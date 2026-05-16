# vSIGMA Candidate v7 Calibration Advisor

- Target date context: 2026-05-16
- Advisory only: this report never edits config/vsigma_price_discipline_config.json.
- CLV tracking status: CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING

## Recommendation Mix
| recommendation | rows |
| --- | --- |
| INSUFFICIENT_CLV_DATA | 1 |

## Advice
| market_family | failure_mode | drift_status | clv_direction | league | n | wins | losses | profit_units | roi_percent | avg_clv_delta | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_UNAVAILABLE | ALL | 12 | 0 | 0 | 0.0 | 0.0 |  | INSUFFICIENT_CLV_DATA | CLV_TRACKING_INSUFFICIENT_TRUE_PRE_MISSING; do not change thresholds. |

## Date Validation

- LEDGER: CLV_DATE_MISMATCH; excluded_rows=19; mismatched_dates=2026-05-14, 2026-05-15
- CLV: PASS; excluded_rows=0; mismatched_dates=None
