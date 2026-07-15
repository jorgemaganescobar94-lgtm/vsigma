# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-15T10:07:04+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 72** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 72 | 1.0776 | 0.6528 | 41.7 | 0.000 | 0.0% |
| L3 (oficial) | 72 | 0.8462 | 0.4913 | 65.3 | 0.119 | +24.7% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 54%) | L3 (Poisson) | 72 | 46 | 0.249 | 0.690 |
| Over 2.5 | base-rate | 72 | 54 | 0.248 | 0.690 |
| BTTS (real 50%) | L3 (Poisson) | 72 | 57 | 0.241 | 0.676 |
| BTTS | base-rate | 72 | 50 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=49%):
- matchup (EN VIVO)  n= 41  acc   51%  Brier 0.246  logloss 0.686
- constante (viejo)  n= 41  acc   51%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=56%):
- matchup (EN VIVO)  n= 41  acc   44%  Brier 0.258  logloss 0.710
- constante (viejo)  n= 41  acc   51%  Brier 0.263  logloss 0.740
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 35** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 62.9 | 62.9 | 62.9 | empate |
| 1X2 logloss | 0.8778 | 0.9016 | 0.8868 | L3 |
| 1X2 brier | 0.514 | 0.5346 | 0.5216 | L3 |
| Over 2.5 acc% | 48.6 | 51.4 | 48.6 | **mx** |
| Over 2.5 logloss | 0.6886 | 0.6862 | 0.6886 | **mx** |
| Over 2.5 brier | 0.2478 | 0.2466 | 0.2478 | **mx** |
| BTTS acc% | 42.9 | 42.9 | 42.9 | empate |
| BTTS logloss | 0.7113 | 0.7205 | 0.7113 | empate |
| BTTS brier | 0.2585 | 0.2636 | 0.2585 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 67 | 3.08 | 3.97 | -2.13 (infraestima) | -0.28 (infraestima) | 40.0% (O/U) |
| tiros (orientativo) | 67 | 6.85 | 8.54 | -5.92 (infraestima) | -0.77 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 67 | 1.92 | 2.18 | +1.41 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 47** partidos (1034 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 1034 | 8% | 0.2547 | 0.0700 | 0.016 | sí | validado (backtest) |
| asistencia | 1034 | 6% | 0.2325 | 0.0584 | 0.028 | no | validado (backtest) |
| tarjeta | 1034 | 10% | 0.3527 | 0.0990 | 0.085 | no | validado (backtest · tope en cola) |
| tiros a puerta | 1034 | 21% | 0.5776 | 0.1515 | 0.092 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.45% vs real 9.77% → sesgo **+6.68pp**
- corregido: pred 12.09% vs real 9.77% → sesgo **+2.32pp** (factor 0.7349, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 41 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=72
- ECE observado = **0.119** vs nulo p95 = 0.164 → dentro del ruido.
- logloss L3 = **0.8462** vs baseline 1.0776 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
