# vSIGMA — Inventario de decluttering (mapa uso vs muerto)

> **READ-ONLY.** Este documento es solo INVENTARIO con evidencia. No borra, desactiva ni
> cambia nada. Generado el 2026-06-22 para planificar poda segura en sesiones siguientes.
> La fecha de última ejecución/modificación es **pista, no prueba**. Ver §Límites.

## Resumen de conteos

### Workflows (53 ficheros `.github/workflows/*.yml`)
| Cubo | n | Definición |
|---|---:|---|
| **ACTIVO** | ~31 | Trigger real (schedule/workflow_run/push/pull_request) + runs en junio-2026 |
| **DORMANT (superseded)** | ~13 | `active` pero solo `workflow_dispatch`, último run ~mayo-2026; su script vive vía la cadena v2/post-match |
| **DUDOSO** | ~8 | dispatch-only sin runs recientes, o `null` (nunca ejecutado), o herramienta on-demand / test |
| **MUERTO/disabled** | 1 | `vsigma_daily_decision_chain.yml` → `disabled_manually` + superseded por v2 |

> Nota: los runs del 2026-06-22 marcados `failure`/`skipped` son el **apagón de Actions por cuota**
> (jobs no arrancados), NO fallos reales de lógica. No cambia la clasificación de actividad.

### Scripts (321 `.py` en `scripts/` + `analysis/` + `tools/`)
| Cubo | n | Definición (conservadora) |
|---|---:|---|
| **ACTIVO (alcanzable)** | **241** | Invocado por un workflow (directo) o importado transitivamente por uno alcanzable |
| **DUDOSO** | **34** | Huérfano del grafo PERO importado por otro `.py`, o en `analysis/` (one-off), o invocado dinámicamente |
| **PROBABLEMENTE MUERTO** | **46** | Huérfano puro: NI en ningún workflow NI importado por alcanzable (requiere AMBAS) |
| Con invocación **dinámica** | 7 | Punto ciego del análisis estático (importlib / subprocess f-string / paths construidos) |

---

## 1. Workflows — clasificación con evidencia

### ACTIVO (trigger + runs recientes junio-2026)
`vsigma_production` (sched, 06-22) · `vsigma_daily_decision_chain_v2` (sched, 06-22) ·
`vsigma_worldcup_cards` (sched, 06-22) · `vsigma_failure_doctor` (workflow_run←Production, 06-22) ·
`vsigma_api_shadow_rule_ledger` (workflow_run←v2) · `vsigma_forced_api_board_fixture_lineups` (workflow_run←v2) ·
`vsigma_prematch_calibration_rule_gate` (workflow_run←forced_lineups) · `vsigma_auto_api_board_batch` (sched) ·
`vsigma_automation_health_monitor` · `vsigma_autonomous_improvement_advisor` · `vsigma_data_quality_governor` ·
`vsigma_evidence_action_router` · `vsigma_evidence_cleaner` · `vsigma_evidence_closure_sequencer` ·
`vsigma_full_post_match_learning_chain` · `vsigma_issue_alerts` · `vsigma_learning_evidence_closer` ·
`vsigma_learning_issue_lifecycle` · `vsigma_learning_residual_quarantine` · `vsigma_live_trigger_validator` ·
`vsigma_mobile_operator_control_panel` · `vsigma_operator_brief` · `vsigma_pattern_promotion_readiness` ·
`vsigma_prelock_live_recheck` · `vsigma_prelock_official_lineup_recheck` · `vsigma_safe_action_dispatcher` ·
`vsigma_safe_auto_pr_generator` · `vsigma_self_improvement_governor` · `vsigma_shadow_experiment_factory` ·
`vsigma_shadow_registry_sync` · `vsigma_automerge_governance` (pull_request).

### DORMANT — workflow standalone superseded (el SCRIPT sigue ACTIVO vía la cadena v2/post-match)
Solo `workflow_dispatch`, último run ~2026-05-24/25. Cada uno envuelve **un** script que la cadena
consolidada (`daily_decision_chain_v2` o `full_post_match_learning_chain`) ya invoca directamente:

