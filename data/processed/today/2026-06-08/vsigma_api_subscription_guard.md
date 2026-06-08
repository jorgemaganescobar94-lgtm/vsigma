# vSIGMA API Subscription Guard - 2026-06-08

## Summary
- api_status: OK
- subscription_plan: Pro
- subscription_active: YES
- subscription_end: 2026-07-08T14:59:54+00:00
- requests_current: 656
- requests_limit_day: 7500
- requests_remaining: 6844
- api_calls_allowed: YES
- executor_mode: PRO_CONTROLLED_EXECUTION
- recommended_executor_limit: 250
- guard_reason: pro plan detected; limit executor to 250 fixtures
- auto_apply: NO
- production_change: NO

## Guardrails
- This guard never creates picks, stake, or market recommendations.
- Free/Pro execution is capped to avoid exhausting daily quota.
- Expired, forbidden, missing-key, or low-remaining quota states skip real API execution.
- Account personal details from the API status response are intentionally not written.

