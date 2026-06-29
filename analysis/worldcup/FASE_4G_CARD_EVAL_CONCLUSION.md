# Fase 4G — Evaluación/calibración del ajuste de riesgo de tarjeta (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada (medición; **pesos NO modificados**) · **Aislamiento:** producto Mundial.

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA, sin clima real. NO toca `data/external`.

## Qué hace

`analysis/worldcup/evaluate_worldcup_card_risk_adjustment.py` compara `probability_card_original` vs
`probability_card_adjusted` (Fase 4F) contra eventos reales de tarjeta del Mundial, **sin tocar pesos**.

- **Conjunto etiquetado:** filas `settled==1` de `worldcup_player_props_log.csv` → `p_card` (original,
  congelado a KO) + `act_card` (tarjeta real 0/1). Denominador completo (todos los jugadores predichos).
- **Adjusted reconstruido:** se aplica `card_risk_adjuster` a esa `p_card` con los perfiles auto
  actuales + contexto de árbitro — **mismo transform que el producto** (`apply_card_adjustment`).
- El `worldcup_player_events.json` solo tiene fixtures **próximos** (sin resultado); se lee para nota de
  consistencia, no para métricas.

**Advertencia metodológica (en el reporte):** los perfiles auto son **acumulativos** (incluyen el propio
partido evaluado) → el adjusted tiene un ligero **look-ahead**; las mejoras son indicativas, no veredicto.

## Resultado (run local, dato real committeado)

- **n evaluadas:** 418 · **eventos de tarjeta reales:** 39 · **tasa real:** 9.3% · `p_card` media 16.4%
  (el modelo sobre-predice tarjetas).
- **Brier:** 0.09307 → **0.09200** (Δ **−0.00107**, mejora).
- **LogLoss:** 0.33359 → **0.32977** (Δ **−0.00382**, mejora).
- Ajuste medio |Δ| = 0.004 (muy conservador). Direcciones: 258 neutro / 91 bajar / 69 subir.
- Sobre-ajuste: 145/359 filas movidas empeoran (40%) → 60% mejoran (neto positivo).

### Dónde mejora
- **Dirección correcta (señal fuerte):** los `subir` (n=69) tienen tasa real **26%** y mejoran Brier;
  los `bajar` (n=91) tienen tasa real **1.1%** y mejoran Brier. El ajuste empuja en la dirección real.
- **Por posición:** mejora en DEF, MID y sobre todo **FWD** (tasa real 4%, el ajuste la baja).
- **Por equipo:** mayoría de equipos con ΔBrier negativo.

### Dónde empeora / no aporta
- Unos pocos equipos con n=11 tienen ΔBrier ligeramente positivo (ruido de muestra pequeña).
- **Factor árbitro INACTIVO:** aún no hay perfiles de árbitro poblados
  (`worldcup_referee_profiles_auto` vacío) → su contribución al ajuste es ~0 (no es fallo, es muestra).

## Recomendación (conservadora)
- **Pesos: MANTENER.** El ajuste mejora ambas métricas, es conservador y direccionalmente correcto.
- **No subir agresividad:** con 39 positivos y perfiles acumulativos (look-ahead) la mejora es marginal
  y no concluyente. No declarar victoria.
- **Factor posición / equipo:** adecuados, mantener.
- **Factor árbitro:** inactivo; reevaluar cuando haya perfiles de árbitro con muestra.

## Artefactos
- `worldcup_card_risk_evaluation.csv` (una fila por predicción evaluada) — **auto-commiteado en CI**.
- `worldcup_card_risk_evaluation_summary.json` + `_report.txt` — gitignored (regenerables).

## Tests
`analysis/worldcup/test_worldcup_card_risk_evaluation.py` (15 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **507 passed**.

## Qué queda para Fase 4H
- Acumular más fixtures/positivos para una conclusión robusta (evitar look-ahead con perfiles
  congelados pre-fixture / leave-one-out).
- Reactivar y reevaluar el factor árbitro cuando haya perfiles de árbitro con muestra.
- Solo entonces considerar recalibrar pesos del `card_risk_adjuster` (con justificación medida).
