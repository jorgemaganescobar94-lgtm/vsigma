# vSIGMA Root Fixture Feed Expansion Diagnostic - 2026-06-01

## Summary
- overall_status: RAW_FIXTURE_SOURCE_MISSING
- root_cause: no dated raw candidate/filter source exists before scoring
- root_scored_same_day_rows: 1
- dated_scored_same_day_rows: 1
- coverage_matrix_rows: 1
- raw_candidate_sources_found: 0
- recommended_fix: Repair fixture fetch/filter producer to create matches_league_filtered.csv or vsigma_top_candidates_v3.csv for the date.
- auto_apply: NO
- production_change: NO

## Feed Checks
- root_scored_matches | status=ONLY_NO_DATA_BLOCKED | type=SCORING_ROOT | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=1 | path=data/processed/matches_vsigma_scored_v3.csv | fix=Expand source coverage and enrich stats/odds/standings before selection.
- dated_scored_snapshot | status=ONLY_NO_DATA_BLOCKED | type=SCORING_DATED | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=1 | path=data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv | fix=Expand source coverage and enrich stats/odds/standings before selection.
- dated_top_candidates | status=MISSING_RAW_CANDIDATE_SOURCE | type=CANDIDATES_DATED | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | path=data/processed/today/2026-06-01/vsigma_top_candidates_v3.csv | fix=Repair fixture fetch/filter stage before scoring.
- dated_league_filtered | status=MISSING_RAW_CANDIDATE_SOURCE | type=LEAGUE_FILTERED_DATED | total=0 | same_day=0 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | path=data/processed/today/2026-06-01/matches_league_filtered.csv | fix=Repair fixture fetch/filter stage before scoring.
- fixture_api_coverage_matrix | status=COVERAGE_BLOCKED | type=COVERAGE_MATRIX | total=1 | same_day=1 | unique_same_day=1 | blocked=1 | no_data_blocked=0 | path=data/processed/today/2026-06-01/vsigma_fixture_api_coverage_matrix.csv | fix=Repair missing stats/odds/lineup/standings coverage.
- real_selector_summary | status=OK | type=REAL_SELECTOR_SUMMARY | total=1 | same_day=1 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | path=data/processed/today/2026-06-01/vsigma_scored_to_real_shortlist_summary.csv | fix=No repair needed for this file.
- real_source_expander | status=OK | type=REAL_SOURCE_SUMMARY | total=1 | same_day=1 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | path=data/processed/today/2026-06-01/vsigma_real_source_coverage_expander_summary.csv | fix=No repair needed for this file.
- fixture_scoring_repair | status=OK | type=REPAIR_SUMMARY | total=1 | same_day=1 | unique_same_day=0 | blocked=0 | no_data_blocked=0 | path=data/processed/today/2026-06-01/vsigma_fixture_scoring_coverage_repair_summary.csv | fix=No repair needed for this file.

## Diagnosis
The dated scored snapshot and coverage matrix now work, but the feed is too narrow because there is no dated raw candidate/filter source before scoring. The pipeline needs a proper fixture fetch/filter layer producing `matches_league_filtered.csv` or `vsigma_top_candidates_v3.csv` for the target date. Current root/dataset contains only Ponte Preta vs Botafogo SP and it is NO_DATA_BLOCKED.

## Guardrails
- This diagnostic does not call APIs, alter secrets, change spend, execute bets or bypass safety gates.
- It diagnoses source width before scoring; it does not relax scoring or selector floors.
- No Bet remains correct until real scored fixtures pass coverage and selector gates.
