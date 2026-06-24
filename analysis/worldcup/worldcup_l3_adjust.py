"""
WORLD CUP 2026 - live HEURISTIC adjustment to the L3 supremacy (ISOLATED, SECONDARY).

NOT the official prediction. The L3 stays official and untouched; this is a transparent,
capped, LABELLED side-estimate that nudges the L3 strength for today's key absences and is
measured forward in the scorecard. NO market (zero odds/predictions). SOFT-FAIL everywhere.

RULE (one sentence):
  For each KEY starter absent (injured, or out of the confirmed XI) who plays in a top-5
  league (tier 1.0) or strong league (tier 0.8), subtract a fixed nudge from his team's L3
  strength (-0.08 tier-1.0, -0.05 tier-0.8), capped at -0.25 per team; then
  sup_adj = (s_home + Δ_home) - (s_away + Δ_away) runs the SAME L3 pipeline -> adjusted 1X2/xG.

KEY player = plays in a top-5/strong league (tier >= 0.80) AND is a regular (apps >= team
median apps), from our own squad_quality_raw_48.csv. Names are matched by deaccented surname
(+ first initial on collisions); no match -> no nudge (no-invent).
"""
from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
SQUAD = OUT_DIR / "squad_quality_raw_48.csv"

STEP = {1.00: 0.08, 0.80: 0.05}   # nudge per absent key player, by club-league tier
CAP = 0.25                         # max total nudge per team (bounded so it can't dominate L3)
MIN_TIER = 0.80                    # only trust absences of clearly high-quality players


# ----------------------------------------------------------------- name matching
def _norm(s) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()
    return s


def _surname_key(name):
    """(surname, first_initial) deaccented. 'M. Crépeau' -> ('crepeau','m')."""
    n = _norm(name).replace(".", " ")
    toks = [t for t in n.split() if t]
    if not toks:
        return ("", "")
    return (toks[-1], toks[0][0] if toks[0] else "")


def _tier(country, league) -> float:
    """Club-league quality tier (0.30..1.00) — reuses the committed squad_strength_model logic."""
    try:
        sys.path.insert(0, str(OUT_DIR))
        import squad_strength_model as ssm  # noqa: E402
        return float(ssm.tier(country, league))
    except Exception:
        return 0.30


# ----------------------------------------------------------------- squad index
def load_squad_index(path: Path = SQUAD) -> dict:
    """team -> {median_apps, players: {surname: [{initial, tier, apps, name}, ...]}}. {} if absent."""
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
            t = _tier(r.get("club_country"), r.get("club_league"))
            a = float(pd.to_numeric(pd.Series([r.get("apps")]), errors="coerce").fillna(0.0).iloc[0])
            sur, init = _surname_key(r.get("player_name"))
            players.setdefault(sur, []).append(
                {"initial": init, "tier": t, "apps": a, "name": str(r.get("player_name"))})
        out[str(team)] = {"median_apps": med, "players": players}
    return out


def _lookup(team_idx, name):
    """Find the squad record for a player name, or None (no-invent on ambiguity)."""
    sur, init = _surname_key(name)
    cands = team_idx.get("players", {}).get(sur, [])
    if not cands:
        return None
    if len(cands) == 1:
        return cands[0]
    for c in cands:               # disambiguate same-surname by first initial
        if c["initial"] and init and c["initial"] == init:
            return c
    return None


def _step(tier) -> float:
    return STEP.get(round(float(tier), 2), 0.0)


def team_delta(team_idx, absent_names):
    """(Δstrength <= 0, [names of key absentees that contributed]) for one team."""
    if not team_idx:
        return 0.0, []
    med = team_idx.get("median_apps", 0.0)
    total = 0.0
    hits = []
    seen = set()
    for nm in absent_names or []:
        rec = _lookup(team_idx, nm)
        if rec is None:
            continue
        if rec["tier"] >= MIN_TIER and rec["apps"] >= med:
            st = _step(rec["tier"])
            if st > 0 and rec["name"] not in seen:
                seen.add(rec["name"])
                total += st
                hits.append(rec["name"])
    return -min(CAP, total), hits


def key_players_out_of_xi(team_idx, lu_team, injured_names):
    """Pre-KO refinement: key players (tier>=0.80 & regular) NOT in the confirmed XI and not
    already injured. None if the XI isn't confirmed (so we don't refine on partial data)."""
    if not team_idx or not lu_team or not lu_team.get("confirmed"):
        return None
    xi_names = lu_team.get("xi_names") or []
    if len(xi_names) < 11:
        return None
    xi_sur = {_surname_key(n)[0] for n in xi_names}
    inj_sur = {_surname_key(n)[0] for n in (injured_names or [])}
    med = team_idx.get("median_apps", 0.0)
    out, seen = [], set()
    for sur, recs in team_idx.get("players", {}).items():
        if not sur or sur in xi_sur or sur in inj_sur:
            continue
        for rec in recs:
            if rec["tier"] >= MIN_TIER and rec["apps"] >= med and rec["name"] not in seen:
                seen.add(rec["name"])
                out.append(rec["name"])
    return out


# ----------------------------------------------------------------- adjusted prediction
def predict_adjusted(pred, home, away, dh, da):
    """Run the SAME L3 pipeline with nudged supremacy. pred = l3_offline.Predictor. None if no rating."""
    sh = pred.strength.get(home)
    sa = pred.strength.get(away)
    if sh is None or sa is None:
        return None
    sys.path.insert(0, str(OUT_DIR))
    import l3_offline  # noqa: E402
    sup = (float(sh) + dh) - (float(sa) + da)
    lh, la = l3_offline.raw_xg(sup, pred.a0, pred.a1, pred.total_mean)
    raw = l3_offline.wdl(lh, la)
    cal = np.array([np.interp(raw[k], pred.iso[k]["ux"], pred.iso[k]["uf"]) for k in range(3)])
    cal = np.clip(cal, 1e-6, None)
    cal = cal / cal.sum()
    return {"adj_home": round(float(cal[0]), 4), "adj_draw": round(float(cal[1]), 4),
            "adj_away": round(float(cal[2]), 4),
            "adj_xg_home": round(float(lh), 2), "adj_xg_away": round(float(la), 2)}


def compute_fixture_adjustment(pred, squad_idx, home, away, inj_home=None, inj_away=None,
                               xi_out_home=None, xi_out_away=None):
    """Full per-fixture adjustment. Returns the adj_* dict, or None if Δ==0 (no adjustment ->
    the ficha shows ONLY L3). basis='inj' (morning, canonical) or 'inj+xi' (pre-KO refinement)."""
    basis = "inj"
    abs_h = list(inj_home or [])
    abs_a = list(inj_away or [])
    if xi_out_home is not None or xi_out_away is not None:
        basis = "inj+xi"
        abs_h += list(xi_out_home or [])
        abs_a += list(xi_out_away or [])
    dh, hits_h = team_delta(squad_idx.get(home, {}), abs_h)
    da, hits_a = team_delta(squad_idx.get(away, {}), abs_a)
    if dh == 0.0 and da == 0.0:
        return None
    adj = predict_adjusted(pred, home, away, dh, da)
    if adj is None:
        return None
    adj.update({"adj_basis": basis,
                "adj_delta_home": round(dh, 3), "adj_delta_away": round(da, 3),
                "adj_absent_home": "; ".join(hits_h), "adj_absent_away": "; ".join(hits_a)})
    return adj
