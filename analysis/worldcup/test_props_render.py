"""
Offline tests for the EXPERIMENTAL player-props block in the Telegram ficha
(build_worldcup_full_card.props_lines / props_block). NO network, NO API.

Covers: block uses exactly the logged numbers · experimental label always present when a
block exists · no props -> no block (ficha intact) · only XI rows · no certainty language.

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


def _df(rows):
    return pd.DataFrame(rows)


def test_block_uses_log_numbers_and_label():
    df = _df([
        {"player": "Yeboah", "is_xi": 1, "p_goal": 0.13, "p_card": 0.17, "exp_shots": 0.8, "p_shot_on": 0.51},
        {"player": "Valencia", "is_xi": 1, "p_goal": 0.08, "p_card": 0.29, "exp_shots": 2.0, "p_shot_on": 0.48},
        {"player": "Caicedo", "is_xi": 1, "p_goal": 0.01, "p_card": 0.46, "exp_shots": 0.3, "p_shot_on": 0.14},
    ])
    lines = F.props_lines(df)
    assert lines, "expected a block"
    assert lines[0] == F.PROPS_LABEL
    assert "EXPERIMENTAL" in lines[0] and "SIN VALIDAR" in lines[0]
    txt = "\n".join(lines)
    assert "Yeboah 13%" in txt      # top scorer, exact logged number
    assert "Caicedo 46%" in txt     # top card risk, exact logged number
    assert "Valencia ~2.0" in txt   # most shots, exact logged number


def test_no_props_no_block():
    assert F.props_lines(_df([])) == []
    assert F.props_lines(None) == []


def test_only_xi_rows_used():
    df = _df([
        {"player": "SubMan", "is_xi": 0, "p_goal": 0.99, "p_card": 0.01, "exp_shots": 0.1, "p_shot_on": 0.1},
        {"player": "Starter", "is_xi": 1, "p_goal": 0.10, "p_card": 0.20, "exp_shots": 1.0, "p_shot_on": 0.4},
    ])
    txt = " ".join(F.props_lines(df))
    assert "Starter" in txt and "SubMan" not in txt


def test_label_marks_provisional_xi():
    df = _df([{"player": "X", "is_xi": 1, "basis": "probable_by_recent_starts",
               "p_goal": 0.2, "p_card": 0.3, "exp_shots": 1.0, "p_shot_on": 0.4}])
    label = F.props_lines(df)[0]
    assert "EXPERIMENTAL" in label
    assert "provisional" in label and "alineación oficial" in label
    assert "confirmado" not in label


def test_label_marks_confirmed_xi():
    df = _df([{"player": "X", "is_xi": 1, "basis": "lineup_confirmed",
               "p_goal": 0.2, "p_card": 0.3, "exp_shots": 1.0, "p_shot_on": 0.4}])
    label = F.props_lines(df)[0]
    assert "(XI confirmado)" in label and "provisional" not in label


def test_label_provisional_wins_when_teams_disagree():
    # one team confirmed, the other still probable -> provisional note (honest)
    df = _df([
        {"player": "Conf", "is_xi": 1, "basis": "lineup_confirmed",
         "p_goal": 0.2, "p_card": 0.3, "exp_shots": 1.0, "p_shot_on": 0.4},
        {"player": "Prob", "is_xi": 1, "basis": "probable_by_recent_starts",
         "p_goal": 0.1, "p_card": 0.2, "exp_shots": 0.8, "p_shot_on": 0.3},
    ])
    assert "provisional" in F.props_lines(df)[0]


def test_label_no_status_when_basis_missing():
    # no 'basis' column -> soft-fail, label unchanged (back-compat with old logs)
    df = _df([{"player": "X", "is_xi": 1, "p_goal": 0.2, "p_card": 0.3,
               "exp_shots": 1.0, "p_shot_on": 0.4}])
    assert F.props_lines(df)[0] == F.PROPS_LABEL


def test_no_certainty_language():
    df = _df([{"player": "X", "is_xi": 1, "p_goal": 0.9, "p_card": 0.1, "exp_shots": 3.0, "p_shot_on": 0.7}])
    txt = " ".join(F.props_lines(df)).lower()
    for bad in CERTAINTY:
        assert bad not in txt, f"certainty word '{bad}'"


def test_props_block_reads_log_for_fixture():
    F._props_cache = None
    td = tempfile.mkdtemp()
    F.PROPS_LOG = Path(td) / "props.csv"
    _df([{"fixture_id": 99, "player": "Z", "is_xi": 1, "p_goal": 0.2, "p_card": 0.3,
          "exp_shots": 1.5, "p_shot_on": 0.5}]).to_csv(F.PROPS_LOG, index=False)
    lines = F.props_block(99)
    assert lines and "Z 20%" in "\n".join(lines)
    assert F.props_block(12345) == []   # different fixture -> no block
    F._props_cache = None               # reset for any other test/run


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} props-render tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
