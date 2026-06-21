# World Cup 2026 — fichas de pronóstico (salida AISLADA)

Producto shadow, **fuera de producción**. Genera una ficha por partido próximo del Mundial
(league id **1**, season 2026) combinando, con la **fuente marcada** en cada dato.

## ¿Producción procesa el Mundial? NO
El allowlist de producción `scripts/filter_leagues.py` usa una lista explícita `(país, liga)`.
Tiene entradas `("world", ...)` para clubes (Libertadores, Sudamericana, AFC/CAF CL) pero **no**
`("world", "world cup")`. Toda liga no listada → `REJECT / "country_league_not_allowlisted"` (línea 246).
Por eso el Mundial **no entra** en el pipeline y este producto vive aislado en `analysis/worldcup/`.

## Qué trae la API para el Mundial (sondeado)
- **/odds**: rico — 12-14 casas incl. **Pinnacle** (sharp). Mercados: Match Winner (1X2), Goals O/U,
  Both Teams Score, y muchos más. → base de la ficha (mercado des-vigado = mejor pronóstico).
- **/predictions** (modelo propio del API): **disponibilidad por partido** — algunos sí (England-Croatia
  45/45/10 con advice), muchos "No predictions available" (selecciones sin datos de club). Se incluye
  donde existe y se marca NO DISPONIBLE donde no. Nunca se usa el placeholder 33/33/33.
- **/standings**: 12 grupos A-L (+1 tabla agregada que se ignora) con rank/puntos/jugados/forma.
- **/fixtures/lineups** e **/injuries**: aún no publicados a horas del partido → se marca y se refresca ~1h antes.

## Fuentes en la ficha
- `[MARKET]` — probabilidad des-vigada (consenso = mediana entre casas; Pinnacle como cross-check).
  De-vig = normalizar 1/odds a suma 1. El consenso ≈ Pinnacle en todos los partidos (de-vig validado).
- `[API-PRED]` — modelo del API (donde existe).
- `[STANDINGS]` — contexto de grupo/forma.
- `[LINEUPS/INJURIES]` — pendiente hasta ~1h antes.

**Honestidad:** el mercado es el mejor pronóstico disponible. NO se inventa edge ni se promociona ningún pick.

## Uso
```powershell
cd C:\Users\jorge\vsigma
.\.venv\Scripts\python.exe analysis/worldcup/build_worldcup_cards.py --from 2026-06-16 --to 2026-06-18
# re-correr cuesta ~0 (odds cacheadas 1h, predictions 6h). Acercándose al KO, re-correr trae lineups/injuries.
```
Salidas: `worldcup_cards.csv`, `worldcup_cards_report.txt` (en esta carpeta).

API: el script reporta la cuota real (forzando /status fresco). El grueso del gasto de hoy fue el backfill
de Brasil (Serie A+B, ~1830 llamadas); las fichas del Mundial cuestan unas pocas decenas de llamadas frescas
(odds + predictions por fixture, una vez; luego cacheadas).

## Integridad del learning loop (cobertura de logueo)
- **Ventana ancha de logueo `[HOY-1, HOY+3]` + rebuild estrecho.** El workflow construye una card
  ancha solo para alimentar el `log` (margen de cobertura: si un día el cron no corre, los partidos
  futuros se loguean igualmente antes del saque). Después **reconstruye la card estrecha** con los args
  originales, que es la única que ven settle/scorecard/render → **el mensaje de Telegram no cambia**.
- **Guard anti-hindsight.** `cmd_log` **nunca loguea un partido cuyo KO ya pasó** (evita capturar la
  predicción con el partido en juego). El logueo sigue siendo lock-first idempotente (dedup por fixture).
- **`worldcup_gaps.txt`.** Registro de fixtures que terminaron **sin haberse logueado nunca** (visibilidad
  de un hueco de cobertura). Es solo un aviso: **NUNCA se backfillean con el resultado ya conocido.**
- **Jornada 1 de grupos: pérdida permanente y correcta.** El learning loop no existía hasta el
  2026-06-19; toda la J1 se jugó antes y no quedó logueada. No se reconstruye (sería hindsight); se
  declara perdida a propósito.
