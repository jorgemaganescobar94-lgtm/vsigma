"""
PLAYER & INDIVIDUAL-EVENTS PREDICTION — SHARED CORE (pure, reusable, NO I/O, NO API, NO betting).

This is the cross-product core for the player-events module (Fase 1). It is consumed by the World Cup
shadow glue (analysis/worldcup/build_worldcup_player_events.py) and is designed to be reusable by the
production pipeline later (it imports nothing product-specific).

DESIGN PRINCIPLES (match CLAUDE.md + the spec's §12 safety rules):
  * NEVER invent numbers. Every metric is derived deterministically from inputs already produced by the
    existing per-player model (λ_goal=xG_i, λ_shots, λ_shot_on, λ_assist, p_card) via Poisson, OR comes
    from an external adapter. If an input is missing, the field is None and a reason is set — no fake %.
  * Honest confidence: every block carries data_quality (alta/media/baja), confidence, and reason.
  * Set-piece / matchups / tactical depth that need data we may not have degrade gracefully to
    "no determinado" with a reason instead of fabricating a hierarchy.
  * NO betting language anywhere (no odds/edge/pick/stake/ROI).

The per-player input rows are the SAME dicts the props model logs:
  {player_id, player, team, is_xi, basis, lam_goal, exp_shots, lam_shot_on, lam_assist, p_card, ...}
"""
from __future__ import annotations

import math
from typing import Optional

EPS = 1e-12

# sample-size thresholds for the honest confidence ladder (player-prop minutes / starts proxy via basis)
CONF_BASIS_HIGH = "lineup_confirmed"      # XI confirmed -> highest confidence the inputs allow
CONF_BASIS_PROBABLE = "probable"          # probable XI -> medium
MIN_RANK_VALUE = 1e-4                      # drop ~zero entries from rankings (no fake names)


# ----------------------------------------------------------------- Poisson helpers
def p_ge1(lam: float) -> float:
    """P(X>=1) for X~Poisson(lam)."""
    lam = max(float(lam or 0.0), 0.0)
    return 1.0 - math.exp(-lam)


def p_ge2(lam: float) -> float:
    """P(X>=2) for X~Poisson(lam) = 1 - P(0) - P(1)."""
    lam = max(float(lam or 0.0), 0.0)
    return 1.0 - math.exp(-lam) * (1.0 + lam)


def _round(x, n=4):
    return None if x is None else round(float(x), n)


