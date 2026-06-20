# vSIGMA Lineup Shock Learning - 2026-06-21

## Summary
- lineup_rows: 23
- lineup_data_status_counts: NO_LINEUP_DATA=15; HAS_LINEUP_DATA=8
- lineup_shock_status_counts: LINEUP_DATA_MISSING=12; OFFICIAL_LINEUP_AVAILABLE_NO_BET_REVIEW=7; DIAGNOSTIC_NO_LINEUP_LEARNING=3; OFFICIAL_LINEUP_AVAILABLE_NEUTRAL=1
- lineup_learning_label_counts: NO_LINEUP_SIGNAL=12; NO_BET_LINEUP_REVIEW=7; DIAGNOSTIC_NOT_REAL_FIXTURE=3; LINEUP_CONTEXT_PRESENT=1
- shock_evidence_level_counts: LOW=13; MEDIUM=7; NONE=3
- manual_review_required_counts: NO=16; YES=7
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
- DIAGNOSTIC_NO_LINEUP_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | official=0 probable=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | evidence=NONE | manual=NO | action=NO_MODEL_CHANGE
- LINEUP_DATA_MISSING | Almeria vs Malaga | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Ceara vs Botafogo SP | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Londrina vs Athletic Club | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Vila Nova vs Nautico Recife | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Banga vs FK Zalgiris Vilnius | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Panevėžys vs Šiauliai | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | TransINVEST Vilnius vs Kauno Žalgiris | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Anápolis vs AO Itabaiana | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Botafogo PB vs Volta Redonda | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA
- LINEUP_DATA_MISSING | Santa Cruz vs Ypiranga-RS | official=0 probable=0 | outcome=PENDING | label=NO_LINEUP_SIGNAL | evidence=LOW | manual=NO | action=COLLECT_LINEUP_DATA

## Guardrails
- This lineup shock report is advisory only and never changes prelock, picks, stake, or weights.
- Missing lineup data is not treated as source failure by itself.
- Red/green labels require causal review before any model lesson is accepted.
- No automatic lineup gate, source registry, or production changes are created here.
