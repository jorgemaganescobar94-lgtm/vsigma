# Backtest — TOTAL DE GOLES dependiente del partido vs total constante (auditoría candidato #1)

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API
**Script:** `analysis/worldcup/total_goals_backtest.py`
**Salidas:** `..._report.txt`, `..._metrics.csv`

## Qué se midió
Hoy `raw_xg` hace `s = a0 + a1·sup`; `xg = (total_mean ± s)/2` con **total_mean CONSTANTE (2.658)**.
Hipótesis: el total real sube en los desajustes, así que un total dependiente del partido debería
calibrar mejor Over/Under 2.5 y BTTS, sin tocar el 1X2 (que depende de la DIFERENCIA, no del total).
Se reutiliza la maquinaria de calibración del L3 (`national_elo_layer3`: `fit_rating` + pesos +
`wdl` + `Isotonic`), mismo walk-forward y mismo split burn-in/OOS. Solo cambia el TOTAL.

**Anti-leakage:** supremacía L3 walk-forward (refit cada 30d, solo datos previos; cross-check vs el
`permatch.csv` committeado, max|Δ|≈0). Coeficientes del total ajustados **solo en burn-in**
(date<2024-01-01, 5614 partidos). Evaluación OOS (≥2024-01-01, **3277 partidos**). Target solo se
puntúa. Isotónica del 1X2 **re-ajustada por modelo** en burn-in (test justo de no-daño).

## (a) Formas del total probadas (coef. ajustados en burn-in, lstsq sobre gh+ga)
| forma | fórmula |
|---|---|
| baseline | total = **2.6578** (constante) |
| (a) \|sup\| | total = 2.193 + **0.675·\|sup\|** |
| (b) \|sup\|+sup² | total = 2.393 + 0.075·\|sup\| + **0.273·sup²** |
| (c) s_home+s_away | total = 2.687 − 0.089·(s_h+s_a) |

## (b) Métricas OOS candidato vs baseline (Δ = baseline − candidato; >0 = candidato mejor)

| forma | Over2.5 Δll · IC95% | BTTS Δll · IC95% | total MAE Δ | 1X2 Δll · IC95% |
|---|---|---|---|---|
| baseline | ll 0.6908, ECE 0.007 | ll 0.7000, **ECE 0.060** | 1.440 | ll 0.9301 |
| **(a) \|sup\|** | +0.0025 [−0.003,+0.008] **n.s.** (ECE↑0.032) | **+0.0209 [+0.012,+0.030] SIG** (ECE↓0.010) | +0.018 | −0.0003 [−0.0011,+0.0004] **OK** |
| **(b) \|sup\|+sup²** | **+0.0047 [+0.0004,+0.0091] SIG** (ECE 0.020) | **+0.0199 [+0.012,+0.028] SIG** (ECE↓0.014) | +0.017 | −0.0005 [−0.0013,+0.0002] **OK** |
| (c) s_h+s_a | −0.0006 n.s. | −0.0035 [−0.006,−0.001] (peor) | +0.002 | −0.0013 [−0.0032,+0.0007] OK |

(SIG = IC95% excluye 0. n.s. = no significativo. ECE↓ = calibración mejora.)

## (c) ¿Sube el total real con \|sup\|? — SÍ, confirmado
Coeficiente `b1 = +0.675` goles por unidad de `|sup|` (ajustado en burn-in). En el rango OOS de
`|sup|` (p10..p90 = 0.11..1.42), eso es un **swing de ≈ +0.88 goles** entre un partido parejo y un
desajuste grande. La hipótesis del total mayor en los desajustes es **real y notable**.

## (d) ¿Se mantiene el 1X2? — SÍ
Con la isotónica re-ajustada por modelo, el 1X2 **apenas se mueve** (Δlogloss ≤ 0.0013) y en las tres
formas el **IC95% del 1X2 incluye 0** → **no hay daño significativo**. Confirma la premisa: el 1X2
depende de la diferencia (`lh−la = s`), que NO cambia; solo el nivel del total cambia la prob. de
empate de forma negligible.
(Nota: aplicar el total nuevo con la isotónica VIEJA sin recalibrar SÍ rompía el 1X2 — por eso el
test correcto recalibra la isotónica, como se haría al desplegar.)

## (e) Recomendación honesta: **INTEGRAR (forma b) — propuesta 🔴 para tu aprobación**
A diferencia de los dos candidatos previos de la auditoría (matchup, contexto) que se descartaron,
**este SÍ aporta valor real y significativo**:
- **BTTS**: mejora **clara y significativa** (Δll +0.020, IC excluye 0) y arregla la **peor
  calibración del baseline** (ECE 0.060 → 0.014). Es el mayor beneficio.
- **Over2.5**: la forma (b) mejora logloss de forma **significativa** (Δ +0.0047) aunque modesta; su
  ECE sube un poco (0.007 → 0.020) — sharper pero algo menos calibrada. La forma (a) no es signif. en
  Over2.5.
- **1X2**: **no se daña** (no significativo en ninguna forma).
- **Hipótesis confirmada**: el total sube +0.88 goles del partido parejo al desajuste.

**Forma recomendada: (b) `total = 2.393 + 0.075·|sup| + 0.273·sup²`** — la única que mejora Over2.5 Y
BTTS de forma significativa sin dañar el 1X2. (La forma (a), más simple, también vale si solo importa
BTTS.) La forma (c) (calidad combinada) se descarta: coef. negativo y empeora BTTS.

**Es un cambio de FÓRMULA del modelo (raw_xg) → 🔴 requiere tu aprobación de gobernanza y trail de
revisión.** Caveats a vigilar si se integra: (i) la calibración de Over2.5 (ECE) baja un poco — vale
la pena un monitor; (ii) re-ajustar la isotónica del 1X2 al adoptar el total nuevo (obligatorio);
(iii) los beneficios absolutos en logloss son modestos (el grande es la calibración de BTTS).

## Limitaciones
- Mejora absoluta de logloss modesta (OU/BTTS ~0.005–0.02); el valor real es la calibración de BTTS.
- Over2.5: sharper pero ECE algo peor → no es una victoria limpia en OU; el grueso del beneficio es BTTS.
- Muestra OOS amplia (3277) → la significancia es sólida, pero es OOS de internacionales 2024-25
  (no específico del Mundial neutral; la dirección debería trasladarse, pero conviene re-mirar en vivo).
