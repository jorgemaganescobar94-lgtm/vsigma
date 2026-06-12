# vSIGMA — Inventario y Auditoría de Workflows

> Documento de gobernanza generado por Claude (operador técnico) en una pasada de **solo lectura**.
> Consolida los pases Día 1 (inventario), Día 1.b (auditoría de los 6 más sensibles) y Día 1.c (cierre de scripts críticos).
> Fecha de auditoría: 2026-06-12. Rama: `main`.
>
> **Reglas respetadas durante la auditoría:** solo lectura; sin commits; sin `git add`; sin tocar `.env`/secrets; sin ejecutar workflows; sin cambiar permisos/thresholds/gates/fórmulas/registry/producción.
> `auto_bet: NO` · `production_change: NO`.

---

## 1. Resumen ejecutivo

vSIGMA tiene **51 archivos `.yml`** en `.github/workflows/` (no ~52 como sugería la memoria inicial). El handoff documentaba ~2 workflows y ~10 scripts; la realidad es **51 workflows y 287 scripts** en `scripts/`. Esto es, en sí mismo, el primer hallazgo de gobernanza: existe una capa de automatización mucho mayor que la documentada.

Hallazgos clave:

- **Patrón dominante:** ~49 workflows hacen `git push origin HEAD:main` directo, sin PR ni revisión humana. Casi todos generan *reports* (`.csv`/`.md` bajo `data/processed/`) y usan `[skip ci]` para no encadenarse. No es inseguro per se, pero significa que `main` se modifica de forma autónoma muchas veces al día.
- **Solo 2 vías cambian el sistema de verdad:**
  1. `vsigma_production.yml` → motor real que produce los **picks oficiales** y consume API (no documentado en el handoff).
  2. `vsigma_automerge_governance.yml` → única vía por la que código entra a `main` auto-aprobado (con guardrail default-deny).
- **6+ workflows con nombres "agresivos"** (`self_improvement_governor`, `formula_patch_governance`, `safe_action_dispatcher`, `shadow_registry_proposals`, `shadow_experiment_factory`, `safe_auto_pr_generator`) resultaron ser **report-only / dry-run**: no modifican lógica, gates, thresholds, fórmulas ni registry. Verificado leyendo los scripts.
- **`auto_bet: NO` se cumple** en todo lo auditado. Ningún workflow coloca apuestas. Estados como `EXECUTE_GOVERNED_PICK` son recomendaciones de revisión manual.
- **No hay `pull_request_target` ni `issue_comment`** → no hay vector obvio de exfiltración de secrets vía PR externo.
- **Riesgo principal real = cuota API:** `production` (modo `auto` cada 30 min) más los workflows de prelock disparan repetidamente `enrich_*` + snapshots de odds. Es casi seguro el origen del límite diario agotado el 2026-06-12.

---

## 2. Inventario de los 51 workflows

`api_shadow_rule_ledger`, `adhoc_fixture_forecast`, `auto_api_board_batch`, `automation_health_monitor`, `automerge_governance`, `autonomous_improvement_advisor`, `calibration_memory_ledger`, `context_adjusted_final_picks`, `context_adjustment_result_auditor`, `context_filter_advisor`, `context_level_matrix`, `daily_decision_chain`, `daily_decision_chain_v2`, `daily_execution_board`, `data_quality_governor`, `evidence_action_router`, `evidence_cleaner`, `evidence_closure_sequencer`, `failure_doctor`, `final_portfolio_verdict`, `forced_api_board_fixture_lineups`, `forecast_market_translator`, `formula_patch_governance`, `full_post_match_learning_chain`, `issue_alerts`, `learning_evidence_closer`, `learning_issue_lifecycle`, `learning_residual_quarantine`, `live_trigger_validator`, `match_stat_forecasts`, `match_stat_forecast_backtest`, `matrix_portfolio_v2`, `mobile_operator_control_panel`, `objective_availability_gate`, `operator_brief`, `pattern_promotion_readiness`, `post_match_refresh_calibration_chain`, `post_match_stat_calibration`, `prelock_live_recheck`, `prelock_official_lineup_recheck`, `prematch_calibration_rule_gate`, `production`, `real_objective_context_gate`, `safe_action_dispatcher`, `safe_auto_pr_generator`, `self_improvement_governor`, `shadow_experiment_factory`, `shadow_registry_proposals`, `shadow_registry_sync`, `smoke_test`, `stat_calibration_governor`.

