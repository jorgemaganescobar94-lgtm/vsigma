# vSIGMA Rejected Source Block Audit - 2026-06-08

## Summary
- rows_reviewed: 70
- rejected_rows: 70
- correct_reject_rows: 34
- manual_review_rows: 36
- whitelist_candidate_rows: 13
- audit_bucket_counts: CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=30; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=23; MANUAL_REVIEW_POSSIBLE_WHITELIST=13; CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=3; CORRECT_REJECT_LOW_TIER_LOW_COVERAGE=1
- review_priority_counts: P3_CORRECT_REJECT=34; P2_REVIEW_LOW_CONFIDENCE=23; P1_REVIEW_CANDIDATE=13
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Dainava vs Garliava | league=1 Lyga | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- FUS Rabat vs Difaa EL Jadida | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Olympique Dcheïra vs Hassania Agadir | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Renaissance Berkane vs Ittihad Tanger | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Wydad AC vs Olympique Safi | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Búzios vs Cardoso Moreira | league=Carioca C | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Ceres vs Tigres do Brasil | league=Carioca C | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Uni Souza vs Barcelona RJ | league=Carioca C | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Monsoon vs Santa Cruz RS | league=Copa Gaúcha | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- 3 de Noviembre vs General Caballero | league=Division Intermedia | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Encarnación vs SOL DE America | league=Division Intermedia | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Aigle Royal vs Gazelle | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Dynamo de Douala vs Cotonsport | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Jeunes Fauves vs Aigle Royal de Moungo | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Panthère vs Victoria United | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Stade Renard vs Unisport Bafang | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Foncha ST vs Tonnerre | league=Elite Two | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Sable vs Bafmeng United | league=Elite Two | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Järfälla vs Stocksund | league=Ettan - Norra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Stockholm Internazionale vs Vasalund | league=Ettan - Norra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Angelholms FF vs Olympic | league=Ettan - Södra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Utsikten vs Rosengård | league=Ettan - Södra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Baghdad vs Karbala | league=Iraqi League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Kiffen vs PuiU Helsinki | league=Kakkonen - Lohko A | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Enppi vs AL Masry | league=League Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Masr vs Wadi Degla | league=League Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Mamoré vs Uberaba | league=Mineiro - 2 | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Atletico Nacional vs Junior | league=Primera A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- UAI Urquiza vs Liniers | league=Primera B Metropolitana | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Berazategui vs Juventud Unida | league=Primera C | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Blooming vs Gualberto Villarroel SJ | league=Primera División | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Liverpool Montevideo vs Cerro Largo | league=Primera División - Apertura | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Jayxun vs Aral | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Metalourg vs FarDu | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Provincial Ovalle vs Trasandino | league=Segunda División | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Kooteepee vs Haka | league=Ykkösliiga | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
