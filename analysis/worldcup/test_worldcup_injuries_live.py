"""
Offline tests for the LIVE injuries adjustment (worldcup_injuries_live). No network, no market.

Covers: position bucketing, per-team xG deltas (offensive -> own xG down; defensive -> opponent
xG up; caps; key-only), the fixture adjustment direction (losing a key attacker lowers the team's
win prob and xG; losing a key defender raises the opponent's xG), exact reversal (flag off / no key
absence -> None -> no inj_*), honest label, soft-fail, and the forever store-guard roundtrip.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_injuries_live as il  # noqa: E402


# Two squads. Brazil: top-5 regulars in every position + a fringe. Korea: one top-5 defender
# (key) + mid-league regulars (tier 0.6 -> never key). League/country tiers reuse the committed
# squad_strength_model (Spain/La Liga -> 1.0, England/Premier League -> 1.0, K League 1 -> 0.6).
ROWS = [
    {"team": "Brazil", "player_name": "Vinicius Jr", "position": "Attacker",
     "club_country": "Spain", "club_league": "La Liga", "apps": 30},
    {"team": "Brazil", "player_name": "Casemiro", "position": "Midfielder",
     "club_country": "Spain", "club_league": "La Liga", "apps": 30},
    {"team": "Brazil", "player_name": "Marquinhos", "position": "Defender",
     "club_country": "Spain", "club_league": "La Liga", "apps": 30},
    {"team": "Brazil", "player_name": "Alisson", "position": "Goalkeeper",
     "club_country": "England", "club_league": "Premier League", "apps": 30},
    {"team": "Brazil", "player_name": "B. Reserva", "position": "Attacker",
     "club_country": "Brazil", "club_league": "Serie A", "apps": 2},
    {"team": "Korea", "player_name": "K. Kim", "position": "Defender",
     "club_country": "Spain", "club_league": "La Liga", "apps": 30},
    {"team": "Korea", "player_name": "K. Min", "position": "Attacker",
     "club_country": "South Korea", "club_league": "K League 1", "apps": 28},
    {"team": "Korea", "player_name": "K. Sub", "position": "Midfielder",
     "club_country": "South Korea", "club_league": "K League 1", "apps": 20},
]


@pytest.fixture()
def idx(tmp_path):
    p = tmp_path / "squad.csv"
    pd.DataFrame(ROWS).to_csv(p, index=False)
    return il.load_squad_index(p)


# ----------------------------------------------------------------- position bucket
def test_position_bucket():
    assert il.position_bucket("Attacker") == "off"
    assert il.position_bucket("Midfielder") == "mid"
    assert il.position_bucket("Defender") == "def"
    assert il.position_bucket("Goalkeeper") == "gk"
    assert il.position_bucket("") == "mid"        # unknown -> moderate (mid)
    assert il.position_bucket(None) == "mid"


# ----------------------------------------------------------------- per-team deltas
def test_team_delta_offensive_lowers_own_xg(idx):
    own, conc, hits = il.team_injury_delta(idx["Brazil"], ["Vinicius Jr"])
    assert own == pytest.approx(0.12) and conc == 0.0
    assert hits[0]["name"] == "Vinicius Jr" and hits[0]["bucket"] == "off"


def test_team_delta_midfielder(idx):
    own, conc, _ = il.team_injury_delta(idx["Brazil"], ["Casemiro"])
    assert own == pytest.approx(0.07) and conc == 0.0


def test_team_delta_defender_and_gk_raise_concede(idx):
    own_d, conc_d, _ = il.team_injury_delta(idx["Brazil"], ["Marquinhos"])
    assert own_d == 0.0 and conc_d == pytest.approx(0.05)
    own_g, conc_g, _ = il.team_injury_delta(idx["Brazil"], ["Alisson"])
    assert own_g == 0.0 and conc_g == pytest.approx(0.04)


def test_team_delta_non_key_is_zero(idx):
    # fringe (low apps) and mid-league regulars never move it
    assert il.team_injury_delta(idx["Brazil"], ["B. Reserva"]) == (0.0, 0.0, [])
    assert il.team_injury_delta(idx["Korea"], ["K. Min", "K. Sub"]) == (0.0, 0.0, [])


def test_team_delta_own_cap(idx, tmp_path):
    big = ROWS + [
        {"team": "Brazil", "player_name": f"Att {i}", "position": "Attacker",
         "club_country": "Spain", "club_league": "La Liga", "apps": 30} for i in range(8)
    ]
    p = tmp_path / "big.csv"
    pd.DataFrame(big).to_csv(p, index=False)
    idx2 = il.load_squad_index(p)
    names = ["Vinicius Jr", "Casemiro"] + [f"Att {i}" for i in range(8)]
    own, _, _ = il.team_injury_delta(idx2["Brazil"], names)
    assert own == pytest.approx(il.CAP_OWN)        # capped at 0.40


def test_no_match_is_zero(idx):
    assert il.team_injury_delta(idx["Brazil"], ["Nobody Unknown"]) == (0.0, 0.0, [])


# ----------------------------------------------------------------- fixture adjustment
BASE = (0.60, 0.22, 0.18)          # displayed motor (e.g. mx_*) for Brazil vs Korea
BXH, BXA = 2.00, 0.60


def test_offensive_home_absence_lowers_home(idx):
    a = il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx, inj_home=["Vinicius Jr"], inj_away=[])
    assert a is not None
    assert a["inj_xg_home"] == pytest.approx(1.88)      # 2.00 - 0.12
    assert a["inj_xg_away"] == pytest.approx(0.60)
    assert a["inj_home"] < BASE[0]                       # losing a key attacker -> lower home win
    assert a["inj_basis"] == "inj"
    assert abs(a["inj_home"] + a["inj_draw"] + a["inj_away"] - 1.0) < 1e-6
    assert "Vinicius Jr" in a["inj_absent_home"]


def test_defensive_away_absence_raises_home_xg(idx):
    a = il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx, inj_home=[], inj_away=["K. Kim"])
    assert a is not None
    assert a["inj_xg_home"] == pytest.approx(2.05)      # Korea's key defender out -> Brazil +0.05
    assert a["inj_xg_away"] == pytest.approx(0.60)
    assert a["inj_home"] > BASE[0]                       # weaker opponent defence -> higher home win
    assert a["inj_concede_away"] == pytest.approx(0.05)


def test_no_key_absence_returns_none(idx):
    assert il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx, inj_home=[], inj_away=[]) is None
    # only non-key absences -> still None (exact reversal: no inj_* written)
    assert il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx,
        inj_home=["B. Reserva"], inj_away=["K. Min"]) is None


def test_flag_off_returns_none(idx, monkeypatch):
    monkeypatch.setattr(il, "INJURIES_LIVE", False)
    assert il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx, inj_home=["Vinicius Jr"], inj_away=[]) is None


def test_soft_fail_on_bad_base(idx):
    # NaN base xg -> None (soft), never raises
    assert il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, np.nan, BXA, idx, inj_home=["Vinicius Jr"]) is None
    assert il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", (np.nan, np.nan, np.nan), BXH, BXA, idx,
        inj_home=["Vinicius Jr"]) is None


def test_xi_refinement_basis(idx):
    a = il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx, inj_home=[], inj_away=[],
        xi_out_home=["Vinicius Jr"], xi_out_away=[])
    assert a is not None and a["inj_basis"] == "inj+xi"
    assert a["inj_xg_home"] == pytest.approx(1.88)


def test_note_wording(idx):
    a = il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, BXH, BXA, idx,
        inj_home=["Vinicius Jr", "Casemiro"], inj_away=["K. Kim"])
    note = a["inj_note"]
    assert note.startswith("Ajustado por bajas:")
    assert "ajuste live, sin validar" in note
    assert "Brazil 2 baja(s) (incl. Vinicius Jr)" in note   # offensive star leads the label
    assert "Korea 1 baja(s) (incl. K. Kim)" in note


def test_xg_floor(idx, tmp_path):
    # an away team that concedes a lot can't push the home xG below the floor for the OTHER side;
    # here force a tiny base xg and many home offensive absences -> floored, never negative
    big = ROWS + [
        {"team": "Brazil", "player_name": f"Att {i}", "position": "Attacker",
         "club_country": "Spain", "club_league": "La Liga", "apps": 30} for i in range(8)
    ]
    p = tmp_path / "big.csv"
    pd.DataFrame(big).to_csv(p, index=False)
    idx2 = il.load_squad_index(p)
    names = ["Vinicius Jr", "Casemiro"] + [f"Att {i}" for i in range(8)]
    a = il.compute_fixture_injury_adjustment(
        "Brazil", "Korea", BASE, 0.20, BXA, idx2, inj_home=names)
    assert a["inj_xg_home"] >= il.XG_FLOOR


# ----------------------------------------------------------------- forever store-guard
def test_store_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(il, "STORE_DIR", tmp_path / "inj")
    assert il.load_injuries_store(999) is None
    il.save_injuries_store(999, {"Brazil": [("Vinicius Jr", "Knee")]})
    got = il.load_injuries_store(999)
    assert got == {"Brazil": [["Vinicius Jr", "Knee"]]}     # tuples persisted as lists


def test_no_market_calls_in_module():
    src = (HERE / "worldcup_injuries_live.py").read_text(encoding="utf-8")
    for bad in ('request("/odds"', "request('/odds'", 'request("/predictions"',
                "request('/predictions'", ".odds(", ".predictions("):
        assert bad not in src
