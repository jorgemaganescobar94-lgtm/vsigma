# vSIGMA Manual Whitelist Review Board - 2026-06-17

## Summary
- review_rows: 1
- p1_review_rows: 1
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=1
- manual_decision_counts: NO_DECISION_REVIEW_ONLY=1
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=1
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=1
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=1
- scoring_permission_counts: NO_SCORING_PERMISSION=1
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=1
- pick_permission_counts: NO_PICK_PERMISSION=1
- stake_permission_counts: NO_STAKE_PERMISSION=1
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
- auto_apply: NO
- production_change: NO

## Review Rows
- #1 | Lake Macquarie vs West Wallsend | league=NNSW League 1 | country=Australia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This board is manual-review only.
- It does not whitelist sources, promote candidates, score fixtures, call APIs, create picks, or create stake permission.
- Every row remains NO_WHITELIST_PERMISSION, NO_CANONICAL_BOARD_PERMISSION, NO_SCORING_PERMISSION, NO_API_ENRICHMENT_PERMISSION, NO_PICK_PERMISSION and NO_STAKE_PERMISSION.
- Any future whitelist must be an explicit separate code change after sample validation.
