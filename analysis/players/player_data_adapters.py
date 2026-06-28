"""
EXTERNAL-DATA ADAPTERS for the player-events module (pluggable, graceful, NO fabrication, NO secrets).

Fase 1 wires the INTERFACES for the external sources requested (xA/xG real per player, referee
tendency, weather) WITHOUT requiring them: each adapter reads an OPTIONAL local file under
data/external/ (which you provide), or an OPTIONAL env key you add yourself. If the source is not
configured, the adapter returns None + a reason — the core then marks the field data_quality=baja and
emits NO fake number (spec §12).

IMPORTANT (CLAUDE.md): this module NEVER writes .env, never creates secrets, and never calls the
network on its own in Fase 1. To activate a source you drop a file in data/external/ (documented
format below) or set an env var; until then everything degrades cleanly.

Optional files (CSV, header on first row):
  * data/external/player_xa90.csv        -> columns: player_id, xa90 [, key_passes90]
  * data/external/referee_card_rates.csv -> columns: referee, cards_per_match [, pen_per_match]
  * data/external/weather_by_fixture.csv -> columns: fixture_id, condition, temp_c, wind_kmh, rain_mm

Optional env (you set it; we only READ it, never write):
  * OPENWEATHER_API_KEY   (presence only enables a future live weather fetch in Fase 2/3)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EXT_DIR = ROOT / "data" / "external"
# Fase 1/2 files (kept for backward compatibility)
XA_FILE = EXT_DIR / "player_xa90.csv"
REF_FILE = EXT_DIR / "referee_card_rates.csv"
WEATHER_FILE = EXT_DIR / "weather_by_fixture.csv"
# Fase 3 richer contracts (documented in data/external/README.md)
XG_XA_FILE = EXT_DIR / "player_xg_xa.csv"
SET_PIECE_TAKERS_FILE = EXT_DIR / "set_piece_takers.csv"
REFEREE_PROFILES_FILE = EXT_DIR / "referee_profiles.csv"
COACH_PROFILES_FILE = EXT_DIR / "coach_tactical_profiles.csv"
POSITIONAL_PROFILES_FILE = EXT_DIR / "player_positional_profiles.csv"
# weather_by_fixture.csv is shared (Fase 3 simply adds optional richer columns).


def _read_csv(path) -> Optional[pd.DataFrame]:
    try:
        p = Path(path)
        if not p.exists():
            return None
        df = pd.read_csv(p)
        return df if len(df) else None
    except Exception:
        return None


def _missing_cols(df, required):
    """Return the subset of `required` columns not present in df (case-sensitive on the header)."""
    return [c for c in required if c not in df.columns]


def _num(v):
    """float(v) or None — never fabricates a value from a blank/NaN/garbage cell."""
    try:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return None
        return float(v)
    except Exception:
        return None


def _txt(v):
    """Clean string or None (NaN/blank -> None)."""
    try:
        if v is None or (isinstance(v, float) and pd.isna(v)):
            return None
        s = str(v).strip()
        return s or None
    except Exception:
        return None


# ----------------------------------------------------------------- xA / key passes (FBref/Understat/StatsBomb)
def load_xa_rates(path=XA_FILE):
    """{player_id: {'xa90': float, 'key_passes90': float|None}} from data/external/player_xa90.csv,
    or ({}, reason) when absent. The core uses xa90 to enrich likely_assisters; absent -> field None."""
    df = _read_csv(path)
    if df is None or "player_id" not in df.columns or "xa90" not in df.columns:
        return {}, "fuente xA/xG por jugador no configurada (data/external/player_xa90.csv) — Fase 3"
    out = {}
    for _, r in df.iterrows():
        try:
            pid = int(r["player_id"])
            out[pid] = {"xa90": float(r["xa90"]),
                        "key_passes90": (float(r["key_passes90"]) if "key_passes90" in df.columns
                                         and pd.notna(r.get("key_passes90")) else None)}
        except Exception:
            continue
    return out, ("xA por jugador cargada (fuente externa)" if out else "fichero xA vacío/ilegible")


# ----------------------------------------------------------------- referee tendency
def load_referee_tendency(referee_name, path=REF_FILE):
    """{'cards_per_match': float, 'pen_per_match': float|None, 'level': alto/medio/bajo} for the named
    referee, or (None, reason) when absent. NEVER guesses a tendency from a name alone."""
    if not referee_name:
        return None, "árbitro no asignado en el fixture"
    df = _read_csv(path)
    if df is None or "referee" not in df.columns or "cards_per_match" not in df.columns:
        return None, "fuente de árbitros no configurada (data/external/referee_card_rates.csv) — Fase 3"
    row = df[df["referee"].astype(str).str.strip().str.lower() == str(referee_name).strip().lower()]
    if not len(row):
        return None, f"árbitro '{referee_name}' sin registro en la tabla externa"
    cpm = float(row["cards_per_match"].iloc[0])
    level = "alto" if cpm >= 4.5 else ("bajo" if cpm <= 3.0 else "medio")
    pen = (float(row["pen_per_match"].iloc[0]) if "pen_per_match" in df.columns
           and pd.notna(row["pen_per_match"].iloc[0]) else None)
    return {"cards_per_match": cpm, "pen_per_match": pen, "level": level}, "árbitro cargado (fuente externa)"


# ----------------------------------------------------------------- weather
def load_weather(fixture_id, path=WEATHER_FILE):
    """{'condition','temp_c','wind_kmh','rain_mm'} for the fixture, or (None, reason). Reads a local
    file only; live OpenWeather fetch is Fase 2/3 and requires an env key YOU add (we only detect it)."""
    df = _read_csv(path)
    if df is None or "fixture_id" not in df.columns:
        has_key = bool(os.environ.get("OPENWEATHER_API_KEY"))
        tail = " (OPENWEATHER_API_KEY presente: fetch en vivo posible en Fase 2)" if has_key else ""
        return None, "clima no configurado (data/external/weather_by_fixture.csv)" + tail
    try:
        row = df[df["fixture_id"].astype("Int64") == int(fixture_id)]
    except Exception:
        return None, "fixture_id no comparable en el fichero de clima"
    if not len(row):
        return None, "fixture sin registro de clima en la tabla externa"
    r = row.iloc[0]
    return ({"condition": r.get("condition"), "temp_c": r.get("temp_c"),
             "wind_kmh": r.get("wind_kmh"), "rain_mm": r.get("rain_mm")}, "clima cargado (fuente externa)")


# ================================================================= FASE 3 — richer external contracts
# Each loader: file absent -> (None/{}, reason); present but missing minimum columns -> (None/{},
# "fuente inválida: faltan columnas ...") so we mark the source invalid instead of inventing values.

# ----------------------------------------------------------------- A) player_xg_xa.csv (real xG/xA)
XG_XA_MIN_COLS = ["player_id", "xg90", "xa90"]


def load_player_xg_xa(path=XG_XA_FILE):
    """{player_id: {xg90, xa90, shots90, sot90, key_passes90, crosses90, minutes, source, ...}} from
    data/external/player_xg_xa.csv, or ({}, reason). Minimum columns: player_id, xg90, xa90. Optional
    columns degrade to None (never fabricated). Used to REPLACE the per-player goal/assist/shot proxy."""
    df = _read_csv(path)
    if df is None:
        return {}, "xG/xA real por jugador no configurado (data/external/player_xg_xa.csv) — Fase 3"
    miss = _missing_cols(df, XG_XA_MIN_COLS)
    if miss:
        return {}, f"fuente xG/xA inválida: faltan columnas {miss}"
    out = {}
    for _, r in df.iterrows():
        try:
            pid = int(r["player_id"])
        except Exception:
            continue
        out[pid] = {
            "xg90": _num(r.get("xg90")), "xa90": _num(r.get("xa90")),
            "shots90": _num(r.get("shots90")), "sot90": _num(r.get("sot90")),
            "key_passes90": _num(r.get("key_passes90")), "crosses90": _num(r.get("crosses90")),
            "minutes": _num(r.get("minutes")), "season": _txt(r.get("season")),
            "competition": _txt(r.get("competition")), "source": _txt(r.get("source")),
            "data_quality": _txt(r.get("data_quality")), "confidence": _txt(r.get("confidence")),
        }
    return out, (f"xG/xA real cargado para {len(out)} jugadores (fuente externa)" if out
                 else "fichero xG/xA vacío/ilegible")


# ----------------------------------------------------------------- B) set_piece_takers.csv (roles/rank)
SET_PIECE_TAKERS_MIN_COLS = ["team_id", "player_id", "role"]
SET_PIECE_ROLES = {"penalty", "direct_free_kick", "corner_left", "corner_right", "indirect_free_kick"}


def load_set_piece_takers(path=SET_PIECE_TAKERS_FILE):
    """{team_id: {role: [ {player_id, player_name, rank, attempts, last_taken_date, confidence}... ]}}
    ordered by rank (then attempts desc). Only known roles are kept. Absent/invalid -> ({}, reason).
    This is source-priority #2 (after real WC events) for set-piece takers — never fabricated."""
    df = _read_csv(path)
    if df is None:
        return {}, "lanzadores de balón parado no configurados (data/external/set_piece_takers.csv) — Fase 3"
    miss = _missing_cols(df, SET_PIECE_TAKERS_MIN_COLS)
    if miss:
        return {}, f"fuente set-piece inválida: faltan columnas {miss}"
    out: dict = {}
    for _, r in df.iterrows():
        try:
            tid = int(r["team_id"]); pid = int(r["player_id"])
        except Exception:
            continue
        role = (_txt(r.get("role")) or "").lower()
        if role not in SET_PIECE_ROLES:
            continue
        entry = {
            "player_id": pid, "player_name": _txt(r.get("player_name")),
            "rank": _num(r.get("rank")), "attempts": _num(r.get("attempts")),
            "last_taken_date": _txt(r.get("last_taken_date")),
            "source": _txt(r.get("source")),
            "confidence": _txt(r.get("confidence")) or "media",
        }
        out.setdefault(tid, {}).setdefault(role, []).append(entry)
    # order each role by rank asc (1 = primary), missing rank last; tiebreak attempts desc
    for tid, roles in out.items():
        for role, lst in roles.items():
            lst.sort(key=lambda e: (e["rank"] if e["rank"] is not None else 1e9,
                                    -(e["attempts"] or 0.0)))
    return out, (f"lanzadores de balón parado cargados para {len(out)} equipos (fuente externa)" if out
                 else "fichero set-piece vacío/sin roles válidos")


