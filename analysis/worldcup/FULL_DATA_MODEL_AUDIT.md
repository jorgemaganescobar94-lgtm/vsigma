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
| 27 | `club_form_diff` (opcional, flag `CLUB_FORM_FEATURE`) | `worldcup_club_form_multiseason.csv` (forma de club **2025/2024/2023** ponderada por recencia, tier de liga) | **REDUNDANTE con L3** — empeora ~0.0009 aun en test favorable (ver abajo) |

| 28 | `duels_won_diff` (opcional, flag `EXTRA_PLAYER_AGG`) | agregado por partido de `/fixtures/players` (rolling) | **INERTE** — 0 cobertura en burn-in → peso 0 |
| 29 | `dribbles_success_diff` | idem | **INERTE** (0 burn-in) |
| 30 | `tackles_total_diff` | idem | **INERTE** (0 burn-in) |
| 31 | `interceptions_diff` | idem | **INERTE** (0 burn-in) |

**intl player-agg (features 28-31):** agregados por partido internacional (duelos/regates/entradas/
intercepciones) sumados a total por equipo, rolling point-in-time. Coste API 0 (re-parseo caché, 152
fixtures). **Honesto: TODOS los datos son 2024+ (0 en burn-in <2024)** → el modelo no puede aprender
un peso → entran **inertes (peso ≈0, sin efecto)**. Añadidos por decisión maximalista SIN gate.
Reversible: `EXTRA_PLAYER_AGG=False` → vuelve al set de 27 EXACTAMENTE.

**club_form (feature 27):** fuerza de selección desde la forma de club 2025 de sus jugadores
(goles+asistencias/90 + rating, ponderado por minutos, normalizado por tier de liga). Coste API 0
(re-parseo del caché, 100% cobertura de las 48 plantillas). Anti-leakage EN VIVO (temporada 2025 <
Mundial 2026). **Reversible**: `CLUB_FORM_FEATURE=True` usa el artifact de 27 feats; `False` vuelve al
de 26 EXACTAMENTE. Orden resultante (Alemania/Francia/España arriba, Sudáfrica/Qatar abajo) ≈ L3 →
señal de fuerza ya capturada por el L3.

**Resumen honesto:** de 26 features, la señal real la aportan las 4 de L3 (y algo forma/squad). Las
~13 de stats rolling + rating son **nulas o redundantes** para 1X2 — meten ruido. Por eso el modelo,
pese a la regularización fuerte, **mide peor** que el L3/ensemble. Se documenta para que quede
constancia de qué aporta cada una.

## A/B honesto (OOS internacionales 2024-2025, N=2680)

- **1X2 logloss:** full-data-26 **0.9273** vs L3 **0.9178** → Δ(L3−fd) = **−0.0095** IC95 [−0.0172,−0.0018], p(fd mejor)=0.01.
- **club_form MULTI-temporada (marginal 26 vs 27):** base(26) **0.9273** vs +club_form(27) **0.9282** → Δ = **−0.0009** IC95 [−0.0016,−0.0002], p=0.01 → **REDUNDANTE/peor** aun con las 3 temporadas (2025/2024/2023, 2645 calls reales, 48/48 selecciones). 2023 cae en burn-in → entrenable, pero **no aporta señal** sobre el L3. Anti-leakage EN VIVO (todas < Mundial 2026); el A/B OOS es indicativo (valor estático por equipo → look-ahead leve). Confirma el patrón del squad-quality.
- **intl player-agg (marginal 27 vs 31):** +club_form(27) **0.9281** vs +player-agg(31) **0.9281** → Δ = **−0.0000** IC95 [−0.0000, +0.0000] → **INERTE** (0 cobertura burn-in → peso 0; entran pero no cambian nada). Coste honesto de la ingestión maximalista sin gate.
- **REGULARIZACIÓN L1 ADOPTADA (2026-07-01, `FULL_DATA_REG="l1c0.1"`):** el barrido por CV burn-in mostró que L2 C=0.30 infra-regularizaba. Con **L1 C=0.1 (saga)** el 1X2 OOS pasa de **0.9281 → 0.9187** (Δ+0.0094 vs config vieja, CI95[+0.0032,+0.0156]) → **empata el ensemble/L3** (0.9187 vs 0.9178, Δ−0.0009 CI cruza 0 = sin diferencia). NO lo bate (techo). L1 deja **21 de 31 features a peso 0** (todas las nulas: club_form, 13 stats rolling, team_rating, squad, 4 player-agg, l3_logit_h); sobreviven ~10 (L3 strength + neutral + forma + rest + h2h). Poisson α=1.0 sin cambio (Over/BTTS iguales). **Reversible:** `FULL_DATA_REG="l2c0.3"` reentrena el modelo viejo **byte-exact** (Δ0).
- **Veredicto:** con L1, el full-data **iguala al ensemble/L3** (ya no ~1% peor); club_form redundante, player-agg inerte (L1 los anula). **NUNCA se afirma superar al ensemble.** Regularización fuerte
  evita que las features nulas lo revienten, pero no puede crear señal donde no la hay.
- El marcador vivo `worldcup_full_data_ab_scorer.py` sigue el A/B fd vs ensemble sobre los partidos WC
  liquidados; si full-data queda por detrás (esperado), es la base para revertir `FULL_DATA_LIVE=False`.

**Framing de producto:** el modelo full-data se muestra con la etiqueta honesta *"usa todas las
features disponibles — NO más preciso que L3/ensemble"*. Ningún claim de mayor precisión.
