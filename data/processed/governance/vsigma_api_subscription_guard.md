# vSIGMA API Subscription Guard - 2026-06-10

## Summary
- api_status: OK
- subscription_plan: UNKNOWN
- subscription_active: NO
- subscription_end: 
- requests_current: 0
- requests_limit_day: 0
- requests_remaining: 0
- api_calls_allowed: NO
- executor_mode: SKIP_API_EXECUTION
- recommended_executor_limit: 0
- guard_reason: subscription not active
- auto_apply: NO
- production_change: NO

## Guardrails
- This guard never creates picks, stake, or market recommendations.
- Free/Pro execution is capped to avoid exhausting daily quota.
- Expired, forbidden, missing-key, or low-remaining quota states skip real API execution.
- Account personal details from the API status response are intentionally not written.

