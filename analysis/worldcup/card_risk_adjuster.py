"""
WORLD CUP 2026 — CARD-RISK ADJUSTER (Fase 4F). PURE function · NO I/O side effects on data/external ·
NO API · NO scraping · NO market/odds/betting · NO fabrication.

Combines, CONSERVATIVELY, the per-player base card probability (already produced by the props model,
possibly bias-corrected upstream) with the auto discipline profiles derived from REAL World Cup events:
  * player card history        (worldcup_card_profiles_auto -> players)
  * card risk by position       (                            -> positions)
  * team discipline environment (                            -> teams)
  * referee card environment    (referee_context, manual>auto>none)

Each source nudges the probability by a SMALL, confidence-weighted step. Tiny samples barely move it
(a 1-match referee is down-weighted hard); conflicting sources net out (conservative); when there is
not enough usable signal the direction is 'neutro' and the ORIGINAL value is kept. The probability is
NEVER driven to zero by the absence of cards.

adjust_card_risk(...) -> {
  probability_card_original, probability_card_adjusted, adjustment_direction (subir/bajar/neutro),
  adjustment_reason, card_risk_components{player_history, position_profile, team_profile,
  referee_profile}, confidence, data_quality
}
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARD_PROFILES_JSON = HERE / "worldcup_card_profiles_auto.json"

# per-source step (the maximum multiplicative nudge before confidence weighting). The player's own
# history is trusted most; the others are softer priors.
STEP_PLAYER = 0.10
STEP_POSITION = 0.05
STEP_TEAM = 0.05
STEP_REFEREE = 0.06

# referee with a thin sample must barely move the number (spec §5).
REF_THIN_MATCHES = 1
REF_THIN_FACTOR = 0.25

# total multiplicative factor is clamped: never more than +30% / -25% even if everything aligns.
FACTOR_MAX = 1.30
FACTOR_MIN = 0.75

# below this much summed usable weight there is not enough signal -> neutro, keep original.
MIN_TOTAL_WEIGHT = 0.15

# probability is clamped to a sane band; the lower clamp is tiny but NON-zero (never zero by absence).
P_MIN = 0.01
P_MAX = 0.95

_CONF_WEIGHT = {
    "alta": 1.0, "media": 0.6, "media-baja": 0.35, "baja": 0.15, "no determinado": 0.0,
}


def conf_weight(label) -> float:
    return _CONF_WEIGHT.get(str(label or "").strip().lower(), 0.0)


def direction_from_label(label) -> int:
    """+1 for 'alto', -1 for 'bajo', 0 for 'medio'/'no determinado'/unknown."""
    s = str(label or "").strip().lower()
    if s == "alto":
        return 1
    if s == "bajo":
        return -1
    return 0


# ============================================================ profile loading (optional)
def load_card_profiles(path=CARD_PROFILES_JSON):
    """Index the auto card profiles by id/position. ({}, reason) when absent/invalid — the adjuster then
    simply has fewer sources (and may return neutro). NEVER fabricates."""
    p = Path(path)
    empty = {"players": {}, "teams": {}, "positions": {}}
    if not p.exists():
        return empty, "perfiles de tarjetas auto no generados todavía (Fase 4F)"
    try:
        payload = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return empty, "perfiles de tarjetas auto ilegibles"
    players = {}
    for pr in payload.get("players", []) or []:
        pid = pr.get("player_id")
        if pid is not None:
            try:
                players[int(pid)] = pr
            except Exception:
                continue
    teams = {}
    for tr in payload.get("teams", []) or []:
        tid = tr.get("team_id")
        if tid is not None:
            try:
                teams[int(tid)] = tr
            except Exception:
                continue
    positions = {}
    for ps in payload.get("positions", []) or []:
        pos = (ps.get("position") or "").strip().upper()
        if pos:
            positions[pos] = ps
    n = len(players) + len(teams) + len(positions)
    return ({"players": players, "teams": teams, "positions": positions},
            f"perfiles de tarjetas auto cargados ({len(players)} jug / {len(teams)} eq / "
            f"{len(positions)} pos)" if n else "perfiles de tarjetas auto vacíos")


# ============================================================ core adjustment (pure)
def _component(label, confidence, step, weight_factor=1.0):
    """One source's contribution dict + its signed weighted step."""
    direction = direction_from_label(label)
    weight = conf_weight(confidence) * float(weight_factor)
    signed = direction * step * weight
    return {
        "label": label if label is not None else "no determinado",
        "direction": ("subir" if direction > 0 else ("bajar" if direction < 0 else "neutro")),
        "confidence": confidence if confidence is not None else "no determinado",
        "weight": round(weight, 3),
        "step": round(signed, 4),
    }, signed, weight


