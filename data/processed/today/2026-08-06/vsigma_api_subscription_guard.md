# vSIGMA API Subscription Guard - 2026-08-06

## Summary
- api_status: OK
- subscription_plan: Ultra
- subscription_active: YES
- subscription_end: 2026-08-09T18:41:36+00:00
- requests_current: 4
- requests_limit_day: 75000
- requests_remaining: 74996
- api_calls_allowed: YES
- executor_mode: MAX_COVERAGE_EXECUTION
- recommended_executor_limit: 0
- guard_reason: high-capacity plan detected; remaining=74996
- auto_apply: NO
- production_change: NO

## Guardrails
- This guard never creates picks, stake, or market recommendations.
- Free/Pro execution is capped to avoid exhausting daily quota.
- Expired, forbidden, missing-key, or low-remaining quota states skip real API execution.
- Account personal details from the API status response are intentionally not written.

