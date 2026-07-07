# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-07T11:01:10+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 65** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 65 | 1.0709 | 0.6490 | 41.5 | 0.000 | 0.0% |
| L3 (oficial) | 65 | 0.8294 | 0.4792 | 67.7 | 0.107 | +26.2% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 57%) | L3 (Poisson) | 65 | 42 | 0.252 | 0.697 |
| Over 2.5 | base-rate | 65 | 57 | 0.245 | 0.684 |
| BTTS (real 49%) | L3 (Poisson) | 65 | 58 | 0.238 | 0.671 |
| BTTS | base-rate | 65 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=53%):
- matchup (EN VIVO)  n= 34  acc   44%  Brier 0.253  logloss 0.698
- constante (viejo)  n= 34  acc   47%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=56%):
- matchup (EN VIVO)  n= 34  acc   44%  Brier 0.257  logloss 0.708
- constante (viejo)  n= 34  acc   56%  Brier 0.261  logloss 0.740
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 28** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 67.9 | 67.9 | 67.9 | empate |
| 1X2 logloss | 0.8465 | 0.8786 | 0.8594 | L3 |
| 1X2 brier | 0.4915 | 0.5185 | 0.5022 | L3 |
| Over 2.5 acc% | 39.3 | 42.9 | 39.3 | **mx** |
| Over 2.5 logloss | 0.7044 | 0.7018 | 0.7044 | **mx** |
| Over 2.5 brier | 0.2557 | 0.2544 | 0.2557 | **mx** |
| BTTS acc% | 42.9 | 42.9 | 42.9 | empate |
| BTTS logloss | 0.7084 | 0.7173 | 0.7084 | empate |
| BTTS brier | 0.257 | 0.262 | 0.257 | empate |
> ⚠️ muestra pequeña (N=28 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 60 | 3.17 | 4.09 | -2.16 (infraestima) | -0.31 (infraestima) | 42.0% (O/U) |
| tiros (orientativo) | 60 | 6.9 | 8.56 | -5.89 (infraestima) | -0.84 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 60 | 1.96 | 2.22 | +1.46 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 40** partidos (880 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 880 | 8% | 0.2447 | 0.0666 | 0.018 | sí | validado (backtest) |
| asistencia | 880 | 6% | 0.2367 | 0.0589 | 0.033 | no | validado (backtest) |
| tarjeta | 880 | 9% | 0.3467 | 0.0967 | 0.085 | no | validado (backtest · tope en cola) |
| tiros a puerta | 880 | 20% | 0.5221 | 0.1498 | 0.098 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.41% vs real 9.43% → sesgo **+6.98pp**
- corregido: pred 12.12% vs real 9.43% → sesgo **+2.68pp** (factor 0.7383, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 34 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=65
- ECE observado = **0.107** vs nulo p95 = 0.173 → dentro del ruido.
- logloss L3 = **0.8294** vs baseline 1.0709 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
