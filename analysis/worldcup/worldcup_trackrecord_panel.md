# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-28T09:59:40+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 43** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 43 | 1.0711 | 0.6490 | 41.9 | 0.000 | 0.0% |
| L3 (oficial) | 43 | 0.8007 | 0.4600 | 67.4 | 0.143 | +29.1% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.7% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 60%) | L3 (Poisson) | 43 | 42 | 0.249 | 0.690 |
| Over 2.5 | base-rate | 43 | 60 | 0.239 | 0.671 |
| BTTS (real 47%) | L3 (Poisson) | 43 | 65 | 0.233 | 0.662 |
| BTTS | base-rate | 43 | 53 | 0.249 | 0.691 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=58%):
- matchup (EN VIVO)  n= 12  acc   50%  Brier 0.242  logloss 0.676
- constante (viejo)  n= 12  acc   42%  Brier 0.251  logloss 0.695
- BTTS     (real Yes=58%):
- matchup (EN VIVO)  n= 12  acc   42%  Brier 0.273  logloss 0.743
- constante (viejo)  n= 12  acc   58%  Brier 0.297  logloss 0.856
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo (en vivo, desde 27-jun)
**N = 6** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado.

| métrica | L3 | mx | líder |
|---|---:|---:|---|
| 1X2 acc% | 66.7 | 66.7 | empate |
| 1X2 logloss | 0.7037 | 0.7128 | L3 |
| 1X2 brier | 0.3997 | 0.4033 | L3 |
| Over 2.5 acc% | 33.3 | 33.3 | empate |
| Over 2.5 logloss | 0.6825 | 0.6746 | **mx** |
| Over 2.5 brier | 0.245 | 0.2412 | **mx** |
| BTTS acc% | 33.3 | 33.3 | empate |
| BTTS logloss | 0.781 | 0.7656 | **mx** |
| BTTS brier | 0.2906 | 0.2859 | **mx** |
> ⚠️ muestra pequeña (N=6 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 38 | 2.56 | 3.03 | -1.47 (infraestima) | -0.58 (infraestima) | 47.0% (O/U) |
| tiros (orientativo) | 38 | 7.56 | 9.01 | -6.15 (infraestima) | -2.44 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 38 | 1.88 | 2.19 | +1.53 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 18** partidos (396 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 396 | 8% | 0.2506 | 0.0685 | 0.035 | sí | validado (backtest) |
| asistencia | 396 | 6% | 0.2392 | 0.0620 | 0.027 | no | validado (backtest) |
| tarjeta | 396 | 10% | 0.3397 | 0.0956 | 0.073 | no | validado (backtest · tope en cola) |
| tiros a puerta | 396 | 19% | 0.5231 | 0.1467 | 0.103 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.23% vs real 9.85% → sesgo **+6.38pp**
- corregido: pred 13.56% vs real 9.85% → sesgo **+3.71pp** (factor 0.8354, flag `CARD_PROP_CORRECTION`)
>  ⚠️ muestra pequeña (N=18 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 12 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=43
- ECE observado = **0.143** vs nulo p95 = 0.211 → dentro del ruido.
- logloss L3 = **0.8007** vs baseline 1.0711 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
