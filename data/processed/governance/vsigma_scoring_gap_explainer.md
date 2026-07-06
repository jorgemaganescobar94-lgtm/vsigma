# vSIGMA Scoring Gap Explainer - 2026-07-06

## Summary
- rows_reviewed: 34
- missing_scored_rows: 2
- no_data_blocked_rows: 4
- not_trusted_rows: 26
- promoted_rows: 2
- gap_status_counts: NOT_TRUSTED_SKIPPED=26; SCORED_ROW_NO_DATA_BLOCKED=4; MISSING_SCORED_ROW=2; PROMOTED=2
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
- Brescia Clube vs Cardoso Moreira | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- CAAC Brasil vs Uniao Central | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Campos AA vs Tigres do Brasil | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- EC Resende vs Búzios | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Benjamín Aceval vs Deportivo Capiata | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Encarnación vs Guairena FC | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Universidad Catolica vs Mushuc Runa SC | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Bars vs Ilbirs | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Centro Español vs Mercedes | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Deportivo Muñiz vs Deportivo Español | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Sportivo Barracas vs Yupanqui | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Miramar vs Atenas | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Christos vs Loudoun 2 | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- FC Miami City vs Miami AC | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Lansing City vs Flint City Bucks | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Lorain County Leviathan vs Erie Sports Center | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Super Nova vs Ogre United | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Portugal vs Spain | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Keflavik vs Fram Reykjavik | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Concórdia U20 vs Joinville U20 | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Colwyn Bay vs Rhyl | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Cracovia Krakow vs Başakşehir | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- FK Partizan vs Neftchi Baku | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Sportfreunde Schwaig vs SSV Jahn Regensburg | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Defensores Glew vs Atletico Pilar | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Estrella de Berisso vs Juventud de Bernal | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
