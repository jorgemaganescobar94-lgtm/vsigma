# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-26T21:58:40+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 31** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 31 | 1.0341 | 0.6243 | 48.4 | 0.000 | 0.0% |
| L3 (oficial) | 31 | 0.8284 | 0.4782 | 67.7 | 0.153 | +23.4% |
| v2 | 31 | 0.8728 | 0.5065 | 67.7 | 0.133 | +18.9% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 61%) | L3 (Poisson) | 31 | 39 | 0.251 | 0.696 |
| Over 2.5 | base-rate | 31 | 61 | 0.237 | 0.667 |
| BTTS (real 42%) | L3 (Poisson) | 31 | 74 | 0.217 | 0.631 |
| BTTS | base-rate | 31 | 58 | 0.243 | 0.680 |

### A/B total de goles — matchup vs constante
_— sin filas con total constante logueado todavía (se llena tras nuevas predicciones NS) —_

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 6** partidos (132 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 132 | 6% | 0.2505 | 0.0656 | 0.068 | no | validado (backtest) |
| asistencia | 132 | 7% | 0.2636 | 0.0683 | 0.044 | no | validado (backtest) |
| tarjeta | 132 | 5% | 0.2626 | 0.0669 | 0.114 | no | validado (backtest · tope en cola) |
| tiros a puerta | 132 | 17% | 0.4553 | 0.1541 | 0.136 | no | ranking solo (no %) |
>  ⚠️ muestra pequeña (N=6 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 0** (de 0 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=0 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=31
- ECE observado = **0.153** vs nulo p95 = 0.246 → dentro del ruido.
- logloss L3 = **0.8284** vs baseline 1.0341 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
