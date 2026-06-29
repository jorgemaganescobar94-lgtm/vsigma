# vSIGMA Trusted Raw Scoring Queue - 2026-06-29

## Summary
- queue_rows: 32
- priority_counts: P1_TRUSTED_MISSING_SCORING=23; P2_LOW_COVERAGE_SCORING=9
- scoring_needed_counts: YES=32
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | Afturelding vs Ægir | league=1. Deild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Cavalry FC vs Supra du Quebec | league=Canadian Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Deportivo Garcilaso vs Deportivo Binacional | league=Copa De La Liga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | FBC Melgar vs UCV Moquegua | league=Copa De La Liga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #5 | P1_TRUSTED_MISSING_SCORING | B68 vs AB | league=Meistaradeildin | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #6 | P1_TRUSTED_MISSING_SCORING | HB Torshavn vs Skála | league=Meistaradeildin | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #7 | P1_TRUSTED_MISSING_SCORING | Vikingur Gota vs NSI Runavik | league=Meistaradeildin | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #8 | P1_TRUSTED_MISSING_SCORING | Gol Gohar vs Chadormalu SC | league=Persian Gulf Pro League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #9 | P1_TRUSTED_MISSING_SCORING | Al Arabi vs Al Fahaheel | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #10 | P1_TRUSTED_MISSING_SCORING | Al Mabarrah vs Al Ansar | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #11 | P1_TRUSTED_MISSING_SCORING | Al Nejmeh vs Racing | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #12 | P1_TRUSTED_MISSING_SCORING | Al Qadsia vs Al Kuwait | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #13 | P1_TRUSTED_MISSING_SCORING | Kazma vs Al Salmiyah | league=Premier League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #14 | P1_TRUSTED_MISSING_SCORING | Fénix vs General Lamadrid | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #15 | P1_TRUSTED_MISSING_SCORING | Sportivo Barracas vs Lujan | league=Primera C | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #16 | P1_TRUSTED_MISSING_SCORING | Democrata GV vs Ivinhema | league=Serie D | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #17 | P2_LOW_COVERAGE_SCORING | Asheville City vs Charlotte Independence 2 | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #18 | P1_TRUSTED_MISSING_SCORING | Auda vs Riga | league=Virsliga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #19 | P1_TRUSTED_MISSING_SCORING | FS Jelgava vs Grobiņa | league=Virsliga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #20 | P1_TRUSTED_MISSING_SCORING | Brazil vs Japan | league=World Cup | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #21 | P1_TRUSTED_MISSING_SCORING | Germany vs Paraguay | league=World Cup | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #22 | P1_TRUSTED_MISSING_SCORING | VJS vs TPV | league=Ykkönen | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #23 | P1_TRUSTED_MISSING_SCORING | IA Akranes vs Fram Reykjavik | league=Úrvalsdeild | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #24 | P2_LOW_COVERAGE_SCORING | Akhmat vs Borac Banja Luka | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #25 | P2_LOW_COVERAGE_SCORING | Arges Pitesti vs Vllaznia Shkodër | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #26 | P2_LOW_COVERAGE_SCORING | CSKA 1948 vs FK Partizan | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #27 | P2_LOW_COVERAGE_SCORING | FK Crvena Zvezda vs Slovan Bratislava | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #28 | P2_LOW_COVERAGE_SCORING | H&W Welders vs Larne | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #29 | P2_LOW_COVERAGE_SCORING | Nizhny Novgorod vs Tekstilshchik | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #30 | P2_LOW_COVERAGE_SCORING | Odense vs Kolding IF | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #31 | P2_LOW_COVERAGE_SCORING | Universitatea Craiova vs Polessya | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #32 | P1_TRUSTED_MISSING_SCORING | Juventud de Bernal vs Deportivo Metalurgico | league=Torneo Promocional Amateur | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
