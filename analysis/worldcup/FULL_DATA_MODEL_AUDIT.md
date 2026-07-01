# Auditoría de fórmulas — qué dato alimenta CADA predicción (World Cup 2026)

**Fecha:** 2026-07-01 · **Contexto:** decisión EXPLÍCITA de Jorge de shippar un modelo *full-data*
que ingiere TODAS las features disponibles en la predicción 1X2/goles mostrada, wire vivo
**reversible**, sabiendo que **MIDE PEOR**. Este documento deja constancia, por predicción, de
exactamente qué datos la alimentan hoy, y marca honestamente qué features son nulas/redundantes.
**No se afirma mayor precisión.** Read-only / aislado / cero mercado.

## Cadena de predicción mostrada (resolver `pred_1x2`)

Prioridad de lo que se MUESTRA/envía (cada eslabón encadena por delta-Poisson sobre el anterior):

```
inj_*  (bajas EN VIVO)                       — INJURIES_LIVE
  > ctx_*  (contexto de grupo)               — CONTEXT_LIVE
    > fd_*  (MODELO FULL-DATA, base)         — FULL_DATA_LIVE   ← NUEVO
      > ens_*  (ENSEMBLE 50/50 mx+L3)        — ENSEMBLE_1X2_LIVE
        > mx_*  (motor amplio)               — MAXMODEL_LIVE
          > our_*  (L3 puro)                 — base siempre presente
```

**Reversibilidad exacta:** `FULL_DATA_LIVE=False` → no se escribe `fd_*` → el picker de
contexto/lesiones y el resolver caen a `ens_*` EXACTAMENTE (Δ=0). Igual para cada flag aguas abajo.
`our_*/mx_*/ens_*/fd_*` **nunca** se sobrescriben (sombra para A/B + rollback).

---

## 1) 1X2 mostrado

| Estado | Qué lo calcula | Datos que lo alimentan |
|---|---|---|
| `FULL_DATA_LIVE=True` (hoy) | **Modelo full-data** (logit multinomial regularizado, C=0.30, temperature) → luego contexto/bajas encadenan | **Las 26 features** de abajo |
| `FULL_DATA_LIVE=False` | Ensemble 50/50 `mx`+`L3` | mx (núcleo L3 + forma/H2H/descanso) y L3 |

El full-data usa la salida L3 (`our_*`) como feature de fuerza, así que **contiene** la señal del L3
más todo lo demás. Contexto de grupo y bajas se aplican encima igual que antes.

## 2) Goles / Over 2.5 / BTTS

| Estado | Qué lo calcula | Datos |
|---|---|---|
| `FULL_DATA_LIVE=True` | `fd_xg_home/away` = **dos GLM Poisson** del full-data (regularizados, α=1.0), sobre las 26 features → matriz Poisson → Over/BTTS | Las 26 features |
| `FULL_DATA_LIVE=False` | `ens_xg_* = our_xg_*` → xG de L3 (matchup total) → Poisson | L3 |

## 3) Stats por equipo (córners / tiros / tarjetas)

**NO tocado por el full-data.** Lo calcula `stats_model` (regresión att/conc ajustada al rival +
ventaja local, ridge, walk-forward). Correcciones de nivel de display aparte
(`worldcup_stats_level_correction`, `card_risk_adjuster`). El full-data es solo 1X2/goles.

## 4) Props de jugador (gol / asistencia / tarjeta / SOT)

**NO tocado por el full-data.** `analysis/players/player_events_core` (+ `worldcup_player_props`,
corrección multiplicativa de p_card). Independiente del modelo 1X2/goles.

---

## Auditoría feature-a-feature del modelo full-data (26 features)

Todas son **point-in-time, anti-leakage** (media time-decay del equipo/rival SOLO de partidos
previos; nunca el valor del propio partido). Veredicto de señal según backtests offline (bake-off,
feature studies, new-fields backtest 2026-07-01):

| # | Feature | Fuente | Señal para 1X2 (honesto) |
|---|---|---|---|
| 1-4 | `l3_logit_h/a`, `l3_xg_h/a` | Salida L3 (`our_*`) | **REAL — es el núcleo.** El L3 es el techo demostrado |
| 5 | `neutral` | Fixture | Marginal (WC casi todo neutral) |
| 6-9 | `form_gf/ga/ppg/streak_diff` | `international_results` (EWMA) | Modesta; parte ya dentro del mx |
| 10 | `rest_diff` | `international_results` | Débil |
| 11 | `h2h_gd` | `international_results` | Débil |
| 12 | `squad_diff` | `squad_quality_raw_48` | Modesta; cobertura solo 48 selecciones WC |
| 13 | `team_rating_diff` | caché `/fixtures/players` | **REDUNDANTE con L3** (≈ fuerza) + cobertura fina → nula/negativa |
| 14-15 | `sot_diff`, `shots_diff` | caché `/fixtures/statistics` + stats_raw | **NULA** para 1X2 |
| 16-18 | `shots_inbox/outbox/blocked_diff` | caché stats | **NULA** (probado 2026-07-01, CI cruza 0) |
| 19 | `gk_saves_diff` | caché stats | **NULA** (tendencia peor) |
| 20-22 | `passes_total/acc/pct_diff` | caché stats | **NULA** (estilo, ya probado) |
| 23 | `offsides_diff` | caché stats | **NULA** |
| 24 | `fouls_diff` | caché stats | **NULA** |
| 25 | `possession_diff` | caché stats + stats_raw | **NULA** (estilo, ya probado) |
| 26 | `corners_diff` | caché stats + stats_raw | **NULA** para 1X2 |

**Resumen honesto:** de 26 features, la señal real la aportan las 4 de L3 (y algo forma/squad). Las
~13 de stats rolling + rating son **nulas o redundantes** para 1X2 — meten ruido. Por eso el modelo,
pese a la regularización fuerte, **mide peor** que el L3/ensemble. Se documenta para que quede
constancia de qué aporta cada una.

## A/B honesto (OOS internacionales 2024-2025, N=2680)

- **1X2 logloss:** full-data **0.9273** vs L3 **0.9178** → Δ(L3−fd) = **−0.0095** IC95 [−0.0172,−0.0018], p(fd mejor)=0.01.
- **Veredicto:** full-data **PEOR** de forma significativa (~1%), como se esperaba. Regularización fuerte
  evita que las features nulas lo revienten, pero no puede crear señal donde no la hay.
- El marcador vivo `worldcup_full_data_ab_scorer.py` sigue el A/B fd vs ensemble sobre los partidos WC
  liquidados; si full-data queda por detrás (esperado), es la base para revertir `FULL_DATA_LIVE=False`.

**Framing de producto:** el modelo full-data se muestra con la etiqueta honesta *"usa todas las
features disponibles — NO más preciso que L3/ensemble"*. Ningún claim de mayor precisión.