Notas transversales:
- **Permisos:** 50/51 tienen `contents: write`. Única excepción: `failure_doctor` (`contents: read`, `actions: read`, `issues: write`).
- **`issues: write` adicional:** `automerge_governance`, `data_quality_governor`, `evidence_action_router`, `evidence_cleaner`, `evidence_closure_sequencer`, `issue_alerts`, `learning_evidence_closer`, `learning_residual_quarantine`, `pattern_promotion_readiness`, `production`, `self_improvement_governor`, `safe_action_dispatcher`, `shadow_experiment_factory`. (`learning_issue_lifecycle`: `issues: read`.)
- **`pull-requests: write`:** solo `automerge_governance`.
- **`[skip ci]` ausente** (commit que podría encadenar): `operator_brief` y `prelock_official_lineup_recheck` (este además tiene trigger `push` → riesgo de auto-disparo).

---

## 3. Clasificación por riesgo

### 🔴 HIGH
- `production` — motor real, decodifica `.env` completo, consumo API intensivo, produce picks oficiales.
- `automerge_governance` — única vía de código auto-aprobado a `main`; allowlist autorreferencial.

### 🟠 MEDIUM
- **API + push (consumo de cuota):** `auto_api_board_batch`, `forced_api_board_fixture_lineups`, `daily_decision_chain_v2`, `live_trigger_validator`, `prelock_live_recheck`, `prelock_official_lineup_recheck`, `full_post_match_learning_chain`, `post_match_refresh_calibration_chain`, `adhoc_fixture_forecast`, `smoke_test`.
- **Encadenados por `workflow_run`:** `api_shadow_rule_ledger`, `prematch_calibration_rule_gate`, `forced_api_board_fixture_lineups`.
- **Nombres engañosos:** `safe_auto_pr_generator`, `safe_action_dispatcher` (capacidad real LOW, pero confusión operativa).

### 🟢 LOW (report-only / advisory)
`automation_health_monitor`, `autonomous_improvement_advisor`, `calibration_memory_ledger`, `context_adjusted_final_picks`, `context_adjustment_result_auditor`, `context_filter_advisor`, `context_level_matrix`, `daily_decision_chain`, `daily_execution_board`, `data_quality_governor`, `evidence_action_router`, `evidence_cleaner`, `evidence_closure_sequencer`, `failure_doctor`, `final_portfolio_verdict`, `forecast_market_translator`, `formula_patch_governance`, `issue_alerts`, `learning_evidence_closer`, `learning_issue_lifecycle`, `learning_residual_quarantine`, `match_stat_forecasts`, `match_stat_forecast_backtest`, `matrix_portfolio_v2`, `mobile_operator_control_panel`, `objective_availability_gate`, `operator_brief`, `pattern_promotion_readiness`, `post_match_stat_calibration`, `real_objective_context_gate`, `self_improvement_governor`, `shadow_experiment_factory`, `shadow_registry_proposals`, `shadow_registry_sync`, `stat_calibration_governor`.

> Nota: el riesgo LOW se refiere a **capacidad de cambiar comportamiento**. Todos escriben a `main` sin revisión, lo cual es un riesgo de gobernanza menor pero compartido.

---

## 4. Tabla de workflows

Leyenda: **Push** = commit+push directo a `main`. **PR/Merge** = crea o mergea PRs. **API** = consume API-Football/API-Sports (directo o vía scripts `enrich_*`/controller). **Afecta** = OFICIAL (picks oficiales) / SHADOW / REPORT / OPS-PR / ISSUES.

