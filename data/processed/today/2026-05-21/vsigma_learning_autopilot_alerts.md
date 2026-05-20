# vSIGMA Learning Autopilot Alerts - 2026-05-21

## Executive Alert Summary
- generated_at: 2026-05-21T00:03:20+01:00
- alerts generated: 7
- alert_type_counts: DATA_QUALITY_REVIEW_REQUIRED=6; OPERATIONAL_REVIEW_REQUIRED=1
- severity_counts: P2=5; P1=2
- issues_opened_or_existing: 7

## Alerts
- P1 | DATA_QUALITY_REVIEW_REQUIRED | source=DATA_BLOCKED | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/29 | auto_apply=NO
- P1 | OPERATIONAL_REVIEW_REQUIRED | source=WAITING_PRELOCK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/30 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=OVER_1_5::UNKNOWN_RISK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/31 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNKNOWN_MARKET::UNKNOWN_RISK | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/32 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/33 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/34 | auto_apply=NO
- P2 | DATA_QUALITY_REVIEW_REQUIRED | source=UNRESOLVED_RESULTS | issue=https://github.com/jorgemaganescobar94-lgtm/vsigma/issues/35 | auto_apply=NO

## Guardrails
- auto_apply: NO for every alert
- production_change: NO for every alert
- official picks changed: NO
- model changes applied: NO