def adjust_card_risk(probability_card, player_profile=None, position_profile=None,
                     team_profile=None, referee_context=None):
    """Conservatively adjust a base card probability with the auto profiles + referee context.
    Every argument is optional; missing/insufficient sources simply contribute nothing. Returns the
    full §5 result dict. Pure (no I/O, no fabrication)."""
    base = None
    try:
        base = None if probability_card is None else float(probability_card)
    except Exception:
        base = None

    # ----- player history -----
    ph = (player_profile or {})
    ph_comp, ph_signed, ph_w = _component(
        ph.get("card_risk_player_history"), ph.get("confidence"), STEP_PLAYER)

    # ----- position -----
    pos = (position_profile or {})
    pos_comp, pos_signed, pos_w = _component(
        pos.get("card_risk_position"), pos.get("confidence"), STEP_POSITION)

    # ----- team -----
    tm = (team_profile or {})
    tm_comp, tm_signed, tm_w = _component(
        tm.get("card_environment_team"), tm.get("confidence"), STEP_TEAM)

    # ----- referee (down-weight a thin sample HARD) -----
    rc = (referee_context or {})
    ref_matches = rc.get("matches_sample")
    try:
        ref_matches = int(ref_matches) if ref_matches is not None else None
    except Exception:
        ref_matches = None
    ref_factor = REF_THIN_FACTOR if (ref_matches is not None and ref_matches <= REF_THIN_MATCHES) else 1.0
    ref_comp, ref_signed, ref_w = _component(
        rc.get("card_environment"), rc.get("confidence"), STEP_REFEREE, weight_factor=ref_factor)

    components = {
        "player_history": ph_comp, "position_profile": pos_comp,
        "team_profile": tm_comp, "referee_profile": ref_comp,
    }

    total_weight = ph_w + pos_w + tm_w + ref_w
    total_signed = ph_signed + pos_signed + tm_signed + ref_signed
    factor = max(FACTOR_MIN, min(FACTOR_MAX, 1.0 + total_signed))

    insufficient = (base is None) or (total_weight < MIN_TOTAL_WEIGHT)

    # conflict = both an upward and a downward usable contribution present
    ups = [c for c in (ph_comp, pos_comp, tm_comp, ref_comp) if c["step"] > 0]
    downs = [c for c in (ph_comp, pos_comp, tm_comp, ref_comp) if c["step"] < 0]
    conflict = bool(ups) and bool(downs)

    if insufficient:
        adjusted = base
        direction = "neutro"
    else:
        adjusted = max(P_MIN, min(P_MAX, base * factor))
        if factor >= 1.02:
            direction = "subir"
        elif factor <= 0.98:
            direction = "bajar"
        else:
            direction = "neutro"

    reason = _reason(base, direction, components, ref_matches, conflict, insufficient)
    confidence, data_quality = _confidence(total_weight, insufficient)

    return {
        "probability_card_original": round(base, 4) if base is not None else None,
        "probability_card_adjusted": round(adjusted, 4) if adjusted is not None else None,
        "adjustment_direction": direction,
        "adjustment_reason": reason,
        "card_risk_components": components,
        "confidence": confidence,
        "data_quality": data_quality,
    }


def _reason(base, direction, components, ref_matches, conflict, insufficient):
    if base is None:
        return "sin probabilidad base del modelo; no se ajusta"
    if insufficient:
        return "datos de disciplina insuficientes (muestra baja en todas las fuentes); se mantiene el valor original"
    bits = []
    name = {"player_history": "historial jugador", "position_profile": "posición",
            "team_profile": "equipo", "referee_profile": "árbitro"}
    for key, c in components.items():
        if c["step"] != 0:
            arrow = "↑" if c["step"] > 0 else "↓"
            bits.append(f"{name[key]} {c['label']} {arrow}")
    core = "; ".join(bits) if bits else "sin sesgo neto de las fuentes"
    extra = []
    if ref_matches is not None and ref_matches <= REF_THIN_MATCHES:
        extra.append("árbitro con muestra baja (peso reducido)")
    if conflict:
        extra.append("fuentes en conflicto -> ajuste conservador")
    tail = (" · " + "; ".join(extra)) if extra else ""
    verb = {"subir": "sube", "bajar": "baja", "neutro": "neutro"}[direction]
    return f"ajuste {verb}: {core}{tail}"


def _confidence(total_weight, insufficient):
    """Card markets are inherently low-confidence; never overstate. Scales modestly with summed weight."""
    if insufficient:
        return "baja", "baja"
    if total_weight >= 1.2:
        return "media-baja", "media"
    if total_weight >= 0.6:
        return "media-baja", "baja"
    return "baja", "baja"