| Workflow | Último run | Script que envuelve | El script está… |
|---|---|---|---|
| `vsigma_context_adjusted_final_picks` | 05-25 | `build_context_adjusted_final_picks.py` | ACTIVO vía v2 |
| `vsigma_context_level_matrix` | 05-25 | `build_context_matrix.py` | ACTIVO vía v2 |
| `vsigma_daily_execution_board` | 05-25 | `build_daily_execution_board.py` | ACTIVO vía v2 |
| `vsigma_forecast_market_translator` | 05-25 | `build_forecast_market_translator.py` | ACTIVO vía v2 |
| `vsigma_match_stat_forecasts` | 05-25 | `build_match_stat_forecasts.py` | ACTIVO vía v2 |
| `vsigma_match_stat_forecast_backtest` | 05-25 | `backtest_match_stat_forecasts.py` | ACTIVO vía v2 |
| `vsigma_matrix_portfolio_v2` | 05-25 | `build_context_matrix_portfolio.py` | ACTIVO vía v2 |
| `vsigma_objective_availability_gate` | 05-25 | `build_objective_availability_gate.py` | ACTIVO vía v2 |
| `vsigma_real_objective_context_gate` | 05-25 | `build_real_objective_context_gate.py` | ACTIVO vía v2 |
| `vsigma_post_match_stat_calibration` | 05-25 | `build_post_match_stat_actuals.py` + `calibrate_…` | ACTIVO vía post-match chain |
| `vsigma_post_match_refresh_calibration_chain` | 05-25 | (4 scripts post-match) | ACTIVO vía post-match chain |
| `vsigma_stat_calibration_governor` | 05-25 | `build_stat_calibration_governor.py` | ACTIVO vía post-match chain |
| `vsigma_calibration_memory_ledger` | 05-25 | `build_calibration_memory_ledger.py` | ACTIVO vía post-match chain |

> **Implicación de poda:** retirar/desactivar estos 13 **workflows** es de bajo riesgo (su función vive
> en la cadena), pero **NO borrar sus scripts** (siguen activos). Verificar antes que ninguno se lanza a mano.

### DUDOSO (necesitan comprobación manual)
| Workflow | Trigger | Último run | Por qué dudoso |
|---|---|---|---|
| `vsigma_adhoc_fixture_forecast` | dispatch | 06-11 | Herramienta **on-demand** legítima (forecast puntual). Mantener. |
| `vsigma_smoke_test` | dispatch+push | 05-15 | Test CI (push path-filtered). ¿Sigue útil? |
| `vsigma_context_adjustment_result_auditor` | dispatch | 05-24 | Su script `build_context_adjustment_result_auditor.py` **no** está en ninguna cadena activa |
| `vsigma_context_filter_advisor` | dispatch | 05-24 | `build_context_filter_calibration_advisor.py` no en cadena activa |
| `vsigma_final_portfolio_verdict` | dispatch | 05-24 | `build_final_portfolio_verdict.py` no en cadena activa |
| `vsigma_shadow_registry_proposals` | dispatch | **nunca** | `build_shadow_registry_proposals.py` no en cadena activa |
| `vsigma_formula_patch_governance` | dispatch | **nunca** | 7 scripts formula_patch; ninguno en cadena activa |
| `vsigma_official_today_picks_mobile` | dispatch | **nunca** | Reciente, nunca ejecutado; `build_official_today_picks_mobile.py` huérfano |

### MUERTO / disabled
| Workflow | Estado | Evidencia |
|---|---|---|
| `vsigma_daily_decision_chain.yml` (v1) | `disabled_manually` | Superseded por `…_v2`; le quitamos el `schedule` (commit 87dbfa56); queda solo `workflow_dispatch`. **Sus scripts NO son dead**: todos están también en v2. |

---

## 2-3. Scripts — 3 cubos con evidencia

### PROBABLEMENTE MUERTO (46) — huérfanos puros (ni workflow ni import alcanzable)
Agrupados por patrón (evidencia adicional entre paréntesis):

**Temporales por nombre (`_tmp`) — los MÁS seguros:**
`build_under35_market_crosscheck_tmp.py` · `build_under35_shadow_report_tmp.py` ·
`train_vsigma_binary_market_models_tmp.py`

**Versiones viejas superseded (la versión nueva SÍ está activa):**
`build_fixture_api_coverage_matrix.py` + `…_v2.py` (activo: `…_v3.py`) ·
`apply_fixture_api_coverage_gate_to_board.py` (activo: `…_v2.py`) ·
`enrich_odds_context.py` + `…_v2.py` (existe `…_v3.py`) ·
`build_shadow_forecast_ab_simulator.py` (activo: `…_v2.py`)

