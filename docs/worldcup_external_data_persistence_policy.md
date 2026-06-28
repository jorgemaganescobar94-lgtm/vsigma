# Política de persistencia de `data/external/` en CI — producto Mundial (Fase 4C-2)

> Estado: **DECISIÓN PENDIENTE de Jorge.** Hoy CI **no** hace `git add` de `data/external/`.
> Este documento describe las opciones; la persistencia automática **no está activada**.

## Contexto

`analysis/worldcup/prepare_worldcup_external_templates.py` mantiene los contratos CSV de
`data/external/` con un *merge incremental seguro* (Fase 4B): añade filas reales nuevas, completa
celdas vacías y refresca hechos auto-derivados, **sin pisar nunca una edición manual ni borrar filas**.

En CI (`vsigma_worldcup_cards.yml`) el paso de `prepare` corre tras la enrichment y **regenera estos
CSV en el runner**, pero el workflow **no los commitea**. Por tanto, hoy:

- los datos auto-derivados (penaltis reales, posición, referee/venue cuando existan) se calculan en
  cada run y alimentan la ficha, **pero no se persisten** entre runs;
- las ediciones manuales que Jorge haga **viven solo en su repo local** hasta que él las commitee.

La auditoría (`audit_worldcup_store_external_context.py`) reporta la cobertura real del store y de los
CSV para decidir con datos, no a ciegas.

## Opciones

### A) No persistir `data/external/` desde CI  *(estado actual)*
- ✅ Más seguro: CI nunca puede pisar una edición manual ni introducir ruido en git.
- ✅ Aislamiento total del producto Mundial.
- ❌ Cada run recalcula desde cero lo auto-derivable; nada se acumula en el repo vía CI.
- ❌ Si una fuente real aparece y desaparece del store (cache TTL), la fila derivada no queda guardada.

### B) Persistir SOLO lo auto-derivado seguro  *(recomendada — aún NO activada)*
Commit automático y acotado, con `git add` de **rutas explícitas** (nunca `git add .`), solo de los
CSV cuyo contenido es 100 % auto-derivado de datos reales del repo:

- `fixture_referees.csv` — `fixture_id, referee_name` desde el store.
- `weather_by_fixture.csv` — **solo** `fixture_id`, `kickoff_time` y `venue`; **nunca** se commitean
  mediciones de clima (esas son manuales/externas).
- `set_piece_takers.csv` — **solo** filas de rol `penalty` derivadas de eventos reales.
- `player_positional_profiles.csv` — **solo** la `position` real (los campos de scouting siguen vacíos).

Y **nunca** se commitean automáticamente los ficheros de relleno manual:
- `player_xg_xa.csv`, `coach_tactical_profiles.csv`, `referee_profiles.csv`.

Salvaguardas obligatorias antes de activar B:
1. El merge ya garantiza no-sobrescritura de filas/celdas manuales (probado en tests Fase 4B).
2. CI debe commitear con `git add <ruta-explícita>` por archivo, **jamás** `git add data/external`.
3. Idealmente, ejecutar `--dry-run` y solo commitear si hay cambios reales (evita commits vacíos).
4. Para `set_piece_takers.csv` / `player_positional_profiles.csv`, plantearse un *guard*: no commitear
   si el archivo contiene alguna fila con `source` no-auto (= contiene edición manual), para 0 riesgo.
- ✅ Acumula datos reales en el repo sin intervención.
- ✅ Riesgo de pisar manual ≈ 0 gracias al merge + guards.
- ❌ Más complejidad en el workflow; commits automáticos de datos en `main`.

### C) Persistir TODO `data/external/`  *(NO recomendada)*
- ❌ Riesgo real de pisar/condicionar datos manuales (xG/xA, árbitros, táctica).
- ❌ Mezcla datos auto y manuales en commits de CI sin separación clara.
- ❌ Contradice la regla de "no inventar / manual es sagrado".

## Recomendación

**Opción B**, con las cuatro salvaguardas, **pero no se activa hasta que Jorge lo apruebe
explícitamente** (es un cambio de comportamiento de CI → nivel 🔴 por tocar persistencia en `main`).
Mientras tanto se mantiene la **opción A** (estado actual): CI solo **audita** y hace **dry-run**, sin
commitear nada de `data/external/`.

## Próximo paso (Fase 4C-3, sujeto a aprobación)

Si Jorge aprueba B: añadir al workflow un paso de commit acotado con rutas explícitas + guard
anti-manual + dry-run previo, y documentar el trail. Hasta entonces, **no activar persistencia**.
