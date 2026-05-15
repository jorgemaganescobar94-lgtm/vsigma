\# vSIGMA Competition Versions



\## Official Frozen Baseline

Nombre:

vSIGMA Competition Accuracy Mode + Probability Calibration



Estado:

VERSIÓN OFICIAL CONGELADA



Componentes principales:

\- rolling fixture statistics

\- recent form

\- standings / league context

\- odds / market fit

\- league coverage matrix

\- injuries in advisory mode

\- lineups with timing governance

\- tightened premium extended governance

\- pick explanation layer

\- daily decision journal

\- competition accuracy mode

\- calibrated competition probabilities



Uso:

\- versión oficial para comparación diaria

\- no tocar arquitectura salvo bug claro o patrón repetido serio



\---



\## Experimental Candidate v2

Nombre:

vSIGMA Competition Candidate — Schedule Strength + Anomaly Cleaning



Estado:

VERSIÓN EXPERIMENTAL EN SHADOW MODE



Mejoras añadidas:

\- strength-of-schedule adjustment for recent sample

\- event-based anomaly cleaning on recent fixtures

\- neutral handling of missing event coverage

\- conservative trust multipliers in scoring / deep analysis



Resultados históricos experimentales (2026-04-23 → 2026-05-08):

\- FULL\_SHORTLIST:

&#x20; - baseline: 20 rows, 16W-4L, +4.07u, ROI 20.35%

&#x20; - experimental: 22 rows, 18W-4L, +7.34u, ROI 33.36%

\- CORE\_ONLY:

&#x20; - baseline: 11 rows, 9W-2L, +2.77u, ROI 25.18%

&#x20; - experimental: 16 rows, 13W-3L, +6.40u, ROI 40.00%



Estado de decisión:

\- todavía no sustituye a la versión oficial

\- se compara en paralelo varios días

\- si mantiene mejora real sin romper limpieza/calibración, puede ascender a oficial



\---



\# Competition Daily Comparison Log



\## 2026-05-11

\### Official Frozen Baseline

\- Picks oficiales:

&#x20; 1. Benfica vs SC Braga — BTTS YES

&#x20; 2. Napoli vs Bologna — HOME WIN

\- Resultado: 1W / 1L

\- Profit: -0.09u

\- ROI: -4.50%

\- Lectura:

&#x20; - Benfica BTTS = WIN\_CONFIRMED

&#x20; - Napoli HOME\_WIN = LOSS\_MATCHED\_FAILURE\_MODE

\- Nota:

&#x20; - un verde limpio y un rojo alineado con FAILURE\_MODE\_DRAW\_LIVE

&#x20; - día prácticamente neutro, sin señal de rotura estructural



\### Experimental Candidate v2

\- No comparado aún en vivo

\- Estado: pendiente / no ejecutado ese día



\---



\## 2026-05-12

\### Official Frozen Baseline

\- Picks oficiales de competición:

&#x20; 1. Southampton vs Middlesbrough — OVER 2.5

&#x20; 2. Servette FC vs Lausanne — OVER 2.5

&#x20; 3. Catanzaro vs Avellino — OVER 1.5

\- Resultado bloque oficial: 1W / 2L

\- Profit aprox.: -1.58u

\- ROI aprox.: -52.7%

\- Shortlist completo:

&#x20; - 4 picks

&#x20; - 1W / 3L

&#x20; - Profit total: -2.58u

&#x20; - ROI: -64.5%

\- Lectura:

&#x20; - patrón dominante = OVER\_2.5 con FAILURE\_MODE\_LOW\_CONVERSION

&#x20; - tesis de goles razonable, pero línea demasiado alta en dos picks core



\### Experimental Candidate v2

\- No comparado aún en vivo

\- Estado: pendiente / no ejecutado ese día



\---



\## 2026-05-13

\### Official Frozen Baseline

\- Picks oficiales de competición:

&#x20; 1. Lens vs Paris Saint Germain — OVER 2.5

&#x20; 2. Alaves vs Barcelona — OVER 2.5

&#x20; 3. Vissel Kobe vs Kyoto Sanga — OVER 1.5

\- Estado: PRE REGISTRADO

\- Pendiente de cierre post-resultados



\### Experimental Candidate v2

\- Pendiente de ejecutar en shadow mode

\- Pendiente de comparación directa



\---



\# Reglas de evaluación

\- No cambiar el sistema por un solo día.

\- Revisar ajustes solo por patrones repetidos.

\- Métricas principales:

&#x20; - Hit rate

&#x20; - Profit units

&#x20; - ROI

