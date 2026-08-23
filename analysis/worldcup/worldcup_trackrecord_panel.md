# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-08-23T08:33:39+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 75** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 75 | 1.0816 | 0.6556 | 40.0 | 0.000 | 0.0% |
| L3 (oficial) | 75 | 0.8549 | 0.4974 | 64.0 | 0.106 | +24.1% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 55%) | L3 (Poisson) | 75 | 45 | 0.249 | 0.691 |
| Over 2.5 | base-rate | 75 | 55 | 0.248 | 0.689 |
| BTTS (real 51%) | L3 (Poisson) | 75 | 56 | 0.241 | 0.678 |
| BTTS | base-rate | 75 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 44  acc   50%  Brier 0.248  logloss 0.688
- constante (viejo)  n= 44  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=57%):
- matchup (EN VIVO)  n= 44  acc   43%  Brier 0.258  logloss 0.711
- constante (viejo)  n= 44  acc   52%  Brier 0.263  logloss 0.737
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 38** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 60.5 | 60.5 | 60.5 | empate |
| 1X2 logloss | 0.8925 | 0.9311 | 0.9086 | L3 |
| 1X2 brier | 0.5242 | 0.554 | 0.5364 | L3 |
| Over 2.5 acc% | 47.4 | 50.0 | 47.4 | **mx** |
| Over 2.5 logloss | 0.691 | 0.6903 | 0.691 | **mx** |
| Over 2.5 brier | 0.249 | 0.2487 | 0.249 | empate |
| BTTS acc% | 42.1 | 42.1 | 42.1 | empate |
| BTTS logloss | 0.712 | 0.7203 | 0.712 | empate |
| BTTS brier | 0.2589 | 0.2635 | 0.2589 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 70 | 3.06 | 3.97 | -2.15 (infraestima) | -0.27 (infraestima) | 41.0% (O/U) |
| tiros (orientativo) | 70 | 6.95 | 8.68 | -6.06 (infraestima) | -0.76 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 70 | 1.93 | 2.21 | +1.37 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 50** partidos (1100 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 1100 | 8% | 0.2574 | 0.0708 | 0.018 | sí | validado (backtest) |
| asistencia | 1100 | 6% | 0.2381 | 0.0604 | 0.029 | no | validado (backtest) |
| tarjeta | 1100 | 10% | 0.3561 | 0.1000 | 0.087 | no | validado (backtest · tope en cola) |
| tiros a puerta | 1100 | 21% | 0.6024 | 0.1529 | 0.089 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.46% vs real 9.82% → sesgo **+6.65pp**
- corregido: pred 12.03% vs real 9.82% → sesgo **+2.22pp** (factor 0.7309, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 44 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=75
- ECE observado = **0.106** vs nulo p95 = 0.162 → dentro del ruido.
- logloss L3 = **0.8549** vs baseline 1.0816 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