| Workflow | Trigger | Permissions | Secrets | Scripts (principales) | Push | PR/Merge | API | Afecta | Recomendación |
|---|---|---|---|---|---|---|---|---|---|
| production | dispatch + schedule (cada 30 min y más) | contents+issues write | **VSIGMA_ENV_B64** (.env completo) | run_vsigma_healthcheck, run_daily_competition_controller, **run_vsigma_auto_controller**, run_today_prelock_pipeline, +learning/shadow | Sí | No | **Sí (alto)** | OFICIAL | MANTENER + LIMITAR + DOCUMENTAR + aprobación humana |
| automerge_governance | pull_request | contents+PR+issues write | GITHUB_TOKEN | check_automerge_guardrails.py + pytest | No | **Merge** | No | CÓDIGO (guardrailed) | AUDITAR MÁS + LIMITAR allowlist |
| auto_api_board_batch | dispatch + schedule 08:10 | contents write | API directas | run_daily_competition_controller, force_api_board_fixture_lineups, build_full_pipeline_candidates_from_api_board, batch | Sí | No | **Sí** | SHADOW/REPORT | MANTENER + LIMITAR |
| forced_api_board_fixture_lineups | dispatch + workflow_run | contents write | API directas | force_api_board_fixture_lineups_refresh | Sí | No | **Sí** | REPORT (lineups) | MANTENER + LIMITAR |
| daily_decision_chain_v2 | dispatch + schedule (2x) | contents write | API + SERPAPI/BING | cadena decisión v2 | Sí | No | **Sí** | OFICIAL/REPORT | AUDITAR + LIMITAR |
| daily_decision_chain | dispatch + schedule (2x) | contents write | — | cadena decisión v1 | Sí | No | No (directo) | REPORT | MANTENER |
| live_trigger_validator | dispatch + schedule (~11x/día) | contents write | API directas | live trigger validator | Sí | No | **Sí** | REPORT | LIMITAR (frecuencia alta) |
| prelock_live_recheck | dispatch + schedule (6x) | contents write | — | prelock live recheck | Sí | No | Posible | OFICIAL (prelock) | LIMITAR |
| prelock_official_lineup_recheck | dispatch + schedule (4x) + **push** | contents write | API + SERPAPI/BING | prelock lineup recheck | Sí (sin `[skip ci]`) | No | **Sí** | OFICIAL (prelock) | LIMITAR + arreglar `[skip ci]` |
| full_post_match_learning_chain | dispatch + schedule (2x) | contents write | API directas | post-match learning chain | Sí | No | **Sí** | REPORT/learning | MANTENER + LIMITAR |
| post_match_refresh_calibration_chain | dispatch | contents write | API directas | post-match refresh calibration | Sí | No | **Sí** | REPORT/calibración | MANTENER |
| adhoc_fixture_forecast | dispatch | contents write | API directas | adhoc fixture forecast | Sí | No | **Sí** | REPORT | MANTENER (manual) |
| smoke_test | dispatch + push | contents write | VSIGMA_ENV_B64 | run_today_match_pipeline | Sí | No | **Sí** | REPORT/test | MANTENER |
| api_shadow_rule_ledger | dispatch + workflow_run | contents write | — | api shadow rule ledger | Sí | No | No | SHADOW/REPORT | AUDITAR cadena |
| prematch_calibration_rule_gate | dispatch + workflow_run | contents write | — | prematch calibration rule gate | Sí | No | No | REPORT/gate | AUDITAR cadena |
| failure_doctor | workflow_run + dispatch | issues write (read contents) | GITHUB_TOKEN | failure doctor | No | No | No | ISSUES | MANTENER |
| self_improvement_governor | dispatch + schedule 00:20 | contents+issues write | GITHUB_TOKEN | build_self_improvement_governor | Sí | No | No | REPORT | MANTENER |
| safe_action_dispatcher | dispatch + schedule 01:00 | contents+issues write | GITHUB_TOKEN | build_safe_action_dispatcher | Sí | No | No | REPORT | MANTENER + renombrar (engañoso) |
| safe_auto_pr_generator | dispatch + schedule (2x) | contents write | — | build_safe_auto_pr_generator | Sí | **No (no crea PR)** | No | OPS-PR plan | MANTENER + renombrar (engañoso) |
| formula_patch_governance | dispatch | contents write | — | build_shadow_calibration_patch_proposals + formula_patch_* (dry-run) | Sí | No | No | REPORT (dry-run) | MANTENER (gate de gobernanza) |
| shadow_registry_proposals | dispatch | contents write | — | build_shadow_registry_proposals | Sí | No | No | SHADOW/REPORT | MANTENER |
| shadow_registry_sync | dispatch + schedule 02:00 | contents write | — | build_shadow_registry_sync | Sí | No | No | SHADOW/REPORT | MANTENER |
| shadow_experiment_factory | dispatch + schedule 01:50 | contents+issues write | GITHUB_TOKEN | build_shadow_experiment_factory | Sí | No | No | SHADOW/REPORT | MANTENER |
| data_quality_governor | dispatch + schedule | contents+issues write | GITHUB_TOKEN | data quality governor | Sí | No | No | REPORT/ISSUES | MANTENER |
| evidence_action_router | dispatch + schedule | contents+issues write | GITHUB_TOKEN | evidence action router | Sí | No | No | REPORT/ISSUES | MANTENER |
| evidence_cleaner | dispatch + schedule | contents+issues write | GITHUB_TOKEN | evidence cleaner | Sí | No | No | REPORT/ISSUES | MANTENER |
| evidence_closure_sequencer | dispatch + schedule | contents+issues write | GITHUB_TOKEN | evidence closure sequencer | Sí | No | No | REPORT/ISSUES | MANTENER |
| issue_alerts | dispatch + schedule (3x) | contents+issues write | GITHUB_TOKEN | issue alerts | Sí | No | No | ISSUES/REPORT | MANTENER |
| learning_evidence_closer | dispatch + schedule | contents+issues write | GITHUB_TOKEN | learning evidence closer | Sí | No | No | REPORT/ISSUES | MANTENER |
| learning_issue_lifecycle | dispatch + schedule | contents write, issues read | GITHUB_TOKEN | learning issue lifecycle | Sí | No | No | ISSUES/REPORT | MANTENER |
| learning_residual_quarantine | dispatch + schedule | contents+issues write | GITHUB_TOKEN | learning residual quarantine | Sí | No | No | REPORT/ISSUES | MANTENER |
| pattern_promotion_readiness | dispatch + schedule | contents+issues write | GITHUB_TOKEN | pattern promotion readiness | Sí | No | No | REPORT | MANTENER |
| automation_health_monitor | dispatch + schedule (3x) | contents write | — | automation health | Sí | No | No | REPORT | MANTENER |
| autonomous_improvement_advisor | dispatch + schedule (2x) | contents write | — | autonomous improvement advisor | Sí | No | No | REPORT | MANTENER |
| calibration_memory_ledger | dispatch | contents write | — | calibration memory ledger | Sí | No | No | REPORT | MANTENER |
| context_adjusted_final_picks | dispatch | contents write | — | context adjusted final picks | Sí | No | No | REPORT | MANTENER |
| context_adjustment_result_auditor | dispatch | contents write | — | context adjustment auditor | Sí | No | No | REPORT | MANTENER |
| context_filter_advisor | dispatch | contents write | — | context filter advisor | Sí | No | No | REPORT | MANTENER |
| context_level_matrix | dispatch | contents write | — | context level matrix | Sí | No | No | REPORT | MANTENER |
| daily_execution_board | dispatch | contents write | — | daily execution board | Sí | No | No | REPORT | MANTENER |
| final_portfolio_verdict | dispatch | contents write | — | final portfolio verdict | Sí | No | No | REPORT | MANTENER |
| forecast_market_translator | dispatch | contents write | — | forecast market translator | Sí | No | No | REPORT | MANTENER |
| match_stat_forecasts | dispatch | contents write | — | match stat forecasts | Sí | No | No | REPORT | MANTENER |
| match_stat_forecast_backtest | dispatch | contents write | — | match stat forecast backtest | Sí | No | No | REPORT | MANTENER |
| matrix_portfolio_v2 | dispatch | contents write | — | matrix portfolio v2 | Sí | No | No | REPORT | MANTENER |
| mobile_operator_control_panel | dispatch + schedule (4x) | contents write | — | mobile operator control panel | Sí | No | No | REPORT | MANTENER |
| objective_availability_gate | dispatch | contents write | — | objective availability gate | Sí | No | No | REPORT | MANTENER |
| operator_brief | dispatch + schedule (4x) | contents write | — | operator brief | Sí (sin `[skip ci]`) | No | No | REPORT | MANTENER + revisar `[skip ci]` |
| post_match_stat_calibration | dispatch | contents write | — | post-match stat calibration | Sí | No | No | REPORT | MANTENER |
| real_objective_context_gate | dispatch | contents write | — | real objective context gate | Sí | No | No | REPORT | MANTENER |
| stat_calibration_governor | dispatch | contents write | — | stat calibration governor | Sí | No | No | REPORT | MANTENER |

