# data/external — fuentes externas opcionales (módulo de jugadores)

Estos ficheros **los aportas tú**. Si no existen, el módulo de jugadores degrada con honestidad
(`data_quality: baja`, `reason: fuente no configurada`) y **no inventa porcentajes** (regla §12).
Ningún proceso escribe aquí automáticamente ni toca `.env`/secrets.

## Ficheros que activan adaptadores

### `player_xa90.csv` — xA / xG reales por jugador (Fase 3)
Fuente recomendada: FBref / Understat / StatsBomb (export manual o tu propio extractor).
```
player_id,xa90,key_passes90
1100,0.31,1.8
```
Activa: `expected_xa` y `expected_key_passes` en `likely_assisters`.

### `referee_card_rates.csv` — tendencia del árbitro
Fuente: agregador de árbitros (export manual).
```
referee,cards_per_match,pen_per_match
Daniele Orsato,4.8,0.21
```
Activa: riesgo de tarjeta por árbitro (nivel alto/medio/bajo).

### `weather_by_fixture.csv` — clima por partido
Fuente: OpenWeather u otra (export manual). El fetch en vivo (Fase 2/3) requeriría que **tú** añadas
`OPENWEATHER_API_KEY` a tu `.env` — este repo solo detecta su presencia, nunca la escribe.
```
fixture_id,condition,temp_c,wind_kmh,rain_mm
1561329,Rain,14,22,3.1
```

### `set_piece_history.csv` — lanzadores de balón parado (Fase 2)
Hasta wirear el extractor de `/fixtures/events`, puedes aportar el historial de lanzadores:
```
team_id,player_id,penalties,free_kicks,corners
2384,1100,4,2,7
```
Activa: jerarquía real de penaltis/faltas/córners en `set_piece_takers` (con `confidence`).

---

## Fase 3 — contratos ampliados (xG/xA real, balón parado, árbitro, clima, táctica, posiciones)

Mismas reglas: **tú aportas el CSV**, nada se escribe aquí solo, no se tocan secrets, y si falta el
fichero (o le faltan columnas mínimas) el adaptador devuelve `{} / None + reason` y el sistema degrada
con `data_quality/confidence/reason` — **nunca inventa valores** (regla §12). Cargados por
`analysis/players/player_data_adapters.py`; el estado se ve en `external_data_status` del JSON.

> **Pre-poblado incremental seguro (Fase 4A/4B).** `analysis/worldcup/prepare_worldcup_external_templates.py`
> crea estas plantillas y las mantiene con un *merge incremental* que **solo** rellena desde datos reales
> ya cacheados en el repo (sin scraping, sin red, sin secrets): lanzadores de **penalti** desde
> `/fixtures/events` (`source=api_football_events`), **posición** del jugador desde alineaciones (fina si
> alguna fuente la trae, si no la gruesa GK/DEF/MID/FWD), y **árbitro/venue** si aparecen en el store.
> El merge **nunca borra filas, nunca duplica y nunca pisa una celda que ya rellenaste a mano**: solo
> añade filas nuevas, completa celdas vacías y refresca los hechos auto-derivados (p. ej. `attempts`,
> `last_taken_date`) de las filas cuyo `source` es automático. Tus ediciones manuales (cualquier `source`
> distinto, o cualquier celda no vacía) son intocables. Lo que no exista todavía se queda vacío.

### A) `player_xg_xa.csv` — xG/xA real por jugador  *(reemplaza el proxy en goles/tiros/asistencias)*
Columnas mínimas: `player_id, xg90, xa90`. Opcionales: el resto (None si faltan).
```
player_id,player_name,team_id,team_name,source,season,competition,minutes,xg,xa,xg90,xa90,shots90,sot90,key_passes90,crosses90,data_quality,confidence
1100,Some Player,2384,SomeTeam,FBref,2025-26,UCL,2480,18.2,9.1,0.66,0.33,3.1,1.4,1.9,1.2,alta,alta
```
Activa: `source_used = real_xg_xa` por jugador; xG/xA/tiros reales sustituyen el λ-proxy **solo en los
campos presentes** (lo demás sigue proxy y se marca como tal).

