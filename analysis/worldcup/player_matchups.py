"""
WORLD CUP 2026 — INDIVIDUAL MATCHUPS (Fase 3). READ-ONLY · NO API · NO market/odds · NO betting.

Crosses the probable XIs (positions + roles from data/external/player_positional_profiles.csv) with the
team styles (coach context) to surface likely INDIVIDUAL duels: winger vs fullback, striker vs centre-
backs, creative midfielder vs opponent press, attacking fullback vs winger, slow centre-back vs fast
striker, keeper vs shot volume.

Honest degradation (spec §8): if there is not enough positional data on BOTH sides, it returns a single
`matchups_heuristic_only` entry with low confidence + reason (optionally seeded by the team-level
heuristic). It never fabricates a duel or a hard %; `advantage` is qualitative and every entry carries
confidence + reason + possible_effect_on_prediction.

Output: list of dicts {player_a, player_b, zone, advantage, confidence, reason,
                        possible_effect_on_prediction}.
"""
from __future__ import annotations

# ---- position normalisation: free-text position string -> coarse bucket (None if unknown) ----
_POS_MAP = {
    "gk": "GK", "goalkeeper": "GK", "portero": "GK",
    "cb": "CB", "center back": "CB", "centre back": "CB", "central": "CB", "dc": "CB",
    "lb": "FB", "rb": "FB", "wb": "FB", "lwb": "FB", "rwb": "FB", "fullback": "FB",
    "full back": "FB", "lateral": "FB", "carrilero": "FB",
    "cdm": "DM", "dm": "DM", "pivote": "DM", "mediocentro defensivo": "DM",
    "cm": "CM", "mc": "CM", "mediocentro": "CM",
    "cam": "AM", "am": "AM", "media punta": "AM", "enganche": "AM", "creativo": "AM",
    "lw": "W", "rw": "W", "lm": "W", "rm": "W", "winger": "W", "extremo": "W", "banda": "W",
    "st": "FWD", "cf": "FWD", "fw": "FWD", "delantero": "FWD", "striker": "FWD", "9": "FWD",
}


def _bucket(pos):
    if not pos:
        return None
    s = str(pos).strip().lower()
    if s in _POS_MAP:
        return _POS_MAP[s]
    for k, v in _POS_MAP.items():
        if k in s:
            return v
    return None


def _profile(pid, positional_map):
    return positional_map.get(int(pid)) if (positional_map and pid is not None) else None


def _enrich_xi(xi, positional_map):
    """xi: [{player_id, player_name, team}] -> add bucket + threat fields from the positional profile.
    Players without a profile are kept but flagged (bucket None)."""
    out = []
    n_with = 0
    for p in xi or []:
        pid = p.get("player_id")
        prof = _profile(pid, positional_map)
        b = _bucket(prof.get("position")) if prof else None
        if prof:
            n_with += 1
        out.append({
            "player_id": pid, "player_name": p.get("player_name") or p.get("player"),
            "team": p.get("team"), "bucket": b,
            "role": (prof or {}).get("role"),
            "pace_threat": (prof or {}).get("pace_threat"),
            "aerial_threat": (prof or {}).get("aerial_threat"),
            "crossing_threat": (prof or {}).get("crossing_threat"),
            "one_v_one": (prof or {}).get("1v1_threat"),
            "attacking_weight": (prof or {}).get("attacking_weight"),
            "defensive_weight": (prof or {}).get("defensive_weight"),
            "card_risk_role": (prof or {}).get("card_risk_role"),
            "has_profile": prof is not None,
        })
    return out, n_with


def _by_bucket(enriched, bucket):
    return [e for e in enriched if e["bucket"] == bucket]


def _hi(v):
    return v is not None and v >= 0.6


def _adv(a_name, b_name, a_better, zone, reason, effect, conf):
    return {"player_a": a_name, "player_b": b_name, "zone": zone,
            "advantage": a_name if a_better else b_name,
            "confidence": conf, "reason": reason, "possible_effect_on_prediction": effect}


