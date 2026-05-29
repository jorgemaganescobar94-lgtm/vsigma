# vSIGMA Fixture API Coverage Matrix - 2026-05-29

## Summary
- fixtures_reviewed: 20
- api_readiness_gates: WAIT_LINEUPS_OR_LIVE_ONLY=20
- lineup_coverage: NONE=20
- recent_stats_coverage: FULL=13; NONE=7
- injuries_coverage: NONE=12; FULL=8
- standings_coverage: FULL=12; NONE=7; PARTIAL=1
- odds_coverage: FULL=13; NONE=7
- auto_apply: NO
- production_change: NO

## Fixture Coverage
- Monza vs Catanzaro | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | stats=FULL | lineups=NONE | injuries=NONE | standings=FULL | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Orgryte IS vs IF Elfsborg | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- KFUM Oslo vs Tromso | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Rosenborg vs Bodo/Glimt | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Aalesund vs Ham-Kam | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Boca Juniors vs U. Catolica | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | stats=FULL | lineups=NONE | injuries=NONE | standings=FULL | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Brann vs Sarpsborg 08 FF | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Cruzeiro vs Barcelona SC | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | stats=FULL | lineups=NONE | injuries=NONE | standings=FULL | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Fredrikstad vs Start | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Valerenga vs Kristiansund BK | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=80.0 | stats=FULL | lineups=NONE | injuries=FULL | standings=FULL | odds=FULL | missing=lineup_coverage=NONE
- Nice vs Saint Etienne | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=72.5 | stats=FULL | lineups=NONE | injuries=FULL | standings=PARTIAL | odds=FULL | missing=lineup_coverage=NONE; standings_coverage=PARTIAL
- America de Cali vs Macara | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | stats=FULL | lineups=NONE | injuries=NONE | standings=FULL | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- Tigre vs Alianza Atletico | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=65.0 | stats=FULL | lineups=NONE | injuries=NONE | standings=FULL | odds=FULL | missing=lineup_coverage=NONE; injuries_coverage=NONE
- FK Trakai vs Suduva Marijampole | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=15.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- TransINVEST Vilnius vs Hegelmann Litauen | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=15.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- El Mokawloon vs Future FC | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=20.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Ghazl El Mehalla vs Haras El Hodood | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=20.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Masr vs Kahraba Ismailia | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=20.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- National Bank of Egypt vs Al Ittihad | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=20.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE
- Cde Juventud Italiana vs Tecnico Universitario | gate=WAIT_LINEUPS_OR_LIVE_ONLY | score=15.0 | stats=NONE | lineups=NONE | injuries=NONE | standings=NONE | odds=NONE | missing=league_coverage=PARTIAL; recent_stats_coverage=NONE; lineup_coverage=NONE; injuries_coverage=NONE; standings_coverage=NONE; odds_coverage=NONE

## Guardrails
- Matrix is diagnostic and gating-oriented.
- It does not execute bets.
- It does not fabricate unavailable API data.
- Missing lineups or low coverage must prevent strong prematch execution.