---

## 5. Sección especial: `vsigma_production.yml`

**Es el motor real del sistema y NO está documentado en `CLAUDE.md` ni en el handoff.**

- **Triggers:** `workflow_dispatch` (modos health/pre/auto/prelock/post/post-yesterday) + schedule intensivo: 08:15 (post-ayer), 09:00 (pre), **cada 30 min de 09:30 a 23:30 (modo `auto`)**, 23:55 (post). Timezone Atlantic/Canary.
- **Permisos:** `contents: write`, `issues: write`.
- **Secret:** `VSIGMA_ENV_B64` → **decodifica el `.env` COMPLETO a disco** (`base64 --decode > .env`, chmod 600). Es el secret más sensible del repo.
- **Scripts:** `run_vsigma_healthcheck.py`, `run_daily_competition_controller.py` (pre/post), **`run_vsigma_auto_controller.py`** (modo `auto`, ventana 90 min), `run_today_prelock_pipeline.py`, `build_prelock_exclusion_audit.py`, y cadena learning/shadow/promotion + dispatch de alertas.
- **Push:** `git add data/raw data/processed notes outputs` → push directo a `main`. Sube artifacts (retención 14 días).
- **Qué hace realmente:** produce las **decisiones/picks oficiales** (estados EXECUTABLE/NO_BET/PRELOCK_BLOCKED, `OFFICIAL_ACTION_SUMMARY`, `next_action=EXECUTE_GOVERNED_PICK`). La lógica de decisión está hardcodeada en `run_vsigma_auto_controller.py`. **No edita** código/config/gates. **Nunca coloca apuestas.**
- **Riesgo:** 🔴 HIGH por criticidad (es producción; `production_change: NO`), por decodificar el env completo, y por consumo API alto (auto cada 30 min).
- **Recomendación:** MANTENER (es el sistema) + LIMITAR frecuencia AUTO + DOCUMENTAR en el handoff + cualquier cambio requiere aprobación explícita de Jorge.

