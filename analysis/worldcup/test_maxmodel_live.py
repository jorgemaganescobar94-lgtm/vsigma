"""
Tests for promoting the MAX model to the live briefing engine (MAXMODEL_LIVE). NO network, NO API.
Locks the safety-critical properties:
  * the render picks mx_* when present (live MAX engine),
  * EXACT reversal: with no mx_* columns the displayed prediction is byte-identical to pure L3 (Δ=0),
  * honest framing (no claim of being more accurate; probabilistic, no market),
  * props stay on the L3 xG (our_xg_*), never mx_xg_*.

Run:  python -m pytest analysis/worldcup/test_maxmodel_live.py -q
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_worldcup_full_card as F  # noqa: E402


def _row(with_mx):
    d = {"home": "A", "away": "B", "round": "Group Stage - 3", "home_group": "Group A",
         "kickoff_utc": "2026-06-30 20:00", "fixture_id": 1,
         "our_home": 0.50, "our_draw": 0.27, "our_away": 0.23,
         "our_xg_home": 1.6, "our_xg_away": 1.1, "our_elo_home": 1.2, "our_elo_away": 0.4}
    if with_mx:
        d.update({"mx_home": 0.61, "mx_draw": 0.23, "mx_away": 0.16,
                  "mx_xg_home": 1.8, "mx_xg_away": 0.8})
    return pd.Series(d)


def test_pred_1x2_picks_mx_when_present():
    ph, pdr, pa, xgh, xga, note = F.pred_1x2(_row(with_mx=True))
    assert (ph, pdr, pa, xgh, xga) == (0.61, 0.23, 0.16, 1.8, 0.8)
    assert note == F.MX_NOTE


def test_exact_reversal_without_mx_equals_l3():
    # no mx_* columns (MAXMODEL_LIVE off) -> displayed prediction is EXACTLY the L3 our_* (note None)
    r = _row(with_mx=False)
    got = F.pred_1x2(r)
    assert got == (0.50, 0.27, 0.23, 1.6, 1.1, None)
    # and byte-identical to the L3 tuple it must reproduce
    l3 = (r["our_home"], r["our_draw"], r["our_away"], r["our_xg_home"], r["our_xg_away"], None)
    assert got == l3


def test_ctx_chains_over_mx():
    # CADENA mx -> contexto: ctx_* ahora se calcula ENCADENADO sobre mx (delta-Poisson), así que en el
    # render ctx_* tiene prioridad SOBRE mx_*. Sin nota de contexto -> mantiene el framing del motor.
    r = _row(with_mx=True)
    r["ctx_home"], r["ctx_draw"], r["ctx_away"] = 0.40, 0.30, 0.30
    r["ctx_xg_home"], r["ctx_xg_away"] = 1.3, 1.2
    ph, *_rest, note = F.pred_1x2(r)
    assert ph == 0.40 and note == F.MX_NOTE
    # con nota de contexto -> se devuelve la nota (para que el "por qué" anote el escenario)
    r["context_note"] = "ajustado por contexto de grupo: A ya clasificado"
    ph2, *_r2, note2 = F.pred_1x2(r)
    assert ph2 == 0.40 and "ajustado por contexto" in note2


def test_framing_is_honest_no_accuracy_claim():
    note = F.MX_NOTE.lower()
    assert "modelo amplio" in note and "probabilístico" in note and "mercado" in note
    for banned in ("más preciso", "mejor", "más exacto", "garantiz"):
        assert banned not in note
    # the live block in the ficha shows the MAX prediction + the honest note
    block = F.match_block(_row(with_mx=True), show_lineups=False)
    assert any("Resultado: A 61%" in ln for ln in block)
    assert any(F.MX_NOTE in ln for ln in block)


def test_props_use_l3_xg_not_mx():
    """In worldcup_player_props the prediction inputs read our_xg_* (L3, validated), NOT mx_xg_*.
    'mx_xg' may appear ONLY inside comment lines (the governance declaration)."""
    src = (HERE / "worldcup_player_props.py").read_text(encoding="utf-8").splitlines()
    code = "\n".join(ln for ln in src if not ln.lstrip().startswith("#"))
    assert '"our_xg_home"' in code and '"our_xg_away"' in code, "props must read our_xg_* (L3)"
    assert "mx_xg" not in code, "props code must NOT read mx_xg_* (only L3 our_xg); mx_xg lives only in a comment"


def test_live_csv_no_zeros_and_granular():
    """Regression on the two real defects: the live mx predictions must have NO class at 0.0% and
    distinct fixtures must get distinct 1X2 (no isotonic-plateau collapse)."""
    p = HERE / "worldcup_maxmodel_shadow_predictions.csv"
    if not p.exists():
        return  # soft: artifact optional in some checkouts
    d = pd.read_csv(p)
    cls = d[["mx_home", "mx_draw", "mx_away"]]
    assert (cls > 0.0).all().all(), "no mx class may be exactly 0.0% (honesty)"
    assert (cls < 1.0).all().all(), "no mx class may be exactly 100%"
    trip = cls.round(4).apply(tuple, axis=1)
    # granularity: the vast majority of fixtures must be distinct (was 46/62 with the step-isotonic)
    assert trip.nunique() >= int(0.95 * len(d)), f"too many identical 1X2 triples ({trip.nunique()}/{len(d)})"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn(); print(f"  PASS {name}")
    print("OK")
