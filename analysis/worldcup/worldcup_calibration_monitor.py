"""
WORLD CUP — L3 1X2 CALIBRATION MONITOR.  Safety net for the auto-learning loop.

Monitor + alert ONLY. It does NOT touch the model, ratings, calibration, lock-at-KO, briefing or
props. It just READS the settled predictions log, measures the LIVE calibration of the PRODUCTION
1X2 (the same l3_* columns the scorecard grades), and fires ONE Telegram alert if it drifts.

WHY: the isotonic calibration is FROZEN (burn-in <2024); the auto-refit changes the RATINGS, not the
calibration. Risk: learned ratings drift away from the frozen calibrated mapping and the 1X2 quietly
loses calibration. This monitor catches that and warns — it never "fixes" anything automatically.

THRESHOLDS (defined a priori, honest + anti-false-alarm):
  * Needs N>=20 settled predictions. Below that -> NO alert ("muestra insuficiente").
  * ALERT if ECE > 0.12 (miscalibrated)  OR  logloss(L3) >= logloss(base-rate) (model not beating
    the naive base rate = it is failing).
Anti-spam: at most ONE alert per run, and an identical alert is not repeated on consecutive days
(small JSON state holds the last alert signature; it re-fires when the situation changes or clears
and returns).

SAFEGUARDS: NO betting endpoints. Reads ONLY the predictions log; writes ONLY its own report + state.
Telegram via the shared dispatcher (fail-soft, no secrets printed). SOFT-FAIL everywhere. Explicit
git add (report + state).
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).resolve().parent
ROOT = OUT_DIR.parents[1]
sys.path.insert(0, str(OUT_DIR))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import worldcup_learning_loop as L  # noqa: E402  (reuse the EXACT scorecard metrics: ECE/logloss/brier)

LOG = OUT_DIR / "worldcup_predictions_log.csv"
REPORT = OUT_DIR / "worldcup_calibration_monitor.txt"
STATE = OUT_DIR / "worldcup_calibration_monitor_state.json"
DISPATCHER = ROOT / "scripts" / "dispatch_telegram_alert.py"

N_MIN = 20         # minimum settled predictions before the monitor is allowed to judge/alert
ECE_MAX = 0.12     # ECE above this -> miscalibrated -> alert


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def evaluate(log):
    """Pure: live calibration of the production L3 1X2 over settled rows. Returns a dict with n,
    sufficient, metrics, baseline, alert flag + reasons. NO I/O, NO Telegram."""
    out = {"n": 0, "sufficient": False, "alert": False, "reasons": [],
           "ece": None, "logloss": None, "brier": None,
           "base_logloss": None, "base_brier": None}
    if log is None or len(log) == 0:
        return out
    settled = log[log["settled"].fillna(0).astype(int) == 1]
    settled = settled[settled["result_1x2"].isin(["H", "D", "A"])]
    cols = ["l3_home", "l3_draw", "l3_away"]
    if not all(c in settled.columns for c in cols) or len(settled) == 0:
        return out
    P = settled[cols].to_numpy(float)
    ok = ~np.isnan(P).any(axis=1)
    P = P[ok]
    y = settled["result_1x2"].map({"H": 0, "D": 1, "A": 2}).to_numpy(int)[ok]
    n = len(y)
    out["n"] = n
    if n < N_MIN:
        return out                      # insufficient sample -> never alert
    out["sufficient"] = True
    Y = np.eye(3)[y]
    m = L._metrics(P, Y)                # identical math to the scorecard (ECE on max-conf reliability)
    base = np.bincount(y, minlength=3) / n
    mb = L._metrics(np.tile(base, (n, 1)), Y)
    out.update(ece=m["ece"], logloss=m["logloss"], brier=m["brier"],
               base_logloss=mb["logloss"], base_brier=mb["brier"])
    reasons = []
    if m["ece"] > ECE_MAX:
        reasons.append(f"ECE={m['ece']:.3f} > {ECE_MAX:.2f} (descalibrado)")
    if m["logloss"] >= mb["logloss"]:
        reasons.append(f"logloss L3={m['logloss']:.4f} >= baseline={mb['logloss']:.4f} (no bate a la tasa base)")
    out["alert"] = len(reasons) > 0
    out["reasons"] = reasons
    return out


def _signature(ev):
    """Stable signature so an identical alert is not repeated day after day, but a meaningful
    change (or clearing) re-fires."""
    if not ev["alert"]:
        return "OK"
    return f"ALERT|ece={round(ev['ece'], 2)}|llbad={int(ev['logloss'] >= ev['base_logloss'])}"


def _load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_state(state):
    try:
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def send_alert(title, body):
    """Reuse the shared Telegram dispatcher (TELEGRAM_* from env; fail-soft; no secrets printed).
    Module-level so tests can monkeypatch it without spawning a subprocess."""
    try:
        subprocess.run(
            [sys.executable, str(DISPATCHER), "--title", title,
             "--date", datetime.now(timezone.utc).strftime("%Y-%m-%d"), "--summary", body],
            cwd=str(ROOT), timeout=30,
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[calib-monitor] alerta no fatal: {type(exc).__name__}")


def _report(ev, status, sent):
    lines = [
        "WORLD CUP — MONITOR DE CALIBRACIÓN L3 (1X2 producción)  [solo monitor + alerta; NO toca el modelo]",
        f"generated_at_utc: {_now_iso()}",
        f"UMBRALES (a priori): N>={N_MIN} · ECE>{ECE_MAX:.2f} -> alerta · logloss_L3 >= logloss_base -> alerta",
        f"ESTADO: {status}",
    ]
    if ev["sufficient"]:
        lines.append(f"N={ev['n']} | ECE={ev['ece']:.3f} | logloss_L3={ev['logloss']:.4f} | "
                     f"brier_L3={ev['brier']:.4f}")
        lines.append(f"baseline (tasa base): logloss={ev['base_logloss']:.4f} | brier={ev['base_brier']:.4f}")
        if ev["reasons"]:
            lines.append("motivo(s): " + " · ".join(ev["reasons"]))
        lines.append(f"alerta Telegram enviada: {'sí' if sent else 'no (sin cambio / OK / anti-spam)'}")
    else:
        lines.append(f"N={ev['n']} (<{N_MIN}) -> MUESTRA INSUFICIENTE: no se evalúa ni se alerta.")
    return "\n".join(lines)


def cmd_run(now=None):
    """Read the settled log, evaluate live L3 calibration, write the report, and (anti-spam) send a
    single Telegram alert if out of threshold. Returns the eval dict + whether an alert was sent."""
    try:
        log = L._read_log() if LOG == L.LOG else (pd.read_csv(LOG) if LOG.exists() else pd.DataFrame())
    except Exception:
        log = pd.DataFrame()
    # ensure the columns _read_log guarantees are present even when reading a foreign path
    for c in ("settled", "result_1x2", "l3_home", "l3_draw", "l3_away"):
        if c not in log.columns:
            log[c] = np.nan
    ev = evaluate(log)

    if not ev["sufficient"]:
        status = "MUESTRA INSUFICIENTE"
    elif ev["alert"]:
        status = "ALERTA"
    else:
        status = "OK"

    sent = False
    state = _load_state()
    sig = _signature(ev)
    if ev["alert"] and sig != state.get("last_signature"):
        body = (f"⚠️ Calibración L3 fuera de umbral: ECE={ev['ece']:.2f}, "
                f"logloss={ev['logloss']:.4f} vs baseline={ev['base_logloss']:.4f} (N={ev['n']}). "
                f"El auto-refit puede estar degradando la calibración del 1X2; revisar. "
                f"[{' · '.join(ev['reasons'])}]")
        send_alert("⚠️ Monitor calibración L3 (Mundial)", body)
        sent = True
    # update state on EVERY sufficient run (so 'OK' clears the signature -> re-fires if it returns)
    if ev["sufficient"]:
        _save_state({"last_signature": sig, "last_run_utc": _now_iso(),
                     "last_status": status, "last_alert_sent": bool(sent)})

    REPORT.write_text(_report(ev, status, sent), encoding="utf-8")
    print(f"calibration_monitor: status={status} N={ev['n']} "
          f"ece={'n/a' if ev['ece'] is None else round(ev['ece'], 3)} "
          f"alert_sent={sent} -> {REPORT.name}")
    return {"ev": ev, "status": status, "sent": sent}


if __name__ == "__main__":
    cmd_run()
