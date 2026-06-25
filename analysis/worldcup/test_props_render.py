"""
Offline tests for the player-props block in the Telegram ficha (build_worldcup_full_card.props_lines
/ props_block) AFTER per-prop labelling. NO network, NO API.

Covers: VALIDADOS section (gol + asistencia) with NO 'no fiarse' disclaimer · EXPERIMENTAL section
(tarjeta with %, tiros as ORDER only — no % / no number) · numbers come straight from the log · no
props -> no block · only XI rows · XI provisional/confirmado tag on the validados header · no
certainty language.

Run:  python analysis/worldcup/test_props_render.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_full_card as F  # noqa: E402

CERTAINTY = ["marcará", "gol seguro", "seguro", "garantiz", "fijo", "100%", "sin duda"]


def _row(player, is_xi=1, **kw):
    base = {"player": player, "is_xi": is_xi, "p_goal": 0.0, "p_assist": 0.0,
            "p_card": 0.0, "exp_shots": 0.0, "p_shot_on": 0.0}
    base.update(kw)
    return base


def _df3():
    return pd.DataFrame([
        _row("Mbappe", p_goal=0.30, p_assist=0.18, p_card=0.10, exp_shots=3.2, p_shot_on=0.7),
        _row("Dembele", p_goal=0.12, p_assist=0.22, p_card=0.15, exp_shots=2.1, p_shot_on=0.5),
        _row("Kante", p_goal=0.03, p_assist=0.05, p_card=0.35, exp_shots=0.6, p_shot_on=0.2),
    ])


def test_validados_goal_assist_no_disclaimer():
    lines = F.props_lines(_df3(), name_fn=str)
    assert lines and F.VALID_LABEL in lines[0]
    txt = "\n".join(lines)
    assert "Validado en backtest" in txt
    assert "no fiarse" not in txt and "SIN VALIDAR" not in txt          # validados: sin descargo
    # gol top by p_goal: Mbappe 30 · Dembele 12 · Kante 3 (exact logged numbers)
    assert "Gol: Mbappe 30%" in txt and "Dembele 12%" in txt
    # asistencia top by p_assist: Dembele 22 · Mbappe 18 · Kante 5  (NEW line)
    assert "Asistencia: Dembele 22%" in txt and "Mbappe 18%" in txt
    assert "se sigue confirmando en vivo" in txt                        # WC neutral/knockout note


def test_experimental_card_pct_and_shots_ranking():
    lines = F.props_lines(_df3(), name_fn=str)
    txt = "\n".join(lines)
    assert F.EXP_LABEL in txt and "Experimental" in F.EXP_LABEL
    # tarjeta top 2 by p_card WITH %: Kante 35 · Dembele 15
    assert "Tarjeta: Kante 35%" in txt and "Dembele 15%" in txt
    # tiros as ORDER only (by exp_shots): Mbappe > Dembele > Kante, NO % / NO number
    shot_line = next(l for l in lines if "Tiros (orden" in l)
    assert "Mbappe > Dembele > Kante" in shot_line
    assert "%" not in shot_line and "~" not in shot_line and "3.2" not in shot_line


def test_no_props_no_block():
    assert F.props_lines(pd.DataFrame()) == []
    assert F.props_lines(None) == []


def test_only_xi_rows_used():
    df = pd.DataFrame([
        _row("SubMan", is_xi=0, p_goal=0.99, p_assist=0.99, p_card=0.99, exp_shots=9.0),
        _row("Starter", is_xi=1, p_goal=0.10, p_assist=0.10, p_card=0.20, exp_shots=1.0),
    ])
    txt = " ".join(F.props_lines(df, name_fn=str))
    assert "Starter" in txt and "SubMan" not in txt


def test_validados_header_marks_provisional_xi():
    df = _df3(); df["basis"] = "probable_by_recent_starts"
    head = F.props_lines(df, name_fn=str)[0]
    assert F.VALID_LABEL in head and "provisional" in head and "alineación oficial" in head
    assert "confirmado" not in head


def test_validados_header_marks_confirmed_xi():
    df = _df3(); df["basis"] = "lineup_confirmed"
    head = F.props_lines(df, name_fn=str)[0]
    assert "(XI confirmado)" in head and "provisional" not in head


def test_validados_header_provisional_wins_mixed():
    df = _df3(); df["basis"] = ["lineup_confirmed", "probable_by_recent_starts", "lineup_confirmed"]
    assert "provisional" in F.props_lines(df, name_fn=str)[0]


def test_no_status_when_basis_missing():
    head = F.props_lines(_df3(), name_fn=str)[0]
    assert head == F.VALID_LABEL                                        # no basis column -> bare label


def test_no_certainty_language():
    df = pd.DataFrame([_row("X", p_goal=0.9, p_assist=0.8, p_card=0.1, exp_shots=3.0)])
    txt = " ".join(F.props_lines(df, name_fn=str)).lower()
    for bad in CERTAINTY:
        assert bad not in txt, f"certainty word '{bad}'"


def test_props_block_reads_log_for_fixture():
    F._props_cache = None
    td = tempfile.mkdtemp()
    F.PROPS_LOG = Path(td) / "props.csv"
    pd.DataFrame([{"fixture_id": 99, "player": "Z", "is_xi": 1, "p_goal": 0.2, "p_assist": 0.15,
                   "p_card": 0.3, "exp_shots": 1.5, "p_shot_on": 0.5}]).to_csv(F.PROPS_LOG, index=False)
    lines = F.props_block(99)
    assert lines and "Z 20%" in "\n".join(lines)        # goal % straight from the log
    assert F.props_block(12345) == []                   # other fixture -> no block
    F._props_cache = None


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} props-render tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
