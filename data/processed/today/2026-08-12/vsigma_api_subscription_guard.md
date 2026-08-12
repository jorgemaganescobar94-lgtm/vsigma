# vSIGMA API Subscription Guard - 2026-08-12

## Summary
- api_status: OK
- subscription_plan: Free
- subscription_active: YES
- subscription_end: 2026-09-09T18:45:04+00:00
- requests_current: 1
- requests_limit_day: 100
- requests_remaining: 99
- api_calls_allowed: YES
- executor_mode: FREE_SAFE_EXECUTION
- recommended_executor_limit: 2
- guard_reason: free plan detected; limit executor to 2 fixtures
- auto_apply: NO
- production_change: NO

## Guardrails
- This guard never creates picks, stake, or market recommendations.
- Free/Pro execution is capped to avoid exhausting daily quota.
- Expired, forbidden, missing-key, or low-remaining quota states skip real API execution.
- Account personal details from the API status response are intentionally not written.