# ----------------------------------------------------------------- per-player expansion
def expand_player(row: dict, xa90: Optional[float] = None, key_passes90: Optional[float] = None,
                  real: Optional[dict] = None) -> dict:
    """Expand one per-player prop row into the full event metric set.

    Two data regimes, clearly flagged (spec §3):
      * PROXY (default): goal/assist/shot λ's are the model's heuristic per-match expectations.
      * REAL xG/xA (Fase 3): if `real` carries xg90/xa90/shots90/sot90 (from player_xg_xa.csv via the
        adapter), those REPLACE the corresponding proxy λ for a near-full-match starter — per-field, so
        a partial source (e.g. only xg90) still keeps the proxy for the rest. NEVER fabricated: a missing
        real field falls back to the proxy and is labelled as proxy.

    `xa90`/`key_passes90` kwargs remain DISPLAY-only (expected_xa / expected_key_passes), as in Fase 1.
    `real` (when present) takes precedence for both the λ adjustment and the displayed xA/key passes.

    Expects row keys: player, team, player_id, is_xi, basis, lam_goal, exp_shots, lam_shot_on,
    lam_assist, p_card. Returns a flat dict with probabilities + expected values + per-player
    data_quality/confidence/reason + source_used (real_xg_xa/proxy) and per-metric source flags.
    """
    real = real or {}
    r_xg = real.get("xg90")
    r_xa = real.get("xa90")
    r_shots = real.get("shots90")
    r_son = real.get("sot90")
    r_kp = real.get("key_passes90")

    lam_goal_proxy = float(row.get("lam_goal") or 0.0)
    lam_shots_proxy = float(row.get("exp_shots") or 0.0)
    lam_son_proxy = float(row.get("lam_shot_on") or 0.0)
    lam_assist_proxy = float(row.get("lam_assist") or 0.0)

    # per-metric: real if supplied, else proxy
    lam_goal = float(r_xg) if r_xg is not None else lam_goal_proxy
    lam_assist = float(r_xa) if r_xa is not None else lam_assist_proxy
    lam_shots = float(r_shots) if r_shots is not None else lam_shots_proxy
    lam_son = float(r_son) if r_son is not None else lam_son_proxy

    goal_src = "real" if r_xg is not None else "proxy"
    assist_src = "real" if r_xa is not None else "proxy"
    shots_src = "real" if (r_shots is not None or r_son is not None) else "proxy"
    used_real = any(v is not None for v in (r_xg, r_xa, r_shots, r_son))

    # display extras: real first, then the legacy kwarg, else None (never invented)
    disp_xa = r_xa if r_xa is not None else xa90
    disp_kp = r_kp if r_kp is not None else key_passes90

    p_card = row.get("p_card")
    basis = str(row.get("basis") or "")

    dq, conf, reason = _player_confidence(row)
    if used_real:
        bits = [k for k, s in (("xG", goal_src), ("xA", assist_src), ("tiros/SOT", shots_src))
                if s == "real"]
        reason = (reason + " · " if reason else "") + f"datos reales: {', '.join(bits)} (fuente externa)"

    out = {
        "player": row.get("player"),
        "team": row.get("team"),
        "player_id": row.get("player_id"),
        "is_xi": int(row.get("is_xi") or 0),
        # goals
        "probability_goal": _round(p_ge1(lam_goal)),
        "expected_goals": _round(lam_goal),
        # shots / shots on target
        "expected_shots": _round(lam_shots),
        "probability_1plus_shot": _round(p_ge1(lam_shots)),
        "probability_2plus_shot": _round(p_ge2(lam_shots)),
        "expected_sot": _round(lam_son),
        "probability_1plus_sot": _round(p_ge1(lam_son)),
        "probability_2plus_sot": _round(p_ge2(lam_son)),
        # assists / creation
        "probability_assist": _round(p_ge1(lam_assist)),
        "expected_assists": _round(lam_assist),
        # creation extras come ONLY from an external adapter (else None, never invented)
        "expected_key_passes": _round(disp_kp) if disp_kp is not None else None,
        "expected_xa": _round(disp_xa) if disp_xa is not None else None,
        # cards (p_card already produced by the model, possibly bias-corrected upstream)
        "probability_card": _round(float(p_card)) if p_card is not None else None,
        "basis": basis,
        # provenance (spec §3 / §9): real_xg_xa vs proxy, per metric
        "source_used": "real_xg_xa" if used_real else "proxy",
        "goal_source": goal_src,
        "assist_source": assist_src,
        "shots_source": shots_src,
        "data_quality": dq,
        "confidence": conf,
        "reason": reason,
    }
    return out


def _player_confidence(row: dict):
    """Honest (data_quality, confidence, reason) for a single player from XI basis + λ availability."""
    basis = str(row.get("basis") or "")
    has_rates = any(row.get(k) not in (None, 0, 0.0) for k in ("lam_goal", "exp_shots", "lam_assist"))
    if not has_rates:
        return "baja", "baja", "sin tasas por jugador (muestra insuficiente)"
    if basis == CONF_BASIS_HIGH:
        return "alta", "media", "XI confirmado; tasas heurísticas por reparto de total de equipo"
    if basis.startswith(CONF_BASIS_PROBABLE):
        return "media", "media", "XI probable (se actualiza con alineación oficial)"
    return "media", "baja", "base de XI no confirmada"


# ----------------------------------------------------------------- rankings
def rank_top(expanded: list, value_key: str, n: int = 3, min_value: float = MIN_RANK_VALUE) -> list:
    """Top-n players by a metric, dropping ~zero entries (never pad with fabricated names)."""
    pool = [e for e in expanded if (e.get(value_key) or 0.0) > min_value]
    pool.sort(key=lambda e: e.get(value_key) or 0.0, reverse=True)
    return pool[:n]


def _scorer_reason(e):
    return (f"xG {e['expected_goals']:.2f}, P(gol) {e['probability_goal']*100:.0f}% "
            f"({e['confidence']})")


def likely_scorers(expanded, n=3):
    return [{"player": e["player"], "team": e["team"], "probability_goal": e["probability_goal"],
             "expected_goals": e["expected_goals"], "reason": _scorer_reason(e),
             "source_used": e.get("source_used", "proxy"), "goal_source": e.get("goal_source", "proxy"),
             "confidence": e["confidence"], "data_quality": e["data_quality"]}
            for e in rank_top(expanded, "expected_goals", n)]


def likely_shots_on_target(expanded, n=3):
    out = []
    for e in rank_top(expanded, "expected_sot", n):
        out.append({"player": e["player"], "team": e["team"],
                    "probability_1_sot": e["probability_1plus_sot"], "expected_sot": e["expected_sot"],
                    "expected_shots": e["expected_shots"],
                    "reason": f"tiros esp. {e['expected_shots']:.1f}, SOT esp. {e['expected_sot']:.1f} "
                              f"({e['confidence']})",
                    "source_used": e.get("source_used", "proxy"),
                    "shots_source": e.get("shots_source", "proxy"),
                    "confidence": e["confidence"], "data_quality": e["data_quality"]})
    return out


