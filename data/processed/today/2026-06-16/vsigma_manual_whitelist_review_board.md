# vSIGMA Manual Whitelist Review Board - 2026-06-16

## Summary
- review_rows: 5
- p1_review_rows: 5
- p2_review_rows: 0
- manual_review_status_counts: PENDING_OPERATOR_REVIEW=5
- manual_decision_counts: NO_DECISION_REVIEW_ONLY=5
- risk_label_counts: MEDIUM_REVIEW_POSSIBLE_WHITELIST=5
- whitelist_permission_counts: NO_WHITELIST_PERMISSION=5
- canonical_board_permission_counts: NO_CANONICAL_BOARD_PERMISSION=5
- scoring_permission_counts: NO_SCORING_PERMISSION=5
- api_enrichment_permission_counts: NO_API_ENRICHMENT_PERMISSION=5
- pick_permission_counts: NO_PICK_PERMISSION=5
- stake_permission_counts: NO_STAKE_PERMISSION=5
- next_action: Review rows manually. Any whitelist change must be a separate explicit code change after validation; this board cannot promote, score, enrich, pick, or stake.
- auto_apply: NO
- production_change: NO

## Review Rows
- #1 | Fortune vs Real de Banjul | league=GFA League | country=Gambia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #2 | GPA vs Team Rhino | league=GFA League | country=Gambia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #3 | Hart Acedemy vs Brikama United | league=GFA League | country=Gambia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #4 | Medina United vs Dutch Lions | league=GFA League | country=Gambia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- #5 | Samger vs Bombada | league=GFA League | country=Gambia | priority=P1_REVIEW_CANDIDATE | risk=MEDIUM_REVIEW_POSSIBLE_WHITELIST | whitelist=NO_WHITELIST_PERMISSION | canonical=NO_CANONICAL_BOARD_PERMISSION | scoring=NO_SCORING_PERMISSION | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This board is manual-review only.
- It does not whitelist sources, promote candidates, score fixtures, call APIs, create picks, or create stake permission.
- Every row remains NO_WHITELIST_PERMISSION, NO_CANONICAL_BOARD_PERMISSION, NO_SCORING_PERMISSION, NO_API_ENRICHMENT_PERMISSION, NO_PICK_PERMISSION and NO_STAKE_PERMISSION.
- Any future whitelist must be an explicit separate code change after sample validation.
