# vSIGMA Data Quality Governor - 2026-06-26

## Executive Data Quality Summary
- generated_at: 2026-06-26T02:34:35+01:00
- executive_status: DATA_QUALITY_REVIEW_REQUIRED
- issues: 14
- severity_counts: P3=14
- issue_type_counts: DATA_QUALITY_BLOCKER=7; UNRESOLVED_RESULTS=4; DATA_QUALITY_PROPOSAL=3
- auto_fix: NO
- production_change: NO

## Prioritized Issues
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=OVER_1_5::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=OVER_2_5::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNKNOWN_MARKET::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED_RESULTS | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=OVER_1_5::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=OVER_2_5::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=UNKNOWN_MARKET::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | UNRESOLVED_RESULTS | n=1 | key=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | UNRESOLVED_RESULTS | n=1 | key=UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | UNRESOLVED_RESULTS | n=1 | key=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | UNRESOLVED_RESULTS | n=1 | key=UNRESOLVED_RESULTS | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.

## Guardrails
- Model changes applied: NO
- Shadow promotions applied: NO
- Production changes applied: NO
- Auto-fix applied: NO
- P1/P2 data-quality issues block promotion and threshold/calibration changes until resolved.