def _duels_one_direction(att, deff, att_team, def_team):
    """Attacking players of one team vs the matching defenders of the other. Returns matchup dicts."""
    out = []
    wingers = _by_bucket(att, "W")
    fwds = _by_bucket(att, "FWD")
    fullbacks = _by_bucket(deff, "FB")
    centrebacks = _by_bucket(deff, "CB")

    # winger vs fullback (pace/1v1/crossing)
    for w in wingers[:2]:
        fb = fullbacks[0] if fullbacks else None
        if not fb:
            continue
        att_edge = _hi(w["pace_threat"]) or _hi(w["one_v_one"]) or _hi(w["crossing_threat"])
        def_edge = _hi(fb["defensive_weight"])
        a_better = att_edge and not def_edge
        out.append(_adv(
            w["player_name"], fb["player_name"], a_better,
            "extremo vs lateral",
            f"{w['player_name']} ({att_team}) por banda contra {fb['player_name']} ({def_team})"
            + (" — extremo con ventaja de velocidad/1v1" if att_edge else ""),
            "más centros/llegadas por esa banda si el extremo gana el duelo",
            "media" if (w["has_profile"] and fb["has_profile"]) else "baja"))

    # striker vs centre-backs (pace vs slow CB / aerial)
    for st in fwds[:1]:
        cb = None
        # prefer the slowest CB if pace is recorded
        cbs_with_pace = [c for c in centrebacks if c["pace_threat"] is not None]
        if cbs_with_pace:
            cb = min(cbs_with_pace, key=lambda c: c["pace_threat"] if c["pace_threat"] is not None else 1.0)
        elif centrebacks:
            cb = centrebacks[0]
        if not cb:
            continue
        fast_striker_slow_cb = _hi(st["pace_threat"]) and (cb["pace_threat"] is not None
                                                           and cb["pace_threat"] <= 0.4)
        a_better = fast_striker_slow_cb or _hi(st["aerial_threat"]) and not _hi(cb["aerial_threat"])
        zone = "central lento vs delantero rápido" if fast_striker_slow_cb else "delantero vs central"
        out.append(_adv(
            st["player_name"], cb["player_name"], a_better, zone,
            f"{st['player_name']} ({att_team}) contra {cb['player_name']} ({def_team})"
            + (" — central con poca velocidad ante delantero rápido" if fast_striker_slow_cb else ""),
            "balones a la espalda / duelo aéreo pueden generar ocasiones",
            "media" if (st["has_profile"] and cb["has_profile"]) else "baja"))
    return out


def build_matchups(home_xi, away_xi, positional_map=None, positional_reason=None,
                   home_style=None, away_style=None, team_heuristic=None, exp_shots_total=None):
    """home_xi/away_xi: [{player_id, player_name, team}]. positional_map: {pid: profile} from the adapter
    (None -> heuristic_only). Returns the §8 matchup list, degrading honestly.

    team_heuristic: optional output of core.key_matchups(...) to seed a heuristic note.
    exp_shots_total: optional expected shots on target total (for the keeper-vs-volume read)."""
    positional_map = positional_map or {}
    h_enr, h_with = _enrich_xi(home_xi, positional_map)
    a_enr, a_with = _enrich_xi(away_xi, positional_map)

    # need at least a couple of profiled players on BOTH sides for real duels
    if not positional_map or h_with < 2 or a_with < 2:
        base = {"zone": "general", "advantage": "no determinado",
                "matchups_heuristic_only": True, "confidence": "baja",
                "reason": (positional_reason or "datos posicionales insuficientes en ambos XI")
                + " — solo lectura heurística de equipo (Fase 3 requiere perfiles posicionales)",
                "possible_effect_on_prediction": "ninguno garantizado; lectura cualitativa de equipo"}
        if team_heuristic:
            h0 = team_heuristic[0] if isinstance(team_heuristic, list) and team_heuristic else None
            if h0 and h0.get("advantage") not in (None, "no determinado"):
                base["player_a"] = h0.get("player_a")
                base["player_b"] = h0.get("player_b")
                base["advantage"] = h0.get("advantage")
                base["reason"] = (h0.get("effect_on_prediction") or base["reason"]) \
                    + " (heurística de equipo, no duelo individual)"
        return [base]

    home_team = (home_xi[0].get("team") if home_xi else None)
    away_team = (away_xi[0].get("team") if away_xi else None)
    matchups = []
    matchups += _duels_one_direction(h_enr, a_enr, home_team, away_team)
    matchups += _duels_one_direction(a_enr, h_enr, away_team, home_team)

    # keeper vs shot volume (only if we can see a keeper + an expected shot volume)
    for side_enr, opp_team, shots in ((h_enr, away_team, exp_shots_total), (a_enr, home_team, exp_shots_total)):
        gk = _by_bucket(side_enr, "GK")
        if gk and shots is not None and shots >= 4.5:
            matchups.append({
                "player_a": gk[0]["player_name"], "player_b": f"volumen de tiro de {opp_team}",
                "zone": "portero vs volumen de tiros",
                "advantage": "no determinado",
                "confidence": "baja",
                "reason": f"se esperan ~{shots:.1f} tiros a puerta del rival; el portero tendrá trabajo",
                "possible_effect_on_prediction": "más paradas esperadas; depende del estado del portero"})

    if not matchups:
        return [{"zone": "general", "advantage": "no determinado", "matchups_heuristic_only": True,
                 "confidence": "baja", "reason": "perfiles presentes pero sin duelos claros por zona",
                 "possible_effect_on_prediction": "ninguno garantizado"}]
    # keep the most informative few
    matchups.sort(key=lambda m: 0 if m["confidence"] == "media" else 1)
    return matchups[:5]
