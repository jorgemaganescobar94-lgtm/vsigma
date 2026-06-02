# vSIGMA Fixture / Scoring Coverage Repair Diagnostic - 2026-06-01

## Summary
- overall_status: MISSING_DATED_SCORING_SNAPSHOT
- root_cause: coverage/scoring stage has no dated source for fixture matrix
- root_scored_rows: 1
- dated_scored_rows: 0
- dated_candidate_sources_found: 0
- coverage_matrix_rows: 0
- recommended_fix: Create dated snapshot data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv from scored root or repair fetch/scoring producer. Then rerun fixture coverage matrix and selector chain.
- auto_apply: NO
- production_change: NO

## Checks
- root_scored_matches | status=ONLY_NO_DATA_BLOCKED | rows=1 | same_day=1 | unique_same_day=1 | path=data/processed/matches_vsigma_scored_v3.csv | fix=Repair scoring enrichment/coverage, not market selection.
- dated_scored_matches | status=MISSING_DATED_SOURCE | rows=0 | same_day=0 | unique_same_day=0 | path=data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv | fix=Create/copy dated scored or candidate snapshot before coverage matrix.
- dated_top_candidates | status=MISSING_DATED_SOURCE | rows=0 | same_day=0 | unique_same_day=0 | path=data/processed/today/2026-06-01/vsigma_top_candidates_v3.csv | fix=Create/copy dated scored or candidate snapshot before coverage matrix.
- dated_league_filtered | status=MISSING_DATED_SOURCE | rows=0 | same_day=0 | unique_same_day=0 | path=data/processed/today/2026-06-01/matches_league_filtered.csv | fix=Create/copy dated scored or candidate snapshot before coverage matrix.
- fixture_api_coverage_matrix | status=EMPTY | rows=0 | same_day=0 | unique_same_day=0 | path=data/processed/today/2026-06-01/vsigma_fixture_api_coverage_matrix.csv | fix=Coverage matrix is empty because its dated source candidates are missing.
- real_source_expander | status=OK | rows=1 | same_day=1 | unique_same_day=0 | path=data/processed/today/2026-06-01/vsigma_real_source_coverage_expander_summary.csv | fix=Use this as corroborating diagnostic only.

## Repair Notes
- build_fixture_api_coverage_matrix_v3 currently reads dated sources only: matches_vsigma_scored_v3.csv, vsigma_top_candidates_v3.csv, or matches_league_filtered.csv under data/processed/today/<date>/.
- Root-level data/processed/matches_vsigma_scored_v3.csv is not enough for the fixture coverage matrix unless copied/snapshotted into the dated folder or the matrix source lookup is expanded.
- Even with a dated snapshot, the only current root scored row is NO_DATA_BLOCKED, so no pick permission should be created.
- This diagnostic does not fetch paid API data, change secrets, execute bets, or bypass No Bet gates.
