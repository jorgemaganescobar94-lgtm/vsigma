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

## Estado de la infraestructura (Fase 4C-3, implementada — persistencia AÚN no activada)

`analysis/worldcup/guard_worldcup_external_persistence.py` ya implementa el **guard anti-manual**
read-only que exige la opción B:
- analiza solo los 4 ficheros permitidos y clasifica cada fila como *auto-persistible* vs *manual
  protegida*, contando celdas manuales;
- bloquea siempre `player_xg_xa.csv`, `referee_profiles.csv`, `coach_tactical_profiles.csv`;
- modo `--strict`: exit 1 si un fichero prohibido entra al set de commit, si un fichero "addable"
  todavía contiene datos manuales (un `git add` wholesale los commitearía → hace falta filtrado),
  o si hay inconsistencia de columnas;
- por defecto es diagnóstico (exit 0) y escribe `worldcup_external_persistence_guard.{txt,csv}`.

El workflow ejecuta el guard en modo **diagnóstico** (sin `--strict`, sin `git add`, sin commit).

## Estado de la infraestructura (Fase 4C-4, implementada — persistencia AÚN no activada)

Fase 4C-4 construye y **simula** la opción B sin activarla. Tres piezas nuevas, todas read-only sobre
`data/external/` (nunca lo mutan) y sin `git add`/`commit`/`push`:

1. `analysis/worldcup/build_worldcup_external_persistable_snapshot.py` — genera bajo
   `analysis/worldcup/persistable_external_snapshot/` una copia **filtrada auto-only** de los 4 ficheros
   permitidos: excluye filas no-auto, **vacía** las columnas manuales (scouting de posición, mediciones
   de clima) conservando el **esquema completo**, y solo emite penaltis reales de eventos. Nunca incluye
   `player_xg_xa.csv` / `referee_profiles.csv` / `coach_tactical_profiles.csv`. Modo `--check`: calcula
   sin escribir (exit 1 si una fuente tiene esquema roto/inesperado).
2. `guard_worldcup_external_persistence.py --strict --snapshot <dir>` — valida el snapshot filtrado;
   debe pasar strict (0 filas/celdas manuales) aunque `data/external` real tenga datos manuales.
3. `analysis/worldcup/simulate_worldcup_external_persistence_commit.py` — **simula** el commit acotado:
   dice qué rutas explícitas se añadirían, detecta diff real frente a `data/external` y detecta commit
   vacío. **Nunca** ejecuta `git add`/`commit`/`push` ni toca `main`.

El workflow ejecuta las tres en modo soft-fail (check → build → guard --strict snapshot → simulación),
**sin** `git add`, **sin** commit, **sin** push. El snapshot y los reportes generados están en
`.gitignore` (regenerables, nunca auto-commiteados).

## Próximo paso (Fase 4C-5, sujeto a aprobación 🔴)

Para activar realmente la opción B haría falta (propuesta → aprobación de Jorge → aplicación):
1. Decidir si se persiste el **snapshot filtrado** o se escribe lo auto-derivado directamente en
   `data/external` vía el merge seguro (Fase 4B) — y commitear con `git add <ruta-explícita>` por archivo.
2. Sustituir la **simulación** por un `git add`/`commit` acotado **condicionado a diff real** (sin
   commits vacíos), con `guard --strict` como gate bloqueante previo.
3. Permisos de escritura del workflow (`contents: write`) y trail de auditoría del commit automático.

Hasta esa aprobación explícita, **no se activa persistencia**: CI solo audita, hace dry-run, construye
el snapshot aislado y **simula**.
