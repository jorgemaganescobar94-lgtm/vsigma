# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-07-06

## Summary
- rows_reviewed: 34
- promoted_rows: 2
- blocked_rows: 4
- quarantine_rows: 2
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=26; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=4; TRUSTED_SOURCE_BUT_NO_SCORED_ROW=2; PROMOTED_TO_SCORING_INPUT=2
- next_action: Promoted rows may feed normal scoring gates only.
- auto_apply: NO
- production_change: NO

## Rows
- Degerfors IF vs Malmo FF | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Jeonbuk Motors vs Gangwon FC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- BK Hacken vs Djurgardens IF | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/matches_league_filtered.csv
- IF Brommapojkarna vs Gais | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/matches_league_filtered.csv
- Suduva Marijampole vs TransINVEST Vilnius | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- Botafogo SP vs Avai | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- Vila Nova vs São Bernardo | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- Brusque vs Figueirense | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- Brescia Clube vs Cardoso Moreira | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- CAAC Brasil vs Uniao Central | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Campos AA vs Tigres do Brasil | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- EC Resende vs Búzios | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Benjamín Aceval vs Deportivo Capiata | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Encarnación vs Guairena FC | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Universidad Catolica vs Mushuc Runa SC | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Bars vs Ilbirs | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Centro Español vs Mercedes | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Deportivo Muñiz vs Deportivo Español | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Sportivo Barracas vs Yupanqui | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Miramar vs Atenas | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Christos vs Loudoun 2 | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- FC Miami City vs Miami AC | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Lansing City vs Flint City Bucks | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Lorain County Leviathan vs Erie Sports Center | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Super Nova vs Ogre United | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Portugal vs Spain | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Keflavik vs Fram Reykjavik | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Concórdia U20 vs Joinville U20 | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Colwyn Bay vs Rhyl | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Cracovia Krakow vs Başakşehir | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- FK Partizan vs Neftchi Baku | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Sportfreunde Schwaig vs SSV Jahn Regensburg | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Defensores Glew vs Atletico Pilar | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Estrella de Berisso vs Juventud de Bernal | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
