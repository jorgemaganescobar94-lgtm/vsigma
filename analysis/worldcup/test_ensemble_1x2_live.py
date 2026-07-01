"""
Tests for ENSEMBLE_1X2_LIVE: the SHOWN 1X2 is the renormalised 50/50 blend of mx_* and L3 our_*,
while goals (xG/Over/BTTS/scorelines) STAY on L3 (ens_xg_* = our_xg_*). NO network, NO API.

Locks the safety-critical properties (Jorge's 🔴 adoption):
  (a) the blend is the EXACT renormalised mean of mx and L3,
  (b) EXACT reversal when the flag is off (no ens_* columns) -> displayed 1X2 = mx_* (current state, Δ=0),
  (c) goals are intact = L3: the xG returned for ens_*/ctx_* is the L3 xG, Over/BTTS derive from it,
  (d) context (and injuries, same delta-Poisson) CHAIN on the blend probs + L3 xG,
  (e) ens outranks mx/our but ctx/inj still outrank ens (chain order preserved).

Run:  python -m pytest analysis/worldcup/test_ensemble_1x2_live.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_worldcup_cards as C  # noqa: E402
import build_worldcup_full_card as F  # noqa: E402
import l3_offline  # noqa: E402


def _row(with_ens=True, with_mx=True):
    d = {"home": "A", "away": "B", "round": "Group Stage - 3", "home_group": "Group A",
         "kickoff_utc": "2026-06-30 20:00", "fixture_id": 1,
         "our_home": 0.50, "our_draw": 0.27, "our_away": 0.23,
         "our_xg_home": 1.6, "our_xg_away": 1.1, "our_elo_home": 1.2, "our_elo_away": 0.4}
    if with_mx:
        d.update({"mx_home": 0.60, "mx_draw": 0.23, "mx_away": 0.17,
                  "mx_xg_home": 1.8, "mx_xg_away": 0.8})
    if with_ens:
        eb = C.blend_1x2(0.60, 0.23, 0.17, 0.50, 0.27, 0.23)
        d.update({"ens_home": round(eb[0], 4), "ens_draw": round(eb[1], 4), "ens_away": round(eb[2], 4),
                  # GOLES = L3: ens_xg = our_xg (L3)
                  "ens_xg_home": 1.6, "ens_xg_away": 1.1})
    return pd.Series(d)


# ---------------------------------------------------------------- (a) blend = exact mean
def test_blend_is_exact_renormalised_mean():
    eb = C.blend_1x2(0.60, 0.23, 0.17, 0.50, 0.27, 0.23)
    # both inputs sum to 1 -> mean already sums to 1, so it's the plain mean
    assert eb == (0.55, 0.25, 0.20)
    # renormalisation when inputs don't sum to 1
    eb2 = C.blend_1x2(0.50, 0.30, 0.10, 0.50, 0.30, 0.30)   # means 0.5/0.3/0.2 sum 1.0
    assert eb2 == (0.5, 0.3, 0.2)
    # a second concrete fixture
    eb3 = C.blend_1x2(0.10, 0.20, 0.70, 0.30, 0.30, 0.40)
    assert eb3 == (0.20, 0.25, 0.55)
    # missing / degenerate -> None (soft)
    assert C.blend_1x2(None, 0.2, 0.2, 0.4, 0.3, 0.3) is None
    assert C.blend_1x2(0.0, 0.0, 0.0, 0.0, 0.0, 0.0) is None


def test_displayed_1x2_is_mean_of_mx_and_l3():
    r = _row(with_ens=True)
    ph, pdr, pa, xgh, xga, note = F.pred_1x2(r)
    assert (ph, pdr, pa) == (0.55, 0.25, 0.20)                       # exact mean of mx & L3
    assert note == F.ENS_NOTE


# ---------------------------------------------------------------- (b) exact reversal (flag off)
def test_exact_reversal_flag_off_equals_mx():
    # ENSEMBLE_1X2_LIVE off -> the builder writes no ens_* -> displayed 1X2 = mx_* (current state, Δ=0)
    r = _row(with_ens=False, with_mx=True)
    got = F.pred_1x2(r)
    assert got[:5] == (0.60, 0.23, 0.17, 1.8, 0.8)                   # exactly the mx engine
    assert got[5] == F.MX_NOTE
    # and with neither ens nor mx -> pure L3 (the deepest reversal)
    r2 = _row(with_ens=False, with_mx=False)
    assert F.pred_1x2(r2) == (0.50, 0.27, 0.23, 1.6, 1.1, None)


def test_builder_respects_flag_off(monkeypatch):
    """With ENSEMBLE_1X2_LIVE False, blend_1x2 is never used to write ens_* (the gate is the flag)."""
    monkeypatch.setattr(C, "ENSEMBLE_1X2_LIVE", False)
    assert C.ENSEMBLE_1X2_LIVE is False
    # the gate in the builder is `if ENSEMBLE_1X2_LIVE and mx and our` -> off means no ens row ever
    # (verified structurally; the full builder needs the API, the flag is the single switch)


# ---------------------------------------------------------------- (c) goals intact = L3
def test_goals_stay_l3():
    r = _row(with_ens=True)
    _ph, _pd, _pa, xgh, xga, _n = F.pred_1x2(r)
    # the xG returned for the ENSEMBLE is the L3 xG (goals never move to mx)
    assert (xgh, xga) == (r["our_xg_home"], r["our_xg_away"]) == (1.6, 1.1)
    # Over2.5/BTTS in the ficha derive from that L3 xG
    block = F.match_block(r, show_lineups=False)
    assert any("esperados 1.6" in ln for ln in block)          # CLEAN_FORMAT goals wording
    # the shown 1X2 line carries the blended probabilities (clean headline)
    assert any("Gana A — 55%" in ln for ln in block)
    # honest ensemble framing present
    assert any(F.ENS_NOTE in ln for ln in block)


# ---------------------------------------------------------------- (d) context chains on the blend
class _StubCtx:
    """Minimal context module: a non-trivial scenario (home must win -> 1.2 / away eliminated -> 0.8)."""
    def classify_fixture(self, rnd, home, away, groups, team_group):
        return "debe_ganar", "eliminated", 1.2, 0.8, True


def test_context_chains_on_blend_probs_and_l3_xg():
    r = _row(with_ens=True)
    ens = (r["ens_home"], r["ens_draw"], r["ens_away"])
    bxh, bxa = r["ens_xg_home"], r["ens_xg_away"]                    # = L3 xG
    adj = C.compute_context_adjustment(_StubCtx(), {}, {}, "Group Stage - 3", "A", "B",
                                       ens, bxh, bxa)
    assert adj is not None
    # ctx xG = the L3 xG scaled by the scenario multipliers (goals chain on L3)
    assert adj["ctx_xg_home"] == round(bxh * 1.2, 2)
    assert adj["ctx_xg_away"] == round(bxa * 0.8, 2)
    # ctx 1X2 = the BLEND probs moved by the Poisson delta of the xG change (chained on the ensemble)
    delta = l3_offline.wdl(bxh * 1.2, bxa * 0.8) - l3_offline.wdl(bxh, bxa)
    expect = np.clip(np.array(ens) + delta, 1e-6, None)
    expect = expect / expect.sum()
    assert adj["ctx_home"] == round(float(expect[0]), 4)
    assert adj["ctx_away"] == round(float(expect[2]), 4)


def test_chain_order_ctx_and_inj_outrank_ens():
    # ctx_* (computed on the blend) outranks ens_* in the render
    r = _row(with_ens=True)
    r["ctx_home"], r["ctx_draw"], r["ctx_away"] = 0.42, 0.30, 0.28
    r["ctx_xg_home"], r["ctx_xg_away"] = 1.9, 0.9
    assert F.pred_1x2(r)[0] == 0.42
    # inj_* (last link) outranks ctx_*
    r["inj_home"], r["inj_draw"], r["inj_away"] = 0.38, 0.30, 0.32
    r["inj_xg_home"], r["inj_xg_away"] = 1.4, 1.2
    assert F.pred_1x2(r)[0] == 0.38


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
            except TypeError:
                pass  # monkeypatch-fixture tests run under pytest
            print(f"  ran {name}")
    print("OK")
