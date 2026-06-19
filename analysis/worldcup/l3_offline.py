"""
WORLD CUP 2026 - LAYER-3 predictor, OFFLINE & NO API (ISOLATED, analysis/worldcup/).

Goal: reproduce the shipped Layer-3 1X2/xG forecast for ANY fixture (incl. new
knockout fixtures that appear as teams advance) using ONLY tiny committed files:
  * national_elo_layer3_ratings.csv        team -> strength (goals vs avg)
  * national_elo_layer3_calibration.json   {a0, a1, total_mean, isotonic curves}

It does NOT refit from international_results.csv (862 KB, not committed) and makes
NO API call. The calibration JSON is BUILT ONCE locally from the already-shipped
ratings + worldcup_our_model_predictions.csv, so the predictor reproduces those
committed values EXACTLY and extends (by isotonic interpolation) to new matchups.

Two roles:
  --build-calibration   (LOCAL, one-off) derive calibration JSON from ratings +
                        worldcup_our_model_predictions.csv. Run when ratings change.
  --regen FIXTURES.csv  (CI-safe, offline) upsert L3 predictions for the fixtures
                        listed (columns fixture_id,home,away[,...]) into
                        worldcup_our_model_predictions.csv WITHOUT touching rows that
                        already exist (locks the pre-match prediction).

NOT production. No .env, no git, no betting logic.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
RATINGS = OUT_DIR / "national_elo_layer3_ratings.csv"
CALIB = OUT_DIR / "national_elo_layer3_calibration.json"
PREDS = OUT_DIR / "worldcup_our_model_predictions.csv"
KMAX = 12


# ----- Poisson helpers (identical math to national_elo_layer3.py) -----
def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def wdl(lh, la):
    """Return [P(home win), P(draw), P(away win)] from independent Poisson xG."""
    M = np.outer(pmf(lh), pmf(la))
    M /= M.sum()
    gh = np.arange(KMAX + 1)[:, None]
    ga = np.arange(KMAX + 1)[None, :]
    return np.array([M[gh > ga].sum(), M[gh == ga].sum(), M[gh < ga].sum()])


def raw_xg(sup, a0, a1, total_mean):
    """Map rating supremacy -> (lambda_home, lambda_away). WC = neutral, no HFA."""
    s = a0 + a1 * sup
    lh = max(0.05, (total_mean + s) / 2.0)
    la = max(0.05, (total_mean - s) / 2.0)
    return lh, la


# ----- calibration (build once locally, then commit the JSON) -----
def build_calibration() -> dict:
    """Derive {a0, a1, total_mean, iso[3]} from ratings + shipped predictions.

    The shipped predictions store, per fixture, the rating supremacy (our_elo_*),
    the calibrated xG (our_xg_*) and the calibrated 1X2 (our_*). That is enough to
    recover the deterministic pre-isotonic map (a0,a1,total_mean) by least squares
    and to reconstruct each isotonic curve as the monotone lookup
    (raw_prob -> calibrated_prob) it produced. No refit, no API.
    """
    if not PREDS.exists():
        raise SystemExit(f"missing {PREDS} - needed to derive calibration")
    df = pd.read_csv(PREDS)
    need = ["our_elo_home", "our_elo_away", "our_xg_home", "our_xg_away",
            "our_home", "our_draw", "our_away"]
    df = df.dropna(subset=need).copy()
    sup = (df["our_elo_home"] - df["our_elo_away"]).to_numpy(float)
    s = (df["our_xg_home"] - df["our_xg_away"]).to_numpy(float)
    total_mean = float(np.mean((df["our_xg_home"] + df["our_xg_away"]).to_numpy(float)))
    # s = a0 + a1*sup  (least squares)
    A = np.c_[np.ones(len(sup)), sup]
    coef, *_ = np.linalg.lstsq(A, s, rcond=None)
    a0, a1 = float(coef[0]), float(coef[1])

    # reconstruct the three isotonic curves: raw wdl prob -> shipped calibrated prob
    cal = df[["our_home", "our_draw", "our_away"]].to_numpy(float)
    raw = np.zeros_like(cal)
    for i in range(len(df)):
        lh, la = raw_xg(sup[i], a0, a1, total_mean)
        raw[i] = wdl(lh, la)
    iso = []
    for k in range(3):
        order = np.argsort(raw[:, k], kind="mergesort")
        rx, cy = raw[order, k], cal[order, k]
        # collapse duplicate raw values (average their calibrated targets)
        ux, uf = [], []
        i = 0
        while i < len(rx):
            j = i
            while j + 1 < len(rx) and rx[j + 1] == rx[i]:
                j += 1
            ux.append(float(rx[i]))
            uf.append(float(np.mean(cy[i:j + 1])))
            i = j + 1
        iso.append({"ux": ux, "uf": uf})

    calib = {
        "a0": a0, "a1": a1, "total_mean": total_mean, "iso": iso,
        "_note": "Layer-3 calibration derived offline from ratings + shipped preds; "
                 "no API, no refit. Rebuild with --build-calibration if ratings change.",
        "_source_fixtures": int(len(df)),
    }
    return calib


class Predictor:
    def __init__(self, ratings: dict, calib: dict):
        self.strength = ratings  # name -> float
        self.a0 = calib["a0"]
        self.a1 = calib["a1"]
        self.total_mean = calib["total_mean"]
        self.iso = calib["iso"]

    def predict(self, home: str, away: str):
        """Return dict of L3 fields, or None if either team has no rating."""
        sh = self.strength.get(home)
        sa = self.strength.get(away)
        if sh is None or sa is None:
            return None
        sup = sh - sa
        lh, la = raw_xg(sup, self.a0, self.a1, self.total_mean)
        raw = wdl(lh, la)
        cal = np.array([np.interp(raw[k], self.iso[k]["ux"], self.iso[k]["uf"])
                        for k in range(3)])
        cal = np.clip(cal, 1e-6, None)
        cal = cal / cal.sum()
        return {
            "our_elo_home": round(float(sh), 2), "our_elo_away": round(float(sa), 2),
            "our_home": round(float(cal[0]), 4), "our_draw": round(float(cal[1]), 4),
            "our_away": round(float(cal[2]), 4),
            "our_xg_home": round(float(lh), 2), "our_xg_away": round(float(la), 2),
        }


def load_predictor():
    """Load the offline predictor from committed files, or None if unavailable."""
    if not (RATINGS.exists() and CALIB.exists()):
        return None
    rt = pd.read_csv(RATINGS)
    strength = {str(r["team"]): float(r["strength"]) for _, r in rt.iterrows()}
    calib = json.loads(CALIB.read_text(encoding="utf-8"))
    return Predictor(strength, calib)


# ----- CLI roles -----
def cmd_build_calibration():
    calib = build_calibration()
    CALIB.write_text(json.dumps(calib, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written: {CALIB}")
    print(f"  a0={calib['a0']:+.4f} a1={calib['a1']:.4f} total_mean={calib['total_mean']:.4f} "
          f"(from {calib['_source_fixtures']} fixtures)")
    # self-check: reproduce shipped predictions
    pred = load_predictor()
    df = pd.read_csv(PREDS)
    err = 0.0
    n = 0
    for _, r in df.iterrows():
        p = pred.predict(str(r["home"]), str(r["away"]))
        if p:
            err = max(err, abs(p["our_home"] - float(r["our_home"])),
                      abs(p["our_away"] - float(r["our_away"])))
            n += 1
    print(f"  self-check vs shipped preds: max |Δprob| = {err:.4f} over {n} fixtures "
          f"({'OK' if err < 0.01 else 'WARN: drift'})")


def cmd_regen(fixtures_csv: str):
    """Upsert L3 predictions for fixtures in fixtures_csv (offline). Locks existing rows."""
    pred = load_predictor()
    if pred is None:
        print("l3_offline: no ratings/calibration committed; nothing to regen.")
        return
    fx = pd.read_csv(fixtures_csv)
    fx = fx.dropna(subset=["fixture_id", "home", "away"])
    existing = {}
    cols = ["fixture_id", "home", "away", "our_elo_home", "our_elo_away",
            "our_home", "our_draw", "our_away", "our_xg_home", "our_xg_away"]
    if PREDS.exists():
        cur = pd.read_csv(PREDS)
        for _, r in cur.iterrows():
            existing[int(r["fixture_id"])] = r.to_dict()
    added = []
    for _, r in fx.iterrows():
        fid = int(r["fixture_id"])
        if fid in existing:
            continue  # never overwrite a locked pre-match prediction
        p = pred.predict(str(r["home"]), str(r["away"]))
        if not p:
            continue
        row = {"fixture_id": fid, "home": r["home"], "away": r["away"], **p}
        existing[fid] = row
        added.append(f"{r['home']} vs {r['away']}")
    if not existing:
        print("l3_offline: no predictions to write.")
        return
    out = pd.DataFrame([existing[k] for k in existing])
    # keep a stable column order (extra columns from the old file preserved at the end)
    ordered = [c for c in cols if c in out.columns] + [c for c in out.columns if c not in cols]
    out[ordered].to_csv(PREDS, index=False)
    print(f"l3_offline: regen complete -> {PREDS} ({len(out)} rows, {len(added)} new)")
    for a in added:
        print(f"   + L3 (from ratings): {a}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Offline Layer-3 World Cup predictor (no API).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--build-calibration", action="store_true",
                   help="LOCAL: derive calibration JSON from ratings + shipped preds")
    g.add_argument("--regen", metavar="FIXTURES_CSV",
                   help="offline: upsert L3 preds for fixtures (fixture_id,home,away)")
    a = ap.parse_args()
    if a.build_calibration:
        cmd_build_calibration()
    else:
        cmd_regen(a.regen)
