# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-05T10:17:10+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 61** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 61 | 1.0690 | 0.6466 | 44.3 | 0.000 | 0.0% |
| L3 (oficial) | 61 | 0.8219 | 0.4748 | 67.2 | 0.095 | +26.6% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +25.0% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 56%) | L3 (Poisson) | 61 | 43 | 0.251 | 0.695 |
| Over 2.5 | base-rate | 61 | 56 | 0.247 | 0.687 |
| BTTS (real 48%) | L3 (Poisson) | 61 | 61 | 0.236 | 0.667 |
| BTTS | base-rate | 61 | 52 | 0.249 | 0.692 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 30  acc   47%  Brier 0.250  logloss 0.694
- constante (viejo)  n= 30  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=53%):
- matchup (EN VIVO)  n= 30  acc   47%  Brier 0.255  logloss 0.704
- constante (viejo)  n= 30  acc   60%  Brier 0.262  logloss 0.744
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 24** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 66.7 | 66.7 | 66.7 | empate |
| 1X2 logloss | 0.8303 | 0.8309 | 0.828 | **ens** |
| 1X2 brier | 0.4825 | 0.4903 | 0.4836 | L3 |
| Over 2.5 acc% | 41.7 | 45.8 | 41.7 | **mx** |
| Over 2.5 logloss | 0.6997 | 0.6946 | 0.6997 | **mx** |
| Over 2.5 brier | 0.2533 | 0.2508 | 0.2533 | **mx** |
| BTTS acc% | 45.8 | 45.8 | 45.8 | empate |
| BTTS logloss | 0.7039 | 0.7136 | 0.7039 | empate |
| BTTS brier | 0.2546 | 0.2602 | 0.2546 | empate |
> ⚠️ muestra pequeña (N=24 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 56 | 3.17 | 4.1 | -2.09 (infraestima) | -0.32 (infraestima) | 43.0% (O/U) |
| tiros (orientativo) | 56 | 7.12 | 8.77 | -6.03 (infraestima) | -0.91 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 56 | 1.95 | 2.23 | +1.51 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 36** partidos (792 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 792 | 8% | 0.2459 | 0.0670 | 0.018 | sí | validado (backtest) |
| asistencia | 792 | 6% | 0.2404 | 0.0605 | 0.032 | no | validado (backtest) |
| tarjeta | 792 | 9% | 0.3463 | 0.0964 | 0.085 | no | validado (backtest · tope en cola) |
| tiros a puerta | 792 | 20% | 0.5323 | 0.1509 | 0.096 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.42% vs real 9.47% → sesgo **+6.95pp**
- corregido: pred 12.32% vs real 9.47% → sesgo **+2.85pp** (factor 0.7502, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 30 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=61
- ECE observado = **0.095** vs nulo p95 = 0.177 → dentro del ruido.
- logloss L3 = **0.8219** vs baseline 1.0690 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
