# vSIGMA Scoring Gap Explainer - 2026-07-06

## Summary
- rows_reviewed: 34
- missing_scored_rows: 27
- no_data_blocked_rows: 4
- not_trusted_rows: 1
- promoted_rows: 2
- gap_status_counts: MISSING_SCORED_ROW=27; SCORED_ROW_NO_DATA_BLOCKED=4; PROMOTED=2; NOT_TRUSTED_SKIPPED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.
- auto_apply: NO
- production_change: NO

## Gap Rows
- Degerfors IF vs Malmo FF | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Jeonbuk Motors vs Gangwon FC | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- BK Hacken vs Djurgardens IF | promotion=PROMOTED_TO_SCORING_INPUT | gap=PROMOTED | stage=SCORING_ALLOWED | scored=SCORED_AVAILABLE | fix=Proceed through normal scoring, translator, board and prelock gates.
- IF Brommapojkarna vs Gais | promotion=PROMOTED_TO_SCORING_INPUT | gap=PROMOTED | stage=SCORING_ALLOWED | scored=SCORED_AVAILABLE | fix=Proceed through normal scoring, translator, board and prelock gates.
- Suduva Marijampole vs TransINVEST Vilnius | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Botafogo SP vs Avai | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Vila Nova vs São Bernardo | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Brusque vs Figueirense | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Brescia Clube vs Cardoso Moreira | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- CAAC Brasil vs Uniao Central | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Campos AA vs Tigres do Brasil | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- EC Resende vs Búzios | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Benjamín Aceval vs Deportivo Capiata | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Encarnación vs Guairena FC | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Universidad Catolica vs Mushuc Runa SC | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Bars vs Ilbirs | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Centro Español vs Mercedes | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Deportivo Muñiz vs Deportivo Español | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Sportivo Barracas vs Yupanqui | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Miramar vs Atenas | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Christos vs Loudoun 2 | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- FC Miami City vs Miami AC | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Lansing City vs Flint City Bucks | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Lorain County Leviathan vs Erie Sports Center | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Super Nova vs Ogre United | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Portugal vs Spain | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Keflavik vs Fram Reykjavik | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Concórdia U20 vs Joinville U20 | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Colwyn Bay vs Rhyl | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Cracovia Krakow vs Başakşehir | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- FK Partizan vs Neftchi Baku | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Sportfreunde Schwaig vs SSV Jahn Regensburg | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Defensores Glew vs Atletico Pilar | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Estrella de Berisso vs Juventud de Bernal | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
