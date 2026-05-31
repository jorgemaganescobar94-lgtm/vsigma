# vSIGMA Probable Lineup Source Import - 2026-05-29

## Summary
- rows_seen: 2
- rows_imported: 2
- rows_rejected: 0
- rows_quarantined: 0
- input_files: data/processed/today/2026-05-29/probable_lineup_sources_autonomous.csv;data/processed/governance/probable_lineup_sources_autonomous.csv
- import_status_counts: IMPORTED=2
- quarantine_reason_counts: none
- sources_seen: sportsmole=2
- template_rows: 20
- auto_apply: NO
- production_change: NO

## Imported Rows
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=fuzzy_official_overlap=5/11;matches=diouf~y diouf:0.96,mendy~a mendy:0.96,clauss~j clauss:0.96,sanson~m sanson:0.96,cho~m cho:0.96
- Nice vs Saint Etienne | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=fuzzy_official_overlap=5/11;matches=diouf~y diouf:0.96,mendy~a mendy:0.96,clauss~j clauss:0.96,sanson~m sanson:0.96,cho~m cho:0.96

## Quarantined Rows
- none.

## Rejected Rows
- none.

## Guardrails
- Importer never scrapes and never fabricates probable XIs.
- Bad extraction quarantine blocks low-quality rows before consensus and accuracy ledger.
- Fuzzy player matching is used only for official-overlap validation, not to create players.
- Official-overlap quarantine prevents bad parsed text from damaging source reliability.
- Probable XI never equals official lineup.
