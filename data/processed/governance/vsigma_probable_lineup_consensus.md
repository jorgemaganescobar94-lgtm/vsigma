# vSIGMA Probable Lineup Consensus v2 - 2026-05-29

## Summary
- fixtures_reviewed: 2
- probable_lineup_gates: PROBABLE_LINEUP_CONFLICT=1; NO_PROBABLE_LINEUP_SOURCES=1
- home_confidence: CONFLICTING_SOURCES=1; NO_APPROVED_SOURCES=1
- away_confidence: NO_APPROVED_SOURCES=2
- auto_apply: NO
- production_change: NO

## Fixture Consensus
- Nice vs Saint Etienne | gate=PROBABLE_LINEUP_CONFLICT | home=CONFLICTING_SOURCES(1 src/2 consensus/w=0.091) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted=sportsmole /  | rejected= / 
- Cde Juventud Italiana vs Tecnico Universitario | gate=NO_PROBABLE_LINEUP_SOURCES | home=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted= /  | rejected= / 

## Guardrails
- Registry-approved probable XI is never treated as official lineup.
- Duplicate source/url/player rows are deduplicated before confidence scoring.
- Disabled, unregistered, out-of-scope, or review-only sources are rejected.
- Weighted consensus can support early shortlist/prelock planning only.
- Final stake still requires official lineup or explicit manual prelock approval.
