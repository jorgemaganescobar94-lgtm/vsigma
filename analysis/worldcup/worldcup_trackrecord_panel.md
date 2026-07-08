# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-08T10:23:03+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 67** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 67 | 1.0737 | 0.6505 | 41.8 | 0.000 | 0.0% |
| L3 (oficial) | 67 | 0.8297 | 0.4793 | 67.2 | 0.102 | +26.3% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 57%) | L3 (Poisson) | 67 | 43 | 0.251 | 0.695 |
| Over 2.5 | base-rate | 67 | 57 | 0.245 | 0.684 |
| BTTS (real 49%) | L3 (Poisson) | 67 | 58 | 0.239 | 0.674 |
| BTTS | base-rate | 67 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=53%):
- matchup (EN VIVO)  n= 36  acc   47%  Brier 0.250  logloss 0.694
- constante (viejo)  n= 36  acc   47%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=56%):
- matchup (EN VIVO)  n= 36  acc   44%  Brier 0.258  logloss 0.710
- constante (viejo)  n= 36  acc   53%  Brier 0.264  logloss 0.745
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 30** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 66.7 | 66.7 | 66.7 | empate |
| 1X2 logloss | 0.8462 | 0.8731 | 0.8567 | L3 |
| 1X2 brier | 0.4909 | 0.5138 | 0.4996 | L3 |
| Over 2.5 acc% | 43.3 | 46.7 | 43.3 | **mx** |
| Over 2.5 logloss | 0.6984 | 0.6951 | 0.6984 | **mx** |
| Over 2.5 brier | 0.2527 | 0.251 | 0.2527 | **mx** |
| BTTS acc% | 43.3 | 43.3 | 43.3 | empate |
| BTTS logloss | 0.7115 | 0.7212 | 0.7115 | empate |
| BTTS brier | 0.2585 | 0.2639 | 0.2585 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 62 | 3.11 | 4.04 | -2.14 (infraestima) | -0.30 (infraestima) | 42.0% (O/U) |
| tiros (orientativo) | 62 | 6.86 | 8.49 | -5.88 (infraestima) | -0.82 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 62 | 1.93 | 2.2 | +1.43 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 42** partidos (924 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 924 | 8% | 0.2506 | 0.0685 | 0.020 | sí | validado (backtest) |
| asistencia | 924 | 6% | 0.2343 | 0.0586 | 0.030 | no | validado (backtest) |
| tarjeta | 924 | 10% | 0.3496 | 0.0981 | 0.084 | no | validado (backtest · tope en cola) |
| tiros a puerta | 924 | 20% | 0.5223 | 0.1512 | 0.094 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.44% vs real 9.74% → sesgo **+6.70pp**
- corregido: pred 12.24% vs real 9.74% → sesgo **+2.50pp** (factor 0.7446, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 36 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=67
- ECE observado = **0.102** vs nulo p95 = 0.170 → dentro del ruido.
- logloss L3 = **0.8297** vs baseline 1.0737 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
