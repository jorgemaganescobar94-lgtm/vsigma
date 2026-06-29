# Fase 4I — Card-risk shadow monitor (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada (monitor; **pesos NO modificados**) · **Aislamiento:** producto Mundial.

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA, sin clima real. NO toca `data/external`.

## Qué hace

`analysis/worldcup/monitor_worldcup_card_risk_shadow.py` convierte el ajuste de riesgo de tarjeta
(Fase 4F) en un **shadow monitor estable**: cada ejecución re-lee las evaluaciones 4G (acumulativa) y 4H
(anti-look-ahead), clasifica el ajuste en un estado, y **persiste una serie temporal de una fila por día**
para vigilar — automáticamente — si el ajuste empieza a aportar señal real cuando haya más partidos y
más positivos. **No toca pesos** y **no promueve** el ajuste.

### Estados (spec §3)
- **INSUFFICIENT_SAMPLE** — positivos < 30 o n < 100.
- **SHADOW_NEUTRAL** — mejora pre_fixture negligible / desaparece / positivos < 75 (estado por defecto).
- **KEEP_WEAK** — pre_fixture mejora Brier+LogLoss, positivos ≥ 75, no negligible, sin segmento peligroso.
- **CONSIDER_RECALIBRATION** — pre_fixture mejora material, positivos ≥ 100, separación subir/bajar clara,
  fracción superviviente ≥ 0.50. (Aun así NO recalibra solo: abre revisión manual.)
- **REDUCE_OR_DISABLE** — pre_fixture empeora ambas, o dirección contraria (subir recibe menos tarjetas
  que bajar).

### Gate de seguridad (spec §4)
`should_adjust_weights(summary) -> bool` devuelve **True solo** si: positivos ≥ 100 **y** pre_fixture
mejora Brier **y** LogLoss **y** ambos materiales **y** separación de dirección estable **y**
`fraction_of_4g_gain_surviving ≥ 0.50`. En cualquier otro caso (y hoy) → **False**.

## Estado actual (dato real)

- **Estado: `SHADOW_NEUTRAL`**.
- **`should_adjust_weights`: `False`**.
- **Motivo:** la mejora pre_fixture es negligible (|ΔBrier|=0.0001, indistinguible de ruido); solo 39
  positivos; sobrevive ≈8% (0.077) de la ganancia acumulada de 4G.
- **Acción:** mantener pesos, no recalibrar (seguir midiendo en shadow).
- Métricas: n=418, positivos=39, tasa real 9.3%; Brier orig 0.09307 → pre_fixture 0.09297 (Δ −0.0001);
  LogLoss orig 0.33359 → pre_fixture 0.33315 (Δ −0.00044); dirección pre_fixture subir 12.3% / bajar 3.8%.

## Reporte interno (no toca el Telegram principal)
```
🟨 Card Risk Shadow Monitor
Estado: SHADOW_NEUTRAL
Motivo: mejora pre_fixture negligible; 39 positivos; ~8% de ganancia acumulada sobrevive.
Acción: mantener pesos, no recalibrar.
```

## Artefactos
- `worldcup_card_risk_shadow_monitor.csv` — serie temporal (una fila por día UTC) — **auto-commiteado en CI**.
- `worldcup_card_risk_shadow_monitor.json` + `_report.txt` — gitignored (regenerables).

## Tests
`analysis/worldcup/test_worldcup_card_risk_shadow_monitor.py` (13 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **532 passed**.

## Qué queda para Fase 4J
- Dejar correr el monitor en CI durante el resto del torneo; el estado migrará solo si la señal aparece.
- Cuando `should_adjust_weights` llegue a True (positivos ≥ 100 + mejora material y superviviente), abrir
  una **revisión manual** de pesos del `card_risk_adjuster` (gate humano; nunca automático).
- Posible alerta interna (no Telegram principal) cuando el estado cambie de SHADOW_NEUTRAL.
