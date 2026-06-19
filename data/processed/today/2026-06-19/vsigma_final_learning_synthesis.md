# vSIGMA Final Learning Synthesis - 2026-06-19

## Overall
- synthesis_status: SYNTHESIS_REVIEW_REQUIRED
- synthesis_priority: HIGH
- learning_permission: MANUAL_REVIEW_ONLY
- synthesis_note: At least one layer has reviewable learning signal; no automatic update is allowed.
- auto_apply: NO
- production_change: NO

## Summary
- layer_rows: 13
- synthesis_status_counts: DIAGNOSTIC_ONLY=6; HOLD_SAMPLE=4; NO_MODEL_CHANGE=2; MANUAL_REVIEW_REQUIRED=1
- synthesis_priority_counts: NONE=8; LOW=4; HIGH=1
- learning_permission_counts: NO_LEARNING_DIAGNOSTIC_ONLY=6; NO_LEARNING_SAMPLE_BLOCKED=4; NO_MODEL_CHANGE=2; MANUAL_REVIEW_ONLY=1

## Layer Rows
- official_pick_ledger | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- postmatch_pick_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- pick_quality_classification | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- market_translation_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- no_bet_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- market_family_calibration | rows=3 | diag=0 manual=0 sample_blocked=3 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- confidence_calibration | rows=1 | diag=0 manual=0 sample_blocked=1 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- source_reliability_learning | rows=15 | diag=0 manual=0 sample_blocked=15 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- league_competition_learning | rows=2 | diag=1 manual=0 sample_blocked=2 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- lineup_shock_learning | rows=12 | diag=2 manual=7 sample_blocked=0 pos=0 neg=0 | status=MANUAL_REVIEW_REQUIRED | permission=MANUAL_REVIEW_ONLY
- goal_timing_learning | rows=12 | diag=2 manual=0 sample_blocked=0 pos=0 neg=0 | status=NO_MODEL_CHANGE | permission=NO_MODEL_CHANGE
- scoreline_neighbor_stress | rows=12 | diag=2 manual=0 sample_blocked=0 pos=0 neg=0 | status=NO_MODEL_CHANGE | permission=NO_MODEL_CHANGE
- portfolio_correlation_learning | rows=12 | diag=12 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY

## Guardrails
- This synthesis is advisory only and never changes model weights, gates, picks, stake, registry, or production.
- Diagnostic-only days are valid and must not train the model.
- Positive/negative/candidate signals require causal review before any future manual patch.
- auto_apply=NO and production_change=NO are hardcoded.
