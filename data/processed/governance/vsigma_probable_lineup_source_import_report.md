# vSIGMA Probable Lineup Source Import - 2026-07-03

## Summary
- rows_seen: 4
- rows_imported: 4
- rows_learning_only: 0
- rows_rejected: 0
- rows_quarantined: 0
- input_files: data/processed/today/2026-07-03/probable_lineup_sources_autonomous.csv;data/processed/governance/probable_lineup_sources_autonomous.csv
- import_status_counts: IMPORTED=4
- quarantine_reason_counts: none
- sources_seen: sportsmole=4
- template_rows: 20
- auto_apply: NO
- production_change: NO

## Imported Rows
- Sirius vs Mjallby AIF | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Sirius vs Mjallby AIF | side=away | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Sirius vs Mjallby AIF | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Sirius vs Mjallby AIF | side=away | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok

## Learning Only Rows
- none.

## Quarantined Rows
- none.

## Rejected Rows
- none.

## Guardrails
- IMPORTED rows may feed consensus/prelock.
- LEARNING_ONLY rows may feed accuracy ledger but must not feed consensus.
- Bad extraction quarantine blocks low-quality rows before consensus and accuracy ledger.
- Fuzzy player matching is used only for official-overlap validation, not to create players.
- Probable XI never equals official lineup.
