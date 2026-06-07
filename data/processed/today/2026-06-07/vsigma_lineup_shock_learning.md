# vSIGMA Lineup Shock Learning - 2026-06-07

## Summary
- lineup_rows: 2
- lineup_data_status_counts: NO_LINEUP_DATA=2
- lineup_shock_status_counts: DIAGNOSTIC_NO_LINEUP_LEARNING=1; LINEUP_DATA_MISSING=1
- lineup_learning_label_counts: DIAGNOSTIC_NOT_REAL_FIXTURE=1; NO_LINEUP_SIGNAL=1
- shock_evidence_level_counts: NONE=1; LOW=1
- manual_review_required_counts: NO=2
- auto_apply: NO
- production_change: NO

## Lineup Shock Rows
- DIAGNOSTIC_NO_LINEUP_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | official=0 probable=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | evidence=NONE | manual=NO | action=NO_MODEL_CHANGE
- LINEUP_DATA_MISSING | Castellón vs Almeria | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA

## Guardrails
- This lineup shock report is advisory only and never changes prelock, picks, stake, or weights.
- Missing lineup data is not treated as source failure by itself.
- Red/green labels require causal review before any model lesson is accepted.
- No automatic lineup gate, source registry, or production changes are created here.
