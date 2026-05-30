# vSIGMA Probable XI Extraction Quality Ledger - 2026-05-29

## Summary
- sources_reviewed: 1
- quarantine_rows: 5
- accepted_rows: 0
- queue_items: 2
- priority_counts: HIGH=2
- failure_class_counts: TEXT_BOUNDARY_FAILURE=1; PARSER_EXTRACTION_FAILURE=1
- auto_apply: NO
- production_change: NO

## Source / Reason Rows
- sportsmole | reason=name_fragment_too_long | class=TEXT_BOUNDARY_FAILURE | priority=HIGH | rows=1 | accepted=0 | quarantined=1 | q=0.750
- sportsmole | reason=official_overlap_too_low | class=PARSER_EXTRACTION_FAILURE | priority=HIGH | rows=4 | accepted=0 | quarantined=4 | q=0.359

## Guardrails
- This ledger is diagnostic only.
- It must not reduce source reliability automatically.
- Parser changes require later validation/promotion rules.
