"""
WORLD CUP — PLAYER-PROP predictions in SHADOW MODE.  ISOLATED · heurístico · NO validado.

Four props per starter: (1) marca gol, (2) ve tarjeta, (3) tiros (+ P≥1 a puerta),
(4) da asistencia. They are PREDICTED, SETTLED and SCORED against their own scorecard —
they are NEVER shown in the ficha and NEVER sent to Telegram. ZERO betting endpoints.

METHOD (honest heuristic — split a team total among its XI by historical share):
  * XI: confirmed /fixtures/lineups startXI if available; else the most-likely XI by RECENT
        national-team starts — how many of the team's last RECENT_N finished matches each
        call-up STARTED (/fixtures?team&last=N + /fixtures/lineups per fixture, store-guarded;
        per-fixture lineups are immutable -> cached 'forever'). Falls back to accumulated
        /players starts (history) only when recent lineups are unavailable (soft-fail).
  * Per-player /90 rates (goals/assists/shots/shots-on/cards) from /players?team&season over
        RATE_SEASONS. Small national samples are SHRUNK toward the XI mean (empirical-Bayes,
        weight minutes/(minutes+PRIOR_MIN)); this is the documented "mix" that stabilises thin
        national samples in the shadow (a true club blend via /players?id is a future refinement).
  * GOL:      λ_i = our_xg_team(L3) × share_goal_i × XI_ATTR;   P = 1−exp(−λ_i).
  * TARJETA:  λ_i = (st_cards_total/2) × share_card_i;          P = 1−exp(−λ_i).
  * TIROS:    λ_shots_i = st_shots_team × share_shots_i;  exp tiros = λ_shots_i;
              P(≥1 a puerta) = 1−exp(−λ_shots_i × on_target_ratio_i).
  * ASIST:    λ_i = our_xg_team × ASSIST_FRAC × share_assist_i; P = 1−exp(−λ_i).
  XI_ATTR<1 leaves "resto no atribuido" (subs/own goals). All probabilistic — no certainty.

Subcommands:  predict (NS only, anti-hindsight, lock-first per fixture) · settle (after FT) ·
              scorecard (per prop type: logloss/brier/ECE + base-rate skill).

KNOCKOUT NOTE (#7, documented bias — behaviour unchanged): the λ are derived from the team's 90'
xG, but settle counts per-player stats over the WHOLE match (incl. extra time). So in a knockout
that goes to 120', settle can mark a prop "hit" on an extra-time event the 90' model never modelled
AND the 90'-based λ under-counts events. Both inflate noise in those few fixtures. This is SHADOW-
only (never shown/sent), so it just adds variance to the props' own scorecard; left as-is for now.

SAFEGUARDS: does NOT touch the L3 / calibration / lock-at-KO / briefing. Anti-hindsight
(predict pre-KO, freeze at KO, settle only after FT). API store-guarded + cached "forever".
SOFT-FAIL everywhere. NO betting endpoints. Explicit git add (log + scorecard only).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
CARDS = OUT_DIR / "worldcup_cards.csv"
LOG = OUT_DIR / "worldcup_player_props_log.csv"
SCORECARD = OUT_DIR / "worldcup_player_props_scorecard.txt"
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "player_props"   # gitignored raw cache

LEAGUE, SEASON = 1, 2026
RATE_SEASONS = [2024, 2025]      # national-team seasons for historical /90 rates
RECENT_N = 8                     # last N finished national-team matches for "probable XI" form
KO_BUFFER = timedelta(minutes=5)
XI_SIZE = 11
XI_ATTR = 0.85                   # fraction of team goals attributed to the XI (rest unattributed)
ASSIST_FRAC = 0.75               # team assists ≈ this × team goals
CARD_TEAM_SPLIT = 0.5            # half the match's expected cards per team (no per-team cards stored)
PRIOR_MIN = 270.0                # empirical-Bayes shrinkage strength (≈3 full matches)
# Per-run safety BACKSTOP (runaway-loop guard), NOT a coverage limiter: the predict must cover the
# WHOLE briefing window so EVERY fixture in the ficha gets props, not only the nearest ones. The
# store-guard caches /rates, /players/squads and recent /fixtures+lineups "forever" -> a warm run
# costs only ~lineups-per-fixture (tens of calls); a fully cold run of a wide window is a few hundred
# (medido: 7 fixtures = 209). Sized FAR below the Pro daily limit (~7500) with generous headroom so a
# cold run never hits the cap and `break`s mid-loop (which is what dropped the distant fixtures).
MAX_API = 1500                   # per-run backstop; warm ~tens, cold-wide a few hundred (<< 7500/día)
MAX_FIXTURES = 64                # cover a multi-day briefing window with margin (was 20)
EPS = 1e-15

PROPS = ["goal", "card", "shot_on", "assist"]   # binary props scored by the scorecard
LOG_COLUMNS = [
    "fixture_id", "kickoff_utc", "team_id", "team", "player_id", "player", "is_xi", "basis",
    "p_goal", "p_card", "p_shot_on", "p_assist", "exp_shots",
    "lam_goal", "lam_card", "lam_shot_on", "lam_assist",
    "logged_at_utc",
    "act_goal", "act_card", "act_shots", "act_shots_on", "act_assist", "act_minutes",
    "settled", "settled_at_utc",
]

_api_calls = 0


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _parse_ko(s):
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return None
    try:
        return datetime.strptime(str(s).strip()[:16], "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _num(v):
    try:
        if v is None:
            return 0.0
        return float(v)
    except (TypeError, ValueError):
        return 0.0


# --------------------------------------------------------------- store-guarded API
def _client():
    from api_football_client import APIFootballClient  # noqa: E402
    return APIFootballClient()


def _get(client, path, params, ttl):
    """Cached, SOFT-FAILING request honoring the per-run API cap. Returns 'response' or None."""
    global _api_calls
    if path in ("/odds", "/predictions", "/odds/live"):
        raise RuntimeError("PURIFICATION VIOLATION: betting endpoint forbidden")
    if _api_calls >= MAX_API:
        return None
    try:
        resp = client.request(path, params, ttl_hours=ttl)
        _api_calls += 1
        return resp.get("response") if isinstance(resp, dict) else None
    except Exception:
        return None


def _store_path(name):
    return STORE_DIR / f"{name}.json"


def _load_store(name):
    p = _store_path(name)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _save_store(name, data):
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    _store_path(name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------- rates (pure aggregation)
def aggregate_rates(player_rows):
    """player_rows: list of /players items. -> {pid: {name, starts, minutes, g90,a90,sh90,son90,c90,
    on_ratio}} aggregated across all statistics blocks (all seasons/teams provided)."""
    acc = {}
    for it in player_rows or []:
        pl = (it.get("player") or {})
        pid = pl.get("id")
        if pid is None:
            continue
        a = acc.setdefault(int(pid), {"name": pl.get("name"), "starts": 0.0, "minutes": 0.0,
                                      "goals": 0.0, "assists": 0.0, "shots": 0.0, "shots_on": 0.0,
                                      "cards": 0.0})
        for st in (it.get("statistics") or []):
            g = st.get("games") or {}
            a["starts"] += _num(g.get("lineups"))
            a["minutes"] += _num(g.get("minutes"))
            gl = st.get("goals") or {}
            a["goals"] += _num(gl.get("total")); a["assists"] += _num(gl.get("assists"))
            sh = st.get("shots") or {}
            a["shots"] += _num(sh.get("total")); a["shots_on"] += _num(sh.get("on"))
            cd = st.get("cards") or {}
            a["cards"] += _num(cd.get("yellow")) + _num(cd.get("red"))
    out = {}
    for pid, a in acc.items():
        m = a["minutes"]
        per90 = (lambda x: (x / (m / 90.0)) if m > 0 else 0.0)
        out[pid] = {
            "name": a["name"], "starts": a["starts"], "minutes": m,
            "g90": per90(a["goals"]), "a90": per90(a["assists"]),
            "sh90": per90(a["shots"]), "son90": per90(a["shots_on"]), "c90": per90(a["cards"]),
            "on_ratio": (a["shots_on"] / a["shots"]) if a["shots"] > 0 else 0.35,
        }
    return out


def fetch_team_rates(client, tid):
    """Store-guarded national-team /90 rates for a team across RATE_SEASONS. ~0 API on re-run."""
    global _api_calls
    name = f"rates_team{int(tid)}_s{'-'.join(map(str, RATE_SEASONS))}"
    cached = _load_store(name)
    if cached is not None:
        return {int(k): v for k, v in cached.items()}
    rows = []
    for s in RATE_SEASONS:
        page, total = 1, 1
        while page <= total and page <= 6 and _api_calls < MAX_API:
            try:
                resp = client.request("/players", {"team": int(tid), "season": s, "page": page},
                                      ttl_hours=24 * 3650)
            except Exception:
                break
            _api_calls += 1
            data = resp if isinstance(resp, dict) else {}
            rows += (data.get("response") or [])
            total = int((data.get("paging") or {}).get("total") or 1)
            page += 1
    rates = aggregate_rates(rows)
    _save_store(name, {str(k): v for k, v in rates.items()})
    return rates


def fetch_squad(client, tid):
    """Store-guarded REAL World Cup squad (convocatoria): {player_id: name}, or None if
    unavailable. /players/squads is NOT a betting endpoint. Cached 'forever' for the tournament.
    Returns None (not {}) on empty/error so we retry next run instead of caching a bad empty."""
    global _api_calls
    name = f"squad_team{int(tid)}"
    cached = _load_store(name)
    if cached:
        return {int(k): v for k, v in cached.items()}
    if _api_calls >= MAX_API:
        return None
    try:
        resp = client.request("/players/squads", {"team": int(tid)}, ttl_hours=24 * 3650)
    except Exception:
        return None
    _api_calls += 1
    out = {}
    for block in ((resp.get("response") if isinstance(resp, dict) else None) or []):
        for p in (block.get("players") or []):
            pid = p.get("id")
            if pid is not None:
                out[int(pid)] = p.get("name")
    if not out:
        return None
    _save_store(name, {str(k): v for k, v in out.items()})
    return out


def fetch_recent_starts(client, tid):
    """Store-guarded RECENT national-team starts: of the team's last RECENT_N FINISHED matches,
    how many each player STARTED (recent form, not accumulated history). Returns {pid: rstarts}
    or {} (soft-fail -> caller falls back to accumulated /players starts).

    API discipline: the fixtures list uses the client TTL (24h) so it refreshes as new matches
    are played; each fixture's startXI is IMMUTABLE -> cached 'forever' in the store. After the
    first warm-up, re-runs cost ~0-1 calls. Never a betting endpoint. Honors the per-run cap."""
    resp = _get(client, "/fixtures", {"team": int(tid), "last": RECENT_N}, 24)
    fids = []
    for f in (resp or []):
        fx = f.get("fixture") or {}
        fid = fx.get("id")
        if fid is not None and (fx.get("status") or {}).get("short") in ("FT", "AET", "PEN"):
            fids.append(int(fid))
    out = {}
    for fid in fids:
        name = f"lineup_fx{fid}"
        store = _load_store(name)
        if store is None:
            r = _get(client, "/fixtures/lineups", {"fixture": fid}, 24 * 3650)
            if r is None:
                continue  # cap hit or error -> skip this fixture (soft-fail), keep the rest
            store = r
            _save_store(name, store)
        for t in (store or []):
            if (t.get("team") or {}).get("id") != int(tid):
                continue
            for p in (t.get("startXI") or []):
                pid = (p.get("player") or {}).get("id")
                if pid is not None:
                    out[int(pid)] = out.get(int(pid), 0.0) + 1.0
    return out


# --------------------------------------------------------------- prediction (pure math)
def poisson_p_ge1(lam):
    """P(N>=1) for N~Poisson(lam). Always in [0,1]."""
    lam = max(0.0, float(lam))
    return 1.0 - math.exp(-lam)


def _shrunk(rate, minutes, xi_mean):
    """Empirical-Bayes shrink a per-90 rate toward the XI mean for thin samples."""
    w = minutes / (minutes + PRIOR_MIN) if minutes > 0 else 0.0
    return w * rate + (1.0 - w) * xi_mean


def _shares(xi, rates, key):
    """Minutes-shrunk rate per player, then shares within the XI (sum=1, or uniform if all 0)."""
    raw = {pid: rates.get(pid, {}).get(key, 0.0) for pid in xi}
    mean = (sum(raw.values()) / len(xi)) if xi else 0.0
    shr = {pid: _shrunk(raw[pid], rates.get(pid, {}).get("minutes", 0.0), mean) for pid in xi}
    tot = sum(shr.values())
    if tot <= 0:
        return {pid: 1.0 / len(xi) for pid in xi} if xi else {}
    return {pid: shr[pid] / tot for pid in xi}


def _pos(x):
    """nan/None-safe non-negative float."""
    try:
        v = float(x)
        return v if (v == v and v > 0) else 0.0
    except (TypeError, ValueError):
        return 0.0


def predict_fixture(team_xg, team_shots, match_cards, xi, rates):
    """Pure: distribute team totals among the XI -> per-player prop dict. team_xg/team_shots are
    THIS team's expected goals/shots; match_cards is the MATCH total (split per team)."""
    team_xg, team_shots, match_cards = _pos(team_xg), _pos(team_shots), _pos(match_cards)
    sh_goal = _shares(xi, rates, "g90")
    sh_assist = _shares(xi, rates, "a90")
    sh_shots = _shares(xi, rates, "sh90")
    sh_card = _shares(xi, rates, "c90")
    team_cards = max(0.0, float(match_cards)) * CARD_TEAM_SPLIT
    out = []
    for pid in xi:
        r = rates.get(pid, {})
        lam_goal = max(0.0, float(team_xg)) * sh_goal.get(pid, 0.0) * XI_ATTR
        lam_assist = max(0.0, float(team_xg)) * ASSIST_FRAC * sh_assist.get(pid, 0.0) * XI_ATTR
        lam_shots = max(0.0, float(team_shots)) * sh_shots.get(pid, 0.0)
        lam_card = team_cards * sh_card.get(pid, 0.0)
        lam_son = lam_shots * float(r.get("on_ratio", 0.35))
        out.append({
            "player_id": pid, "player": r.get("name"),
            "p_goal": poisson_p_ge1(lam_goal), "lam_goal": lam_goal,
            "p_card": poisson_p_ge1(lam_card), "lam_card": lam_card,
            "exp_shots": lam_shots, "p_shot_on": poisson_p_ge1(lam_son), "lam_shot_on": lam_son,
            "p_assist": poisson_p_ge1(lam_assist), "lam_assist": lam_assist,
        })
    return out


