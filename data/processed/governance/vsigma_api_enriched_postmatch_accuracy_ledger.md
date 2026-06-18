# vSIGMA API-Enriched Postmatch Accuracy Ledger - 2026-06-18

## Summary
- rows_reviewed: 35
- finished_rows: 17
- pending_rows: 18
- accuracy_bucket_counts: PENDING_RESULT=18; PARTIAL_SIGNAL_VALIDATED=8; STRONG_SIGNAL_VALIDATED=6; SIGNAL_FAILED=3
- api_1x2_counts: PENDING_RESULT=18; MISS=11; HIT=6
- api_double_chance_counts: PENDING_RESULT=18; HIT=13; MISS=4
- api_dnb_counts: PENDING_RESULT=18; VOID=7; HIT=6; MISS=4
- over_1_5_counts: PENDING_RESULT=18; HIT=15; MISS=2
- over_2_5_counts: PENDING_RESULT=18; MISS=10; HIT=7
- under_3_5_counts: PENDING_RESULT=18; HIT=15; MISS=2
- btts_counts: PENDING_RESULT=18; HIT=11; MISS=6
- pick_permission_counts: NO_PICK_PERMISSION=35
- stake_permission_counts: NO_STAKE_PERMISSION=35
- next_action: Use this ledger to calibrate signal buckets after results are final. Do not promote picks or stake from it.
- auto_apply: NO
- production_change: NO

## Evaluated Rows
- Indy Eleven vs Brooklyn | result=pending | prediction=Indy Eleven | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- FC Tulsa vs Monterey Bay | result=2-0 | prediction=FC Tulsa | side=HOME | signal=97 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Forward Madison vs Fort Wayne | result=1-1 | prediction=Forward Madison | side=HOME | signal=66 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Khovd Western vs Khangarid | result=1-2 | prediction=Khangarid | side=AWAY | signal=96 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Khovd vs Deren | result=0-6 | prediction=Deren | side=AWAY | signal=90 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=MISS | btts=MISS | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Akademiya Ontustik vs Yelimay Semey 2 | result=1-1 | prediction=Akademiya Ontustik | side=HOME | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- JKT Tanzania vs Tanzania Prisons | result=0-1 | prediction=JKT Tanzania | side=HOME | signal=64 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=MISS | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=SIGNAL_FAILED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Pamba Jiji vs Mtibwa Sugar | result=4-0 | prediction=Mtibwa Sugar | side=AWAY | signal=76 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=HIT | o2.5=HIT | u3.5=MISS | btts=MISS | bucket=SIGNAL_FAILED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Fountain Gate vs Young Africans | result=0-2 | prediction=Young Africans | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Arys vs Kaspij Aktau 2 | result=1-2 | prediction=Kaspij Aktau 2 | side=AWAY | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Meshakhte vs Gagra | result=1-1 | prediction=Gagra | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Renaissance Berkane vs Olympique Safi | result=0-0 | prediction=Renaissance Berkane | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=MISS | o2.5=MISS | u3.5=HIT | btts=MISS | bucket=SIGNAL_FAILED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Olympique Dcheïra vs FAR Rabat | result=1-1 | prediction=FAR Rabat | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Wydad AC vs FUS Rabat | result=1-2 | prediction=Wydad AC | side=HOME | signal=73 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Yacoub El Mansour vs Hassania Agadir | result=2-1 | prediction=Hassania Agadir | side=AWAY | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=MISS | dnb=MISS | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Turan Turkistan vs Aktobe Jas | result=pending | prediction=Turan Turkistan | side=HOME | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Bamboutos vs Bafmeng United | result=pending | prediction=Bamboutos | side=HOME | signal=70 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Tonnerre vs Yafoot | result=1-1 | prediction=Tonnerre | side=HOME | signal=67 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Union Douala vs Sable | result=1-1 | prediction=Sable | side=AWAY | signal=65 MEDIUM_SIGNAL_REVIEW | 1x2=MISS | dc=HIT | dnb=VOID | o1.5=HIT | o2.5=MISS | u3.5=HIT | btts=HIT | bucket=PARTIAL_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Dinamo Tbilisi vs Samgurali | result=pending | prediction=Dinamo Tbilisi | side=HOME | signal=65 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Elva vs Viimsi | result=pending | prediction=Viimsi | side=AWAY | signal=75 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Johvi Phoenix vs Legion | result=pending | prediction=Johvi Phoenix | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Luunja vs JK Tabasalu | result=pending | prediction=Luunja | side=HOME | signal=90 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Eskilsminne vs Trollhättan | result=pending | prediction=Eskilsminne | side=HOME | signal=62 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Jonkopings Sodra vs Lund | result=pending | prediction=Jonkopings Sodra | side=HOME | signal=89 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Skövde AIK vs Hässleholms IF | result=pending | prediction=Hässleholms IF | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Trelleborg vs Rosengård | result=pending | prediction=Trelleborg | side=HOME | signal=58 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Tvååker vs Angelholms FF | result=pending | prediction=Angelholms FF | side=AWAY | signal=64 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Gefle IF vs Stockholm Internazionale | result=pending | prediction=Stockholm Internazionale | side=AWAY | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Hammarby Talang vs Järfälla | result=pending | prediction=Hammarby Talang | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Vasalund vs Karlberg | result=pending | prediction=Vasalund | side=HOME | signal=100 HIGH_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Arlanda vs Stocksund | result=pending | prediction=Stocksund | side=AWAY | signal=58 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Sollentuna vs FBK Karlstad | result=pending | prediction=Sollentuna | side=HOME | signal=69 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- AC Oulu vs Mariehamn | result=2-1 | prediction=AC Oulu | side=HOME | signal=94 HIGH_SIGNAL_REVIEW | 1x2=HIT | dc=HIT | dnb=HIT | o1.5=HIT | o2.5=HIT | u3.5=HIT | btts=HIT | bucket=STRONG_SIGNAL_VALIDATED | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION
- Fransta vs Friska Viljor | result=pending | prediction=Friska Viljor | side=AWAY | signal=62 MEDIUM_SIGNAL_REVIEW | 1x2=PENDING_RESULT | dc=PENDING_RESULT | dnb=PENDING_RESULT | o1.5=PENDING_RESULT | o2.5=PENDING_RESULT | u3.5=PENDING_RESULT | btts=PENDING_RESULT | bucket=PENDING_RESULT | pick=NO_PICK_PERMISSION | stake=NO_STAKE_PERMISSION

## Guardrails
- This ledger is postmatch calibration only.
- It does not create picks, stake, canonical board permission, or whitelist permission.
- Historical promotion rules must be implemented separately after enough sample size exists.
