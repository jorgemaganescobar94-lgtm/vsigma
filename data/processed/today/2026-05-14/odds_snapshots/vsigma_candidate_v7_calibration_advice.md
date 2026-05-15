# vSIGMA Candidate v7 Calibration Advisor

- Target date context: 2026-05-14
- Advisory only: this report never edits config/vsigma_price_discipline_config.json.
- CLV tracking status: CLV_TRACKING_AVAILABLE_OR_NOT_REQUIRED

## Recommendation Mix
| recommendation | rows |
| --- | --- |
| RAISE_MIN_EDGE | 2 |

## Advice
| market_family | failure_mode | drift_status | clv_direction | league | n | wins | losses | profit_units | roi_percent | avg_clv_delta | recommendation | recommendation_reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_NEGATIVE | ALL | 11 | 0 | 11 | -11.0 | -100.0 | 0.05 | RAISE_MIN_EDGE | ROI is negative and CLV is negative; suggest stricter v7 edge requirement. |
| OVER_1_5 | LOW_CONVERSION | WATCH_PATTERN | CLV_NEGATIVE | League A | 11 | 0 | 11 | -11.0 | -100.0 | 0.05 | RAISE_MIN_EDGE | ROI is negative and CLV is negative; suggest stricter v7 edge requirement. |