# --------------------------------------------------------------- XI selection
def get_xi(client, fid, tid, rates, squad, recent=None):
    """(list[pid], basis). Confirmed startXI if published (AUTHORITATIVE); else the most-likely
    XI AMONG THE REAL SQUAD (convocatoria), ranked by RECENT starts when available (titularidades
    de los últimos RECENT_N partidos), tie-broken by accumulated history. If recent starts are
    unavailable it falls back to accumulated /players starts. If the squad is unavailable, returns
    ([], 'no_squad') -> the caller OMITS this team rather than invent an XI from non-call-ups.

    Only the RANKING of the probable XI changes; call-ups with neither recent nor historical data
    sort LAST, and non-call-ups are NEVER eligible. The confirmed-lineup path is untouched."""
    resp = _get(client, "/fixtures/lineups", {"fixture": fid}, 0.25)
    for t in (resp or []):
        if (t.get("team") or {}).get("id") == int(tid):
            xi = [int((p.get("player") or {}).get("id")) for p in (t.get("startXI") or [])
                  if (p.get("player") or {}).get("id") is not None]
            if len(xi) >= XI_SIZE:
                return xi[:XI_SIZE], "lineup_confirmed"
    if not squad:
        return [], "no_squad"   # NEVER invent an XI from players who are not in the squad
    recent = recent or {}
    have_recent = any(float(recent.get(pid, 0.0)) > 0 for pid in squad)
    # rank ONLY the called-up players: recent starts first (form), then accumulated history,
    # then accumulated minutes. Call-ups with no data at all fall to the back.
    cand = sorted(squad.keys(), key=lambda pid: (
        -float(recent.get(pid, 0.0)),
        -rates.get(pid, {}).get("starts", 0.0),
        -rates.get(pid, {}).get("minutes", 0.0)))
    basis = "probable_by_recent_starts" if have_recent else "probable_by_squad_starts"
    return cand[:XI_SIZE], basis


