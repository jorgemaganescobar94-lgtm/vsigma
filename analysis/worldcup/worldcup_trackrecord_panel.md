# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-27T12:40:02+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 37** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 37 | 1.0612 | 0.6428 | 43.2 | 0.000 | 0.0% |
| L3 (oficial) | 37 | 0.8164 | 0.4698 | 67.6 | 0.126 | +26.9% |
| v2 | 37 | 0.8594 | 0.4955 | 67.6 | 0.141 | +22.9% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 59%) | L3 (Poisson) | 37 | 43 | 0.249 | 0.691 |
| Over 2.5 | base-rate | 37 | 59 | 0.241 | 0.675 |
| BTTS (real 43%) | L3 (Poisson) | 37 | 70 | 0.223 | 0.643 |
| BTTS | base-rate | 37 | 57 | 0.245 | 0.684 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n=  6  acc   67%  Brier 0.239  logloss 0.670
- constante (viejo)  n=  6  acc   50%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=50%):
- matchup (EN VIVO)  n=  6  acc   50%  Brier 0.255  logloss 0.704
- constante (viejo)  n=  6  acc   67%  Brier 0.253  logloss 0.701
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 12** partidos (264 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 264 | 6% | 0.2307 | 0.0625 | 0.038 | no | validado (backtest) |
| asistencia | 264 | 7% | 0.2446 | 0.0656 | 0.035 | no | validado (backtest) |
| tarjeta | 264 | 10% | 0.3447 | 0.0977 | 0.073 | no | validado (backtest · tope en cola) |
| tiros a puerta | 264 | 17% | 0.5804 | 0.1541 | 0.122 | no | ranking solo (no %) |
>  ⚠️ muestra pequeña (N=12 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 4** (de 6 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=4 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=37
- ECE observado = **0.126** vs nulo p95 = 0.228 → dentro del ruido.
- logloss L3 = **0.8164** vs baseline 1.0612 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
