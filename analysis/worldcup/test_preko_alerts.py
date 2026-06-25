"""
Offline tests for the PRE-KO focused alert (build_worldcup_preko_alerts). NO network, NO API.

Covers: selection only of imminent + BOTH-XI-confirmed + not-already-sent fixtures · anti-hindsight
(started/settled fixtures never selected) · dedup (a fixture alerted once is never re-selected) ·
no candidates -> silent (empty manifest) · message carries the confirmed-XI props + honesty note.

Run:  python analysis/worldcup/test_preko_alerts.py
"""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_worldcup_preko_alerts as A  # noqa: E402

NOW = datetime(2026, 6, 26, 18, 0, tzinfo=timezone.utc)


def _ko(mins_from_now):
    return (NOW + timedelta(minutes=mins_from_now)).strftime("%Y-%m-%d %H:%M")


def _card(fid, mins, lh="conf", la="conf", **kw):
    base = {"fixture_id": fid, "kickoff_utc": _ko(mins), "home": "Germany", "away": "Mexico",
            "home_group": "Group A", "lineup_home": lh, "lineup_away": la,
            "our_home": 0.55, "our_draw": 0.25, "our_away": 0.20,
            "our_xg_home": 1.8, "our_xg_away": 1.0}
    base.update(kw)
    return base


def test_selects_imminent_confirmed_unsent():
    cards = pd.DataFrame([_card(1, 60)])
    cands = A.select_candidates(cards, sent_ids=set(), now=NOW)
    assert len(cands) == 1 and int(cands[0][0]["fixture_id"]) == 1
    assert 55 < cands[0][1] < 61   # ~60 min to KO


def test_skips_not_yet_confirmed():
    cards = pd.DataFrame([
        _card(1, 60, lh="prob", la="conf"),   # one team only probable
        _card(2, 60, lh="conf", la="pend"),   # one team pending
        _card(3, 60, lh="conf", la="conf"),   # both confirmed -> the only one selected
    ])
    cands = A.select_candidates(cards, sent_ids=set(), now=NOW)
    assert [int(c[0]["fixture_id"]) for c in cands] == [3]


def test_skips_outside_window_and_started():
    cards = pd.DataFrame([
        _card(1, 200),    # too far (>90 min)
        _card(2, -10),    # already kicked off -> anti-hindsight, never selected
        _card(3, 0),      # exactly at KO -> not strictly pre-KO
        _card(4, 45),     # in window -> selected
    ])
    cands = A.select_candidates(cards, sent_ids=set(), now=NOW)
    assert [int(c[0]["fixture_id"]) for c in cands] == [4]


def test_dedup_skips_already_sent():
    cards = pd.DataFrame([_card(1, 60), _card(2, 60)])
    cands = A.select_candidates(cards, sent_ids={1}, now=NOW)
    assert [int(c[0]["fixture_id"]) for c in cands] == [2]


def test_missing_lineup_columns_soft():
    # cards built with no imminent fixture may lack lineup_* columns entirely -> select nothing
    cards = pd.DataFrame([{"fixture_id": 1, "kickoff_utc": _ko(60), "home": "A", "away": "B"}])
    assert A.select_candidates(cards, sent_ids=set(), now=NOW) == []


def test_render_message_confirmed_props_and_honesty():
    r = pd.Series(_card(1, 58, adj_home=0.50, adj_draw=0.27, adj_away=0.23,
                         adj_absent_home="Musiala"))
    title, body = A.render_message(r, 58.0, props_fn=lambda fid: [
        "⚠️ EXPERIMENTAL · heurístico · SIN VALIDAR (...): (XI confirmado)",
        "  Gol: K. Havertz 30%"])
    txt = "\n".join(body)
    assert "Alineación confirmada" in body[0]
    assert "Saque en ~58 min" in body[1]
    assert "Resultado L3" in txt and "fuerza de selección" in txt
    assert "Ajuste por bajas" in txt and "sin Musiala" in txt    # L3-adj line
    assert "(XI confirmado)" in txt                              # confirmed-XI props
    assert "NO mejora" in txt                                    # honesty note
    assert "alineación confirmada" in title.lower()


def test_cmd_select_silent_when_no_candidates():
    td = Path(tempfile.mkdtemp())
    A.CARDS = td / "cards.csv"; A.MANIFEST = td / "man.txt"
    A.PENDING = td / "pend.csv"; A.PREVIEW = td / "prev.txt"; A.OUT_DIR = td
    pd.DataFrame([_card(1, 300)]).to_csv(A.CARDS, index=False)   # nothing imminent
    n = A.cmd_select(now=NOW)
    assert n == 0
    assert A.MANIFEST.read_text(encoding="utf-8") == ""          # empty manifest -> send nothing


def test_select_then_marksent_then_no_resend():
    td = Path(tempfile.mkdtemp())
    A.CARDS = td / "cards.csv"; A.MANIFEST = td / "man.txt"; A.PENDING = td / "pend.csv"
    A.PREVIEW = td / "prev.txt"; A.SENT = td / "sent.csv"; A.OUT_DIR = td
    pd.DataFrame([_card(7, 60)]).to_csv(A.CARDS, index=False)
    # run 1: selects fixture 7, writes manifest + pending (NOT yet marked)
    assert A.cmd_select(now=NOW) == 1
    assert A.MANIFEST.read_text(encoding="utf-8").strip() != ""
    # a re-select BEFORE marking would still pick it (not yet sent) — dedup is post-send
    assert A.cmd_select(now=NOW) == 1
    # mark sent (called after the send step), then re-select -> silent (dedup)
    A.cmd_mark_sent()
    assert 7 in A._load_sent_ids()
    assert A.cmd_select(now=NOW) == 0
    assert A.MANIFEST.read_text(encoding="utf-8") == ""


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} preko-alert tests passed (no network, no API).")


if __name__ == "__main__":
    _run()
