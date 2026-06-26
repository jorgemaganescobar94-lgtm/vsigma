# Bake-off OOS: L3 vs Dixon-Coles vs ML(GBM) — 1X2 y goles. CONCLUSIÓN

**Read-only · sin API · sin cambios en producción.** Script: `model_bakeoff_backtest.py`
(reutiliza el sup walk-forward de producción `national_elo_layer3_permatch.csv`, `national_elo_layer3.Isotonic`
y los pesos/decay de L3; DC y ML se ajustan walk-forward sobre los mismos datos).

## (a) Cómo se montó Dixon-Coles y el ML
- **Marco común:** mismos partidos internacionales (`international_results.csv` + `sup_pre_l3` walk-forward
  de permatch). Burn-in <2024 (calibración) / **OOS 2024-2025** (evaluación). Cada modelo se ajusta solo
  con datos previos; la **isotónica se ajusta SOLO en burn-in** (igual para los 3). Intersección de fixtures
  con predicción en los 3 → apples-to-apples. **2360 partidos OOS** / 3648 burn-in. Truncado Poisson KMAX=12.
- **Dixon-Coles:** ataque/defensa por equipo por MV Poisson ponderada (escalado iterativo multiplicativo),
  factor local H (solo si no neutral), corrección τ(ρ) de marcadores bajos por verosimilitud-perfil (grid).
  Decay temporal HL=730d (igual que L3), **refit walk-forward cada 60d** (ventana 6a). → λ asimétricas →
  matriz de marcadores τ-corregida → 1X2/OU/BTTS. (ρ mediana OOS ≈ −0.02.)
- **ML:** `sklearn HistGradientBoostingClassifier` (1.9.0, instalado) — multiclase 1X2 + binarios Over2.5/BTTS.
  Features leak-free: `sup_pre_l3`, neutral, importancia del torneo, tasas de forma reciente (goles a favor/en
  contra y puntos, últimos 10), nº de internacionales en 365d previos. Refit walk-forward cada 60d con
  `sample_weight` = decay temporal. (Las λ de DC NO se usan como feature: evita acoplamiento ML↔DC.)
- **L3 (campeón, tal cual producción):** `sup_pre_l3` → margin `a0+a1·sup` (lstsq/burn-in) → **total MATCHUP
  `tb0+tb1|sup|+tb2·sup²` con tope `TOTAL_CAP`** (el motor enviado) → Poisson → isotónica. Se incluye además
  `L3_const` (total constante = L3 vieja) para cuantificar la aportación del total matchup.

## (b) Tabla OOS (mismos 2360 partidos) con significancia vs L3
Δlogloss = L3 − modelo (>0 = el modelo MEJORA sobre L3); IC95% bootstrap pareado (20000, semilla fija).

**1X2 (H/D/A):**
| modelo | logloss | brier | ECE | acc% | Δlogloss vs L3 (IC95%) |
|---|---|---|---|---|---|
| **L3** | **0.90215** | 0.53047 | 0.025 | 58.2 | (ref) |
| L3_const | 0.90147 | 0.53005 | 0.024 | 58.2 | +0.0007 [−0.0004,+0.0018] no signif |
| DixonColes | 0.94246 | 0.53571 | 0.047 | 58.6 | −0.0403 [−0.073,−0.011] **PEOR** |
| ML_GBM | 0.92741 | 0.53869 | 0.049 | 57.8 | −0.0253 [−0.042,−0.012] **PEOR** |

**Over 2.5** (real 49%):
| modelo | logloss | brier | Δlogloss vs L3 (IC95%) |
|---|---|---|---|
| **L3** | 0.70250 | 0.24556 | (ref) |
| L3_const | 0.69738 | 0.24769 | +0.0051 [−0.008,+0.023] no signif |
| DixonColes | **0.68165** | 0.24431 | +0.0209 [+0.001,+0.046] **BATE** |
| ML_GBM | 0.68351 | **0.24306** | +0.0190 [+0.002,+0.040] **BATE** |

**BTTS** (real 44%):
| modelo | logloss | brier | Δlogloss vs L3 (IC95%) |
|---|---|---|---|
| **L3** | 0.68413 | 0.24335 | (ref) |
| L3_const | 0.70606 | 0.24476 | −0.0219 [−0.050,+0.002] no signif |
| DixonColes | 0.68129 | 0.24409 | +0.0028 [−0.008,+0.018] no signif |
| ML_GBM | **0.68087** | 0.24398 | +0.0033 [−0.006,+0.017] no signif |

## (c) ¿Alguno BATE a L3 de forma clara y significativa?
- **1X2 → NO. L3 es el techo.** DC y ML son **significativamente PEORES** (IC excluyen 0 por debajo). El
  margin-Massey ridge con up-weight cross-conf gana el resultado; DC (orientado a goles) y el GBM no lo
  alcanzan. `L3_const ≈ L3` → el total matchup no afecta al 1X2 (depende del margin).
- **BTTS → NO (con la L3 de producción).** El total matchup mejora la L3 de 0.706 a **0.684** (Δ−0.022);
  con esa L3, DC y ML **dejan de batirla** (IC incluyen 0). El "BATE" inicial era solo el handicap de la
  L3 con total constante.
- **Over 2.5 → SÍ, ventaja FINA pero significativa.** DC (Δ+0.021) y ML (Δ+0.019) baten a L3 con IC95%
  que excluye 0 — pero el **límite inferior roza 0** (+0.001/+0.002): señal real, modesta y frágil.

## (d) Recomendación honesta
- **1X2 y BTTS: confirmar TECHO.** Mantener L3. Ningún modelo lo bate; en 1X2 son claramente peores y en
  BTTS el total matchup ya cerró la brecha. No adoptar DC/ML aquí.
- **Over 2.5: SEGUIR EXPLORANDO, no adoptar aún.** DC/ML tienen una ventaja pequeña y significativa pero
  frágil (IC casi toca 0) sobre un producto en sombra. Camino razonable: explorar un **refinamiento de la
  línea de goles/OU basado en Dixon-Coles** (ataque/defensa asimétricos) **solo para el mercado de totales**,
  manteniendo L3 para 1X2 — sin tocar el 1X2 que L3 domina. Antes de adoptar: re-test con más OOS (2025-2026),
  varias semillas de bootstrap y coste de complejidad (DC añade refit por bloque).
- **Lectura de fondo:** L3 es la mejor para el RESULTADO; los modelos de goles (DC, GBM) solo arañan en
  TOTALES, y el total matchup ya recuperó casi toda esa ventaja. Coherente con la teoría (margin gana 1X2,
  ataque/defensa gana goles). **Sin cambios en producción.** Análisis versionado (script + report + metrics + rows).
