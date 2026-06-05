# vSIGMA Probable Lineup Source Registry - 2026-06-05

## Summary
- total_sources: 15
- enabled: YES=15
- status: ACTIVE=13; REVIEW_ONLY=2
- source_types: global=7; local=7; official=1
- methods: manual_import=15
- auto_apply: NO
- production_change: NO

## Sources
- sportsmole | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.85 | reliability=0.72 | method=manual_import
- whoscored | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.90 | reliability=0.78 | method=manual_import
- rotowire | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.80 | reliability=0.70 | method=manual_import
- guardian_predicted | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Premier League | country=England | priority=0.92 | reliability=0.82 | method=manual_import
- sports_gambler | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.78 | reliability=0.68 | method=manual_import
- sportskeeda | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.72 | reliability=0.60 | method=manual_import
- ninetymin | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.72 | reliability=0.62 | method=manual_import
- footballtransfers | enabled=YES | status=ACTIVE | scope=multi_league | league=ALL | country=ALL | priority=0.70 | reliability=0.60 | method=manual_import
- lequipe | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Ligue 1 | country=France | priority=0.86 | reliability=0.76 | method=manual_import
- maxifoot | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Ligue 1 | country=France | priority=0.78 | reliability=0.68 | method=manual_import
- madeinfoot | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Ligue 1 | country=France | priority=0.76 | reliability=0.66 | method=manual_import
- gffn | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Ligue 1 | country=France | priority=0.72 | reliability=0.62 | method=manual_import
- standard_sport | enabled=YES | status=ACTIVE | scope=selected_leagues | league=Premier League | country=England | priority=0.78 | reliability=0.68 | method=manual_import
- local_media_generic | enabled=YES | status=REVIEW_ONLY | scope=league_specific | league=CONFIGURABLE | country=CONFIGURABLE | priority=0.88 | reliability=0.75 | method=manual_import
- club_official_hint | enabled=YES | status=REVIEW_ONLY | scope=team_specific | league=CONFIGURABLE | country=CONFIGURABLE | priority=0.95 | reliability=0.85 | method=manual_import

## Guardrails
- Registry approves sources for probable XI only, never official lineups.
- Disabled or non-active sources must not influence consensus.
- REVIEW_ONLY sources require explicit per-use review before activation.
