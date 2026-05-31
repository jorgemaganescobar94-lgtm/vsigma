# vSIGMA Fixture API Coverage Matrix v3 - 2026-05-29

## Summary
- fixtures_reviewed: 2
- api_readiness_gates: WAIT_LINEUPS_OR_LIVE_ONLY=1; LOW_COVERAGE_NO_BET=1
- lineup_coverage: NONE=2
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=2
- recent_stats_coverage: FULL=1; NONE=1
- injuries_coverage: FULL=1; NONE=1
- standings_coverage: PARTIAL=1; NONE=1
- odds_coverage: FULL=1; NONE=1
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Nice vs Saint Etienne | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=72.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=FULL | odds=FULL | missing=lineup_coverage=NONE; standings_coverage=PARTIAL
- Cde Juventud Italiana vs Tecnico Universitario | gate=LOW_COVERAGE_NO_BET | score=15.0 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=NONE | injuries=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
