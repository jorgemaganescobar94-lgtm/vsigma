# vSIGMA Dated Scored Snapshot - 2026-08-18

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 14
- same_day_rows: 14
- rows_written: 14
- no_data_blocked_rows: 9
- non_blocked_rows: 5
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-08-18/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Independ. Rivadavia vs Fluminense | fixture_id=1547770 | league=CONMEBOL Libertadores | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Fenerbahçe vs Lyon | fixture_id=1622621 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Dinamo Zagreb vs Viking | fixture_id=1622620 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL_STATS
- Deportivo Recoleta vs Boca Juniors | fixture_id=1607651 | league=CONMEBOL Sudamericana | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL_STATS
- Levski Sofia vs AEK Athens FC | fixture_id=1622622 | league=UEFA Champions League | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Hapoel Acre vs Maccabi Kiryat Gat | fixture_id=1555107 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Hapoel Afula vs Ashdod | fixture_id=1555108 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Hapoel Kfar Shalem vs Kafr Qasim | fixture_id=1555109 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Hapoel Ra'anana vs Maccabi Ahi Nazareth | fixture_id=1555111 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Hapoel Rishon LeZion vs Hapoel Kfar Saba | fixture_id=1555110 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Ironi Modi'in vs Maccabi Herzliya | fixture_id=1555112 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Maccabi Bnei Raina vs Bnei Yehuda | fixture_id=1555113 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Maccabi Kabilio Jaffa vs Kiryat Yam SC | fixture_id=1555114 | league=Liga Leumit | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Londrina vs Atletico Goianiense | fixture_id=1520826 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
