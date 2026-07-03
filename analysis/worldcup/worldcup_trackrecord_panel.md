# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-03T10:41:10+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 56** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 56 | 1.0571 | 0.6384 | 46.4 | 0.000 | 0.0% |
| L3 (oficial) | 56 | 0.8200 | 0.4731 | 67.9 | 0.110 | +25.9% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +25.2% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 59%) | L3 (Poisson) | 56 | 45 | 0.248 | 0.690 |
| Over 2.5 | base-rate | 56 | 59 | 0.242 | 0.677 |
| BTTS (real 48%) | L3 (Poisson) | 56 | 61 | 0.237 | 0.669 |
| BTTS | base-rate | 56 | 52 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=56%):
- matchup (EN VIVO)  n= 25  acc   52%  Brier 0.245  logloss 0.682
- constante (viejo)  n= 25  acc   44%  Brier 0.251  logloss 0.694
- BTTS     (real Yes=56%):
- matchup (EN VIVO)  n= 25  acc   44%  Brier 0.261  logloss 0.717
- constante (viejo)  n= 25  acc   56%  Brier 0.270  logloss 0.766
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 19** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 68.4 | 68.4 | 68.4 | empate |
| 1X2 logloss | 0.8271 | 0.8111 | 0.8164 | **mx** |
| 1X2 brier | 0.4793 | 0.4724 | 0.4731 | **mx** |
| Over 2.5 acc% | 47.4 | 47.4 | 47.4 | empate |
| Over 2.5 logloss | 0.6863 | 0.68 | 0.6863 | **mx** |
| Over 2.5 brier | 0.2467 | 0.2436 | 0.2467 | **mx** |
| BTTS acc% | 42.1 | 42.1 | 42.1 | empate |
| BTTS logloss | 0.7214 | 0.722 | 0.7214 | empate |
| BTTS brier | 0.2631 | 0.2643 | 0.2631 | empate |
> ⚠️ muestra pequeña (N=19 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 51 | 2.95 | 3.88 | -1.85 (infraestima) | -0.61 (infraestima) | 45.0% (O/U) |
| tiros (orientativo) | 51 | 7.02 | 8.52 | -5.84 (infraestima) | -1.92 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 51 | 1.95 | 2.24 | +1.62 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 31** partidos (682 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 682 | 8% | 0.2476 | 0.0679 | 0.021 | sí | validado (backtest) |
| asistencia | 682 | 6% | 0.2417 | 0.0609 | 0.032 | no | validado (backtest) |
| tarjeta | 682 | 9% | 0.3361 | 0.0926 | 0.085 | no | validado (backtest · tope en cola) |
| tiros a puerta | 682 | 20% | 0.5431 | 0.1498 | 0.094 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.32% vs real 8.94% → sesgo **+7.37pp**
- corregido: pred 12.24% vs real 8.94% → sesgo **+3.29pp** (factor 0.7498, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 25 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=56
- ECE observado = **0.110** vs nulo p95 = 0.187 → dentro del ruido.
- logloss L3 = **0.8200** vs baseline 1.0571 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
