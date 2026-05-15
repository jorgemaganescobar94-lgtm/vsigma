# vSIGMA project instructions

## Mission
Build and maintain the most precise, reliable, and automatic possible football analysis pipeline for:
- match reading
- market translation
- edge vs odds
- execution governance
- real backtesting
- threshold calibration

## Environment
- Repository root: C:\vsigma
- OS: Windows / PowerShell
- Python environment: .venv inside repo
- Prefer running Python as:
  .\.venv\Scripts\python.exe <script>
- If a package is missing, install it inside .venv, not globally.

## Non-negotiables
- No manual workarounds when an automated fix is possible.
- Prefer robust scripts over ad hoc edits.
- Preserve reproducibility.
- Do not silently change CSV schemas without checking downstream dependencies.
- Before editing a script, inspect current repo state and relevant CSV columns.
- After each meaningful code change, run the narrowest valid verification command.
- Save reports under data\processed and scripts under scripts.
- Never delete historical outputs unless replacing them with a clearly better version.

## Working style
- Think like an engineering agent, not a chat assistant.
- Inspect, plan briefly, implement, run, verify, iterate.
- When blocked, diagnose the real root cause instead of patch stacking.
- Prefer stable fixes over clever ones.
- Keep code explicit, defensive, and production-oriented.

## Repo conventions
- Use fixture_id as the primary join key whenever possible.
- Treat duplicate columns after merges as a data-quality risk and handle them defensively.
- Normalize result labels robustly.
- Backtests must distinguish:
  - all rows
  - actionable only
  - non-actionable
  - graded bets only
- Calibration logic must be evidence-based and driven by real labeled outcomes.

## Output expectations
When you finish a task:
1. list files changed
2. list commands run
3. state whether validation passed
4. state exact next recommended engineering step
