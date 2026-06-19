# vSIGMA Lineup Shock Learning - 2026-06-19

## Summary
- lineup_rows: 12
- lineup_data_status_counts: HAS_LINEUP_DATA=8; NO_LINEUP_DATA=4
- lineup_shock_status_counts: OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW=7; DIAGNOSTIC_NO_LINEUP_LEARNING=2; LINEUP_DATA_MISSING=2; OFFICIAL_LINEUP_AVAILABLE_NEUTRAL=1
- lineup_learning_label_counts: NO_BET_LINEUP_REVIEW=7; DIAGNOSTIC_NOT_REAL_FIXTURE=2; NO_LINEUP_SIGNAL=2; LINEUP_CONTEXT_PRESENT=1
- shock_evidence_level_counts: MEDIUM=7; LOW=3; NONE=2
- manual_review_required_counts: YES=7; NO=5
- auto_apply: NO
- production_change: NO

## Lineup Shock Rows
- DIAGNOSTIC_NO_LINEUP_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | official=0 probable=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | evidence=NONE | manual=NO | action=NO_MODEL_CHANGE
- LINEUP_DATA_MISSING | Las Palmas vs Malaga | official=0 probable=0 | outcome=NO_PICK | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Almeria vs Castellón | official=2 probable=0 | outcome=NO_PICK | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- OFFICIAL_LINEUP_AVAILABLE_NEUTRAL | Almeria vs Castellón | official=2 probable=0 | outcome=NO_PICK | label=LINEUP_CONTEXT_PRESENT | evidence=LOW | manual=NO | action=KEEP_COLLECTING_SAMPLE
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Nautico Recife vs Fortaleza EC | official=2 probable=0 | outcome=NO_PICK | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Ponte Preta vs Cuiaba | official=2 probable=0 | outcome=NO_PICK | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Malaga vs Las Palmas | official=2 probable=0 | outcome=PENDING | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Maringá vs Maranhão | official=2 probable=0 | outcome=PENDING | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- LINEUP_DATA_MISSING | TransINVEST Vilnius vs FK Trakai | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | Gnistan vs Lahti | official=2 probable=0 | outcome=PENDING | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW | SJK vs VPS | official=2 probable=0 | outcome=PENDING | label=NO_BET_LINEUP_REVIEW | evidence=MEDIUM | manual=YES | action=REVIEW_IF_LINEUP_CONFIRMED_NO_BET_OR_MISSED_ENTRY
- DIAGNOSTIC_NO_LINEUP_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | official=0 probable=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | evidence=NONE | manual=NO | action=NO_MODEL_CHANGE

## Guardrails
- This lineup shock report is advisory only and never changes prelock, picks, stake, or weights.
- Missing lineup data is not treated as source failure by itself.
- Red/green labels require causal review before any model lesson is accepted.
- No automatic lineup gate, source registry, or production changes are created here.
