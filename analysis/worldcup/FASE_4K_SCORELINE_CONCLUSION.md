# Fase 4K — Distribución de marcadores top-3/5 + evaluación (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada (salida derivada + medición; **modelo base NO modificado**) · **Aislamiento:** producto Mundial.

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA externo, sin clima real. NO toca `data/external`.
**No cambia xG/λ base, pesos, modelo 1X2, modelo de goles ni predicciones existentes.**

## Qué hace

1. `build_worldcup_scoreline_distribution.py` — para cada fixture con goles esperados numéricos, construye
   una rejilla Poisson independiente (0..10 por lado), los **top-5 marcadores** y el **1X2 implícito** por
   la distribución (sanity check). Prioridad de λ: `inj_xg > ctx_xg > mx_xg > l3_xg > our_xg`; `safe_num`
   evita el bug de strings (`inj_home`/`inj_away`). Sin λ → fixture no generado (no_evaluable).
2. `evaluate_worldcup_scoreline_distribution.py` — mide la distribución contra resultados reales.
3. Integra en Fase 4J: el módulo **"Marcadores top-3/5"** deja de ser NO_DISPONIBLE → **ACTIVO**.

## Resultados (dato real)

- **Fixtures con distribución:** 55/55 (44 liquidados + 11 próximos).
- **Acierto de marcador exacto (44 liquidados):** top-1 **11.4%** · top-3 **36.4%** · top-5 **52.3%**.
- Prob. media del marcador real **0.078** · rank medio del marcador real **6.98** (44/44 dentro de rejilla).
- **1X2 derivado de la distribución:** accuracy **0.682** — **idéntico** al 1X2 directo del modelo
  (sanity check OK; la Poisson reproduce el 1X2 del modelo).
- **Goles (MAE desde λ):** home 1.07 · away 0.78 · total **1.56** · bias total −0.20 — consistente con
  el módulo de goles de 4J.

## Ejemplo de salida (Telegram opcional)
```
🎯 Marcadores probables (Poisson sobre xG, conf. media)
  1. 1-1 — 12%
  2. 1-0 — 11%
  3. 2-1 — 9%
```
(De momento NO se ha añadido al Telegram principal; queda como salida estructurada + evaluación. Si se
añade, será sin lenguaje de apuestas y con fuente/confidence explícitas.)

## Artefactos
- `worldcup_scoreline_distribution.csv` (fila por marcador top-5 por fixture) — **auto-commiteado en CI**.
- `worldcup_scoreline_evaluation.csv` (fila por fixture evaluado) — **auto-commiteado en CI**.
- `*_distribution.json` / `*_evaluation_summary.json` / `*_report.txt` — gitignored (regenerables).

## Tests
`analysis/worldcup/test_worldcup_scoreline_distribution.py` (12 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **556 passed**.

## Qué queda para Fase 4L
- (Opcional) añadir la sección "Marcadores probables" al Telegram de player-events (sin apuestas).
- Crear scorecard de SOT de equipo para activar ese último módulo NO_EVALUABLE de 4J.
- Medir una corrección de nivel para tiros de equipo (infra) y tiros a puerta por jugador (sobre),
  siempre con el patrón medir → anti-look-ahead → shadow antes de tocar pesos.
