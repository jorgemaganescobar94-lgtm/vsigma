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
