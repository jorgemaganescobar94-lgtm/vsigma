"""
WORLD CUP 2026 — COACH / TACTICAL CONTEXT (Fase 3). READ-ONLY · NO API · NO market/odds · NO betting.

Reads data/external/coach_tactical_profiles.csv (via the adapter) and turns the qualitative coach
profile of each team into a readable style description + a probable MATCH SCRIPT. It deliberately
produces NO hard percentages from a purely qualitative profile (spec §7): it shades the narrative only.
Marks every output as manual/external and degrades honestly when a profile is absent.

Analyses: base formation, pressing, defensive block, transition speed, width, wing usage, set-piece
emphasis, substitution aggression, knockout management.

Output per team (build_team_style) + a combined script (build_tactical_context):
  {home_style, away_style, expected_match_script, confidence, reason, source}
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402

# qualitative buckets we recognise (anything else is passed through verbatim, never invented)
_HIGH = {"alto", "alta", "high", "muy alto", "intenso"}
_LOW = {"bajo", "baja", "low", "muy bajo", "pasivo"}


def _lvl(v):
    if not v:
        return None
    s = str(v).strip().lower()
    if s in _HIGH:
        return "alto"
    if s in _LOW:
        return "bajo"
    return "medio"


def build_team_style(team_name, profile):
    """Readable style string for one team from its profile dict (or a None-degraded note)."""
    if not profile:
        return {"team": team_name, "style": "estilo no determinado (sin perfil táctico externo)",
                "coach_name": None, "confidence": "baja", "source": None,
                "reason": "perfil táctico no configurado para este equipo — Fase 3"}
    bits = []
    if profile.get("base_formation"):
        bits.append(f"formación base {profile['base_formation']}")
    press = _lvl(profile.get("pressing_level"))
    if press:
        bits.append({"alto": "presión alta", "bajo": "presión baja",
                     "medio": "presión media"}[press])
    block = _lvl(profile.get("defensive_block"))
    if block:
        bits.append({"alto": "bloque alto", "bajo": "bloque bajo replegado",
                     "medio": "bloque medio"}[block])
    trans = _lvl(profile.get("transition_speed"))
    if trans:
        bits.append({"alto": "transiciones rápidas", "bajo": "transiciones lentas/elaboradas",
                     "medio": "transición media"}[trans])
    width = _lvl(profile.get("width_usage"))
    if width:
        bits.append({"alto": "mucho juego por bandas/extremos", "bajo": "juego interior/estrecho",
                     "medio": "amplitud media"}[width])
    if profile.get("build_up_style"):
        bits.append(f"salida {profile['build_up_style']}")
    if profile.get("set_piece_emphasis"):
        bits.append(f"énfasis en balón parado: {profile['set_piece_emphasis']}")
    subs = _lvl(profile.get("substitution_aggression"))
    if subs:
        bits.append({"alto": "cambios agresivos/tempranos", "bajo": "cambios conservadores",
                     "medio": "gestión de cambios media"}[subs])
    if profile.get("knockout_risk_profile"):
        bits.append(f"eliminatorias: {profile['knockout_risk_profile']}")
    style = "; ".join(bits) if bits else "perfil presente pero sin campos descriptivos"
    return {"team": team_name, "style": style, "coach_name": profile.get("coach_name"),
            "confidence": profile.get("confidence") or "media", "source": profile.get("source"),
            "reason": "perfil táctico externo (cualitativo, sin % duro)"}


def _script(home_style, away_style, hp, ap):
    """Probable match script from the two qualitative profiles. Narrative only — no percentages."""
    if not hp and not ap:
        return "sin guion táctico (perfiles no disponibles)"
    h_press = _lvl((hp or {}).get("pressing_level"))
    a_press = _lvl((ap or {}).get("pressing_level"))
    h_block = _lvl((hp or {}).get("defensive_block"))
    a_block = _lvl((ap or {}).get("defensive_block"))
    parts = []
    if h_press == "alto" and a_press == "alto":
        parts.append("dos equipos a presión alta: partido roto, muchas transiciones")
    elif "alto" in (h_press, a_press) and "bajo" in (h_block, a_block):
        parts.append("presión alta contra bloque bajo: un equipo intentará encerrar al otro")
    elif h_block == "bajo" and a_block == "bajo":
        parts.append("dos bloques bajos: partido cerrado, pocas ocasiones claras")
    h_width = _lvl((hp or {}).get("width_usage"))
    a_width = _lvl((ap or {}).get("width_usage"))
    if "alto" in (h_width, a_width):
        parts.append("peligro por bandas/centros para al menos un equipo")
    if (hp or {}).get("knockout_risk_profile") or (ap or {}).get("knockout_risk_profile"):
        parts.append("gestión de eliminatoria puede frenar el ritmo en tramos")
    return " · ".join(parts) if parts else "estilos compatibles sin un patrón dominante claro"


def build_tactical_context(home_id, away_id, home_name, away_name, coach_map=None, coach_reason=None):
    """Combined §7 tactical context for one fixture. coach_map: {team_id: profile} from the adapter
    (loaded once by the caller); if None we load it here. Degrades honestly per team."""
    if coach_map is None:
        coach_map, coach_reason = adapters.load_coach_profiles()
    hp = coach_map.get(int(home_id)) if home_id is not None else None
    ap = coach_map.get(int(away_id)) if away_id is not None else None
    home = build_team_style(home_name, hp)
    away = build_team_style(away_name, ap)
    have = bool(hp) + bool(ap)
    conf = "media" if have == 2 else ("baja" if have == 1 else "baja")
    if have == 0:
        reason = coach_reason or "perfiles tácticos no configurados — Fase 3"
    elif have == 1:
        reason = "solo un equipo tiene perfil táctico externo; guion parcial"
    else:
        reason = "ambos perfiles tácticos externos (cualitativo, no altera el número de la predicción)"
    return {
        "home_style": home, "away_style": away,
        "expected_match_script": _script(home, away, hp, ap),
        "confidence": conf, "data_quality": "media" if have else "baja",
        "source": "manual/externo (coach_tactical_profiles.csv)", "reason": reason,
    }
