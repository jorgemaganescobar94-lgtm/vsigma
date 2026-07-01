"""
WORLD CUP 2026 - CLUB-FORM MULTI-TEMPORADA (2025/2024/2023) de los jugadores de las 48 plantillas.
ISOLATED. NO market. Jorge's explicit decision (2026-07-01), consciente del coste y de la redundancia.

PASO 0 (guard de cuota OBLIGATORIO): lee /status; si REMAINING < MIN_REMAINING -> ABORTA sin gastar.
PASO 1: /players?id=X&season={2024,2023} para los ~1248 jugadores (2025 ya cacheado). STORE-GUARDED
        (cache forever: jugador-temporada ya presente -> 0 calls), rate-limit (min_interval del cliente)
        + backoff, QUOTA-STOP (para si queda poco margen), RESUMIBLE (re-run continúa). Reporta calls REALES.
PASO 2: club_form multi-temporada = media ponderada por RECENCIA (2025>2024>2023) y minutos del
        rendimiento de club (rating + goles+asist/90), normalizado por tier de liga. Anti-leakage EN
        VIVO (todas las temporadas < Mundial 2026); 2023 cae en burn-in -> feature ENTRENABLE.

Salida: worldcup_club_form_multiseason.csv (per selección). Cero endpoints de apuesta.
"""
from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))
from api_football_client import APIFootballClient, APIFootballError  # noqa: E402
from extract_worldcup_club_form import tier, pick_domestic  # noqa: E402 (reuse; no import side-effects)

ROSTER = HERE / "squad_quality_raw_48.csv"
OUT = HERE / "worldcup_club_form_multiseason.csv"
SEASONS = [2024, 2023]                 # 2025 already cached; these are the fresh ones
RECENCY = {2025: 1.0, 2024: 0.6, 2023: 0.36}   # recency weights (decay ~0.6/season)
TTL_FOREVER = 24 * 3650                # a past completed season never changes
MIN_REMAINING = 3000                   # PASO 0 guard: need at least this free to start
QUOTA_STOP = 500                       # stop mid-run if remaining falls below this (headroom)


def quota(c):
    try:
        req = ((c.request("/status", None, ttl_hours=0, force_refresh=True).get("response", {}) or {})
               .get("requests") or {})
        return req.get("current"), req.get("limit_day")
    except Exception:
        return None, None


def fetch_players(c, max_fresh):
    roster = pd.read_csv(ROSTER)
    pids = [int(x) for x in roster["player_id"].dropna().astype(int).unique()]
    cur0, lim = quota(c)
    print(f"PASO 0 guard: quota current={cur0}/{lim} -> remaining={None if lim is None else lim-cur0}")
    if cur0 is None or lim is None:
        print("ABORT: no pude leer la cuota."); return None
    remaining = lim - cur0
    if remaining < MIN_REMAINING:
        print(f"ABORT: remaining {remaining} < MIN_REMAINING {MIN_REMAINING}. NO empiezo.")
        return None
    print(f"PASO 1: {len(pids)} jugadores x seasons {SEASONS} (store-guarded). start_current={cur0}")

    fresh = 0
    stop = None
    for s in SEASONS:
        for i, pid in enumerate(pids):
            if fresh >= max_fresh:
                stop = f"MAX_FRESH cap {max_fresh}"; break
            for attempt in range(4):
                try:
                    c.request("/players", {"id": pid, "season": s}, ttl_hours=TTL_FOREVER)
                    break
                except APIFootballError as e:
                    if getattr(e, "is_plan_limit", False):
                        stop = f"PLAN/LIMIT: {e}"; break
                    time.sleep(1.0 * (attempt + 1))
                except Exception:
                    time.sleep(1.0 * (attempt + 1))
            if stop and "PLAN" in stop:
                break
            if (i % 120) == 0:
                cur, lim = quota(c)
                if cur is not None and lim is not None:
                    fresh = cur - cur0
                    if (lim - cur) < QUOTA_STOP:
                        stop = f"QUOTA_STOP: remaining {lim-cur} < {QUOTA_STOP}"; break
        if stop:
            break
    cur1, lim = quota(c)
    real = (cur1 - cur0) if (cur1 is not None and cur0 is not None) else "n/a"
    print(f"PASO 1 done. stop={stop or 'completado'} | REAL calls spent={real} | "
          f"quota now={cur1}/{lim} (remaining {None if lim is None else lim-cur1})")
    return {"spent": real, "cur0": cur0, "cur1": cur1}