# --------------------------------------------------------------- log helpers
def _read_log():
    if LOG.exists():
        df = pd.read_csv(LOG)
        for c in LOG_COLUMNS:
            if c not in df.columns:
                df[c] = np.nan
        return df[LOG_COLUMNS]
    return pd.DataFrame(columns=LOG_COLUMNS)


def _fixture_team_index(client):
    """fid -> (home_id, away_id, status) from the cached /fixtures call (~0 marginal API)."""
    idx = {}
    resp = _get(client, "/fixtures", {"league": LEAGUE, "season": SEASON}, 6)
    for f in (resp or []):
        fx = f.get("fixture") or {}
        tm = f.get("teams") or {}
        fid = fx.get("id")
        if fid is None:
            continue
        idx[int(fid)] = ((tm.get("home") or {}).get("id"), (tm.get("away") or {}).get("id"),
                         (fx.get("status") or {}).get("short"))
    return idx


# --------------------------------------------------------------- predict
def cmd_predict():
    if not CARDS.exists():
        print("player_props predict: no cards.csv; nothing to do."); return
    cards = pd.read_csv(CARDS)
    log = _read_log()
    client = _client()
    tindex = _fixture_team_index(client)
    now = datetime.now(timezone.utc)

    _STUB = {"name": None, "starts": 0.0, "minutes": 0.0, "g90": 0.0, "a90": 0.0,
             "sh90": 0.0, "son90": 0.0, "c90": 0.0, "on_ratio": 0.35}
    fresh_rows, repredicted, done = [], set(), 0
    for _, r in cards.iterrows():
        if done >= MAX_FIXTURES or _api_calls >= MAX_API:
            break
        fid = r.get("fixture_id")
        if pd.isna(fid):
            continue
        fid = int(fid)
        ko = _parse_ko(r.get("kickoff_utc"))
        # LOCK-AT-KO: (re)predict ONLY while NS / strictly pre-KO. At/after kickoff the fixture is
        # FROZEN (skipped -> its existing rows are never touched; settled rows never touched).
        if ko is None or now >= (ko - KO_BUFFER):
            continue
        ids = tindex.get(fid)
        if not ids or ids[0] is None or ids[1] is None:
            continue
        fixture_rows = []
        # DECLARACIÓN (gobernanza): los props derivan del xG del L3 (our_xg_*), que es el VALIDADO en
        # backtest. Aunque el briefing muestre el modelo amplio (mx_*) como motor en vivo, los inputs
        # de props NO cambian a mx_xg_* sin una validación aparte de los props sobre ese xG.
        for side, tid, team_name, xg_col, sh_col in (
                ("home", ids[0], r.get("home"), "our_xg_home", "st_shots_home"),
                ("away", ids[1], r.get("away"), "our_xg_away", "st_shots_away")):
            team_xg = r.get(xg_col)
            if pd.isna(team_xg):
                continue
            rates = dict(fetch_team_rates(client, tid) or {})
            squad = fetch_squad(client, tid)
            recent = fetch_recent_starts(client, tid)   # {pid: recent starts}; {} -> soft fallback
            # call-ups with no historical rate are still eligible (shrunk to the XI mean): give
            # them a stub rate carrying their squad name so they can be logged.
            if squad:
                for pid, nm in squad.items():
                    if pid not in rates:
                        rates[pid] = {**_STUB, "name": nm}
            xi, basis = get_xi(client, fid, tid, rates, squad, recent)
            if not xi:
                continue  # no squad -> OMIT this team (never show non-call-ups)
            preds = predict_fixture(team_xg, r.get(sh_col, 0.0), r.get("st_cards_total", 0.0), xi, rates)
            for p in preds:
                fixture_rows.append({
                    "fixture_id": fid, "kickoff_utc": r.get("kickoff_utc"),
                    "team_id": int(tid), "team": team_name,
                    "player_id": p["player_id"], "player": p["player"], "is_xi": 1, "basis": basis,
                    "p_goal": round(p["p_goal"], 4), "p_card": round(p["p_card"], 4),
                    "p_shot_on": round(p["p_shot_on"], 4), "p_assist": round(p["p_assist"], 4),
                    "exp_shots": round(p["exp_shots"], 2),
                    "lam_goal": round(p["lam_goal"], 4), "lam_card": round(p["lam_card"], 4),
                    "lam_shot_on": round(p["lam_shot_on"], 4), "lam_assist": round(p["lam_assist"], 4),
                    "logged_at_utc": _now_iso(),
                    "act_goal": np.nan, "act_card": np.nan, "act_shots": np.nan,
                    "act_shots_on": np.nan, "act_assist": np.nan, "act_minutes": np.nan,
                    "settled": 0, "settled_at_utc": np.nan,
                })
        if fixture_rows:
            fresh_rows += fixture_rows
            repredicted.add(fid)
            done += 1

    if repredicted:
        if len(log):
            settled = log["settled"].fillna(0).astype(int) == 1
            # drop ONLY the UNSETTLED rows of re-predicted fixtures; keep settled rows + all others
            drop = log["fixture_id"].astype("Int64").isin(repredicted) & ~settled
            log = log[~drop]
        log = pd.concat([log, pd.DataFrame(fresh_rows)], ignore_index=True)[LOG_COLUMNS]
        log.to_csv(LOG, index=False)
    print(f"player_props predict: {len(repredicted)} NS fixture(s) (re)predicted, +{len(fresh_rows)} rows "
          f"| API calls={_api_calls} -> {LOG.name}")


