# Backtest del contexto de clasificación — RE-CORRIDO con classify_fixture corregido

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API
**Script:** `analysis/worldcup/context_shadow_backtest.py` (importa el `classify_fixture` nuevo)
**Salidas:** `..._report.txt`, `..._rows.csv`, `..._metrics.csv`
**Sustituye** a la CONCLUSION anterior (lógica vieja/errónea, obsoleta).

## Qué cambió
`classify_fixture` se reconstruyó: ahora afirma un escenario NO neutral SOLO cuando es
**matemáticamente cierto por puntos** (enumerador del partido paralelo en la última jornada; respeta
mejores terceros y desempates → si dependen de GD/ajenos, NEUTRAL). El backtest se re-ejecutó tal
cual, mismo universo (17 torneos-temporada de selecciones, K4 limpio), mismo anti-leakage (standings
de jornadas previas, ratings L3 walk-forward, calibración congelada). 162 partidos de última jornada;
sin cambio de muestra, solo cambia el etiquetado.

## (a) Partidos NO triviales: 162 → **81** (la mitad)

| | Clasificador VIEJO (obsoleto) | Clasificador NUEVO (cierto por puntos) |
|---|---|---|
| no triviales (mult≠1.0) | **162** | **81** |

**Distribución por escenario** (sobre ambos equipos, 324 etiquetas) con el clasificador nuevo:

| escenario | nº | mult | ¿ajusta? |
|---|---|---|---|
| tercero_en_disputa | 207 | ×1.0 | no (neutral) |
| le_vale_empate | 58 | ×0.97 | sí |
| ya_clasificado | 33 | ×0.92 | sí |
| intrascendente | 22 | ×1.0 | no (dead rubber) |
| partido_decisivo | 3 | ×1.0 | no |
| eliminado | 1 | ×0.95 | sí |
| debe_ganar | 0 | — | nunca (inalcanzable en grupo de 4) |

Lo esperado: el clasificador estricto manda la mayoría a **neutral** (tercero_en_disputa, ×1.0) y
solo etiqueta lo cierto. Quedan dos escenarios con muestra real (le_vale_empate 58, ya_clasificado
33); `eliminado` casi no aparece (1) y `debe_ganar` no aparece (demostrablemente inalcanzable).

## (b) Métricas context-adjusted vs L3 puro (solo no triviales, N=81)

| corte | n | Δlogloss | Δbrier | acc L3→ctx | ¿ctx bate? |
|---|---|---|---|---|---|
| **GLOBAL** | 81 | **+0.0117** | **+0.0066** | 45.7→44.4% | sí (nominal) |
| le_vale_empate (×0.97) | 58 | +0.0157 | +0.0091 | 44.8→43.1% | sí |
| ya_clasificado (×0.92) | 33 | +0.0085 | +0.0053 | 48.5→48.5% | sí |
| eliminado (×0.95) | 1 | −0.069 | −0.038 | — | no (n=1, ruido) |

(Δ = L3 − ctx; positivo = ctx mejora.) Over 2.5: ctx mejora (logloss 0.6938→0.6868).

**Significancia (bootstrap pareado, 20000 resamples, semilla fija):**
- Δlogloss media **+0.0117** (1.05% del L3); ctx mejor en **46% de los partidos**.
- **IC95% Δlogloss = [−0.0020, +0.0263] → INCLUYE 0 (no significativo)**, P(Δ>0) = **95%**.
- IC95% Δbrier = [−0.0018, +0.0152] → incluye 0, P(Δ>0) = 94%.

**Comparativa con la corrida anterior (clasificador viejo):**

| | viejo (N=162) | nuevo (N=81) |
|---|---|---|
| Δlogloss medio | +0.0055 | **+0.0117** |
| mejora relativa | 0.52% | **1.05%** |
| P(Δ>0) bootstrap | 88% | **95%** |
| IC95% Δlogloss | [−0.0036, +0.0148] | [−0.0020, +0.0263] |
| ¿significativo (IC excluye 0)? | no | **no (al borde)** |

## (c) Veredicto honesto
Con el clasificador corregido la señal es **más limpia y un poco más fuerte**: solo dos escenarios
ciertos (le_vale_empate, ya_clasificado), ambos mejoran de forma consistente, el efecto relativo
dobla al anterior (1.05% vs 0.52%) y la confianza sube a P≈95%. **PERO sigue SIN ser
estadísticamente significativo**: el IC95% de Δlogloss y Δbrier **todavía incluye el 0** (apenas:
límite inferior −0.002), y ctx solo gana en el 46% de los partidos (el agregado lo arrastran pocos).
La muestra no-trivial se **redujo a la mitad (81)** justamente porque el clasificador honesto se niega
a etiquetar lo dudoso. No es "mejora clara y significativa": es una mejora direccional, al borde de
la significancia, sobre una muestra modesta.

## (d) Recomendación
**DEJAR DORMIDO EN SOMBRA — no reactivar (`CONTEXT_LIVE` sigue False).** El criterio para reactivar
era "mejora clara y significativa"; no se cumple (IC95% incluye 0). Reactivar ajustaría las
predicciones reales con un edge que no se distingue del ruido al 95%.
- **No invertir más esfuerzo aquí por ahora.** El clasificador ya es correcto y conservador; el A/B
  en sombra puede seguir corriendo gratis y acumulando partidos reales del Mundial como red de
  seguridad, pero sin trabajo adicional.
- **Umbral para una futura reactivación:** que el IC95% de Δlogloss Y Δbrier **excluya el 0** sobre
  una muestra mayor (acumulando Mundial 2026 + futuros torneos), y que la mejora se mantenga por
  escenario (le_vale_empate y ya_clasificado, los únicos que firman). Hasta entonces, dormido.

## Anti-leakage (sin cambios respecto a la corrida anterior)
Standings reconstruidos solo de jornadas previas del mismo grupo; ratings L3 walk-forward
(`fit_rating` con `date < partido`); calibración congelada; target solo para puntuar. Sin API.

## Limitaciones
- N no-trivial modesto (81); por escenario aún menor (le_vale_empate 58, ya_clasificado 33).
- `eliminado` (n=1) y `debe_ganar` (n=0) no son evaluables — el clasificador estricto casi nunca los
  certifica en grupos de 4 (correcto, pero deja esos escenarios sin medir).
- Mejores terceros aproximados de forma conservadora (no cross-group) → muchos partidos genuinamente
  tensos quedan neutral; es el precio honesto de no etiquetar lo incierto.
