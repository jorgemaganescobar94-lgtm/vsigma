"""
Offline tests for the shared player-events core + external adapters. No network, no API, no betting.
Covers: Poisson expansion (1+/2+ shots/SOT), no-fabrication when inputs/sources are missing, rankings
(sorted, zero-dropped, never padded), set-piece hierarchy with/without history and primary-absent
promotion, two-XI scenarios, heuristic matchups degradation, honest confidence flags, and adapters
returning None + reason when the external source is absent.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import player_events_core as core  # noqa: E402
import player_data_adapters as adapters  # noqa: E402


def _row(player, pid, team, lam_goal=0.0, exp_shots=0.0, lam_son=0.0, lam_assist=0.0, p_card=None,
         is_xi=1, basis="probable_by_squad_starts"):
    return {"player": player, "player_id": pid, "team": team, "is_xi": is_xi, "basis": basis,
            "lam_goal": lam_goal, "exp_shots": exp_shots, "lam_shot_on": lam_son,
            "lam_assist": lam_assist, "p_card": p_card}


# ----------------------------------------------------------------- Poisson
def test_poisson_helpers():
    assert core.p_ge1(0.0) == 0.0
    assert core.p_ge1(1.0) == pytest.approx(1 - math.exp(-1))
    assert core.p_ge2(1.0) == pytest.approx(1 - math.exp(-1) * 2)
    # 2+ always <= 1+
    for lam in (0.1, 0.5, 1.0, 2.0):
        assert core.p_ge2(lam) <= core.p_ge1(lam) + 1e-12


def test_expand_player_metrics_and_no_fabrication():
    e = core.expand_player(_row("A", 1, "T", lam_goal=0.4, exp_shots=2.0, lam_son=0.8,
                                lam_assist=0.2, p_card=0.15))
    assert e["probability_goal"] == pytest.approx(1 - math.exp(-0.4), abs=1e-4)
    assert e["expected_goals"] == 0.4
    assert e["probability_1plus_shot"] > e["probability_2plus_shot"]
    assert e["expected_sot"] == 0.8
    assert e["probability_card"] == 0.15
    # xA / key passes NOT provided -> None, never invented
    assert e["expected_xa"] is None and e["expected_key_passes"] is None
    # with an adapter value they appear
    e2 = core.expand_player(_row("A", 1, "T", lam_assist=0.2), xa90=0.31, key_passes90=1.4)
    assert e2["expected_xa"] == 0.31 and e2["expected_key_passes"] == 1.4


def test_confidence_flags_honest():
    assert core.expand_player(_row("A", 1, "T"))["data_quality"] == "baja"        # no rates
    assert core.expand_player(_row("A", 1, "T", lam_goal=0.3,
                                   basis="lineup_confirmed"))["data_quality"] == "alta"
    assert core.expand_player(_row("A", 1, "T", lam_goal=0.3,
                                   basis="probable_by_squad_starts"))["data_quality"] == "media"


# ----------------------------------------------------------------- rankings
def test_rankings_sorted_and_zero_dropped():
    exp = [core.expand_player(_row("Hi", 1, "T", lam_goal=0.5, exp_shots=3, lam_son=1.2, lam_assist=0.3)),
           core.expand_player(_row("Mid", 2, "T", lam_goal=0.2, exp_shots=1, lam_son=0.4, lam_assist=0.1)),
           core.expand_player(_row("Zero", 3, "T", lam_goal=0.0, exp_shots=0, lam_son=0, lam_assist=0))]
    sc = core.likely_scorers(exp, 3)
    assert [s["player"] for s in sc] == ["Hi", "Mid"]        # Zero dropped, sorted
    assert len(core.likely_shots_on_target(exp, 5)) == 2     # never padded to 5


def test_card_risk_floor():
    exp = [core.expand_player(_row("Risky", 1, "T", lam_goal=0.1, p_card=0.40)),
           core.expand_player(_row("Calm", 2, "T", lam_goal=0.1, p_card=0.05))]
    cr = core.card_risk(exp, 4, min_p=0.12)
    assert [c["player"] for c in cr] == ["Risky"] and cr[0]["confidence"] == "baja"


# ----------------------------------------------------------------- set-piece (§4)
def test_set_piece_no_history_is_not_fabricated():
    sp = core.set_piece_hierarchy([1, 2, 3], {1: "A", 2: "B", 3: "C"}, penalty_history=None)
    assert sp["penalties"]["primary"] is None
    assert sp["penalties"]["confidence"] == "baja" and "evento" in sp["penalties"]["reason"].lower()


def test_set_piece_with_history_ranks_and_confidence():
    sp = core.set_piece_hierarchy([1, 2, 3], {1: "A", 2: "B", 3: "C"},
                                  penalty_history={1: 4, 2: 1, 3: 0})
    assert sp["penalties"]["primary"] == "A" and sp["penalties"]["secondary"] == "B"
    assert sp["penalties"]["confidence"] == "alta"           # 4 pens, dominant


def test_set_piece_primary_absent_from_xi():
    # historical taker (id 9) NOT in the probable XI -> not chosen, honest flag
    sp = core.set_piece_hierarchy([1, 2], {1: "A", 2: "B", 9: "Star"},
                                  penalty_history={9: 5, 1: 1})
    assert sp["penalties"]["primary"] == "A"                 # 9 excluded (not in XI)


def test_set_piece_injured_excluded():
    sp = core.set_piece_hierarchy([1, 2], {1: "A", 2: "B"}, penalty_history={1: 5, 2: 2},
                                  injured_ids=[1])
    assert sp["penalties"]["primary"] == "B"                 # injured primary dropped


# ----------------------------------------------------------------- scenarios + matchups
def test_scenario_delta():
    prob = [core.expand_player(_row("A", 1, "T", lam_goal=0.3)),
            core.expand_player(_row("B", 2, "T", lam_goal=0.2))]
    assert core.scenario_delta(prob, None)["available"] is False
    alt = [core.expand_player(_row("A", 1, "T", lam_goal=0.3)),
           core.expand_player(_row("C", 3, "T", lam_goal=0.25))]
    d = core.scenario_delta(prob, alt)
    assert d["available"] is True
    kinds = {c["player"]: c["change"] for c in d["changes"]}
    assert kinds.get("C") == "ENTRA" and kinds.get("B") == "SALE"


def test_matchups_degrade_without_data():
    mu = core.key_matchups(None, None)
    assert mu[0]["advantage"] == "no determinado"
    mu2 = core.key_matchups({"team": "H", "attack_xg": 2.0}, {"team": "A", "attack_xg": 1.0})
    assert mu2[0]["advantage"] == "H" and mu2[0]["confidence"] == "baja"


def test_build_player_predictions_schema():
    h = [core.expand_player(_row("A", 1, "H", lam_goal=0.4, exp_shots=2, lam_son=0.9, lam_assist=0.2))]
    a = [core.expand_player(_row("B", 2, "A", lam_goal=0.3, exp_shots=1.5, lam_son=0.6, lam_assist=0.15))]
    sp = core.set_piece_hierarchy([1], {1: "A"})
    obj = core.build_player_predictions({"fixture_id": 1, "home": "H", "away": "A"}, h, a, sp, sp,
                                        core.key_matchups(None, None))
    pp = obj["player_predictions"]
    for k in ("likely_scorers", "likely_shots_on_target", "likely_assisters", "set_piece_takers",
              "card_risk", "key_matchups"):
        assert k in pp
    assert obj["data_quality"] in ("alta", "media", "baja")


# ----------------------------------------------------------------- adapters (external, graceful)
def test_adapters_absent_return_none_reason(tmp_path):
    xa, reason = adapters.load_xa_rates(tmp_path / "nope.csv")
    assert xa == {} and "no configurada" in reason
    ref, rr = adapters.load_referee_tendency("Mr Ref", tmp_path / "nope.csv")
    assert ref is None and "no configurada" in rr
    w, wr = adapters.load_weather(123, tmp_path / "nope.csv")
    assert w is None and "no configurado" in wr


def test_adapter_xa_loads_when_present(tmp_path):
    p = tmp_path / "xa.csv"
    pd.DataFrame([{"player_id": 7, "xa90": 0.33, "key_passes90": 1.8}]).to_csv(p, index=False)
    xa, reason = adapters.load_xa_rates(p)
    assert xa[7]["xa90"] == 0.33 and xa[7]["key_passes90"] == 1.8


def test_adapter_referee_levels(tmp_path):
    p = tmp_path / "ref.csv"
    pd.DataFrame([{"referee": "Strict Sam", "cards_per_match": 5.2}]).to_csv(p, index=False)
    ref, _ = adapters.load_referee_tendency("strict sam", p)
    assert ref["level"] == "alto"


def test_modules_have_no_network_or_secret_writes():
    """Real isolation property: the modules never call the network, an odds/predictions endpoint, or
    WRITE secrets/.env (reading os.environ.get for an optional key is allowed)."""
    for f in ("player_events_core.py", "player_data_adapters.py"):
        src = (HERE / f).read_text(encoding="utf-8")
        for bad in ('requests.', "urllib", "httpx", 'request("/odds"', "request('/odds'",
                    'request("/predictions"', "APIFootballClient",
                    'open(".env"', "os.environ[", "environ.setdefault"):
            assert bad not in src, f"{f} contiene patrón prohibido: {bad}"
