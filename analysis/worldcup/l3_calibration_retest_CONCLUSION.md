# L3 1X2 CALIBRATION RE-TEST — veredicto

**Read-only · sin API · sin cambio de producción · sin commit.** Motivado por la infra-dispersión
monótona del L3 en las 5 bandas del Mundial (favoritos infra-llamados, underdogs sobre-llamados),
consistente en L3 y v2 (N=65) pero DENTRO del ruido (ECE 0.107 < p95 nulo 0.173). Regla de honestidad:
nada se ajusta a los 65 partidos del Mundial; todo se ajusta en burn-in (<2024) y se JUZGA en el OOS
histórico grande [2024-01-01, 2026-06-11). WC-2026 es holdout secundario (confirmación, nunca ajuste).

- **Temperatura ajustada (burn-in):** C1 (sobre isotónica) **T=1.0000**, C3 (sin isotónica) **T=1.1075**. Estabilidad train/val interno de C1: T_train=1.0267 / T_val=0.9758.
  T>=1: NO sharpening — la infra-dispersión no se confirma fuera del Mundial.

- **Gate:** idéntico a la re-prueba DC — ADOPTAR sólo si Δlogloss(C0-Cx)>0 en el histórico, con IC95 que
  excluye 0 con margen cómodo (min_lo≥0.005) y robusto en 10 semillas.

## Veredicto por variante (juez = OOS_PRIMARY histórico)

| variante | logloss C0→Cx | ΔECE | Δlogloss medio | IC95 (min_lo..max_hi) | veredicto |
|---|---|---|---|---|---|
| C1_temp | 0.93095→0.93095 | -0.0000 | +0.00000 | [-0.00000..+0.00000] | NO adoptar (IC incluye 0) |
| C2_rolliso | 0.93095→0.92973 | -0.0074 | +0.00123 | [+0.00004..+0.00244] | FRÁGIL — IC roza 0 (min_lo=+0.0000 < margen +0.005) -> NO adoptar |
| C3_temp_noiso | 0.93095→0.92590 | -0.0018 | +0.00505 | [+0.00021..+0.01279] | FRÁGIL — IC roza 0 (min_lo=+0.0002 < margen +0.005) -> NO adoptar |

## Confirmación WC-2026 (secundario, NO decide)

| variante | logloss C0→Cx | ΔECE | Δlogloss medio | veredicto WC |
|---|---|---|---|---|
| C1_temp | 0.89206→0.89206 | +0.0000 | +0.00000 | NO adoptar (IC incluye 0) |
| C2_rolliso | 0.89206→0.89527 | +0.0109 | -0.00321 | NO adoptar (IC incluye 0) |
| C3_temp_noiso | 0.89206→0.88996 | +0.0069 | +0.00211 | NO adoptar (IC incluye 0) |

## Recomendación

- **Ninguna variante** supera el gate estricto en el OOS histórico. La infra-dispersión observada en
  el Mundial es coherente con RUIDO (ECE dentro del p95 nulo) y/o no es corregible con la muestra
  fiable disponible. **Recomendación: cerrar el tema, mantener C0 (producción) sin cambios.**

_Artefactos: l3_calibration_retest_report.txt · l3_calibration_retest_metrics.csv · este CONCLUSION.md. No se tocó producción ni la isotónica congelada._