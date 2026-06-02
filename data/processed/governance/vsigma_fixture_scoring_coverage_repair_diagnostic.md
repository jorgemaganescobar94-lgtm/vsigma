# vSIGMA Fixture / Scoring Coverage Repair Diagnostic - 2026-06-01

## Summary
- overall_status: ROOT_SCORING_FEED_TOO_NARROW
- root_cause: root scored feed has one or fewer same-day rows
- root_scored_rows: 1
- dated_scored_rows: 1
- dated_candidate_sources_found: 1
- coverage_matrix_rows: 1
- recommended_fix: Repair fixture fetch/scoring coverage before selector/model evaluation.
- auto_apply: NO
- production_change: NO

## Checks
- root_scored_matches | status=ONLY_NO_DATA_BLOCKED | rows=1 | same_day=1 | unique_same_day=1 | path=data\processed\matches_vsigma_scored_v3.csv | fix=Repair scoring enrichment/coverage, not market selection.
- dated_scored_matches | status=OK | rows=1 | same_day=1 | unique_same_day=1 | path=data\processed\today\2026-06-01\matches_vsigma_scored_v3.csv | fix=No repair needed for this file.
- dated_top_candidates | status=MISSING_DATED_SOURCE | rows=0 | same_day=0 | unique_same_day=0 | path=data\processed\today\2026-06-01\vsigma_top_candidates_v3.csv | fix=Create/copy dated scored or candidate snapshot before coverage matrix.
- dated_league_filtered | status=MISSING_DATED_SOURCE | rows=0 | same_day=0 | unique_same_day=0 | path=data\processed\today\2026-06-01\matches_league_filtered.csv | fix=Create/copy dated scored or candidate snapshot before coverage matrix.
- fixture_api_coverage_matrix | status=OK | rows=1 | same_day=1 | unique_same_day=1 | path=data\processed\today\2026-06-01\vsigma_fixture_api_coverage_matrix.csv | fix=No repair needed for this file.
- real_source_expander | status=OK | rows=1 | same_day=1 | unique_same_day=0 | path=data\processed\today\2026-06-01\vsigma_real_source_coverage_expander_summary.csv | fix=No repair needed for this file.

## Repair Notes
- build_fixture_api_coverage_matrix_v3 currently reads dated sources only: matches_vsigma_scored_v3.csv, vsigma_top_candidates_v3.csv, or matches_league_filtered.csv under data/processed/today/<date>/.
- Root-level data/processed/matches_vsigma_scored_v3.csv is not enough for the fixture coverage matrix unless copied/snapshotted into the dated folder or the matrix source lookup is expanded.
- This diagnostic does not fetch paid API data, change secrets, execute bets, or bypass No Bet gates.
