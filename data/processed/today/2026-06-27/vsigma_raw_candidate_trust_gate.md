# vSIGMA Raw Candidate Trust Gate - 2026-06-27

## Summary
- rows_reviewed: 0
- trusted_rows: 0
- quarantine_rows: 0
- blocked_rows: 0
- trust_status_counts: none
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.
- auto_apply: NO
- production_change: NO

## Rows
- none. No local raw fixture discovery candidates found.

## Guardrails
- Trust gate is defensive and can only restrict downstream use.
- Rejected source rows cannot feed scoring without explicit future whitelist.
- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.
- No bets, stakes, secrets, API calls, or safety gates are changed.