&#x20; - Brier / calibración

&#x20; - Calidad del bloque CORE

&#x20; - Calidad del bloque competition\_top

&#x20; - Failure modes repetidos



\---



\## Experimental Candidate v3

Nombre:

vSIGMA Competition Candidate — Odds Structure Depth



Estado:

VERSIÓN EXPERIMENTAL SECUNDARIA / NO PROMOVIDA



Mejoras añadidas:

\- odds ladder / odds structure depth

\- implied probability relationships across related market families

\- bookmaker support breadth

\- odds dispersion / coherence

\- line-width governance

\- side fragility flags

\- total ladder shape

\- market translation hints



Resultado histórico experimental (2026-04-23 → 2026-05-08):

\- Rows: 9

\- W-L: 7-2

\- Hit rate: 77.78%

\- Profit: +2.31u

\- ROI: 25.67%

\- Brier: 0.168394



Comparación:

\- mejora ligeramente a candidate v2

\- no supera a la baseline oficial congelada

\- la ganancia parece venir sobre todo de traducción de mercado / anchura de línea

\- no demuestra mejora suficiente para ascender a oficial



Decisión:

\- mantener como experimento secundario

\- no promover a versión oficial

\- no sustituye a baseline ni a candidate v2 como principal retador



Veredicto:

ODDS\_STRUCTURE\_DEPTH\_PARTIAL



\---



\## Experimental Candidate v4

Nombre:

vSIGMA Competition Candidate — O2.5 Low Conversion Firewall



Estado:

VERSIÓN EXPERIMENTAL SHADOW-ONLY / NO PROMOVIDA



Mejoras añadidas:

\- firewall específico para OVER\_2\_5 con FAILURE\_MODE\_LOW\_CONVERSION

\- decisiones posibles:

&#x20; - KEEP\_OVER\_2\_5

&#x20; - DEGRADE\_TO\_OVER\_1\_5

&#x20; - REMOVE\_FROM\_COMPETITION\_TOP

&#x20; - SECONDARY\_ONLY

\- soporte para downgrade real OVER\_2\_5 -> OVER\_1\_5 cuando el mercado alternativo es limpio



Resultado live 2026-05-13:

\- Baseline: 3 picks, 1W / 2L, -1.56u, ROI -52.0%

\- Candidate v2: 2 picks, 1W / 1L, -0.56u, ROI -28.0%

\- Candidate v4: 1 pick, 1W / 0L, +0.44u, ROI 44.0%



Lectura live:

\- v4 evitó Lens vs PSG OVER\_2\_5, que perdió.

\- v4 mantuvo Stockport vs Stevenage OVER\_1\_5, que ganó.

\- Corrigió bien el patrón reciente de OVER\_2\_5 + LOW\_CONVERSION.



Resultado histórico evaluable:

\- Baseline: 9 rows, 7W / 2L, +2.03u, ROI 22.56%

\- Candidate v2: 8 rows, 6W / 2L, +1.67u, ROI 20.88%

\- Candidate v4: 6 rows, 4W / 2L, +0.25u, ROI 4.17%



Decisión:

\- No promover.

\- Mantener en shadow mode.

\- El umbral actual parece demasiado destructivo en histórico.

\- Seguir recogiendo días live antes de ajustar o promocionar.



Veredicto:

O25\_LOW\_CONVERSION\_FIREWALL\_PARTIAL


---

## Experimental Candidate v5
Nombre:
vSIGMA Competition Candidate — Player Impact Layer

Estado:
VERSIÓN EXPERIMENTAL SHADOW-ONLY / NO PROMOVIDA

Mejoras añadidas:
- player impact enrichment
- attacking core availability score
- defensive core availability score
- goalkeeper confidence flags
- player impact coverage flags
- player impact market translation hints
- conservative player-impact adjustments

Resultado actual 2026-05-14:
- Official baseline top: 0
- Candidate v2 top: 0
- Candidate v5 shortlist: 0
- Candidate v5 top: 0
- Día sin picks.

Resultado histórico evaluable:
- Baseline official: 9 rows, 7W / 2L, +2.03u, ROI 22.56%, Brier 0.168610
- Candidate v2: 8 rows, 6W / 2L, +1.67u, ROI 20.88%, Brier 0.183962
- Candidate v5: 8 rows, 6W / 2L, +1.67u, ROI 20.88%, Brier 0.183962

Player-impact adjustments:
- 3 total
- 2 strengthened
- 1 downgraded
- 0 blocked

