# vSIGMA Dated Scored Snapshot - 2026-08-11

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 20
- same_day_rows: 20
- rows_written: 20
- no_data_blocked_rows: 7
- non_blocked_rows: 13
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-08-11/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Fluminense vs Independ. Rivadavia | fixture_id=1547760 | league=CONMEBOL Libertadores | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Kairat Almaty vs Levski Sofia | fixture_id=1607170 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Apollon Limassol vs Brann | fixture_id=1607601 | league=UEFA Europa Conference League | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Sabah FA vs Aarhus | fixture_id=1607172 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- NEC Nijmegen vs Olympiakos Piraeus | fixture_id=1598829 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Bodo/Glimt vs Union St. Gilloise | fixture_id=1598827 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Slovan Bratislava vs Mjallby AIF | fixture_id=1607173 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Sturm Graz vs Fenerbahçe | fixture_id=1607174 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Lyon vs Sparta Praha | fixture_id=1598828 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Saburtalo vs Larne | fixture_id=1607180 | league=UEFA Europa League | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Kauno Žalgiris vs Dinamo Zagreb | fixture_id=1607171 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Celje vs Ararat-Armenia | fixture_id=1605371 | league=UEFA Champions League | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Boca Juniors vs Deportivo Recoleta | fixture_id=1607648 | league=CONMEBOL Sudamericana | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- FK Crvena Zvezda vs Hapoel Beer Sheva | fixture_id=1607169 | league=UEFA Champions League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- CSKA 1948 vs Panathinaikos | fixture_id=1607603 | league=UEFA Europa Conference League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Chippa United vs Richards Bay | fixture_id=1600305 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Marumo Gallants vs Kruger United | fixture_id=1600306 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Polokwane City vs Stellenbosch | fixture_id=1600307 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- TS Galaxy vs Mamelodi Sundowns | fixture_id=1600308 | league=Premier Soccer League | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Avai vs CRB | fixture_id=1520801 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
