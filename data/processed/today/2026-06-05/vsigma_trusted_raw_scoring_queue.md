# vSIGMA Trusted Raw Scoring Queue - 2026-06-05

## Summary
- queue_rows: 35
- priority_counts: P1_TRUSTED_MISSING_SCORING=19; P2_LOW_COVERAGE_SCORING=16
- scoring_needed_counts: YES=35
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Las Palmas vs Malaga | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Castellón vs Almeria | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | HK Kopavogur vs Afturelding | league=1. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | Njardvik vs IR Reykjavik | league=1. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #5 | P1_TRUSTED_MISSING_SCORING | Ægir vs Leiknir R. | league=1. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #6 | P1_TRUSTED_MISSING_SCORING | Hvíti riddarinn vs Haukar | league=2. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #7 | P1_TRUSTED_MISSING_SCORING | Kormákur / Hvöt vs Magni | league=2. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #8 | P1_TRUSTED_MISSING_SCORING | JS Kabylie vs CR Belouizdad | league=Ligue 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #9 | P1_TRUSTED_MISSING_SCORING | JS Saoura vs CS Constantine | league=Ligue 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #10 | P1_TRUSTED_MISSING_SCORING | MC Alger vs ASO Chlef | league=Ligue 1 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #11 | P1_TRUSTED_MISSING_SCORING | Guarulhos vs Paulínia FU | league=Paulista Série B | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #12 | P1_TRUSTED_MISSING_SCORING | Binga vs US Bougouba | league=Première Division | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #13 | P1_TRUSTED_MISSING_SCORING | Ituzaingó vs Real Pilar | league=Primera B Metropolitana | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #14 | P1_TRUSTED_MISSING_SCORING | Wanderers vs Danubio | league=Primera División - Apertura | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #15 | P1_TRUSTED_MISSING_SCORING | Sabadell vs Real Madrid II | league=Primera División RFEF - Play Offs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #16 | P1_TRUSTED_MISSING_SCORING | Plaza Colonia vs Sportivo Huracan | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #17 | P1_TRUSTED_MISSING_SCORING | Puerto Cabello II vs Zamora FC B | league=Segunda División | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #18 | P1_TRUSTED_MISSING_SCORING | Preston Lions vs Melbourne City II | league=Victoria NPL | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #19 | P2_LOW_COVERAGE_SCORING | Tatran Všechovice vs Brumov | league=4. liga - Divizie E | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #20 | P2_LOW_COVERAGE_SCORING | Angola vs Mauritania | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #21 | P2_LOW_COVERAGE_SCORING | Azerbaijan vs Malta | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #22 | P2_LOW_COVERAGE_SCORING | Benin vs Niger | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #23 | P2_LOW_COVERAGE_SCORING | Central African Republic vs Togo | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #24 | P2_LOW_COVERAGE_SCORING | Hungary vs Finland | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #25 | P2_LOW_COVERAGE_SCORING | Paraguay vs Nicaragua | league=Friendlies | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #26 | P2_LOW_COVERAGE_SCORING | Allerheiligen vs FSC Hochegger Dächer | league=Landesliga - Steiermark | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #27 | P2_LOW_COVERAGE_SCORING | Bruck an der Mur vs Union RB Weinland Gamlit | league=Landesliga - Steiermark | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #28 | P2_LOW_COVERAGE_SCORING | Ilz vs Köflach | league=Landesliga - Steiermark | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #29 | P2_LOW_COVERAGE_SCORING | Schladming vs Pachern | league=Landesliga - Steiermark | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #30 | P2_LOW_COVERAGE_SCORING | Gurten vs Weiz | league=Regionalliga - Mitte | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #31 | P2_LOW_COVERAGE_SCORING | Ried II vs SV Lafnitz | league=Regionalliga - Mitte | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #32 | P2_LOW_COVERAGE_SCORING | Voitsberg vs Wolfsberger AC II | league=Regionalliga - Mitte | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #33 | P2_LOW_COVERAGE_SCORING | Oberwart vs Krems / Rehberg | league=Regionalliga - Ost | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #34 | P2_LOW_COVERAGE_SCORING | TWL Elektra vs SV Horn | league=Regionalliga - Ost | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #35 | P1_TRUSTED_MISSING_SCORING | Estrella de Berisso vs Atletico Pilar | league=Torneo Promocional Amateur | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
