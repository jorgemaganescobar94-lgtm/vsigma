"""
Offline tests for worldcup_context_shadow (SHADOW). NO network, NO API.

Covers: scenario classification on synthetic standings (qualified/eliminated/must-win/draw-ok/
dead-rubber/knockout) · context_predict recomputes 1X2/OU coherently (mult>1 raises that team's
win+over; mult==1 -> identical to L3) · anti-hindsight (no predict after KO, never touches settled;
settle writes nothing pre-FT) · scorecard compares ctx vs L3, filters non-trivial, applies the
N>=20 criterion · nothing leaks to Telegram (module has no dispatch/manifest path).

Run:  python analysis/worldcup/test_context_shadow.py
"""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_context_shadow as C  # noqa: E402

NOW = datetime(2026, 6, 26, 12, 0, tzinfo=timezone.utc)
FUT = (NOW + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
PAST = (NOW - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")


# ---- a tiny fake L3 predictor with IDENTITY calibration (so cal == normalized raw wdl) ----
class FakePred:
    def __init__(self):
        self.strength = {"A": 0.5, "B": -0.5, "C": 0.0, "D": 0.0}
        self.a0, self.a1, self.total_mean = 0.0, 1.0, 2.6
        ident = {"ux": [0.0, 1.0], "uf": [0.0, 1.0]}
        self.iso = [dict(ident), dict(ident), dict(ident)]


def _table(rows):
    """rows: list of (name, points, played, gd)."""
    return [{"name": n, "points": p, "played": pl, "gd": gd} for n, p, pl, gd in rows]


# ----------------------------------------------------------------- scenario classification
def test_status_qualified_and_eliminated():
    # group of 4, 2 played each; leader 6 pts is mathematically safe vs the field below
    table = _table([("A", 6, 2, 5), ("B", 4, 2, 2), ("C", 1, 2, -3), ("D", 0, 2, -4)])
    qA, eA, remA, rankA = C._team_status("A", table)
    assert qA and not eA and remA == 1 and rankA == 1
    # D: 0 pts, 1 game left (max 3); two teams (A,B) already strictly above its ceiling -> eliminated
    qD, eD, remD, _ = C._team_status("D", table)
    assert eD and not qD


def test_classify_must_win_vs_draw_ok():
    # last group game (played 2). A is 1st-2nd by points -> draw ok; Y is 4th (NOT 3rd, so not the
    # best-third exception) but still mathematically alive -> must win. 3rd (B) would be neutral.
    groups = {"Group A": _table([("A", 4, 2, 3), ("X", 4, 2, 2), ("B", 4, 2, 1), ("Y", 1, 2, -6)])}
    tg = {"A": "Group A", "X": "Group A", "B": "Group A", "Y": "Group A"}
    sh, sa, mh, ma, nt = C.classify_fixture("Group Stage - 3", "A", "Y", groups, tg)
    assert sh == "le_vale_empate" and sa == "debe_ganar"
    assert mh == C.MULT["le_vale_empate"] and ma == C.MULT["debe_ganar"] and nt


def test_classify_dead_rubber_both_resolved():
    # A clinched (6=2W, only 1 rival can reach its floor), Y eliminated (0; two rivals already
    # strictly above its ceiling of 3) -> both resolved -> intrascendente. (Max 6 pts after 2 games.)
    groups = {"Group A": _table([("A", 6, 2, 6), ("X", 4, 2, 1), ("B", 1, 2, -3), ("Y", 0, 2, -4)])}
    tg = {k: "Group A" for k in ("A", "X", "B", "Y")}
    sh, sa, mh, ma, nt = C.classify_fixture("Group Stage - 3", "A", "Y", groups, tg)
    assert sh == "intrascendente" and sa == "intrascendente"     # scenario tag unchanged
    # 'intrascendente' NEUTRALIZADO a 1.00 (backtest): el escenario se sigue detectando, pero ya NO
    # ajusta -> mult 1.0/1.0 -> el partido es TRIVIAL (nt=False), idéntico a L3.
    assert mh == C.MULT["intrascendente"] == 1.0 and ma == C.MULT["intrascendente"] == 1.0
    assert not nt


def test_classify_third_place_is_neutral_in_dispute():
    # 4-group last matchday: C is 3rd by points. Top-2 logic alone would call it must-win, but in
    # the 48-team format a best third can advance -> NEUTRAL 'tercero_en_disputa' (mult 1.0).
    groups = {"G": _table([("A", 6, 2, 4), ("B", 4, 2, 1), ("C", 3, 2, 0), ("D", 0, 2, -5)])}
    tg = {k: "G" for k in ("A", "B", "C", "D")}
    sh, sa, mh, ma, nt = C.classify_fixture("Group Stage - 3", "C", "D", groups, tg)
    assert sh == "tercero_en_disputa" and mh == 1.0 and C.MULT["tercero_en_disputa"] == 1.0
    assert sa == "eliminado"          # 4th, clinched below -> still eliminated (documented residual)
    # the 3rd-placed team is NOT marked eliminado/debe_ganar (signal not polluted)
    assert sh not in ("eliminado", "debe_ganar")


def test_fixture_status_index_aet_null_fulltime_gives_none():
    fx = {"response": [
        {"fixture": {"id": 1, "status": {"short": "AET"}}, "goals": {"home": 2, "away": 1},
         "score": {"fulltime": {"home": None, "away": None}}},          # null 90' -> must be None
        {"fixture": {"id": 2, "status": {"short": "FT"}}, "goals": {"home": 3, "away": 0},
         "score": {"fulltime": {"home": 3, "away": 0}}},
    ]}

    class FakeClient:
        def request(self, path, params, ttl_hours=None):
            return fx
    idx = C._fixture_status_index(FakeClient())
    assert idx[1]["gh"] is None and idx[1]["ga"] is None   # AET w/o 90' -> no goals -> settle skips
    assert idx[2]["gh"] == 3 and idx[2]["ga"] == 0


def test_settle_skips_aet_with_null_90_score():
    tmp = Path(tempfile.mkdtemp())
    C.LOG = tmp / "log.csv"
    pd.DataFrame([{**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": 7, "settled": 0,
                   "ctx_home": 0.5}], columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C._client = lambda: None
    C._fixture_status_index = lambda client: {7: {"status": "AET", "gh": None, "ga": None}}
    C.cmd_settle()
    assert int(pd.read_csv(C.LOG).iloc[0]["settled"]) == 0   # never settled from post-ET goals


def test_classify_knockout_is_trivial():
    sh, sa, mh, ma, nt = C.classify_fixture("Round of 32", "A", "B", {}, {})
    assert sh == "knockout" and sa == "knockout" and mh == 1.0 and ma == 1.0 and not nt


def test_classify_missing_standings_unknown_trivial():
    sh, sa, mh, ma, nt = C.classify_fixture("Group Stage - 1", "A", "B", {}, {})
    assert sh == "unknown" and sa == "unknown" and not nt   # no table -> no adjustment


# ----------------------------------------------------------------- context recompute
def test_context_predict_mult_one_equals_l3():
    pred = FakePred()
    cp = C.context_predict(pred, "A", "B", 1.0, 1.0)
    assert abs(cp["ctx_home"] - cp["l3_home"]) < 1e-9
    assert abs(cp["ctx_over25"] - cp["l3_over25"]) < 1e-9


def test_context_predict_boost_raises_win_and_over():
    pred = FakePred()
    cp = C.context_predict(pred, "A", "B", 1.20, 1.0)   # boost home attack
    assert cp["ctx_home"] > cp["l3_home"], "more home xG -> more home win prob"
    assert cp["ctx_over25"] > cp["l3_over25"], "more xG -> more Over 2.5"
    assert cp["ctx_away"] < cp["l3_away"]
    # dead-rubber style cut lowers Over
    cp2 = C.context_predict(pred, "C", "D", 0.90, 0.90)
    assert cp2["ctx_over25"] < cp2["l3_over25"]


def test_context_predict_none_without_rating():
    assert C.context_predict(FakePred(), "A", "ZZ", 1.0, 1.0) is None


# ----------------------------------------------------------------- anti-hindsight
def _seed_cards(tmp, rows):
    C.CARDS = tmp / "cards.csv"
    pd.DataFrame(rows).to_csv(C.CARDS, index=False)


def test_predict_skips_after_ko_and_no_invention():
    tmp = Path(tempfile.mkdtemp())
    _seed_cards(tmp, [{"fixture_id": 1, "kickoff_utc": PAST, "home": "A", "away": "B",
                       "round": "Group Stage - 3", "our_home": 0.5}])
    C.LOG = tmp / "log.csv"
    C.load_predictor = lambda: FakePred()
    C._client = lambda: None
    C.fetch_standings = lambda client, day=None: []
    C.build_status_maps = lambda s: ({}, {})
    C.cmd_predict(now=NOW)
    assert not C.LOG.exists() or len(pd.read_csv(C.LOG)) == 0   # KO passed -> nothing logged


def test_predict_logs_pre_ko_and_freezes_settled():
    tmp = Path(tempfile.mkdtemp())
    _seed_cards(tmp, [
        {"fixture_id": 1, "kickoff_utc": FUT, "home": "A", "away": "B",
         "round": "Group Stage - 3", "our_home": 0.5},        # NS -> (re)predicted
        {"fixture_id": 2, "kickoff_utc": PAST, "home": "C", "away": "D",
         "round": "Group Stage - 3", "our_home": 0.4},        # KO passed -> not first-logged
    ])
    C.LOG = tmp / "log.csv"
    pd.DataFrame([{**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": 9, "kickoff_utc": PAST,
                   "home": "C", "away": "D", "ctx_home": 0.7, "settled": 1, "result_1x2": "H",
                   "nontrivial": 1}], columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C.load_predictor = lambda: FakePred()
    C._client = lambda: None
    # both A and B in last game, both alive -> non-trivial scenario
    groups = {"G": _table([("A", 4, 2, 2), ("X", 4, 2, 2), ("B", 3, 2, 0), ("Y", 0, 2, -4)])}
    tg = {"A": "G", "X": "G", "B": "G", "Y": "G"}
    C.fetch_standings = lambda client, day=None: [{}]
    C.build_status_maps = lambda s: (groups, tg)
    C.cmd_predict(now=NOW)
    df = pd.read_csv(C.LOG)
    assert 1 in set(df["fixture_id"]) and 2 not in set(df["fixture_id"])  # only NS logged
    f9 = df[df.fixture_id == 9].iloc[0]
    assert int(f9["settled"]) == 1 and abs(f9["ctx_home"] - 0.7) < 1e-9   # settled row frozen


def test_settle_writes_nothing_before_ft():
    tmp = Path(tempfile.mkdtemp())
    C.LOG = tmp / "log.csv"
    pd.DataFrame([{**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": 7, "settled": 0,
                   "ctx_home": 0.5}], columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C._client = lambda: None
    C._fixture_status_index = lambda client: {7: {"status": "NS", "gh": None, "ga": None}}
    C.cmd_settle()
    df = pd.read_csv(C.LOG)
    assert int(df.iloc[0]["settled"]) == 0 and pd.isna(df.iloc[0]["result_1x2"])


def test_settle_fills_real_result_after_ft():
    tmp = Path(tempfile.mkdtemp())
    C.LOG = tmp / "log.csv"
    pd.DataFrame([{**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": 7, "settled": 0,
                   "ctx_home": 0.5}], columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C._client = lambda: None
    C._fixture_status_index = lambda client: {7: {"status": "FT", "gh": 2, "ga": 1}}
    C.cmd_settle()
    df = pd.read_csv(C.LOG)
    assert int(df.iloc[0]["settled"]) == 1 and df.iloc[0]["result_1x2"] == "H"
    assert df.iloc[0]["result_ft_gh"] == 2 and df.iloc[0]["result_ft_ga"] == 1


# ----------------------------------------------------------------- scorecard
def test_scorecard_compares_and_small_sample():
    tmp = Path(tempfile.mkdtemp())
    C.LOG = tmp / "log.csv"; C.SCORECARD = tmp / "sc.txt"
    rows = []
    for i in range(6):
        rows.append({**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": i, "home": "A", "away": "B",
                     "scenario_home": "debe_ganar", "scenario_away": "eliminado", "nontrivial": 1,
                     "l3_home": 0.5, "l3_draw": 0.3, "l3_away": 0.2, "l3_over25": 0.5,
                     "ctx_home": 0.6, "ctx_draw": 0.25, "ctx_away": 0.15, "ctx_over25": 0.55,
                     "result_ft_gh": 2, "result_ft_ga": 1, "result_1x2": "H", "settled": 1})
    # one TRIVIAL settled row that must be EXCLUDED from the comparison
    rows.append({**{c: np.nan for c in C.LOG_COLUMNS}, "fixture_id": 99, "home": "C", "away": "D",
                 "scenario_home": "knockout", "scenario_away": "knockout", "nontrivial": 0,
                 "l3_home": 0.5, "l3_draw": 0.3, "l3_away": 0.2, "ctx_home": 0.5, "ctx_draw": 0.3,
                 "ctx_away": 0.2, "result_1x2": "H", "settled": 1})
    pd.DataFrame(rows, columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C.cmd_scorecard()
    txt = C.SCORECARD.read_text(encoding="utf-8")
    assert "CRITERIO DE GRADUACIÓN" in txt and "N>=20" in txt
    assert "MUESTRA INSUFICIENTE" in txt and "SIGUE EN SOMBRA" in txt
    assert "NO trivial=6" in txt and "triviales (sin cambio, excluidos)=1" in txt
    assert "L3 puro" in txt and "context-adj" in txt


def test_scorecard_empty_is_safe():
    tmp = Path(tempfile.mkdtemp())
    C.LOG = tmp / "log.csv"; C.SCORECARD = tmp / "sc.txt"
    pd.DataFrame(columns=C.LOG_COLUMNS).to_csv(C.LOG, index=False)
    C.cmd_scorecard()
    assert "Aún sin partidos" in C.SCORECARD.read_text(encoding="utf-8")


def test_no_telegram_leak():
    # no SEND vector: no dispatcher import/call, no manifest, no HTTP send. (A doc mention of
    # "NOT shown on Telegram" is fine; we forbid the actual leak mechanisms.)
    src = Path(C.__file__).read_text(encoding="utf-8").lower()
    for bad in ("dispatch_telegram", "manifest", "sendmessage", "urllib", "api.telegram"):
        assert bad not in src, f"context shadow must not reference '{bad}' (send vector)"


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} context-shadow tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