---

## 6. Sección especial: `vsigma_automerge_governance.yml`

Única vía por la que código entra a `main` **auto-aprobado**.

- **Trigger:** `pull_request` (opened, synchronize, reopened, labeled, ready_for_review). **No tiene `workflow_dispatch`.**
- **Permisos:** `contents: write`, `pull-requests: write`, `issues: write`. **Secret:** `GITHUB_TOKEN`.
- **Acción:** `gh pr merge "$PR" --merge --delete-branch` si pasan los gates; comenta el PR.
- **Gates:** label `automerge-safe` + no-draft + autor confiable (owner / `github-actions[bot]` / `codex[bot]` / `openai-codex[bot]`) + rama `vsigma-*` o `codex/*` + `check_automerge_guardrails.py` + `pytest tests/test_automerge_guardrails.py` + `git diff --check`.
- **Guardrail (`check_automerge_guardrails.py`):** default-deny.
  - **Permite:** prefijos `.github/workflows/`, `tests/`, `docs/`, `.codex/`, más exactos (`build_autonomous_monitoring_summary.py`, `dispatch_autonomous_monitoring_notification.py`, `build_daily_command_center.py`, **`check_automerge_guardrails.py`**, `README.md`, `AGENTS.md`).
  - **Bloquea:** todo `data/`, `.env`, cualquier ruta con "secret", `scripts/*` cuyo nombre contenga `scoring/score/model/prediction/calibration/selection/backtest/odds/enrich/filter/core/threshold/rank/market/result`, y por defecto todo lo no allowlisted.
  - ⇒ **No puede auto-mergear cambios a scoring/modelo/thresholds/gates/datos/secrets.** Buen diseño.
- **Riesgo residual (por esto es HIGH):**
  1. **Autorreferencial:** `check_automerge_guardrails.py` está en la allowlist → un PR podría debilitar el guardrail y auto-mergearse.
  2. **Workflows editables:** `.github/workflows/` allowlisted (el test `test_allows_github_workflow_changes` lo confirma con `vsigma_production.yml`) → un PR podría modificar cualquier workflow y auto-mergearse.
  3. **Tests editables:** `tests/` allowlisted → se podría neutralizar el test del guardrail.
  4. **Confianza en bots** `codex[bot]`/`openai-codex[bot]`. El gate real es el label `automerge-safe` (requiere permiso de escritura para ponerlo).
