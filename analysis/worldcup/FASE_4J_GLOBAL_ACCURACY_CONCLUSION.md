# Fase 4J — Evaluación global de precisión predictiva (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada (solo medición; **nada modificado**) · **Aislamiento:** producto Mundial.

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA externo, sin clima real. NO toca `data/external`.
**No cambia pesos, modelos, predicciones, Telegram ni fuentes externas.**

## Qué hace

`analysis/worldcup/evaluate_worldcup_prediction_accuracy.py` mide TODOS los outputs principales del
producto contra resultados reales liquidados y los presenta en un panel con estado
(ACTIVO / SHADOW / NO_EVALUABLE / INSUFFICIENT_SAMPLE) y recomendación por módulo. Usa `safe_prob`
(ignora valores no numéricos — sin repetir el bug `inj_home`/`inj_away`). Donde un output no existe
todavía (p. ej. distribución de marcadores), se marca `NO_DISPONIBLE` — nunca se inventa.

Fuentes: `worldcup_predictions_log.csv` (1X2 + goles), `worldcup_player_props_log.csv` (jugadores),
`worldcup_team_stats_scorecard.csv` (team stats), `worldcup_card_risk_shadow_monitor.json` (shadow).

## Resultados (dato real)

| Módulo | Estado | n | Métrica | Sesgo |
|---|---|---|---|---|
| Resultado 1X2 | ACTIVO | 44 | accuracy **0.682** (Brier/LogLoss multiclase) | real H18/D10/A16 |
| Goles/marcador | ACTIVO | 44 | MAE total **1.56** | infra −0.20 |
| Jugadores: gol | ACTIVO | 418 | Brier **0.068** | leve sobre (avg 9.1% vs real 7.7%) |
| Jugadores: asistencia | ACTIVO | 418 | Brier **0.059** | leve sobre (7.0% vs 6.0%) |
| Jugadores: tiros a puerta | ACTIVO | 418 | Brier **0.147** | **sobre** (28.6% vs 18.9%) |
| Jugadores: tarjetas | ACTIVO | 418 | Brier **0.093** | **sobre** (16.4% vs 9.3%) |
| Jugadores: nº tiros | ACTIVO | 418 | MAE **0.74** | sobre +0.27 |
| Team stats: córners | ACTIVO | 39 | MAE **2.53** | **infra** −1.39 |
| Team stats: tiros | ACTIVO | 39 | MAE **7.42** | **infra** −6.05 |
| Team stats: tarjetas | ACTIVO | 39 | MAE **1.91** | **sobre** +1.56 |
| Team stats: SOT | NO_EVALUABLE | — | sin scorecard de SOT de equipo | — |
| Ajuste riesgo de tarjeta (4F-4I) | SHADOW | 418 | ΔBrier pre_fixture −0.0001 | sin señal real |

## Conclusión ejecutiva

- **Mejor señal:** RESULTADO 1X2 (68% acierto) y goles (MAE total 1.56). Gol/asistencia por jugador
  bien calibrados.
- **Peor / sesgos a vigilar:** sobrepredicción de **tiros a puerta**, **tarjetas** (jugador y equipo) y
  nº de tiros; **infrapredicción** fuerte de **tiros de equipo** (bias −6.05) y córners (−1.39).
- **Shadow:** el ajuste de riesgo de tarjeta (no aporta señal real sin look-ahead).
- **No evaluable:** SOT de equipo (no hay scorecard) y top-3/5 de marcadores (no hay distribución).
- **Prioridad siguiente (antes de añadir fuentes externas):** estructurar una salida de
  **distribución de marcadores** (para top-3/5) y un **scorecard de SOT de equipo**, y seguir
  acumulando muestra de props por jugador. Las calibraciones de tiros/tarjetas (sobre) y tiros de
  equipo (infra) son los candidatos más claros a corrección de nivel — pero **medir antes de tocar**.

## Artefactos
- `worldcup_prediction_accuracy.csv` (una fila por módulo) — **auto-commiteado en CI**.
- `worldcup_prediction_accuracy_summary.json` + `_report.txt` — gitignored (regenerables).

## Tests
`analysis/worldcup/test_worldcup_prediction_accuracy.py` (12 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **544 passed**.

## Qué queda para Fase 4K
- Implementar la salida de distribución de marcadores (top-3/5) y su evaluación.
- Crear scorecard de SOT de equipo para activar ese módulo.
- Evaluar/medir una corrección de nivel para tiros de equipo (infra) y tiros a puerta por jugador
  (sobre) — siempre con el patrón medir → anti-look-ahead → shadow antes de tocar pesos.
