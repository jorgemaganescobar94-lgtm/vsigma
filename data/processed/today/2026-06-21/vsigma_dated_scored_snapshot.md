# vSIGMA Dated Scored Snapshot - 2026-06-21

## Summary
- snapshot_status: SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED
- source_rows: 11
- same_day_rows: 11
- rows_written: 11
- no_data_blocked_rows: 11
- non_blocked_rows: 0
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-21/matches_vsigma_scored_v3.csv
- next_action: Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Džiugas Telšiai vs Suduva Marijampole | fixture_id=1522831 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Avai vs Cuiaba | fixture_id=1520731 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- CRB vs Fortaleza EC | fixture_id=1520733 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Goias vs Operario-PR | fixture_id=1520734 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- São Bernardo vs Juventude | fixture_id=1520737 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Barra vs Amazonas | fixture_id=1526856 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Brusque vs Floresta | fixture_id=1526858 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Caxias vs Maringá | fixture_id=1526864 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Ferroviária vs Inter De Limeira | fixture_id=1526860 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Ituano vs Figueirense | fixture_id=1526861 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Maranhão vs Paysandu | fixture_id=1526862 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
