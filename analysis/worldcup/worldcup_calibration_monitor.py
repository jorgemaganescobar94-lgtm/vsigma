"""
WORLD CUP — L3 1X2 CALIBRATION MONITOR.  Safety net for the auto-learning loop.

Monitor + alert ONLY. It does NOT touch the model, ratings, calibration, lock-at-KO, briefing or
props. It just READS the settled predictions log, measures the LIVE calibration of the PRODUCTION
1X2 (the same l3_* columns the scorecard grades), and fires ONE Telegram alert if it drifts.

WHY: the isotonic calibration is FROZEN (burn-in <2024); the auto-refit changes the RATINGS, not the
calibration. Risk: learned ratings drift away from the frozen calibrated mapping and the 1X2 quietly
loses calibration. This monitor catches that and warns — it never "fixes" anything automatically.

THRESHOLDS (defined a priori, honest + NOISE-ADAPTIVE so small samples don't false-alarm):
  * Needs N>=15 settled predictions. Below that even the null simulation is unstable -> NO alert
    ("muestra insuficiente").
  * ECE alarm is ADAPTIVE TO SAMPLE NOISE: simulate the NULL ECE distribution at the CURRENT N
    (for each settled row draw the outcome FROM its own L3 probs => perfectly calibrated by
    construction, recompute ECE with the SAME max-confidence definition, repeat N_SIM times with a
    FIXED seed), take the p95 (NULL_PCTL). ALERT only if observed ECE > null p95 — i.e. worse than
    sampling noise alone would explain. (At N=25 a perfectly-calibrated model already expects
    ECE~0.17, so the old fixed 0.12 false-alarmed; this fixes it.)
  * Independent alarm, always valid: logloss(L3) >= logloss(base-rate) (model not beating the naive
    base rate = it is failing). NOT noise-gated.
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

N_MIN = 15         # minimum settled predictions; below this the null ECE simulation is too unstable
NULL_PCTL = 95     # alert only if observed ECE exceeds this percentile of the noise-null ECE
N_SIM = 5000       # null-distribution simulations
SEED = 20260101    # FIXED RNG seed -> the adaptive threshold is reproducible run-to-run (no flicker)


def _now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ece(P, y):
    """ECE on the max-confidence reliability — the SAME definition the monitor/scorecard use
    (worldcup_learning_loop._metrics). P row-normalised; y = int labels {0,1,2}. Used for both the
    observed value and the null simulation so the comparison is apples-to-apples."""
    conf = P.max(1)
    correct = (P.argmax(1) == y).astype(float)
    edges = np.linspace(0, 1, 11)
    n = len(P)
    e = 0.0
    for i in range(10):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.sum() / n * abs(conf[m].mean() - correct[m].mean())
    return float(e)


def null_ece_pctl(P, pctl=NULL_PCTL, n_sim=N_SIM, seed=SEED):
    """Null ECE distribution at the CURRENT N: draw outcomes FROM each row's own probs (=> perfectly
    calibrated by construction) and recompute ECE n_sim times; return the `pctl` percentile. SEEDED
    -> stable run-to-run. The per-bin confidence means and bin memberships are FIXED across sims
    (only the outcomes change), so this is cheap."""
    n = len(P)
    conf = P.max(1)
    pred = P.argmax(1)
    edges = np.linspace(0, 1, 11)
    masks = [(conf > edges[i]) & (conf <= edges[i + 1]) for i in range(10)]
    cnt = np.array([int(m.sum()) for m in masks])
    conf_mean = np.array([conf[m].mean() if cnt[i] else 0.0 for i, m in enumerate(masks)])
    cum = np.cumsum(P, axis=1)
    rng = np.random.default_rng(seed)
    sims = np.empty(n_sim)
    for s in range(n_sim):
        r = rng.random(n)
        y = (r[:, None] < cum).argmax(1)                 # categorical draw from each row's probs
        correct = (pred == y).astype(float)
        e = 0.0
        for i, m in enumerate(masks):
            if cnt[i]:
                e += cnt[i] / n * abs(conf_mean[i] - correct[m].mean())
        sims[s] = e
    return float(np.percentile(sims, pctl))


def evaluate(log):
    """Pure: live calibration of the production L3 1X2 over settled rows. Returns a dict with n,
    sufficient, metrics, baseline, alert flag + reasons. NO I/O, NO Telegram."""
    out = {"n": 0, "sufficient": False, "alert": False, "reasons": [],
           "ece": None, "logloss": None, "brier": None,
           "base_logloss": None, "base_brier": None, "null_p": None, "null_pctl": NULL_PCTL}
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
    P = P / P.sum(axis=1, keepdims=True)
    Y = np.eye(3)[y]
    m = L._metrics(P, Y)                # identical math to the scorecard (ECE on max-conf reliability)
    base = np.bincount(y, minlength=3) / n
    mb = L._metrics(np.tile(base, (n, 1)), Y)
    null_p = null_ece_pctl(P)          # noise-adaptive ECE threshold at THIS N (seeded -> stable)
    out.update(ece=m["ece"], logloss=m["logloss"], brier=m["brier"],
               base_logloss=mb["logloss"], base_brier=mb["brier"], null_p=null_p)
    reasons = []
    if m["ece"] > null_p:               # worse than sampling noise alone explains at this N
        reasons.append(f"ECE={m['ece']:.3f} > nulo p{NULL_PCTL}={null_p:.3f} (peor que el ruido a N={n})")
    if m["logloss"] >= mb["logloss"]:   # independent, always valid
        reasons.append(f"logloss L3={m['logloss']:.4f} >= baseline={mb['logloss']:.4f} (no bate a la tasa base)")
    out["alert"] = len(reasons) > 0
    out["reasons"] = reasons
    return out


def _signature(ev):
    """Stable signature so an identical alert is not repeated day after day, but a meaningful
    change (or clearing) re-fires."""
    if not ev["alert"]:
        return "OK"
    return (f"ALERT|ece_over={int(ev['ece'] > ev['null_p'])}|"
            f"llbad={int(ev['logloss'] >= ev['base_logloss'])}")


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
        f"UMBRAL ADAPTATIVO AL RUIDO (a priori): N>={N_MIN} · ALERTA si ECE_obs > nulo p{NULL_PCTL} "
        f"(sim. {N_SIM}x, seed fijo) O logloss_L3 >= logloss_base",
        f"ESTADO: {status}",
    ]
    if ev["sufficient"]:
        lines.append(f"N={ev['n']} | ECE_observado={ev['ece']:.3f} | nulo p{NULL_PCTL}(N={ev['n']})={ev['null_p']:.3f} "
                     f"-> ECE {'POR ENCIMA del ruido' if ev['ece'] > ev['null_p'] else 'dentro del ruido'}")
        lines.append(f"logloss_L3={ev['logloss']:.4f} vs baseline={ev['base_logloss']:.4f} "
                     f"-> {'NO bate' if ev['logloss'] >= ev['base_logloss'] else 'bate'} la tasa base "
                     f"| brier_L3={ev['brier']:.4f} (base {ev['base_brier']:.4f})")
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
        body = (f"⚠️ Calibración L3 fuera de umbral (adaptativo al ruido, N={ev['n']}): "
                f"ECE={ev['ece']:.3f} vs nulo p{NULL_PCTL}={ev['null_p']:.3f}; "
                f"logloss={ev['logloss']:.4f} vs baseline={ev['base_logloss']:.4f}. "
                f"Peor que el ruido de muestra; el auto-refit puede estar degradando el 1X2; revisar. "
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
