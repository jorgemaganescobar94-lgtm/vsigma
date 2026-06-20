# vSIGMA Manual Whitelist Review Board - 2026-06-20

## Summary
- review_rows: 4
- p1_review_rows: 4
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=4
- manual_decision_counts: NO_DECISION_REVIEW_ONLY=4
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=4
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=4
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=4
- scoring_permission_counts: NO_SCORING_PERMISSION=4
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=4
- pick_permission_counts: NO_PICK_PERMISSION=4
- stake_permission_counts: NO_STAKE_PERMISSION=4
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
- auto_apply: NO
- production_change: NO

## Review Rows
- #1 | Cheongju Showking vs Yangcheon TNT | league=FA Cup | country=South-Korea | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #2 | Seogot vs Areum | league=FA Cup | country=South-Korea | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #3 | Yangsan United vs Anseong | league=FA Cup | country=South-Korea | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #4 | Yeonsu Songdo vs Ulsan FC | league=FA Cup | country=South-Korea | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This board is manual-review only.
- It does not whitelist sources, promote candidates, score fixtures, call APIs, create picks, or create stake permission.
- Every row remains NO_WHITELIST_PERMISSION, NO_CANONICAL_BOARD_PERMISSION, NO_SCORING_PERMISSION, NO_API_ENRICHMENT_PERMISSION, NO_PICK_PERMISSION and NO_STAKE_PERMISSION.
- Any future whitelist must be an explicit separate code change after sample validation.
