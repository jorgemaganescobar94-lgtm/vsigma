# vSIGMA Dated Scored Snapshot - 2026-06-27

## Summary
- snapshot_status: SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED
- source_rows: 12
- same_day_rows: 12
- rows_written: 12
- no_data_blocked_rows: 12
- non_blocked_rows: 0
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-27/matches_vsigma_scored_v3.csv
- next_action: Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Criciuma vs São Bernardo | fixture_id=1520743 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Operario-PR vs America Mineiro | fixture_id=1520749 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- AO Itabaiana vs Ferroviária | fixture_id=1526869 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Floresta vs Barra | fixture_id=1526867 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Inter De Limeira vs Maringá | fixture_id=1526868 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Paysandu vs Santa Cruz | fixture_id=1526871 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- AC Oulu vs Lahti | fixture_id=1495720 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Gnistan vs VPS | fixture_id=1495718 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- HJK Helsinki vs KuPS | fixture_id=1495716 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Ilves vs SJK | fixture_id=1495715 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Mariehamn vs Inter Turku | fixture_id=1495717 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Turku PS vs FF Jaro | fixture_id=1495719 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
