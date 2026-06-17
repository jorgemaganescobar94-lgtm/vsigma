# vSIGMA Dated Scored Snapshot - 2026-06-17

## Summary
- snapshot_status: SNAPSHOT_DIAGNOSTIC_ONLY_ALL_NO_DATA_BLOCKED
- source_rows: 2
- same_day_rows: 2
- rows_written: 2
- no_data_blocked_rows: 2
- non_blocked_rows: 0
- source_path: data/processed/matches_vsigma_scored_v3.csv
- output_path: data/processed/today/2026-06-17/matches_vsigma_scored_v3.csv
- next_action: Snapshot written for coverage diagnostics only; do not create picks. Repair enrichment/coverage.
- auto_apply: NO
- production_change: NO

## Snapshot Rows
- Gnistan vs Lahti | fixture_id=1495707 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL
- SJK vs VPS | fixture_id=1495708 | league=Veikkausliiga | priority=NO_DATA_BLOCKED | market_hint=UNDER_OR_TEAM_TOTAL_UNDER_CHECK | data_warning=OK_FULL

## Guardrails
- Snapshot creation does not create picks, stake permission, or live permission.
- NO_DATA_BLOCKED rows may be snapshotted for diagnostics, but they remain blocked downstream.
- Dated snapshots only make existing scored rows visible to dated-source consumers such as fixture coverage matrix.
