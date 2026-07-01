"""
Offline tests for the tournament Monte Carlo (worldcup_tournament_sim). NO network, NO API.

Covers: bracket build from (synthetic) fixtures · the VALIDATION GUARD (reproduces the populated
octavos -> ok; a mismatch -> NOT ok, no odds) · Monte Carlo invariants (sum P(champion)~=100% among
alive, seed reproducible, eliminated teams = 0, played-R32 winners are FIXED facts) · a clear
favourite gets more P than a minnow · reversibility (TOURNAMENT_SIM=False -> no section).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_tournament_sim as T  # noqa: E402


def _fx(round_, home, away, played=False, winner=None, date="2026-07-01T12:00:00+00:00", fid=1):
    return {"fixture": {"id": fid, "date": date, "status": {"short": "FT" if played else "NS"}},
            "league": {"round": round_},
            "teams": {"home": {"name": home, "winner": (winner == home) if played else None},
                      "away": {"name": away, "winner": (winner == away) if played else None}}}


def _synthetic(populate_r16=True, wrong_r16=False):
    """16 R32 (date-ordered A0..A15 vs B0..B15); slots 0-6 PLAYED (home Ak wins). R16 fixtures for the
    slots whose both feeders are played, matching R16_MAP -> guard should PASS (or wrong -> FAIL)."""
    fx = []
    for k in range(16):
        fx.append(_fx("Round of 32", f"A{k}", f"B{k}", played=(k <= 6), winner=f"A{k}",
                      date=f"2026-06-28T{k:02d}:00:00+00:00", fid=100 + k))   # monotonic -> date-idx==k
    win = {k: f"A{k}" for k in range(7)}   # slots 0..6 winners
    if populate_r16:
        for a, b in T.R16_MAP:
            if a in win and b in win:       # both feeders decided -> the API would have this R16
                fx.append(_fx("Round of 16", win[a], win[b], fid=200 + a))
    if wrong_r16:
        fx.append(_fx("Round of 16", "A0", "A4", fid=999))   # NOT a real map pairing -> guard fail
    return fx


def _predict_factory(strong=None):
    """Neutral-ish predict: 'strong' team wins 0.9; vs 'strong' 0.1; else 0.5. Draw 0.2."""
    def predict(a, b):
        if a == strong:
            ph = 0.9
        elif b == strong:
            ph = 0.1
        else:
            ph = 0.5
        return {"our_home": ph - 0.1, "our_draw": 0.2, "our_away": 0.9 - ph}
    return predict


class _FakeClient:
    def __init__(self, fixtures):
        self._fx = fixtures

    def request(self, path, params=None, **kw):
        return {"response": self._fx if path == "/fixtures" else []}


# ----------------------------------------------------------------- bracket + guard
def test_build_bracket_needs_full_r32():
    assert T.build_bracket([]) is None                       # no R32 -> None
    br = T.build_bracket(_synthetic())
    assert br is not None and len(br["r32"]) == 16


def test_guard_passes_when_map_reproduces_octavos():
    br = T.build_bracket(_synthetic(populate_r16=True))
    ok, detail = T.validate_guard(br)
    assert ok, detail
    assert "reproducidos por el cuadro=3" in detail          # 3 populated R16 all reproduced


def test_guard_fails_on_mismatch_and_blocks_odds():
    br = T.build_bracket(_synthetic(populate_r16=True, wrong_r16=True))
    ok, detail = T.validate_guard(br)
    assert not ok and "DESAJUSTE" in detail
    # run_sim must return NO odds when the guard fails (never publish a wrong tree)
    odds, ok2, _ = T.run_sim(client=_FakeClient(_synthetic(wrong_r16=True)), predict=_predict_factory())
    assert odds is None and ok2 is False


def test_guard_no_octavos_yet_does_not_publish():
    br = T.build_bracket(_synthetic(populate_r16=False))      # no R16 populated
    ok, detail = T.validate_guard(br)
    assert not ok and "checked=0" in detail                  # nothing to validate -> do NOT publish


# ----------------------------------------------------------------- Monte Carlo invariants
def test_sim_sum_champion_is_100pct_and_eliminated_zero():
    odds, ok, _ = T.run_sim(client=_FakeClient(_synthetic()), predict=_predict_factory("A3"), n=5000)
    assert ok and odds
    s = sum(v["p_champ"] for v in odds.values())
    assert abs(s - 1.0) < 1e-9                                # exactly one champion per iteration
    # a played-R32 LOSER (B0) is eliminated -> 0 everywhere
    assert odds["B0"]["p_champ"] == 0.0 and odds["B0"]["p_semi"] == 0.0
    # sums across rounds: 2 finalists, 4 semifinalists
    assert abs(sum(v["p_final"] for v in odds.values()) - 2.0) < 1e-9
    assert abs(sum(v["p_semi"] for v in odds.values()) - 4.0) < 1e-9


def test_sim_seed_reproducible():
    a, _, _ = T.run_sim(client=_FakeClient(_synthetic()), predict=_predict_factory("A3"), n=3000, seed=42)
    b, _, _ = T.run_sim(client=_FakeClient(_synthetic()), predict=_predict_factory("A3"), n=3000, seed=42)
    assert a == b                                            # same seed -> identical odds


def test_played_r32_winner_is_fixed_fact():
    # A5 won its R32 (played) and B5 lost -> B5 has 0 champion prob, A5 > 0
    odds, ok, _ = T.run_sim(client=_FakeClient(_synthetic()), predict=_predict_factory(), n=3000)
    assert odds["B5"]["p_champ"] == 0.0 and odds["A5"]["p_semi"] > 0.0


def test_clear_favourite_beats_minnow():
    odds, ok, _ = T.run_sim(client=_FakeClient(_synthetic()), predict=_predict_factory("A3"), n=8000)
    # A3 (strong, and advanced as a played winner) must dominate a random alive team
    assert odds["A3"]["p_champ"] > 0.30
    assert odds["A3"]["p_champ"] > odds["A6"]["p_champ"]


# ----------------------------------------------------------------- reversibility
def test_flag_off_no_section(monkeypatch):
    monkeypatch.setattr(T, "TOURNAMENT_SIM", False)
    assert T.tournament_block() == []                        # flag off -> nothing rendered (no API)
