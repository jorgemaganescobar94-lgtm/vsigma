# vSIGMA Dated Scored Snapshot - 2026-06-10

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 2
- same_day_rows: 2
- rows_written: 2
- no_data_blocked_rows: 1
- non_blocked_rows: 1
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-10/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Malaga vs Las Palmas | fixture_id=1548055 | league=Segunda División | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL_STATS
- Cape Town City vs Magesi | fixture_id=1546281 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
