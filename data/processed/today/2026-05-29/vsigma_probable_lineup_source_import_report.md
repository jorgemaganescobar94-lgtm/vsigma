# vSIGMA Probable Lineup Source Import - 2026-05-29

## Summary
- rows_seen: 2
- rows_imported: 0
- rows_rejected: 0
- rows_quarantined: 2
- input_files: data/processed/today/2026-05-29/probable_lineup_sources_autonomous.csv;data/processed/governance/probable_lineup_sources_autonomous.csv
- import_status_counts: QUARANTINED=2
- quarantine_reason_counts: official_overlap_too_low=2
- sources_seen: sportsmole=2
- template_rows: 20
- auto_apply: NO
- production_change: NO

## Imported Rows
- none. No probable XI rows passed quality gate.

## Quarantined Rows
- Nice vs Saint Etienne | side=home | source=sportsmole | reason=official_overlap_too_low | q=0.450 | notes=official_overlap=0/11
- Nice vs Saint Etienne | side=home | source=sportsmole | reason=official_overlap_too_low | q=0.450 | notes=official_overlap=0/11

## Rejected Rows
- none.

## Guardrails
- Importer never scrapes and never fabricates probable XIs.
- Bad extraction quarantine blocks low-quality rows before consensus and accuracy ledger.
- Official-overlap quarantine prevents bad parsed text from damaging source reliability.
- Probable XI never equals official lineup.
