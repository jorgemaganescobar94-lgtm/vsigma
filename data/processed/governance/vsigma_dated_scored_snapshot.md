# vSIGMA Dated Scored Snapshot - 2026-07-04

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 17
- same_day_rows: 17
- rows_written: 17
- no_data_blocked_rows: 12
- non_blocked_rows: 5
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-04/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Halmstad vs Vasteras SK FK | fixture_id=1494198 | league=Allsvenskan | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Degerfors IF vs Malmo FF | fixture_id=1494194 | league=Allsvenskan | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Jeonbuk Motors vs Gangwon FC | fixture_id=1506988 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Daejeon Citizen vs Bucheon FC 1995 | fixture_id=1506987 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- FC Anyang vs Pohang Steelers | fixture_id=1506986 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Panevėžys vs Hegelmann Litauen | fixture_id=1547581 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Criciuma vs Sport Recife | fixture_id=1520752 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Londrina vs CRB | fixture_id=1520756 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Novorizontino vs Atletico Goianiense | fixture_id=1520758 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Confiança vs Barra | fixture_id=1526878 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Maranhão vs Inter De Limeira | fixture_id=1526881 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Maringá vs Volta Redonda | fixture_id=1526882 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Santa Cruz vs Ituano | fixture_id=1526883 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- FF Jaro vs Ilves | fixture_id=1495724 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Lahti vs Gnistan | fixture_id=1495723 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- SJK vs Turku PS | fixture_id=1495725 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- VPS vs Mariehamn | fixture_id=1495726 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
