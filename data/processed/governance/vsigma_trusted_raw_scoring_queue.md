# vSIGMA Trusted Raw Scoring Queue - 2026-07-09

## Summary
- queue_rows: 29
- priority_counts: P2_LOW_COVERAGE_SCORING=16; P1_TRUSTED_MISSING_SCORING=13
- scoring_needed_counts: YES=29
- source_gap_status: MISSING_SCORED_ROW
- next_action: Use this queue as the explicit input list for a future scoring/enrichment repair stage. Do not create picks from queue rows.
- auto_apply: NO
- production_change: NO

## Queue Rows
- #1 | P1_TRUSTED_MISSING_SCORING | ML Vitebsk vs Universitatea Craiova | league=UEFA Champions League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #2 | P1_TRUSTED_MISSING_SCORING | Petrocub vs Egnatia Rrogozhinë | league=UEFA Champions League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #3 | P1_TRUSTED_MISSING_SCORING | Zira vs Torpedo Kutaisi | league=UEFA Europa Conference League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #4 | P1_TRUSTED_MISSING_SCORING | Akademiya Ontustik vs Arys | league=1. Division | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #5 | P1_TRUSTED_MISSING_SCORING | Aktobe Jas vs Khan Tengri | league=1. Division | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #6 | P1_TRUSTED_MISSING_SCORING | Jaiyq vs Tobol 2 | league=1. Division | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #7 | P1_TRUSTED_MISSING_SCORING | Atletico Grau vs Carlos A. Mannucci | league=Copa De La Liga | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #8 | P1_TRUSTED_MISSING_SCORING | Maardu vs Flora II | league=Esiliiga A | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #9 | P1_TRUSTED_MISSING_SCORING | Musa vs GrIFK | league=Kakkonen - Lohko B | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #10 | P1_TRUSTED_MISSING_SCORING | Deportivo Cuenca Juniors vs LDU Portoviejo | league=Liga Pro Serie B | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #11 | P1_TRUSTED_MISSING_SCORING | Hardrock vs Dynamos | league=Premier Soccer League | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #12 | P1_TRUSTED_MISSING_SCORING | Izhevsk vs Dinamo Barnaul | league=Second League - Group 4 | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #13 | P2_LOW_COVERAGE_SCORING | Dayton Dutch Lions vs West Virginia Alliance | league=USL League Two | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #14 | P1_TRUSTED_MISSING_SCORING | France vs Morocco | league=World Cup | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #15 | P2_LOW_COVERAGE_SCORING | Benrath vs Fortuna Düsseldorf | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #16 | P2_LOW_COVERAGE_SCORING | CFR 1907 Cluj vs Karpaty | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #17 | P2_LOW_COVERAGE_SCORING | Chemnitzer FC vs Union Berlin | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #18 | P2_LOW_COVERAGE_SCORING | Cracovia Krakow vs Pardubice | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #19 | P2_LOW_COVERAGE_SCORING | Debreceni VSC vs Železničar Pančevo | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #20 | P2_LOW_COVERAGE_SCORING | FC Ingolstadt 04 vs Lask Linz | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #21 | P2_LOW_COVERAGE_SCORING | H&W Welders vs Dergview | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #22 | P2_LOW_COVERAGE_SCORING | Karlsruher SC vs SGV Freiberg | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #23 | P2_LOW_COVERAGE_SCORING | Korona Kielce vs Omonia Nicosia | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #24 | P2_LOW_COVERAGE_SCORING | OFK Beograd vs Buducnost Podgorica | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #25 | P2_LOW_COVERAGE_SCORING | Polessya vs Jagiellonia | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #26 | P2_LOW_COVERAGE_SCORING | Rapid vs Slovan Liberec | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #27 | P2_LOW_COVERAGE_SCORING | Red Bull Salzburg vs Metalist 1925 Kharkiv | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #28 | P2_LOW_COVERAGE_SCORING | Rennes vs Caen | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row
- #29 | P2_LOW_COVERAGE_SCORING | SV Wehen vs FC 08 Homburg | league=Friendlies Clubs | scoring_needed=YES | reason=trusted raw candidate has no matching scored row

## Guardrails
- This queue is diagnostic/planning only.
- It does not call APIs, create picks, create stake permission, or bypass gates.
- Queue rows must pass future scoring, enrichment, translator, board and prelock gates before any market discussion.
