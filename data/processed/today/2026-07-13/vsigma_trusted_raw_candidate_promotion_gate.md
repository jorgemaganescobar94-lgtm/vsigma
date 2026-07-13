# vSIGMA Trusted Raw Candidate Promotion Gate - 2026-07-13

## Summary
- rows_reviewed: 35
- promoted_rows: 1
- blocked_rows: 2
- quarantine_rows: 26
- promotion_status_counts: TRUSTED_SOURCE_BUT_NO_SCORED_ROW=26; NOT_TRUSTED_NO_PROMOTION=6; TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED=2; PROMOTED_TO_SCORING_INPUT=1
- next_action: Promoted rows may feed normal scoring gates only.
- auto_apply: NO
- production_change: NO

## Rows
- Ulsan Hyundai FC vs Jeonbuk Motors | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Gwangju FC vs Pohang Steelers | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_api_enriched_fixture_results_refresh.csv
- Djurgardens IF vs Halmstad | status=PROMOTED_TO_SCORING_INPUT | allowed=SCORING_ALLOWED_WITH_NORMAL_GATES | reason=trusted source has matching scored row without blocking data warnings | source=data/processed/governance/vsigma_promoted_raw_fixture_candidates.csv
- America Mineiro vs Londrina | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- AO Itabaiana vs Brusque | status=TRUSTED_SOURCE_BUT_NO_DATA_BLOCKED | allowed=NO_PROMOTION_NO_BET | reason=matching scored row is NO_DATA_BLOCKED | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Vestri vs Fylkir | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Deportivo Capiata vs Atlético Tembetary | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Independiente F.b.c. vs Tacuary | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Maardu vs Tartu Welco | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Arsenal Tula vs Tekstilshchik | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Chelyabinsk vs Ska-khabarovsk | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Ural vs Torpedo Moskva | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Honka vs HJS Akatemia | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Reyady Abaseya vs Racing | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Claypole vs Leones de Rosario | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Fénix vs Sportivo Barracas | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Cerro Largo vs Defensor Sporting | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- La Luz vs Tacuarembo | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Paysandu vs Fenix | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- 9 de Julio Rafaela vs Defensores de Belgrano VR | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Breidablik vs Keflavik | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Singapore vs Laos W | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Vietnam vs Gangwon FC | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Gloggnitz vs SC Wiener Neustadt | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- HNK Gorica vs Göztepe | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- IFK Varnamo vs Naestved | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- NK Lokomotiva Zagreb vs Epitsentr Dunayivtsi | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Sigma Olomouc vs Shabab Al Ahli Dubai | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Wolfsberger AC vs Hradec Králové | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Zenit vs Dinamo Makhachkala | status=TRUSTED_SOURCE_BUT_NO_SCORED_ROW | allowed=WAIT_SCORING | reason=trusted raw candidate has no matching scored row | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- XV de Piracicaba U20 vs Desportivo Brasil U20 | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Estudiantes Rio Cuarto 2 vs Defensa y Justicia Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Ferro 2 vs Lanús Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Gimnasia Mendoza 2 vs Sarmiento Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv
- Quilmes 2 vs Central Córdoba SdE Res. | status=NOT_TRUSTED_NO_PROMOTION | allowed=DIAGNOSTIC_ONLY | reason=raw candidate is not TRUSTED_RAW_SOURCE | source=data/processed/governance/vsigma_raw_candidate_trust_gate.csv

## Guardrails
- Promotion gate can only restrict or route to normal scoring; it never creates picks or stake permission.
- TRUSTED_RAW_SOURCE is necessary but not sufficient for promotion.
- NO_DATA_BLOCKED scored rows cannot be promoted.
- Normal downstream gates remain mandatory even after promotion.
