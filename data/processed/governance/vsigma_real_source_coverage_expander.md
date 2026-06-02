# vSIGMA Real Source Coverage Expander - 2026-06-01

## Summary
- overall_status: REAL_SOURCE_PRESENT_BUT_ALL_BLOCKED
- root_cause: same-day scored rows exist but no row passed real selector floors
- max_same_day_fixture_count: 1
- root_scored_same_day_rows: 1
- dated_scored_same_day_rows: 1
- real_shortlist_rows: 0
- real_bets_rows: 0
- official_lineup_same_day_rows: 0
- official_lineup_unique_same_day_fixtures: 0
- next_action: Inspect data quality floors and source coverage; keep No Bet.
- auto_apply: NO
- production_change: NO

## Source Rows
- root_scored_matches | status=ONLY_NO_DATA_BLOCKED | type=SCORING_ROOT | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=1 | real_like=0 | proxy_like=0 | path=data\processed\matches_vsigma_scored_v3.csv | detail=same-day scoring rows exist but all are NO_DATA_BLOCKED
- dated_scored_matches | status=ONLY_NO_DATA_BLOCKED | type=SCORING_DATED | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=1 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\matches_vsigma_scored_v3.csv | detail=same-day scoring rows exist but all are NO_DATA_BLOCKED
- real_shortlist | status=EMPTY | type=REAL_SELECTOR | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\vsigma_real_today_execution_shortlist.csv | detail=file exists but has no rows
- real_bets_only | status=EMPTY | type=REAL_SELECTOR | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\vsigma_real_today_execution_bets_only.csv | detail=file exists but has no rows
- selector_summary | status=HAS_SAME_DAY_ROWS | type=REAL_SELECTOR_SUMMARY | total=1 | same_day=1 | unique_same_day=0 | blocked=1 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\vsigma_scored_to_real_shortlist_summary.csv | detail=file has same-day rows
- official_lineups | status=NO_SAME_DAY_ROWS | type=LINEUP_SNAPSHOT | total=30 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\official_lineup_sources.csv | detail=file has rows but none for target date
- probable_lineup_consensus | status=EMPTY | type=LINEUP_PROBABLE | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\vsigma_probable_lineup_consensus.csv | detail=file exists but has no rows
- daily_board | status=EMPTY | type=BOARD | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | real_like=0 | proxy_like=0 | path=data\processed\today\2026-06-01\vsigma_daily_execution_board.csv | detail=file exists but has no rows

## Guardrails
- This expander is diagnostic; it does not fetch paid API data or execute bets.
- Lineup snapshots are coverage evidence only, not candidate permission.
- Real candidates must come from scored fixture rows and pass selector floors.
