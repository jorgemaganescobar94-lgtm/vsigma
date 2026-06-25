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
