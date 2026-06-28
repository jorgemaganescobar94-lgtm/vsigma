# vSIGMA Dated Scored Snapshot - 2026-06-28

## Summary
- snapshot_status: SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED
- source_rows: 8
- same_day_rows: 8
- rows_written: 8
- no_data_blocked_rows: 8
- non_blocked_rows: 0
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-28/matches_vsigma_scored_v3.csv
- next_action: Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Banga vs Hegelmann Litauen | fixture_id=1547570 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Džiugas Telšiai vs FK Zalgiris Vilnius | fixture_id=1547571 | league=A Lyga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Athletic Club vs Avai | fixture_id=1520740 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Atletico Goianiense vs Ponte Preta | fixture_id=1520741 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Fortaleza EC vs Sport Recife | fixture_id=1520745 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Juventude vs Ceara | fixture_id=1520746 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Nautico Recife vs Goias | fixture_id=1520747 | league=Serie B | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- Figueirense vs Guarani Campinas | fixture_id=1526866 | league=Serie C | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
