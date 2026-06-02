# vSIGMA Raw Fixture Candidate Source Diagnostic - 2026-06-01

## Summary
- overall_status: NO_RAW_CANDIDATES_BUILT
- accepted_rows: 0
- rejected_rows: 2
- sources_checked: 4
- source_status_counts: NO_ACCEPTED_ROWS=2; MISSING=2
- next_action: Repair upstream fixture fetch/filter source; do not fabricate rows from blocked data.
- auto_apply: NO
- production_change: NO

## Sources
- dated_scored_snapshot | status=NO_ACCEPTED_ROWS | rows=1 | same_day=1 | accepted=0 | rejected=1 | path=data/processed/today/2026-06-01/matches_vsigma_scored_v3.csv | detail=same-day row exists but is blocked/NO_DATA_BLOCKED and cannot become raw candidate.
- root_scored_matches | status=NO_ACCEPTED_ROWS | rows=1 | same_day=1 | accepted=0 | rejected=1 | path=data/processed/matches_vsigma_scored_v3.csv | detail=root row exists but is blocked/NO_DATA_BLOCKED and cannot become raw candidate.
- dated_top_candidates | status=MISSING | rows=0 | same_day=0 | accepted=0 | rejected=0 | path=data/processed/today/2026-06-01/vsigma_top_candidates_v3.csv | detail=source missing.
- dated_league_filtered | status=MISSING | rows=0 | same_day=0 | accepted=0 | rejected=0 | path=data/processed/today/2026-06-01/matches_league_filtered.csv | detail=source missing.

## Diagnosis
No local source has a valid raw fixture candidate for 2026-06-01. The only available fixture is Ponte Preta vs Botafogo SP and it is NO_DATA_BLOCKED. v69.0 must not fabricate rows from that. The next real repair is upstream fixture fetch/filter generation.

## Guardrails
- Diagnostic only; does not call APIs, alter secrets, spend money, create picks or bypass No Bet.
- Blocked or NO_DATA_BLOCKED rows cannot become raw candidates.
- Use accepted rows only as input to normal scoring and safety gates.
