# vSIGMA Dated Scored Snapshot - 2026-07-07

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 12
- same_day_rows: 12
- rows_written: 12
- no_data_blocked_rows: 0
- non_blocked_rows: 12
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-07/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Vikingur Reykjavik vs Gyori ETO FC | fixture_id=1554374 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Lincoln Red Imps FC vs Inter Club d'Escaldes | fixture_id=1554368 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Ararat-Armenia vs Riga | fixture_id=1554361 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- KI Klaksvik vs Atert Bissen | fixture_id=1554367 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Sabah FA vs The New Saints | fixture_id=1554371 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Vardar Skopje vs KuPS | fixture_id=1554373 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Borac Banja Luka vs Levski Sofia | fixture_id=1554362 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Kauno Žalgiris vs Drita | fixture_id=1554366 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- AF Elbasani vs Bate Borisov | fixture_id=1554389 | league=UEFA Europa Conference League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Floriana vs Shamrock Rovers | fixture_id=1554364 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- UNA Strassen vs La Fiorita | fixture_id=1554410 | league=UEFA Europa Conference League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Tre Fiori vs Larne | fixture_id=1554372 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=NO_DATA_ENRICHMENT_REQUIRED | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
