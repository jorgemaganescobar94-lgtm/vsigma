# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-29T14:21:10+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 44** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 44 | 1.0702 | 0.6488 | 40.9 | 0.000 | 0.0% |
| L3 (oficial) | 44 | 0.7984 | 0.4582 | 68.2 | 0.151 | +29.4% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 59%) | L3 (Poisson) | 44 | 43 | 0.247 | 0.688 |
| Over 2.5 | base-rate | 44 | 59 | 0.242 | 0.677 |
| BTTS (real 45%) | L3 (Poisson) | 44 | 66 | 0.233 | 0.662 |
| BTTS | base-rate | 44 | 55 | 0.248 | 0.689 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=54%):
- matchup (EN VIVO)  n= 13  acc   54%  Brier 0.239  logloss 0.670
- constante (viejo)  n= 13  acc   46%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=54%):
- matchup (EN VIVO)  n= 13  acc   46%  Brier 0.269  logloss 0.735
- constante (viejo)  n= 13  acc   54%  Brier 0.295  logloss 0.846
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo (en vivo, desde 27-jun)
**N = 7** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado.

| métrica | L3 | mx | líder |
|---|---:|---:|---|
| 1X2 acc% | 71.4 | 71.4 | empate |
| 1X2 logloss | 0.7032 | 0.7389 | L3 |
| 1X2 brier | 0.3969 | 0.4207 | L3 |
| Over 2.5 acc% | 42.9 | 42.9 | empate |
| Over 2.5 logloss | 0.6693 | 0.6566 | **mx** |
| Over 2.5 brier | 0.2384 | 0.2322 | **mx** |
| BTTS acc% | 42.9 | 42.9 | empate |
| BTTS logloss | 0.7608 | 0.7496 | **mx** |
| BTTS brier | 0.281 | 0.2779 | **mx** |
> ⚠️ muestra pequeña (N=7 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 39 | 2.53 | 3.0 | -1.39 (infraestima) | -0.54 (infraestima) | 49.0% (O/U) |
| tiros (orientativo) | 39 | 7.42 | 8.9 | -6.05 (infraestima) | -2.36 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 39 | 1.91 | 2.21 | +1.56 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 19** partidos (418 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 418 | 8% | 0.2520 | 0.0680 | 0.037 | sí | validado (backtest) |
| asistencia | 418 | 6% | 0.2304 | 0.0591 | 0.027 | no | validado (backtest) |
| tarjeta | 418 | 9% | 0.3336 | 0.0931 | 0.078 | no | validado (backtest · tope en cola) |
| tiros a puerta | 418 | 19% | 0.5191 | 0.1468 | 0.099 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.40% vs real 9.33% → sesgo **+7.07pp**
- corregido: pred 13.35% vs real 9.33% → sesgo **+4.02pp** (factor 0.8139, flag `CARD_PROP_CORRECTION`)
>  ⚠️ muestra pequeña (N=19 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 13 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=44
- ECE observado = **0.151** vs nulo p95 = 0.208 → dentro del ruido.
- logloss L3 = **0.7984** vs baseline 1.0702 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
