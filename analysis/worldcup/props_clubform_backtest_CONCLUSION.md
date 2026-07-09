# Props de gol — forma de CLUB: veredicto

**Read-only · sin API · sin commit · sin tocar producción.** ¿Mezclar la forma de club 2025 (leak-free)
mejora la prop de gol sobre national-only? Test walk-forward sobre el WC-2026 liquidado.

- Muestra: 924 jugador-partido WC · base rate 8.1% · OOS test 462 filas · K*=500 min.
- **Baseline V0 = EXACTO de producción** (rates `fetch_team_rates`, RATE_SEASONS=[2024,2025]): fidelidad
  vs el `lam_goal` congelado del log **corr(p)=1.000, logloss idéntico (0.25065)**. Resuelve la caveat del
  test previo (baseline reconstruido débil, corr 0.688, que inflaba falsamente el efecto a +0.035 "ADOPTAR").

## Veredicto por variante (juez = OOS, baseline V0 nat-only)

| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |
|---|---|---|---|---|
| V0 (nat-only, baseline) | 0.24499 | (baseline) | — | — |
| V1 (blend K*=500) | 0.23004 | +0.01495 | [-0.00622..+0.03927] | NO adoptar (IC incluye 0) |
| V2 (club-only) | 0.23299 | +0.01200 | [-0.01278..+0.03941] | NO adoptar (IC incluye 0) |

## Recomendación

- **Ninguna variante supera el gate estricto** contra el V0 EXACTO de producción. El efecto es
  **direccionalmente positivo** (V1 Δlogloss +0.01495, ~6% relativo; V2 +0.01200) pero el **IC95 incluye 0**
  ([-0.006..+0.039] y [-0.013..+0.039]) → no excluye 0 con el margen exigido. Muestra WC infrapotenciada
  (OOS 462 filas, ~38 goles).
- **Recomendación: NO adoptar. Cerrar / L1-zero — no tocar `worldcup_player_props.py`.** La señal de club
  es prometedora (mejora media positiva y robusta en signo) pero no probada; **re-evaluable al crecer N** del
  WC liquidado (con estos mismos scripts, sin más API). El dato decide, no la intuición.

_Artefactos: props_clubform_backtest_report.txt · _metrics.csv · este CONCLUSION.md. No se tocó worldcup_player_props.py._