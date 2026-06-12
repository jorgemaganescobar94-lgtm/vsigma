# vSIGMA — Complete Handoff to Claude

## Purpose
This document transfers operational ownership of vSIGMA to Claude/Claude Code. The project must continue from the existing repository and workflows. Do not rewrite the system. Do not duplicate API integrations. Maintain strict governance.

## Repository
- GitHub: `jorgemaganescobar94-lgtm/vsigma`
- Local expected path: `C:\Users\jorge\vsigma`
- Main branch: `main`
- User timezone: `Atlantic/Canary`
- Python runtime: `3.11`

## Product definition
vSIGMA is a football betting decision-support system. It is not an auto-betting system. It ingests football data, builds candidate boards, validates markets through gates, rejects weak/unsupported prices, and produces manual-review outputs.

The core objective is not to maximize number of picks. The objective is to avoid bad picks, protect bankroll, maintain auditability, and allow `NO_BET` as a high-quality decision.

## Non-negotiable governance
- `auto_bet: NO`
- `production_change: NO` unless explicitly approved by Jorge
- No direct bet placement
- No automatic stake execution
- No secret exposure
- No invented data
- No undocumented threshold/gate changes
- No `git add .`
- No promotion of shadow logic without evidence

## Current working model
The current system contains two layers:

### Existing API/daily system
This is the older production/shadow ecosystem:
- API-Football/API-Sports client
- today match pipeline
- daily competition controller
- daily execution board
- forced API lineup board bridge
- healthcheck, ledger, governance, learning summaries

### New full-shadow decision system
This is the newer governed decision layer:
- U35 gate
- team total gate
- market governance
- price survival
- final execution lock
- execution confirmation
- full candidate runner
- batch candidate runner
- bridge from API board to batch runner

The current transition task is to connect both systems safely, not replace either.

## Important recent commits
- `9a99a3b` — Add scheduled API board batch workflow
- `a4b79c5` — Support RapidAPI transport in API football client
- `f4393be` — Ignore API board bridge outputs
- `861a1fc` — Add API board to batch candidate bridge
- `7b027f8` — vSIGMA auto 2026-06-12
- `911e9d4` — Ignore batch shadow pipeline outputs
- `f6eb5e0` — Fix batch shadow pipeline report hint
- `e6d39ed` — Add batch shadow pipeline runner

## API client status
File: `scripts/api_football_client.py`

The client loads `.env` and `.env.local`. It supports both:

### API-Sports direct
Environment variables:
- `API_FOOTBALL_KEY`
- `APIFOOTBALL_KEY`
- `API_SPORTS_KEY`
- `APISPORTS_KEY`
- `API_FOOTBALL_API_KEY`

Endpoint:
- `https://v3.football.api-sports.io`

Header:
- `x-apisports-key`

### RapidAPI
Environment variables:
- `RAPIDAPI_KEY`
- `X_RAPIDAPI_KEY`

Endpoint:
- `https://api-football-v1.p.rapidapi.com/v3`

Headers:
- `x-rapidapi-key`
- `x-rapidapi-host`

## API status at handoff
On 2026-06-12, local environment was fixed to Python 3.11 and dependencies worked. API authentication then reached the provider but returned:

`You have reached the request limit for the day`

This means:
- credentials were structurally recognized
- no further API-heavy work should be attempted until quota reset
- next daily run should happen after quota reset

## Python environment
The repo must use Python 3.11.

Known bad environment:
- `C:\Python314\python.exe` caused NumPy/Pandas binary incompatibility.

Correct setup:

```powershell
cd C:\Users\jorge\vsigma
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install --no-cache-dir --force-reinstall -r requirements.txt
.\.venv\Scripts\python.exe -c "import sys, requests, numpy, pandas; print(sys.version); print('OK requests/numpy/pandas')"
```

## Daily automation workflow
File: `.github/workflows/vsigma_auto_api_board_batch.yml`

Purpose:
- scheduled daily PRE/API refresh
- controller status
- forced API lineups
- API board bridge
- batch shadow pipeline
- commit reports

Schedule:
- `10 8 * * *` UTC, approximately 09:10 Atlantic/Canary during summer.

Hard rules:
- no bet placement
- manual review only
- commits reports only

## API board bridge
File: `scripts/build_full_pipeline_candidates_from_api_board.py`

Purpose:
- reads existing daily execution board / governance board
- reads existing forced API board lineups
- converts compatible rows into batch runner input CSV
- refuses unsupported markets
- refuses rows without odds
- refuses 1X2 rows without probabilities
- does not call API directly
- does not invent data

