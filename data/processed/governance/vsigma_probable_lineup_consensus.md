# vSIGMA Probable Lineup Consensus v2 - 2026-05-29

## Summary
- fixtures_reviewed: 2
- probable_lineup_gates: PROBABLE_XI_CONSENSUS_LOW=1; NO_PROBABLE_LINEUP_SOURCES=1
- home_confidence: LOW_WEIGHTED=1; NO_APPROVED_SOURCES=1
- away_confidence: NO_APPROVED_SOURCES=2
- auto_apply: NO
- production_change: NO

## Fixture Consensus
- Nice vs Saint Etienne | gate=PROBABLE_XI_CONSENSUS_LOW | home=LOW_WEIGHTED(1 src/11 consensus/w=1.000) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted=sportsmole (internal_conflict:sportsmole) /  | rejected= / 
- Cde Juventud Italiana vs Tecnico Universitario | gate=NO_PROBABLE_LINEUP_SOURCES | home=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted= /  | rejected= / 

## Guardrails
- Registry-approved probable XI is never treated as official lineup.
- Multiple rows from the same source are reduced to one best extraction before consensus scoring.
- Duplicate source/url/player rows are deduplicated before confidence scoring.
- Disabled, unregistered, out-of-scope, or review-only sources are rejected.
- Weighted consensus can support early shortlist/prelock planning only.
- Final stake still requires official lineup or explicit manual prelock approval.