# ----------------------------------------------------------------- C) referee_profiles.csv
REFEREE_PROFILES_MIN_COLS = ["referee_name", "yellow_cards_pg"]


def load_referee_profiles(path=REFEREE_PROFILES_FILE):
    """{referee_name_lower: {referee_name, matches, yellow_cards_pg, red_cards_pg, fouls_pg,
    penalties_pg, home_cards_pg, away_cards_pg, tournament_context, source, confidence}}, or
    ({}, reason). Minimum columns: referee_name, yellow_cards_pg. Never guesses from a name."""
    df = _read_csv(path)
    if df is None:
        return {}, "perfiles de árbitro no configurados (data/external/referee_profiles.csv) — Fase 3"
    miss = _missing_cols(df, REFEREE_PROFILES_MIN_COLS)
    if miss:
        return {}, f"fuente de árbitros inválida: faltan columnas {miss}"
    out = {}
    for _, r in df.iterrows():
        name = _txt(r.get("referee_name"))
        if not name:
            continue
        out[name.lower()] = {
            "referee_name": name, "matches": _num(r.get("matches")),
            "yellow_cards_pg": _num(r.get("yellow_cards_pg")), "red_cards_pg": _num(r.get("red_cards_pg")),
            "fouls_pg": _num(r.get("fouls_pg")), "penalties_pg": _num(r.get("penalties_pg")),
            "home_cards_pg": _num(r.get("home_cards_pg")), "away_cards_pg": _num(r.get("away_cards_pg")),
            "tournament_context": _txt(r.get("tournament_context")), "source": _txt(r.get("source")),
            "data_quality": _txt(r.get("data_quality")), "confidence": _txt(r.get("confidence")),
        }
    return out, (f"perfiles de árbitro cargados ({len(out)}) (fuente externa)" if out
                 else "fichero de árbitros vacío/ilegible")


