"""
WORLD CUP 2026 — REFEREE CONTEXT (Fase 3). READ-ONLY · NO API · NO market/odds · NO betting.

Reads data/external/referee_profiles.csv (via the player-data adapter) and, IF a fixture carries a
referee name, produces an honest qualitative read of the expected CARD environment and a possible
PENALTY environment. It ONLY shades the explanation / the card RANGE — it never invents a tendency,
never fabricates a number, and never touches the 1X2 / goals / props prediction.

Linking: the WC card CSV does not carry the referee. The build script resolves a referee name from
(1) an optional data/external/fixture_referees.csv map, or (2) the cached fixture meta if present.
Absent referee or absent profile -> confidence baja + reason (spec §5, §12).

Output dict (spec §5):
  {referee_name, expected_card_environment, possible_penalty_environment, confidence, reason,
   yellow_cards_pg, red_cards_pg, penalties_pg, data_quality, sample}
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402

# sample floors for an honest confidence ladder (matches needed before we trust the rate)
MIN_SAMPLE_HIGH = 25
MIN_SAMPLE_MED = 10

# tournament-aware thresholds (yellow cards/game). WC/knockout football tends to be a touch tighter
# than busy domestic leagues; thresholds are conservative and only label the ENVIRONMENT, not a number.
CARD_HIGH = 4.5
CARD_LOW = 3.0
PEN_HIGH = 0.30
PEN_LOW = 0.12


def _unassigned(reason):
    return {"referee_name": None, "expected_card_environment": "no determinado",
            "possible_penalty_environment": "no determinado", "confidence": "baja",
            "data_quality": "baja", "sample": None, "yellow_cards_pg": None, "red_cards_pg": None,
            "penalties_pg": None, "reason": reason}


def build_referee_context(referee_name, profiles=None, profiles_reason=None):
    """referee_name: resolved name (or None). profiles: {name_lower: profile} from the adapter (loaded
    once by the caller); if None we load it here. Returns the §5 structure, degrading honestly."""
    if profiles is None:
        profiles, profiles_reason = adapters.load_referee_profiles()
    if not referee_name:
        return _unassigned("árbitro no asignado al fixture (sin nombre de árbitro disponible)")
    if not profiles:
        return _unassigned(profiles_reason or "perfiles de árbitro no configurados — Fase 3")
    prof = profiles.get(str(referee_name).strip().lower())
    if not prof:
        return _unassigned(f"árbitro '{referee_name}' sin registro en la tabla externa")

    sample = prof.get("matches")
    yc = prof.get("yellow_cards_pg")
    rc = prof.get("red_cards_pg")
    pen = prof.get("penalties_pg")

    # confidence from sample size (honest: a thin sample can't assert a tendency)
    if sample is None:
        conf, dq = "baja", "baja"
        sample_note = "muestra de partidos no indicada"
    elif sample >= MIN_SAMPLE_HIGH:
        conf, dq = "media", "alta"
        sample_note = f"{int(sample)} partidos"
    elif sample >= MIN_SAMPLE_MED:
        conf, dq = "baja", "media"
        sample_note = f"muestra moderada ({int(sample)} partidos) — orientativo"
    else:
        conf, dq = "baja", "baja"
        sample_note = f"muestra pequeña ({int(sample)} partidos) — no concluyente"

    # card environment (only if we actually have the yellow rate)
    if yc is None:
        card_env = "no determinado"
    elif sample is not None and sample < MIN_SAMPLE_MED:
        card_env = "indeterminado (muestra insuficiente)"
    elif yc >= CARD_HIGH:
        card_env = "alto (árbitro de tarjeta fácil; rango de tarjetas algo más alto)"
    elif yc <= CARD_LOW:
        card_env = "bajo (árbitro permisivo; rango de tarjetas algo más bajo)"
    else:
        card_env = "medio (sin sesgo claro respecto a la media)"

    # penalty environment (very soft — penalties are rare and noisy)
    if pen is None:
        pen_env = "no determinado (sin tasa de penaltis)"
    elif sample is not None and sample < MIN_SAMPLE_HIGH:
        pen_env = "indeterminado (penaltis son raros; muestra insuficiente para asegurar tendencia)"
    elif pen >= PEN_HIGH:
        pen_env = "ligeramente más propenso a señalar penalti (orientativo)"
    elif pen <= PEN_LOW:
        pen_env = "ligeramente menos propenso a señalar penalti (orientativo)"
    else:
        pen_env = "en la media"

    ctx = prof.get("tournament_context")
    reason = f"perfil externo; {sample_note}" + (f"; contexto: {ctx}" if ctx else "")
    if prof.get("confidence"):
        reason += f"; confianza de fuente: {prof['confidence']}"

    return {
        "referee_name": prof.get("referee_name") or referee_name,
        "expected_card_environment": card_env,
        "possible_penalty_environment": pen_env,
        "confidence": conf,
        "data_quality": dq,
        "sample": int(sample) if sample is not None else None,
        "yellow_cards_pg": yc, "red_cards_pg": rc, "penalties_pg": pen,
        "reason": reason,
    }
