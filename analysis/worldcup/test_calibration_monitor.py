"""
Offline tests for worldcup_calibration_monitor (NOISE-ADAPTIVE threshold). NO network/API/Telegram.

Covers: well-calibrated log with HIGH absolute ECE but < null p95 -> NO alert (the false-alarm fix) ·
genuinely miscalibrated (ECE >> null p95) -> alert · logloss >= baseline -> alert (independent of
ECE) · N<15 -> never alert · reproducibility (seeded null -> identical verdict) · monitor NEVER
writes the predictions log.

Run:  python analysis/worldcup/test_calibration_monitor.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_calibration_monitor as M  # noqa: E402


def _rows(specs):
    return pd.DataFrame([{"fixture_id": i, "settled": 1, "result_1x2": res,
                          "l3_home": h, "l3_draw": d, "l3_away": a}
                         for i, (h, d, a, res) in enumerate(specs)])


# A PERFECTLY-CALIBRATED-BY-CONSTRUCTION log: varied, informative favourites with outcomes drawn
# FROM each row's own probs (fixed seed). Spread confidence -> non-trivial absolute ECE, but it is
# a sample from the null so it stays < null p95. seed=2 lands ECE≈0.25 (>2× the old 0.12 threshold).
_PROTOS = [(0.5, 0.3, 0.2), (0.6, 0.25, 0.15), (0.7, 0.2, 0.1), (0.45, 0.30, 0.25),
           (0.15, 0.20, 0.65), (0.25, 0.30, 0.45), (0.40, 0.30, 0.30), (0.55, 0.25, 0.20)]


def _calibrated(n=20, seed=2):
    rng = np.random.default_rng(seed)
    P = np.array([_PROTOS[i % len(_PROTOS)] for i in range(n)], float)
    cum = np.cumsum(P, 1)
    y = (rng.random(n)[:, None] < cum).argmax(1)
    res = np.array(["H", "D", "A"])[y]
    return pd.DataFrame({"fixture_id": range(n), "settled": 1, "result_1x2": res,
                         "l3_home": P[:, 0], "l3_draw": P[:, 1], "l3_away": P[:, 2]})


# Overconfident: says 0.9 but favourites win only ~50% -> ECE far above the null.
MISCAL = [(0.9, 0.05, 0.05, "H")] * 10 + [(0.9, 0.05, 0.05, "A")] * 10
# Model == marginal base rate -> logloss equal (>=) but ECE≈0 (low-ECE, logloss-only failure).
LL_BAD = [(0.4, 0.3, 0.3, "H")] * 8 + [(0.4, 0.3, 0.3, "D")] * 6 + [(0.4, 0.3, 0.3, "A")] * 6


# ----------------------------------------------------------------- evaluate (pure)
def test_high_ece_within_null_no_alert():
    """THE FIX: a calibrated log whose absolute ECE is high (would trip the OLD fixed 0.12) but is
    still within sampling noise (< null p95) must NOT alert."""
    ev = M.evaluate(_calibrated(20, seed=2))
    assert ev["sufficient"] and ev["n"] == 20
    assert ev["ece"] > 0.12, "this case must exceed the OLD fixed threshold (else it proves nothing)"
    assert ev["null_p"] > 0.12, "adaptive threshold at small N must be well above the old 0.12"
    assert ev["ece"] < ev["null_p"] and ev["alert"] is False and ev["reasons"] == []


def test_miscalibrated_above_null_alerts():
    ev = M.evaluate(_rows(MISCAL))
    assert ev["sufficient"] and ev["ece"] > ev["null_p"] and ev["alert"] is True
    assert any("nulo" in r for r in ev["reasons"])


def test_logloss_not_better_than_base_alerts_independent():
    ev = M.evaluate(_rows(LL_BAD))
    assert ev["sufficient"] and ev["ece"] <= ev["null_p"]          # ECE within noise -> no ECE reason
    assert ev["logloss"] >= ev["base_logloss"] and ev["alert"] is True
    assert any("logloss" in r for r in ev["reasons"]) and not any("nulo" in r for r in ev["reasons"])


def test_small_sample_never_alerts():
    ev = M.evaluate(_rows(MISCAL[:14]))                            # N=14 < 15
    assert ev["n"] == 14 and ev["sufficient"] is False and ev["alert"] is False


def test_reproducible_seeded_verdict():
    df = _calibrated(18, seed=3)
    a, b = M.evaluate(df), M.evaluate(df)
    assert a["null_p"] == b["null_p"] and a["alert"] == b["alert"]  # seeded null -> stable
    # and the null percentile itself is deterministic for fixed P
    P = df[["l3_home", "l3_draw", "l3_away"]].to_numpy(float)
    assert M.null_ece_pctl(P) == M.null_ece_pctl(P)


def test_empty_and_no_l3_columns_safe():
    assert M.evaluate(pd.DataFrame())["alert"] is False
    df = pd.DataFrame([{"settled": 1, "result_1x2": "H"}])
    assert M.evaluate(df)["n"] == 0 and M.evaluate(df)["alert"] is False


# ----------------------------------------------------------------- cmd_run (I/O + anti-spam)
def _setup(tmp, df):
    M.LOG = Path(tmp) / "worldcup_predictions_log.csv"
    M.REPORT = Path(tmp) / "mon.txt"
    M.STATE = Path(tmp) / "state.json"
    df.to_csv(M.LOG, index=False)
    sent = []
    M.send_alert = lambda title, body: sent.append((title, body))
    return sent


def test_cmd_run_insufficient_writes_report_no_alert():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, _rows(MISCAL[:14]))
        res = M.cmd_run()
        assert res["status"] == "MUESTRA INSUFICIENTE" and res["sent"] is False and sent == []
        assert "MUESTRA INSUFICIENTE" in M.REPORT.read_text(encoding="utf-8")


def test_cmd_run_calibrated_high_ece_is_OK():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, _calibrated(20, seed=2))
        res = M.cmd_run()
        assert res["status"] == "OK" and res["sent"] is False and sent == []
        txt = M.REPORT.read_text(encoding="utf-8")
        assert "dentro del ruido" in txt and "nulo p95" in txt


def test_cmd_run_alert_sends_once_antispam():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, _rows(MISCAL))
        r1 = M.cmd_run()
        assert r1["status"] == "ALERTA" and r1["sent"] is True and len(sent) == 1
        assert "nulo p95" in sent[0][1]
        r2 = M.cmd_run()
        assert r2["sent"] is False and len(sent) == 1               # anti-spam


def test_cmd_run_clears_then_refires():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, _rows(MISCAL))
        M.cmd_run()                                                  # alert (1)
        _calibrated(20, seed=2).to_csv(M.LOG, index=False)           # clears -> OK
        ok = M.cmd_run()
        assert ok["status"] == "OK" and ok["sent"] is False and len(sent) == 1
        _rows(MISCAL).to_csv(M.LOG, index=False)                     # returns -> re-fire
        assert M.cmd_run()["sent"] is True and len(sent) == 2


def test_cmd_run_never_writes_predictions_log():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp, _rows(MISCAL))
        before = M.LOG.read_bytes()
        M.cmd_run()
        assert M.LOG.read_bytes() == before, "monitor must NOT modify the predictions log"
        assert M.REPORT.exists() and M.STATE.exists()


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} calibration-monitor tests passed (no network, no API, no Telegram).")


if __name__ == "__main__":
    _run()
