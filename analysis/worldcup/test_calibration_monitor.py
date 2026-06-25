"""
Offline tests for worldcup_calibration_monitor. NO network, NO API, NO Telegram (send is patched).

Covers: well-calibrated log (N>=20, beats base) -> no alert · miscalibrated (high ECE) -> alert ·
logloss >= baseline (low ECE) -> alert · N<20 -> never alert · anti-spam (identical alert not
repeated; clears + re-fires) · monitor NEVER writes the predictions log.

Run:  python analysis/worldcup/test_calibration_monitor.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import worldcup_calibration_monitor as M  # noqa: E402


def _rows(specs):
    return pd.DataFrame([{"fixture_id": i, "settled": 1, "result_1x2": res,
                          "l3_home": h, "l3_draw": d, "l3_away": a}
                         for i, (h, d, a, res) in enumerate(specs)])


# Well-calibrated AND more informative than the marginal base rate (two distinct, internally
# calibrated favourites): conf 0.7 ≈ accuracy 0.7 -> ECE≈0; logloss < base-rate logloss.
CALIB = ([(0.7, 0.2, 0.1, "H")] * 7 + [(0.7, 0.2, 0.1, "D")] * 2 + [(0.7, 0.2, 0.1, "A")] * 1 +
         [(0.1, 0.2, 0.7, "A")] * 7 + [(0.1, 0.2, 0.7, "D")] * 2 + [(0.1, 0.2, 0.7, "H")] * 1)
# Overconfident: says 0.9 but wins only ~50% -> ECE≈0.4.
MISCAL = [(0.9, 0.05, 0.05, "H")] * 10 + [(0.9, 0.05, 0.05, "A")] * 10
# Model == marginal base rate -> logloss equal (>=) but ECE≈0 (low-ECE failure).
LL_BAD = [(0.4, 0.3, 0.3, "H")] * 8 + [(0.4, 0.3, 0.3, "D")] * 6 + [(0.4, 0.3, 0.3, "A")] * 6


# ----------------------------------------------------------------- evaluate (pure)
def test_well_calibrated_no_alert():
    ev = M.evaluate(_rows(CALIB))
    assert ev["sufficient"] and ev["n"] == 20
    assert ev["ece"] <= M.ECE_MAX and ev["logloss"] < ev["base_logloss"]
    assert ev["alert"] is False and ev["reasons"] == []


def test_miscalibrated_high_ece_alerts():
    ev = M.evaluate(_rows(MISCAL))
    assert ev["sufficient"] and ev["ece"] > M.ECE_MAX
    assert ev["alert"] is True
    assert any("ECE" in r for r in ev["reasons"])


def test_logloss_not_better_than_base_alerts():
    ev = M.evaluate(_rows(LL_BAD))
    assert ev["sufficient"] and ev["ece"] <= M.ECE_MAX        # low ECE, still alerts on logloss
    assert ev["logloss"] >= ev["base_logloss"] and ev["alert"] is True
    assert any("logloss" in r for r in ev["reasons"])


def test_small_sample_never_alerts():
    ev = M.evaluate(_rows(MISCAL[:19]))                       # N=19 < 20
    assert ev["n"] == 19 and ev["sufficient"] is False and ev["alert"] is False


def test_empty_and_no_l3_columns_safe():
    assert M.evaluate(pd.DataFrame()) ["alert"] is False
    df = pd.DataFrame([{"settled": 1, "result_1x2": "H"}])    # no l3_* columns
    assert M.evaluate(df)["n"] == 0 and M.evaluate(df)["alert"] is False


# ----------------------------------------------------------------- cmd_run (I/O + anti-spam)
def _setup(tmp, specs):
    M.LOG = Path(tmp) / "worldcup_predictions_log.csv"
    M.REPORT = Path(tmp) / "mon.txt"
    M.STATE = Path(tmp) / "state.json"
    _rows(specs).to_csv(M.LOG, index=False)
    sent = []
    M.send_alert = lambda title, body: sent.append((title, body))
    return sent


def test_cmd_run_insufficient_writes_report_no_alert():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, CALIB[:19])
        res = M.cmd_run()
        assert res["status"] == "MUESTRA INSUFICIENTE" and res["sent"] is False and sent == []
        txt = M.REPORT.read_text(encoding="utf-8")
        assert "MUESTRA INSUFICIENTE" in txt and "N=19" in txt


def test_cmd_run_alert_sends_once_antispam():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, MISCAL)
        r1 = M.cmd_run()
        assert r1["status"] == "ALERTA" and r1["sent"] is True and len(sent) == 1
        assert "Calibración L3 fuera de umbral" in sent[0][1]
        # identical situation next run -> anti-spam: NOT re-sent
        r2 = M.cmd_run()
        assert r2["status"] == "ALERTA" and r2["sent"] is False and len(sent) == 1


def test_cmd_run_clears_then_refires():
    with tempfile.TemporaryDirectory() as tmp:
        sent = _setup(tmp, MISCAL)
        M.cmd_run()                                  # alert (1)
        _rows(CALIB).to_csv(M.LOG, index=False)      # situation clears -> OK
        ok = M.cmd_run()
        assert ok["status"] == "OK" and ok["sent"] is False and len(sent) == 1
        _rows(MISCAL).to_csv(M.LOG, index=False)     # returns -> must re-fire
        again = M.cmd_run()
        assert again["sent"] is True and len(sent) == 2


def test_cmd_run_never_writes_predictions_log():
    with tempfile.TemporaryDirectory() as tmp:
        _setup(tmp, MISCAL)
        before = M.LOG.read_bytes()
        M.cmd_run()
        assert M.LOG.read_bytes() == before, "monitor must NOT modify the predictions log"
        # only its own artifacts exist
        assert M.REPORT.exists() and M.STATE.exists()


def _run():
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"  PASS {fn.__name__}")
    print(f"\n{len(fns)}/{len(fns)} calibration-monitor tests passed (no network, no API, no Telegram).")


if __name__ == "__main__":
    _run()
