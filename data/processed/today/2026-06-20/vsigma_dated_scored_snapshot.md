# vSIGMA Dated Scored Snapshot - 2026-06-20

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 10
- same_day_rows: 10
- rows_written: 10
- no_data_blocked_rows: 9
- non_blocked_rows: 1
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-20/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Almeria vs Malaga | fixture_id=1551272 | league=Segunda División | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Banga vs FK Zalgiris Vilnius | fixture_id=1522830 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Panevėžys vs Šiauliai | fixture_id=1522828 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- TransINVEST Vilnius vs Kauno Žalgiris | fixture_id=1522829 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Ceara vs Botafogo SP | fixture_id=1520732 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Londrina vs Athletic Club | fixture_id=1520735 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Vila Nova vs Nautico Recife | fixture_id=1520739 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Anápolis vs AO Itabaiana | fixture_id=1526855 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Botafogo PB vs Volta Redonda | fixture_id=1526857 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Santa Cruz vs Ypiranga-RS | fixture_id=1526863 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
