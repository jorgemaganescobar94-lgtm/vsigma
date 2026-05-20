# vSIGMA automerge governance v06

Este flujo permite automerge solo para PRs de infraestructura/reporting/testing con guardrails estrictos.

## Qué PRs se automergean

Un PR solo puede automergearse si cumple **todo**:

- tiene el label `automerge-safe`
- no está en draft
- la rama empieza por `vsigma-` o `codex/`
- autor confiable (owner del repo o bots reconocidos: `github-actions[bot]`, `codex[bot]`, `openai-codex[bot]`)
- pasa `scripts/check_automerge_guardrails.py`
- pasa `python -m pytest tests/test_automerge_guardrails.py -q`
- pasa `git diff --check`

Si pasa todo, se habilita merge commit y borrado de rama cuando sea posible.

## Cómo activar `automerge-safe`

1. Crear PR con cambios únicamente en zonas seguras.
2. Añadir label `automerge-safe` en GitHub.
3. Esperar ejecución de `vSIGMA Automerge Governance`.

## Qué cambios nunca se automergean

Siempre bloqueados:

- `data/`
- `.env`
- nombres de archivo con `secret`
- scripts relacionados con scoring/model/prediction/calibration/selection/backtest/odds/enrich/filter/core/ranking/threshold/market/result
- cualquier archivo fuera de la allowlist explícita

## Por qué scoring/modelo requiere revisión humana

La lógica predictiva (fórmulas, thresholds, calibración, ranking y selección de mercados) impacta directamente decisiones de ejecución y riesgo financiero. Esos cambios requieren revisión humana para garantizar trazabilidad, control de calidad y gobernanza del sistema.
