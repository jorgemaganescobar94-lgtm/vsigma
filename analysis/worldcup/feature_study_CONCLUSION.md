# Feature study — World Cup data model (June 2026)

ISOLATED in `analysis/worldcup/`. Real data only, **ZERO market/odds**. Not production
(the betting pipeline is untouched). Goal: add several real-data sources, measure each
one's **out-of-sample (walk-forward)** contribution, and keep **only** the features that
clearly and stably improve. Honest gating intact.

## Method
- Baselines = the current models: L3 rating (1X2 / goals) and the opponent-adjusted
  stats model (corners / shots).
- Each candidate feature is added **separately**, the model is **refit strict walk-forward**
  (refit every 45 days on prior rows only; predict each row pre-fit), and scored on OOS rows
  (`date >= 2024-08-01`).
- 1X2/goals metrics: multiclass **log-loss** + **Brier** (raw Poisson, no isotonic, so
  calibration is not a confound) and goals RMSE. Stats metric: **RMSE** of the count.

## Study A — goals / 1X2  (baseline = L3 `sup_pre_l3`, 8860 matches, ~2525 OOS)
| feature | logloss | brier | Δlogloss | Δbrier | verdict |
|---|---|---|---|---|---|
| baseline (sup_pre_l3) | 0.9227 | 0.5469 | — | — | BASELINE |
| +rest_diff (días descanso) | 0.9228 | 0.5469 | −0.0% | −0.0% | **discard** |
| +hfa (anfitrión/local) | 0.9228 | 0.5467 | −0.0% | +0.0% | **discard** |
| +sup2 (interacción fuerza) | 0.9223 | 0.5465 | +0.0% | +0.1% | **discard** |
| +xg_sup (rating xG) | — | — | — | — | **insuficiente** (xG sólo 14% de fixtures → 0 partidos OOS con rating válido) |
| +rest+sup2 | 0.9224 | 0.5465 | +0.0% | +0.1% | **discard** |

**Conclusión A: ninguna feature mejora.** La supremacía del rating L3 ya captura todo lo
que estas señales aportan; descanso, ventaja de anfitrión e interacción de fuerza son ~0 OOS.
xG **no es evaluable**: la cobertura de `/fixtures/statistics` para partidos internacionales
es del 14% (177/1264 fixtures; mayoría de amistosos/clasificatorios sin xG), insuficiente para
un rating walk-forward. **Se integra: nada.**

## Study B — corners / shots  (baseline = opponent-adjusted att/conc + home; 2528 filas)
| stat | feature | RMSE | ΔRMSE | verdict |
|---|---|---|---|---|
| corners | baseline | 2.847 | — | BASELINE |
| corners | +poss_form | 2.839 | +0.3% | discard (marginal, muestra −) |
| corners | +sot_form | 2.838 | +0.3% | discard (marginal, muestra −) |
| corners | +rest | 2.847 | −0.0% | discard |
| corners | **+opp_str** | **2.729** | **+4.1%** | **KEEP** |
| shots | baseline | 5.545 | — | BASELINE |
| shots | +poss_form | 5.504 | +0.7% | discard (marginal, muestra −) |
| shots | +sot_form | 5.479 | +1.2% | discard (marginal, muestra −) |
| shots | +rest | 5.555 | −0.2% | discard |
| shots | **+opp_str** | **5.072** | **+8.5%** | **KEEP** |

**Conclusión B: sólo `opp_str` (fuerza L3 del rival) mejora de forma clara y estable**
(córners +4.1%, tiros +8.5%, **muestra completa**). `poss_form`/`sot_form` para tiros pasan
el umbral pero son marginales (+0.7/1.2%) y sobre **muestra reducida** (exigen ≥3 partidos
previos con ese campo) → se descartan por parsimonia y estabilidad. `rest` ≈ 0.

## Integrado (sólo lo que mejora)
`opp_str` añadido como regresor estándar (no regularizado) al modelo de stats
(`stats_model.py`): `logE[count] = mu + gamma·home + β·opp_str_z + att[team] + conc[opp]`,
con `opp_str` = fuerza L3 del rival estandarizada (mean/std en la calibración) y
`β` negativo (rival más fuerte → menos córners/tiros). Re-fit + walk-forward confirma el
salto OOS (deviance-lift vs base-rate):

| stat | lift antes | lift después | β(opp_str) | gating |
|---|---|---|---|---|
| córners | +14.3% | **+19.9%** | −0.24 | se muestra (BAJA CONF) |
| tiros | +28.3% | **+38.1%** | −0.24 | se muestra (BAJA CONF) |
| tarjetas | +2.2% | +3.5% | +0.12 | **oculta** (sigue <4% → ruido) |

El gating honesto NO cambia: córners/tiros se muestran, tarjetas sigue fuera de la ficha
(sólo métrica del scorecard). Predicción usa la fuerza L3 del rival ya committeada
(`national_elo_layer3_ratings.csv`); cero llamadas extra en runtime.

## Gasto de API
xG extraído sobre los 1264 fixtures **ya cacheados** (`/fixtures/statistics`, TTL 30 días) →
**spend = 0** (cuota 906→906). Resto del estudio: offline, 0 API. Total del estudio: **0 llamadas**.
