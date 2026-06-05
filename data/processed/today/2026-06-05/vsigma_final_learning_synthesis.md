# vSIGMA Final Learning Synthesis - 2026-06-05

## Overall
- synthesis_status: SYNTHESIS_HOLD_SAMPLE
- synthesis_priority: LOW
- learning_permission: NO_LEARNING_SAMPLE_BLOCKED
- synthesis_note: No reviewable signal; one or more layers are blocked by sample.
- auto_apply: NO
- production_change: NO

## Summary
- layer_rows: 13
- synthesis_status_counts: DIAGNOSTIC_ONLY=10; HOLD_SAMPLE=3
- synthesis_priority_counts: NONE=10; LOW=3
- learning_permission_counts: NO_LEARNING_DIAGNOSTIC_ONLY=10; NO_LEARNING_SAMPLE_BLOCKED=3

## Layer Rows
- official_pick_ledger | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- postmatch_pick_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- pick_quality_classification | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- market_translation_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- no_bet_audit | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- market_family_calibration | rows=1 | diag=0 manual=0 sample_blocked=1 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- confidence_calibration | rows=1 | diag=0 manual=0 sample_blocked=1 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- source_reliability_learning | rows=15 | diag=0 manual=0 sample_blocked=15 pos=0 neg=0 | status=HOLD_SAMPLE | permission=NO_LEARNING_SAMPLE_BLOCKED
- league_competition_learning | rows=1 | diag=1 manual=0 sample_blocked=1 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- lineup_shock_learning | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- goal_timing_learning | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- scoreline_neighbor_stress | rows=1 | diag=1 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY
- portfolio_correlation_learning | rows=11 | diag=11 manual=0 sample_blocked=0 pos=0 neg=0 | status=DIAGNOSTIC_ONLY | permission=NO_LEARNING_DIAGNOSTIC_ONLY

## Guardrails
- This synthesis is advisory only and never changes model weights, gates, picks, stake, registry, or production.
- Diagnostic-only days are valid and must not train the model.
- Positive/negative/candidate signals require causal review before any future manual patch.
- auto_apply=NO and production_change=NO are hardcoded.
