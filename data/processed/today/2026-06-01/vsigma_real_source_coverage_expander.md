# vSIGMA Real Source Coverage Expander - 2026-06-01

## Summary
- overall_status: SOURCE_FEED_TOO_NARROW
- root_cause: scored source has only one same-day fixture and no dated scored snapshot
- max_same_day_fixture_count: 1
- root_scored_same_day_rows: 1
- dated_scored_same_day_rows: 0
- real_shortlist_rows: 0
- real_bets_rows: 0
- official_lineup_same_day_rows: 0
- official_lineup_unique_same_day_fixtures: 0
- next_action: Expand or repair fixture fetch/scoring coverage for the target date. Keep No Bet until real scored candidates exist.
- auto_apply: NO
- production_change: NO

## Source Rows
- root_scored_matches | status=ONLY_NO_DATA_BLOCKED | type=SCORING_ROOT | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=1 | real_like=0 | proxy_like=0 | path=data/processed/matches_vsigma_scored_v3.csv | detail=same-day scoring row exists but is NO_DATA_BLOCKED.
- dated_scored_matches | status=MISSING | type=SCORING_DATED | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv | detail=dated scored snapshot is missing.
- real_shortlist | status=EMPTY_OR_NO_REAL_CANDIDATES | type=REAL_SELECTOR | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/vsigma_real_today_execution_shortlist.csv | detail=real selector produced no real shortlist rows.
- real_bets_only | status=EMPTY_OR_NO_REAL_CANDIDATES | type=REAL_SELECTOR | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/vsigma_real_today_execution_bets_only.csv | detail=real selector produced no real bets-only rows.
- selector_summary | status=HAS_SUMMARY | type=REAL_SELECTOR_SUMMARY | total=1 | same_day=1 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/vsigma_scored_to_real_shortlist_summary.csv | detail=selector confirms source_rows=1, same_day_rows=1, real_shortlist_rows=0, real_bets_rows=0.
- official_lineups | status=LINEUP_NOT_TARGET_DATE | type=LINEUP_SNAPSHOT | total=30 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/official_lineup_sources.csv | detail=official lineup file exists but rows are from other dates, not target date.
- daily_board | status=EMPTY | type=BOARD | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data/processed/today/2026-06-01/vsigma_daily_execution_board.csv | detail=board has no rows because no real scored candidate reached translator/board.

## Diagnosis
The real selector works, but the source feed is too narrow: only one same-day scored fixture exists and it is NO_DATA_BLOCKED. No dated scored snapshot exists for 2026-06-01, and official lineup snapshots cannot be treated as scored candidate coverage. The next fix is not a market/pick change; it is fixture fetch/scoring coverage expansion.

## Guardrails
- This expander is diagnostic; it does not fetch paid API data or execute bets.
- Lineup snapshots are coverage evidence only, not candidate permission.
- Real candidates must come from scored fixture rows and pass selector floors.
