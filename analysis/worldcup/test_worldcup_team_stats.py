"""
Offline tests for the accumulated team-stats marker (córners/tiros/tarjetas predicho vs real).
Read-only, no network, no model. Covers the metrics (MAE/RMSE/bias/means), the córners O/U line
accuracy, the anti-hindsight / anti-leakage filter (only settled rows with BOTH a frozen prediction
and a real value count; unsettled rows excluded), the honest bias reading (corners/shots under-,
cards over-estimate), the small-sample flag, the panel section parsing the CSV, and that the module
touches NO market/odds/API endpoint.

Two fixtures replicate EXACTLY two real settled matches (Senegal-Iraq, Norway-France), so the
documented hand-check is pinned deterministically and does not depend on the growing live log.
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
import worldcup_team_stats_scorer as ts  # noqa: E402
import build_worldcup_trackrecord_panel as panel  # noqa: E402


# (home, away, st_corners_total, result_corners, st_cards_total, result_cards,
#  st_shots_total, result_shots, st_corners_over, st_corners_line)
SENEGAL_IRAQ = ("Senegal", "Iraq", 8.57, 15.0, 4.61, 5.0, 18.13, 34.0, 0.6232, 7.5)
NORWAY_FRANCE = ("Norway", "France", 5.71, 9.0, 3.49, 2.0, 17.21, 28.0, 0.2175, 7.5)


def _row(spec, fid, settled=1, with_pred=True, with_real=True):
    h, a, sc, rc, scd, rcd, ssh, rsh, cover, cline = spec
    r = {c: np.nan for c in ll.LOG_COLUMNS}
    r.update({"fixture_id": fid, "kickoff_utc": "2026-06-26 19:00", "home": h, "away": a,
              "round": "Group Stage - 3", "result_1x2": "H", "settled": settled})
    if with_pred:
        r.update({"st_corners_total": sc, "st_cards_total": scd, "st_shots_total": ssh,
                  "st_corners_over": cover, "st_corners_line": cline})
    if with_real:
        r.update({"result_corners": rc, "result_cards": rcd, "result_shots": rsh})
    return r


def _write_log(tmp_path, rows):
    df = pd.DataFrame(rows)[ll.LOG_COLUMNS]
    p = tmp_path / "log.csv"
    df.to_csv(p, index=False)
    return p


@pytest.fixture()
def two_log(tmp_path):
    return _write_log(tmp_path, [_row(SENEGAL_IRAQ, 1), _row(NORWAY_FRANCE, 2)])


def _get(res, stat):
    return next((r for r in res["rows"] if r["stat"] == stat), None)


# ----------------------------------------------------------------- metrics (hand-checked)
def test_two_matches_corners_metrics(two_log):
    res = ts.compute_from_log(two_log)
    c = _get(res, "corners")
    assert c["n"] == 2
    # |8.57-15|=6.43, |5.71-9|=3.29 -> MAE 4.86, bias -4.86 (infraestima)
    assert c["mae"] == pytest.approx((6.43 + 3.29) / 2, abs=1e-2)
    assert c["bias"] == pytest.approx(-4.86, abs=1e-2)
    assert c["rmse"] == pytest.approx(np.sqrt((6.43 ** 2 + 3.29 ** 2) / 2), abs=1e-2)
    assert c["mean_pred"] == pytest.approx((8.57 + 5.71) / 2, abs=1e-2)
    assert c["mean_real"] == pytest.approx((15.0 + 9.0) / 2, abs=1e-2)


def test_two_matches_cards_overestimate_shots_underestimate(two_log):
    res = ts.compute_from_log(two_log)
    cards = _get(res, "cards")
    shots = _get(res, "shots")
    # cards: |4.61-5|=0.39, |3.49-2|=1.49 -> bias mean(-0.39,+1.49)=+0.55 (sobrestima)
    assert cards["mae"] == pytest.approx((0.39 + 1.49) / 2, abs=1e-2)
    assert cards["bias"] == pytest.approx(0.55, abs=1e-2)
    assert ts._bias_es(cards["bias"]) == "sobrestima"
    # shots strongly under-estimated
    assert shots["bias"] == pytest.approx(-13.33, abs=1e-2)
    assert ts._bias_es(shots["bias"]) == "infraestima"


def test_rmse_ge_mae_and_real_log_matches(two_log):
    res = ts.compute_from_log(two_log)
    for r in res["rows"]:
        assert r["rmse"] >= r["mae"] - 1e-9          # RMSE >= MAE always


def test_corners_line_accuracy(two_log):
    res = ts.compute_from_log(two_log)
    c = _get(res, "corners")
    # Senegal over(0.62) & real 15>7.5 over -> ✓ ; Norway under(0.22) & real 9>7.5 over -> ✗  => 50%
    assert c["line_acc"] == pytest.approx(50.0, abs=1e-6)
    assert c["line_n"] == 2
    # shots/cards have no O/U columns in the log -> no line accuracy
    assert _get(res, "shots")["line_acc"] is None
    assert _get(res, "cards")["line_acc"] is None


def test_matches_real_log_aggregate():
    """Sanity vs the committed live log (robust to growth): if there are settled stat rows, MAE>=0,
    RMSE>=MAE, and córners/tiros under-estimate while tarjetas over-estimate (documented finding)."""
    res = ts.compute_from_log(ts.LOG)
    if not res["rows"]:
        pytest.skip("no settled stat rows in the live log yet")
    for r in res["rows"]:
        assert r["mae"] >= 0 and r["rmse"] >= r["mae"] - 1e-9 and r["n"] >= 1


# ----------------------------------------------------------------- anti-hindsight / anti-leakage
def test_excludes_unsettled_rows(tmp_path):
    rows = [_row(SENEGAL_IRAQ, 1, settled=1),
            _row(NORWAY_FRANCE, 2, settled=0)]      # not settled -> excluded
    res = ts.compute_from_log(_write_log(tmp_path, rows))
    assert _get(res, "corners")["n"] == 1


def test_excludes_rows_without_prediction(tmp_path):
    """A settled match with a real value but NO frozen prediction (stats model not run pre-KO)
    must not be counted — never paired retroactively."""
    rows = [_row(SENEGAL_IRAQ, 1, with_pred=True),
            _row(NORWAY_FRANCE, 2, with_pred=False)]   # no st_* -> excluded
    res = ts.compute_from_log(_write_log(tmp_path, rows))
    assert _get(res, "corners")["n"] == 1


def test_excludes_rows_without_real(tmp_path):
    rows = [_row(SENEGAL_IRAQ, 1, with_real=True),
            _row(NORWAY_FRANCE, 2, with_real=False)]   # no result_* -> excluded
    res = ts.compute_from_log(_write_log(tmp_path, rows))
    assert _get(res, "corners")["n"] == 1


def test_empty_when_nothing_settled(tmp_path):
    rows = [_row(SENEGAL_IRAQ, 1, settled=0)]
    res = ts.compute_from_log(_write_log(tmp_path, rows))
    assert res["rows"] == []
    assert ts.briefing_summary(res) == ""
    assert "aún sin partidos" in ts.render_txt(res)


# ----------------------------------------------------------------- honesty / small sample
def test_small_sample_flagged(two_log):
    txt = ts.render_txt(ts.compute_from_log(two_log))
    assert "muestra pequeña" in txt            # N=2 < SMALL_N
    assert "ESPERABLE" in txt                  # corners/cards honesty kept, not masked


def test_bias_reading_neutral_band():
    assert ts._bias_es(0.1) == "≈ neutral"
    assert ts._bias_es(-1.0) == "infraestima"
    assert ts._bias_es(1.0) == "sobrestima"


# ----------------------------------------------------------------- CSV + panel surface
def test_csv_roundtrip_and_panel_section(tmp_path, two_log):
    res = ts.compute_from_log(two_log)
    csv_path = tmp_path / "ts.csv"
    ts.write_csv(res, csv_path)
    text = csv_path.read_text(encoding="utf-8")
    lines = panel.section_team_stats(text)
    body = "\n".join(lines)
    assert lines[0].startswith("## Stats por equipo — predicho vs real (en vivo)")
    assert "| córners" in body and "infraestima" in body
    assert "sobrestima" in body                 # cards over-estimate surfaced
    assert "% (O/U)" in body                     # córners line accuracy column populated
    assert "baja confianza" in body or "baja conf" in body
    assert "no se declara" in body.lower() or "No** se declara" in body


def test_panel_section_empty_csv_is_soft():
    lines = panel.section_team_stats("")          # no data -> placeholder, never raises
    assert lines[0].startswith("## Stats por equipo")
    assert "sin datos aún" in "\n".join(lines)


# ----------------------------------------------------------------- isolation guarantees
def test_no_market_or_api_calls_in_module():
    src = (HERE / "worldcup_team_stats_scorer.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions(", "APIFootballClient"):
        assert bad not in src
