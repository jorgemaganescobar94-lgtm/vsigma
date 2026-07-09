# Props de gol — forma de CLUB (sample HISTÓRICO potente): veredicto

**Read-only · sin commit · sin tocar producción.** Test definitivo de club-form sobre el backtest
histórico de props (torneos 2024, ~3062 jugador-partido) con V0 nacional point-in-time (prior-season
2023, leak-free) + club-2022 (campaña cerrada May-2023, universalmente pre-partido).

- Muestra: 3062 jugador-partido · base rate 8.1% · positivos 248 · OOS test 1424 · K*=40000 min · club disponible en 91% de filas.

## Veredicto por variante (juez = OOS, baseline V0 nacional)

| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |
|---|---|---|---|---|
| V0 (nacional prior=prod) | 0.24580 | (baseline) | — | — |
| V1 (blend K*=40000) | 0.24418 | +0.00163 | [-0.00622..+0.00873] | NO adoptar (IC incluye 0) |
| V2 (club-2022-only) | 0.26398 | -0.01818 | [-0.03452..-0.00241] | PEOR que V0 (IC excluye 0 por debajo) |

## Recomendación

- **CIERRE DEFINITIVO (con potencia).** Ninguna variante supera el gate:
  - **V1 (blend)** Δlogloss +0.0016, IC95 [−0.006..+0.009] → **IC∋0**; además **K*=40.000** (el mayor del
    grid) = el tuneo en train empuja a **ignorar el club** (K→∞ ≡ V0).
  - **V2 (club-only)** Δlogloss −0.018, IC95 [−0.035..−0.002] → **significativamente PEOR** que nacional.
- El **+6% del WC era ruido de muestra pequeña** (~38 goles); con 6× potencia (248 goles) el efecto se
  anula. Las tasas de gol NACIONALES ya capturan el contexto de selección (rol/rivales/nivel) que no
  transfiere limpio desde el club. **Recomendación: CERRAR / L1-zero. No tocar `worldcup_player_props.py`.**

_Artefactos: props_clubform_hist_backtest_report.txt · _metrics.csv · este CONCLUSION.md. No se tocó worldcup_player_props.py._