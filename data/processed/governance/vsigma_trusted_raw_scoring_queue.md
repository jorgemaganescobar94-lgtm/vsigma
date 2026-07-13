# vSIGMA Trusted Raw Scoring Queue - 2026-07-13

## Summary
- queue_rows: 26
- priority_counts: P1_TRUSTED_MISSING_SCORING=18; P2_LOW_COVERAGE_SCORING=8
- scoring_needed_counts: YES=26
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Ulsan Hyundai FC vs Jeonbuk Motors | league=K League 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Gwangju FC vs Pohang Steelers | league=K League 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Vestri vs Fylkir | league=1. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | Deportivo Capiata vs Atlético Tembetary | league=Division Intermedia | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #5 | P1_TRUSTED_MISSING_SCORING | Independiente F.b.c. vs Tacuary | league=Division Intermedia | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #6 | P1_TRUSTED_MISSING_SCORING | Maardu vs Tartu Welco | league=Esiliiga A | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #7 | P1_TRUSTED_MISSING_SCORING | Arsenal Tula vs Tekstilshchik | league=First League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #8 | P1_TRUSTED_MISSING_SCORING | Chelyabinsk vs Ska-khabarovsk | league=First League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #9 | P1_TRUSTED_MISSING_SCORING | Ural vs Torpedo Moskva | league=First League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #10 | P1_TRUSTED_MISSING_SCORING | Honka vs HJS Akatemia | league=Kakkonen - Lohko B | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #11 | P1_TRUSTED_MISSING_SCORING | Reyady Abaseya vs Racing | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #12 | P1_TRUSTED_MISSING_SCORING | Claypole vs Leones de Rosario | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #13 | P1_TRUSTED_MISSING_SCORING | Fénix vs Sportivo Barracas | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #14 | P1_TRUSTED_MISSING_SCORING | Cerro Largo vs Defensor Sporting | league=Primera División - Apertura | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #15 | P1_TRUSTED_MISSING_SCORING | La Luz vs Tacuarembo | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #16 | P1_TRUSTED_MISSING_SCORING | Paysandu vs Fenix | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #17 | P1_TRUSTED_MISSING_SCORING | 9 de Julio Rafaela vs Defensores de Belgrano VR | league=Torneo Federal A | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #18 | P1_TRUSTED_MISSING_SCORING | Breidablik vs Keflavik | league=Úrvalsdeild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #19 | P2_LOW_COVERAGE_SCORING | Vietnam vs Gangwon FC | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #20 | P2_LOW_COVERAGE_SCORING | Gloggnitz vs SC Wiener Neustadt | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #21 | P2_LOW_COVERAGE_SCORING | HNK Gorica vs Göztepe | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #22 | P2_LOW_COVERAGE_SCORING | IFK Varnamo vs Naestved | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #23 | P2_LOW_COVERAGE_SCORING | NK Lokomotiva Zagreb vs Epitsentr Dunayivtsi | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #24 | P2_LOW_COVERAGE_SCORING | Sigma Olomouc vs Shabab Al Ahli Dubai | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #25 | P2_LOW_COVERAGE_SCORING | Wolfsberger AC vs Hradec Králové | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #26 | P2_LOW_COVERAGE_SCORING | Zenit vs Dinamo Makhachkala | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