### B) `set_piece_takers.csv` — lanzadores declarados (penaltis/faltas/córners)
Columnas mínimas: `team_id, player_id, role`. `role` ∈ {`penalty`, `direct_free_kick`, `corner_left`,
`corner_right`, `indirect_free_kick`}.
```
team_id,team_name,player_id,player_name,role,rank,attempts,last_taken_date,source,data_quality,confidence
2384,SomeTeam,1100,Some Player,penalty,1,12,2026-06-20,manual,alta,alta
```
Prioridad de fuente §4: **eventos reales del Mundial > set_piece_takers.csv > historial de jugador >
no determinado** (se etiqueta `source_priority_used`).

### C) `referee_profiles.csv` — perfil del árbitro
Columnas mínimas: `referee_name, yellow_cards_pg`. Opcionales: el resto.
```
referee_name,matches,yellow_cards_pg,red_cards_pg,fouls_pg,penalties_pg,home_cards_pg,away_cards_pg,tournament_context,source,data_quality,confidence
Daniele Orsato,40,4.8,0.18,24.1,0.21,2.4,2.6,UEFA elite,manual,alta,media
```
Vinculación: el árbitro se asocia al fixture vía `fixture_referees.csv` (abajo) o si el fixture lo trae.
Solo matiza la **explicación** y el **rango de tarjetas/penaltis** si hay muestra suficiente.

### C-bis) `fixture_referees.csv` — mapa fixture → árbitro *(opcional, para vincular C)*
La ficha del Mundial no trae el árbitro; este mapa permite enlazarlo. Sin él, el árbitro queda
`no determinado` (honesto).
```
fixture_id,referee_name
1561329,Daniele Orsato
```

### D) `weather_by_fixture.csv` — clima por partido  *(acepta esquema Fase 3 y el legacy de Fase 2)*
Columna mínima: `fixture_id`.
```
fixture_id,venue,kickoff_time,temperature,humidity,wind_speed,rain_probability,pitch_condition,source,data_quality,confidence
1561329,Stadium,2026-06-20T18:00:00Z,31,55,12,0.1,seco,OpenWeather,media,media
```
Solo altera el guion (cualitativo) bajo **condiciones extremas** (viento fuerte, calor extremo, lluvia).

### E) `coach_tactical_profiles.csv` — perfil táctico del seleccionador  *(cualitativo, sin % duro)*
Columnas mínimas: `team_id, coach_name`. Opcionales: el resto.
```
team_id,team_name,coach_name,base_formation,pressing_level,defensive_block,build_up_style,transition_speed,width_usage,set_piece_emphasis,substitution_aggression,knockout_risk_profile,source,data_quality,confidence
2384,SomeTeam,Some Coach,4-3-3,alto,medio,corto,alto,bandas,alto,alto,conservador,manual,media,media
```
Activa: descripción de estilo + guion táctico por partido. **No genera porcentajes**.

### F) `player_positional_profiles.csv` — perfil posicional del jugador  *(alimenta matchups §8)*
Columnas mínimas: `player_id, position`. `*_threat`/`*_weight` ∈ [0,1] (None si faltan).
```
player_id,player_name,team_id,position,role,preferred_zone,attacking_weight,defensive_weight,aerial_threat,pace_threat,1v1_threat,crossing_threat,card_risk_role,source,data_quality,confidence
1100,Some Player,2384,RW,extremo,banda derecha,0.8,0.2,0.4,0.85,0.8,0.7,bajo,manual,media,media
```
Activa: duelos individuales (extremo vs lateral, central lento vs delantero rápido, portero vs volumen
de tiro…). Sin perfiles suficientes en ambos XI → `matchups_heuristic_only` con confianza baja.
