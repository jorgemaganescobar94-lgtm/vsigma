"""
Human-readable "POR QUÉ" for each Layer-3 World Cup prediction. PURE RENDERING — it only
formats numbers the prediction ALREADY produced (team strengths, neutral venue, xG, probs,
and the optional injury adjustment). It does NOT call the model, recompute ratings, or hit
any API. Soft by design: on any bad/missing input it returns "" so the card renders unchanged.

Honest framing (mandatory): states it uses ONLY the own historical national-team rating,
WITHOUT market/odds, and that it is probabilistic. No certainty language. If there is no
injury adjustment, no adjustment line is shown (nothing invented).
"""
from __future__ import annotations


def _num(x):
    try:
        v = float(x)
        return v if v == v else None  # reject NaN
    except (TypeError, ValueError):
        return None


def _level(margin: float) -> str:
    """Honest favouritism wording from the rating margin — never asserts certainty."""
    if margin < 0.45:
        return "ligero favorito"
    if margin < 0.95:
        return "favorito"
    if margin < 1.70:
        return "favorito claro"
    return "muy favorito"


def explain_l3(home, away, s_home, s_away, neutral,
               xg_home, xg_away, p_home, p_draw, p_away,
               adj_basis=None, adj_absent_home=None, adj_absent_away=None,
               adj_delta_home=None, adj_delta_away=None) -> str:
    """Build the 'Por qué:' sentence from already-computed fields. '' if strength missing."""
    sh, sa = _num(s_home), _num(s_away)
    if sh is None or sa is None:
        return ""
    sup = sh - sa  # supremacy = exactly the difference of the shown strengths (no recompute)

    if abs(sup) < 0.15:
        head = f"{home} y {away} muy parejos — ratings casi iguales ({sh:+.2f} vs {sa:+.2f})"
    else:
        fav, oth, margin = (home, away, sup) if sup > 0 else (away, home, -sup)
        head = f"{fav} {_level(margin)} — rating +{margin:.2f} sobre {oth}"
    parts = [f"Por qué: {head} (modelo propio de selecciones, sin mercado/cuotas)."]

    # venue: WC is neutral -> no home advantage. (neutral falsy would imply a home edge.)
    is_neutral = True if neutral is None else bool(int(neutral)) if str(neutral).strip() not in ("", "nan") else True
    parts.append("Campo neutral: sin ventaja local." if is_neutral
                 else f"Local {home}: leve ventaja de campo.")

    # injury adjustment — ONLY if present (never invented)
    bits = []
    for team, delta, absent in ((home, adj_delta_home, adj_absent_home),
                                (away, adj_delta_away, adj_absent_away)):
        dv = _num(delta)
        has_abs = isinstance(absent, str) and absent.strip() and absent.strip().lower() != "nan"
        if (dv is not None and abs(dv) >= 0.005) or has_abs:
            seg = f"{team} {dv:+.2f}" if dv is not None else f"{team}"
            if has_abs:
                seg += f" (sin {absent.strip()})"
            bits.append(seg)
    if bits:
        parts.append("Bajas clave: " + " · ".join(bits) + ".")

    xh, xa = _num(xg_home), _num(xg_away)
    ph, pd_, pa = _num(p_home), _num(p_draw), _num(p_away)
    if None not in (xh, xa, ph, pd_, pa):
        parts.append(f"Es probabilístico → xG {xh:.1f}-{xa:.1f}, "
                     f"prob {ph * 100:.0f}/{pd_ * 100:.0f}/{pa * 100:.0f}%.")
    return " ".join(parts)


def explain_l3_clean(home, away, s_home, s_away, neutral,
                     adj_absent_home=None, adj_absent_away=None,
                     adj_delta_home=None, adj_delta_away=None) -> str:
    """Natural-language 'por qué' for the CLEAN format: WHY the model favours a side, in words,
    WITHOUT jargon (no 'rating'/'xG') and WITHOUT the honesty tail or the prob/xG restatement
    (those live in the headline, the Goles section and the single footer note). Pure rendering; ''
    if strength missing. 'rating' is explained as 'plantilla histórica más fuerte'."""
    sh, sa = _num(s_home), _num(s_away)
    if sh is None or sa is None:
        return ""
    sup = sh - sa
    if abs(sup) < 0.15:
        parts = [f"{home} y {away} están muy parejos (fuerza de plantilla casi igual)"]
    else:
        fav, oth, margin = (home, away, sup) if sup > 0 else (away, home, -sup)
        parts = [f"{fav} es {_level(margin)}: su plantilla histórica es más fuerte "
                 f"(ventaja de {margin:.2f} sobre {oth})"]
    is_neutral = True if neutral is None else bool(int(neutral)) if str(neutral).strip() not in ("", "nan") else True
    parts.append("campo neutral, sin ventaja local" if is_neutral else f"{home} juega en casa (leve ventaja)")
    bits = []
    for team, delta, absent in ((home, adj_delta_home, adj_absent_home),
                                (away, adj_delta_away, adj_absent_away)):
        has_abs = isinstance(absent, str) and absent.strip() and absent.strip().lower() != "nan"
        if has_abs:
            bits.append(f"{team} sin {absent.strip()}")
    tail = f". Bajas clave: {' · '.join(bits)}." if bits else "."
    return parts[0] + " — " + parts[1] + tail


