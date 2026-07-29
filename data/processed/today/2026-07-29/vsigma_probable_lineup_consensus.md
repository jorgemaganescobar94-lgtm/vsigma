# vSIGMA Probable Lineup Consensus v2 - 2026-07-29

## Summary
- fixtures_reviewed: 4
- probable_lineup_gates: PROBABLE_XI_CONSENSUS_LOW=3; NO_PROBABLE_LINEUP_SOURCES=1
- home_confidence: NO_APPROVED_SOURCES=2; LOW_WEIGHTED=2
- away_confidence: NO_APPROVED_SOURCES=2; LOW_WEIGHTED=2
- auto_apply: NO
- production_change: NO

## Fixture Consensus
- IF Brommapojkarna vs Hammarby FF | gate=NO_PROBABLE_LINEUP_SOURCES | home=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted= /  | rejected= / 
- KFUM Oslo vs Molde | gate=PROBABLE_XI_CONSENSUS_LOW | home=LOW_WEIGHTED(1 src/11 consensus/w=1.000) | away=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | accepted=sportsmole /  | rejected= / 
- Remo vs Vitoria | gate=PROBABLE_XI_CONSENSUS_LOW | home=LOW_WEIGHTED(1 src/11 consensus/w=1.000) | away=LOW_WEIGHTED(1 src/11 consensus/w=1.000) | accepted=sportsmole (internal_conflict:sportsmole) / sportsmole (internal_conflict:sportsmole) | rejected= / 
- Aalesund vs Viking | gate=PROBABLE_XI_CONSENSUS_LOW | home=NO_APPROVED_SOURCES(0 src/0 consensus/w=0.000) | away=LOW_WEIGHTED(1 src/11 consensus/w=1.000) | accepted= / sportsmole | rejected= / 

## Guardrails
- Registry-approved probable XI is never treated as official lineup.
- Multiple rows from the same source are reduced to one best extraction before consensus scoring.
- Duplicate source/url/player rows are deduplicated before confidence scoring.
- Disabled, unregistered, out-of-scope, or review-only sources are rejected.
- Weighted consensus can support early shortlist/prelock planning only.
- Final stake still requires official lineup or explicit manual prelock approval.
