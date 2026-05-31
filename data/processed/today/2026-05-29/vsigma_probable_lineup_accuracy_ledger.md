# vSIGMA Probable XI Accuracy Ledger - 2026-05-29

## Summary
- rows_reviewed: 1
- evaluated_rows: 1
- pending_rows: 0
- grade_counts: D=1
- source_grade_summary: sportsmole:n=1,avg=0.455
- auto_apply: NO
- production_change: NO

## Rows
- Nice vs Saint Etienne | side=home | source=sportsmole | status=EVALUATED | grade=D | match=5/11 | probable=11

## Guardrails
- Accuracy ledger is learning-only and never applies production changes.
- Accuracy ledger reads only accepted probable rows after quarantine, never autonomous raw rows.
- Fuzzy player matching is used for evaluation only and does not fabricate players.
- Probable XI is evaluated only when official lineup players are available.
- NO_OFFICIAL_LINEUP is a pending state, not a source failure.
- Source reliability changes must be handled by a later governor module.
