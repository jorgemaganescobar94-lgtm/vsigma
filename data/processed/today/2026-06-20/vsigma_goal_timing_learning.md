# vSIGMA Goal Timing Learning - 2026-06-20

## Summary
- goal_timing_rows: 13
- goal_timing_data_status_counts: NO_GOAL_TIMING_DATA=13
- goal_timing_profile_counts: GOAL_TIMING_DATA_MISSING=10; DIAGNOSTIC_NO_GOAL_TIMING_LEARNING=3
- goal_timing_learning_label_counts: NO_TIMING_SIGNAL=10; DIAGNOSTIC_NOT_REAL_FIXTURE=3
- timing_evidence_level_counts: LOW=10; NONE=3
- manual_review_required_counts: NO=13
- auto_apply: NO
- production_change: NO

## Goal Timing Rows
- DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- GOAL_TIMING_DATA_MISSING | Las Palmas vs Malaga | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Almeria vs Castellón | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Almeria vs Castellón | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Nautico Recife vs Fortaleza EC | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Ponte Preta vs Cuiaba | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Malaga vs Las Palmas | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Maringá vs Maranhão | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | TransINVEST Vilnius vs FK Trakai | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | Gnistan vs Lahti | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- GOAL_TIMING_DATA_MISSING | SJK vs VPS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=PENDING | label=NO_TIMING_SIGNAL | manual=NO | action=COLLECT_GOAL_EVENT_DATA
- DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE
- DIAGNOSTIC_NO_GOAL_TIMING_LEARNING | NO_PROMOTED_RAW_CANDIDATES vs NO_SCORING_SAFE_ROWS | first_goal=NA team=UNKNOWN | 0-0HT=UNKNOWN early15=NO late75=0 | outcome=NO_PICK | label=DIAGNOSTIC_NOT_REAL_FIXTURE | manual=NO | action=NO_MODEL_CHANGE

## Guardrails
- This goal timing report is advisory only and never changes picks, stake, live gates, or weights.
- Missing event data is not treated as a model failure by itself.
- Early/late goal labels require causal review before any lesson is accepted.
- No automatic entry timing, live, source registry, or production changes are created here.
