# vSIGMA Rejected Source Block Audit - 2026-06-09

## Summary
- rows_reviewed: 124
- rejected_rows: 124
- correct_reject_rows: 80
- manual_review_rows: 44
- whitelist_candidate_rows: 32
- audit_bucket_counts: CORRECT_REJECT_YOUTH_RESERVE_TEAM_TOKEN=63; MANUAL_REVIEW_POSSIBLE_WHITELIST=32; CORRECT_REJECT_FRIENDLY_CONTEXT_VOLATILITY=16; REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION=12; CORRECT_REJECT_LOW_TIER_LOW_COVERAGE=1
- review_priority_counts: P3_CORRECT_REJECT=80; P1_REVIEW_CANDIDATE=32; P2_REVIEW_LOW_CONFIDENCE=12
- next_action: Review P1/P2 rows manually. Do not change trust gates or whitelist automatically from this audit.
- auto_apply: NO
- production_change: NO

## Review Candidates
- Be'sat Kermanshah vs Mes Soongoun | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Damash Gilanian vs Mes Shahr-e Babak | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Mes Kerman vs Naft Gachsaran | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Naft Bandar Abbas vs Shahrdari Noshahr | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Nassaji Mazandaran vs Shenavarsazi Qeshm | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Navad Urmia vs Fard Alborz | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Niroye Zamini vs Ario Eslamshahr | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Saipa vs Havadar | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Sanat Naft vs Pars Jonoubi JAM | league=Azadegan League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Latvia vs Faroe Islands | league=Baltic Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Lithuania vs Estonia | league=Baltic Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- CR Khemis Zemamra vs UTS Rabat | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Kawkab Marrakech vs Raja Casablanca | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Maghreb Fès vs FAR Rabat | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Yacoub El Mansour vs CODM Meknès | league=Botola Pro | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Stade Migoveen vs Ogooue FC | league=Championnat D1 | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Atlantic vs Kumba | league=Elite Two | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Resovia Rzeszów vs KSZO 1929 | league=II Liga - East | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Sokół Kleczew vs Górnik Polkowice | league=II Liga - East | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- 22 de Julio vs Atletico FC | league=Liga Pro Serie B | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- 9 de Octubre vs Cuniburo | league=Liga Pro Serie B | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Singleton Strikers vs Cessnock City Hornets | league=NNSW League 1 | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Ahrobiznes Volochysk vs Kudrivka | league=Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Livyi Bereh vs Oleksandria | league=Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Bulawayo Chiefs vs TelOne | league=Premier Soccer League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Bougouni vs USFAS Bamako | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Djoliba vs Réal Bamako | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Stade Malien Bamako vs Binga | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- US Bougouba vs Diarra | league=Première Division | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Lochin vs Kattaqurgon | league=Pro League A | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Logan Lightning vs Redlands United | league=Queensland Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Al Hilal Port Sudan vs Al Ahli Wad Medani | league=Sudani Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Hilal El-Fasher vs Hay Al Wadi | league=Sudani Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Umm Mughad vs Al Fallah | league=Sudani Premier League | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Honka vs HJK Helsinki | league=Suomen Cup | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- IK brage vs Ljungskile SK | league=Superettan | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Oddevold vs IFK Norrkoping | league=Superettan | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Osters IF vs IFK Varnamo | league=Superettan | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Sandviken vs Falkenbergs FF | league=Superettan | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- United Nordic vs Ostersunds FK | league=Superettan | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected
- Konyaspor vs AFC Eskilstuna | league=Svenska Cupen | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Räppe vs Hässleholms IF | league=Svenska Cupen | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- Vendelsö vs Haninge | league=Svenska Cupen | bucket=MANUAL_REVIEW_POSSIBLE_WHITELIST | priority=P1_REVIEW_CANDIDATE | candidate=YES_REVIEW_ONLY | reason=source was rejected but league name looks like senior/structured competition after low-trust hardening
- SJK Akatemia vs JIPPO | league=Ykkösliiga | bucket=REVIEW_REJECTED_SOURCE_UNKNOWN_COMPETITION | priority=P2_REVIEW_LOW_CONFIDENCE | candidate=MAYBE_REVIEW_ONLY | reason=source is rejected and no strong low-trust token or senior token was detected

## Guardrails
- This audit is advisory only.
- It does not promote, whitelist, score, enrich, call APIs, create picks, or create stake permission.
- Any trust expansion must be implemented in a separate reviewed change after sample validation.
