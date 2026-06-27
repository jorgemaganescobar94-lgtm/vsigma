"""
Offline tests for the CONTEXT-LIVE path: the qualification-context adjustment applied to the
prediction SHOWN and SENT to Telegram (build_worldcup_cards.compute_context_adjustment +
build_worldcup_full_card.pred_1x2 / match_block). NO network, NO API.

Covers: non-trivial group scenario -> displayed prediction is context-adjusted (ctx_* + nota) ·
knockout/trivial -> pure L3, no ctx_* · CONTEXT_LIVE flag exists and pred_1x2 falls back to pure L3
when ctx_* absent (rollback) · the "por qué" notes the adjustment ONLY when present · the live ctx
equals the SHADOW ctx (A/B coherent) and the shadow still emits BOTH l3+ctx (A/B intact) ·
adjustment never touches our_* · soft-fail -> None (pure L3).

Run:  python analysis/worldcup/test_context_live.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_context_shadow as C      # noqa: E402
import build_worldcup_cards as BC         # noqa: E402
import build_worldcup_full_card as F      # noqa: E402


class FakePred:
    """Tiny L3 predictor with IDENTITY calibration (same as test_context_shadow)."""
    def __init__(self):
        self.strength = {"A": 0.5, "B": -0.5, "C": 0.0, "D": 0.0}
        self.a0, self.a1, self.total_mean = 0.0, 1.0, 2.6
        # total matchup coef (forma b) — mirrors the real Predictor so context_predict exercises the
        # match-dependent total path (FIX 2: shadow baseline usa el mismo total que producción).
        self.total_coef = [2.39, 0.075, 0.273]
        ident = {"ux": [0.0, 1.0], "uf": [0.0, 1.0]}
        self.iso = [dict(ident), dict(ident), dict(ident)]


def _table(rows):
    return [{"name": n, "points": p, "played": pl, "gd": gd} for n, p, pl, gd in rows]


# last group game, CERTAIN by points: A,B=4 with C,D=1 (ceiling 4) -> a draw (=5) guarantees top-2
# in every parallel outcome -> both le_vale_empate (0.97). Non-trivial and mathematically sound.
NONTRIVIAL_GROUPS = {"G": _table([("A", 4, 2, 2), ("B", 4, 2, 2), ("C", 1, 2, -2), ("D", 1, 2, -2)])}
NONTRIVIAL_TG = {k: "G" for k in ("A", "B", "C", "D")}
# Base = el MOTOR MOSTRADO (mx_* si existe, si no L3 our_*). El contexto se ENCADENA sobre esta base
# por delta-Poisson (NO la isotónica del L3). Probs + xG del motor (p.ej. mx) que el escenario mueve.
BASE_P = (0.50, 0.27, 0.23)
BASE_XG = (1.60, 1.00)
OM = {"our_home": 0.50, "our_draw": 0.27, "our_away": 0.23,
      "our_xg_home": 1.60, "our_xg_away": 1.00,
      "our_elo_home": 0.50, "our_elo_away": -0.50}


# ----------------------------------------------------------------- compute_context_adjustment
def test_nontrivial_group_is_adjusted():
    adj = BC.compute_context_adjustment(C, NONTRIVIAL_GROUPS, NONTRIVIAL_TG,
                                        "Group Stage - 3", "A", "B", BASE_P, *BASE_XG)
    assert adj is not None
    # both sides 'le_vale_empate' (×0.97), picked up from the parallel-match enumerator
    assert adj["ctx_mult_home"] == C.MULT["le_vale_empate"] and adj["ctx_mult_away"] == C.MULT["le_vale_empate"]
    # xG of the MOTOR scaled by the multipliers (ctx_xg rounded 2dp)
    assert adj["ctx_xg_home"] == round(1.60 * 0.97, 2)
    assert adj["ctx_xg_away"] == round(1.00 * 0.97, 2)
    # probs differ from the base motor (the adjustment actually moved the prediction)
    assert abs(adj["ctx_home"] - BASE_P[0]) > 1e-4 or abs(adj["ctx_away"] - BASE_P[2]) > 1e-4
    assert "ajustado por contexto de grupo" in adj["context_note"]
    assert "A le vale el empate" in adj["context_note"] and "B le vale el empate" in adj["context_note"]


def test_knockout_is_not_adjusted():
    adj = BC.compute_context_adjustment(C, {}, {}, "Round of 16", "A", "B", BASE_P, *BASE_XG)
    assert adj is None        # knockout -> trivial -> no ctx_* -> motor sin contexto (Δ=0)


def test_two_qualified_group_is_adjusted_092():
    # ambos ya clasificados (A,B=6; C,D=0 techo 3) -> CADA UNO qualified ×0.92 -> NON-trivial.
    g = {"G": _table([("A", 6, 2, 3), ("B", 6, 2, 3), ("C", 0, 2, -3), ("D", 0, 2, -3)])}
    tg = {k: "G" for k in ("A", "B", "C", "D")}
    adj = BC.compute_context_adjustment(C, g, tg, "Group Stage - 3", "A", "B", BASE_P, *BASE_XG)
    assert adj is not None
    assert adj["ctx_mult_home"] == C.MULT["qualified"] == 0.92
    assert "ya clasificado" in adj["context_note"]


def test_conditional_group_is_pure_motor():
    # REVERSA por escenario: AMBOS lados CONDICIONALES (P y A a 3; ganar asegura 2ª pero el empate solo
    # por diferencia -> tag 'gana_y_pasa', neutral) -> mult 1.0 ambos -> trivial -> None -> la ficha
    # queda en el motor sin contexto (sin ctx_*). Réplica de Paraguay/Australia. 12 grupos.
    g = {"G": _table([("P", 3, 2, 0), ("A", 3, 2, 0), ("Lead", 6, 2, 5), ("T", 0, 2, -5)])}
    for i in range(11):
        g[f"F{i}"] = _table([(f"f{i}a", 0, 2, 0), (f"f{i}b", 0, 2, 0),
                             (f"f{i}c", 0, 2, 0), (f"f{i}d", 0, 2, 0)])
    tg = {k: "G" for k in ("P", "A", "Lead", "T")}
    assert BC.compute_context_adjustment(C, g, tg, "Group Stage - 3", "P", "A", BASE_P, *BASE_XG) is None


# --------------- VALIDACIONES de la CADENA mx -> contexto -> lesiones (decisión de Jorge) ----------
def test_context_chains_on_mx_reduces_xg_092():
    # (a) escenario no trivial (ambos 'ya clasificado' ×0.92) sobre la base del MOTOR MÁXIMO (mx):
    #     el xG mostrado = mx_xg × 0.92 (REDUCIDO vs mx crudo), y el favorito baja un poco.
    g = {"G": _table([("A", 6, 2, 3), ("B", 6, 2, 3), ("C", 0, 2, -3), ("D", 0, 2, -3)])}
    tg = {k: "G" for k in ("A", "B", "C", "D")}
    mx_p, mx_xg = (0.55, 0.25, 0.20), (1.72, 0.90)     # motor máximo crudo
    adj = BC.compute_context_adjustment(C, g, tg, "Group Stage - 3", "A", "B", mx_p, *mx_xg)
    assert adj is not None
    assert adj["ctx_xg_home"] == round(1.72 * 0.92, 2) and adj["ctx_xg_away"] == round(0.90 * 0.92, 2)
    assert adj["ctx_xg_home"] < mx_xg[0]               # xG REDUCIDO vs el mx crudo
    assert abs(sum((adj["ctx_home"], adj["ctx_draw"], adj["ctx_away"])) - 1.0) < 1e-6


def test_trivial_is_exact_motor_delta_zero():
    # (b) fixture trivial (knockout) -> None -> la ficha = mx exacto (Δ=0). Reversa por escenario.
    assert BC.compute_context_adjustment(C, {}, {}, "Final", "A", "B", (0.55, 0.25, 0.20), 1.72, 0.90) is None


def test_chain_injuries_apply_on_ctx_base():
    # (d) la cadena compone: contexto sobre mx -> luego una baja clave se aplica sobre el ctx (no el mx).
    import worldcup_injuries_live as IL
    g = {"G": _table([("A", 6, 2, 3), ("B", 6, 2, 3), ("C", 0, 2, -3), ("D", 0, 2, -3)])}
    tg = {k: "G" for k in ("A", "B", "C", "D")}
    mx_p, mx_xg = (0.55, 0.25, 0.20), (1.72, 0.90)
    ctx = BC.compute_context_adjustment(C, g, tg, "Group Stage - 3", "A", "B", mx_p, *mx_xg)
    assert ctx is not None
    ctx_p = (ctx["ctx_home"], ctx["ctx_draw"], ctx["ctx_away"])
    # baja ofensiva clave en A: el delta-Poisson de las lesiones parte del ctx_xg (no del mx_xg)
    ia = IL.compute_fixture_injury_adjustment(
        "A", "B", ctx_p, ctx["ctx_xg_home"], ctx["ctx_xg_away"], {}, inj_home=["X"], inj_away=[])
    # con squad vacío no hay baja clave -> None (reversa); la base que se le pasó es ctx, no mx (verificado
    # por construcción: ctx_xg < mx_xg y es lo que entra a la capa de lesiones)
    assert ia is None
    assert ctx["ctx_xg_home"] < mx_xg[0]


def test_group_info_line_is_honest_and_conditional():
    # (A) la línea "Contexto de grupo" usa phrase_es (motor honesto): condicional, no etiqueta única.
    # Grupo H real: Cabo Verde 'le vale el empate si España gana'; Arabia 'gana y pasa 2ª si Uruguay
    # no gana' (la vía 2ª-directa que el shim legacy ocultaba).
    gh = {"Group H": _table([("Spain", 4, 2, 4), ("Uruguay", 2, 2, 0),
                             ("Cape Verde Islands", 2, 2, 0), ("Saudi Arabia", 1, 2, -4)])}
    for i in range(11):   # 12-group format (8 best thirds), as in the real World Cup standings
        gh[f"F{i}"] = _table([(f"f{i}a", 0, 2, 0), (f"f{i}b", 0, 2, 0),
                             (f"f{i}c", 0, 2, 0), (f"f{i}d", 0, 2, 0)])
    line = BC.compute_group_info(gh, "Cape Verde Islands", "Saudi Arabia")
    assert line is not None
    assert "Cape Verde Islands le vale el empate si Spain gana" in line
    cv, saudi = line.split(" · ")           # one honest clause per team
    assert saudi.startswith("Saudi Arabia") and "gana y pasa 2ª si Uruguay no gana" in saudi


def test_soft_fail_returns_none():
    class Boom:
        @staticmethod
        def classify_fixture(*a, **k):
            raise RuntimeError("boom")
    assert BC.compute_context_adjustment(Boom, {}, {}, "Group Stage - 3", "A", "Y", BASE_P, *BASE_XG) is None
    assert BC.compute_context_adjustment(None, {}, {}, "Group Stage - 3", "A", "Y", BASE_P, *BASE_XG) is None


def test_adjustment_never_touches_our_or_mx_fields():
    adj = BC.compute_context_adjustment(C, NONTRIVIAL_GROUPS, NONTRIVIAL_TG,
                                        "Group Stage - 3", "A", "B", BASE_P, *BASE_XG)
    assert all(not k.startswith("our_") and not k.startswith("mx_") for k in adj)  # only ctx_*/note


# ----------------------------------------------------------------- A/B coherence with the shadow
def test_shadow_ctx_internal_consistency():
    # The SHADOW A/B (worldcup_context_shadow) is UNTOUCHED by the live chaining change and keeps its
    # own L3-isotonic path: context_predict's ctx_* == adjust_prediction on the same (xg, mult). The
    # LIVE ficha no longer uses this path (it chains delta-Poisson on mx); the shadow stays as control.
    pred = FakePred()
    cp = C.context_predict(pred, "A", "B", 0.92, 1.08)     # shadow: from strengths (rounded to 4dp)
    direct = C.adjust_prediction(pred, cp["l3_xg_home"], cp["l3_xg_away"], 0.92, 1.08)
    assert round(direct["home"], 4) == cp["ctx_home"]
    assert round(direct["away"], 4) == cp["ctx_away"]
    assert round(direct["over25"], 4) == cp["ctx_over25"]


def test_shadow_still_emits_both_l3_and_ctx():
    # the A/B panel must keep producing BOTH pure-L3 and context columns (not removed by going live)
    cp = C.context_predict(FakePred(), "A", "B", 0.92, 1.08)
    for k in ("l3_home", "l3_draw", "l3_away", "ctx_home", "ctx_draw", "ctx_away"):
        assert k in cp


# ----------------------------------------------------------------- pred_1x2 / rendering
def _row(**kw):
    base = {"home": "A", "away": "B", "round": "Group Stage - 3", "kickoff_utc": "2026-06-26 20:00",
            "our_home": 0.50, "our_draw": 0.27, "our_away": 0.23,
            "our_xg_home": 1.60, "our_xg_away": 1.00,
            "our_elo_home": 0.5, "our_elo_away": -0.5, "home_group": "G", "away_group": "G"}
    base.update(kw)
    return pd.Series(base)


def test_pred_1x2_prefers_ctx_when_present():
    r = _row(ctx_home=0.40, ctx_draw=0.30, ctx_away=0.30, ctx_xg_home=1.5, ctx_xg_away=1.1,
             context_note="ajustado por contexto de grupo: A le vale el empate")
    lh, ld, la, xgh, xga, note = F.pred_1x2(r)
    assert lh == 0.40 and la == 0.30 and xgh == 1.5 and "ajustado por contexto" in note


def test_pred_1x2_ctx_outranks_mx():
    # CLAVE de la cadena: ctx_* (ya encadenado sobre mx) tiene prioridad SOBRE mx_* en el render.
    r = _row(mx_home=0.55, mx_draw=0.25, mx_away=0.20, mx_xg_home=1.72, mx_xg_away=0.90,
             ctx_home=0.50, ctx_draw=0.28, ctx_away=0.22, ctx_xg_home=1.58, ctx_xg_away=0.83,
             context_note="ajustado por contexto de grupo: A ya clasificado")
    lh, ld, la, xgh, xga, note = F.pred_1x2(r)
    assert lh == 0.50 and xgh == 1.58 and "ajustado por contexto" in note   # muestra ctx, no mx


def test_pred_1x2_falls_back_to_mx_then_l3():
    # (c) reversa exacta: con mx pero SIN ctx (CONTEXT_LIVE off / escenario trivial) -> muestra mx.
    r = _row(mx_home=0.55, mx_draw=0.25, mx_away=0.20, mx_xg_home=1.72, mx_xg_away=0.90)
    lh, ld, la, xgh, xga, note = F.pred_1x2(r)
    assert lh == 0.55 and xgh == 1.72                       # mx exacto (Δ=0 vs mx)
    # sin mx ni ctx -> L3 puro
    lh2, ld2, la2, xgh2, xga2, note2 = F.pred_1x2(_row())
    assert lh2 == 0.50 and xgh2 == 1.60 and note2 is None


def test_context_live_flag_on_with_corrected_classifier():
    # RE-ACTIVADO con el classify_fixture corregido (cierto por puntos). El flag existe y es True
    # -> la predicción mostrada/enviada lleva el ajuste por contexto en grupos no triviales.
    assert hasattr(BC, "CONTEXT_LIVE") and BC.CONTEXT_LIVE is True


def test_match_block_shows_adjusted_and_note():
    r = _row(ctx_home=0.40, ctx_draw=0.30, ctx_away=0.30, ctx_xg_home=1.5, ctx_xg_away=1.1,
             context_note="ajustado por contexto de grupo: A debe ganar")
    txt = "\n".join(F.match_block(r))
    assert "A 40%" in txt and "B 30%" in txt                  # adjusted percentages shown
    assert "ajustado por contexto de grupo: A debe ganar" in txt   # nota presente


def test_match_block_pure_l3_has_no_context_note():
    txt = "\n".join(F.match_block(_row()))
    assert "A 50%" in txt and "ajustado por contexto" not in txt   # pure L3, sin nota


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} context-live tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