Decisión:
- No promover.
- Mantener en shadow mode.
- Útil como capa explicativa, pero sin mejora agregada demostrada.
- Evaluar en vivo solo el subconjunto donde player_impact_adjustment_action != NOT_APPLIED.

Veredicto:
PLAYER_IMPACT_LAYER_PARTIAL

---

## Experimental Candidate v6
Nombre:
vSIGMA Competition Candidate — API Predictions Benchmark

Estado:
VERSIÓN EXPERIMENTAL SHADOW-ONLY / NO PROMOVIDA

Mejoras añadidas:
- integración del endpoint API Predictions como benchmark externo
- comparación entre pick vSIGMA y predicción externa API
- flags de alineación / desacuerdo
- ajuste conservador de confianza
- reportes diarios y post-resultados separados

Resultado actual 2026-05-14:
- Official baseline top: 0
- Candidate v2 top: 0
- Candidate v6 shortlist: 0
- Candidate v6 top: 0
- Día sin picks.
- API prediction calls: 0 porque candidate v2 no tenía filas para auditar.

Resultado histórico evaluable:
- Baseline official: 9 rows, 7W / 2L, +2.03u, ROI 22.56%, Brier 0.168610
- Candidate v2: 8 rows, 6W / 2L, +1.67u, ROI 20.88%, Brier 0.183962
- Candidate v6: 6 rows, 4W / 2L, +0.25u, ROI 4.17%, Brier 0.230726

API Predictions Coverage:
- Historical benchmark rows with predictions: 22
- API calls: 22
- API errors: 0
- Aligned rows: 5
- Disagreement rows: 5
- Strengthened rows: 5
- Weakened rows: 0
- Secondary/removed-from-v6-selection rows: 5

Lectura:
- El benchmark de predicciones externas añadió información explicativa.
- Como filtro de selección, sobrepodó el bloque y empeoró resultados.
- El subconjunto alineado que sobrevivió fue 1W / 0L, pero el sistema global quedó peor.
- No debe usarse como selector.

Decisión:
- No promover.
- Mantener solo como capa de auditoría / explicación externa.
- No permitir que API Predictions genere picks ni filtre de forma fuerte.
- La baseline oficial sigue siendo superior.

Veredicto:
API_PREDICTIONS_BENCHMARK_NOT_HELPFUL

---

## Experimental Candidate v7
Nombre:
vSIGMA Competition Candidate — Price Discipline + CLV + Drift Execution Guard

Estado:
VERSIÓN EXPERIMENTAL SHADOW-ONLY / NO PROMOVIDA

Mejoras añadidas:
- disciplina de precio por familia de mercado
- edge mínimo requerido según mercado y failure mode
- penalización por drift monitor
- tracking de CLV / movimiento de cuota
- control de picks con edge fino
- bloqueo o secondary-only cuando el precio no compensa el riesgo

Resultado live 2026-05-14:
- Candidate v7 no hizo picks top.
- Bloqueó los dos picks de candidate v2 como PRICE_THIN_SECONDARY_ONLY:
  1. Valencia vs Rayo Vallecano — OVER 1.5
     - actual edge: 0.135214
     - required edge: 0.143
     - drift: WATCH_PATTERN
     - CLV: CLV_FLAT
  2. Bradford vs Bolton — OVER 1.5
     - actual edge: 0.136220
     - required edge: 0.143
     - drift: WATCH_PATTERN
     - CLV: CLV_FLAT
- Esa decisión evitó un bloque que terminó 1W / 1L y -0.60u.

Resultado histórico evaluable:
- Baseline: 9 rows, 7W / 2L, +2.03u, ROI 22.56%
- Candidate v2: 8 rows, 6W / 2L, +1.67u, ROI 20.88%
- Candidate v7: 3 rows, 3W / 0L, +2.42u, ROI 80.67%

Segmentos relevantes:
- v2 OVER_1_5 + LOW_CONVERSION: 5 rows, 3W / 2L, -0.75u, ROI -15.0%
- v7 OVER_1_5 + LOW_CONVERSION: 0 rows
- v7 retained OVER_2_5 + LOW_CONVERSION: 2 rows, 2W / 0L, +1.42u
- v7 retained WIN + DRAW_LIVE: 1 row, 1W / 0L, +1.00u

Decisión:
- No promover todavía por muestra pequeña.
- Mantener como shadow prioritario.
- Comparar diariamente contra baseline y candidate v2.
- Si mantiene mejor ROI sin destruir demasiado volumen, puede convertirse en el principal retador a la baseline.

Veredicto:
PRICE_DISCIPLINE_CLV_GUARD_PARTIAL

