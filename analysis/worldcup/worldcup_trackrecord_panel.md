# 📊 Panel de Track-Record — Mundial 2026 (vSIGMA)
_Generado: 2026-07-10T10:59:01+00:00 · consolidado de scorecards existentes · **solo lectura, no recalcula predicciones** · sin mercado/cuotas._

> Honestidad: **validado** = superó el baseline en backtest histórico; **sombra** = en observación en vivo; donde la muestra aún no basta se marca explícitamente.

## 1X2 — modelo L3 (oficial)
**N = 68** partidos liquidados · 1X2 a 90' vs resultado real (sin mercado).

| predictor | N | logloss | brier | acc% | ECE | skill vs base |
|---|---:|---:|---:|---:|---:|---:|
| base-rate (baseline) | 68 | 1.0705 | 0.6484 | 42.6 | 0.000 | 0.0% |
| L3 (oficial) | 68 | 0.8296 | 0.4791 | 67.6 | 0.109 | +26.1% |
| v2 | 43 | 0.8501 | 0.4884 | 67.4 | 0.138 | +24.8% |
> ⚠️ semántica mixta: parte de las filas son 'primera predicción (mañana)' y parte 'última pre-saque' (cambio lock-at-KO a mitad de torneo) — interpretar la mejora con cautela.

## Goles — Over 2.5 y BTTS (L3 Poisson vs base-rate)

| mercado | modelo | N | acc% | brier | logloss |
|---|---|---:|---:|---:|---:|
| Over 2.5 (real 56%) | L3 (Poisson) | 68 | 44 | 0.250 | 0.693 |
| Over 2.5 | base-rate | 68 | 56 | 0.247 | 0.686 |
| BTTS (real 49%) | L3 (Poisson) | 68 | 59 | 0.239 | 0.673 |
| BTTS | base-rate | 68 | 51 | 0.250 | 0.693 |

### A/B total de goles — matchup vs constante
- Over 2.5 (real Over=51%):
- matchup (EN VIVO)  n= 37  acc   49%  Brier 0.249  logloss 0.691
- constante (viejo)  n= 37  acc   49%  Brier 0.250  logloss 0.693
- BTTS     (real Yes=54%):
- matchup (EN VIVO)  n= 37  acc   46%  Brier 0.257  logloss 0.709
- constante (viejo)  n= 37  acc   51%  Brier 0.265  logloss 0.746
- (si 'constante' bate sostenidamente a 'matchup' -> revisar / poner TOTAL_MATCHUP_LIVE=False)

## L3 vs Motor máximo vs Ensemble (en vivo, desde 27-jun)
**N = 31** partidos liquidados con predicción mx · cara a cara congelado al saque (lock-at-KO, anti-hindsight) vs resultado real · sin mercado. ens = ENSEMBLE 1X2 mostrado (media 50/50 mx+L3); en Over2.5/BTTS ens=L3 por diseño.

| métrica | L3 | mx | ens | líder |
|---|---:|---:|---:|---|
| 1X2 acc% | 67.7 | 67.7 | 67.7 | empate |
| 1X2 logloss | 0.8453 | 0.8659 | 0.8526 | L3 |
| 1X2 brier | 0.4902 | 0.5082 | 0.4964 | L3 |
| Over 2.5 acc% | 45.2 | 48.4 | 45.2 | **mx** |
| Over 2.5 logloss | 0.6945 | 0.6913 | 0.6945 | **mx** |
| Over 2.5 brier | 0.2507 | 0.2491 | 0.2507 | **mx** |
| BTTS acc% | 45.2 | 45.2 | 45.2 | empate |
| BTTS logloss | 0.7101 | 0.7187 | 0.7101 | empate |
| BTTS brier | 0.2579 | 0.2627 | 0.2579 | empate |
> _Solo mide; NO toca el modelo ni las predicciones (mx_*/l3_* congelados en el log)._

## Stats por equipo — predicho vs real (en vivo)
**Total por partido** (suma de ambos equipos) · predicción congelada al saque (anti-hindsight) vs real liquidado · sin mercado.

| stat | N | MAE | RMSE | sesgo crudo (pred−real) | sesgo corregido | ¿acierto línea? |
|---|---:|---:|---:|---|---|---|
| córners (baja conf.) | 63 | 3.12 | 4.03 | -2.16 (infraestima) | -0.30 (infraestima) | 41.0% (O/U) |
| tiros (orientativo) | 63 | 6.89 | 8.49 | -5.93 (infraestima) | -0.81 (infraestima) | — |
| tarjetas (ruido · oculto en ficha) | 63 | 1.95 | 2.21 | +1.46 (sobrestima) | — (no corregido) | — |
> 🔧 **Corrección de nivel auto-aprendida (córners/tiros MOSTRADOS)**: aditiva, encogida por muestra (×N/(N+25)), reversible (flag `STATS_LEVEL_CORRECTION`). El **sesgo corregido** debe acercarse a 0 vs el crudo. **Tarjetas EXCLUIDAS** (ruido).
> Honestidad: **córners = baja confianza · tarjetas = ruido** → un error alto es ESPERABLE; el marcador lo refleja sin maquillar. **No** se declara nada 'bueno/malo': solo se acumula durante el torneo.
> _Solo mide / corrige el valor MOSTRADO; el modelo y el log (st_*/result_*) quedan en CRUDO._

## Props de jugador (SOMBRA · heurístico)
**Liquidados = 43** partidos (946 filas jugador-prop) · umbral graduación N≥30.

| prop | N | base% | logloss | brier | ECE | ¿mejora vivo? | estado backtest |
|---|---:|---:|---:|---:|---:|---|---|
| gol | 946 | 8% | 0.2499 | 0.0685 | 0.019 | sí | validado (backtest) |
| asistencia | 946 | 6% | 0.2320 | 0.0581 | 0.029 | no | validado (backtest) |
| tarjeta | 946 | 10% | 0.3478 | 0.0975 | 0.084 | no | validado (backtest · tope en cola) |
| tiros a puerta | 946 | 20% | 0.5542 | 0.1511 | 0.095 | no | ranking solo (no %) |

**Tarjeta — sesgo crudo vs corregido** (deflación reversible de `p_card`; gol/asistencia NO se tocan):
- crudo: pred 16.44% vs real 9.62% → sesgo **+6.82pp**
- corregido: pred 12.13% vs real 9.62% → sesgo **+2.51pp** (factor 0.7376, flag `CARD_PROP_CORRECTION`)
> _Validado (backtest) = graduó en el backtest histórico (N=3062 jugador-partido). El estado EN VIVO sigue en sombra hasta liquidar N≥umbral en partidos del Mundial._

## A/B de contexto — L3 puro vs ajuste de grupo (SOMBRA)
**No triviales liquidados = 9** (de 37 liquidados) · umbral N≥20.
> Estado: **sigue en SOMBRA** — muestra insuficiente para graduar; los multiplicadores son hipótesis (signo ambiguo), el scorecard es el juez.
>  ⚠️ muestra pequeña (N=9 < umbral 20): métricas orientativas, aún no concluyentes.

## Monitor de calibración L3 (1X2)
**Estado: 🟢 OK** · N=68
- ECE observado = **0.109** vs nulo p95 = 0.169 → dentro del ruido.
- logloss L3 = **0.8296** vs baseline 1.0705 (bate la tasa base).
> _Monitor solo alerta; NO toca el modelo._

---
_Panel generado por build_worldcup_trackrecord_panel.py · no modifica el modelo ni las predicciones · World Cup = producto en sombra aislado._
