# vSIGMA Dated Scored Snapshot - 2026-07-15

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 6
- same_day_rows: 6
- rows_written: 6
- no_data_blocked_rows: 0
- non_blocked_rows: 6
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-15/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Sutjeska vs Kairat Almaty | fixture_id=1554386 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Atert Bissen vs KI Klaksvik | fixture_id=1554375 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Universitatea Craiova vs ML Vitebsk | fixture_id=1554388 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Egnatia Rrogozhinë vs Petrocub | fixture_id=1554377 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Malisheva vs Vllaznia Shkodër | fixture_id=1554428 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Dečić vs FK Liepaja | fixture_id=1554421 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