# --------------------------------------------------------------- settle
def cmd_settle():
    log = _read_log()
    if log.empty:
        print("player_props settle: empty log."); return
    client = _client()
    tindex = _fixture_team_index(client)
    now = datetime.now(timezone.utc)
    unsettled = log[log["settled"].fillna(0).astype(int) == 0]
    fids = sorted(set(unsettled["fixture_id"].dropna().astype(int)))
    # columns that hold strings must be object dtype (empty cols load as float64;
    # pandas 2.x raises LossySetitemError writing an ISO string into a float64 column)
    log["settled_at_utc"] = log["settled_at_utc"].astype(object)
    n_set = 0
    for fid in fids:
        if _api_calls >= MAX_API:
            break
        st = (tindex.get(fid) or (None, None, None))[2]
        if st not in ("FT", "AET", "PEN"):
            continue  # settle ONLY after the match is finished
        name = f"fxplayers_{fid}"
        store = _load_store(name)
        if store is None:
            resp = _get(client, "/fixtures/players", {"fixture": fid}, 24 * 3650)
            if resp is None:
                continue
            store = resp
            _save_store(name, store)
        actual = {}
        for t in (store or []):
            for pl in (t.get("players") or []):
                pid = (pl.get("player") or {}).get("id")
                sblk = (pl.get("statistics") or [{}])[0]
                g = sblk.get("games") or {}; gl = sblk.get("goals") or {}
                sh = sblk.get("shots") or {}; cd = sblk.get("cards") or {}
                if pid is None:
                    continue
                actual[int(pid)] = {
                    "min": _num(g.get("minutes")), "goal": 1 if _num(gl.get("total")) > 0 else 0,
                    "assist": 1 if _num(gl.get("assists")) > 0 else 0,
                    "shots": _num(sh.get("total")), "shots_on": _num(sh.get("on")),
                    "card": 1 if (_num(cd.get("yellow")) + _num(cd.get("red"))) > 0 else 0,
                }
        mask = (log["fixture_id"].astype("Int64") == fid) & (log["settled"].fillna(0).astype(int) == 0)
        for i in log[mask].index:
            pid = int(log.at[i, "player_id"]) if not pd.isna(log.at[i, "player_id"]) else None
            a = actual.get(pid, {"min": 0, "goal": 0, "assist": 0, "shots": 0, "shots_on": 0, "card": 0})
            log.at[i, "act_minutes"] = a["min"]; log.at[i, "act_goal"] = a["goal"]
            log.at[i, "act_assist"] = a["assist"]; log.at[i, "act_shots"] = a["shots"]
            log.at[i, "act_shots_on"] = a["shots_on"]; log.at[i, "act_card"] = a["card"]
            log.at[i, "settled"] = 1; log.at[i, "settled_at_utc"] = _now_iso()
        n_set += 1
    log.to_csv(LOG, index=False)
    print(f"player_props settle: {n_set} fixture(s) settled | API calls={_api_calls} -> {LOG.name}")


