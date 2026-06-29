"""
WORLD CUP 2026 — REFEREE CONTEXT (Fase 3 + Fase 4E). READ-ONLY · NO API · NO market/odds · NO betting.

Reads a referee profile and produces an honest qualitative read of the expected CARD environment and a
possible PENALTY environment. It ONLY shades the explanation / the card RANGE — it never invents a
tendency, never fabricates a number, never touches the 1X2 / goals / props prediction.

Profile source priority (Fase 4E §4):
  1. data/external/referee_profiles.csv  (MANUAL, via the player-data adapter) — wins if it has the ref.
  2. analysis/worldcup/worldcup_referee_profiles_auto.csv  (AUTO, derived from REAL World Cup events) —
     used as a fallback, always tagged source=worldcup_events_auto.
  3. neither -> "no determinado" + honest reason.

A thin auto sample (e.g. 1 match) is surfaced with low confidence and a "do not extrapolate" reason; a
hard percentage is never presented as reliable on a tiny sample.

Output dict (spec §5, extended in 4E with profile_source / matches_sample / card_environment):
  {referee_name, profile_source, matches_sample, card_environment, expected_card_environment,
   possible_penalty_environment, confidence, reason, yellow_cards_pg, red_cards_pg, penalties_pg,
   data_quality, sample}
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "analysis" / "players"))

import player_data_adapters as adapters  # noqa: E402

AUTO_PROFILES_FILE = HERE / "worldcup_referee_profiles_auto.csv"

# sample floors for an honest confidence ladder on the MANUAL profile (matches before we trust the rate)
MIN_SAMPLE_HIGH = 25
MIN_SAMPLE_MED = 10

# tournament-aware thresholds (yellow cards/game) for the MANUAL profile's qualitative label.
CARD_HIGH = 4.5
CARD_LOW = 3.0
PEN_HIGH = 0.30
PEN_LOW = 0.12


def _unassigned(reason):
    return {"referee_name": None, "profile_source": None, "matches_sample": None,
            "card_environment": "no determinado", "expected_card_environment": "no determinado",
            "possible_penalty_environment": "no determinado", "confidence": "baja",
            "data_quality": "baja", "sample": None, "yellow_cards_pg": None, "red_cards_pg": None,
            "penalties_pg": None, "reason": reason}


# ============================================================ auto-profile loader (Fase 4E)
def load_auto_referee_profiles(path=AUTO_PROFILES_FILE):
    """{referee_name_lower: profile} from worldcup_referee_profiles_auto.csv. ({}, reason) if absent."""
    p = Path(path)
    if not p.exists():
        return {}, "perfiles de árbitro auto no generados todavía (Fase 4E)"
    try:
        df = pd.read_csv(p)
    except Exception:
        return {}, "perfiles de árbitro auto ilegibles"
    if "referee_name" not in df.columns or len(df) == 0:
        return {}, "perfiles de árbitro auto vacíos"
    out = {}
    for _, r in df.iterrows():
        name = str(r.get("referee_name") or "").strip()
        if not name:
            continue
        out[name.lower()] = {k: (None if pd.isna(r.get(k)) else r.get(k)) for k in df.columns}
    return out, f"perfiles de árbitro auto cargados ({len(out)}) — eventos reales del Mundial"


# ============================================================ manual profile -> context (Fase 3)
def _from_manual(prof, referee_name):
    sample = prof.get("matches")
    yc = prof.get("yellow_cards_pg")
    rc = prof.get("red_cards_pg")
    pen = prof.get("penalties_pg")

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

    if yc is None:
        card_label, card_env = "no determinado", "no determinado"
    elif sample is not None and sample < MIN_SAMPLE_MED:
        card_label, card_env = "no determinado", "indeterminado (muestra insuficiente)"
    elif yc >= CARD_HIGH:
        card_label, card_env = "alto", "alto (árbitro de tarjeta fácil; rango de tarjetas algo más alto)"
    elif yc <= CARD_LOW:
        card_label, card_env = "bajo", "bajo (árbitro permisivo; rango de tarjetas algo más bajo)"
    else:
        card_label, card_env = "medio", "medio (sin sesgo claro respecto a la media)"

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
        "profile_source": prof.get("source") or "manual",
        "matches_sample": int(sample) if sample is not None else None,
        "card_environment": card_label,
        "expected_card_environment": card_env,
        "possible_penalty_environment": pen_env,
        "confidence": conf,
        "data_quality": dq,
        "sample": int(sample) if sample is not None else None,
        "yellow_cards_pg": yc, "red_cards_pg": rc, "penalties_pg": pen,
        "reason": reason,
    }


# ============================================================ auto profile -> context (Fase 4E)
def _num(v):
    try:
        return None if v is None or (isinstance(v, float) and pd.isna(v)) else float(v)
    except Exception:
        return None


def _from_auto(prof, referee_name):
    matches = prof.get("matches")
    matches = int(matches) if matches is not None and str(matches).strip() != "" else 0
    card_label = str(prof.get("card_environment") or "no determinado")
    pen_label = str(prof.get("penalty_environment") or "no determinado")

    if card_label == "no determinado":
        card_env = "no determinado (muestra insuficiente)"
    else:
        tail = "muestra mínima — no extrapolar" if matches <= 1 else (
            "muestra reducida" if matches <= 3 else "muestra real")
        card_env = f"{card_label} ({matches} partido(s) Mundial auto; {tail})"

    if pen_label == "no determinado":
        pen_env = "no determinado (muestra insuficiente para penaltis)"
    else:
        pen_env = f"{pen_label} (orientativo; {matches} partidos, Mundial auto)"

    reason = (str(prof.get("reason") or "")).strip()
    reason = (reason + "; " if reason else "") + "fuente: Mundial auto (eventos reales)"

    return {
        "referee_name": prof.get("referee_name") or referee_name,
        "profile_source": "worldcup_events_auto",
        "matches_sample": matches,
        "card_environment": card_label,
        "expected_card_environment": card_env,
        "possible_penalty_environment": pen_env,
        "confidence": str(prof.get("confidence") or "baja"),
        "data_quality": str(prof.get("data_quality") or "baja"),
        "sample": matches,
        "yellow_cards_pg": _num(prof.get("yellow_cards_pg")),
        "red_cards_pg": _num(prof.get("red_cards_pg")),
        "penalties_pg": _num(prof.get("penalties_pg")),
        "reason": reason,
    }


# ============================================================ public entry
def build_referee_context(referee_name, profiles=None, profiles_reason=None,
                          auto_profiles=None, auto_reason=None):
    """Resolve a referee context, MANUAL first then AUTO (Fase 4E §4). profiles/auto_profiles are the
    name->profile maps (loaded once by the caller); None -> load here. Degrades honestly to 'no
    determinado' with a reason when nothing is available."""
    if profiles is None:
        profiles, profiles_reason = adapters.load_referee_profiles()
    if not referee_name:
        return _unassigned("árbitro no asignado al fixture (sin nombre de árbitro disponible)")

    key = str(referee_name).strip().lower()
    # 1) MANUAL profile wins
    prof = (profiles or {}).get(key)
    if prof:
        return _from_manual(prof, referee_name)

    # 2) AUTO fallback (real World Cup events)
    if auto_profiles is None:
        auto_profiles, auto_reason = load_auto_referee_profiles()
    auto = (auto_profiles or {}).get(key)
    if auto:
        return _from_auto(auto, referee_name)

    # 3) nothing available
    if not profiles and not auto_profiles:
        return _unassigned(profiles_reason or "perfiles de árbitro no configurados")
    return _unassigned(f"árbitro '{referee_name}' sin registro (ni manual ni auto)")
