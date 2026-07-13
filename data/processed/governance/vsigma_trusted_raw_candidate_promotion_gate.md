# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-07-13

## Summary
- rows_reviewed: 35
- promoted_rows: 1
- blocked_rows: 2
- quarantine_rows: 2
- promotion_status_counts: NOT_TRUSTED_NO_PROMOTION=30; TRUSTED_SOURCE_BUT_NO_SCORED_ROW=2; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=2; PROMOTED_TO_SCORING_INPUT=1
- next_action: Promoted rows may feed normal scoring gates only.
- auto_apply: NO
- production_change: NO

## Rows
- Ulsan Hyundai FC vs Jeonbuk Motors | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Gwangju FC vs Pohang Steelers | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Djurgardens IF vs Halmstad | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/matches_league_filtered.csv
- America Mineiro vs Londrina | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- AO Itabaiana vs Brusque | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/matches_league_filtered.csv
- Vestri vs Fylkir | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Deportivo Capiata vs Atlético Tembetary | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Independiente F.b.c. vs Tacuary | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Maardu vs Tartu Welco | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Arsenal Tula vs Tekstilshchik | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Chelyabinsk vs Ska-khabarovsk | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Ural vs Torpedo Moskva | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Honka vs HJS Akatemia | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Reyady Abaseya vs Racing | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Claypole vs Leones de Rosario | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Fénix vs Sportivo Barracas | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Cerro Largo vs Defensor Sporting | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- La Luz vs Tacuarembo | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Paysandu vs Fenix | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- 9 de Julio Rafaela vs Defensores de Belgrano VR | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Breidablik vs Keflavik | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Singapore vs Laos W | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Vietnam vs Gangwon FC | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Gloggnitz vs SC Wiener Neustadt | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- HNK Gorica vs Göztepe | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- IFK Varnamo vs Naestved | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- NK Lokomotiva Zagreb vs Epitsentr Dunayivtsi | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Sigma Olomouc vs Shabab Al Ahli Dubai | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Wolfsberger AC vs Hradec Králové | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Zenit vs Dinamo Makhachkala | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- XV de Piracicaba U20 vs Desportivo Brasil U20 | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Estudiantes Rio Cuarto 2 vs Defensa y Justicia Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Ferro 2 vs Lanús Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Gimnasia Mendoza 2 vs Sarmiento Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv
- Quilmes 2 vs Central Córdoba SdE Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/matches_league_rejected.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
