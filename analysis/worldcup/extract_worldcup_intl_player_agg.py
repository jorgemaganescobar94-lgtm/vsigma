"""
WORLD CUP 2026 - agregados de stats de JUGADOR por partido internacional -> totales por equipo.
ISOLATED. Coste API = 0 (re-parsea SOLO el sqlite ya cacheado: /fixtures/players). NO market.

Jorge's maximalist decision (2026-07-01): ingerir TODO el dato featurizable. Esto suma los stats
por-jugador (duelos/regates/entradas/intercepciones/pases) a TOTALES por equipo y partido, para
luego construir features rolling point-in-time por selección.

HONESTIDAD DE COBERTURA: los /fixtures/players cacheados son TODOS 2024-2026 (0 en burn-in <2024) y
varios campos (dribbles/tackles) vienen muchas veces None. Se reporta el fill real por campo.

ANTI-LEAKAGE: este script solo AGREGA; las features rolling (en worldcup_full_data_model) usan
únicamente partidos PREVIOS. Salida: worldcup_intl_player_agg.csv (una fila por equipo-partido).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = ROOT / "data" / "cache" / "api_football_cache.sqlite3"
IR = HERE / "international_results.csv"
OUT = HERE / "worldcup_intl_player_agg.csv"

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _n(v):
    try:
        return float(v) if v not in (None, "") else None
    except Exception:
        return None


def build():
    ir = pd.read_csv(IR)
    ir_fids = set(int(x) for x in ir["fixture_id"].dropna().astype(int))
    date_by = dict(zip(ir["fixture_id"].astype(int), ir["date"]))

    conn = sqlite3.connect(CACHE)
    rows = []
    for pj, rj in conn.execute(
            "SELECT params_json,response_json FROM api_cache WHERE path='/fixtures/players'"):
        fid = json.loads(pj).get("fixture")
        if fid is None or int(fid) not in ir_fids:
            continue
        fid = int(fid)
        for tb in (json.loads(rj).get("response") or []):
            tid = (tb.get("team") or {}).get("id")
            if tid is None:
                continue
            agg = defaultdict(float); cnt = defaultdict(int); nplay = 0
            for p in tb.get("players", []) or []:
                st = ((p.get("statistics") or [{}])[0]) or {}
                if not st:
                    continue
                nplay += 1
                du = st.get("duels") or {}; dr = st.get("dribbles") or {}
                tk = st.get("tackles") or {}; pa = st.get("passes") or {}
                for key, val in (("duels_won", du.get("won")), ("duels_total", du.get("total")),
                                 ("dribbles_success", dr.get("success")),
                                 ("tackles_total", tk.get("total")),
                                 ("interceptions", tk.get("interceptions")),
                                 ("passes_total", pa.get("total"))):
                    v = _n(val)
                    if v is not None:
                        agg[key] += v; cnt[key] += 1
            rec = {"fixture_id": fid, "date": str(date_by.get(fid))[:10], "team_id": int(tid),
                   "n_players": nplay}
            for k in ("duels_won", "duels_total", "dribbles_success", "tackles_total",
                      "interceptions", "passes_total"):
                rec[k] = agg[k] if cnt[k] > 0 else None
                rec[f"{k}_nfill"] = cnt[k]
            rows.append(rec)
    conn.close()

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)

    print("=" * 84)
    print("AGREGADOS DE STATS DE JUGADOR POR PARTIDO INTERNACIONAL (totales por equipo) — 0 API")
    print("=" * 84)
    print(f"filas (equipo-partido): {len(df)} | fixtures: {df['fixture_id'].nunique() if len(df) else 0} "
          f"| equipos: {df['team_id'].nunique() if len(df) else 0}")
    if len(df):
        print("\nFILL por campo (equipo-partidos con dato no-nulo):")
        for k in ("duels_won", "duels_total", "dribbles_success", "tackles_total",
                  "interceptions", "passes_total"):
            nn = df[k].notna().sum()
            print(f"  {k:18} {nn:4d}/{len(df)} = {100*nn/len(df):3.0f}%")
    print(f"\nWritten: {OUT}")


if __name__ == "__main__":
    build()
