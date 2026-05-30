# vSIGMA Probable XI Extraction Quality Ledger - 2026-05-29

## Summary
- sources_reviewed: 1
- quarantine_rows: 5
- accepted_rows: 0
- queue_items: 1
- priority_counts: HIGH=1
- failure_class_counts: PARSER_EXTRACTION_FAILURE=1
- auto_apply: NO
- production_change: NO

## Source / Reason Rows
- sportsmole | reason=official_overlap_too_low | class=PARSER_EXTRACTION_FAILURE | priority=HIGH | rows=5 | accepted=0 | quarantined=5 | q=0.450

## Guardrails
- This ledger is diagnostic only.
- It must not reduce source reliability automatically.
- Parser changes require later validation/promotion rules.
