"""
Offline tests for the reversible, auto-learned CARD-prop correction (deflates shown p_card).
No network, no model, read-only over the model (post-hoc display fix). Covers: the shrunk
multiplicative factor (factor = 1 − shrink(1−ratio), shrink = N/(N+25), N = settled matches),
the cap clamp, the apply (p_card deflated, gol/asistencia/tiros UNTOUCHED, [0,1] clamp, high p
deflated more in absolute terms), EXACT revert with the flag off (Δ=0), soft-fail with no state,
the props scorecard reporting raw vs corrected card bias, the panel surfacing it, and that the
module touches NO market/odds/API endpoint.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_card_prop_correction as C  # noqa: E402
import worldcup_player_props as pp  # noqa: E402
import build_worldcup_trackrecord_panel as panel  # noqa: E402


def _props_log(tmp_path, rows):
    cols = ["fixture_id", "kickoff_utc", "team", "player", "is_xi", "basis",
            "p_goal", "p_card", "p_shot_on", "p_assist", "exp_shots", "act_card", "act_goal",
            "act_assist", "act_shots_on", "settled"]
    df = pd.DataFrame(rows)
    for c in cols:
        if c not in df.columns:
            df[c] = np.nan
    p = tmp_path / "props.csv"
    df[cols].to_csv(p, index=False)
    return p


def _settled_rows(p_cards, act_cards, fixtures):
    return [{"fixture_id": f, "player": f"P{i}", "is_xi": 1, "p_card": pc, "act_card": ac,
             "p_goal": 0.1, "p_assist": 0.08, "p_shot_on": 0.3, "exp_shots": 1.0, "settled": 1}
            for i, (pc, ac, f) in enumerate(zip(p_cards, act_cards, fixtures))]


# ----------------------------------------------------------------- estimate
def test_estimate_factor_formula(tmp_path):
    # 4 player-rows over 2 matches; p_card mean 0.40, real rate 0.25 -> ratio 0.625
    rows = _settled_rows([0.40, 0.40, 0.40, 0.40], [1, 0, 0, 0], [1, 1, 2, 2])
    est = C.estimate(_props_log(tmp_path, rows))
    n_matches = 2
    shrink = n_matches / (n_matches + C.K_SHRINK)
    ratio = 0.25 / 0.40
    expect = 1.0 - shrink * (1.0 - ratio)
    assert est["n_matches"] == 2 and est["n_rows"] == 4
    assert est["ratio"] == pytest.approx(ratio, abs=1e-9)
    assert est["shrink"] == pytest.approx(shrink, abs=1e-9)
    assert est["factor"] == pytest.approx(expect, abs=1e-9)
    assert 0 < est["factor"] < 1            # over-prediction -> deflate


def test_estimate_grows_with_n(tmp_path):
    """More matches -> larger shrink -> factor moves further from 1 toward the ratio (auto-learning)."""
    small = C.estimate(_props_log(tmp_path, _settled_rows([0.4] * 4, [1, 0, 0, 0], [1, 1, 2, 2])))
    rows = _settled_rows([0.4] * 60, [1, 0, 0, 0] * 15, list(range(1, 31)) * 2)
    big = C.estimate(_props_log(tmp_path, rows))
    assert big["shrink"] > small["shrink"]
    assert big["factor"] < small["factor"]   # closer to ratio (more deflation)


def test_cap_clamps_factor(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "FACTOR_FLOOR", 0.99)
    est = C.estimate(_props_log(tmp_path, _settled_rows([0.4] * 4, [1, 0, 0, 0], [1, 1, 2, 2])))
    assert est["capped"] is True and est["factor"] == pytest.approx(0.99, abs=1e-9)


def test_estimate_none_when_no_settled(tmp_path):
    rows = _settled_rows([0.4, 0.4], [1, 0], [1, 1])
    df = pd.read_csv(_props_log(tmp_path, rows)); df["settled"] = 0
    p = tmp_path / "ns.csv"; df.to_csv(p, index=False)
    assert C.estimate(p) is None


# ----------------------------------------------------------------- apply (display only)
def _state(tmp_path, factor=0.8):
    p = tmp_path / "state.csv"
    pd.DataFrame([{"n_matches": 18, "n_rows": 396, "mean_pred": 0.16, "real_rate": 0.10,
                   "ratio": 0.6, "shrink": 0.42, "factor": factor, "k": 25.0, "capped": False}]).to_csv(p, index=False)
    return p


def _card_df():
    return pd.DataFrame([
        {"fixture_id": 1, "player": "Hi", "is_xi": 1, "p_card": 0.50, "p_goal": 0.20,
         "p_assist": 0.10, "p_shot_on": 0.4, "exp_shots": 2.0},
        {"fixture_id": 1, "player": "Lo", "is_xi": 1, "p_card": 0.10, "p_goal": 0.05,
         "p_assist": 0.03, "p_shot_on": 0.2, "exp_shots": 1.0},
    ])


def test_apply_deflates_card_only(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", True)
    df = _card_df()
    out = C.apply_to_props_df(df, state_path=_state(tmp_path, 0.8))
    assert out is not df                      # a copy, original untouched
    assert out.iloc[0]["p_card"] == pytest.approx(0.40, abs=1e-9)   # 0.50 * 0.8
    assert out.iloc[1]["p_card"] == pytest.approx(0.08, abs=1e-9)   # 0.10 * 0.8
    # high p deflated MORE in absolute terms (multiplicative)
    assert (0.50 - 0.40) > (0.10 - 0.08)
    # gol / asistencia / tiros NEVER touched
    for col in ("p_goal", "p_assist", "p_shot_on", "exp_shots"):
        assert (out[col].to_numpy() == df[col].to_numpy()).all()
    # original df not mutated
    assert df.iloc[0]["p_card"] == 0.50


def test_apply_clamps_to_unit_interval(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", True)
    df = _card_df()
    out = C.apply_to_props_df(df, state_path=_state(tmp_path, factor=1.5))  # 0.5*1.5=0.75 ok; check <=1
    assert (out["p_card"] <= 1.0).all() and (out["p_card"] >= 0.0).all()


def test_flag_off_exact_revert(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", False)
    df = _card_df()
    out = C.apply_to_props_df(df, state_path=_state(tmp_path, 0.8))
    assert (out["p_card"].to_numpy() == df["p_card"].to_numpy()).all()   # Δ=0 EXACT
    assert C.load_factor(_state(tmp_path, 0.8)) is None


def test_no_state_no_correction(tmp_path, monkeypatch):
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", True)
    df = _card_df()
    out = C.apply_to_props_df(df, state_path=tmp_path / "nope.csv")
    assert (out["p_card"].to_numpy() == df["p_card"].to_numpy()).all()


def test_load_factor_respects_flag(tmp_path, monkeypatch):
    st = _state(tmp_path, 0.8)
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", False)
    assert C.load_factor(st) is None
    monkeypatch.setattr(C, "CARD_PROP_CORRECTION", True)
    assert C.load_factor(st) == pytest.approx(0.8)


# ----------------------------------------------------------------- scorecard raw vs corrected (req 4)
def test_scorecard_reports_raw_and_corrected(tmp_path, monkeypatch):
    # settled card data: pred 0.40 mean, real rate 0.00 -> raw bias +40pp (clear over-prediction)
    settled = pd.DataFrame(_settled_rows([0.40, 0.40, 0.40, 0.40], [0, 0, 0, 0], [1, 1, 2, 2]))
    monkeypatch.setattr(pp, "CARD_CORRECTION_CSV", _state(tmp_path, factor=0.5))
    out = "\n".join(pp._card_bias_raw_vs_corrected(settled))
    assert "crudo" in out and "corregido" in out
    assert "baja ✓" in out                    # corrected |bias| < raw |bias|
    assert "factor 0.5000" in out


def test_scorecard_no_factor_is_soft(tmp_path, monkeypatch):
    settled = pd.DataFrame(_settled_rows([0.20, 0.20], [1, 0], [1, 1]))
    monkeypatch.setattr(pp, "CARD_CORRECTION_CSV", tmp_path / "nope.csv")
    out = "\n".join(pp._card_bias_raw_vs_corrected(settled))
    assert "sin factor" in out or "sin corrección" in out


# ----------------------------------------------------------------- panel surface
def test_panel_props_shows_card_raw_vs_corrected():
    sc = (
        "partidos liquidados=18 | filas jugador-prop=396 | umbral graduación N>=30\n"
        "  card     396  10% 0.3000 0.0900 0.073 0.3100 0.0950   no\n"
        "  TARJETA — sesgo CRUDO vs CORREGIDO (deflación de p_card; gol/asistencia NO se tocan):\n"
        "    crudo:     media pred 16.23%  vs real  9.85%  -> sesgo +6.38pp\n"
        "    corregido: media pred 13.56%  vs real  9.85%  -> sesgo +3.71pp  (factor 0.8354; |sesgo| baja ✓)\n"
    )
    body = "\n".join(panel.section_props(sc))
    assert "sesgo crudo vs corregido" in body
    assert "+6.38pp" in body and "+3.71pp" in body
    assert "factor 0.8354" in body and "CARD_PROP_CORRECTION" in body


# ----------------------------------------------------------------- isolation
def test_no_market_or_api_calls_in_module():
    src = (HERE / "worldcup_card_prop_correction.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient"):
        assert bad not in src
