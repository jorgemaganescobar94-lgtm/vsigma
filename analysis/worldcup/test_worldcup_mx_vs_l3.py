"""
Offline tests for the accumulated "Motor máximo (mx) vs L3" marker (read-only, no network, no model).

Covers: the anti-hindsight filter (only settled rows WITH a frozen mx prediction count; unsettled or
mx-less rows are excluded), the head-to-head metrics (1X2 acc/logloss/brier + Poisson Over2.5/BTTS),
leader detection + tie band, the honest small-sample verdict (NO winner below N), the compact briefing
line, the panel section parsing the CSV, and that the module touches NO market/odds endpoint.

The 6-fixture fixture replicates EXACTLY last night's six settled World Cup matches (2026-06-27/28),
so the documented validation — mx 1X2 4/6, L3 1X2 4/6 (66.7%) — is pinned deterministically and does
not depend on the live, growing log.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_learning_loop as ll  # noqa: E402
import worldcup_mx_vs_l3_scorer as mx  # noqa: E402
import build_worldcup_trackrecord_panel as panel  # noqa: E402


# Last night's six settled fixtures (real frozen mx_*/l3_* + 90' result). H/D/A argmax:
#   L3: H, A, A(✗ res D), H, H(✗ res D), A  -> 4/6
#   mx: H, A, H(✗ res D), H, H(✗ res D), A  -> 4/6
SIX = [
    # home, away, ko, l3(h,d,a), l3xg(h,a), mx(h,d,a), mxxg(h,a), ft(h,a), 1x2
    ("Croatia", "Ghana", "2026-06-27 21:00", (0.6422, 0.1952, 0.1626), (1.95, 0.72),
     (0.7078, 0.1935, 0.0986), (1.96, 0.68), (2, 1), "H"),
    ("Panama", "England", "2026-06-27 21:00", (0.0588, 0.1848, 0.7565), (0.53, 2.28),
     (0.1171, 0.2168, 0.6661), (0.73, 2.0), (0, 2), "A"),
    ("Colombia", "Portugal", "2026-06-27 23:30", (0.3297, 0.3012, 0.3691), (1.09, 1.31),
     (0.3808, 0.2877, 0.3315), (1.23, 1.14), (0, 0), "D"),
    ("Congo DR", "Uzbekistan", "2026-06-27 23:30", (0.4412, 0.2928, 0.266), (1.37, 1.06),
     (0.5462, 0.2585, 0.1952), (1.59, 0.84), (3, 1), "H"),
    ("Algeria", "Austria", "2026-06-28 02:00", (0.5426, 0.2617, 0.1958), (1.61, 0.9),
     (0.6013, 0.237, 0.1617), (1.67, 0.82), (3, 3), "D"),
    ("Jordan", "Argentina", "2026-06-28 02:00", (0.0294, 0.1025, 0.8681), (0.35, 2.87),
     (0.0493, 0.16, 0.7906), (0.57, 2.71), (1, 3), "A"),
]


def _row(spec, fid, settled=1, with_mx=True):
    h, a, ko, l3, l3xg, mxp, mxxg, ft, res = spec
    r = {c: np.nan for c in ll.LOG_COLUMNS}
    r.update({
        "fixture_id": fid, "kickoff_utc": ko, "home": h, "away": a, "round": "Group Stage - 3",
        "l3_home": l3[0], "l3_draw": l3[1], "l3_away": l3[2],
        "l3_xg_home": l3xg[0], "l3_xg_away": l3xg[1],
        "result_ft_gh": ft[0], "result_ft_ga": ft[1], "result_1x2": res, "settled": settled,
    })
    if with_mx:
        r.update({"mx_home": mxp[0], "mx_draw": mxp[1], "mx_away": mxp[2],
                  "mx_xg_home": mxxg[0], "mx_xg_away": mxxg[1]})
    return r


def _write_log(tmp_path, rows):
    df = pd.DataFrame(rows)[ll.LOG_COLUMNS]
    p = tmp_path / "log.csv"
    df.to_csv(p, index=False)
    return p


@pytest.fixture()
def six_log(tmp_path):
    return _write_log(tmp_path, [_row(s, i + 1) for i, s in enumerate(SIX)])


# ----------------------------------------------------------------- core metrics
def test_six_games_1x2_both_four_of_six(six_log):
    res = mx.compute_from_log(six_log)
    assert res["n"] == 6
    assert res["since"] == "27-jun"          # earliest mx-present settled kickoff
    acc = mx._get(res, "1X2", "acc")
    # mx 4/6 and L3 4/6 -> 66.7% each, exactly as validated against the real log
    assert acc["l3"] == pytest.approx(400 / 6, abs=0.05)
    assert acc["mx"] == pytest.approx(400 / 6, abs=0.05)
    assert acc["leader"] == "empate"


def test_six_games_leaders(six_log):
    res = mx.compute_from_log(six_log)
    # L3 leads 1X2 log-loss/Brier; mx leads the Poisson Over2.5/BTTS log-loss/Brier (real numbers)
    assert mx._get(res, "1X2", "logloss")["leader"] == "L3"
    assert mx._get(res, "1X2", "brier")["leader"] == "L3"
    assert mx._get(res, "Over 2.5", "logloss")["leader"] == "mx"
    assert mx._get(res, "BTTS", "logloss")["leader"] == "mx"
    # all three markets present with the three metrics each
    keys = {(r["market"], r["metric"]) for r in res["rows"]}
    for m in ("1X2", "Over 2.5", "BTTS"):
        for k in ("acc", "logloss", "brier"):
            assert (m, k) in keys


def test_metrics_match_learning_loop_helpers(six_log):
    """The 1X2 numbers must equal the shared learning-loop metric helper (single source of truth)."""
    df = pd.read_csv(six_log)
    P = df[["l3_home", "l3_draw", "l3_away"]].to_numpy(float)
    y = df["result_1x2"].map({"H": 0, "D": 1, "A": 2}).to_numpy(int)
    expect = ll._metrics(P, np.eye(3)[y])
    res = mx.compute_from_log(six_log)
    assert mx._get(res, "1X2", "logloss")["l3"] == pytest.approx(expect["logloss"], abs=1e-9)
    assert mx._get(res, "1X2", "brier")["l3"] == pytest.approx(expect["brier"], abs=1e-9)


# ----------------------------------------------------------------- anti-hindsight / anti-leakage
def test_excludes_rows_without_mx(tmp_path):
    """A settled fixture with NO mx prediction (mx entered live later) must NOT be counted —
    mx is never backfilled retroactively."""
    rows = [_row(SIX[0], 1, settled=1, with_mx=True),
            _row(SIX[1], 2, settled=1, with_mx=False)]   # mx absent -> excluded
    res = mx.compute_from_log(_write_log(tmp_path, rows))
    assert res["n"] == 1


def test_excludes_unsettled_rows(tmp_path):
    """A future fixture WITH an mx prediction but not yet settled must NOT be counted."""
    rows = [_row(SIX[0], 1, settled=1, with_mx=True),
            _row(SIX[1], 2, settled=0, with_mx=True)]    # not settled -> excluded
    res = mx.compute_from_log(_write_log(tmp_path, rows))
    assert res["n"] == 1


def test_no_mx_settled_yet_is_graceful(tmp_path):
    """Only mx-less settled rows -> N=0, empty briefing, placeholder txt, NO winner."""
    rows = [_row(SIX[0], 1, settled=1, with_mx=False)]
    res = mx.compute_from_log(_write_log(tmp_path, rows))
    assert res["n"] == 0 and res["rows"] == []
    assert mx.briefing_line(res) == ""
    assert "aún sin partidos" in mx.render_txt(res)


# ----------------------------------------------------------------- leader logic
def test_leader_tie_band_and_direction():
    # lower-is-better metric: smaller wins; within tie band -> empate
    assert mx._leader(0.70, 0.60, lower_better=True, tie=mx.TIE_LL)[0] == "mx"
    assert mx._leader(0.60, 0.70, lower_better=True, tie=mx.TIE_LL)[0] == "L3"
    assert mx._leader(0.700000, 0.700001, lower_better=True, tie=mx.TIE_LL)[0] == "empate"
    # higher-is-better metric (accuracy)
    assert mx._leader(60.0, 67.0, lower_better=False, tie=mx.TIE_ACC)[0] == "mx"
    assert mx._leader(np.nan, 1.0, lower_better=True, tie=mx.TIE_LL)[0] == "n/d"


# ----------------------------------------------------------------- briefing line + verdict honesty
def test_briefing_line_format_and_small_sample(six_log):
    line = mx.briefing_line(mx.compute_from_log(six_log))
    assert line.startswith("⚙️ Motor máximo vs L3 (N=6 · desde 27-jun):")
    assert "1X2 67% vs 67%" in line              # mx% vs L3% (motor máximo primero)
    assert "muestra pequeña, orientativo" in line


def test_no_winner_declared_below_threshold(six_log):
    txt = mx.render_txt(mx.compute_from_log(six_log))
    assert "NO se declara ganador" in txt
    assert "muestra pequeña" in txt


def test_winner_named_only_with_large_n(tmp_path):
    """Above SMALL_N the verdict may name a leader; build a >threshold log to exercise that path."""
    rows = []
    for i in range(mx.SMALL_N + 6):
        rows.append(_row(SIX[i % 6], i + 1))
    res = mx.compute_from_log(_write_log(tmp_path, rows))
    assert res["n"] >= mx.SMALL_N
    txt = mx.render_txt(res)
    assert "NO se declara ganador" not in txt
    assert "VEREDICTO" in txt


# ----------------------------------------------------------------- CSV + panel surface
def test_csv_roundtrip_and_panel_section(tmp_path, six_log):
    res = mx.compute_from_log(six_log)
    csv_path = tmp_path / "mx.csv"
    mx.write_csv(res, csv_path)
    text = csv_path.read_text(encoding="utf-8")
    lines = panel.section_mx_vs_l3(text)
    body = "\n".join(lines)
    assert lines[0].startswith("## L3 vs Motor máximo (en vivo, desde 27-jun)")
    assert "**N = 6**" in body
    assert "| 1X2 acc% | 66.7 | 66.7 | empate |" in body
    assert "**mx**" in body                       # mx leads at least one binary metric -> bolded
    assert "NO se declara ganador" in body        # small-sample honesty carried into the panel


def test_panel_section_empty_csv_is_soft():
    lines = panel.section_mx_vs_l3("")             # no data -> placeholder, never raises
    assert lines[0].startswith("## L3 vs Motor máximo")
    assert "sin datos aún" in "\n".join(lines)


# ----------------------------------------------------------------- isolation guarantees
def test_no_market_or_api_calls_in_module():
    src = (HERE / "worldcup_mx_vs_l3_scorer.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient"):
        assert bad not in src
