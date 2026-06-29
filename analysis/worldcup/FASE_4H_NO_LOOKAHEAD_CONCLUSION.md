# Fase 4H — Evaluación anti-look-ahead del ajuste de riesgo de tarjeta (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada (medición; **pesos NO modificados**) · **Aislamiento:** producto Mundial.

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA, sin clima real. NO toca `data/external`.

## Qué hace

`analysis/worldcup/evaluate_worldcup_card_risk_adjustment_no_lookahead.py` re-evalúa el ajuste de
Fase 4F/4G pero **reconstruyendo los perfiles auto sin información futura**, para comprobar si la mejora
marginal de 4G sobrevive al quitar la contaminación temporal (perfiles acumulativos).

Tres modos, mismo adjuster/lookup, difieren solo en qué eventos alimentan los perfiles por fixture:
- **cumulative** — todos los eventos (= régimen 4G; con look-ahead). Baseline.
- **pre_fixture** — solo eventos de **jornadas estrictamente anteriores** (`date < fecha del fixture`).
  Estimación limpia anti-look-ahead.
- **leave_one_fixture_out** — todos los eventos menos los del propio fixture (usa fixtures posteriores →
  menos estricto; diagnóstico auxiliar).

Conjunto etiquetado = filas `settled` de `worldcup_player_props_log.csv` (`p_card` congelado + `act_card`).
Perfiles reconstruidos por cutoff con la **misma derivación** que Fase 4F (sin fuentes nuevas, sin scraping).

## Resultado (run local, dato real committeado)

| Modo | n | pos | Brier orig→adj (Δ) | LogLoss orig→adj (Δ) |
|---|---|---|---|---|
| cumulative (4G) | 418 | 39 | 0.09307 → 0.09177 (**−0.0013**) | 0.33359 → 0.32903 (**−0.00456**) |
| **pre_fixture** | 418 | 39 | 0.09307 → 0.09297 (**−0.0001**) | 0.33359 → 0.33315 (**−0.00044**) |
| leave_one_out | 418 | 39 | 0.09307 → 0.09297 (**−0.0001**) | 0.33359 → 0.33315 (**−0.00044**) |

- **Solo ~8% de la ganancia de 4G sobrevive sin look-ahead** (`fraction_of_4g_gain_surviving ≈ 0.077`).
  El ~92% restante era contaminación temporal (perfiles acumulativos que incluían el propio partido).
- `|ΔBrier|` pre_fixture = 0.0001 (< 0.0005 ≈ 0.5% relativo) → **indistinguible de ruido**.
- Dirección: aún débilmente correcta (pre_fixture `subir` real 12.3% vs `bajar` 3.8% vs `neutro` 9.8%),
  pero mucho más débil que el 26%/1.1% inflado de 4G.
- **`leave_one_out ≈ pre_fixture`**: los fixtures evaluados (R32, 06-25→06-28) son los **más recientes**
  del dataset; cada equipo juega una vez por ronda, así que apenas hay eventos posteriores → excluir-uno
  coincide casi con solo-previos. (No es bug; es la estructura temporal del dato.)
- 56% de las filas tienen perfil de jugador (el resto se ajusta solo por posición/equipo/árbitro).

## Conclusión y recomendación (conservadora)

- **La mejora de Fase 4G se DESVANECE sin look-ahead** (magnitud negligible). No se declara mejora real.
- **Pesos: NO tocar.** Recomendación: **congelar el ajuste como SHADOW y tratarlo como neutral**; no
  subir pesos. El ajuste no daña (sigue ligeramente negativo y direccionalmente correcto) pero tampoco
  aporta señal medible una vez quitado el look-ahead, con esta muestra (39 positivos, 19 fixtures).
- No bajar pesos: el ajuste es conservador y no empeora; mantenerlo como shadow hasta acumular muestra.

## Artefactos
- `worldcup_card_risk_no_lookahead_evaluation.csv` (una fila por predicción; original + pre + loo) —
  **auto-commiteado en CI**.
- `worldcup_card_risk_no_lookahead_summary.json` + `_report.txt` — gitignored (regenerables).

## Tests
`analysis/worldcup/test_worldcup_card_risk_no_lookahead.py` (11 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **518 passed**.

## Qué queda para Fase 4I
- Reevaluar cuando haya **más rondas/positivos** (la muestra anti-look-ahead crecerá según avance el torneo).
- Si con más muestra la mejora pre_fixture se vuelve material y estable → considerar mantener/recalibrar.
- Si sigue negligible → decidir si retirar el ajuste o dejarlo como shadow permanente.
- El factor árbitro: con perfiles mayormente de 1 partido aporta ~0; reevaluar al acumular muestra.
