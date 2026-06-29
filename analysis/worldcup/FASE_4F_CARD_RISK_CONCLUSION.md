# Fase 4F — Perfiles auto de tarjetas + ajuste de riesgo (predicción futbolística pura)

**Fecha:** 2026-06-29 · **Estado:** completada · **Aislamiento:** producto Mundial (`analysis/worldcup/`).

Sin apuestas, sin cuotas, sin mercados, sin picks, sin edge, sin ROI, sin stakes, sin ejecución.
Sin scraping, sin fuentes externas, sin xG/xA, sin clima real. NO toca `data/external`.

## Qué hace

Deriva, **solo con datos reales ya capturados por el producto Mundial**, perfiles de disciplina
(tarjetas) por jugador, equipo y posición, y los combina de forma **conservadora** con el contexto de
árbitro para ajustar la probabilidad de tarjeta por jugador.

### 1. `build_worldcup_card_profiles_auto.py`
Lee (read-only):
- `analysis/worldcup/worldcup_fixture_events.csv` (tarjetas reales por fixture/equipo/jugador, Fase 2)
- `data/external/player_positional_profiles.csv` (mapeo `player_id → posición` GK/DEF/MID/FWD)
- `data/external/fixture_referees.csv` y `worldcup_referee_profiles_auto.csv` (solo nota de disponibilidad)

Genera (artefactos del Mundial; NO `data/external`):
- `worldcup_card_profiles_auto.csv` (tabla de jugadores) — **auto-commiteado en CI**
- `worldcup_card_profiles_auto.json` (`{meta, players, teams, positions}`) — gitignored (regenerable)
- `worldcup_card_profiles_auto_report.txt` — gitignored

**Métricas por jugador:** `matches_sample`, tarjetas (amarillas/rojas/2ª amarilla/total), `*_pg`,
`card_risk_player_history` (bajo/medio/alto/no determinado), `data_quality`, `confidence`, `reason`,
`source=worldcup_events_auto`.
**Por equipo:** `cards_for_pg`, `cards_against_pg` (derivado de `team_id` vs `opponent_id`),
`card_environment_team`.
**Por posición:** `cards_pg` por fixture observado y `card_risk_position` **relativo** a la media de
posiciones con muestra usable.

Reglas de honestidad: muestra de 1 partido → `confidence=baja` y label de jugador limitado a `medio`
(1 tarjeta no es tendencia); jugador con muestra **sin** tarjetas → `bajo` con confianza baja y aviso
"no asumir riesgo cero" (nunca cero duro); posición con < 4 tarjetas → `no determinado`.

### 2. `card_risk_adjuster.py` (función pura)
Combina, con pasos pequeños ponderados por confianza:
- historial del jugador (paso 0.10), posición (0.05), equipo (0.05), árbitro (0.06).
- El árbitro con muestra ≤ 1 partido se **infrapondera ×0.25** (no subir por 1 partido).
- Factor total acotado a **[0.75, 1.30]**; probabilidad nunca a 0 por ausencia de tarjetas.
- Fuentes en conflicto → se **netean** (conservador). Señal insuficiente → `neutro` y se mantiene el original.

Devuelve por jugador: `probability_card_original`, `probability_card_adjusted`,
`adjustment_direction` (subir/bajar/neutro), `adjustment_reason`, `card_risk_components`
(player_history/position_profile/team_profile/referee_profile), `confidence`, `data_quality`.

### 3. Integración
- `build_worldcup_player_events.py` carga los perfiles una vez y aplica el ajuste al bloque `card_risk`;
  el JSON por jugador incluye original + ajustado + dirección + motivo + componentes.
- `build_worldcup_player_events_telegram.py` muestra el % ajustado, el `Motivo:` y un aviso de muestra
  baja. Sin lenguaje de apuestas (verificado en build).
- `player_events_core.card_risk` ahora expone `player_id` (para enlazar perfiles).

## Cómo se ajusta `probability_card` (ejemplos reales)
| Caso | original → ajustado | dirección |
|---|---|---|
| historial alto + árbitro alto pero 1 partido | 0.20 → 0.2075 | subir (mínimo, árbitro infraponderado) |
| jugador + posición + equipo altos, árbitro medio | 0.20 → 0.219 | subir (moderado, dentro del tope) |
| sin datos de disciplina | 0.20 → 0.20 | neutro (mantiene original) |
| muestra sin tarjetas (historial bajo) | 0.20 → 0.193 | bajar (nunca a cero) |
| historial alto + equipo bajo (conflicto) | 0.20 → 0.206 | subir (neteado, conservador) |

## Tests
`analysis/worldcup/test_worldcup_card_profiles_auto.py` (18 tests). Suite completa
`pytest analysis/players analysis/worldcup` → **484 passed**.

## Qué queda para Fase 4G
- Activar split izquierda/derecha y posición fina cuando exista en datos reales.
- Calibración out-of-sample de los umbrales (alto/medio/bajo) según se acumulan más fixtures.
- Considerar enlazar `card_environment` de árbitro por entorno total (for+against) además del propio del equipo.
- Posible promoción a `data/external` solo tras gobernanza (hoy se mantiene aislado).
