# vSIGMA Trusted Raw Scoring Queue - 2026-07-06

## Summary
- queue_rows: 27
- priority_counts: P1_TRUSTED_MISSING_SCORING=19; P2_LOW_COVERAGE_SCORING=8
- scoring_needed_counts: YES=27
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Degerfors IF vs Malmo FF | league=Allsvenskan | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Jeonbuk Motors vs Gangwon FC | league=K League 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Brescia Clube vs Cardoso Moreira | league=Carioca C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | CAAC Brasil vs Uniao Central | league=Carioca C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #5 | P1_TRUSTED_MISSING_SCORING | Campos AA vs Tigres do Brasil | league=Carioca C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #6 | P1_TRUSTED_MISSING_SCORING | EC Resende vs Búzios | league=Carioca C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #7 | P1_TRUSTED_MISSING_SCORING | Benjamín Aceval vs Deportivo Capiata | league=Division Intermedia | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #8 | P1_TRUSTED_MISSING_SCORING | Encarnación vs Guairena FC | league=Division Intermedia | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #9 | P1_TRUSTED_MISSING_SCORING | Universidad Catolica vs Mushuc Runa SC | league=Liga Pro | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #10 | P1_TRUSTED_MISSING_SCORING | Bars vs Ilbirs | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #11 | P1_TRUSTED_MISSING_SCORING | Centro Español vs Mercedes | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #12 | P1_TRUSTED_MISSING_SCORING | Deportivo Muñiz vs Deportivo Español | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #13 | P1_TRUSTED_MISSING_SCORING | Sportivo Barracas vs Yupanqui | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #14 | P1_TRUSTED_MISSING_SCORING | Miramar vs Atenas | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #15 | P2_LOW_COVERAGE_SCORING | Christos vs Loudoun 2 | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #16 | P2_LOW_COVERAGE_SCORING | FC Miami City vs Miami AC | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #17 | P2_LOW_COVERAGE_SCORING | Lansing City vs Flint City Bucks | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #18 | P2_LOW_COVERAGE_SCORING | Lorain County Leviathan vs Erie Sports Center | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #19 | P1_TRUSTED_MISSING_SCORING | Super Nova vs Ogre United | league=Virsliga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #20 | P1_TRUSTED_MISSING_SCORING | Portugal vs Spain | league=World Cup | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #21 | P1_TRUSTED_MISSING_SCORING | Keflavik vs Fram Reykjavik | league=Úrvalsdeild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #22 | P2_LOW_COVERAGE_SCORING | Colwyn Bay vs Rhyl | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #23 | P2_LOW_COVERAGE_SCORING | Cracovia Krakow vs Başakşehir | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #24 | P2_LOW_COVERAGE_SCORING | FK Partizan vs Neftchi Baku | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #25 | P2_LOW_COVERAGE_SCORING | Sportfreunde Schwaig vs SSV Jahn Regensburg | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #26 | P1_TRUSTED_MISSING_SCORING | Defensores Glew vs Atletico Pilar | league=Torneo Promocional Amateur | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #27 | P1_TRUSTED_MISSING_SCORING | Estrella de Berisso vs Juventud de Bernal | league=Torneo Promocional Amateur | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
