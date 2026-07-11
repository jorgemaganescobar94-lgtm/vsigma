# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-11T09:42:19+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 69** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 69 | 1.0672 | 0.6461 | 43.5 | 0.000 | 0.0% |
| L3 (oficial) | 69 | 0.8291 | 0.4787 | 68.1 | 0.115 | +25.9% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 57%) | L3 (Poisson) | 69 | 43 | 0.251 | 0.695 |
| Over 2.5 | base-rate | 69 | 57 | 0.246 | 0.685 |
| BTTS (real 49%) | L3 (Poisson) | 69 | 58 | 0.240 | 0.674 |
| BTTS | base-rate | 69 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=53%):
- matchup (EN VIVO)  n= 38  acc   47%  Brier 0.250  logloss 0.694
- constante (viejo)  n= 38  acc   47%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=55%):
- matchup (EN VIVO)  n= 38  acc   45%  Brier 0.258  logloss 0.710
- constante (viejo)  n= 38  acc   53%  Brier 0.264  logloss 0.743
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 32** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 68.8 | 68.8 | 68.8 | empate |
| 1X2 logloss | 0.8438 | 0.8598 | 0.8488 | L3 |
| 1X2 brier | 0.489 | 0.5036 | 0.4935 | L3 |
| Over 2.5 acc% | 43.8 | 46.9 | 43.8 | **mx** |
| Over 2.5 logloss | 0.6984 | 0.6962 | 0.6984 | **mx** |
| Over 2.5 brier | 0.2527 | 0.2516 | 0.2527 | **mx** |
| BTTS acc% | 43.8 | 43.8 | 43.8 | empate |
| BTTS logloss | 0.7106 | 0.7202 | 0.7106 | empate |
| BTTS brier | 0.2581 | 0.2634 | 0.2581 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 64 | 3.1 | 4.01 | -2.10 (infraestima) | -0.28 (infraestima) | 42.0% (O/U) |
| tiros (orientativo) | 64 | 6.78 | 8.43 | -5.83 (infraestima) | -0.79 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 64 | 1.93 | 2.2 | +1.44 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 44** partidos (968 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 968 | 8% | 0.2510 | 0.0689 | 0.019 | sí | validado (backtest) |
| asistencia | 968 | 6% | 0.2310 | 0.0578 | 0.029 | no | validado (backtest) |
| tarjeta | 968 | 10% | 0.3508 | 0.0985 | 0.087 | no | validado (backtest · tope en cola) |
| tiros a puerta | 968 | 20% | 0.5525 | 0.1513 | 0.093 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.47% vs real 9.71% → sesgo **+6.76pp**
- corregido: pred 12.16% vs real 9.71% → sesgo **+2.45pp** (factor 0.7382, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 38 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=69
- ECE observado = **0.115** vs nulo p95 = 0.168 → dentro del ruido.
- logloss L3 = **0.8291** vs baseline 1.0672 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
