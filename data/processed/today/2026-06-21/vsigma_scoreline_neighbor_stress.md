# vSIGMA Scoreline Neighbor Stress - 2026-06-21

## Summary
- scoreline_rows: 23
- scoreline_data_status_counts: NO_SCORELINE_DATA=23
- scoreline_neighbor_bucket_counts: NO_SCORELINE=23
- scoreline_stress_status_counts: SCORELINE_DATA_MISSING=20; DIAGNOSTIC_NO_SCORELINE_STRESS=3
- scoreline_learning_label_counts: NO_SCORELINE_SIGNAL=20; DIAGNOSTIC_NOT_REAL_FIXTURE=3
- stress_evidence_level_counts: LOW=20; NONE=3
- manual_review_required_counts: NO=23
- auto_apply: NO
- production_change: NO

## Scoreline Rows
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- SCORELINE_DATA_MISSING | Las Palmas vs Malaga | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Almeria vs Castellón | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Almeria vs Castellón | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Nautico Recife vs Fortaleza EC | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Ponte Preta vs Cuiaba | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=NO_PICK | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Malaga vs Las Palmas | score=NA bucket=NO_SCORELINE | market=TOTAL_GOALS outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Maringá vs Maranhão | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | TransINVEST Vilnius vs FK Trakai | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Gnistan vs Lahti | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | SJK vs VPS | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- DIAGNOSTIC_NO_SCORELINE_STRESS | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | score=NA bucket=NO_SCORELINE | market=NO_MARKET outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- SCORELINE_DATA_MISSING | Almeria vs Malaga | score=NA bucket=NO_SCORELINE | market=TOTAL_GOALS outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Ceara vs Botafogo SP | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Londrina vs Athletic Club | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Vila Nova vs Nautico Recife | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Banga vs FK Zalgiris Vilnius | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Panevėžys vs Šiauliai | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | TransINVEST Vilnius vs Kauno Žalgiris | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Anápolis vs AO Itabaiana | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Botafogo PB vs Volta Redonda | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA
- SCORELINE_DATA_MISSING | Santa Cruz vs Ypiranga-RS | score=NA bucket=NO_SCORELINE | market=UNKNOWN_FAMILY outcome=PENDING | label=NO_SCORELINE_SIGNAL | manual=NO | action=COLLECT_FINAL_SCORELINE_DATA

## Guardrails
- This scoreline stress report is advisory only and never changes picks, stake, gates, or weights.
- Neighbor labels are review candidates, not automatic truth.
- Diagnostic and missing-scoreline rows must not train the model.
- No automatic market-family, live, or production changes are created here.