# --------------------------------------------------------------------------------------------------
# PER-METRIC "PORQUÉ" HELPERS (clean card). Each verbalises the REAL driver of ONE shown number, as
# the code computes it (verified against national_elo_layer3.probs / build_worldcup_full_card /
# worldcup_player_props.predict_fixture / stats_model.Predictor.predict). Pure rendering, no recompute,
# no market, no invented football narrative. Any bad/missing input -> "" (soft-fail: the card drops
# the sub-line, never breaks). Probabilistic language only, never certainty.
# --------------------------------------------------------------------------------------------------
def explain_goals_clean(home, away, xg_home, xg_away) -> str:
    """WHY these expected goals. REAL mechanism (national_elo_layer3.probs): the L3 model turns the
    rating SUPREMACY into the margin s=a0+a1·sup (which fixes the GAP xgh−xga) and a match-dependent
    TOTAL t (which fixes the SUM xgh+xga), then splits lh=(t+s)/2, la=(t−s)/2. It is NOT a per-team
    attack-vs-defence matchup (that would be Dixon-Coles) — so we say 'diferencia de fuerza' + 'total',
    faithfully."""
    xh, xa = _num(xg_home), _num(xg_away)
    if xh is None or xa is None:
        return ""
    total = xh + xa
    head = (f"Esos esperados salen del modelo de selecciones: la diferencia de fuerza fija la brecha "
            f"entre ambos y un total esperado ({total:.1f}) reparte los goles")
    if abs(xh - xa) < 0.25:
        return f"{head} — van muy parejos ({xh:.1f} y {xa:.1f})."
    fav, hi, lo = (home, xh, xa) if xh > xa else (away, xa, xh)
    return f"{head} — {fav} genera más ({hi:.1f} vs {lo:.1f})."


def explain_over25_clean(o25, xg_home, xg_away) -> str:
    """WHY this Over 2.5 %. REAL mechanism: o25 is the tail M[(gh+ga)>=3] of the independent-Poisson
    score_matrix(xgh,xga); the total esperado is exactly xgh+xga. So Over 2.5 tracks where that total
    sits relative to 2.5. o25 is the ALREADY-SHOWN probability (clamped)."""
    p, xh, xa = _num(o25), _num(xg_home), _num(xg_away)
    if p is None or xh is None or xa is None:
        return ""
    total = xh + xa
    if abs(total - 2.5) < 0.15:
        band = "pegado a 2.5 (muy repartido)"
    elif total >= 3.0:
        band = "bastante por encima de 2.5"
    elif total > 2.5:
        band = "justo por encima de 2.5"
    elif total > 2.0:
        band = "justo por debajo de 2.5"
    else:
        band = "bastante por debajo de 2.5"
    return f"Over 2.5 ≈ {p * 100:.0f}% porque el total esperado ({total:.1f}) cae {band}."


def explain_btts_clean(btts, home, away, xg_home, xg_away) -> str:
    """WHY this BTTS %. REAL mechanism: btts = M[(gh>=1)&(ga>=1)] = (1−e^−λh)(1−e^−λa) for the two
    independent Poissons; the BINDING term is the team with the LOWER expected goals (easier to keep
    scoreless). btts is the ALREADY-SHOWN probability."""
    p, xh, xa = _num(btts), _num(xg_home), _num(xg_away)
    if p is None or xh is None or xa is None:
        return ""
    if abs(xh - xa) < 0.25:
        return (f"BTTS {p * 100:.0f}% porque los dos generan parecido ({xh:.1f} y {xa:.1f}) "
                f"y pide que ambos marquen.")
    lo_team, lo_val = (home, xh) if xh < xa else (away, xa)
    return (f"BTTS {p * 100:.0f}% porque depende de que marque {lo_team}, "
            f"que solo genera {lo_val:.1f} esperados.")


def explain_scorelines_clean() -> str:
    """WHY these scorelines. REAL mechanism: they are the highest-probability cells of the same
    independent-Poisson score_matrix(xgh,xga). No recompute, no certainty."""
    return "Son los más probables según esa distribución de goles (Poisson por equipo con esos esperados)."


def explain_players_clean(card_deflated=False) -> str:
    """WHY the player props. REAL mechanism (worldcup_player_props.predict_fixture): per player
    λ = (goles/tiros/tarjetas esperados del equipo) × su cuota histórica /90 (encogida hacia la media
    del XI) ; el % = P(≥1) Poisson. Los tiros se muestran como ORDEN (exp_shots), sin %, porque su
    logloss no bate la tasa base. Si la deflación de tarjeta está activa, se dice con honestidad."""
    base = ("Cada % = ritmo histórico del jugador (por 90') repartiendo los goles/tarjetas esperados "
            "de su equipo, vía Poisson; los tiros son orden por volumen, no probabilidad.")
    if card_deflated:
        base += " La tarjeta va con corrección a la baja (el modelo la sobreestimaba)."
    return base


def explain_stats_clean(level_corrected=False) -> str:
    """WHY these córners/tiros. REAL mechanism (stats_model.Predictor.predict): per team
    λ = exp(mu + att[equipo] + conc[rival] + β·fuerza), i.e. la propensión propia cruzada con lo que
    concede el rival. Los córners/tiros MOSTRADOS llevan además una corrección de nivel ADITIVA AL
    ALZA cuando está activa (el modelo los subestimaba); se menciona solo si de verdad se aplica."""
    base = "Estimados cruzando la propensión de cada equipo con lo que concede el rival (modelo de datos)."
    if level_corrected:
        base += " Con corrección de nivel al alza en córners/tiros (el modelo los subestimaba)."
    return base
