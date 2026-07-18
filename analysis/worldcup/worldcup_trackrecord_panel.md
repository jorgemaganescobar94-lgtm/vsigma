# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-18T09:30:38+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 73** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 73 | 1.0777 | 0.6530 | 41.1 | 0.000 | 0.0% |
| L3 (oficial) | 73 | 0.8439 | 0.4895 | 65.8 | 0.111 | +25.0% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 55%) | L3 (Poisson) | 73 | 45 | 0.249 | 0.692 |
| Over 2.5 | base-rate | 73 | 55 | 0.248 | 0.689 |
| BTTS (real 51%) | L3 (Poisson) | 73 | 56 | 0.241 | 0.677 |
| BTTS | base-rate | 73 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 42  acc   50%  Brier 0.248  logloss 0.689
- constante (viejo)  n= 42  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=57%):
- matchup (EN VIVO)  n= 42  acc   43%  Brier 0.259  logloss 0.712
- constante (viejo)  n= 42  acc   52%  Brier 0.263  logloss 0.739
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 36** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 63.9 | 63.9 | 63.9 | empate |
| 1X2 logloss | 0.8722 | 0.8999 | 0.8831 | L3 |
| 1X2 brier | 0.5098 | 0.5333 | 0.5188 | L3 |
| Over 2.5 acc% | 47.2 | 50.0 | 47.2 | **mx** |
| Over 2.5 logloss | 0.6918 | 0.6907 | 0.6918 | **mx** |
| Over 2.5 brier | 0.2494 | 0.2489 | 0.2494 | **mx** |
| BTTS acc% | 41.7 | 41.7 | 41.7 | empate |
| BTTS logloss | 0.7128 | 0.7208 | 0.7128 | empate |
| BTTS brier | 0.2593 | 0.2637 | 0.2593 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 68 | 3.05 | 3.94 | -2.11 (infraestima) | -0.27 (infraestima) | 41.0% (O/U) |
| tiros (orientativo) | 68 | 6.82 | 8.49 | -5.90 (infraestima) | -0.76 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 68 | 1.9 | 2.17 | +1.39 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 48** partidos (1056 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 1056 | 8% | 0.2555 | 0.0703 | 0.016 | sí | validado (backtest) |
| asistencia | 1056 | 6% | 0.2327 | 0.0586 | 0.027 | no | validado (backtest) |
| tarjeta | 1056 | 10% | 0.3559 | 0.1000 | 0.087 | no | validado (backtest · tope en cola) |
| tiros a puerta | 1056 | 21% | 0.5747 | 0.1514 | 0.091 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.45% vs real 9.85% → sesgo **+6.60pp**
- corregido: pred 12.11% vs real 9.85% → sesgo **+2.26pp** (factor 0.7361, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 42 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=73
- ECE observado = **0.111** vs nulo p95 = 0.168 → dentro del ruido.
- logloss L3 = **0.8439** vs baseline 1.0777 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
