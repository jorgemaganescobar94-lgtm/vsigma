# Props de gol — recencia / forma de torneo: veredicto

**Read-only · sin API · sin commit · sin tocar producción.** ¿Incorporar la forma reciente/del
torneo a las props de gol mejora sobre la ventana fija `RATE_SEASONS=[2024,2025]`? Test walk-forward
anti-leakage sobre el backtest histórico de props (torneos 2024 = análogo del Mundial en curso).

- Muestra: 3062 jugador-partido · base rate gol 8.1% · 2026 filas con forma intra-ventana (66.2%).
- OOS (test temporal): 1424 filas. K* recencia (tuneado SOLO en train) = **2160 min**.

## Veredicto por variante (juez = OOS test)

| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |
|---|---|---|---|---|
| V0 (producción) | 0.24580 | (baseline) | — | — |
| V1 (pool minutos) | 0.24368 | +0.00212 | [-0.00114..+0.00567] | NO adoptar (IC incluye 0) |
| V2 (K*=2160) | 0.24393 | +0.00187 | [-0.00016..+0.00429] | NO adoptar (IC incluye 0) |

## Recomendación

- **Ninguna variante** supera el gate estricto en el OOS. La ventana fija (más estable) predice
  igual o mejor que perseguir la forma reciente: el efecto no excluye 0 con claridad. Coherente con
  que la forma intra-torneo es muestra pequeña y ruidosa (rachas que regresan a la media).
  **Recomendación: cerrar. Mantener V0 (`RATE_SEASONS` fija) sin cambios.** El dato decide, no la intuición.

_Artefactos: props_recency_backtest_report.txt · props_recency_backtest_metrics.csv · este CONCLUSION.md. No se tocó worldcup_player_props.py ni RATE_SEASONS._