# ----------------------------------------------------------------- D) weather_by_fixture.csv (richer)
def load_weather_by_fixture(path=WEATHER_FILE):
    """{fixture_id: {venue, kickoff_time, temperature, humidity, wind_speed, rain_probability,
    pitch_condition, source, confidence}}, or ({}, reason). Accepts BOTH the Fase 3 schema and the
    legacy Fase 2 schema (condition/temp_c/wind_kmh/rain_mm) -> mapped. Minimum: fixture_id."""
    df = _read_csv(path)
    if df is None:
        return {}, "clima por partido no configurado (data/external/weather_by_fixture.csv) — Fase 3"
    if "fixture_id" not in df.columns:
        return {}, "fuente de clima inválida: falta columna fixture_id"
    out = {}
    for _, r in df.iterrows():
        try:
            fid = int(r["fixture_id"])
        except Exception:
            continue
        # Fase 3 columns first, fall back to legacy names so an old file still activates.
        out[fid] = {
            "venue": _txt(r.get("venue")),
            "kickoff_time": _txt(r.get("kickoff_time")),
            "temperature": _num(r.get("temperature")) if "temperature" in df.columns else _num(r.get("temp_c")),
            "humidity": _num(r.get("humidity")),
            "wind_speed": _num(r.get("wind_speed")) if "wind_speed" in df.columns else _num(r.get("wind_kmh")),
            "rain_probability": _num(r.get("rain_probability")),
            "rain_mm": _num(r.get("rain_mm")),
            "pitch_condition": (_txt(r.get("pitch_condition")) if "pitch_condition" in df.columns
                                else _txt(r.get("condition"))),
            "condition": _txt(r.get("condition")),
            "source": _txt(r.get("source")),
            "data_quality": _txt(r.get("data_quality")), "confidence": _txt(r.get("confidence")),
        }
    return out, (f"clima cargado para {len(out)} partidos (fuente externa)" if out
                 else "fichero de clima vacío/ilegible")


