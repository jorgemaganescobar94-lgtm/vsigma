# vSIGMA Scoring Gap Explainer - 2026-07-13

## Summary
- rows_reviewed: 35
- missing_scored_rows: 26
- no_data_blocked_rows: 2
- not_trusted_rows: 6
- promoted_rows: 1
- gap_status_counts: MISSING_SCORED_ROW=26; NOT_TRUSTED_SKIPPED=6; SCORED_ROW_NO_DATA_BLOCKED=2; PROMOTED=1
- next_action: Repair scoring/enrichment for trusted raw candidates; no market discussion until rows are scored and non-blocked.
- auto_apply: NO
- production_change: NO

## Gap Rows
- Ulsan Hyundai FC vs Jeonbuk Motors | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Gwangju FC vs Pohang Steelers | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Djurgardens IF vs Halmstad | promotion=PROMOTED_TO_SCORING_INPUT | gap=PROMOTED | stage=SCORING_ALLOWED | scored=SCORED_AVAILABLE | fix=Proceed through normal scoring, translator, board and prelock gates.
- America Mineiro vs Londrina | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- AO Itabaiana vs Brusque | promotion=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | gap=SCORED_ROW_NO_DATA_BLOCKED | stage=SCORING_ENRICHMENT_BLOCKED | scored=NO_DATA_BLOCKED | fix=Repair enrichment inputs for stats/odds/standings/coverage; do not promote until non-blocked.
- Vestri vs Fylkir | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Deportivo Capiata vs Atlético Tembetary | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Independiente F.b.c. vs Tacuary | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Maardu vs Tartu Welco | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Arsenal Tula vs Tekstilshchik | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Chelyabinsk vs Ska-khabarovsk | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Ural vs Torpedo Moskva | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Honka vs HJS Akatemia | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Reyady Abaseya vs Racing | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Claypole vs Leones de Rosario | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Fénix vs Sportivo Barracas | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Cerro Largo vs Defensor Sporting | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- La Luz vs Tacuarembo | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Paysandu vs Fenix | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- 9 de Julio Rafaela vs Defensores de Belgrano VR | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Breidablik vs Keflavik | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Singapore vs Laos W | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Vietnam vs Gangwon FC | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Gloggnitz vs SC Wiener Neustadt | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- HNK Gorica vs Göztepe | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- IFK Varnamo vs Naestved | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- NK Lokomotiva Zagreb vs Epitsentr Dunayivtsi | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Sigma Olomouc vs Shabab Al Ahli Dubai | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Wolfsberger AC vs Hradec Králové | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- Zenit vs Dinamo Makhachkala | promotion=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | gap=MISSING_SCORED_ROW | stage=SCORING_NOT_RUN_FOR_TRUSTED_RAW | scored=MISSING | fix=Run/repair scoring enrichment over trusted raw fixture candidates before market translation.
- XV de Piracicaba U20 vs Desportivo Brasil U20 | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Estudiantes Rio Cuarto 2 vs Defensa y Justicia Res. | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Ferro 2 vs Lanús Res. | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Gimnasia Mendoza 2 vs Sarmiento Res. | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.
- Quilmes 2 vs Central Córdoba SdE Res. | promotion=NOT_TRUSTED_NO_PROMOTION | gap=NOT_TRUSTED_SKIPPED | stage=RAW_TRUST_GATE_BLOCK | scored=MISSING | fix=Keep diagnostic only unless future whitelist changes source trust.

## Guardrails
- Scoring gap explainer is diagnostic only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Missing scored rows must be repaired upstream before translator/board discussion.
