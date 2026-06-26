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
        ident = {"ux": [0.0, 1.0], "uf": [0.0, 1.0]}
        self.iso = [dict(ident), dict(ident), dict(ident)]


def _table(rows):
    return [{"name": n, "points": p, "played": pl, "gd": gd} for n, p, pl, gd in rows]


# last group game, CERTAIN by points: A,B=4 with C,D=1 (ceiling 4) -> a draw (=5) guarantees top-2
# in every parallel outcome -> both le_vale_empate (0.97). Non-trivial and mathematically sound.
NONTRIVIAL_GROUPS = {"G": _table([("A", 4, 2, 2), ("B", 4, 2, 2), ("C", 1, 2, -2), ("D", 1, 2, -2)])}
NONTRIVIAL_TG = {k: "G" for k in ("A", "B", "C", "D")}
OM = {"our_home": 0.50, "our_draw": 0.27, "our_away": 0.23,
      "our_xg_home": 1.60, "our_xg_away": 1.00,
      "our_elo_home": 0.50, "our_elo_away": -0.50}


# ----------------------------------------------------------------- compute_context_adjustment
def test_nontrivial_group_is_adjusted():
    adj = BC.compute_context_adjustment(C, FakePred(), NONTRIVIAL_GROUPS, NONTRIVIAL_TG,
                                        "Group Stage - 3", "A", "B", OM)
    assert adj is not None
    # both sides 'le_vale_empate' (×0.97), picked up from the parallel-match enumerator
    assert adj["ctx_mult_home"] == C.MULT["le_vale_empate"] and adj["ctx_mult_away"] == C.MULT["le_vale_empate"]
    # xG scaled by the multipliers, recomputed via the module's machinery (ctx_xg rounded 2dp)
    assert adj["ctx_xg_home"] == round(1.60 * 0.97, 2)
    assert adj["ctx_xg_away"] == round(1.00 * 0.97, 2)
    # probs differ from pure L3 (the adjustment actually moved the prediction)
    assert abs(adj["ctx_home"] - OM["our_home"]) > 1e-4 or abs(adj["ctx_away"] - OM["our_away"]) > 1e-4
    assert "ajustado por contexto de grupo" in adj["context_note"]
    assert "A le vale el empate" in adj["context_note"] and "B le vale el empate" in adj["context_note"]


def test_knockout_is_not_adjusted():
    adj = BC.compute_context_adjustment(C, FakePred(), {}, {}, "Round of 16", "A", "B", OM)
    assert adj is None        # knockout -> trivial -> no ctx_* -> pure L3


def test_trivial_group_is_not_adjusted():
    # both teams already clinched (A,B=6; C,D=0 ceiling 3) -> dead rubber -> intrascendente (×1.0)
    # -> trivial -> None (no adjustment written).
    g = {"G": _table([("A", 6, 2, 3), ("B", 6, 2, 3), ("C", 0, 2, -3), ("D", 0, 2, -3)])}
    tg = {k: "G" for k in ("A", "B", "C", "D")}
    assert BC.compute_context_adjustment(C, FakePred(), g, tg, "Group Stage - 3", "A", "B", OM) is None


def test_soft_fail_returns_none():
    class Boom:
        @staticmethod
        def classify_fixture(*a, **k):
            raise RuntimeError("boom")
    assert BC.compute_context_adjustment(Boom, FakePred(), {}, {}, "Group Stage - 3", "A", "Y", OM) is None
    assert BC.compute_context_adjustment(None, FakePred(), {}, {}, "Group Stage - 3", "A", "Y", OM) is None


def test_adjustment_never_touches_our_fields():
    adj = BC.compute_context_adjustment(C, FakePred(), NONTRIVIAL_GROUPS, NONTRIVIAL_TG,
                                        "Group Stage - 3", "A", "B", OM)
    assert all(not k.startswith("our_") for k in adj)   # only ctx_*/context_note are produced


# ----------------------------------------------------------------- A/B coherence with the shadow
def test_live_ctx_matches_shadow_ctx():
    # the live adjustment must equal the SHADOW context_predict ctx_* for the same (xg, mult):
    # both call adjust_prediction with the same inputs -> identical (single source of truth).
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


def test_pred_1x2_falls_back_to_l3_without_ctx():
    lh, ld, la, xgh, xga, note = F.pred_1x2(_row())      # no ctx_* -> rollback to pure L3
    assert lh == 0.50 and la == 0.23 and xgh == 1.60 and note is None


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