# --------------------------------------------------------------- scorecard
def _logloss(p, y):
    p = np.clip(np.asarray(p, float), EPS, 1 - EPS)
    y = np.asarray(y, float)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def _brier(p, y):
    return float(np.mean((np.asarray(p, float) - np.asarray(y, float)) ** 2))


def _ece(p, y, bins=10):
    p = np.asarray(p, float); y = np.asarray(y, float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (p > edges[i]) & (p <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(p) * abs(p[m].mean() - y[m].mean())
    return float(e)


GRADUATION_NOTE = (
    "# CRITERIO DE GRADUACIÓN (definido ANTES de ver datos; no post-hoc): un prop pasa de SOMBRA\n"
    "# a producción (mostrarse en Telegram) SOLO si, con N>=30 PARTIDOS liquidados, su predicción\n"
    "# supera al baseline (tasa base del prop) en logloss Y en brier, y tiene ECE<=0.08. Si no,\n"
    "# se queda en sombra. Etiqueta interna: heurístico / no validado.\n"
    "#\n"
    "# ESTADO TRAS BACKTEST HISTÓRICO (internacionales 2024-25, N=3062 jugador-partido, anti-leakage:\n"
    "#   rates de temporada anterior + xG L3 walk-forward + XI confirmado; target nunca como feature):\n"
    "#   * GOL y ASISTENCIA -> GRADUADOS: baten al baseline en logloss Y brier, ECE<=0.02, % fiables\n"
    "#     (gol skill ll +20%/br +13%; asistencia +20%/+11%). Se muestran en la sección VALIDADOS de\n"
    "#     la ficha, sin la etiqueta 'no fiarse'.\n"
    "#   * TARJETA -> GRADUADA tras el RE-TEST con los inputs del MODELO DE STATS de producción\n"
    "#     (props_retest_stats_inputs_*): bate baseline en logloss Y brier, ECE 0.032. Se muestra en la\n"
    "#     sección VALIDADOS, con TOPE de display en la cola (p>0.45 -> '45%+'): la calibración es\n"
    "#     conservadora/optimista en la cola alta y con n pequeño, así que el % alto se capa.\n"
    "#   * TIROS-A-PUERTA -> RANKING ONLY (no gradúa): incluso con los inputs del modelo el logloss\n"
    "#     sigue por debajo del baseline (skill -5.9%; mejora ECE 0.089->0.059 y brier, pero no logloss).\n"
    "#     En la ficha: solo ORDEN (no probabilidad), sin %.\n"
    "# Este scorecard EN VIVO sigue corriendo como CONFIRMACIÓN independiente sobre partidos del Mundial.\n"
)


CARD_CORRECTION_CSV = OUT_DIR / "worldcup_card_prop_correction.csv"


def _card_bias_raw_vs_corrected(settled):
    """Lines reporting the TARJETA bias RAW vs CORRECTED (mean p_card vs real rate act_card>=1), to
    verify the deflation pulls it toward 0. Reads the factor from the correction state (read-only,
    soft). Returns [] if no card data / no factor. NEVER declares victory with N<30."""
    try:
        if "p_card" not in settled.columns or "act_card" not in settled.columns:
            return []
        sub = settled.dropna(subset=["p_card", "act_card"])
        if not len(sub):
            return []
        p = pd.to_numeric(sub["p_card"], errors="coerce").to_numpy(float)
        y = (pd.to_numeric(sub["act_card"], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
        ok = ~np.isnan(p)
        p, y = p[ok], y[ok]
        if not len(p):
            return []
        n_matches = int(sub.loc[ok if len(ok) == len(sub) else sub.index, "fixture_id"].nunique()) \
            if "fixture_id" in sub.columns else len(p)
        mean_pred = float(p.mean())
        real = float(y.mean())
        bias_raw = (mean_pred - real) * 100.0
        factor = None
        if CARD_CORRECTION_CSV.exists():
            try:
                cdf = pd.read_csv(CARD_CORRECTION_CSV)
                if not cdf.empty and "factor" in cdf.columns:
                    factor = float(cdf["factor"].iloc[0])
            except Exception:
                factor = None
        out = ["", "  TARJETA — sesgo CRUDO vs CORREGIDO (deflación de p_card; gol/asistencia NO se tocan):"]
        out.append(f"    crudo:     media pred {mean_pred*100:5.2f}%  vs real {real*100:5.2f}%  "
                   f"-> sesgo {bias_raw:+.2f}pp")
        if factor is not None:
            mp_c = mean_pred * factor
            bias_c = (mp_c - real) * 100.0
            drop = "baja ✓" if abs(bias_c) < abs(bias_raw) - 1e-9 else "no baja"
            out.append(f"    corregido: media pred {mp_c*100:5.2f}%  vs real {real*100:5.2f}%  "
                       f"-> sesgo {bias_c:+.2f}pp  (factor {factor:.4f}; |sesgo| {drop})")
        else:
            out.append("    corregido: (sin factor en worldcup_card_prop_correction.csv -> sin corrección)")
        out.append("    (la corrección solo afecta el VALOR MOSTRADO; el log queda en CRUDO. "
                   "Muestra pequeña -> orientativo, NO es victoria.)")
        return out
    except Exception:
        return []


def cmd_scorecard():
    log = _read_log()
    lines = [GRADUATION_NOTE, "=" * 78,
             "PLAYER PROPS — track record (SOMBRA · heurístico · NO validado · sin mercado)",
             "=" * 78]
    settled = log[log["settled"].fillna(0).astype(int) == 1] if len(log) else log
    n_matches = int(settled["fixture_id"].nunique()) if len(settled) else 0
    n_rows = len(settled)
    lines.append(f"generated_at_utc: {_now_iso()}")
    lines.append(f"partidos liquidados={n_matches} | filas jugador-prop={n_rows} | umbral graduación N>=30")
    if n_matches < 30:
        lines.append("MUESTRA INSUFICIENTE para graduar (N<30). Métricas mostradas son orientativas.")
    lines.append("")
    act_map = {"goal": "act_goal", "card": "act_card", "shot_on": "act_shots_on", "assist": "act_assist"}
    pcol = {"goal": "p_goal", "card": "p_card", "shot_on": "p_shot_on", "assist": "p_assist"}
    if n_rows == 0:
        lines.append("Aún sin filas liquidadas; el scorecard se llenará tras los primeros FT.")
    else:
        hdr = f"  {'prop':9} {'n':>5} {'base%':>6} {'logloss':>8} {'brier':>7} {'ECE':>6} {'ll_base':>8} {'br_base':>7} {'mejora?':>8}"
        lines.append(hdr); lines.append("  " + "-" * (len(hdr) - 2))
        for prop in PROPS:
            ac = act_map[prop]
            sub = settled[pd.notna(settled[ac])]
            if prop == "shot_on":
                y = (pd.to_numeric(sub[ac], errors="coerce").fillna(0) >= 1).astype(int).to_numpy()
            else:
                y = pd.to_numeric(sub[ac], errors="coerce").fillna(0).astype(int).to_numpy()
            p = pd.to_numeric(sub[pcol[prop]], errors="coerce").to_numpy()
            ok = ~np.isnan(p)
            y, p = y[ok], p[ok]
            if len(y) == 0:
                lines.append(f"  {prop:9} {0:>5}  (sin datos)"); continue
            base = float(y.mean())
            pbase = np.full_like(p, base, dtype=float)
            ll, br, ece = _logloss(p, y), _brier(p, y), _ece(p, y)
            llb, brb = _logloss(pbase, y), _brier(pbase, y)
            better = "sí" if (ll < llb and br < brb and ece <= 0.08) else "no"
            lines.append(f"  {prop:9} {len(y):>5} {base*100:>5.0f}% {ll:>8.4f} {br:>7.4f} {ece:>6.3f} "
                         f"{llb:>8.4f} {brb:>7.4f} {better:>8}")
        lines.append("")
        lines.append("  (baseline = tasa base del prop; 'mejora?'=sí solo si bate logloss Y brier Y ECE<=0.08.)")
        lines.append("  (muestra pequeña -> orientativo; la graduación exige N>=30 partidos.)")
        # ---- TARJETA: sesgo CRUDO vs CORREGIDO (verifica que la deflación lo acerca a 0). El factor se
        #      lee del estado de worldcup_card_prop_correction (read-only, soft); el log queda en CRUDO.
        lines += _card_bias_raw_vs_corrected(settled)
    SCORECARD.write_text("\n".join(lines), encoding="utf-8")
    print(f"player_props scorecard: matches={n_matches} rows={n_rows} -> {SCORECARD.name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup player props (SHADOW; isolated).")
    ap.add_argument("cmd", choices=["predict", "settle", "scorecard"])
    a = ap.parse_args()
    {"predict": cmd_predict, "settle": cmd_settle, "scorecard": cmd_scorecard}[a.cmd]()
