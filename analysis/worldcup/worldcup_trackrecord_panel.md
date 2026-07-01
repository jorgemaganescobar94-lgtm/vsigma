# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-01T11:49:47+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 50** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 50 | 1.0737 | 0.6504 | 42.0 | 0.000 | 0.0% |
| L3 (oficial) | 50 | 0.8263 | 0.4782 | 68.0 | 0.141 | +26.5% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 58%) | L3 (Poisson) | 50 | 44 | 0.248 | 0.689 |
| Over 2.5 | base-rate | 50 | 58 | 0.244 | 0.680 |
| BTTS (real 48%) | L3 (Poisson) | 50 | 62 | 0.236 | 0.667 |
| BTTS | base-rate | 50 | 52 | 0.250 | 0.692 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=53%):
- matchup (EN VIVO)  n= 19  acc   53%  Brier 0.243  logloss 0.680
- constante (viejo)  n= 19  acc   47%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=58%):
- matchup (EN VIVO)  n= 19  acc   42%  Brier 0.266  logloss 0.727
- constante (viejo)  n= 19  acc   58%  Brier 0.279  logloss 0.794
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 13** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 69.2 | 61.5 | 61.5 | L3 |
| 1X2 logloss | 0.8546 | 0.8652 | 0.8569 | L3 |
| 1X2 brier | 0.502 | 0.5132 | 0.5047 | L3 |
| Over 2.5 acc% | 46.2 | 46.2 | 46.2 | empate |
| Over 2.5 logloss | 0.6838 | 0.6808 | 0.6838 | **mx** |
| Over 2.5 brier | 0.2455 | 0.244 | 0.2455 | **mx** |
| BTTS acc% | 38.5 | 38.5 | 38.5 | empate |
| BTTS logloss | 0.737 | 0.7306 | 0.737 | **mx** |
| BTTS brier | 0.2704 | 0.2686 | 0.2704 | **mx** |
> ⚠️ muestra pequeña (N=13 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 45 | 3.04 | 3.97 | -2.05 (infraestima) | -0.73 (infraestima) | 47.0% (O/U) |
| tiros (orientativo) | 45 | 7.12 | 8.57 | -5.87 (infraestima) | -2.10 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 45 | 1.92 | 2.23 | +1.55 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 25** partidos (550 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 550 | 8% | 0.2527 | 0.0685 | 0.030 | sí | validado (backtest) |
| asistencia | 550 | 6% | 0.2381 | 0.0617 | 0.024 | no | validado (backtest) |
| tarjeta | 550 | 9% | 0.3381 | 0.0932 | 0.082 | no | validado (backtest · tope en cola) |
| tiros a puerta | 550 | 21% | 0.5088 | 0.1500 | 0.083 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.21% vs real 9.09% → sesgo **+7.12pp**
- corregido: pred 12.65% vs real 9.09% → sesgo **+3.56pp** (factor 0.7804, flag `CARD_PROP_CORRECTION`)
>  ⚠️ muestra pequeña (N=25 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 19 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=50
- ECE observado = **0.141** vs nulo p95 = 0.199 → dentro del ruido.
- logloss L3 = **0.8263** vs baseline 1.0737 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
