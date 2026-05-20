# vSIGMA Learning Autopilot Alerts - 2026-05-20

## Executive Alert Summary
- generated_at: 2026-05-20T22:14:03+01:00
- alerts generated: 6
- alert_type_counts: DATA_QUALITY_REVIEW_REQUIRED=5; OPERATIONAL_REVIEW_REQUIRED=1
- severity_counts: P2=5; P1=1
- issues_opened_or_existing: 6

## Alerts
- P1 | OPERATIONAL_REVIEW_REQUIRED | source=WAITING_PRELOCK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/23 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=OVER_1_5::UNKNOWN_RISK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/24 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNKNOWN_MARKET::UNKNOWN_RISK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/25 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/26 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/27 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED_RESULTS | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/28 | auto_apply=NO

## Guardrails
- auto_apply: NO for every alert
- production_change: NO for every alert
- official picks changed: NO
- model changes applied: NO
