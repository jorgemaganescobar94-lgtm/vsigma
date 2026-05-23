# vSIGMA Data Quality Governor - 2026-05-22

## Executive Data Quality Summary
- generated_at: 2026-05-23T14:46:27+01:00
- executive_status: DATA_QUALITY_BLOCKS_MODEL_CHANGE
- issues: 19
- severity_counts: P3=17; P2=2
- issue_type_counts: DATA_QUALITY_BLOCKER=8; UNRESOLVED_RESULTS=4; DATA_QUALITY_PROPOSAL=3; NO_SIGNAL=1; UNKNOWN_RISK=1; UNKNOWN_MARKET=1; UNRESOLVED_LEDGER_ROWS=1
- auto_fix: NO
- production_change: NO

## Prioritized Issues
- P2 | NO_SIGNAL | n=3 | key=NO_SIGNAL | action=Populate improvement_signal or classify as monitor-only.
- P2 | UNKNOWN_RISK | n=3 | key=UNKNOWN_RISK | action=Populate accuracy_primary_risk before pattern mining.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=DATA_BLOCKED | action=Resolve this evidence blocker before model/shadow promotion.
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
- P3 | UNKNOWN_MARKET | n=1 | key=UNKNOWN_MARKET | action=Normalize missing market_primary before pattern mining.
- P3 | UNRESOLVED_LEDGER_ROWS | n=1 | key=RESULT_STATUS_UNRESOLVED | action=Run/verify post-result labeling until learning rows close.
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