# Squad-quality (player-based) strength × L3 — ¿añade poder predictivo OOS? CONCLUSIÓN

**Read-only · sin cambios en producción · sin API.** Script: `squad_quality_blend_backtest.py`
(reutiliza `context_shadow_backtest.WFRatings`, `props_retest_stats_inputs.team_rates`, helpers L3).

## (a) Cómo se construyó la fuerza-por-jugadores y la comparabilidad entre ligas
- **Métrica:** `games.rating` NO está en la caché de props (solo `minutes,g90,a90,sh90,son90,c90,on_ratio`)
  y traerlo costaría API (cuota = zona roja). Por el fallback de la propia tarea, se usó un **compuesto
  ofensivo** de las tasas /90 de **selección 2023**: `q_p = z(g90) + 0.5·z(a90)`, con **shrinkage por
  minutos** `rate·m/(m+270)` (colapsa las tasas-fluke de pocos minutos hacia 0).
- **Agregación a equipo (documentada):** `avg` = media ponderada por minutos sobre la plantilla;
  `topN` = media de los 14 con más minutos (proxy de XI de facto); `min` = concentración de minutos
  top-N (control NO ofensivo). Feature = `squad_diff = fuerza(local) − fuerza(visitante)`.
- **Comparabilidad entre ligas (el riesgo principal):** las tasas son de **partidos de selección**
  (escala internacional común), NO `games.rating` de club → el problema "7.0 en 2ª ≠ 7.0 en Premier"
  **NO afecta** a esta métrica. Limitación residual honesta: g90/a90 son **ofensivos** (defensas/porteros
  puntúan bajo); el ponderado por minutos corrige parcialmente por rol. El control no-ofensivo (`min`)
  también se midió.
- **Ruido de muestra pequeña (medido y mitigado):** sin shrinkage, selecciones minúsculas (St. Vincent,
  Dominica, islas con 2-14 jugadores cacheados) encabezaban el ranking por un g90 fluke. Con shrinkage
  K=270 el **top-N** ordena bien (Irán, Japón, Egipto, Senegal, Nigeria arriba). `avg` sobre rosters
  minúsculos sigue ruidoso → **top-N es la agregación robusta**.

## (b) Métricas candidato vs baseline OOS (con significancia)
Faithful a L3: `margin = a0 + a1·sup_L3 [+ a2·squad_diff]` por lstsq en **burn-in 2024** → Poisson →
isotónica (burn-in) → evaluado **OOS 2025**. Muestra: 759 partidos entre 2 equipos cacheados
(442 burn-in / 317 OOS). `corr(sup_L3, sqd_avg)=+0.35`.

| modelo (OOS, n=317) | logloss | brier | ECE | acc% | a2 | Δlogloss(base−cand) IC95% |
|---|---|---|---|---|---|---|
| baseline [sup_L3] | **0.90684** | **0.54521** | 0.024 | 53.9 | — | (ref) |
| + sqd_avg | 0.91493 | 0.54832 | 0.065 | 51.4 | −0.178 | −0.0081 [−0.022,+0.006] no signif |
| + sqd_top14 | 0.91081 | 0.54692 | 0.046 | 54.3 | −0.122 | −0.0040 [−0.015,+0.007] no signif |
| + sqd_min (ctrl) | 0.91828 | 0.55257 | 0.051 | 53.6 | −1.357 | −0.0114 [−0.030,+0.007] no signif |

- **Ningún** scoring propio (logloss/brier) mejora; todos los puntos son **negativos** (candidato algo
  peor) y todos los **IC95% incluyen 0**. La accuracy del top-N sube 0.4 pp (~1 partido, ruido).
- **Subgrupo "pocos partidos recientes"** (min(local,visit) internacionales en 365d previos; mediana=11):
  - thin (n=232): Δlogloss = −0.0073, IC95 [−0.025,+0.011] → **no signif**.
  - thick (n=85): Δlogloss = −0.0102, IC95 [−0.027,+0.007] → **no signif**.
  - La hipótesis era más fuerte aquí y **tampoco se sostiene**.
- Over 2.5: total constante e igual entre modelos → sin señal añadida (el squad solo mueve el reparto).

## (c) ¿El peso aprendido es significativo y mejora OOS, o el L3 ya lo captura?
**El L3 ya lo captura.** El peso `a2` es pequeño y **negativo** (−0.12 top-N), no positivo como predecía
la hipótesis; con la métrica cruda era −0.51, y el shrinkage (quitar ruido minnow) lo acercó a 0 →
gran parte de la "señal" cruda era ruido de muestra pequeña. OOS el candidato **no mejora** en ninguna
métrica propia, ni global ni en el subgrupo favorable. La correlación `sup_L3 ~ squad` (+0.35) confirma
que el rating de resultados ya incorpora buena parte de la calidad de plantilla.

## (d) Recomendación honesta: **DESCARTAR** (con un caveat acotado)
- **Descartar** integrar la fuerza-por-jugadores (compuesto ofensivo de selección) al 1X2/goles:
  no añade poder predictivo OOS distinguible de 0, ni siquiera donde la hipótesis es más fuerte.
- **Caveat acotado (no invalida el null):** el compuesto es ofensivo y de baja resolución para naciones
  con pocos datos. Un rating de jugador **integral** (`games.rating` de temporada de club, defensa
  incluida) podría re-testearse, pero exige **API** (cuota) **+ estandarización entre ligas** (el riesgo
  que aquí se evitó). Dado que (i) el L3 ya correlaciona con y subsume el compuesto y (ii) no hay señal
  ni en el corte favorable, la carga de la prueba para volver a intentarlo es alta.
- **No se cambia producción.** Análisis versionado (script + report + metrics + rows).