- **Recomendación:** AUDITAR MÁS + LIMITAR: sacar `check_automerge_guardrails.py`, `tests/` y `.github/workflows/` de la allowlist (o exigir aprobación humana para esas rutas); revisar branch protection y quién/qué puede poner `automerge-safe`.

---

## 7. Consumo de API y riesgo de cuota

**El agotamiento de cuota del 2026-06-12 es casi seguro consecuencia de la frecuencia de llamadas API, no de un fallo de credenciales.**

Workflows que consumen API (10):
`production`, `auto_api_board_batch`, `forced_api_board_fixture_lineups`, `daily_decision_chain_v2`, `live_trigger_validator`, `prelock_live_recheck` (posible), `prelock_official_lineup_recheck`, `full_post_match_learning_chain`, `post_match_refresh_calibration_chain`, `adhoc_fixture_forecast`, `smoke_test`.

Principales drivers de consumo:
- **`production` modo `auto` cada 30 min (~28 ciclos/día):** cada ciclo lanza `run_today_prelock_pipeline.py`, que ejecuta 4 pasos `enrich_*` (injuries, lineups, odds_context_v3, odds_structure_depth) + `capture_odds_snapshots`. Es el mayor consumidor.
- **`live_trigger_validator`:** ~11 ejecuciones/día.
- **`prelock_live_recheck` (6x) y `prelock_official_lineup_recheck` (4x):** llamadas repetidas en ventana de partido.
- **`auto_api_board_batch` (1x/día):** PRE + lineups forzados.

Notas:
- `run_vsigma_healthcheck.py` **NO** llama a la API de fútbol (solo lee archivos y detecta presencia de clave sin imprimirla).
- Varios de estos workflows pueden solaparse en el tiempo, multiplicando llamadas.
- **Acción recomendada (P1):** medir y reducir la frecuencia de `production auto` y de los prelock rechecks antes que tocar nada más. No cambiar lógica; solo cadencia de schedule, con aprobación de Jorge.

---

## 8. Workflows report-only (sin cambiar comportamiento)

Confirmado por lectura de scripts: escriben solo en `data/processed/` y los workflows hacen `git add` únicamente de rutas de report. **No editan** código, gates, thresholds, fórmulas ni registry.

- **Governor/advisory:** `self_improvement_governor`, `safe_action_dispatcher`, `data_quality_governor`, `autonomous_improvement_advisor`, `stat_calibration_governor`.
- **Shadow:** `shadow_registry_proposals`, `shadow_registry_sync` (no materializa registry real; `guardrail_status=SHADOW_REGISTRY_SYNC_REPORT_ONLY`), `shadow_experiment_factory`.
- **Formula patch (dry-run):** `formula_patch_governance` y sus scripts `build_formula_patch_dry_run_diff.py` / `_decision_gate.py` — los diffs son **texto comentado**, nunca se aplican; `auto_apply=NO`, `production_change=NO`.
- **Evidence/learning/issues:** `evidence_action_router`, `evidence_cleaner`, `evidence_closure_sequencer`, `learning_*`, `issue_alerts`, `pattern_promotion_readiness`, `failure_doctor`.
- **Reporting/ops:** `automation_health_monitor`, `mobile_operator_control_panel`, `operator_brief`, `context_*`, `match_stat_*`, `matrix_portfolio_v2`, `final_portfolio_verdict`, `objective_availability_gate`, `real_objective_context_gate`, `forecast_market_translator`, `calibration_memory_ledger`, `daily_execution_board`, `post_match_stat_calibration`.
- **Healthcheck:** `run_vsigma_healthcheck.py` — diagnóstico puro, no expone secretos.

---

## 9. Nombres engañosos

Dos workflows tienen nombres que sugieren capacidades que **no** poseen. Riesgo operativo (malentendido), no técnico.

- **`safe_auto_pr_generator`** — **NO crea PRs.** No invoca `gh`. Ejecuta `build_safe_auto_pr_generator.py`, que escribe un "plan de PR" (`vsigma_safe_auto_pr_plan.*`) scoped solo a reporting/ops (`ALLOWED_AREAS`: operator_brief/workflow_order/health/automation_health/issue_alert; `BLOCKED_AREAS` incluyen calibration/stake/market/odds/prediction) con `auto_merge=NO`, `pr_action=CREATE_REVIEW_ONLY_PR_PLAN`. Luego hace push directo a `main` del plan.
- **`safe_action_dispatcher`** — **NO ejecuta acciones/comandos.** El script `build_safe_action_dispatcher.py` rankea acciones manuales sugeridas y declara explícitamente: *"This dispatcher never auto-runs commands"* / *"report-only; operator must launch prelock manually."*

