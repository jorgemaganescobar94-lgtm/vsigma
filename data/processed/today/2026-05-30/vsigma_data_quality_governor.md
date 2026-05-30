# vSIGMA Data Quality Governor - 2026-05-30

## Executive Data Quality Summary
- generated_at: 2026-05-30T09:41:31+01:00
- executive_status: DATA_QUALITY_BLOCKS_MODEL_CHANGE
- issues: 20
- severity_counts: P3=19; P2=1
- issue_type_counts: DATA_QUALITY_BLOCKER=8; DATA_QUALITY_PROPOSAL=4; UNRESOLVED_RESULTS=4; UNRESOLVED_LEDGER_ROWS=1; NO_SIGNAL=1; UNKNOWN_MARKET=1; UNKNOWN_RISK=1
- auto_fix: NO
- production_change: NO

## Prioritized Issues
- P2 | UNRESOLVED_LEDGER_ROWS | n=4 | key=RESULT_STATUS_UNRESOLVED | action=Run/verify post-result labeling until learning rows close.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=DATA_BLOCKED | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=OVER_1_5::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=OVER_2_5::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNKNOWN_MARKET::UNKNOWN_RISK | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::OVER_1_5::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::OVER_2_5::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED::UNKNOWN_MARKET::UNKNOWN_RISK::NO_SIGNAL | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_BLOCKER | n=1 | key=UNRESOLVED_RESULTS | action=Resolve this evidence blocker before model/shadow promotion.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=DATA_BLOCKED | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=OVER_1_5::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=OVER_2_5::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | DATA_QUALITY_PROPOSAL | n=1 | key=UNKNOWN_MARKET::UNKNOWN_RISK | action=Clean UNKNOWN/UNRESOLVED/NO_SIGNAL evidence and rebuild learning outputs.
- P3 | NO_SIGNAL | n=1 | key=NO_SIGNAL | action=Populate improvement_signal or classify as monitor-only.
- P3 | UNKNOWN_MARKET | n=1 | key=UNKNOWN_MARKET | action=Normalize missing market_primary before pattern mining.
- P3 | UNKNOWN_RISK | n=1 | key=UNKNOWN_RISK | action=Populate accuracy_primary_risk before pattern mining.
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