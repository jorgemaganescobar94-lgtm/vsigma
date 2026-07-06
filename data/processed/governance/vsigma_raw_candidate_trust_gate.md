# vSIGMA Raw Candidate Trust Gate - 2026-07-06

## Summary
- rows_reviewed: 34
- trusted_rows: 8
- quarantine_rows: 0
- blocked_rows: 26
- trust_status_counts: REJECTED_SOURCE_BLOCK=26; TRUSTED_RAW_SOURCE=8
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.
- auto_apply: NO
- production_change: NO

## Rows
- Degerfors IF vs Malmo FF | league=Allsvenskan | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Jeonbuk Motors vs Gangwon FC | league=K League 1 | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- BK Hacken vs Djurgardens IF | league=Allsvenskan | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- IF Brommapojkarna vs Gais | league=Allsvenskan | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Suduva Marijampole vs TransINVEST Vilnius | league=A Lyga | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Botafogo SP vs Avai | league=Serie B | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Vila Nova vs São Bernardo | league=Serie B | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Brusque vs Figueirense | league=Serie C | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Brescia Clube vs Cardoso Moreira | league=Carioca C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- CAAC Brasil vs Uniao Central | league=Carioca C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Campos AA vs Tigres do Brasil | league=Carioca C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- EC Resende vs Búzios | league=Carioca C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Benjamín Aceval vs Deportivo Capiata | league=Division Intermedia | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Encarnación vs Guairena FC | league=Division Intermedia | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Universidad Catolica vs Mushuc Runa SC | league=Liga Pro | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Bars vs Ilbirs | league=Premier League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Centro Español vs Mercedes | league=Primera C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Deportivo Muñiz vs Deportivo Español | league=Primera C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Sportivo Barracas vs Yupanqui | league=Primera C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Miramar vs Atenas | league=Segunda División | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Christos vs Loudoun 2 | league=USL League Two | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- FC Miami City vs Miami AC | league=USL League Two | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Lansing City vs Flint City Bucks | league=USL League Two | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Lorain County Leviathan vs Erie Sports Center | league=USL League Two | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Super Nova vs Ogre United | league=Virsliga | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Portugal vs Spain | league=World Cup | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Keflavik vs Fram Reykjavik | league=Úrvalsdeild | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Concórdia U20 vs Joinville U20 | league=Catarinense U20 | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Colwyn Bay vs Rhyl | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Cracovia Krakow vs Başakşehir | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- FK Partizan vs Neftchi Baku | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Sportfreunde Schwaig vs SSV Jahn Regensburg | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Defensores Glew vs Atletico Pilar | league=Torneo Promocional Amateur | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Estrella de Berisso vs Juventud de Bernal | league=Torneo Promocional Amateur | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv

## Guardrails
- Trust gate is defensive and can only restrict downstream use.
- Rejected source rows cannot feed scoring without explicit future whitelist.
- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.
- No bets, stakes, secrets, API calls, or safety gates are changed.
