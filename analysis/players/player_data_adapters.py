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
XA_FILE = EXT_DIR / "player_xa90.csv"
REF_FILE = EXT_DIR / "referee_card_rates.csv"
WEATHER_FILE = EXT_DIR / "weather_by_fixture.csv"


def _read_csv(path) -> Optional[pd.DataFrame]:
    try:
        p = Path(path)
        if not p.exists():
            return None
        df = pd.read_csv(p)
        return df if len(df) else None
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


def adapters_status():
    """Quick presence report for the daily log (which external sources are active)."""
    return {
        "xa90": XA_FILE.exists(),
        "referee_card_rates": REF_FILE.exists(),
        "weather": WEATHER_FILE.exists(),
        "openweather_key_present": bool(os.environ.get("OPENWEATHER_API_KEY")),
    }
