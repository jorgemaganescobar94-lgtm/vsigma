# vSIGMA Dated Scored Snapshot - 2026-07-11

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 13
- same_day_rows: 13
- rows_written: 13
- no_data_blocked_rows: 5
- non_blocked_rows: 8
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-07-11/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Orgryte IS vs BK Hacken | fixture_id=1494207 | league=Allsvenskan | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Aalesund vs Molde | fixture_id=1494692 | league=Eliteserien | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Tromso vs Valerenga | fixture_id=1494699 | league=Eliteserien | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Fredrikstad vs Lillestrom | fixture_id=1494694 | league=Eliteserien | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Gwangju FC vs Pohang Steelers | fixture_id=1506993 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Ulsan Hyundai FC vs Jeonbuk Motors | fixture_id=1506994 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Mjallby AIF vs AIK Stockholm | fixture_id=1494206 | league=Allsvenskan | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Gimcheon Sangmu FC vs Bucheon FC 1995 | fixture_id=1506992 | league=K League 1 | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL_STATS
- Kauno Žalgiris vs Panevėžys | fixture_id=1547585 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Caxias vs Floresta | fixture_id=1526894 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Gnistan vs Mariehamn | fixture_id=1495731 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Lahti vs HJK Helsinki | fixture_id=1495730 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Turku PS vs AC Oulu | fixture_id=1495732 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
