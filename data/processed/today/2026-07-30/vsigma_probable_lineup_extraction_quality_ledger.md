# vSIGMA Probable XI Extraction Quality Ledger - 2026-07-30

## Summary
- sources_reviewed: 1
- quarantine_rows: 5
- accepted_rows: 7
- queue_items: 1
- priority_counts: HIGH=1
- failure_class_counts: PARSER_EXTRACTION_FAILURE=1
- auto_apply: NO
- production_change: NO

## Source / Reason Rows
- sportsmole | reason=OK | class=ACCEPTED_SIGNAL | priority=NONE | rows=7 | accepted=7 | quarantined=0 | q=1.000
- sportsmole | reason=official_overlap_too_low | class=PARSER_EXTRACTION_FAILURE | priority=HIGH | rows=5 | accepted=7 | quarantined=5 | q=0.109

## Guardrails
- This ledger is diagnostic only.
- It must not reduce source reliability automatically.
- Parser changes require later validation/promotion rules.
