# RE-TEST tarjeta / tiros-a-puerta con INPUTS DEL MODELO DE STATS (no constantes)

**Fecha:** 2026-06-26 · **Modo:** READ-ONLY · **NO** se tocó producción · **NO** API · **NO** Telegram
**Script:** `analysis/worldcup/props_retest_stats_inputs.py`
**Salidas:** `..._report.txt`, `..._metrics.csv`, `..._calibration.csv`

## Qué se hizo
Re-test del backtest histórico de los props **tarjeta** y **tiros-a-puerta (≥1)**, quitando el
confound del primer backtest: en vez de inputs de equipo **constantes** (12 tiros, 3.8 tarjetas)
se usaron las estimaciones **walk-forward del modelo de stats de producción** (`stats_model.py`,
Poisson log-lineal de tiros/tarjetas con feature `opp_str`), repartidas al XI con la **misma
maquinaria de producción** (`worldcup_player_props.predict_fixture` / `_logloss/_brier/_ece`).

**Muestra:** los ~150 partidos internacionales cacheados del primer backtest (ene–jun 2024,
AFCON/AsianCup/WCQ). El modelo de stats solo cubre **97 de 150** (los 53 restantes son selecciones
de AFCON/AsianCup ausentes de `worldcup_stats_raw.csv`; ratearlos sería inventar → excluidos).
La constante se recalculó sobre los **mismos 97** (control apples-to-apples) y sobre los 150
completos (reproducción del original).

## Validación de la reconstrucción (clave)
El script reproduce el primer backtest **exactamente**: 3062 filas (idéntico al número original),
tarjeta bate baseline con cola optimista, **tiros con logloss peor que baseline y ECE 0.082 ≈ el
0.079 documentado**. La maquinaria es fiel → la comparación es creíble.

## Resultados

| Tabla | Inputs | prop | n | logloss skill | brier skill | ECE | ¿GRADÚA? |
|---|---|---|---|---|---|---|---|
| A (150) | constantes | card | 3062 | +10.3% | +7.3% | 0.032 | sí (formal) |
| A (150) | constantes | shot_on | 3062 | **−11.4%** | +19.7% | 0.082 | **no** |
| B (97) | constantes | card | 2059 | +12.5% | +9.4% | 0.035 | sí (formal) |
| B (97) | constantes | shot_on | 2059 | **−7.4%** | +21.0% | 0.089 | **no** |
| **C (97)** | **MODELO** | card | 1971 | +13.6% | +10.6% | 0.032 | sí (formal) |
| **C (97)** | **MODELO** | shot_on | 1971 | **−5.9%** | +24.2% | 0.059 | **no** |

Criterio de graduación (pre-registrado): logloss **Y** brier baten baseline **Y** ECE≤0.08.

### Tarjeta
- **Gradúa por el criterio formal con ambos inputs** (ya lo hacía con constantes). El confound
  **no** era lo que la bloqueaba: lo que la mantuvo "EXPERIMENTAL" fue la **cola sobre-optimista**.
- El modelo **mejora** algo (logloss skill +12.5%→+13.6%, brier +9.4%→+10.6%) y **tensa la banda
  media-alta** (gap 0.30–0.50: const +6.6% → modelo +1.2%).
- **Pero la cola extrema sigue optimista**: banda p>0.50 gap **+22.8% (const) → +24.1% (modelo)**,
  aunque es ínfima (n≈10). El modelo no resuelve esa punta.

### Tiros-a-puerta (≥1)
- **NO gradúa con ninguno de los dos.** El confound **no** era toda la historia.
- El modelo **sí ayuda**: ECE **0.089 → 0.059** (ya por debajo de 0.08), brier skill +21%→+24%,
  y mejora todas las bandas de calibración (cola p>0.50 gap +13.8% → +8.8%).
- **El bloqueo persiste en logloss**: sigue **por debajo del baseline** (skill −5.9%). Brier alto +
  logloss negativo = modelo bien calibrado en media pero penalizado por la cola de confianza; la
  tasa base (constante 21%) nunca arriesga y por eso no come penalización de logloss. Tiro-a-puerta
  ≥1 por jugador es intrínsecamente difícil de batir sobre base-rate con este método share+Poisson.

## Recomendación honesta
- **Tarjeta → MANTENER ETIQUETADO** (no graduar a "fiable" sin matices). Cumple el criterio formal,
  el modelo la mejora, pero la punta de alta confianza sigue inflada. Si se quisiera graduar, hacerlo
  **con tope/aviso en p>0.40** (donde la calibración se degrada) y vigilada por el scorecard en vivo.
- **Tiros-a-puerta → SOLO RANKING (orden), no probabilidad.** El modelo mejora la calibración (ahora
  ECE≤0.08) pero **no aporta skill de logloss sobre base-rate**. Mostrar como orden de probabilidad,
  no como % fiable.
- **Inputs del modelo > constantes** en ambos casos (mejor calibración y brier) → si se siguen
  mostrando estos props, usar los inputs del modelo de stats, no las constantes.

## Anti-leakage (confirmado)
- Rates /90 = **temporada 2023** (estrictamente previa a los partidos de 2024). Verificado: los 92
  ficheros de rates son `s2023`.
- Betas del modelo de stats = **walk-forward**, refit solo con `date < partido` (MIN_PAST=150, HL=540d);
  `lam_hat` finito para los 194 team-matches.
- XI = startXI **confirmado** (input observado). Target = actuals de `/fixtures/players` (solo salida).
- **Única mira-adelante menor (documentada):** la feature `opp_str` usa ratings L3 finales +
  estandarización full-sample — idéntica al modelo de stats de producción; coef pequeño. No se oculta.

## Limitaciones
- Muestra reducida a 97/150 por cobertura del modelo de stats (no es sesgo de selección dirigido,
  pero AFCON/AsianCup quedan fuera).
- La cola extrema de ambos props tiene n muy bajo (≈10); sus gaps son ruidosos.
- El modelo de stats subestima tiros en media (lam≈10.4 vs real 11.5); la constante 12 estaba más
  cerca de la media pero peor calibrada por partido.
