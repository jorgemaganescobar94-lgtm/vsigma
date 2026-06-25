"""
Offline tests for worldcup_explain.explain_l3 — pure rendering, NO network/API/model.
Verifies the explanation uses exactly s_home/s_away/sup and adj_* from the record, says
"sin ventaja local" on a neutral venue, omits the adjustment line when there are no
injuries, and never uses certainty language.

Run:  python analysis/worldcup/test_worldcup_explain.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_explain as E  # noqa: E402

CERTAINTY = ["ganará", "gana seguro", "seguro", "garantiz", "sin duda", "100%", "fijo"]


def test_uses_strength_diff_exactly():
    # sup = 1.86 - 1.19 = 0.67 -> "rating +0.67 sobre Ecuador"; Germany favourite
    txt = E.explain_l3("Germany", "Ecuador", 1.86, 1.19, neutral=1,
                       xg_home=1.89, xg_away=0.77, p_home=0.575, p_draw=0.256, p_away=0.169)
    assert "Germany" in txt and "+0.67 sobre Ecuador" in txt
    assert "modelo propio de selecciones, sin mercado/cuotas" in txt
    assert "Es probabilístico" in txt
    assert "57/26/17%" in txt  # 0.575/0.256/0.169 formatted with .0f


def test_neutral_says_no_home_advantage():
    txt = E.explain_l3("A", "B", 1.0, 0.0, neutral=1,
                       xg_home=1.5, xg_away=1.0, p_home=0.5, p_draw=0.25, p_away=0.25)
    assert "Campo neutral: sin ventaja local." in txt


def test_no_injury_line_when_no_absences():
    txt = E.explain_l3("A", "B", 1.0, 0.2, neutral=1,
                       xg_home=1.6, xg_away=0.9, p_home=0.55, p_draw=0.26, p_away=0.19,
                       adj_basis=None, adj_absent_home="", adj_absent_away="",
                       adj_delta_home=0.0, adj_delta_away=0.0)
    assert "Bajas clave" not in txt


def test_injury_line_uses_adj_fields():
    txt = E.explain_l3("Germany", "Ecuador", 1.86, 1.19, neutral=1,
                       xg_home=1.9, xg_away=0.9, p_home=0.57, p_draw=0.26, p_away=0.17,
                       adj_basis="inj", adj_absent_home="", adj_absent_away="Caicedo",
                       adj_delta_home=0.0, adj_delta_away=-0.05)
    assert "Bajas clave:" in txt
    assert "Ecuador -0.05" in txt and "sin Caicedo" in txt
    assert "Germany" not in txt.split("Bajas clave:")[1].split(".")[0]  # home (no absence) not listed


def test_even_match_says_parejos_no_favourite():
    txt = E.explain_l3("A", "B", 1.00, 1.05, neutral=1,
                       xg_home=1.3, xg_away=1.3, p_home=0.36, p_draw=0.28, p_away=0.36)
    assert "parejos" in txt and "favorito" not in txt


def test_no_certainty_language():
    for sup in (2.5, 0.6, 0.0):
        txt = E.explain_l3("A", "B", 1.0 + sup, 1.0, neutral=1,
                           xg_home=2.0, xg_away=0.8, p_home=0.7, p_draw=0.2, p_away=0.1)
        low = txt.lower()
        for bad in CERTAINTY:
            assert bad not in low, f"certainty word '{bad}' in: {txt}"


def test_soft_fail_on_missing_strength():
    assert E.explain_l3("A", "B", None, 1.0, 1, 1.0, 1.0, 0.4, 0.3, 0.3) == ""
    assert E.explain_l3("A", "B", float("nan"), 1.0, 1, 1.0, 1.0, 0.4, 0.3, 0.3) == ""


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} explain tests passed (no network, no API, no model).")


if __name__ == "__main__":
    _run()
