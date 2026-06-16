# vSIGMA Dated Scored Snapshot - 2026-06-16

## Summary
- snapshot_status: SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED
- source_rows: 3
- same_day_rows: 3
- rows_written: 3
- no_data_blocked_rows: 3
- non_blocked_rows: 0
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-16/matches_vsigma_scored_v3.csv
- next_action: Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- FK Zalgiris Vilnius vs Panevėžys | fixture_id=1547577 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Suduva Marijampole vs Šiauliai | fixture_id=1547576 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- TransINVEST Vilnius vs FK Trakai | fixture_id=1547575 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
