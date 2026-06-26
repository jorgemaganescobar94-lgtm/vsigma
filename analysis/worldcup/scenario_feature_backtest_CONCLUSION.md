# Motor de clasificación correcto + escenario como FEATURE aprendida

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API
**Script:** `analysis/worldcup/scenario_feature_backtest.py`
**Salidas:** `..._report.txt`, `..._metrics.csv`

Extiende el harness del backtest de contexto (`context_shadow_backtest`): misma muestra (última jornada
de grupo de torneos de selecciones), ratings L3 walk-forward, calibración congelada, anti-leakage
(standings de jornadas previas). Reutiliza `reconstruct_groups`/`WFRatings`/`l3_offline`, no los duplica.

## PARTE 1 — Motor de clasificación (correcto, desempates FIFA)
Por equipo, en la última jornada de un grupo de 4: enumera las 9 combinaciones de resultados restantes
(su partido W/D/L × el partido PARALELO W/D/L), calcula los puntos finales y aplica el orden real
(puntos → diferencia de goles → goles a favor → head-to-head). Como GD/GF dependen de marcadores
desconocidos, un **empate a puntos en la frontera** se marca `gd_dependent` (lo decidiría GD/GF/h2h), no
se afirma. Mejores terceros por formato (6 grupos → top-2 + 4 terceros; 12 → top-2 + 8; resto solo
top-2), con cota cross-group conservadora usando las tablas de TODOS los grupos.

**Features por equipo:** `qualified, eliminated, controls_destiny, draw_enough, must_win,
depends_on_others, gd_dependent, alive_as_third`.

**Validación (casos construidos, todos correctos):**

| caso | salida del motor |
|---|---|
| clasificado cierto (A=6, nadie llega) | **qualified** |
| le vale el empate (A=4, paralelo techo 4) | **draw_enough** (controls_destiny) |
| debe ganar (solo ganando entra) | **must_win** (controls_destiny) |
| todos parejos | **depends_on_others** (+gd_dependent) |
| 4º seguro (otros 3 por encima de su techo) | **eliminated** |
| 3º por puntos, formato 6 grupos | **alive_as_third** (NO eliminated) |

El motor distingue correctamente control-propio / depende-de-otro / GD / mejor-tercero.

## PARTE 2 — Escenario como FEATURE aprendida (no multiplicador fijo)
Se añaden las features al modelo de goles y el ajuste **aprende** su efecto en burn-in (<2024):
`log((goles+0.5)/(xG_L3+0.5)) ~ features`. OOS (≥2024) se compara feature vs baseline (xG L3 solo) en
goles (Poisson dev), Over2.5, BTTS y 1X2. Bootstrap pareado IC95%.

**Muestra:** 162 partidos / 324 team-matches · burn-in 188 · **OOS 136** (68 partidos pareados).
Features muy **colineales** (`gd_dependent` activa en 174/188 burn-in).

**Resultados OOS (Δ = baseline − feature; >0 con IC95% que excluye 0 = la feature mejora):**

| modelo | Goles dev (base→feat) | Over2.5 Δ | BTTS Δ | 1X2 Δ |
|---|---|---|---|---|
| FULL (8 flags, OLS) | 167 → **207 (peor)** | −0.113 (n.s.) | **−0.184 SIGNIF (peor)** | −0.049 (n.s.) |
| FULL + ridge | 167 → **183 (peor)** | −0.043 (n.s.) | **−0.099 SIGNIF (peor)** | −0.014 (n.s.) |
| PARSIMONIOSO (low_stakes + must_win) | 167 → 167 (≈igual) | −0.002 (n.s.) | −0.032 (n.s.) | +0.009 (n.s.) |

- Los modelos ricos (full, ridge) **SOBREAJUSTAN** y **empeoran OOS** de forma **significativa en BTTS**
  (las features colineales aprenden ruido en burn-in que no generaliza).
- El modelo **parsimonioso** (que no puede sobreajustar) es **NEUTRAL**: ningún delta significativo en
  ninguna métrica. No hay señal.

## (c) ¿Mejora la feature de escenario?
**NO.** En el mejor caso (parsimonioso) es neutral (cero mejora significativa); en los ricos, empeora
(BTTS significativamente). El 1X2 nunca mejora. Es **coherente con el hallazgo previo** del escenario
como multiplicador fijo (no significativo): la calidad del rival y la fuerza ya están en el xG L3, y el
escenario de clasificación **no aporta poder predictivo marginal** al modelo de goles/1X2.

La muestra es modesta (OOS 68 partidos) — pero la conclusión es robusta: el test parsimonioso, que NO
puede sobreajustar, no muestra señal, y los tests ricos empeoran. No es solo "insuficiente": no hay
indicio de mejora en ninguna especificación razonable.

## (d) Recomendación honesta
- **NO integrar el escenario como FEATURE del modelo.** No mejora la predicción OOS (la empeora si el
  modelo es rico, neutral si es parsimonioso). El xG L3 ya captura lo predictivo.
- **El MOTOR sí es valioso como INFORMACIÓN, no como input del modelo.** Ahora es correcto (desempates
  FIFA, mejores terceros, control-propio/depende-de-otro). Si se quiere, podría MOSTRARSE en la ficha
  como contexto ("le vale el empate", "debe ganar", "vivo como mejor tercero") — etiqueta informativa
  honesta, separada de la predicción probabilística. Eso NO toca el modelo y no arrastra el sobreajuste.
- En resumen: **escenario = información para el lector, no feature del modelo.** Queda en sombra como
  motor de clasificación correcto; no entra en la predicción.

## Anti-leakage
Standings de jornadas previas (mismo grupo); ratings L3 walk-forward (`date<partido`); coeficientes de
la feature ajustados SOLO en burn-in; calibración congelada; target solo para puntuar. Sin API.

## Limitaciones
- OOS modesto (68 partidos pareados); features muy colineales (gd_dependent ~90%).
- Mejores terceros con cota cross-group conservadora (no enumeración exacta entre grupos) — documentado.
- Modelo de goles log-lineal simple (OLS sobre log-ratio); un Poisson-GLM regularizado daría resultados
  parecidos dado que el parsimonioso ya es neutral.
