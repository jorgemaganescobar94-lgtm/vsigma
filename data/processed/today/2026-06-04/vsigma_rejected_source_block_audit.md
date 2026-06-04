# vSIGMA Rejected Source Block Audit - 2026-06-04

## Summary
- rows_reviewed: 108
- rejected_rows: 108
- correct_reject_rows: 67
- manual_review_rows: 41
- whitelist_candidate_rows: 29
- audit_bucket_counts: CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=39; MANUAL_REVIEW_POSSIBLE_WHITELIST=29; CORRECT_REJECT_LOW_TIER_LOW_COVERAGE=17; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=12; CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=11
- review_priority_counts: P3_CORRECT_REJECT=67; P1_REVIEW_CANDIDATE=29; P2_REVIEW_LOW_CONFIDENCE=12
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Lebanon vs Yemen | league=Asian Cup - Qualification | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- FAR Rabat vs Difaa EL Jadida | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Hassania Agadir vs FUS Rabat | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- San Lorenzo vs Deportivo Riestra | league=Copa Argentina | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Bagé vs Brasil DE Pelotas | league=Copa Gaúcha | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Deportivo Santani vs Resistencia | league=Division Intermedia | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Paraguari AC vs Atlético Tembetary | league=Division Intermedia | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Colombe vs Unisport Bafang | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Fortuna Mfou vs Aigle Royal de Moungo | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- PWD Bamenda vs Canon | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Panthère vs Stade Renard | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Victoria United vs Jeunes Fauves | league=Elite One | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- AFC Eskilstuna vs Karlberg | league=Ettan - Norra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Laholm vs Hässleholms IF | league=Ettan - Södra | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Fortune vs BST Galaxy | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- GPA vs Dutch Lions | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Real de Banjul vs Falcons | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- TMT vs Bombada | league=GFA League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- PEPO vs Reipas | league=Kakkonen - Lohko A | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- ÅIFK vs P-Iirot | league=Kakkonen - Lohko B | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Cuniburo vs Cumbayá | league=Liga Pro Serie B | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- AS Camberene vs Jaraaf | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Ben Aknoun vs USM Alger | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Casa Sport vs DSC | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Gorée vs Stade de Mbour | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Guédiawaye vs Teungueth | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Génération Foot vs AJEL | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- HLM vs Pikine | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- La Linguère vs Wally Daan | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Ouakam vs Sonacos | league=Ligue 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Sao Luis vs Tupan | league=Maranhense - 2 | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Welayta Dicha vs Negelle Arsi | league=Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- ASKO vs Derby Academie | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Bakaridjan vs Stade Malien Bamako | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Mali Coura vs Bougouni | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- USFAS Bamako vs Onze Créateurs | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Real Potosí vs ABB | league=Primera División | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Kattaqurgon vs FarDu | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Respublika FA vs Qiziriq | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Shortan vs Metalourg | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Stocksund vs Stockholm Internazionale | league=Svenska Cupen | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
