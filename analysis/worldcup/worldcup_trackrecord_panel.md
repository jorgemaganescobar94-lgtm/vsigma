# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-06T12:09:30+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 63** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 63 | 1.0710 | 0.6485 | 42.9 | 0.000 | 0.0% |
| L3 (oficial) | 63 | 0.8338 | 0.4825 | 66.7 | 0.109 | +25.6% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 57%) | L3 (Poisson) | 63 | 41 | 0.252 | 0.698 |
| Over 2.5 | base-rate | 63 | 57 | 0.245 | 0.683 |
| BTTS (real 49%) | L3 (Poisson) | 63 | 59 | 0.237 | 0.670 |
| BTTS | base-rate | 63 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=53%):
- matchup (EN VIVO)  n= 32  acc   44%  Brier 0.253  logloss 0.700
- constante (viejo)  n= 32  acc   47%  Brier 0.250  logloss 0.694
- BTTS     (real Yes=56%):
- matchup (EN VIVO)  n= 32  acc   44%  Brier 0.256  logloss 0.707
- constante (viejo)  n= 32  acc   59%  Brier 0.261  logloss 0.741
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 26** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 65.4 | 65.4 | 65.4 | empate |
| 1X2 logloss | 0.8585 | 0.8808 | 0.8665 | L3 |
| 1X2 brier | 0.5005 | 0.5206 | 0.5077 | L3 |
| Over 2.5 acc% | 38.5 | 42.3 | 38.5 | **mx** |
| Over 2.5 logloss | 0.7063 | 0.7032 | 0.7063 | **mx** |
| Over 2.5 brier | 0.2566 | 0.2551 | 0.2566 | **mx** |
| BTTS acc% | 42.3 | 42.3 | 42.3 | empate |
| BTTS logloss | 0.7077 | 0.7187 | 0.7077 | empate |
| BTTS brier | 0.2566 | 0.2627 | 0.2566 | empate |
> ⚠️ muestra pequeña (N=26 < 30): **NO se declara ganador**, el acumulado crece hasta el final del Mundial. Si el mx queda por detrás, este marcador + el A/B son la base para revertir (MAXMODEL_LIVE=False).
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 58 | 3.23 | 4.15 | -2.19 (infraestima) | -0.32 (infraestima) | 41.0% (O/U) |
| tiros (orientativo) | 58 | 7.06 | 8.69 | -6.01 (infraestima) | -0.88 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 58 | 1.97 | 2.24 | +1.46 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 38** partidos (836 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 836 | 8% | 0.2480 | 0.0677 | 0.019 | sí | validado (backtest) |
| asistencia | 836 | 6% | 0.2369 | 0.0589 | 0.033 | no | validado (backtest) |
| tarjeta | 836 | 10% | 0.3477 | 0.0973 | 0.083 | no | validado (backtest · tope en cola) |
| tiros a puerta | 836 | 20% | 0.5262 | 0.1500 | 0.095 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.39% vs real 9.57% → sesgo **+6.82pp**
- corregido: pred 12.28% vs real 9.57% → sesgo **+2.71pp** (factor 0.7490, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 32 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=63
- ECE observado = **0.109** vs nulo p95 = 0.176 → dentro del ruido.
- logloss L3 = **0.8338** vs baseline 1.0710 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
