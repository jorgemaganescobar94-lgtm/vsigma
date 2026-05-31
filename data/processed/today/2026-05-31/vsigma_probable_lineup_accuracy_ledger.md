# vSIGMA Probable XI Accuracy Ledger - 2026-05-31

## Summary
- rows_reviewed: 6
- evaluated_rows: 0
- pending_rows: 6
- learning_only_rows: 0
- promoted_rows: 6
- grade_counts: NO_OFFICIAL_LINEUP=6
- source_grade_summary: none
- auto_apply: NO
- production_change: NO

## Rows
- Almeria vs Valladolid | side=away | source=sports_gambler | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11
- Zaragoza vs Malaga | side=home | source=sports_gambler | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11
- Cordoba vs Huesca | side=away | source=sports_gambler | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11
- Palmeiras vs Chapecoense-sc | side=home | source=sportsmole | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11
- Palmeiras vs Chapecoense-sc | side=home | source=sports_gambler | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11
- Deportivo La Coruna vs Las Palmas | side=away | source=sports_gambler | probable_status=IMPORTED | status=NO_OFFICIAL_LINEUP | grade=NO_OFFICIAL_LINEUP | match=0/0 | probable=11

## Guardrails
- Accuracy ledger is learning-only and never applies production changes.
- IMPORTED rows may feed consensus; LEARNING_ONLY rows are evaluated but must not feed consensus/prelock.
- Accuracy ledger never reads autonomous raw rows directly.
- Fuzzy player matching is used for evaluation only and does not fabricate players.
- Source reliability changes must be handled by a later governor module.
