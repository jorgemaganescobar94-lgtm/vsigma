# vSIGMA Claude Setup Guide

## Goal
Move day-to-day vSIGMA operation to Claude/Claude Code while keeping the repository, API pipeline, workflows, and manual-review governance intact.

## Local setup
1. Install Claude Code using the current official Anthropic instructions for Windows.
2. Open PowerShell.
3. Go to the repo:

```powershell
cd C:\Users\jorge\vsigma
```

4. Start Claude Code:

```powershell
claude
```

5. Paste the first prompt from:

```text
docs/VSIGMA_CLAUDE_FIRST_PROMPT.md
```

## Repository files Claude must read first
- `CLAUDE.md`
- `docs/VSIGMA_HANDOFF_TO_CLAUDE.md`
- `docs/VSIGMA_CLAUDE_OPERATOR_RUNBOOK.md`
- `docs/VSIGMA_CLAUDE_FIRST_PROMPT.md`

## Claude Code operating mode
Recommended initial mode:
- read-only first session
- no file edits in first session
- no secret access
- no autonomous production changes

After Claude proves it understands the repo:
- allow documentation fixes
- allow small bug fixes
- allow workflow diagnosis
- require explicit approval for strategy, thresholds, gates, and market expansion

## First 7-day transition

### Day 1
Claude reads docs and summarizes architecture. No edits.

### Day 2
Claude checks scheduled workflow outputs and reports operational status.

### Day 3
Claude diagnoses any API/workflow errors after quota reset.

### Day 4
Claude proposes one small maintenance improvement.

### Day 5
Claude implements one approved low-risk improvement.

### Day 6
Claude verifies docs/runbooks match actual repo behavior.

### Day 7
Claude becomes primary daily operator for repo maintenance and status review.

## What remains manual
- API key management.
- Real-money decisions.
- Approval of threshold/gate changes.
- Approval of new market families.
- Any production-risk workflow change.

## Daily Claude prompt after transition

```text
Revisa el estado diario de vSIGMA para hoy. Usa CLAUDE.md y el runbook. Mira los workflows, informes generados, batch report, API status, errores y candidatos. No modifiques archivos salvo que encuentres un fix documental menor. Dame veredicto operativo y siguiente acción.
```
