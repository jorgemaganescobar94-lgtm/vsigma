"""
WORLD CUP 2026 - CLUB-FORM de selección desde la forma de club de sus jugadores (ISOLATED).

Jorge's explicit decision (2026-07-01). Feature = fuerza de selección derivada del rendimiento
de CLUB (temporada 2025, ya COMPLETADA antes del Mundial jun-2026 -> anti-leakage seguro EN VIVO)
de los jugadores de las 48 plantillas, NORMALIZADO por fuerza de liga (tier 0..1). NO market.

COSTE API = 0: re-parsea SOLO el sqlite ya cacheado (/players?id&season=2025, 100% cobertura de
las 48 plantillas). Store-guarded/idempotente. Ningún endpoint de apuesta.

PASO 1 (por jugador): de la MISMA carga cacheada, elige la liga DOMÉSTICA principal (excluye copas/
amistosos/selección) y extrae minutos, apps, rating, goles, asistencias, liga -> tier de liga.
PASO 2 (por selección): media ponderada por MINUTOS (proxy de titularidad) de
    * rating de club normalizado por tier   (cf_rating)
    * (goles+asistencias)/90 normalizado por tier (cf_ga90)
  composite club_form = cf_rating + 2.0*cf_ga90. Jugador sin datos de club -> excluido y marcado.

ANTI-LEAKAGE: SOLO temporada 2025 (pre-Mundial). NUNCA datos del propio torneo.

Salidas (git-add explícito): worldcup_club_form_raw.csv (jugador) + worldcup_club_form.csv (selección).
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = ROOT / "data" / "cache" / "api_football_cache.sqlite3"
ROSTER = HERE / "squad_quality_raw_48.csv"       # player_id -> team/team_id (48 squads)
RAW_OUT = HERE / "worldcup_club_form_raw.csv"
TEAM_OUT = HERE / "worldcup_club_form.csv"
SEASON = 2025

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# competitions that are NOT a domestic club league (mirror of extract_squad_quality_48.EXCLUDE_KW)
EXCLUDE_KW = ["friendl", "uefa", "conmebol", "concacaf", " afc", "caf ", "fifa", "cup", "copa",
              "qualification", "nations", "trophy", "playoff", "community", "recopa",
              "libertadores", "sudamericana", "world", "olympic", "leagues cup"]

# league-strength tier 0..1 — faithful copy of squad_strength_model.tier (kept local to avoid an
# import side-effect). Documented proxy: 1.00 top-5 EU / 0.80 strong-EU / 0.60 mid / 0.45-0.50 low.
TIER1 = {("england", "premier league"), ("spain", "la liga"), ("italy", "serie a"),
         ("germany", "bundesliga"), ("france", "ligue 1")}
STRONG_EU = {"portugal", "netherlands", "belgium", "turkey", "austria", "switzerland",
             "scotland", "greece", "russia", "ukraine", "saudi-arabia", "saudi arabia"}
MID = {"usa", "mexico", "brazil", "argentina", "japan", "south-korea", "south korea",
       "denmark", "norway", "sweden", "poland", "czech-republic", "czechia", "croatia",
       "serbia", "qatar", "united-arab-emirates", "uae", "colombia", "egypt", "usa "}


def tier(country, league):
    co = str(country or "").strip().lower(); lg = str(league or "").strip().lower()
    if (co, lg) in TIER1:
        return 1.00
    if co == "england" and "championship" in lg:
        return 0.80
    if co in STRONG_EU:
        return 0.80
    if co in MID:
        return 0.60
    if lg and lg != "nan":
        if any(k in lg for k in ("2", "segunda", "serie b", "championship", "liga ii")):
            return 0.45
        return 0.50
    return 0.30


def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except Exception:
        return None


def pick_domestic(stats):
    """Primary domestic-league block: most appearances/minutes among non-cup/non-national comps."""
    cand = []
    for r in stats or []:
        lg = r.get("league") or {}
        name = str(lg.get("name") or "").lower()
        if not name or any(k in name for k in EXCLUDE_KW):
            continue
        g = r.get("games") or {}
        goals = r.get("goals") or {}
        cand.append({
            "apps": g.get("appearences") or 0, "minutes": g.get("minutes") or 0,
            "rating": _num(g.get("rating")),
            "goals": goals.get("total") or 0, "assists": goals.get("assists") or 0,
            "club": (r.get("team") or {}).get("name"),
            "league_country": lg.get("country"), "league_name": lg.get("name"),
        })
    if not cand:
        return None
    cand.sort(key=lambda x: (x["apps"], x["minutes"]), reverse=True)
    return cand[0]


def load_cached_players():
    """(player_id, season) -> statistics list, from the sqlite cache ONLY (0 API)."""
    out = {}
    if not CACHE.exists():
        return out
    conn = sqlite3.connect(CACHE)
    try:
        for pj, rj in conn.execute(
                "SELECT params_json,response_json FROM api_cache WHERE path='/players'"):
            p = json.loads(pj)
            if p.get("season") != SEASON or p.get("id") is None:
                continue
            resp = json.loads(rj).get("response") or []
            if resp:
                out[int(p["id"])] = resp[0].get("statistics") or []
    finally:
        conn.close()
    return out


def build():
    roster = pd.read_csv(ROSTER)
    players = load_cached_players()
    rows = []
    for r in roster.itertuples(index=False):
        pid = int(r.player_id)
        dom = pick_domestic(players.get(pid))
        rec = {"team": r.team, "team_id": int(r.team_id), "player_id": pid,
               "player_name": getattr(r, "player_name", None), "has_club": dom is not None}
        if dom:
            mins = float(dom["minutes"] or 0)
            ga = float(dom["goals"] or 0) + float(dom["assists"] or 0)
            ga90 = (ga * 90.0 / mins) if mins >= 180 else None   # need ~2 full matches for a rate
            rec.update({
                "club": dom["club"], "league_country": dom["league_country"],
                "league_name": dom["league_name"], "apps": dom["apps"], "minutes": mins,
                "rating": dom["rating"], "goals": dom["goals"], "assists": dom["assists"],
                "ga90": (round(ga90, 3) if ga90 is not None else None),
                "tier": tier(dom["league_country"], dom["league_name"])})
        rows.append(rec)
    raw = pd.DataFrame(rows)
    raw.to_csv(RAW_OUT, index=False)

    # ---- PASO 2: aggregate per selección (minutes-weighted, tier-normalized) ----
    team_rows = []
    for tid, g in raw.groupby("team_id"):
        withclub = g[g["has_club"]].copy()
        n = len(g); nc = len(withclub)
        rat = withclub.dropna(subset=["rating", "minutes"])
        ga = withclub.dropna(subset=["ga90", "minutes"])
        # weights = minutes (proxy titularidad); tier-normalized performance
        def wmean(sub, col):
            w = sub["minutes"].to_numpy(float)
            if w.sum() <= 0:
                return None
            return float(np.average((sub["tier"] * sub[col]).to_numpy(float), weights=w))
        cf_rating = wmean(rat, "rating") if len(rat) else None
        cf_ga90 = wmean(ga, "ga90") if len(ga) else None
        club_form = None
        if cf_rating is not None:
            club_form = cf_rating + 2.0 * (cf_ga90 or 0.0)
        team_rows.append({
            "team": g["team"].iloc[0], "team_id": int(tid),
            "club_form": (round(club_form, 3) if club_form is not None else None),
            "cf_rating": (round(cf_rating, 3) if cf_rating is not None else None),
            "cf_ga90": (round(cf_ga90, 3) if cf_ga90 is not None else None),
            "mean_tier": round(float(np.average(withclub["tier"], weights=withclub["minutes"].clip(lower=1)))
                               if nc else 0.0, 3),
            "n_players": n, "n_with_club": nc, "coverage": round(nc / max(n, 1), 3)})
    team = pd.DataFrame(team_rows).sort_values("club_form", ascending=False, na_position="last")
    team.to_csv(TEAM_OUT, index=False)

    # ---- report ----
    print("=" * 90)
    print(f"CLUB-FORM por selección (temporada de club {SEASON}, pre-Mundial; normalizado por tier de liga)")
    print("=" * 90)
    print(f"jugadores en roster: {len(raw)} | con datos de club: {int(raw['has_club'].sum())} "
          f"({100*raw['has_club'].mean():.0f}%) | selecciones: {team['team_id'].nunique()}")
    print(f"club_form = cf_rating(tier-normalizado) + 2.0*cf_ga90(tier-normalizado). API calls: 0 (cache).")
    print("\nTOP 12 y BOTTOM 6 por club_form:")
    show = ["team", "club_form", "cf_rating", "cf_ga90", "mean_tier", "n_with_club", "coverage"]
    print(team[show].head(12).to_string(index=False))
    print("  ...")
    print(team[show].tail(6).to_string(index=False))
    print(f"\nWritten: {RAW_OUT}\nWritten: {TEAM_OUT}")


if __name__ == "__main__":
    build()
