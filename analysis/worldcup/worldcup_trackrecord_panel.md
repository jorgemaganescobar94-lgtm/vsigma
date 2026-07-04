# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-04T14:12:45+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 59** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 59 | 1.0644 | 0.6429 | 45.8 | 0.000 | 0.0% |
| L3 (oficial) | 59 | 0.8375 | 0.4860 | 66.1 | 0.088 | +24.4% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +25.4% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 56%) | L3 (Poisson) | 59 | 44 | 0.250 | 0.693 |
| Over 2.5 | base-rate | 59 | 56 | 0.246 | 0.686 |
| BTTS (real 49%) | L3 (Poisson) | 59 | 59 | 0.238 | 0.672 |
| BTTS | base-rate | 59 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 28  acc   50%  Brier 0.248  logloss 0.690
- constante (viejo)  n= 28  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=57%):
- matchup (EN VIVO)  n= 28  acc   43%  Brier 0.262  logloss 0.718
- constante (viejo)  n= 28  acc   57%  Brier 0.270  logloss 0.763
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 22** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 63.6 | 63.6 | 63.6 | empate |
| 1X2 logloss | 0.8729 | 0.8575 | 0.8628 | **mx** |
| 1X2 brier | 0.5131 | 0.5108 | 0.5093 | **ens** |
| Over 2.5 acc% | 45.5 | 45.5 | 45.5 | empate |
| Over 2.5 logloss | 0.695 | 0.691 | 0.695 | **mx** |
| Over 2.5 brier | 0.251 | 0.249 | 0.251 | **mx** |
| BTTS acc% | 40.9 | 40.9 | 40.9 | empate |
| BTTS logloss | 0.7218 | 0.7216 | 0.7218 | empate |
| BTTS brier | 0.2634 | 0.2641 | 0.2634 | empate |
> ⚠️ muestra pequeña (N=22 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 54 | 3.06 | 4.01 | -1.95 (infraestima) | -0.30 (infraestima) | 44.0% (O/U) |
| tiros (orientativo) | 54 | 7.38 | 8.93 | -6.27 (infraestima) | -0.98 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 54 | 1.94 | 2.22 | +1.59 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 34** partidos (748 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 748 | 8% | 0.2513 | 0.0685 | 0.020 | sí | validado (backtest) |
| asistencia | 748 | 6% | 0.2427 | 0.0612 | 0.033 | no | validado (backtest) |
| tarjeta | 748 | 9% | 0.3332 | 0.0915 | 0.087 | no | validado (backtest · tope en cola) |
| tiros a puerta | 748 | 20% | 0.5408 | 0.1523 | 0.094 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.29% vs real 8.69% → sesgo **+7.60pp**
- corregido: pred 11.91% vs real 8.69% → sesgo **+3.22pp** (factor 0.7311, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 28 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=59
- ECE observado = **0.088** vs nulo p95 = 0.181 → dentro del ruido.
- logloss L3 = **0.8375** vs baseline 1.0644 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
