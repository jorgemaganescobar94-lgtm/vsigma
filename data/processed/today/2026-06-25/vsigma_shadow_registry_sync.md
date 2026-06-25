# vSIGMA Shadow Registry Sync - 2026-06-25

## Summary
- factory_rows: 2
- sync_status_counts: REGISTRY_CREATE_NEEDED=1; ALREADY_REGISTERED=1
- auto_apply: NO
- production_change: NO

## Registry Sync Rows
- #1 | REGISTRY_CREATE_NEEDED | pattern=WAITING_PRELOCK::OVER_1_5::FAILURE_MODE_LOW_CONVERSION::WAIT_FOR_POST_RESULTS | factory=CREATE_SHADOW_ONLY | registry=MISSING | next=CREATE_REGISTRY_ENTRY_REVIEW_ONLY
- #2 | ALREADY_REGISTERED | pattern=OVER_1_5::FAILURE_MODE_LOW_CONVERSION | factory=CONTINUE_SHADOW_ONLY | registry=ACTIVE_SHADOW_ONLY | next=CONTINUE_FORWARD_TEST

## Guardrails
- This report does not create or modify registry entries automatically.
- Registry changes require separate review.
- Production picks remain unchanged.
