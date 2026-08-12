# vSIGMA Dated Scored Snapshot - 2026-08-12

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 15
- same_day_rows: 15
- rows_written: 15
- no_data_blocked_rows: 8
- non_blocked_rows: 7
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-08-12/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- FC Copenhagen vs Debreceni VSC | fixture_id=1607607 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Platense vs Coquimbo Unido | fixture_id=1547763 | league=CONMEBOL Libertadores | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Deportes Tolima vs Independiente del Valle | fixture_id=1547758 | league=CONMEBOL Libertadores | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Palmeiras vs Cerro Porteno | fixture_id=1547762 | league=CONMEBOL Libertadores | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- RB Bragantino vs Atletico-MG | fixture_id=1607197 | league=CONMEBOL Sudamericana | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Rapid Vienna vs Paide | fixture_id=1607625 | league=UEFA Europa Conference League | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Tigre vs Atletico Torque | fixture_id=1606077 | league=CONMEBOL Sudamericana | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- GKS Katowice vs Hapoel Tel Aviv | fixture_id=1607609 | league=UEFA Europa Conference League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Arkadag vs Goa | fixture_id=1565673 | league=AFC Champions League Two | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- East Bengal II vs Al Arabi | fixture_id=1569333 | league=AFC Champions League Two | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Amazulu vs Orlando Pirates | fixture_id=1600309 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Durban City vs Golden Arrows | fixture_id=1600310 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Kaizer Chiefs vs Sekhukhune United | fixture_id=1600311 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Milford FC vs Siwelele | fixture_id=1600312 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- La Unión vs Aucas | fixture_id=1548677 | league=Copa Ecuador | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
