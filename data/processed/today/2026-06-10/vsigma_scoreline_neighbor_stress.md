# vSIGMA Scoreline Neighbor Stress - 2026-06-10

## Summary
- scoreline_rows: 6
- scoreline_data_status_counts: NO_SCORELINE_DATA=6
- scoreline_neighbor_bucket_counts: NO_SCORELINE=6
- scoreline_stress_status_counts: SCORELINE_DATA_MISSING=5; DIAGNOSTIC_NO_SCORELINE_STRESS=1
- scoreline_learning_label_counts: NO_SCORELINE_SIGNAL=5; DIAGNOSTIC_NOT_REAL_FIXTURE=1
- stress_evidence_level_counts: LOW=5; NONE=1
- manual_review_required_counts: NO=6
- auto_apply: NO
- production_change: NO

## Scoreline Rows
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- SCORELINE_DATA_MISSING | Las Palmas vs Malaga | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Almeria vs Castellón | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Almeria vs Castellón | score=NA bucket=NO_SCORELINE | market=TOTAL_GOALS outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Nautico Recife vs Fortaleza EC | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Ponte Preta vs Cuiaba | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA

## Guardrails
- This scoreline stress report is advisory only and never changes picks, stake, gates, or weights.
- Neighbor labels are review candidates, not automatic truth.
- Diagnostic and missing-scoreline rows must not train the model.
- No automatic market-family, live, or production changes are created here.