def likely_assisters(expanded, n=3):
    out = []
    for e in rank_top(expanded, "expected_assists", n):
        kp = e.get("expected_key_passes")
        a_src = e.get("assist_source", "proxy")
        label = "xA real" if a_src == "real" else "xA-proxy"
        out.append({"player": e["player"], "team": e["team"],
                    "probability_assist": e["probability_assist"], "expected_assists": e["expected_assists"],
                    "expected_key_passes": kp,
                    "reason": f"{label} {e['expected_assists']:.2f}"
                              + ("" if kp is None else f", pases clave esp. {kp:.1f}")
                              + f" ({e['confidence']})",
                    "source_used": e.get("source_used", "proxy"), "assist_source": a_src,
                    "confidence": e["confidence"], "data_quality": e["data_quality"]})
    return out


def card_risk(expanded, n=4, min_p=0.12):
    """Players with the highest modelled card probability (only above a floor; honest, low-conf market)."""
    pool = [e for e in expanded if (e.get("probability_card") or 0.0) >= min_p]
    pool.sort(key=lambda e: e.get("probability_card") or 0.0, reverse=True)
    out = []
    for e in pool[:n]:
        out.append({"player": e["player"], "team": e["team"], "probability_card": e["probability_card"],
                    "reason": f"P(tarjeta) {e['probability_card']*100:.0f}% — mercado de tarjeta es "
                              f"baja confianza ({e['confidence']})",
                    "confidence": "baja", "data_quality": e["data_quality"]})
    return out


# ----------------------------------------------------------------- set-piece hierarchy (§4)
def set_piece_hierarchy(xi_player_ids, names_by_id, penalty_history=None, injured_ids=None,
                        corner_history=None, fk_history=None, last_taken=None, full_history=None):
    """Detect set-piece takers from REAL history (counts by player). NEVER fabricates a taker: if no
    history is supplied, returns 'no determinado' + reason (the events extractor populates it, Fase 2).

    penalty_history / corner_history / fk_history: {player_id: count} from /fixtures/events or an
    external file. injured_ids: players absent from the probable XI. last_taken: {pid:{date,scored}}
    for the penalty explainer. full_history: the GLOBAL {pid: count} (incl. players NOT in the XI) so we
    can explain "the usual taker is not in the XI -> who takes it instead".
    Returns the §11 set_piece_takers structure (penalties block carries the §3 explainer fields).
    """
    xi = set(int(p) for p in (xi_player_ids or []))
    injured = set(int(p) for p in (injured_ids or []))
    last_taken = last_taken or {}

    def _rank(hist):
        if not hist:
            return {"primary": None, "secondary": None, "confidence": "baja",
                    "reason": "sin historial de eventos (no determinado)"}
        avail = {int(pid): c for pid, c in hist.items()
                 if int(pid) in xi and int(pid) not in injured and c > 0}
        # was there a usual taker who is NOT available in this XI? (explains the promotion)
        global_top = None
        if full_history:
            gorder = sorted(((int(p), c) for p, c in full_history.items() if c > 0),
                            key=lambda kv: kv[1], reverse=True)
            global_top = gorder[0][0] if gorder else None
        if not avail:
            return {"primary": None, "secondary": None, "confidence": "baja",
                    "reason": "lanzador habitual ausente del XI probable (no determinado para este XI)"}
        order = sorted(avail.items(), key=lambda kv: kv[1], reverse=True)
        primary_id, top = order[0]
        secondary_id = order[1][0] if len(order) > 1 else None
        total = sum(avail.values())
        share = top / total if total else 0.0
        conf = "alta" if (top >= 3 and share >= 0.6) else ("media" if top >= 2 else "baja")
        reason = f"más lanzamientos registrados ({top}); {share*100:.0f}% del XI disponible"
        out = {"primary": names_by_id.get(primary_id),
               "secondary": names_by_id.get(secondary_id) if secondary_id else None,
               "confidence": conf, "reason": reason,
               "primary_count": top,
               "primary_last": last_taken.get(primary_id)}
        # §3 explainer: usual taker out of the XI -> promoted alternative
        if global_top is not None and global_top not in avail:
            out["if_primary_absent"] = (f"el lanzador habitual no está en el XI probable; "
                                        f"asumiría {names_by_id.get(primary_id)}")
            out["confidence"] = "media" if conf == "alta" else "baja"
        else:
            out["if_primary_absent"] = (f"si {names_by_id.get(primary_id)} no juega, asumiría "
                                        f"{names_by_id.get(secondary_id)}" if secondary_id
                                        else "sin suplente claro de lanzador")
        return out

    pen = _rank(penalty_history)
    fk = _rank(fk_history)
    ck = _rank(corner_history)
    ck_note = " · sin split izq/der (requiere dato de lado · Fase 3)"
    ck_left = dict(ck); ck_left["reason"] = ck["reason"] + ck_note
    ck_right = dict(ck); ck_right["reason"] = ck["reason"] + ck_note
    return {"penalties": pen, "direct_free_kicks": fk, "corners_left": ck_left, "corners_right": ck_right}


