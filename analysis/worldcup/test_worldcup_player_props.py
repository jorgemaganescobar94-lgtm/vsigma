"""
Offline tests for worldcup_player_props (SHADOW). NO network, NO API.
Covers: share normalization, P=1-exp(-lam) in [0,1], anti-hindsight (no predict after KO,
never touches settled), settle writes nothing pre-FT, scorecard metrics, no leakage.

Run:  python analysis/worldcup/test_worldcup_player_props.py
"""
from __future__ import annotations

import math
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_player_props as P  # noqa: E402

NOW = datetime.now(timezone.utc)
FUT = (NOW + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
PAST = (NOW - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")

# 11 synthetic starters with varied rates
RATES = {i: {"name": f"P{i}", "starts": 20 - i, "minutes": 1800.0,
             "g90": 0.5 if i == 1 else 0.1, "a90": 0.3 if i == 2 else 0.1,
             "sh90": 3.0 if i == 1 else 1.0, "son90": 1.2, "c90": 0.2,
             "on_ratio": 0.4} for i in range(1, 12)}
XI = list(RATES.keys())


def test_poisson_p_in_range():
    for lam in (0.0, 0.01, 0.5, 2.0, 50.0):
        p = P.poisson_p_ge1(lam)
        assert 0.0 <= p <= 1.0
    assert P.poisson_p_ge1(0.0) == 0.0
    assert abs(P.poisson_p_ge1(1.0) - (1 - math.exp(-1))) < 1e-12


def test_shares_normalize_to_one():
    sh = P._shares(XI, RATES, "g90")
    assert abs(sum(sh.values()) - 1.0) < 1e-9
    assert all(v >= 0 for v in sh.values())
    # player 1 has the highest g90 -> highest share
    assert max(sh, key=sh.get) == 1


def test_shares_uniform_when_all_zero():
    zero = {i: {"minutes": 100.0} for i in XI}
    sh = P._shares(XI, zero, "g90")
    assert all(abs(v - 1.0 / len(XI)) < 1e-9 for v in sh.values())


def test_predict_distributes_team_total_with_attribution():
    preds = P.predict_fixture(team_xg=2.0, team_shots=12.0, match_cards=4.0, xi=XI, rates=RATES)
    assert len(preds) == 11
    # goal lambdas sum to XI_ATTR * team_xg (rest unattributed)
    sum_lam_goal = sum(p["lam_goal"] for p in preds)
    assert abs(sum_lam_goal - P.XI_ATTR * 2.0) < 1e-9
    # shots distribute the team shots fully (no attribution factor on shots)
    assert abs(sum(p["exp_shots"] for p in preds) - 12.0) < 1e-9
    # all probabilities valid
    for p in preds:
        for k in ("p_goal", "p_card", "p_shot_on", "p_assist"):
            assert 0.0 <= p[k] <= 1.0


def test_predict_uses_exact_lambda_for_probability():
    preds = P.predict_fixture(2.0, 12.0, 4.0, XI, RATES)
    for p in preds:
        assert abs(p["p_goal"] - (1 - math.exp(-p["lam_goal"]))) < 1e-12


def _seed(rows):
    P.LOG = Path(tempfile.mkdtemp()) / "props_log.csv"
    if rows is not None:
        pd.DataFrame(rows, columns=P.LOG_COLUMNS).to_csv(P.LOG, index=False)


def test_anti_hindsight_predict_skips_after_ko(monkeypatch=None):
    # cards.csv with one fixture whose KO already passed -> predict must add nothing
    tmp = Path(tempfile.mkdtemp())
    P.CARDS = tmp / "cards.csv"; P.LOG = tmp / "props_log.csv"
    pd.DataFrame([{"fixture_id": 1, "kickoff_utc": PAST, "home": "A", "away": "B",
                   "our_xg_home": 1.5, "our_xg_away": 1.0, "st_shots_home": 10,
                   "st_shots_away": 9, "st_cards_total": 4}]).to_csv(P.CARDS, index=False)
    P._fixture_team_index = lambda client: {1: (100, 200, "NS")}
    P._client = lambda: None
    P.cmd_predict()
    assert not P.LOG.exists() or len(pd.read_csv(P.LOG)) == 0


def test_settle_writes_nothing_before_ft():
    tmp = Path(tempfile.mkdtemp())
    P.LOG = tmp / "props_log.csv"
    pd.DataFrame([{**{c: np.nan for c in P.LOG_COLUMNS},
                   "fixture_id": 7, "player_id": 50, "kickoff_utc": PAST, "settled": 0,
                   "p_goal": 0.3}], columns=P.LOG_COLUMNS).to_csv(P.LOG, index=False)
    P._fixture_team_index = lambda client: {7: (1, 2, "NS")}   # NOT finished
    called = {"n": 0}
    def _boom(*a, **k):
        called["n"] += 1
        return None
    P._get = _boom
    P._client = lambda: None
    P.cmd_settle()
    df = pd.read_csv(P.LOG)
    assert int(df.iloc[0]["settled"]) == 0          # unchanged
    assert pd.isna(df.iloc[0]["act_goal"])          # no actual written pre-FT


def test_scorecard_metrics_and_small_sample_note():
    tmp = Path(tempfile.mkdtemp())
    P.LOG = tmp / "props_log.csv"; P.SCORECARD = tmp / "sc.txt"
    rows = []
    for i in range(6):
        rows.append({**{c: np.nan for c in P.LOG_COLUMNS}, "fixture_id": i, "player_id": i,
                     "p_goal": 0.2, "p_card": 0.25, "p_shot_on": 0.6, "p_assist": 0.15,
                     "act_goal": i % 2, "act_card": 0, "act_shots_on": (2 if i % 2 else 0),
                     "act_assist": 0, "settled": 1})
    pd.DataFrame(rows, columns=P.LOG_COLUMNS).to_csv(P.LOG, index=False)
    P.cmd_scorecard()
    txt = P.SCORECARD.read_text(encoding="utf-8")
    assert "CRITERIO DE GRADUACIÓN" in txt and "N>=30" in txt
    assert "MUESTRA INSUFICIENTE" in txt
    assert "goal" in txt and "logloss" in txt


def test_get_xi_fallback_excludes_non_callups():
    P._get = lambda *a, **k: []   # no confirmed lineup -> fallback path
    # player 1 has the MOST starts but is NOT called up -> must be excluded
    rates = {i: {"name": f"P{i}", "starts": float(100 - i)} for i in range(1, 14)}
    squad = {i: f"P{i}" for i in range(2, 13)}   # call-ups = 2..12 (11 players)
    xi, basis = P.get_xi(None, 1, 99, rates, squad)
    assert basis == "probable_by_squad_starts"
    assert 1 not in xi, "highest-starts player must be excluded when not in the squad"
    assert set(xi) == set(range(2, 13))
    assert len(xi) == 11


def test_get_xi_recent_starts_outrank_history():
    P._get = lambda *a, **k: []   # no confirmed lineup -> probable path
    squad = {i: f"P{i}" for i in range(1, 14)}          # 13 call-ups, XI picks 11
    # historical starts ascending with id: 13,12,11 are the "historical" front-runners
    rates = {i: {"name": f"P{i}", "starts": float(i), "minutes": 90.0 * i} for i in range(1, 14)}
    # players 1 & 2 (historical also-rans) have STARTED the most RECENTLY
    recent = {1: 8.0, 2: 7.0}
    xi, basis = P.get_xi(None, 1, 99, rates, squad, recent)
    assert basis == "probable_by_recent_starts"
    assert 1 in xi and 2 in xi, "recent starters must enter the probable XI"
    # the two lowest-history call-ups with NO recent starts drop out
    assert 3 not in xi and 4 not in xi, "displaced by the recent starters"
    # the recent starters lead the ranking order
    assert xi[0] == 1 and xi[1] == 2
    assert len(xi) == 11 and set(xi) <= set(squad)


def test_get_xi_recent_soft_fallback_to_history():
    P._get = lambda *a, **k: []
    squad = {i: f"P{i}" for i in range(1, 13)}
    rates = {i: {"name": f"P{i}", "starts": float(100 - i), "minutes": 900.0} for i in range(1, 13)}
    # no recent data ({} or None) -> fall back to accumulated history, OLD basis
    for rec in ({}, None):
        xi, basis = P.get_xi(None, 1, 99, rates, squad, rec)
        assert basis == "probable_by_squad_starts"
        assert xi[0] == 1, "lowest id == most historical starts ranks first"


def test_get_xi_recent_excludes_non_callups():
    P._get = lambda *a, **k: []
    # a non-call-up (id 999) with huge recent starts must NEVER appear
    rates = {i: {"name": f"P{i}", "starts": 5.0} for i in range(1, 13)}
    rates[999] = {"name": "Impostor", "starts": 50.0}
    squad = {i: f"P{i}" for i in range(1, 12)}     # 11 call-ups, 999 NOT among them
    recent = {999: 8.0, 1: 6.0}
    xi, _ = P.get_xi(None, 1, 99, rates, squad, recent)
    assert 999 not in xi and len(xi) == 11
    assert set(xi) == set(range(1, 12))


def test_fetch_recent_starts_counts_startxi_and_softfails(monkeypatch=None):
    # synthetic /fixtures (2 FT + 1 NS) then per-fixture lineups via a stubbed _get / store
    P.STORE_DIR = Path(tempfile.mkdtemp())
    fixtures = [
        {"fixture": {"id": 10, "status": {"short": "FT"}}},
        {"fixture": {"id": 11, "status": {"short": "FT"}}},
        {"fixture": {"id": 12, "status": {"short": "NS"}}},   # not finished -> ignored
    ]
    lineups = {
        10: [{"team": {"id": 99}, "startXI": [{"player": {"id": 1}}, {"player": {"id": 2}}]}],
        11: [{"team": {"id": 99}, "startXI": [{"player": {"id": 1}}, {"player": {"id": 3}}]},
             {"team": {"id": 77}, "startXI": [{"player": {"id": 500}}]}],  # other team ignored
    }

    def _fake_get(client, path, params, ttl):
        if path == "/fixtures":
            return fixtures
        if path == "/fixtures/lineups":
            return lineups.get(int(params["fixture"]))
        return None
    P._get = _fake_get
    rec = P.fetch_recent_starts(None, 99)
    assert rec.get(1) == 2.0          # started both finished matches
    assert rec.get(2) == 1.0 and rec.get(3) == 1.0
    assert 500 not in rec             # belonged to the opponent
    assert 12 not in [k for k in rec]  # NS fixture never counted


def test_get_xi_empty_squad_no_invention():
    P._get = lambda *a, **k: []
    rates = {i: {"name": f"P{i}", "starts": 10.0} for i in range(1, 15)}
    assert P.get_xi(None, 1, 99, rates, None) == ([], "no_squad")
    assert P.get_xi(None, 1, 99, rates, {})[0] == []        # empty squad -> no XI invented


def test_get_xi_confirmed_lineup_is_authoritative():
    lineup = [{"team": {"id": 99}, "startXI": [{"player": {"id": i}} for i in range(1, 12)]}]
    P._get = lambda *a, **k: lineup
    xi, basis = P.get_xi(None, 1, 99, {}, {500: "irrelevant"})
    assert basis == "lineup_confirmed" and xi == list(range(1, 12))


def test_lock_at_ko_repredicts_ns_and_freezes_settled():
    tmp = Path(tempfile.mkdtemp())
    P.CARDS = tmp / "cards.csv"; P.LOG = tmp / "log.csv"
    pd.DataFrame([
        {"fixture_id": 1, "kickoff_utc": FUT, "home": "A", "away": "B", "our_xg_home": 1.6,
         "our_xg_away": 1.0, "st_shots_home": 11, "st_shots_away": 9, "st_cards_total": 4},
        {"fixture_id": 2, "kickoff_utc": PAST, "home": "C", "away": "D", "our_xg_home": 1.2,
         "our_xg_away": 1.1, "st_shots_home": 10, "st_shots_away": 10, "st_cards_total": 4},
    ]).to_csv(P.CARDS, index=False)
    pd.DataFrame([
        {**{c: np.nan for c in P.LOG_COLUMNS}, "fixture_id": 1, "player_id": 1, "p_goal": 0.99,
         "settled": 0, "is_xi": 1},                                   # STALE NS row -> to be replaced
        {**{c: np.nan for c in P.LOG_COLUMNS}, "fixture_id": 2, "player_id": 5, "p_goal": 0.5,
         "act_goal": 1, "settled": 1, "is_xi": 1},                    # SETTLED row -> must be frozen
    ], columns=P.LOG_COLUMNS).to_csv(P.LOG, index=False)
    rates = {i: {"name": f"P{i}", "starts": 11 - i, "minutes": 900.0, "g90": 0.2, "a90": 0.1,
                 "sh90": 1.0, "son90": 0.4, "c90": 0.1, "on_ratio": 0.4} for i in range(1, 12)}
    P._client = lambda: None
    P._fixture_team_index = lambda c: {1: (10, 20, "NS"), 2: (30, 40, "FT")}
    P.fetch_team_rates = lambda c, tid: dict(rates)
    P.fetch_squad = lambda c, tid: {i: f"P{i}" for i in range(1, 12)}
    P._get = lambda *a, **k: []
    P.cmd_predict()
    df = pd.read_csv(P.LOG)
    f1, f2 = df[df.fixture_id == 1], df[df.fixture_id == 2]
    assert len(f1) > 0 and 0.99 not in set(round(x, 2) for x in f1["p_goal"].dropna()), "NS rows must be re-predicted"
    assert len(f2) == 1 and int(f2.iloc[0]["settled"]) == 1, "settled fixture frozen (1 row)"
    assert f2.iloc[0]["act_goal"] == 1 and abs(f2.iloc[0]["p_goal"] - 0.5) < 1e-9, "settled row untouched"


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} player-props tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