**Evaluaciones históricas one-off:**
`run_candidate_v4_historical_evaluation.py` · `…_v5…` · `…_v6…` · `…_v7…` ·
`run_extended_historical_evaluation.py` · `run_odds_structure_depth_historical_evaluation.py` ·
`run_recent_lab_historical_evaluation.py`

**Entrenamiento / datasets one-off:**
`train_vsigma_stat_models.py` · `train_vsigma_statistical_baseline.py` · `build_modeling_dataset_api.py` ·
`build_top5_dataset_chunked.py` · `build_football_data_uk_dataset.py` · `build_learning_backfill.py` ·
`apply_vsigma_ml_shadow_forecast.py` · `evaluate_vsigma_ml_agreement.py` · `evaluate_vsigma_market_blend.py`

**Utilidades de odds / datos sueltas:**
`cache_odds_reference.py` · `inspect_odds_reference.py` · `rebuild_odds_snapshots_for_date.py` ·
`enrich_odds_context*` (arriba) · `refresh_finished_results.py` · `score_matches.py` ·
`add_country_to_matches.py` · `audit_numeric_data.py` · `sanitize_fake_zeros.py` ·
`create_manual_stats_template.py` · `check_api_plan.py` · `enrich_recent_form.py`

**Gates / coverage diagnósticos sueltos:**
`apply_proxy_bridge_calibration_guard.py` · `build_api_enrichment_allowlist_dry_run.py` ·
`build_fixture_scoring_coverage_repair_diagnostic.py` · `build_real_source_coverage_expander.py` ·
`build_root_fixture_feed_expansion_diagnostic.py` · `build_vsigma_drift_monitor.py` ·
`build_adhoc_postmatch_learning_all.py` · `evaluate_gate_stability_splits.py` ·
`evaluate_team_total_gates_by_league.py` · `evaluate_u35_gate_by_league.py`

### DUDOSO (34) — NO marcar como muerto sin comprobación
- **`analysis/worldcup/watchdog.py`** ⚠️ — **ACTIVO de hecho**: lo ejecuta **Windows Task Scheduler**
  (`vSIGMA_WorldCup_Watchdog`), invisible al grafo (no lo invoca ningún `.yml`/`.py`). **NO TOCAR.**
  Igual para `analysis/worldcup/run_local_daily.ps1` (tarea `vSIGMA_WorldCup_LocalDaily`; no es `.py`, fuera del conteo).
- **Estudios offline `analysis/` (one-off de investigación):** `dixon_coles_offline.py`,
  `expected_stats_model_offline.py`, `precision_offline_analysis.py`, `predictability_scan_offline.py`,
  `corners_cards_market_signal.py`, `product_forecast_card_prototype.py`, `stat_forecaster_prototype.py`,
  `four_input_rating_validation.py`, `xg_vs_proxy_validation.py`, `validate_seriebr_model.py`,
  `extract_premier_xg.py`, `extract_seriebr_stats.py`. — Soportan análisis ya documentados (memoria);
  conservar como referencia, no son pipeline.
- **Lineaje del modelo Mundial (`analysis/worldcup/`):** `extract_*`, `national_elo_*`, `squad_*`,
  `feature_study_*`, `sharpening_study.py` (+ su `test_…`). Construyeron el modelo que hoy sirve la
  worldcup card; dormidos pero parte del producto. Conservar.
- **Importados por otro `.py` (no huérfanos reales):** `backtest_vsigma.py`,
  `build_adhoc_postmatch_learning_ledger.py`, `build_execution_mode_comparison.py`,
  `build_historical_execution_shortlist_backtest.py`, `build_vsigma_historical_dataset.py`,
  `calibrate_vsigma_thresholds.py`, `run_historical_labeling_pipeline.py`,
  `run_vsigma_backtest_calibration.py`. — Alguien los importa; comprobar si ese alguien es alcanzable.

