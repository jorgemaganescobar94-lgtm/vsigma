# v69.1 — Upstream Fixture Fetch/Filter Producer Plan

## Status
Implemented as an operational repair plan. No API calls were made. No secrets were touched. No spend was increased. No picks or stakes were created.

## Current finding
The pipeline now has a dated scored snapshot and the fixture coverage matrix can see the dated scored row, but there is still no broad raw fixture/candidate source before scoring.

Current 2026-06-01 state:
- Root scored rows: 1
- Dated scored rows: 1
- Coverage matrix rows: 1
- Raw candidate/filter sources found: 0
- Existing scored row: Ponte Preta vs Botafogo SP
- Current row state: NO_DATA_BLOCKED

## Root cause
The system lacks a dated pre-scoring producer for either:

- `data/processed/today/<date>/matches_league_filtered.csv`
- `data/processed/today/<date>/vsigma_top_candidates_v3.csv`

Without one of those files, scoring and downstream candidate selection can only work with whatever already exists in `data/processed/matches_vsigma_scored_v3.csv`.

## Required producer contract
A safe upstream fixture fetch/filter producer must create a dated local file with this minimum contract:

```text
target_date
fixture_id
fixture_datetime_utc
league
league_id
country
home_team
away_team
home_team_id
away_team_id
fixture_status_short
league_filter_reason
auto_apply=NO
production_change=NO
```

Preferred output:

```text
data/processed/today/<date>/matches_league_filtered.csv
```

Optional secondary output:

```text
data/processed/today/<date>/vsigma_top_candidates_v3.csv
```

## Safety gates
The producer must not:

- place bets;
- create stake permission;
- touch secrets;
- increase API spend;
- fabricate fixtures;
- convert lineup snapshots into scored candidates;
- bypass No Bet gates;
- convert `NO_DATA_BLOCKED` rows into candidates.

## Local-only first strategy
Before any API fetch is added, the producer should search existing local files in this order:

1. `data/raw/**/<date>*.csv`
2. `data/processed/today/<date>/*fixtures*.csv`
3. `data/processed/today/<date>/*matches*.csv`
4. `data/processed/*fixtures*.csv`
5. `data/processed/*matches*.csv`

Only rows with fixture identity and target-date alignment can be copied into `matches_league_filtered.csv`.

## API strategy, later only if explicitly approved
If no local raw fixtures exist, create a separate API fetcher later. It must be explicitly gated with:

```text
auto_apply=NO
production_change=NO
api_fetch_enabled=false by default
max_api_calls configured
```

No API fetch should run automatically until manually enabled.

## Acceptance test
For any target date, v69.1 is successful when:

```text
data/processed/today/<date>/matches_league_filtered.csv exists
```

and contains more than zero target-date rows that are not `NO_DATA_BLOCKED`.

Then rerun:

```powershell
python scripts/build_scored_to_real_shortlist.py --date <date> --timezone Atlantic/Canary
python scripts/build_dated_scored_snapshot.py --date <date> --timezone Atlantic/Canary
python scripts/build_fixture_api_coverage_matrix_v3.py --date <date> --timezone Atlantic/Canary
python scripts/build_consolidated_daily_operator_panel_v3.py --date <date> --timezone Atlantic/Canary
```

## Current verdict
For 2026-06-01: No Bet remains correct. There are no real raw candidates beyond one blocked scored row.
