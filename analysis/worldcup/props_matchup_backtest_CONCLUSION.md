# Valor marginal de la GRANULARIDAD DE MATCHUP en los props gol/asistencia

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API
**Script:** `analysis/worldcup/props_matchup_backtest.py`
**Salidas:** `..._report.txt`, `..._metrics.csv`
**Muestra:** los mismos 150 partidos / **3062 filas jugador-prop** del backtest de props (XI confirmado,
rates de temporada previa, actuals por jugador). Anti-leakage idéntico.

## La pregunta
El método actual (ya validado) es `λ_jugador = xG_equipo(L3) × cuota_jugador`. El **xG de equipo YA
refleja** enfrentarse a un rival débil (supremacía L3). La hipótesis: ¿los jugadores ELITE explotan a
los rivales DÉBILES **más que proporcionalmente** (más de lo que el xG de equipo ya predice)? Lo
relevante NO es batir la tasa base (eso ya lo hace), sino batir al **MÉTODO ACTUAL** — el valor
marginal de la INTERACCIÓN.

## (a) Fórmulas de matchup probadas
`λ_match = λ_base × max(0, 1 + β · z_off · z_weak)`  (β = hipótesis fija, NO ajustada al test)
- `z_off` = calidad ofensiva del jugador estandarizada (g90 para gol, a90 para asistencia, temp. previa).
- **FORM A**: `z_weak = −fuerza L3 del rival` (walk-forward) — el MISMO signal que ya hay en el xG,
  reusado en INTERACCIÓN con la calidad del jugador (¿aporta la interacción sobre el efecto principal?).
- **FORM B**: `z_weak = goles encajados/partido del rival en internacionales previos` (walk-forward) —
  una medida defensiva más fina e independiente, no directamente en el rating de margen L3.
- β principal = 0.25 (+1SD elite vs +1SD débil → ×1.25). Barrido de sensibilidad incluido.

El término `z_off·z_weak ≈ 0` en media → mayormente REDISTRIBUYE λ hacia elite-vs-débil; si la
hipótesis fuese cierta, mejoraría el logloss ahí.

## (b) Métricas matchup vs MÉTODO ACTUAL (β=0.25)

| prop | método | logloss | brier | ECE | Δll(base−match) · IC95% | ¿signif? |
|---|---|---|---|---|---|---|
| **GOL** | ACTUAL (baseline) | **0.22394** | **0.06437** | 0.0200 | — (ref) | |
| | matchup A (−L3opp) | 0.26474 | 0.06674 | 0.0145 | **−0.0408** [−0.084, −0.009] | **SÍ (peor)** |
| | matchup B (opp_gc) | 0.25311 | 0.06658 | 0.0176 | **−0.0292** [−0.063, −0.006] | **SÍ (peor)** |
| **ASIST** | ACTUAL (baseline) | **0.17241** | **0.04693** | 0.0161 | — (ref) | |
| | matchup A (−L3opp) | 0.20962 | 0.04880 | 0.0160 | **−0.0372** [−0.079, −0.006] | **SÍ (peor)** |
| | matchup B (opp_gc) | 0.18807 | 0.04831 | 0.0158 | **−0.0157** [−0.039, −0.002] | **SÍ (peor)** |

Δ = base − matchup; **negativo = matchup PEOR**. El IC95% excluye 0 **por el lado malo** en los 4 casos
→ la interacción empeora de forma **estadísticamente significativa** en logloss Y brier.

**Sensibilidad a β** (Δll base−match; >0 sería mejor) — **todo negativo, en TODA dirección:**

| prop | form | β=−0.25 | β=−0.15 | β=0.15 | β=0.25 | β=0.40 |
|---|---|---|---|---|---|---|
| gol | A | −0.088 | −0.013 | −0.015 | −0.041 | −0.111 |
| gol | B | −0.067 | −0.023 | −0.005 | −0.029 | −0.088 |
| asist | A | −0.066 | −0.022 | −0.024 | −0.037 | −0.075 |
| asist | B | −0.066 | −0.033 | −0.003 | −0.016 | −0.052 |

Ningún β —ni positivo (elite explota débil) ni negativo (lo contrario)— mejora. El óptimo es **β=0**
(el método actual). Cuanto más fuerte la interacción, peor.

## (c) ¿Aporta la interacción valor marginal real?
**NO. Lo contrario: la empeora de forma significativa.** El IC95% de Δlogloss y Δbrier excluye el 0
en el lado equivocado (matchup peor) en gol y asistencia, en ambas formas. La sensibilidad confirma
que el óptimo es no interactuar. Conclusión directa: **el xG de equipo (L3) ya captura por completo la
calidad defensiva del rival** para estos props; añadir una interacción elite×débil solo inyecta ruido
sobre un baseline que ya está bien calibrado (ECE 0.02) y degrada sus predicciones (sobre-confianza en
elite-vs-débil que no se materializa).

## (d) Recomendación honesta
**DESCARTAR.** No integrar granularidad de matchup en los props de jugador. No aporta sobre el método
actual; lo empeora. La calidad del rival ya está donde debe (en el xG de equipo), y la cuota del
jugador (g90/a90 histórico) ya reparte correctamente sin necesidad de un término de interacción. Cero
cambios en producción; el método validado (gol/asistencia) se mantiene tal cual.

## Anti-leakage
XI confirmado (input observado); rates /90 de temporada previa; fuerza L3 y goles-encajados del rival
walk-forward (`date < partido`); target solo para puntuar. Estandarización z con media/desv. de la
muestra (transformación fija, mira-adelante menor documentada, sin fuga del target). Sin API.

## Limitaciones
- β es una hipótesis fija (no ajustada al test, a propósito); el barrido en [−0.25, +0.40] cubre el
  rango razonable y todo empeora, así que la conclusión no depende de β.
- Formas de interacción simples y multiplicativas; no se exploran formas exóticas (no hay motivo: el
  efecto principal ya está saturado por el xG y cualquier interacción simple solo añade varianza).
