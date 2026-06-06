# vSIGMA Scoreline Neighbor Stress - 2026-06-06

## Summary
- scoreline_rows: 2
- scoreline_data_status_counts: NO_SCORELINE_DATA=2
- scoreline_neighbor_bucket_counts: NO_SCORELINE=2
- scoreline_stress_status_counts: DIAGNOSTIC_NO_SCORELINE_STRESS=2
- scoreline_learning_label_counts: DIAGNOSTIC_NOT_REAL_FIXTURE=2
- stress_evidence_level_counts: NONE=2
- manual_review_required_counts: NO=2
- auto_apply: NO
- production_change: NO

## Scoreline Rows
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE

## Guardrails
- This scoreline stress report is advisory only and never changes picks, stake, gates, or weights.
- Neighbor labels are review candidates, not automatic truth.
- Diagnostic and missing-scoreline rows must not train the model.
- No automatic market-family, live, or production changes are created here.
