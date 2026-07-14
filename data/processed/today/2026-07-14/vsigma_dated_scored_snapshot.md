# vSIGMA Dated Scored Snapshot - 2026-07-14

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 11
- same_day_rows: 11
- rows_written: 11
- no_data_blocked_rows: 0
- non_blocked_rows: 11
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-14/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Gyori ETO FC vs Vikingur Reykjavik | fixture_id=1554378 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Inter Club d'Escaldes vs Lincoln Red Imps FC | fixture_id=1554380 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Riga vs Ararat-Armenia | fixture_id=1554384 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- The New Saints vs Sabah FA | fixture_id=1554387 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- KuPS vs Vardar Skopje | fixture_id=1554381 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Saburtalo vs Flora Tallinn | fixture_id=1554379 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Levski Sofia vs Borac Banja Luka | fixture_id=1554383 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Drita vs Kauno Žalgiris | fixture_id=1554376 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Shamrock Rovers vs Floriana | fixture_id=1554385 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- La Fiorita vs UNA Strassen | fixture_id=1554425 | league=UEFA Europa Conference League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Larne vs Tre Fiori | fixture_id=1554382 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=NO_DATA_ENRICHMENT_REQUIRED | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