### ACTIVO (241) — ejemplos de utilidades compartidas (evidencia de por qué NO son dead)
- `scripts/dispatch_telegram_alert.py` — usado por `worldcup_cards`, `failure_doctor`, `issue_alerts`.
- `scripts/api_football_client.py` — usado por `auto_api_board_batch` (+ importado por el cliente API).
- `scripts/run_daily_competition_controller.py` — `production` + `auto_api_board_batch`.
- `analysis/worldcup/{build_worldcup_cards,build_worldcup_full_card,worldcup_learning_loop}.py` — `worldcup_cards`.
- Los ~40 scripts de la cadena `daily_decision_chain_v2` y los ~30 de `full_post_match_learning_chain`.

---

## 4. Duplicados / superseded, sin-trigger, experimentales

**Pares versionados (vieja muerta · nueva activa):**
- `build_fixture_api_coverage_matrix` `.py`/`_v2` ❌ · `_v3` ✅
- `apply_fixture_api_coverage_gate_to_board` `.py` ❌ · `_v2` ✅
- `enrich_odds_context` `.py`/`_v2` ❌ · `_v3` ✅
- `build_shadow_forecast_ab_simulator` `.py` ❌ · `_v2` ✅
- `daily_decision_chain` **workflow** v1 (disabled) · **v2** activo

**Workflows sin trigger efectivo:** `daily_decision_chain.yml` (disabled_manually; tras nuestro cambio
solo `workflow_dispatch`).

**Workflows nunca ejecutados (`null`):** `formula_patch_governance`, `shadow_registry_proposals`,
`official_today_picks_mobile`.

**Experimentales / one-off (`analysis/`):** todos los `analysis/*.py` y `analysis/worldcup/*model*`,
`*study*`, `extract_*` — estudios de investigación, no pipeline de producción.

---

## 5. LÍMITES del análisis (dónde el estático NO llega)

1. **Windows Task Scheduler** (local): `watchdog.py` y `run_local_daily.ps1` se ejecutan desde tareas
   locales, **no** desde ningún `.yml`/`.py`. El grafo los ve como huérfanos → marcados DUDOSO, **no** muertos.
2. **Invocación dinámica** (7 scripts): `importlib`, `subprocess(... f"...")`, o paths `.py` construidos con
   variables. Si alguno llama por nombre construido a un script de la lista "muerta", el grafo no lo ve:
   `scripts/select_core_candidates.py`, `scripts/create_manual_stats_template.py`,
   `scripts/enrich_recent_form.py`, `analysis/validate_seriebr_model.py`,
   `analysis/worldcup/{squad_blend_model_v2,squad_strength_model}.py`, `analysis/xg_vs_proxy_validation.py`.
3. **`workflow_dispatch` manual**: cualquier workflow dormant puede lanzarse a mano; "sin runs recientes"
   no es "inútil".
4. **Fecha git** = pista, no prueba. Un script viejo puede seguir siendo el activo.
5. Referencias en **docs/markdown/notebooks** no cuentan como uso de ejecución y no se rastrearon como edges.

---

## 6. Candidatos OBVIOS y seguros a retirar PRIMERO (orden de menor riesgo)

> Aun así: **proponer → aprobar → aplicar** en sesión aparte. Esto es solo el shortlist.

1. **`*_tmp.py` (3):** `build_under35_market_crosscheck_tmp.py`, `build_under35_shadow_report_tmp.py`,
   `train_vsigma_binary_market_models_tmp.py`. — Temporales por nombre, huérfanos puros.
2. **Versiones viejas con sucesor activo (4-5):** `build_fixture_api_coverage_matrix.py` + `_v2`,
   `apply_fixture_api_coverage_gate_to_board.py`, `enrich_odds_context.py` + `_v2`,
   `build_shadow_forecast_ab_simulator.py`. — La `vN` nueva es la que corre.
3. **Evaluaciones históricas one-off (7):** `run_candidate_v4/v5/v6/v7_historical_evaluation.py`,
   `run_extended_/run_odds_structure_depth_/run_recent_lab_historical_evaluation.py`.
4. **Workflows DORMANT superseded (13):** desactivar (no borrar) los standalone de §1 cuyo script ya vive
   en v2 — reduce ruido de Actions sin tocar funcionalidad. **Conservar sus scripts.**

**Verificación previa imprescindible antes de borrar cualquier "muerto":** `grep -r "<nombre_sin_.py>"`
sobre todo el repo (incluye los 7 dinámicos y docs) para descartar invocación por string. Y nunca tocar
los DUDOSO (§3), en especial `watchdog.py`.
