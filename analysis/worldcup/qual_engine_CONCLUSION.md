# Motor de clasificación (qual_engine) — reconstrucción honesta · FASE 1 (READ-ONLY)

**Fecha:** 2026-06-26 · **Estado:** motor + validación + tests. **NO aplicado a producción** (la ficha sigue
usando el shim legacy; la aplicación va en FASE 2 tras visto bueno de Jorge).

## Qué estaba mal (bugs reales)
El motor colapsaba cada equipo a UNA etiqueta y ocultaba la condicionalidad:
- **Arabia Saudí** salía *"vivo como mejor tercero"* cuando en realidad **puede pasar 2ª DIRECTA** (gana y
  Uruguay no gana).
- **Cabo Verde** salía *"debe ganar"* cuando **le vale el empate si España gana** (Uruguay pierde).
- **Equipos de 4 pts** (España, Japón, Países Bajos, Egipto, Portugal, Ghana, Inglaterra) salían
  *"ya clasificado"* sin tener el top-2 garantizado: si pierden y se alinea el paralelo, caen a 3º.

Causa raíz: el motor trataba *"vivo como mejor tercero"* (un MAYBE con corte cross-group desconocido) y los
empates a puntos en la frontera (que decide la diferencia de goles) como **clasificación segura (YES)**.

## El motor correcto
`analyze_team(table, match, team, all_tables, n_groups)` enumera las **9 ramas** (propio W/D/L × paralelo
W/D/L), calcula los puntos finales de los 4 y aplica el orden FIFA. Regla de honestidad:

- **YES (seguro)** = top-2 **por PUNTOS** (independiente de la diferencia de goles).
- **MAYBE (depende)** = empate a puntos en la frontera (lo decide la diferencia de goles) **o** plaza de
  mejor tercero (corte cross-group). Nunca se afirma como seguro, pero **nunca oculta una vía clara**.
- **NO** = fuera.

Por cada resultado propio resume un *verdict* (`secures` / `secures_if` / `alive_if` / `dead`) y la
**condición del partido paralelo**. `phrase_es()` produce la frase honesta y condicional; `short_tag()` da
una categoría gruesa. **Mejores terceros:** cota conservadora documentada (`alive_as_third`) — un 3º con
`q` puntos sigue vivo salvo que ≥`n_thirds` grupos garanticen ya un 3º mejor (≥3 equipos por encima de `q`).
Nunca elimina en falso: *"eliminado"* solo si NINGUNA rama clasifica; *"debe ganar"* solo si únicamente
ganar puede clasificar (ni empate ni derrota, en ninguna rama).

## Validación (Grupo H — los casos exigidos)
| Equipo | Etiqueta honesta |
|---|---|
| **Arabia Saudí** | gana y pasa 2ª **si Uruguay no gana** (si Uruguay gana, 2ª por diferencia de goles); con empate solo sigue vivo como mejor tercero si España gana |
| **Cabo Verde** | **le vale el empate si España gana** (en otro caso, 2ª por diferencia de goles o mejor tercero); gana y pasa 2ª |
| **Uruguay** | **gana y pasa 2ª**; con empate/derrota solo sigue vivo como mejor tercero |
| **España** | **le vale el empate** (NO "ya clasificado"); perdiendo aún pasa si Cabo Verde y Arabia empatan, en otro caso depende de diferencia de goles / mejor tercero |

Tabla completa de los 12 grupos: `qual_engine_audit_report.txt` (auditada a mano, grupo por grupo).

## Entregables (todo en `analysis/worldcup/`, READ-ONLY, sin endpoints de apuesta)
- `qual_engine.py` — motor honesto nuevo + shim legacy intacto (la ficha en vivo no cambia).
- `qual_engine_audit.py` + `qual_engine_audit_report.txt` — corre el motor sobre TODOS los grupos con
  standings reales (cache) y emparejamientos reales de última jornada (cache sqlite, solo lectura).
- `test_qual_engine_honest.py` — 16 tests (una por categoría + 4 casos reales + cotas). 16/16 OK.
- La suite legacy `test_qual_engine.py` sigue pasando 15/15 (la ficha no se tocó).

## FASE 2 (pendiente de aprobación)
Sustituir `compute_group_info` (y, si procede, la pata de predicción) por `analyze_team`/`phrase_es`,
retirando el shim legacy `classify_team`/`LABEL_ES`.
