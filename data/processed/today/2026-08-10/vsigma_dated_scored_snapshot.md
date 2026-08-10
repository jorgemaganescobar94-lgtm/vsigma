# vSIGMA Dated Scored Snapshot - 2026-08-10

## Summary
- snapshot_status: SNAPSHOT_WRITTEN_WITH_REAL_ROWS
- source_rows: 9
- same_day_rows: 9
- rows_written: 9
- no_data_blocked_rows: 3
- non_blocked_rows: 6
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-08-10/matches_vsigma_scored_v3.csv
- next_action: Rerun coverage matrix and selector chain; downstream gates still required.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Sirius vs IF Brommapojkarna | fixture_id=1494239 | league=Allsvenskan | priority=A_ANALIZAR_PRIMERO | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Vasteras SK FK vs Djurgardens IF | fixture_id=1494240 | league=Allsvenskan | priority=B_ANALIZAR | market_hint=AWAY_SIDE_OR_AWAY_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Santa Clara vs Nacional | fixture_id=1575453 | league=Primeira Liga | priority=B_ANALIZAR | market_hint=HOME_SIDE_OR_HOME_TEAM_TOTAL_CHECK | data_warning=OK_FULL
- Silkeborg vs Odense | fixture_id=1548989 | league=Superliga | priority=B_ANALIZAR | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Jong AZ vs FC Eindhoven | fixture_id=1551745 | league=Eerste Divisie | priority=C_SOLO_SI_BLOQUE_SECO | market_hint=OVER_OR_BTTS_CHECK | data_warning=OK_FULL
- Jong PSV U21 vs FC Volendam | fixture_id=1551746 | league=Eerste Divisie | priority=C_SOLO_SI_BLOQUE_SECO | market_hint=NO_DATA_ENRICHMENT_REQUIRED | data_warning=OK_FULL
- Pendikspor vs Batman Petrolspor | fixture_id=1585694 | league=1. Lig | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- TransINVEST Vilnius vs Panevėžys | fixture_id=1547607 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Goias vs Londrina | fixture_id=1520805 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
