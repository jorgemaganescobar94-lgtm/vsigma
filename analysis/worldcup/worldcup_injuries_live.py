"""
WORLD CUP 2026 - LIVE injuries adjustment to the DISPLAYED prediction (motor máximo).

This is NOT a trained feature: injuries have NO backtest history here, so it cannot be
validated offline. It is an HONEST, LABELLED, REVERSIBLE *live* nudge — not a model claim.
It moves the xG of the DISPLAYED engine (mx_* if present, else ctx_*/our_*) for today's KEY
absences and recomputes 1X2/OU/BTTS with the SAME Poisson machinery (l3_offline.wdl for the
1X2 delta; the ficha's own score_matrix for OU/BTTS, which already reads the displayed xG).
NO market (zero odds/predictions calls). SOFT-FAIL everywhere.

REVERSAL (exact):
  * INJURIES_LIVE = False  -> compute_fixture_injury_adjustment() returns None -> no inj_*
    columns are written -> the ficha shows EXACTLY the unadjusted motor máximo.
  * No key absence moves the xG (or no injury data) -> None (soft) -> same exact reversal.

It REUSES the proven starter/name-matching machinery from worldcup_l3_adjust (deaccented
surname + initial match; KEY = tier>=0.80 top-5/strong league AND apps>=team median). The L3
strength-space shadow adjustment (worldcup_l3_adjust) stays UNTOUCHED and keeps running for
its own A/B; only its secondary ficha line is suppressed by the renderer when an inj_* live
adjustment exists (so the reader never sees two injury adjustments at once).

COEFFICIENTS (xG-space, conservative, capped) — DOCUMENTED, NOT validated:
  Per KEY absence, by squad position (from squad_quality_raw_48.csv):
    Attacker    -> OWN team xG   -0.12 (tier 1.0) / -0.10 (tier 0.8)
    Midfielder  -> OWN team xG   -0.07 (tier 1.0) / -0.06 (tier 0.8)
    Defender    -> OPPONENT xG   +0.05 (marginal; a weaker defence concedes a little more)
    Goalkeeper  -> OPPONENT xG   +0.04 (marginal)
    unknown pos -> treated as Midfielder (moderate own-xG nudge)
  Caps per team: own-xG drop <= 0.40 ; opponent-xG add (conceded) <= 0.40.
  Adjusted xG floored at 0.15 (no degenerate Poisson). Defence is deliberately marginal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]   # .../vsigma (repo root; matches build_worldcup_cards)
SQUAD = OUT_DIR / "squad_quality_raw_48.csv"
STORE_DIR = ROOT / "data" / "processed" / "worldcup" / "injuries_live"

sys.path.insert(0, str(OUT_DIR))
import worldcup_l3_adjust as base  # noqa: E402  (reuse _surname_key/_tier/_lookup/key_players_out_of_xi)

# 🔴 EN VIVO: FLAG de la capa de bajas. True -> se calcula y se MUESTRA el ajuste (columnas inj_*);
# la ficha muestra inj_* por encima de mx_*/ctx_*/our_*. False -> compute_* devuelve None -> NO se
# escriben inj_* -> REVERSA EXACTA al motor máximo sin tocar nada más. Es la ÚNICA fuente de verdad
# del flag (build_worldcup_cards solo llama a compute_*; con False no hay inj_* -> ficha sin cambio).
INJURIES_LIVE = True

# coeficientes xG-space (documentados arriba). Clave por tier ∈ {1.00, 0.80} (sólo jugadores clave).
OFF_STEP = {1.00: 0.12, 0.80: 0.10}   # atacante -> baja el xG PROPIO
MID_STEP = {1.00: 0.07, 0.80: 0.06}   # centrocampista -> baja el xG PROPIO (menor)
DEF_STEP = {1.00: 0.05, 0.80: 0.05}   # defensa -> sube el xG del RIVAL (marginal)
GK_STEP = {1.00: 0.04, 0.80: 0.04}    # portero -> sube el xG del RIVAL (marginal)
CAP_OWN = 0.40                         # tope de reducción de xG propio por equipo
CAP_CONCEDE = 0.40                     # tope de xG concedido (sumado al rival) por equipo
XG_FLOOR = 0.15                        # suelo del xG ajustado (Poisson no degenerado)
MIN_TIER = 0.80                        # sólo bajas de jugadores claramente de alto nivel

_STEP_BY_BUCKET = {"off": OFF_STEP, "mid": MID_STEP, "def": DEF_STEP, "gk": GK_STEP}
BUCKET_ES = {"off": "ATQ", "mid": "MED", "def": "DEF", "gk": "POR"}


# ----------------------------------------------------------------- position bucket
def position_bucket(position) -> str:
    """Map a squad 'position' to off|mid|def|gk. Unknown -> 'mid' (moderate own-xG)."""
    p = base._norm(position)
    if "attack" in p or "forward" in p or "striker" in p or "winger" in p:
        return "off"
    if "goal" in p or "keeper" in p:
        return "gk"
    if "defen" in p or "back" in p:
        return "def"
    if "midfield" in p:
        return "mid"
    return "mid"


# ----------------------------------------------------------------- squad index (with position)
def load_squad_index(path: Path = SQUAD) -> dict:
    """team -> {median_apps, players: {surname: [{initial, tier, apps, name, position}, ...]}}.
    Same structure base._lookup/key_players_out_of_xi expect, PLUS a 'position' field. {} if absent."""
    if not Path(path).exists():
        return {}
    try:
        df = pd.read_csv(path)
    except Exception:
        return {}
    out = {}
    for team, g in df.groupby("team"):
        apps = pd.to_numeric(g["apps"], errors="coerce").fillna(0.0)
        med = float(apps.median()) if len(apps) else 0.0
        players = {}
        for _, r in g.iterrows():
            t = base._tier(r.get("club_country"), r.get("club_league"))
            a = float(pd.to_numeric(pd.Series([r.get("apps")]), errors="coerce").fillna(0.0).iloc[0])
            sur, init = base._surname_key(r.get("player_name"))
            players.setdefault(sur, []).append(
                {"initial": init, "tier": t, "apps": a, "name": str(r.get("player_name")),
                 "position": str(r.get("position") or "")})
        out[str(team)] = {"median_apps": med, "players": players}
    return out


# ----------------------------------------------------------------- forever store (/injuries)
def _store_path(fid) -> Path:
    return STORE_DIR / f"injuries_fx{int(fid)}.json"


def load_injuries_store(fid):
    """Forever-cached parsed /injuries for a fixture: {team_name: [[player, reason], ...]} or None."""
    p = _store_path(fid)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def save_injuries_store(fid, by_team) -> None:
    """Persist the parsed by-team injuries forever (store-guard). Soft-fail (best effort)."""
    try:
        STORE_DIR.mkdir(parents=True, exist_ok=True)
        payload = {str(k): [list(x) for x in v] for k, v in (by_team or {}).items()}
        _store_path(fid).write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


# ----------------------------------------------------------------- per-team xG delta
def team_injury_delta(team_idx, absent_names):
    """For ONE team's absent KEY players, return (own_drop>=0, concede_add>=0, hits).
      own_drop    = Σ off/mid steps -> this team SCORES less (applied to its OWN xG), capped.
      concede_add = Σ def/gk steps  -> this team's defence weaker -> OPPONENT scores a bit more, capped.
      hits        = [{'name','bucket','tier'}] for the KEY absentees that actually contributed.
    No team / no key absence -> (0.0, 0.0, [])."""
    if not team_idx:
        return 0.0, 0.0, []
    med = team_idx.get("median_apps", 0.0)
    own = 0.0
    concede = 0.0
    hits, seen = [], set()
    for nm in absent_names or []:
        rec = base._lookup(team_idx, nm)
        if rec is None:
            continue
        if rec["tier"] < MIN_TIER or rec["apps"] < med:
            continue
        if rec["name"] in seen:
            continue
        bucket = position_bucket(rec.get("position"))
        step = _STEP_BY_BUCKET[bucket].get(round(float(rec["tier"]), 2), 0.0)
        if step <= 0:
            continue
        seen.add(rec["name"])
        if bucket in ("off", "mid"):
            own += step
        else:
            concede += step
        hits.append({"name": rec["name"], "bucket": bucket, "tier": round(float(rec["tier"]), 2)})
    return min(CAP_OWN, own), min(CAP_CONCEDE, concede), hits


# ----------------------------------------------------------------- label
def _key_name(hits):
    """The single most important absentee for the label (offensive first, then by tier)."""
    if not hits:
        return None
    order = {"off": 0, "mid": 1, "def": 2, "gk": 3}
    return sorted(hits, key=lambda h: (order[h["bucket"]], -h["tier"]))[0]["name"]


def _absent_str(hits):
    """'Vinicius Jr (ATQ); Casemiro (MED)' for the logged absentee field."""
    return "; ".join(f"{h['name']} ({BUCKET_ES[h['bucket']]})" for h in hits)


def build_note(home, away, hits_h, hits_a):
    """Honest ficha label (Jorge's wording). None if neither team has a contributing absence."""
    parts = []
    if hits_h:
        parts.append(f"{home} {len(hits_h)} baja(s) (incl. {_key_name(hits_h)})")
    if hits_a:
        parts.append(f"{away} {len(hits_a)} baja(s) (incl. {_key_name(hits_a)})")
    if not parts:
        return None
    return "Ajustado por bajas: " + " · ".join(parts) + " — ajuste live, sin validar"


# ----------------------------------------------------------------- fixture adjustment
def compute_fixture_injury_adjustment(home, away, base_probs, base_xg_home, base_xg_away,
                                      squad_idx, inj_home=None, inj_away=None,
                                      xi_out_home=None, xi_out_away=None):
    """LIVE injuries adjustment for ONE fixture, on the DISPLAYED engine.

    base_probs       = (p_home, p_draw, p_away) of the engine actually shown (mx_* if present).
    base_xg_home/away = the displayed xG (mx_xg_* if present, else ctx_*/our_*).
    Returns an inj_* dict, or None (flag off / no key absence / no rating / soft-fail) -> EXACT
    reversal (the caller then writes no inj_* columns). The 1X2 moves by the Poisson DELTA of the
    xG change applied to the displayed probs, so Δxg==0 -> Δprob==0 (exact)."""
    if not INJURIES_LIVE:
        return None
    try:
        if base_probs is None or base_xg_home is None or base_xg_away is None:
            return None
        if any(pd.isna(v) for v in (base_xg_home, base_xg_away, *base_probs)):
            return None
        basis = "inj"
        abs_h = list(inj_home or [])
        abs_a = list(inj_away or [])
        if xi_out_home is not None or xi_out_away is not None:
            basis = "inj+xi"
            abs_h += list(xi_out_home or [])
            abs_a += list(xi_out_away or [])
        own_h, conc_h, hits_h = team_injury_delta(squad_idx.get(home, {}), abs_h)
        own_a, conc_a, hits_a = team_injury_delta(squad_idx.get(away, {}), abs_a)
        if not hits_h and not hits_a:
            return None
        bxh, bxa = float(base_xg_home), float(base_xg_away)
        # home xG: minus its OWN offensive drop, plus what AWAY now concedes (away def/gk out); vice-versa
        xg_h = max(XG_FLOOR, bxh - own_h + conc_a)
        xg_a = max(XG_FLOOR, bxa - own_a + conc_h)
        if abs(xg_h - bxh) < 1e-9 and abs(xg_a - bxa) < 1e-9:
            return None
        import l3_offline  # noqa: E402  (SAME Poisson machinery as the L3/ficha)
        delta = l3_offline.wdl(xg_h, xg_a) - l3_offline.wdl(bxh, bxa)
        p = np.array([float(base_probs[0]), float(base_probs[1]), float(base_probs[2])]) + delta
        p = np.clip(p, 1e-6, None)
        p = p / p.sum()
        note = build_note(home, away, hits_h, hits_a)
        return {
            "inj_home": round(float(p[0]), 4), "inj_draw": round(float(p[1]), 4),
            "inj_away": round(float(p[2]), 4),
            "inj_xg_home": round(float(xg_h), 2), "inj_xg_away": round(float(xg_a), 2),
            "inj_basis": basis,
            "inj_drop_home": round(own_h, 3), "inj_drop_away": round(own_a, 3),
            "inj_concede_home": round(conc_h, 3), "inj_concede_away": round(conc_a, 3),
            "inj_count_home": len(hits_h), "inj_count_away": len(hits_a),
            "inj_absent_home": _absent_str(hits_h), "inj_absent_away": _absent_str(hits_a),
            "inj_note": note,
        }
    except Exception:  # noqa: BLE001  (soft-fail -> sin ajuste -> reversa exacta)
        return None
