# vSIGMA Dated Scored Snapshot - 2026-07-31

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 4
- same_day_rows: 4
- rows_written: 4
- no_data_blocked_rows: 0
- non_blocked_rows: 4
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-31/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Bodo/Glimt vs Lillestrom | fixture_id=1494717 | league=Eliteserien | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Dundee Utd vs Rangers | fixture_id=1556628 | league=Premiership | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Valerenga vs Ham-Kam | fixture_id=1494723 | league=Eliteserien | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Lask Linz vs Grazer AK | fixture_id=1561894 | league=Bundesliga | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