Key outputs:
- `data/processed/batch_inputs/vsigma_api_board_candidates_<date>.csv`
- `data/processed/governance/vsigma_api_board_candidate_bridge_<date>.md`
- `data/processed/governance/vsigma_api_board_candidate_bridge_skipped_<date>.csv`

Known behavior from test:
- It correctly read 1 board row and 86 lineup rows.
- It skipped `Malaga vs Las Palmas` because market `OVER_1_5_SUPPORTED` is not yet supported by the full-shadow runner.

## Batch runner
File: `scripts/run_vsigma_batch_shadow_pipeline.py`

Validated with synthetic Torino vs Genoa test:
- Candidate at @1.35 became `EXECUTE_SMALL_STAKE_MONITOR`.
- Candidate at @1.25 became `NO_EXECUTION_PRICE_FAIL`.
- Output correctly split executable/no execution.
- Repo remained clean after cleanup.

Hard rules:
- never places bets
- output is operational, not a guarantee

## Full shadow runner
File: `scripts/run_vsigma_full_shadow_pipeline.py`

Pipeline layers:
1. `apply_under35_shadow_gate.py`
2. `build_u35_market_action_hint.py`
3. `apply_team_total_gate.py`
4. `build_market_governance_summary.py`
5. `build_price_survival_check.py`
6. `build_final_execution_lock.py`
7. `build_execution_confirmation_check.py`

Validated synthetic Canada vs Bosnia manual test:
- Market: `HOME`
- Odds: `1.80`
- Final: `NO_EXECUTION_PRICE_THIN`
- Important: this was not API-backed, and must not be treated as official.

## Market support gap
The new full-shadow runner currently supports a narrower set of markets than the older board language.

Example issue:
- Old board market: `OVER_1_5_SUPPORTED`
- New full runner: does not yet support `OVER_1_5_SUPPORTED`
- Bridge skipped row as `UNSUPPORTED_MARKET`

Potential future improvement:
- add full-shadow support for `OVER_1_5`
- map `OVER_1_5_SUPPORTED` to `OVER_1_5`
- add price survival for over 1.5
- add gate governance for over 1.5

Do not add this without tests.

## Canada vs Bosnia incident
Jorge asked whether system prediction came from the real API. It did not. It used manual/synthetic forecast data. This was corrected.

Correct lesson:
- Do not present manual vSIGMA-style analysis as system output.
- A real system pick must come from API/daily board or documented manual candidate input.
- API quota exhaustion prevented full API evaluation on 2026-06-12.

## Commands for next operator session
Start with:

```powershell
cd C:\Users\jorge\vsigma
git pull origin main
git status
git log -8 --oneline
```

Check latest auto workflow output after scheduled run:

```powershell
Get-Content "data/processed/today/YYYY-MM-DD/vsigma_auto_api_board_batch_status.md" -Encoding UTF8
```

If batch exists:

```powershell
Get-Content "data/processed/governance/vsigma_batch_shadow_pipeline_auto_api_board_YYYY_MM_DD.md" -Encoding UTF8
```

If API failed:

```powershell
.\.venv\Scripts\python.exe - <<'PY'
from scripts.api_football_client import APIFootballClient, APIFootballError
c = APIFootballClient()
print('provider:', c.provider)
print('key_name:', c.key_name)
print('base_url:', c.base_url)
print('headers:', list(c.headers.keys()))
print('key_mask:', c.api_key[:4] + '...' + c.api_key[-4:])
try:
    print(c.status(force_refresh=True))
except APIFootballError as e:
    print('status:', e.status_code)
    print('msg:', e.message)
    print('api_errors:', e.api_errors)
    print('response:', e.response_text)
PY
```

## Development priorities after handoff
1. Confirm next scheduled workflow run after API quota reset.
2. Verify generated `vsigma_auto_api_board_batch_status.md`.
3. If bridge writes zero candidates because markets are unsupported, add support for the most common old-board markets one by one.
4. First likely market support gap: `OVER_1_5_SUPPORTED` -> governed `OVER_1_5` full-shadow market.
5. Keep all output manual-review only.

## How Claude should work
- First read `CLAUDE.md`.
- Then read this handoff.
- Then inspect latest `git status`, latest workflow output, latest daily reports.
- Never assume today’s data exists.
- If asked for a pick, state whether it is:
  - official system
  - shadow system
  - API-backed
  - manual/synthetic
  - unavailable
- Use exact PowerShell commands for Jorge.

## Final transition statement
Claude can become primary operator for this repo only if it follows this handoff, respects guardrails, and uses the existing API/daily board architecture. The project is ready for Claude to take over maintenance and daily operations, but real betting execution remains manual outside the system.
