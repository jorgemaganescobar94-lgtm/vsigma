# vSIGMA Daily Decision Journal - Shadow Candidate v4 Pre

- Date: 2026-05-24
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Layer: candidate v2 + O2.5 Low Conversion Firewall

## O2.5 Low Conversion Firewall

- KEEP_OVER_2_5: 0
- DEGRADE_TO_OVER_1_5: 2
  - Huesca vs Castellón: OVER_2_5 -> OVER_1_5 (score 8.5)
  - Sporting Gijon vs Almeria: OVER_2_5 -> OVER_1_5 (score 8.5)
- SECONDARY_ONLY: 0
- REMOVE_FROM_COMPETITION_TOP: 0

## Candidate v4 Shadow Top

| accuracy_mode_rank | home_team | away_team | market_primary | over25_low_conversion_firewall_decision | over25_low_conversion_confirmation_score |
| --- | --- | --- | --- | --- | --- |
| 1 | Huesca | Castellón | OVER_1_5 | DEGRADE_TO_OVER_1_5 | 8.5 |
| 2 | Catanzaro | Monza | OVER_1_5 | NOT_APPLIED | 0.0 |

## Baseline vs Candidate v2 vs Candidate v4

| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_V2+CANDIDATE_V4 | 1392205 | Huesca vs Castellón | Segunda División |  | 1 | 1 |  | OVER_2_5 | OVER_1_5 | OVER_2_5 | DEGRADE_TO_OVER_1_5 | 8.5 | MARKET_DOWNGRADED_TO_OVER_1_5 |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |
| BASELINE | 1392207 | Sporting Gijon vs Almeria | Segunda División | 1 |  |  | OVER_2_5 |  |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  |  |
| BASELINE+CANDIDATE_V2 | 1492273 | Flamengo vs Palmeiras | Serie A | 3 | 3 |  | OVER_1_5 | OVER_1_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |  |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1545796 | Catanzaro vs Monza | Serie B | 2 | 2 | 2 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |
