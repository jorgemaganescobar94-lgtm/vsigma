# vSIGMA Probable Lineup Source Registry - 2026-05-29

## Summary
- total_sources: 7
- enabled: YES=7
- status: ACTIVE=5; REVIEW_ONLY=2
- source_types: global=4; local=2; official=1
- methods: manual_import=7
- auto_apply: NO
- production_change: NO

## Sources
- sportsmole | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.85 | reliability=0.72 | method=manual_import
- whoscored | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.90 | reliability=0.78 | method=manual_import
- rotowire | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.80 | reliability=0.70 | method=manual_import
- guardian_predicted | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Premier League | country=England | priority=0.92 | reliability=0.82 | method=manual_import
- sports_gambler | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.78 | reliability=0.68 | method=manual_import
- local_media_generic | enabled=YES | status=REVIEW_ONLY | scope=league_specific | league=CONFIGURABLE | country=CONFIGURABLE | priority=0.88 | reliability=0.75 | method=manual_import
- club_official_hint | enabled=YES | status=REVIEW_ONLY | scope=team_specific | league=CONFIGURABLE | country=CONFIGURABLE | priority=0.95 | reliability=0.85 | method=manual_import

## Guardrails
- Registry approves sources for probable XI only, never official lineups.
- Disabled or non-active sources must not influence consensus.
- REVIEW_ONLY sources require explicit per-use review before activation.
