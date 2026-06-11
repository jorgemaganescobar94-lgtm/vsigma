# vSIGMA Fixture API Coverage Matrix v3 - 2026-06-10

## Summary
- fixtures_reviewed: 1
- api_readiness_gates: LOW_COVERAGE_NO_BET=1
- lineup_coverage: NONE=1
- probable_lineup_gates: NO_PROBABLE_LINEUP_SOURCES=1
- recent_stats_coverage: FULL=1
- injuries_coverage: NONE=1
- standings_coverage: PARTIAL=1
- odds_coverage: NONE=1
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Malaga vs Las Palmas | gate=LOW_COVERAGE_NO_BET | score=47.5 | lineups=NONE | probable=NO_PROBABLE_LINEUP_SOURCES | stats=FULL | injuries=NONE | odds=NONE | missing=lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=PARTIAL; odds_coverage=NONE

## Guardrails
- Official lineup remains primary truth.
- Probable XI consensus supports early shortlist only.
- Final stake still requires official lineup, prelock confirmation, or explicit manual override.
- It does not fabricate unavailable lineup data.
- Dated scored snapshot can expose existing scored rows to coverage matrix but cannot create pick permission.
