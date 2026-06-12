# First Prompt for Claude / Claude Code

Use this exact prompt when opening the project with Claude Code.

```text
Actúa como operador técnico principal del proyecto vSIGMA.

Antes de modificar nada:
1. Lee CLAUDE.md.
2. Lee docs/VSIGMA_HANDOFF_TO_CLAUDE.md.
3. Lee docs/VSIGMA_CLAUDE_OPERATOR_RUNBOOK.md.
4. Ejecuta solo lectura: git status, git log -8 --oneline y lista de workflows.
5. Resume arquitectura, estado actual, scripts críticos, workflows activos, riesgos y próximos pasos.

Reglas obligatorias:
- No modifiques archivos en esta primera pasada.
- No toques .env, .env.local ni secrets.
- No expongas claves.
- No uses git add .
- Mantén auto_bet: NO y production_change: NO.
- No llames pick oficial a nada que no salga del sistema.
- Si falta API, cuota, odds, lineups o datos, dilo claramente.

Después de tu resumen, propón un plan de transición de 7 días para que tú seas el operador principal del repo, con tareas pequeñas, validables y reversibles.
```

## Second prompt after Claude summarizes

```text
Correcto. Ahora asume mantenimiento operativo diario. Revisa si el workflow programado vSIGMA Auto API Board Batch generó outputs para la fecha actual. No cambies código todavía. Lee los informes y dime: estado API, candidatos, batch, errores, No Bet/ejecutables y siguiente acción.
```

## Prompt for safe code changes

```text
Propón un cambio pequeño y reversible para mejorar vSIGMA. Antes de editar, dime: objetivo, archivos, riesgo, comandos de validación y rollback. No cambies thresholds, gates, estrategias ni producción sin aprobación explícita.
```
