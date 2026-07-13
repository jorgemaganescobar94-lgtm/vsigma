# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-13T11:15:37+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 71** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 71 | 1.0771 | 0.6523 | 42.3 | 0.000 | 0.0% |
| L3 (oficial) | 71 | 0.8423 | 0.4886 | 66.2 | 0.116 | +25.1% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.9% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 55%) | L3 (Poisson) | 71 | 45 | 0.249 | 0.692 |
| Over 2.5 | base-rate | 71 | 55 | 0.248 | 0.688 |
| BTTS (real 51%) | L3 (Poisson) | 71 | 56 | 0.241 | 0.676 |
| BTTS | base-rate | 71 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 40  acc   50%  Brier 0.248  logloss 0.689
- constante (viejo)  n= 40  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=57%):
- matchup (EN VIVO)  n= 40  acc   42%  Brier 0.259  logloss 0.711
- constante (viejo)  n= 40  acc   52%  Brier 0.262  logloss 0.739
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 34** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 64.7 | 64.7 | 64.7 | empate |
| 1X2 logloss | 0.8704 | 0.8918 | 0.8782 | L3 |
| 1X2 brier | 0.5089 | 0.5277 | 0.5157 | L3 |
| Over 2.5 acc% | 47.1 | 50.0 | 47.1 | **mx** |
| Over 2.5 logloss | 0.6923 | 0.6903 | 0.6923 | **mx** |
| Over 2.5 brier | 0.2497 | 0.2486 | 0.2497 | **mx** |
| BTTS acc% | 41.2 | 41.2 | 41.2 | empate |
| BTTS logloss | 0.7125 | 0.7226 | 0.7125 | empate |
| BTTS brier | 0.2591 | 0.2646 | 0.2591 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 66 | 3.12 | 4.0 | -2.15 (infraestima) | -0.28 (infraestima) | 41.0% (O/U) |
| tiros (orientativo) | 66 | 6.95 | 8.6 | -6.02 (infraestima) | -0.79 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 66 | 1.93 | 2.19 | +1.41 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 46** partidos (1012 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 1012 | 8% | 0.2535 | 0.0699 | 0.015 | sí | validado (backtest) |
| asistencia | 1012 | 6% | 0.2340 | 0.0587 | 0.029 | no | validado (backtest) |
| tarjeta | 1012 | 10% | 0.3510 | 0.0986 | 0.085 | no | validado (backtest · tope en cola) |
| tiros a puerta | 1012 | 21% | 0.5468 | 0.1507 | 0.089 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.43% vs real 9.68% → sesgo **+6.75pp**
- corregido: pred 12.06% vs real 9.68% → sesgo **+2.38pp** (factor 0.7339, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 40 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=71
- ECE observado = **0.116** vs nulo p95 = 0.166 → dentro del ruido.
- logloss L3 = **0.8423** vs baseline 1.0771 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
