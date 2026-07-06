# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-07-06

## Summary
- rows_reviewed: 34
- promoted_rows: 2
- blocked_rows: 4
- quarantine_rows: 27
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=27; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=4; PROMOTED_TO_SCORING_INPUT=2; NOT_TRUSTED_NO_PROMOTION=1
- next_action: Promoted rows may feed normal scoring gates only.
- auto_apply: NO
- production_change: NO

## Rows
- Degerfors IF vs Malmo FF | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Jeonbuk Motors vs Gangwon FC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- BK Hacken vs Djurgardens IF | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/governance/vsigma_promoted_raw_fixture_candidates.csv
- IF Brommapojkarna vs Gais | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/governance/vsigma_promoted_raw_fixture_candidates.csv
- Suduva Marijampole vs TransINVEST Vilnius | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Botafogo SP vs Avai | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Vila Nova vs São Bernardo | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Brusque vs Figueirense | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Brescia Clube vs Cardoso Moreira | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- CAAC Brasil vs Uniao Central | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Campos AA vs Tigres do Brasil | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- EC Resende vs Búzios | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Benjamín Aceval vs Deportivo Capiata | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Encarnación vs Guairena FC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Universidad Catolica vs Mushuc Runa SC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Bars vs Ilbirs | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Centro Español vs Mercedes | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Deportivo Muñiz vs Deportivo Español | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Sportivo Barracas vs Yupanqui | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Miramar vs Atenas | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Christos vs Loudoun 2 | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- FC Miami City vs Miami AC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Lansing City vs Flint City Bucks | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Lorain County Leviathan vs Erie Sports Center | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Super Nova vs Ogre United | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Portugal vs Spain | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Keflavik vs Fram Reykjavik | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Concórdia U20 vs Joinville U20 | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Colwyn Bay vs Rhyl | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Cracovia Krakow vs Başakşehir | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- FK Partizan vs Neftchi Baku | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Sportfreunde Schwaig vs SSV Jahn Regensburg | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Defensores Glew vs Atletico Pilar | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Estrella de Berisso vs Juventud de Bernal | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
