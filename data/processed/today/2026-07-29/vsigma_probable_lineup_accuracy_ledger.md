# vSIGMA Probable XI Accuracy Ledger - 2026-07-29

## Summary
- rows_reviewed: 11
- evaluated_rows: 11
- pending_rows: 0
- learning_only_rows: 5
- promoted_rows: 6
- grade_counts: B=4; A=2; C=3; D=2
- source_grade_summary: sportsmole:n=11,avg=0.661
- auto_apply: NO
- production_change: NO

## Rows
- KFUM Oslo vs Molde | side=home | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=B | match=8/11 | probable=11
- Remo vs Vitoria | side=home | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=A | match=10/11 | probable=11
- Remo vs Vitoria | side=away | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=B | match=8/11 | probable=11
- Remo vs Vitoria | side=away | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=A | match=10/11 | probable=11
- Remo vs Vitoria | side=home | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=B | match=9/11 | probable=11
- Aalesund vs Viking | side=away | source=sportsmole | probable_status=IMPORTED | status=EVALUATED | grade=B | match=8/11 | probable=11
- KFUM Oslo vs Molde | side=away | source=sportsmole | probable_status=LEARNING_ONLY | status=EVALUATED | grade=C | match=7/11 | probable=11
- KFUM Oslo vs Molde | side=away | source=sportsmole | probable_status=LEARNING_ONLY | status=EVALUATED | grade=D | match=3/11 | probable=11
- Remo vs Vitoria | side=away | source=sportsmole | probable_status=LEARNING_ONLY | status=EVALUATED | grade=D | match=5/11 | probable=11
- Aalesund vs Viking | side=home | source=sportsmole | probable_status=LEARNING_ONLY | status=EVALUATED | grade=C | match=6/11 | probable=11
- Aalesund vs Viking | side=home | source=sportsmole | probable_status=LEARNING_ONLY | status=EVALUATED | grade=C | match=6/11 | probable=11

## Guardrails
- Accuracy ledger is learning-only and never applies production changes.
- IMPORTED rows may feed consensus; LEARNING_ONLY rows are evaluated but must not feed consensus/prelock.
- Accuracy ledger never reads autonomous raw rows directly.
- Fuzzy player matching is used for evaluation only and does not fabricate players.
- Source reliability changes must be handled by a later governor module.
