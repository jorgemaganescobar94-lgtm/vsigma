# vSIGMA Daily Decision Journal - Shadow Candidate v4 Pre

- Date: 2026-05-13
- Timezone: Atlantic/Canary
- Mode: SHADOW / experimental / non-official
- Layer: candidate v2 + O2.5 Low Conversion Firewall

## O2.5 Low Conversion Firewall

- KEEP_OVER_2_5: 0
- DEGRADE_TO_OVER_1_5: 0
- SECONDARY_ONLY: 1
  - Lens vs Paris Saint Germain: OVER_2_5 -> OVER_2_5 (score 12.0)
- REMOVE_FROM_COMPETITION_TOP: 0

## Candidate v4 Shadow Top

| accuracy_mode_rank | home_team | away_team | market_primary | over25_low_conversion_firewall_decision | over25_low_conversion_confirmation_score |
| --- | --- | --- | --- | --- | --- |
| 1 | Stockport County | Stevenage | OVER_1_5 | NOT_APPLIED | 0.0 |

## Baseline vs Candidate v2 vs Candidate v4

| comparison_status | fixture_id | fixture | league | baseline_rank | candidate_v2_rank | candidate_v4_rank | baseline_market | candidate_v2_market | candidate_v4_market | candidate_v4_original_market | candidate_v4_firewall_decision | candidate_v4_firewall_score | candidate_v4_firewall_action | baseline_primary_risk | candidate_v2_primary_risk | candidate_v4_primary_risk |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BASELINE+CANDIDATE_V2 | 1387952 | Lens vs Paris Saint Germain | Ligue 1 | 2 | 1 |  | OVER_2_5 | OVER_2_5 |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |  |
| BASELINE | 1391169 | Alaves vs Barcelona | La Liga | 1 |  |  | OVER_2_5 |  |  |  |  |  |  | FAILURE_MODE_LOW_CONVERSION |  |  |
| BASELINE+CANDIDATE_V2+CANDIDATE_V4 | 1544063 | Stockport County vs Stevenage | League One | 3 | 2 | 1 | OVER_1_5 | OVER_1_5 | OVER_1_5 | OVER_1_5 | NOT_APPLIED | 0.0 | NO_ACTION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION | FAILURE_MODE_LOW_CONVERSION |
