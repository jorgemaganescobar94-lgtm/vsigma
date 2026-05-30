# vSIGMA v66.7 — Autonomous Safe Work Authorization Policy

## Purpose

This file records the user's standing operational authorization for ChatGPT to keep improving the vSIGMA repository in autonomous safe mode.

The policy is intended to reduce repetitive confirmations for routine safe engineering work. It does not override GitHub, ChatGPT connector, platform, legal, billing, security, or repository protection controls.

## Standing authorization

The user authorizes ChatGPT to perform safe repository work without asking for confirmation each time when the work is inside the permitted scope below.

Operational phrase from the user: repeated instructions such as `hazlo`, `sigue`, `sigamos`, `modo autónomo seguro`, `mejora el sistema`, or equivalent are sufficient to continue safe work within this policy.

## Permitted autonomous scope

ChatGPT may autonomously:

- Create new diagnostic scripts under `scripts/`.
- Modify existing non-destructive vSIGMA scripts.
- Add or update GitHub Actions workflows that only generate reports, ledgers, gates, boards, or diagnostics.
- Add trigger bridge files under `.vsigma/triggers/`.
- Add governance, report, ledger, calibration, and audit files under `.vsigma/` or `data/processed/`.
- Improve parsers, gates, filters, ledgers, dashboards, operator briefs, and source registries.
- Add safety modules that block, quarantine, downgrade, or audit weak data.
- Re-run workflows through trigger bridge commits.
- Fix bugs that break the daily chain, prelock recheck, operator brief, or learning loop.
- Add guardrails that prevent false positives, stale data, bad extraction, low coverage, or invalid picks.
- Use existing repository secrets indirectly through GitHub Actions when the workflow already needs them, without exposing secret values.
- Commit changes directly to `main` when the change is safe, reversible, and diagnostic/governance oriented.

## Mandatory confirmation scope

ChatGPT must ask the user before doing any of the following:

- Deleting important source files, workflows, ledgers, or historical data.
- Rotating, revealing, copying, or modifying API keys, secrets, tokens, passwords, or credentials.
- Adding paid services, increasing API usage limits, changing billing settings, or increasing monthly cost.
- Executing real bets, staking, auto-betting, or connecting to a bookmaker/account that could place bets.
- Sending money, moving funds, trading assets, or modifying financial accounts.
- Publishing external content outside GitHub without the user's explicit instruction.
- Making destructive changes to production systems outside this repository.
- Disabling major safety gates such as No Bet, stake blocking, bad extraction quarantine, or official-lineup prelock checks.
- Rewriting large parts of the model logic in a way that removes existing governance without a rollback path.
- Changing repository visibility, ownership, permissions, branch protection, or collaborator access.

## Betting and execution safety

This project may analyze markets, but autonomous work must remain diagnostic.

- No script may execute bets.
- No workflow may place stakes.
- No output may be treated as automatic financial instruction.
- Official stake remains blocked unless the user manually decides otherwise outside this system.
- `No Bet`, `Watch`, `Prelock Required`, `Live Only`, and quarantine states are valid successful governance outcomes.

## Secret handling

- Never print, commit, log, or expose secret values.
- Reference secrets only by environment variable name inside workflows.
- If a secret is missing, scripts must degrade safely to `NO_API_KEY`, `NO_SEARCH_KEY`, `NO_DATA`, or equivalent.
- If a workflow fails because of missing secrets, report the missing secret name, not the value.

## Data-quality rules

Autonomous changes must preserve or improve these principles:

- Do not fabricate data.
- Do not treat probable lineups as official lineups.
- Do not convert one-source probable XI into strong consensus.
- Do not treat parser failures as source failures without evidence.
- Do not let raw autonomous extraction bypass quarantine.
- Do not let low coverage become a strong pick.
- Do not fill top lists for quantity if the edge is weak.
- Prefer safe downgrade, quarantine, watch-only, live-only, or no-bet over forced picks.

## Rollback and reversibility

Every autonomous change should be:

- Committed with a clear message.
- Small enough to understand and revert.
- Guarded by `auto_apply=NO` and `production_change=NO` when appropriate.
- Compatible with existing daily reports and ledgers.
- Transparent in final user summaries.

## Default response behavior

When the user asks to continue improving the system, ChatGPT should:

1. Choose the highest-value safe improvement.
2. Implement it directly if it is within permitted scope.
3. Run or trigger the relevant workflow when possible.
4. Verify outputs.
5. Report what changed, what worked, and what remains blocked.

ChatGPT should not repeatedly ask for permission for routine safe changes covered by this policy.

## Version note

Active policy version: v66.7 — Autonomous Safe Work Authorization Policy.

This policy is an operating agreement inside the repo. It does not technically grant platform-level permanent permissions; it records user intent and governs how ChatGPT should act when the connector permits the action.