# ----------------------------------------------------------------- E) coach_tactical_profiles.csv
COACH_PROFILES_MIN_COLS = ["team_id", "coach_name"]


def load_coach_profiles(path=COACH_PROFILES_FILE):
    """{team_id: {coach_name, base_formation, pressing_level, defensive_block, build_up_style,
    transition_speed, width_usage, set_piece_emphasis, substitution_aggression, knockout_risk_profile,
    source, confidence}}, or ({}, reason). Qualitative profile — NO hard percentages are derived."""
    df = _read_csv(path)
    if df is None:
        return {}, "perfiles tácticos del seleccionador no configurados " \
                   "(data/external/coach_tactical_profiles.csv) — Fase 3"
    miss = _missing_cols(df, COACH_PROFILES_MIN_COLS)
    if miss:
        return {}, f"fuente de perfiles de entrenador inválida: faltan columnas {miss}"
    fields = ["coach_name", "base_formation", "pressing_level", "defensive_block", "build_up_style",
              "transition_speed", "width_usage", "set_piece_emphasis", "substitution_aggression",
              "knockout_risk_profile", "team_name", "source", "data_quality", "confidence"]
    out = {}
    for _, r in df.iterrows():
        try:
            tid = int(r["team_id"])
        except Exception:
            continue
        out[tid] = {f: _txt(r.get(f)) for f in fields}
    return out, (f"perfiles tácticos cargados para {len(out)} equipos (fuente externa)" if out
                 else "fichero de perfiles de entrenador vacío/ilegible")


# ----------------------------------------------------------------- F) player_positional_profiles.csv
POSITIONAL_PROFILES_MIN_COLS = ["player_id", "position"]
_POS_NUM_FIELDS = ["attacking_weight", "defensive_weight", "aerial_threat", "pace_threat",
                   "1v1_threat", "crossing_threat"]


def load_positional_profiles(path=POSITIONAL_PROFILES_FILE):
    """{player_id: {position, role, preferred_zone, attacking_weight, defensive_weight, aerial_threat,
    pace_threat, 1v1_threat, crossing_threat, card_risk_role, team_id, source, confidence}}, or
    ({}, reason). Numeric *_threat/_weight fields parsed as floats (None if blank) — feed matchups."""
    df = _read_csv(path)
    if df is None:
        return {}, "perfiles posicionales no configurados " \
                   "(data/external/player_positional_profiles.csv) — Fase 3"
    miss = _missing_cols(df, POSITIONAL_PROFILES_MIN_COLS)
    if miss:
        return {}, f"fuente de perfiles posicionales inválida: faltan columnas {miss}"
    out = {}
    for _, r in df.iterrows():
        try:
            pid = int(r["player_id"])
        except Exception:
            continue
        d = {
            "player_name": _txt(r.get("player_name")), "team_id": _num(r.get("team_id")),
            "position": _txt(r.get("position")), "role": _txt(r.get("role")),
            "preferred_zone": _txt(r.get("preferred_zone")),
            "card_risk_role": _txt(r.get("card_risk_role")), "source": _txt(r.get("source")),
            "data_quality": _txt(r.get("data_quality")), "confidence": _txt(r.get("confidence")),
        }
        for f in _POS_NUM_FIELDS:
            d[f] = _num(r.get(f))
        out[pid] = d
    return out, (f"perfiles posicionales cargados para {len(out)} jugadores (fuente externa)" if out
                 else "fichero de perfiles posicionales vacío/ilegible")


def adapters_status():
    """Quick presence report for the daily log (which external sources are active). Fase 1/2 + Fase 3."""
    return {
        # Fase 1/2
        "xa90": XA_FILE.exists(),
        "referee_card_rates": REF_FILE.exists(),
        "weather": WEATHER_FILE.exists(),
        "openweather_key_present": bool(os.environ.get("OPENWEATHER_API_KEY")),
        # Fase 3
        "xg_xa": XG_XA_FILE.exists(),
        "set_piece_takers": SET_PIECE_TAKERS_FILE.exists(),
        "referee_profiles": REFEREE_PROFILES_FILE.exists(),
        "coach_profiles": COACH_PROFILES_FILE.exists(),
        "positional_profiles": POSITIONAL_PROFILES_FILE.exists(),
    }


def external_data_status():
    """The §9 `external_data_status` block for the JSON: which Fase 3 sources are active right now."""
    return {
        "xg_xa_available": XG_XA_FILE.exists(),
        "set_piece_available": SET_PIECE_TAKERS_FILE.exists(),
        "referee_available": REFEREE_PROFILES_FILE.exists(),
        "weather_available": WEATHER_FILE.exists(),
        "coach_profile_available": COACH_PROFILES_FILE.exists(),
        "positional_profile_available": POSITIONAL_PROFILES_FILE.exists(),
    }
