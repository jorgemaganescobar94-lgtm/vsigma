# vSIGMA Probable Lineup Source Import - 2026-05-29

## Summary
- rows_seen: 8
- rows_imported: 8
- rows_rejected: 0
- input_files: data/processed/today/2026-05-29/probable_lineup_sources_autonomous.csv;data/processed/governance/probable_lineup_sources_autonomous.csv
- import_status_counts: IMPORTED=8
- sources_seen: sportsmole=8
- template_rows: 20
- auto_apply: NO
- production_change: NO

## Imported Rows
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK

## Guardrails
- Importer never scrapes and never fabricates probable XIs.
- Imported rows still pass through registry-weighted consensus validation.
- Probable XI never equals official lineup.
