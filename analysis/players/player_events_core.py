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
def expand_player(row: dict, xa90: Optional[float] = None, key_passes90: Optional[float] = None) -> dict:
    """Expand one per-player prop row into the full event metric set. Poisson from the model λ's only;
    xA / key passes come from an external adapter (None -> field None + reason, never fabricated).

    Expects row keys: player, team, player_id, is_xi, basis, lam_goal, exp_shots, lam_shot_on,
    lam_assist, p_card.  Returns a flat dict with probabilities + expected values + a per-player
    data_quality/confidence/reason.
    """
    lam_goal = float(row.get("lam_goal") or 0.0)
    lam_shots = float(row.get("exp_shots") or 0.0)
    lam_son = float(row.get("lam_shot_on") or 0.0)
    lam_assist = float(row.get("lam_assist") or 0.0)
    p_card = row.get("p_card")
    basis = str(row.get("basis") or "")

    dq, conf, reason = _player_confidence(row)

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
        "expected_key_passes": _round(key_passes90) if key_passes90 is not None else None,
        "expected_xa": _round(xa90) if xa90 is not None else None,
        # cards (p_card already produced by the model, possibly bias-corrected upstream)
        "probability_card": _round(float(p_card)) if p_card is not None else None,
        "basis": basis,
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
                    "confidence": e["confidence"], "data_quality": e["data_quality"]})
    return out


def likely_assisters(expanded, n=3):
    out = []
    for e in rank_top(expanded, "expected_assists", n):
        kp = e.get("expected_key_passes")
        out.append({"player": e["player"], "team": e["team"],
                    "probability_assist": e["probability_assist"], "expected_assists": e["expected_assists"],
                    "expected_key_passes": kp,
                    "reason": f"xA-proxy {e['expected_assists']:.2f}"
                              + ("" if kp is None else f", pases clave esp. {kp:.1f}")
                              + f" ({e['confidence']})",
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
                        corner_history=None, fk_history=None):
    """Detect set-piece takers from REAL recent history (counts by player). NEVER fabricates a taker:
    if no history is supplied, returns 'no determinado' + reason (requires the events extractor, Fase 2).

    penalty_history / corner_history / fk_history: optional {player_id: count} from /fixtures/events or
    an external file. injured_ids: players absent from the probable XI -> primary may be promoted.
    Returns the §11 set_piece_takers structure with primary/secondary/confidence per category.
    """
    xi = set(int(p) for p in (xi_player_ids or []))
    injured = set(int(p) for p in (injured_ids or []))

    def _rank(hist):
        if not hist:
            return None, None, "baja", "sin historial de eventos (requiere extractor de eventos · Fase 2)"
        # only players in the probable XI and available are eligible to take it in THIS match
        avail = {int(pid): c for pid, c in hist.items()
                 if int(pid) in xi and int(pid) not in injured and c > 0}
        if not avail:
            # the historical taker(s) exist but are not in the available XI -> flag it honestly
            return None, None, "baja", "lanzador habitual ausente del XI probable o sin datos en este XI"
        order = sorted(avail.items(), key=lambda kv: kv[1], reverse=True)
        primary = names_by_id.get(order[0][0])
        secondary = names_by_id.get(order[1][0]) if len(order) > 1 else None
        top = order[0][1]
        total = sum(avail.values())
        # confidence by dominance + sample
        share = top / total if total else 0.0
        if top >= 3 and share >= 0.6:
            conf = "alta"
        elif top >= 2:
            conf = "media"
        else:
            conf = "baja"
        reason = f"lanzador con más registros recientes ({top}); cuota {share*100:.0f}% del XI disponible"
        return primary, secondary, conf, reason

    pen_p, pen_s, pen_c, pen_r = _rank(penalty_history)
    fk_p, fk_s, fk_c, fk_r = _rank(fk_history)
    ck_p, ck_s, ck_c, ck_r = _rank(corner_history)

    return {
        "penalties": {"primary": pen_p, "secondary": pen_s, "confidence": pen_c, "reason": pen_r},
        "direct_free_kicks": {"primary": fk_p, "secondary": fk_s, "confidence": fk_c, "reason": fk_r},
        # left/right corner split needs foot/side data we don't have -> single corner list, honest note
        "corners_left": {"primary": ck_p, "secondary": ck_s, "confidence": ck_c,
                         "reason": ck_r + " · sin split izq/der (requiere dato de lado · Fase 2)"},
        "corners_right": {"primary": ck_p, "secondary": ck_s, "confidence": ck_c,
                          "reason": ck_r + " · sin split izq/der (requiere dato de lado · Fase 2)"},
    }


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
