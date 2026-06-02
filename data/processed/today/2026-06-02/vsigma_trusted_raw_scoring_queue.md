# vSIGMA Trusted Raw Scoring Queue - 2026-06-02

## Summary
- queue_rows: 44
- priority_counts: P1_TRUSTED_MISSING_SCORING=28; P2_LOW_COVERAGE_SCORING=16
- scoring_needed_counts: YES=44
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Ario Eslamshahr vs Shahrdari Noshahr | league=Azadegan League | scoring_needed=YES
- #2 | P1_TRUSTED_MISSING_SCORING | Fard Alborz vs Mes Kerman | league=Azadegan League | scoring_needed=YES
- #3 | P1_TRUSTED_MISSING_SCORING | Havadar vs Navad Urmia | league=Azadegan League | scoring_needed=YES
- #4 | P1_TRUSTED_MISSING_SCORING | Mes Shahr-e Babak vs Sanat Naft | league=Azadegan League | scoring_needed=YES
- #5 | P1_TRUSTED_MISSING_SCORING | Mes Soongoun vs Niroye Zamini | league=Azadegan League | scoring_needed=YES
- #6 | P1_TRUSTED_MISSING_SCORING | Naft Gachsaran vs Be'sat Kermanshah | league=Azadegan League | scoring_needed=YES
- #7 | P1_TRUSTED_MISSING_SCORING | Nassaji Mazandaran vs Damash Gilanian | league=Azadegan League | scoring_needed=YES
- #8 | P1_TRUSTED_MISSING_SCORING | Pars Jonoubi JAM vs Naft Bandar Abbas | league=Azadegan League | scoring_needed=YES
- #9 | P1_TRUSTED_MISSING_SCORING | Shenavarsazi Qeshm vs Saipa | league=Azadegan League | scoring_needed=YES
- #10 | P1_TRUSTED_MISSING_SCORING | Mangasport vs Bitam | league=Championnat D1 | scoring_needed=YES
- #11 | P1_TRUSTED_MISSING_SCORING | US Oyem vs Lozo | league=Championnat D1 | scoring_needed=YES
- #12 | P1_TRUSTED_MISSING_SCORING | Vautour Club vs Ogooue FC | league=Championnat D1 | scoring_needed=YES
- #13 | P1_TRUSTED_MISSING_SCORING | Independiente Medellin vs Cucuta | league=Copa Colombia | scoring_needed=YES
- #14 | P1_TRUSTED_MISSING_SCORING | Assyriska FF vs Enköping | league=Ettan - Norra | scoring_needed=YES
- #15 | P1_TRUSTED_MISSING_SCORING | Rosengård vs Angelholms FF | league=Ettan - Södra | scoring_needed=YES
- #16 | P1_TRUSTED_MISSING_SCORING | Olimpia Grudziądz vs Sandecja Nowy Sącz | league=II Liga - East | scoring_needed=YES
- #17 | P1_TRUSTED_MISSING_SCORING | Al Kahrabaa vs Al-Karma | league=Iraqi League | scoring_needed=YES
- #18 | P1_TRUSTED_MISSING_SCORING | Al Quwa Al Jawiya vs Zakho | league=Iraqi League | scoring_needed=YES
- #19 | P1_TRUSTED_MISSING_SCORING | Al Shorta vs Al Minaa Basra | league=Iraqi League | scoring_needed=YES
- #20 | P1_TRUSTED_MISSING_SCORING | Erbil vs Baghdad | league=Iraqi League | scoring_needed=YES
- #21 | P1_TRUSTED_MISSING_SCORING | Gharraf vs Naft Maysan | league=Iraqi League | scoring_needed=YES
- #22 | P1_TRUSTED_MISSING_SCORING | USM Alger vs CR Belouizdad | league=Ligue 1 | scoring_needed=YES
- #23 | P1_TRUSTED_MISSING_SCORING | Afrique Football Élite vs Diarra | league=Première Division | scoring_needed=YES
- #24 | P1_TRUSTED_MISSING_SCORING | Djoliba vs Binga | league=Première Division | scoring_needed=YES
- #25 | P1_TRUSTED_MISSING_SCORING | Deportivo Merlo vs Deportivo Laferrere | league=Primera B Metropolitana | scoring_needed=YES
- #26 | P1_TRUSTED_MISSING_SCORING | Union Brescia vs Ascoli | league=Serie C - Promotion - Play-offs | scoring_needed=YES
- #27 | P1_TRUSTED_MISSING_SCORING | Al-Hilal Omdurman II vs Al Ahli Wad Medani | league=Sudani Premier League | scoring_needed=YES
- #28 | P1_TRUSTED_MISSING_SCORING | Hilal El-Fasher vs Al Fallah | league=Sudani Premier League | scoring_needed=YES
- #29 | P2_LOW_COVERAGE_SCORING | Hudiksvall vs Friska Viljor | league=Svenska Cupen | scoring_needed=YES
- #30 | P2_LOW_COVERAGE_SCORING | Sävedalen vs Böljan | league=Svenska Cupen | scoring_needed=YES
- #31 | P2_LOW_COVERAGE_SCORING | Vastkurd vs Trollhättan | league=Svenska Cupen | scoring_needed=YES
- #32 | P2_LOW_COVERAGE_SCORING | New Jersey Copa vs Cedar Stars Rush | league=USL League Two | scoring_needed=YES
- #33 | P2_LOW_COVERAGE_SCORING | Vermont Green vs Boston Bolts | league=USL League Two | scoring_needed=YES
- #34 | P1_TRUSTED_MISSING_SCORING | JJK vs VJS | league=Ykkönen | scoring_needed=YES
- #35 | P1_TRUSTED_MISSING_SCORING | Rops vs OLS | league=Ykkönen | scoring_needed=YES
- #36 | P2_LOW_COVERAGE_SCORING | Mariánské Lázně vs Karlovy Vary | league=4. liga - Divizie B | scoring_needed=YES
- #37 | P2_LOW_COVERAGE_SCORING | Nové Sady vs Sokol Lanžhot | league=4. liga - Divizie E | scoring_needed=YES
- #38 | P2_LOW_COVERAGE_SCORING | Croatia vs Belgium | league=Friendlies | scoring_needed=YES
- #39 | P2_LOW_COVERAGE_SCORING | Georgia vs Romania | league=Friendlies | scoring_needed=YES
- #40 | P2_LOW_COVERAGE_SCORING | Morocco vs Madagascar | league=Friendlies | scoring_needed=YES
- #41 | P2_LOW_COVERAGE_SCORING | Wales vs Ghana | league=Friendlies | scoring_needed=YES
- #42 | P2_LOW_COVERAGE_SCORING | Korneuburg vs Ybbs | league=Landesliga - Niederosterreich | scoring_needed=YES
- #43 | P2_LOW_COVERAGE_SCORING | Blau-Weiß Feldkirch vs FC Egg | league=Landesliga - Vorarlbergliga | scoring_needed=YES
- #44 | P2_LOW_COVERAGE_SCORING | Greuther Fürth II vs Cham | league=Regionalliga - Bayern | scoring_needed=YES

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