**Recomendación:** documentar/renombrar para evitar que se asuma creación de PRs o ejecución automática.

---

## 10. Recomendaciones priorizadas

### P0 — Crítico
- **Documentar `production.yml`** como motor real en `CLAUDE.md`/handoff (hoy es un hueco de gobernanza).
- **Endurecer `automerge_governance`:** sacar `check_automerge_guardrails.py`, `tests/` y `.github/workflows/` de la allowlist (o exigir aprobación humana en esas rutas); revisar branch protection y quién puede poner `automerge-safe`; reconsiderar la confianza en bots `codex`.
- **No tocar producción/gates/fórmulas/thresholds sin aprobación explícita de Jorge** (regla permanente).

### P1 — Importante
- **Reducir consumo API:** revisar y bajar la cadencia de `production auto` (cada 30 min) y de los prelock rechecks; medir llamadas por ciclo. Solo cambios de schedule, con OK de Jorge, sin tocar lógica.
- **Arreglar `[skip ci]`** en `prelock_official_lineup_recheck` (tiene trigger `push` y commitea sin `[skip ci]` → riesgo de auto-disparo) y revisar `operator_brief`.
- **Auditar las cadenas `workflow_run`** (`api_shadow_rule_ledger`, `prematch_calibration_rule_gate`, `forced_api_board_fixture_lineups`) para mapear qué disparan.

### P2 — Mejora documental
- **Renombrar/documentar** `safe_auto_pr_generator` y `safe_action_dispatcher` (nombres engañosos).
- **Inventariar los 287 scripts** de `scripts/` (este documento cubre workflows; falta el mapa de scripts).
- Mantener este documento actualizado cuando cambien workflows.

---

## 11. Reglas de operación para Claude

- `auto_bet: NO` y `production_change: NO` son mandatorios.
- Nunca colocar, automatizar ni disparar apuestas reales. `EXECUTE_*` = solo revisión manual.
- No exponer claves/secrets; no tocar `.env`/`.env.local`/GitHub Secrets salvo petición explícita de Jorge.
- No usar `git add .`; añadir solo archivos explícitos.
- No cambiar thresholds/gates/fórmulas/registry/producción sin razón de gobernanza documentada y aprobación de Jorge.
- No llamar "pick oficial" a nada que no salga de `production`/board oficial. Clasificar siempre: OFICIAL SISTEMA / SHADOW / API-BACKED / MANUAL-SINTÉTICO / NO DISPONIBLE / NO BET.
- No crear nuevos extractores API si el board/pipeline existente sirve.
- Si la cuota API está agotada, reportar `API_LIMIT_EXHAUSTED` y detener trabajo API-pesado.
- Preferir `NO_BET` cuando el edge es débil, el precio fino, el dato viejo o faltan gates.

---

## 12. Stop conditions

Detener y reportar/preguntar cuando:
- Cuota API agotada o clave inválida.
- Un workflow falla con error desconocido.
- Reports generados están viejos/stale.
- Un candidato requiere soporte de mercado no implementado.
- Un cambio tocaría thresholds/gates/fórmulas/producción/registry.
- El repo local tiene trabajo del usuario no commiteado e inesperado.
- Se detecta un PR con label `automerge-safe` que toca workflows/tests/guardrail.

---

## 13. Próximos pasos recomendados

1. **(P0)** Revisar y aprobar este inventario; luego commitearlo (commit explícito, `[skip ci]`).
2. **(P0)** Añadir `production.yml` al handoff/`CLAUDE.md` como motor principal.
3. **(P1)** Medir consumo API real por ciclo y proponer (sin aplicar) un ajuste de cadencia de schedule.
4. **(P1)** Plan de endurecimiento de `automerge_governance` (solo propuesta, revisión humana).
5. **(P2)** Inventario de los 287 scripts.
6. Continuar el plan de transición de 7 días (Día 2: verificación de entorno local; el `requirements.txt` está en UTF-16 — documentado, no corregido aún).

---

_Documento de auditoría. No modifica comportamiento del sistema. Generado en modo solo lectura; pendiente de revisión por Jorge antes de commit._