# ----------------------------------------------------------------- two-XI scenarios (§12)
def scenario_delta(probable_expanded, alternative_expanded):
    """Compare the team's likely-scorer/assist picture under probable vs alternative XI. Returns the
    list of players whose involvement changes the most (added/removed/shifted) — honest impact, no %
    invention. If alternative is None/empty -> single-scenario note."""
    if not alternative_expanded:
        return {"available": False, "reason": "XI alternativo no disponible (se usa solo XI probable)"}
    by_id_prob = {e["player_id"]: e for e in probable_expanded}
    by_id_alt = {e["player_id"]: e for e in alternative_expanded}
    changes = []
    for pid, alt in by_id_alt.items():
        if pid not in by_id_prob:
            changes.append({"player": alt["player"], "team": alt["team"], "change": "ENTRA",
                            "expected_goals_alt": alt["expected_goals"]})
    for pid, prob in by_id_prob.items():
        if pid not in by_id_alt:
            changes.append({"player": prob["player"], "team": prob["team"], "change": "SALE",
                            "expected_goals_probable": prob["expected_goals"]})
    return {"available": True, "changes": changes,
            "reason": "diferencias de XI probable vs alternativo (impacto cualitativo, sin % inventado)"}


# ----------------------------------------------------------------- key matchups (§7) — HEURISTIC, labelled
def key_matchups(home_summary, away_summary):
    """Heuristic matchup read from TEAM-LEVEL signal only (we lack positional/duel data in Fase 1).
    Returns a SMALL, clearly-labelled heuristic list; never claims a hard %.

    home_summary/away_summary: {team, attack_xg, def_concede_proxy, corner_dominance} (floats or None).
    """
    out = []

    def _avail(d):
        return d and d.get("attack_xg") is not None

    if not (_avail(home_summary) and _avail(away_summary)):
        return [{"zone": "general", "advantage": "no determinado",
                 "effect_on_prediction": "datos insuficientes para matchups individuales (Fase 3: requiere "
                 "datos posicionales/duelos)", "confidence": "baja"}]
    # attack vs defence (team level), labelled heuristic
    h_atk, a_atk = home_summary["attack_xg"], away_summary["attack_xg"]
    adv = home_summary["team"] if h_atk >= a_atk else away_summary["team"]
    out.append({
        "player_a": f"ataque {home_summary['team']}", "player_b": f"defensa {away_summary['team']}",
        "zone": "ataque-defensa (equipo)",
        "advantage": adv,
        "effect_on_prediction": f"mayor xG esperado favorece a {adv} en tiros/goles "
                                f"(heurística de equipo, no duelo individual)",
        "confidence": "baja",
    })
    return out


# ----------------------------------------------------------------- top-level assembly (§11)
def build_player_predictions(fixture_meta, home_expanded, away_expanded, set_piece_home, set_piece_away,
                             matchups, top_n=3, scenarios=None):
    """Assemble the §11 structured player_predictions object for one fixture. Pure dict; the caller
    serialises it. data_quality/confidence at fixture level summarise the per-player flags."""
    both = home_expanded + away_expanded
    n_players = len(both)
    n_with_rates = sum(1 for e in both if e["data_quality"] != "baja")
    if n_players == 0:
        fixture_dq, fixture_conf = "baja", "baja"
    elif n_with_rates / n_players >= 0.7:
        fixture_dq, fixture_conf = "media", "media"
    else:
        fixture_dq, fixture_conf = "baja", "baja"

    return {
        "fixture": fixture_meta,
        "data_quality": fixture_dq,
        "confidence": fixture_conf,
        "player_predictions": {
            "likely_scorers": likely_scorers(both, top_n),
            "likely_shots_on_target": likely_shots_on_target(both, top_n),
            "likely_assisters": likely_assisters(both, top_n),
            "set_piece_takers": {"home": set_piece_home, "away": set_piece_away},
            "card_risk": card_risk(both),
            "key_matchups": matchups,
        },
        "scenarios": scenarios or {"available": False, "reason": "XI alternativo no evaluado"},
    }
