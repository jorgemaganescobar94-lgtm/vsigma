"""
WORLD CUP 2026 — WEATHER CONTEXT (Fase 3). READ-ONLY · NO API · NO market/odds · NO betting.

Reads data/external/weather_by_fixture.csv (via the adapter) and, IF a fixture has a row, produces an
honest qualitative read of the weather impact on tempo, shots, crosses, possession and fatigue. It only
shades the EXPLANATION — it does NOT modify the prediction except (conceptually) under EXTREME conditions
(heavy rain, strong wind, extreme heat), and even then it only LABELS the likely effect, never invents a
number. Absent weather row -> confidence baja + reason (spec §6, §12).

Output dict (spec §6):
  {weather_summary, impact_on_tempo, impact_on_shots, impact_on_crosses, impact_on_possession,
   impact_on_fatigue, confidence, reason, extreme, data_quality}
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402

# EXTREME thresholds (only these justify hinting at a real effect on the game).
WIND_STRONG = 30.0       # km/h sustained -> long balls/crosses/shooting from distance degrade
HEAT_EXTREME = 32.0      # °C -> tempo down, fatigue up, more rotation late
COLD_EXTREME = 2.0       # °C
RAIN_PROB_HIGH = 0.6     # >=60% -> slick pitch
RAIN_MM_WET = 2.0        # mm -> slick pitch even without a probability column


def _none_ctx(reason):
    return {"weather_summary": "no determinado", "impact_on_tempo": "neutro",
            "impact_on_shots": "neutro", "impact_on_crosses": "neutro",
            "impact_on_possession": "neutro", "impact_on_fatigue": "neutro",
            "extreme": False, "confidence": "baja", "data_quality": "baja", "reason": reason}


def _is_wet(w):
    rp = w.get("rain_probability")
    rmm = w.get("rain_mm")
    cond = (w.get("pitch_condition") or w.get("condition") or "").lower()
    if rp is not None and rp >= RAIN_PROB_HIGH:
        return True
    if rmm is not None and rmm >= RAIN_MM_WET:
        return True
    return any(k in cond for k in ("rain", "lluvia", "storm", "tormenta", "wet", "snow", "nieve"))


def build_weather_context(fixture_id, weather_map=None, weather_reason=None):
    """fixture_id: int. weather_map: {fid: {...}} from the adapter (loaded once by the caller); if None
    we load it here. Returns the §6 structure, degrading honestly when no row exists."""
    if weather_map is None:
        weather_map, weather_reason = adapters.load_weather_by_fixture()
    if not weather_map:
        return _none_ctx(weather_reason or "clima no configurado — Fase 3")
    try:
        w = weather_map.get(int(fixture_id))
    except Exception:
        w = None
    if not w:
        return _none_ctx("fixture sin registro de clima en la tabla externa")

    temp = w.get("temperature")
    wind = w.get("wind_speed")
    # A row with NO actual measurements (e.g. a kickoff/venue-only template row) is NOT "normal
    # weather" — it is unknown. Degrade honestly instead of implying benign conditions.
    has_measurement = any(w.get(k) is not None for k in
                          ("temperature", "humidity", "wind_speed", "rain_probability", "rain_mm")) \
        or bool(w.get("pitch_condition")) or bool(w.get("condition"))
    if not has_measurement:
        return _none_ctx("fila de clima sin mediciones (solo kickoff/venue) — pendiente de rellenar")
    wet = _is_wet(w)
    parts = []
    if temp is not None:
        parts.append(f"{temp:.0f}°C")
    if wind is not None:
        parts.append(f"viento {wind:.0f} km/h")
    if wet:
        parts.append("campo húmedo/lluvia")
    if w.get("pitch_condition"):
        parts.append(str(w["pitch_condition"]))
    summary = ", ".join(parts) if parts else "datos de clima parciales"

    tempo = shots = crosses = possession = fatigue = "neutro"
    extreme = False
    notes = []

    if wind is not None and wind >= WIND_STRONG:
        extreme = True
        shots = "tiros lejanos menos fiables (viento fuerte)"
        crosses = "centros menos precisos (viento fuerte)"
        possession = "juego más directo/menos elaboración"
        notes.append("viento fuerte")
    if wet:
        extreme = True
        tempo = "transiciones más rápidas (balón desliza)"
        possession = "control más difícil; posibles errores"
        notes.append("campo húmedo")
    if temp is not None and temp >= HEAT_EXTREME:
        extreme = True
        tempo = "ritmo más bajo por calor"
        fatigue = "fatiga elevada; más rotación en la segunda parte"
        notes.append("calor extremo")
    elif temp is not None and temp <= COLD_EXTREME:
        notes.append("frío intenso")

    if not extreme:
        reason = "clima dentro de rangos normales; sin impacto material en la predicción"
        conf = "media"
    else:
        reason = "condiciones extremas (" + ", ".join(notes) + "): efecto CUALITATIVO sobre el guion, " \
                 "no se altera el número de la predicción"
        conf = "media"
    if w.get("confidence"):
        reason += f"; confianza de fuente: {w['confidence']}"

    return {
        "weather_summary": summary,
        "impact_on_tempo": tempo, "impact_on_shots": shots, "impact_on_crosses": crosses,
        "impact_on_possession": possession, "impact_on_fatigue": fatigue,
        "extreme": extreme, "confidence": conf, "data_quality": "media", "reason": reason,
    }
