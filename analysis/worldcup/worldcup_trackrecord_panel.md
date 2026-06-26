# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-26T22:24:02+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 33** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 33 | 1.0271 | 0.6208 | 48.5 | 0.000 | 0.0% |
| L3 (oficial) | 33 | 0.8143 | 0.4677 | 69.7 | 0.117 | +24.7% |
| v2 | 33 | 0.8544 | 0.4932 | 69.7 | 0.151 | +20.5% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 64%) | L3 (Poisson) | 33 | 36 | 0.253 | 0.699 |
| Over 2.5 | base-rate | 33 | 64 | 0.231 | 0.655 |
| BTTS (real 42%) | L3 (Poisson) | 33 | 73 | 0.219 | 0.634 |
| BTTS | base-rate | 33 | 58 | 0.244 | 0.682 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=100%):
- matchup (EN VIVO)  n=  2  acc    0%  Brier 0.283  logloss 0.759
- constante (viejo)  n=  2  acc    0%  Brier 0.255  logloss 0.703
- BTTS     (real Yes=50%):
- matchup (EN VIVO)  n=  2  acc   50%  Brier 0.243  logloss 0.678
- constante (viejo)  n=  2  acc  100%  Brier 0.226  logloss 0.646
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 8** partidos (176 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 176 | 7% | 0.2567 | 0.0711 | 0.043 | no | validado (backtest) |
| asistencia | 176 | 9% | 0.2821 | 0.0775 | 0.051 | sí | validado (backtest) |
| tarjeta | 176 | 7% | 0.2869 | 0.0772 | 0.092 | no | validado (backtest · tope en cola) |
| tiros a puerta | 176 | 19% | 0.4547 | 0.1517 | 0.096 | no | ranking solo (no %) |
>  ⚠️ muestra pequeña (N=8 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 0** (de 2 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=0 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=33
- ECE observado = **0.117** vs nulo p95 = 0.236 → dentro del ruido.
- logloss L3 = **0.8143** vs baseline 1.0271 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
