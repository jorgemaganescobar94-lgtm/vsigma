# RE-TEST Dixon-Coles · mercados de GOLES · muestra ampliada (WC liquidado). CONCLUSIÓN

**Read-only · sin API · sin cambios en producción.** Script: `dc_goals_retest_backtest.py`
(reutiliza VERBATIM el harness del bake-off `model_bakeoff_backtest.py`: fit DC, τ, Poisson, receta
isotónica, bloques walk-forward). Solo se cambia: (a) OOS extendido a 2026 (incluye WC liquidado),
(b) se añade el mercado de **marcadores**, (c) bootstrap **multi-semilla** (10 semillas), (d) slices
temporales para aislar la aportación WC.

## Montaje (anti-leakage estricto, idéntico para ambos)
- **Burn-in** `[2019-01-01, 2024-01-01)` — SOLO aquí se ajustan la isotónica (O2.5/BTTS) y los coefs de
  L3 (margin lstsq + total MATCHUP `tb0+tb1|sup|+tb2·sup²`, tope `TOTAL_CAP`, el motor de producción).
- **OOS extendido** `[2024-01-01, 2027-01-01)` — evaluación. DC se re-ajusta walk-forward cada 60d
  (ventana 6a, HL=730d) usando SOLO datos previos a cada bloque → λ asimétricas → matriz τ-corregida.
- **Marcadores:** NLL por partido del marcador REAL bajo la matriz completa de cada modelo (sin isotónica
  por celda — imposible en un conjunto; trato idéntico para ambos → justo; es EXACTAMENTE donde actúa la
  corrección τ de DC).
- **Slices:** `HIST_2024_2025` (reproduce el bake-off), `2026_ALL` (486, único dato nuevo real),
  `WC2026_ONLY` (16, se omite por n<30), `ALL_EXPANDED` (2846 = primario).
- **Honestidad de alcance:** de los partidos 2026 con `sup_pre_l3` leak-free, **solo 16 son WC**. La
  aportación WC al OOS es **marginal** (16 de 2846). El grueso de "2026" son amistosos/AFCON/clasis.
- **1X2 fuera de alcance** (DC no lo mejora, ya probado en el bake-off; L3 es el techo del resultado).

## Gate de adopción (estricto, por lo frágil que fue)
Δlogloss = L3 − DC (>0 ⇒ DC mejor). **ADOPTAR** solo si: media>0 **Y** todas las 10 semillas dan lo>0
**Y** `min_lo ≥ +0.005` (margen cómodo = 5× el frágil previo +0.001 y ~¼ del efecto). Un lo meramente
positivo (p.ej. +0.003) **NO** cruza: eso es "rozar 0", no excluirlo con claridad.

## Tabla primaria — OOS_ALL_EXPANDED (n=2846, incl. WC liquidado)
| mercado | L3 logloss | DC logloss | Δlogloss (L3−DC) | IC95 (min..max entre 10 semillas) | p | ¿robusto entre semillas? | veredicto |
|---|---|---|---|---|---|---|---|
| **Over 2.5** | 0.70491 | **0.68298** | **+0.02194** | **[+0.00298 .. +0.04483]** | 0.992 | Sí (signo estable) | **FRÁGIL — lo roza 0 (+0.003 < +0.005) → NO adoptar** |
| **BTTS** | **0.68611** | 0.68409 | +0.00201 | [−0.00748 .. +0.01461] | 0.605 | No (IC incluye 0) | **NO adoptar (IC incluye 0)** |
| **Marcador** | **2.88803** | 3.51363 | **−0.62559** | [−0.76633 .. −0.49164] | 0.000 | Sí (IC excluye 0 por DEBAJO) | **L3 TECHO — DC claramente PEOR** |

### Corte histórico (reproduce el bake-off) y corte 2026 (único dato nuevo)
| mercado | slice | Δlogloss (L3−DC) | IC95 (min..max) | veredicto |
|---|---|---|---|---|
| Over 2.5 | HIST 2024-25 (2360) | +0.02085 | [+0.00090 .. +0.04594] | frágil (lo roza 0, igual que antes) |
| Over 2.5 | **2026 solo (486)** | +0.02723 | **[−0.00984 .. +0.09098]** | **NO significativo (IC incluye 0)** |
| BTTS | 2026 solo | −0.00202 | [−0.01910 .. +0.01492] | sin señal |
| Marcador | 2026 solo | −1.81670 | [−2.37406 .. −1.29876] | DC MUY peor (λ ruidosas en equipos WC/2026) |

## Veredicto honesto — ¿DC ya cruza el umbral con claridad, o sigue frágil?
**Sigue FRÁGIL. Se cierra el tema DC para los mercados de goles. Nada que adoptar.**

1. **Over 2.5 — la señal es REAL y robusta entre semillas, pero NO cruza el gate estricto.** La muestra
   ampliada movió el límite inferior del IC de **+0.001 → +0.003**: se despegó de 0 apenas, y solo porque
   creció n. **El único dato genuinamente nuevo (2026) NO confirma por sí solo** — su IC incluye 0
   ([−0.010, +0.091]). Es exactamente el caso "rozando 0" que el gate fue diseñado para rechazar. La
   mejora es pequeña (+0.02 logloss) y no justifica la complejidad de DC (refit por bloque) en producción.
2. **BTTS — sin señal.** IC incluye 0 en todos los cortes. Confirma el bake-off: el total-matchup de L3
   ya cerró la brecha.
3. **Marcadores — DC es CLARAMENTE PEOR** (robusto, p=0.000, IC excluye 0 por debajo). La τ de DC casi no
   actúa (ρ mediana ≈ 0) y sus λ individuales dan peor verosimilitud del marcador exacto que el total
   MATCHUP de L3; en 2026 el deterioro es grande (3.5–4.8 vs ~2.9), señal de ratings DC ruidosos en
   equipos con pocos datos. La corrección de marcadores bajos de DC **no aporta** aquí.

**Fondo:** coherente con el bake-off previo y con la teoría. El total-matchup de L3 ya captura casi toda
la ventaja de goles; DC solo araña en Over2.5 con una señal fina que la muestra ampliada **no** convirtió
en decisiva, y es peor en el joint de marcadores. **Recomendación: mantener L3, cerrar DC.** Reabrir solo
si en el futuro se acumula un OOS genuinamente nuevo (no histórico) mucho mayor. **Sin cambios en
producción.** Artefactos: `dc_goals_retest_backtest.py` + `_report.txt` + `_metrics.csv` + este md.