def aggregate(c):
    """PASO 2: multi-season club_form from cached /players (2025+2024+2023), recency+minutes weighted."""
    roster = pd.read_csv(ROSTER)
    team_num_r = defaultdict(float); team_w_r = defaultdict(float)
    team_num_g = defaultdict(float); team_w_g = defaultdict(float)
    team_name = {}; team_players = defaultdict(set); team_pseasons = defaultdict(int)
    team_wtier_num = defaultdict(float); team_wtier_den = defaultdict(float)
    for r in roster.itertuples(index=False):
        pid = int(r.player_id); tid = int(r.team_id); team_name[tid] = r.team
        team_players[tid].add(pid)
        for season in (2025, 2024, 2023):
            try:
                resp = c.request("/players", {"id": pid, "season": season},
                                 ttl_hours=TTL_FOREVER).get("response") or []
            except Exception:
                resp = []
            if not resp:
                continue
            dom = pick_domestic(resp[0].get("statistics") or [])
            if not dom:
                continue
            mins = float(dom["minutes"] or 0)
            if mins <= 0:
                continue
            team_pseasons[tid] += 1
            t = tier(dom["league_country"], dom["league_name"])
            w = RECENCY[season] * mins            # recency- AND minutes-weighted
            team_wtier_num[tid] += w * t; team_wtier_den[tid] += w
            if dom["rating"] is not None:
                team_num_r[tid] += w * t * float(dom["rating"]); team_w_r[tid] += w
            if mins >= 180:
                ga90 = (float(dom["goals"] or 0) + float(dom["assists"] or 0)) * 90.0 / mins
                team_num_g[tid] += w * t * ga90; team_w_g[tid] += w
    rows = []
    for tid in sorted(team_name):
        cf_rating = (team_num_r[tid] / team_w_r[tid]) if team_w_r[tid] > 0 else None
        cf_ga90 = (team_num_g[tid] / team_w_g[tid]) if team_w_g[tid] > 0 else None
        club_form = (cf_rating + 2.0 * (cf_ga90 or 0.0)) if cf_rating is not None else None
        rows.append({
            "team": team_name[tid], "team_id": tid,
            "club_form": (round(club_form, 3) if club_form is not None else None),
            "cf_rating": (round(cf_rating, 3) if cf_rating is not None else None),
            "cf_ga90": (round(cf_ga90, 3) if cf_ga90 is not None else None),
            "mean_tier": (round(team_wtier_num[tid] / team_wtier_den[tid], 3)
                          if team_wtier_den[tid] > 0 else None),
            "n_players": len(team_players[tid]), "n_player_seasons": team_pseasons[tid]})
    df = pd.DataFrame(rows).sort_values("club_form", ascending=False, na_position="last")
    df.to_csv(OUT, index=False)
    print("\n" + "=" * 90)
    print("CLUB-FORM MULTI-TEMPORADA (2025/2024/2023, recencia+minutos, tier-normalizado)")
    print("=" * 90)
    tot_ps = df["n_player_seasons"].sum()
    print(f"selecciones: {len(df)} | player-seasons con datos de club: {tot_ps} "
          f"(media {tot_ps/max(len(df),1):.1f}/selección) | con club_form: {df['club_form'].notna().sum()}/48")
    show = ["team", "club_form", "cf_rating", "cf_ga90", "mean_tier", "n_player_seasons"]
    print("\nTOP 10 / BOTTOM 5:")
    print(df[show].head(10).to_string(index=False))
    print("  ...")
    print(df[show].tail(5).to_string(index=False))
    print(f"\nWritten: {OUT}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-fresh", type=int, default=2600)
    ap.add_argument("--aggregate-only", action="store_true", help="skip fetch, only rebuild the CSV from cache")
    a = ap.parse_args()
    c = APIFootballClient()
    if not a.aggregate_only:
        res = fetch_players(c, a.max_fresh)
        if res is None:
            print("Guard/abort -> no aggrego."); return
    aggregate(c)


if __name__ == "__main__":
    main()
