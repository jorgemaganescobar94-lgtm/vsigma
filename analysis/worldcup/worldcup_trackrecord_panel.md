# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-19T09:55:42+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 74** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 74 | 1.0774 | 0.6530 | 40.5 | 0.000 | 0.0% |
| L3 (oficial) | 74 | 0.8504 | 0.4943 | 64.9 | 0.102 | +24.3% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 55%) | L3 (Poisson) | 74 | 45 | 0.250 | 0.693 |
| Over 2.5 | base-rate | 74 | 55 | 0.247 | 0.687 |
| BTTS (real 51%) | L3 (Poisson) | 74 | 55 | 0.242 | 0.678 |
| BTTS | base-rate | 74 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=51%):
- matchup (EN VIVO)  n= 43  acc   49%  Brier 0.249  logloss 0.691
- constante (viejo)  n= 43  acc   49%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=58%):
- matchup (EN VIVO)  n= 43  acc   42%  Brier 0.259  logloss 0.712
- constante (viejo)  n= 43  acc   53%  Brier 0.262  logloss 0.737
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 37** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 62.2 | 62.2 | 62.2 | empate |
| 1X2 logloss | 0.8844 | 0.9211 | 0.8995 | L3 |
| 1X2 brier | 0.5187 | 0.5472 | 0.5303 | L3 |
| Over 2.5 acc% | 45.9 | 48.6 | 45.9 | **mx** |
| Over 2.5 logloss | 0.6946 | 0.6939 | 0.6946 | **mx** |
| Over 2.5 brier | 0.2508 | 0.2504 | 0.2508 | empate |
| BTTS acc% | 40.5 | 40.5 | 40.5 | empate |
| BTTS logloss | 0.7133 | 0.722 | 0.7133 | empate |
| BTTS brier | 0.2596 | 0.2644 | 0.2596 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 69 | 3.01 | 3.91 | -2.08 (infraestima) | -0.26 (infraestima) | 42.0% (O/U) |
| tiros (orientativo) | 69 | 6.99 | 8.72 | -6.08 (infraestima) | -0.77 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 69 | 1.93 | 2.2 | +1.43 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 49** partidos (1078 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 1078 | 9% | 0.2608 | 0.0720 | 0.018 | sí | validado (backtest) |
| asistencia | 1078 | 6% | 0.2415 | 0.0614 | 0.029 | no | validado (backtest) |
| tarjeta | 1078 | 10% | 0.3524 | 0.0988 | 0.086 | no | validado (backtest · tope en cola) |
| tiros a puerta | 1078 | 21% | 0.6060 | 0.1532 | 0.090 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.43% vs real 9.65% → sesgo **+6.79pp**
- corregido: pred 11.94% vs real 9.65% → sesgo **+2.29pp** (factor 0.7266, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 43 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=74
- ECE observado = **0.102** vs nulo p95 = 0.163 → dentro del ruido.
- logloss L3 = **0.8504** vs baseline 1.0774 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
