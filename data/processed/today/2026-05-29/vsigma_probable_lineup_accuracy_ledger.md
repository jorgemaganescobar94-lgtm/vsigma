# vSIGMA Probable XI Accuracy Ledger - 2026-05-29

## Summary
- rows_reviewed: 5
- evaluated_rows: 5
- pending_rows: 0
- grade_counts: D=5
- source_grade_summary: sportsmole:n=5,avg=0.036
- auto_apply: NO
- production_change: NO

## Rows
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=0/11 | probable=10
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=1/11 | probable=10
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=1/11 | probable=10
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=0/11 | probable=11
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=0/11 | probable=10

## Guardrails
- Accuracy ledger is learning-only and never applies production changes.
- Probable XI is evaluated only when official lineup players are available.
- NO_OFFICIAL_LINEUP is a pending state, not a source failure.
- Source reliability changes must be handled by a later governor module.
