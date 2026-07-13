# vSIGMA Raw Candidate Trust Gate - 2026-07-13

## Summary
- rows_reviewed: 35
- trusted_rows: 5
- quarantine_rows: 0
- blocked_rows: 30
- trust_status_counts: REJECTED_SOURCE_BLOCK=30; TRUSTED_RAW_SOURCE=5
- next_action: Only TRUSTED_RAW_SOURCE rows may be considered for scoring; quarantine/rejected rows remain diagnostic only.
- auto_apply: NO
- production_change: NO

## Rows
- Ulsan Hyundai FC vs Jeonbuk Motors | league=K League 1 | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Gwangju FC vs Pohang Steelers | league=K League 1 | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Djurgardens IF vs Halmstad | league=Allsvenskan | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- America Mineiro vs Londrina | league=Serie B | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- AO Itabaiana vs Brusque | league=Serie C | status=TRUSTED_RAW_SOURCE | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=source is not rejected and competition is not low-trust by token gate | source=data/processed/matches_league_filtered.csv
- Vestri vs Fylkir | league=1. Deild | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Deportivo Capiata vs Atlético Tembetary | league=Division Intermedia | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Independiente F.b.c. vs Tacuary | league=Division Intermedia | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Maardu vs Tartu Welco | league=Esiliiga A | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Arsenal Tula vs Tekstilshchik | league=First League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Chelyabinsk vs Ska-khabarovsk | league=First League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Ural vs Torpedo Moskva | league=First League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Honka vs HJS Akatemia | league=Kakkonen - Lohko B | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Reyady Abaseya vs Racing | league=Premier League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Claypole vs Leones de Rosario | league=Primera C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Fénix vs Sportivo Barracas | league=Primera C | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Cerro Largo vs Defensor Sporting | league=Primera División - Apertura | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- La Luz vs Tacuarembo | league=Segunda División | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Paysandu vs Fenix | league=Segunda División | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- 9 de Julio Rafaela vs Defensores de Belgrano VR | league=Torneo Federal A | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Breidablik vs Keflavik | league=Úrvalsdeild | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Singapore vs Laos W | league=Asean Championship Women | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Vietnam vs Gangwon FC | league=Friendlies | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Gloggnitz vs SC Wiener Neustadt | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- HNK Gorica vs Göztepe | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- IFK Varnamo vs Naestved | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- NK Lokomotiva Zagreb vs Epitsentr Dunayivtsi | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Sigma Olomouc vs Shabab Al Ahli Dubai | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Wolfsberger AC vs Hradec Králové | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Zenit vs Dinamo Makhachkala | league=Friendlies Clubs | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- XV de Piracicaba U20 vs Desportivo Brasil U20 | league=Paulista - U20 | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Estudiantes Rio Cuarto 2 vs Defensa y Justicia Res. | league=Reserve League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Ferro 2 vs Lanús Res. | league=Reserve League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Gimnasia Mendoza 2 vs Sarmiento Res. | league=Reserve League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv
- Quilmes 2 vs Central Córdoba SdE Res. | league=Reserve League | status=REJECTED_SOURCE_BLOCK | allowed=DIAGNOSTIC_ONLY_NO_SCORING | reason=source path indicates the fixture came from rejected league/filter output | source=data/processed/matches_league_rejected.csv

## Guardrails
- Trust gate is defensive and can only restrict downstream use.
- Rejected source rows cannot feed scoring without explicit future whitelist.
- Youth/women/reserve/academy rows remain quarantine-only unless explicitly whitelisted.
- No bets, stakes, secrets, API calls, or safety gates are changed.
