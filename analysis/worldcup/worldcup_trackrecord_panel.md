# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-06-30T16:50:09+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 47** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 47 | 1.0815 | 0.6555 | 40.4 | 0.000 | 0.0% |
| L3 (oficial) | 47 | 0.8245 | 0.4772 | 66.0 | 0.141 | +27.2% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 57%) | L3 (Poisson) | 47 | 45 | 0.248 | 0.688 |
| Over 2.5 | base-rate | 47 | 57 | 0.244 | 0.682 |
| BTTS (real 49%) | L3 (Poisson) | 47 | 62 | 0.236 | 0.667 |
| BTTS | base-rate | 47 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=50%):
- matchup (EN VIVO)  n= 16  acc   56%  Brier 0.240  logloss 0.674
- constante (viejo)  n= 16  acc   50%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=62%):
- matchup (EN VIVO)  n= 16  acc   38%  Brier 0.271  logloss 0.738
- constante (viejo)  n= 16  acc   56%  Brier 0.286  logloss 0.816
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 10** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 60.0 | 60.0 | 60.0 | empate |
| 1X2 logloss | 0.8545 | 0.8867 | 0.8682 | L3 |
| 1X2 brier | 0.5045 | 0.5322 | 0.5155 | L3 |
| Over 2.5 acc% | 50.0 | 50.0 | 50.0 | empate |
| Over 2.5 logloss | 0.6758 | 0.6697 | 0.6758 | **mx** |
| Over 2.5 brier | 0.2416 | 0.2386 | 0.2416 | **mx** |
| BTTS acc% | 30.0 | 30.0 | 30.0 | empate |
| BTTS logloss | 0.7584 | 0.7542 | 0.7584 | **mx** |
| BTTS brier | 0.2806 | 0.2803 | 0.2806 | empate |
> ⚠️ muestra pequeña (N=10 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 42 | 2.87 | 3.75 | -1.81 (infraestima) | -0.68 (infraestima) | 48.0% (O/U) |
| tiros (orientativo) | 42 | 7.25 | 8.71 | -5.90 (infraestima) | -2.20 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 42 | 1.9 | 2.19 | +1.50 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 22** partidos (484 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 484 | 8% | 0.2571 | 0.0697 | 0.035 | sí | validado (backtest) |
| asistencia | 484 | 6% | 0.2233 | 0.0570 | 0.027 | no | validado (backtest) |
| tarjeta | 484 | 10% | 0.3446 | 0.0961 | 0.082 | no | validado (backtest · tope en cola) |
| tiros a puerta | 484 | 20% | 0.5305 | 0.1549 | 0.092 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.30% vs real 9.50% → sesgo **+6.79pp**
- corregido: pred 13.12% vs real 9.50% → sesgo **+3.61pp** (factor 0.8049, flag `CARD_PROP_CORRECTION`)
>  ⚠️ muestra pequeña (N=22 < umbral 30): métricas orientativas, aún no concluyentes.
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 16 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=47
- ECE observado = **0.141** vs nulo p95 = 0.204 → dentro del ruido.
- logloss L3 = **0.8245** vs baseline 1.0815 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
