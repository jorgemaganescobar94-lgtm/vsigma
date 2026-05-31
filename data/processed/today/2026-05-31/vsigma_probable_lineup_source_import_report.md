# vSIGMA Probable Lineup Source Import - 2026-05-31

## Summary
- rows_seen: 12
- rows_imported: 12
- rows_learning_only: 0
- rows_rejected: 0
- rows_quarantined: 0
- input_files: data/processed/today/2026-05-31/probable_lineup_sources_autonomous.csv;data/processed/governance/probable_lineup_sources_autonomous.csv
- import_status_counts: IMPORTED=12
- quarantine_reason_counts: none
- sources_seen: sports_gambler=10; sportsmole=2
- template_rows: 240
- auto_apply: NO
- production_change: NO

## Imported Rows
- Almeria vs Valladolid | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Zaragoza vs Malaga | side=home | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Cordoba vs Huesca | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Palmeiras vs Chapecoense-sc | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Palmeiras vs Chapecoense-sc | side=home | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Deportivo La Coruna vs Las Palmas | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Almeria vs Valladolid | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Zaragoza vs Malaga | side=home | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Cordoba vs Huesca | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Palmeiras vs Chapecoense-sc | side=home | source=sportsmole | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Palmeiras vs Chapecoense-sc | side=home | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok
- Deportivo La Coruna vs Las Palmas | side=away | source=sports_gambler | status=IMPORTED | reason=OK | q=1.000 | notes=quality_ok

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
