# vSIGMA Dated Scored Snapshot - 2026-07-08

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 9
- same_day_rows: 9
- rows_written: 9
- no_data_blocked_rows: 2
- non_blocked_rows: 7
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-08/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Kairat Almaty vs Sutjeska | fixture_id=1554365 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Zira vs Torpedo Kutaisi | fixture_id=1554414 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- FC Differdange 03 vs Ilves | fixture_id=1554395 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- ML Vitebsk vs Universitatea Craiova | fixture_id=1554369 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Flora Tallinn vs Saburtalo | fixture_id=1554363 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Petrocub vs Egnatia Rrogozhinë | fixture_id=1554370 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- GAP Connah S Quay FC vs Ballkani | fixture_id=1554393 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Saint-Laurent vs Forge | fixture_id=1544845 | league=Canadian Championship | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Santo Domingo vs Independiente del Valle | fixture_id=1542926 | league=Copa Ecuador | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
