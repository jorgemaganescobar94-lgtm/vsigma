# Backtest de la heurística de CONTEXTO de clasificación (worldcup_context_shadow)

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API
**Script:** `analysis/worldcup/context_shadow_backtest.py`
**Salidas:** `..._report.txt`, `..._rows.csv`, `..._metrics.csv`

## Qué se midió
Backtest histórico de la heurística que ajusta el xG L3 por el ESCENARIO de grupo (ya clasificado,
eliminado, debe ganar, le vale empate, intrascendente) sobre la **última jornada de fase de grupos**
de torneos finales de **SELECCIONES NACIONALES** pasados. Se reutiliza la lógica del módulo
(`classify_fixture` + `MULT` + `context_predict`), sin duplicarla. Se mide **context-adjusted vs L3
puro** solo en escenarios NO triviales (donde el multiplicador cambia la predicción).

## (a) Muestra — 0 clubes confirmado
- **Filas de clubes en el dataset: 0.** `international_results.csv` es de selecciones; todos los
  `league_tag` son competiciones de selección.
- **17 torneos-temporada INCLUIDOS** (reconstrucción K4 limpia, grupos de 4 de liga simple):
  WC 2018/2022, Euro 2024, AFCON 2021/2023/2025, AsianCup 2019/2023, CopaAmerica 2019/2024,
  GoldCup 2019/2021/2023/2025, GulfCup 2019/2023/2024.
- **6 EXCLUIDOS automáticamente** (no reconstruyen K4 limpio / formato no liga-simple / datos
  polucionados): AFCON 2019 (198 partidos — tag contaminado), Euro 2020 (313 — incluye clasif.),
  ArabCup 2021/2025, CopaAmerica 2021 (grupos de 5), WC 2026 (torneo en curso, incompleto).
- **162 partidos** de última jornada con rating L3 walk-forward disponible; **todos no triviales.**

**Distribución por escenario** (sobre ambos equipos, 324 etiquetas):
`le_vale_empate` 112 · `tercero_en_disputa` 81 (neutral, ×1.0) · `debe_ganar` 41 · `eliminado` 40 ·
`ya_clasificado` 28 · `intrascendente` 22.

## (b) Métricas context vs L3 puro (1X2, solo no triviales)

| Corte | n | Δlogloss | Δbrier | ¿ctx bate? |
|---|---|---|---|---|
| **GLOBAL** | 162 | **+0.0055** | **+0.0032** | sí (nominal) |
| ya_clasificado (×0.92) | 28 | +0.0120 | +0.0071 | sí |
| eliminado (×0.95) | 40 | +0.0054 | +0.0035 | sí |
| debe_ganar (×1.08) | 41 | **+0.0178** | +0.0126 | sí (más fuerte) |
| le_vale_empate (×0.97) | 101 | +0.0062 | +0.0029 | sí |
| **intrascendente (×0.90)** | 11 | **−0.0245** | **−0.0128** | **no (empeora)** |

(Δ = L3 − ctx; positivo = ctx mejora.) Over 2.5: ctx también mejora (logloss 0.6932→0.6863).

**Significancia (bootstrap pareado por partido, 20000 resamples, semilla fija):**
- Δlogloss media **+0.0055** (0.52% del L3); ctx mejor en **solo 45% de los partidos** (el agregado
  lo arrastran pocos partidos donde ayuda mucho).
- **IC95% Δlogloss = [−0.0036, +0.0148] → INCLUYE 0 (NO significativo).** P(Δ>0)=88%.
- IC95% Δbrier = [−0.0025, +0.0089] → INCLUYE 0. P(Δ>0)=86%.

## (c) ¿Mejora, empeora o es indistinguible?
**Direccionalmente MEJORA, pero dentro del ruido.** El ajuste bate al L3 en logloss y brier de forma
agregada (cumple el criterio nominal del módulo: bate ambos con N≥20), y mejora en 4 de 5 escenarios
con signo consistente — pero el **IC95% incluye 0**: a 95% de confianza no se distingue del ruido
(confianza one-sided 88%). La mejora relativa es minúscula (0.52%) y solo el 45% de partidos mejoran.

## (d) Recomendación honesta
- **SEGUIR EN SOMBRA (no graduar a vivo todavía).** El veredicto es **ambiguo, no claro**: el signo
  es favorable y consistente, pero no supera el ruido. Graduar exigiría una señal robusta; esta no lo
  es aún. El scorecard en vivo del módulo debe seguir acumulando partidos de Mundial.
- **`debe_ganar` (×1.08) es el multiplicador más prometedor** (Δll +0.0178, mejor en 54% de partidos):
  la hipótesis "el que debe ganar ataca más" es la que mejor aguanta. Candidato a graduar primero si
  se aísla, pero aún con N pequeño.
- **`intrascendente` (×0.90) es el ÚNICO que EMPEORA** de forma consistente (Δll −0.0245, mejor en
  solo 18% de 11 partidos). Es el candidato a **RETIRAR o poner a 1.0** (revisar): bajar el xG de
  ambos equipos en partidos "de facto amistoso" no se sostiene en estos datos. Muestra pequeña (n=11),
  así que: marcar para vigilancia y, si persiste, retirar — NO aplicar nada automáticamente.
- Ningún cambio en producción aquí: los multiplicadores son hipótesis; el scorecard es el juez.

## Anti-leakage (confirmado)
- **Standings pre-partido** reconstruidos SOLO desde jornadas previas del mismo grupo (fecha
  estrictamente anterior); nunca de la jornada predicha. Sin API.
- **Ratings L3 walk-forward**: `fit_rating` sobre partidos internacionales con `date < fecha_partido`
  (mismos pesos: importancia por tag, cross-conf, decaimiento HL=730d). Ningún partido futuro entra.
- **Calibración congelada** (`national_elo_layer3_calibration.json`: a0/a1/total_mean/iso) como
  transformación fija — la "calibración congelada" pedida; lenta y no discriminativa. Documentado.
- **Target** = resultado 90' (1X2 / Over2.5) solo para puntuar, nunca como feature.

## Limitaciones (honestas)
- `classify_fixture` se usa TAL CUAL, incluida su regla WC-2026 de mejores terceros
  (rank==3 → `tercero_en_disputa`, neutral). En torneos de solo-top-2 (WC 2018/2022) esto etiqueta
  como trivial a algunos terceros genuinamente "a vida o muerte" → quedan fuera del set graduado
  (reduce N, no corrompe las filas incluidas).
- Se omite ventaja de campo (el módulo asume neutral); algún anfitrión de fase de grupos no era neutral.
- N por escenario pequeño (11–101); los veredictos por escenario son orientativos.
- Formatos de doble vuelta (Nations League, clasificatorios) quedan fuera: `classify_fixture` asume
  liga simple (per_team=G−1) y los mal-clasificaría.
