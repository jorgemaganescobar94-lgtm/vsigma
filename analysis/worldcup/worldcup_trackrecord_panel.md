# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-02T10:45:58+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 53** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 53 | 1.0717 | 0.6486 | 43.4 | 0.000 | 0.0% |
| L3 (oficial) | 53 | 0.8258 | 0.4774 | 67.9 | 0.108 | +26.4% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.9% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 58%) | L3 (Poisson) | 53 | 43 | 0.249 | 0.691 |
| Over 2.5 | base-rate | 53 | 58 | 0.243 | 0.679 |
| BTTS (real 49%) | L3 (Poisson) | 53 | 60 | 0.237 | 0.671 |
| BTTS | base-rate | 53 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=55%):
- matchup (EN VIVO)  n= 22  acc   50%  Brier 0.246  logloss 0.684
- constante (viejo)  n= 22  acc   45%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=59%):
- matchup (EN VIVO)  n= 22  acc   41%  Brier 0.266  logloss 0.727
- constante (viejo)  n= 22  acc   55%  Brier 0.277  logloss 0.784
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 16** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 68.8 | 62.5 | 62.5 | L3 |
| 1X2 logloss | 0.8475 | 0.8503 | 0.8461 | **ens** |
| 1X2 brier | 0.4948 | 0.502 | 0.4954 | L3 |
| Over 2.5 acc% | 43.8 | 43.8 | 43.8 | empate |
| Over 2.5 logloss | 0.6893 | 0.6832 | 0.6893 | **mx** |
| Over 2.5 brier | 0.2482 | 0.2452 | 0.2482 | **mx** |
| BTTS acc% | 37.5 | 37.5 | 37.5 | empate |
| BTTS logloss | 0.735 | 0.7332 | 0.735 | **mx** |
| BTTS brier | 0.2697 | 0.2699 | 0.2697 | empate |
> ⚠️ muestra pequeña (N=16 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 48 | 2.93 | 3.88 | -1.86 (infraestima) | -0.64 (infraestima) | 46.0% (O/U) |
| tiros (orientativo) | 48 | 7.16 | 8.69 | -5.91 (infraestima) | -2.02 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 48 | 1.92 | 2.21 | +1.57 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 28** partidos (616 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 616 | 8% | 0.2484 | 0.0679 | 0.023 | sí | validado (backtest) |
| asistencia | 616 | 6% | 0.2462 | 0.0622 | 0.029 | no | validado (backtest) |
| tarjeta | 616 | 9% | 0.3338 | 0.0917 | 0.082 | no | validado (backtest · tope en cola) |
| tiros a puerta | 616 | 20% | 0.5014 | 0.1499 | 0.089 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.18% vs real 8.93% → sesgo **+7.25pp**
- corregido: pred 12.35% vs real 8.93% → sesgo **+3.42pp** (factor 0.7632, flag `CARD_PROP_CORRECTION`)
>  ⚠️ muestra pequeña (N=28 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 22 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=53
- ECE observado = **0.108** vs nulo p95 = 0.190 → dentro del ruido.
- logloss L3 = **0.8258** vs baseline 1.0717 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
