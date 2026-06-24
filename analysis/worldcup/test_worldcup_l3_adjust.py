"""
Offline tests for the L3-adj heuristic live adjustment (mock predictor + squad, no network).

Covers: the rule (key absence -> correct nudge, cap, no-match -> 0), XI refinement, soft
(no data -> no adjustment), no leakage (only listed absentees move it), L3 left untouched,
and the scorecard adding an L3+adj row without changing the L3 row. Zero odds/predictions.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_l3_adjust as adj  # noqa: E402


# ----------------------------------------------------------------- fakes
class FakePred:
    """Stand-in for l3_offline.Predictor with identity isotonic curves."""
    def __init__(self, strength):
        self.strength = strength
        self.a0 = 0.0
        self.a1 = 1.5
        self.total_mean = 2.66
        # identity isotonic over [0,1]
        self.iso = [{"ux": [0.0, 1.0], "uf": [0.0, 1.0]} for _ in range(3)]


def squad_index(monkeypatch, tmp_path, rows):
    df = pd.DataFrame(rows)
    p = tmp_path / "squad.csv"
    df.to_csv(p, index=False)
    return adj.load_squad_index(p)


# A small two-team squad: Brazil has a top-5 star (tier 1.0) + a strong-league regular (0.8);
# Korea has only mid-league players (tier 0.6 -> never triggers a nudge).
ROWS = [
    {"team": "Brazil", "player_name": "Vinicius Jr", "club_country": "Spain",
     "club_league": "La Liga", "apps": 30},                       # tier 1.00 regular
    {"team": "Brazil", "player_name": "J. Silva", "club_country": "Portugal",
     "club_league": "Primeira Liga", "apps": 25},                 # tier 0.80 regular
    {"team": "Brazil", "player_name": "B. Reserva", "club_country": "Brazil",
     "club_league": "Serie A", "apps": 2},                        # tier 0.60 fringe
    {"team": "Korea", "player_name": "K. Min", "club_country": "South Korea",
     "club_league": "K League 1", "apps": 28},                    # tier 0.60
    {"team": "Korea", "player_name": "P. Sub", "club_country": "South Korea",
     "club_league": "K League 1", "apps": 20},
]


@pytest.fixture()
def idx(tmp_path):
    return squad_index(None, tmp_path, ROWS)


def test_tier_step_and_key_player(idx):
    bz = idx["Brazil"]
    # Vinicius Jr -> tier 1.0 regular -> step 0.08
    d, hits = adj.team_delta(bz, ["Vinicius Jr"])
    assert d == pytest.approx(-0.08) and hits == ["Vinicius Jr"]
    # strong-league regular -> 0.05
    d2, _ = adj.team_delta(bz, ["J. Silva"])
    assert d2 == pytest.approx(-0.05)
    # both -> 0.13
    d3, hits3 = adj.team_delta(bz, ["Vinicius Jr", "J. Silva"])
    assert d3 == pytest.approx(-0.13) and set(hits3) == {"Vinicius Jr", "J. Silva"}


def test_fringe_and_mid_tier_no_nudge(idx):
    # tier 0.60 fringe (Brazil) and mid-league Korea regulars -> no nudge
    assert adj.team_delta(idx["Brazil"], ["B. Reserva"]) == (0.0, [])
    assert adj.team_delta(idx["Korea"], ["K. Min", "P. Sub"]) == (0.0, [])


def test_cap(idx, tmp_path):
    # many key absences must not exceed the -0.25 cap
    big = ROWS + [
        {"team": "Brazil", "player_name": f"Star {i}", "club_country": "England",
         "club_league": "Premier League", "apps": 30} for i in range(6)
    ]
    idx2 = squad_index(None, tmp_path, big)
    names = ["Vinicius Jr", "J. Silva"] + [f"Star {i}" for i in range(6)]
    d, hits = adj.team_delta(idx2["Brazil"], names)
    assert d == pytest.approx(-0.25)            # capped
    assert len(hits) >= 5


def test_no_match_is_zero(idx):
    assert adj.team_delta(idx["Brazil"], ["Nobody Unknown"]) == (0.0, [])


def test_compute_fixture_adjustment_injuries(idx):
    pred = FakePred({"Brazil": 1.8, "Korea": 0.4})
    base = adj.predict_adjusted(pred, "Brazil", "Korea", 0.0, 0.0)
    a = adj.compute_fixture_adjustment(pred, idx, "Brazil", "Korea",
                                       inj_home=["Vinicius Jr"], inj_away=[])
    assert a["adj_basis"] == "inj"
    assert a["adj_delta_home"] == pytest.approx(-0.08) and a["adj_delta_away"] == 0.0
    assert a["adj_absent_home"] == "Vinicius Jr"
    # losing a key home player lowers Brazil's win prob vs the unadjusted base
    assert a["adj_home"] < base["adj_home"]


def test_no_absence_returns_none(idx):
    pred = FakePred({"Brazil": 1.8, "Korea": 0.4})
    assert adj.compute_fixture_adjustment(pred, idx, "Brazil", "Korea",
                                          inj_home=[], inj_away=[]) is None
    # only mid/fringe absences -> still None (no adjustment shown)
    assert adj.compute_fixture_adjustment(pred, idx, "Brazil", "Korea",
                                          inj_home=["B. Reserva"], inj_away=["K. Min"]) is None


def test_xi_refinement_basis(idx):
    pred = FakePred({"Brazil": 1.8, "Korea": 0.4})
    lu_home = {"confirmed": True, "xi_names": [f"P{i}" for i in range(10)] + ["J. Silva"]}
    # Vinicius Jr is NOT in the XI and not injured -> key player out of XI
    out = adj.key_players_out_of_xi(idx["Brazil"], lu_home, injured_names=[])
    assert "Vinicius Jr" in out and "J. Silva" not in out
    a = adj.compute_fixture_adjustment(pred, idx, "Brazil", "Korea",
                                       inj_home=[], inj_away=[],
                                       xi_out_home=out, xi_out_away=[])
    assert a["adj_basis"] == "inj+xi"
    assert a["adj_delta_home"] == pytest.approx(-0.08)


def test_xi_not_confirmed_returns_none(idx):
    assert adj.key_players_out_of_xi(idx["Brazil"],
                                     {"confirmed": False, "xi_names": []}, []) is None


def test_no_leakage_only_listed_absentees(idx):
    # an injury list that names a player NOT key, plus an empty one, must not move it
    pred = FakePred({"Brazil": 1.8, "Korea": 0.4})
    a = adj.compute_fixture_adjustment(pred, idx, "Brazil", "Korea",
                                       inj_home=["B. Reserva"], inj_away=[])
    assert a is None  # nothing key absent -> no phantom adjustment


# ----------------------------------------------------------------- scorecard integration
import worldcup_learning_loop as ll  # noqa: E402


def _settled_log_with_adj():
    """Two settled fixtures: one WITH an adjustment, one WITHOUT (adj NaN)."""
    rows = [
        {"fixture_id": 1, "home": "Brazil", "away": "Korea", "kickoff_utc": "2026-06-20 19:00",
         "l3_home": 0.6, "l3_draw": 0.22, "l3_away": 0.18, "l3_xg_home": 1.9, "l3_xg_away": 0.8,
         "adj_home": 0.55, "adj_draw": 0.24, "adj_away": 0.21, "adj_basis": "inj",
         "adj_delta_home": -0.08, "adj_delta_away": 0.0,
         "adj_absent_home": "Vinicius Jr", "adj_absent_away": "",
         "result_ft_gh": 1, "result_ft_ga": 1, "result_1x2": "D", "settled": 1},
        {"fixture_id": 2, "home": "Spain", "away": "Japan", "kickoff_utc": "2026-06-20 22:00",
         "l3_home": 0.5, "l3_draw": 0.27, "l3_away": 0.23, "l3_xg_home": 1.6, "l3_xg_away": 1.0,
         "adj_home": np.nan, "adj_draw": np.nan, "adj_away": np.nan, "adj_basis": np.nan,
         "result_ft_gh": 2, "result_ft_ga": 0, "result_1x2": "H", "settled": 1},
    ]
    return pd.DataFrame(rows)


def test_scorecard_adds_l3adj_row_without_changing_l3(tmp_path, monkeypatch):
    log = tmp_path / "log.csv"
    df = _settled_log_with_adj()
    for c in ll.LOG_COLUMNS:
        if c not in df.columns:
            df[c] = np.nan
    df[ll.LOG_COLUMNS].to_csv(log, index=False)
    monkeypatch.setattr(ll, "LOG", log)
    sc = tmp_path / "scorecard.txt"
    monkeypatch.setattr(ll, "SCORECARD", sc)
    ll.cmd_scorecard()
    text = sc.read_text(encoding="utf-8")
    assert "L3+adj" in text                       # detail table has the secondary row
    assert "(4b)" in text                         # active-only block present
    # L3 row still present and unchanged-looking (its own line in the detail table)
    assert any(line.strip().startswith("L3 ") for line in text.splitlines())


def test_no_market_calls_in_module():
    # the module makes NO API calls at all; assert no market call signatures appear in code
    src = (HERE / "worldcup_l3_adjust.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions("):
        assert bad not in src
