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
import os
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

# 🛡️ TOPE DE SEGURIDAD del total de goles dependiente del partido (auditoría read-only, fix defensivo).
# El total matchup = tb0+tb1·|sup|+tb2·sup² crece con el cuadrado del desnivel; extrapolado a un |sup|
# extremo (>3.5, INALCANZABLE en el campo del Mundial: máx real ~2.24 -> total ~3.93) daría totales
# irreales (>6) y xG >7. TOTAL_CAP capa el total para eliminar esa cola. NUNCA muerde en datos reales
# (máx WC 3.93 < 5.5; máx burn-in < 5.5) -> NO cambia ninguna predicción ni la calibración committeada.
# Constante nombrada por si se quiere ajustar; es la ÚNICA fuente de verdad (national_elo_layer3 la reutiliza).
TOTAL_CAP = 5.5

# 🔴 FLAG DE REVERSA del TOTAL DE GOLES dependiente del partido (auditoría candidato #1, forma b:
# total = tb0 + tb1·|sup| + tb2·sup²). True (default) -> total dependiente del partido (mejora OU/BTTS
# OOS sin dañar el 1X2; backtest total_goals_backtest). False -> total CONSTANTE total_mean (= modelo
# viejo EXACTO: usa total_mean + la isotónica iso_const). Reversa INSTANTÁNEA en runtime (no requiere
# re-ajustar nada: el JSON lleva total_mean, total_coef e iso/iso_const). Override por entorno
# L3_TOTAL_MATCHUP=0 para apagar sin tocar código.
TOTAL_MATCHUP_LIVE = os.environ.get("L3_TOTAL_MATCHUP", "1") != "0"


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


def total_goals(sup, total_mean, total_coef, matchup):
    """The match TOTAL fed to the xG split. matchup + total_coef present -> match-dependent
    total = tb0 + tb1·|sup| + tb2·sup² (forma b); else the CONSTANT total_mean (old behaviour)."""
    if matchup and total_coef is not None:
        tb0, tb1, tb2 = (float(total_coef[0]), float(total_coef[1]), float(total_coef[2]))
        return min(tb0 + tb1 * abs(sup) + tb2 * sup * sup, TOTAL_CAP)   # 🛡️ tope de seguridad
    return total_mean


def raw_xg(sup, a0, a1, total_mean, total_coef=None, matchup=None):
    """Map rating supremacy -> (lambda_home, lambda_away). WC = neutral, no HFA. The DIFFERENCE
    s=a0+a1·sup is unchanged; only the TOTAL level depends on the match when matchup is on
    (total_coef present). matchup defaults to the live flag; pass matchup=False to force the old
    constant-total behaviour (used for the A/B and the flag-off reversal)."""
    if matchup is None:
        matchup = TOTAL_MATCHUP_LIVE
    s = a0 + a1 * sup
    total = total_goals(sup, total_mean, total_coef, matchup)
    lh = max(0.05, (total + s) / 2.0)
    la = max(0.05, (total - s) / 2.0)
    return lh, la


def _reconstruct_iso(raw, cal):
    """Monotone lookup raw_prob -> shipped calibrated_prob for the 3 outcomes."""
    iso = []
    for k in range(3):
        order = np.argsort(raw[:, k], kind="mergesort")
        rx, cy = raw[order, k], cal[order, k]
        ux, uf, i = [], [], 0
        while i < len(rx):
            j = i
            while j + 1 < len(rx) and rx[j + 1] == rx[i]:
                j += 1
            ux.append(float(rx[i])); uf.append(float(np.mean(cy[i:j + 1]))); i = j + 1
        iso.append({"ux": ux, "uf": uf})
    return iso


# ----- calibration (build once locally, then commit the JSON) -----
def build_calibration() -> dict:
    """Derive {a0, a1, total_mean, total_coef, iso, iso_const} from ratings + shipped predictions.

    The shipped predictions store, per fixture, the rating supremacy (our_elo_*), the calibrated xG
    (our_xg_*) and the calibrated 1X2 (our_*). That recovers the pre-isotonic map (a0,a1), the
    match-dependent total coefficients (tb0,tb1,tb2; forma b) by least squares, and the (matchup)
    isotonic curve as the monotone lookup it produced. The CONSTANT total_mean and the const-total
    isotonic (iso_const) — needed for the flag-off reversal — CANNOT be derived from the (matchup)
    predictions; they are PRESERVED from the authoritative JSON written by national_elo_layer3.main()
    (run it first). No refit on raw results here, no API.
    """
    if not PREDS.exists():
        raise SystemExit(f"missing {PREDS} - needed to derive calibration")
    prev = json.loads(CALIB.read_text(encoding="utf-8")) if CALIB.exists() else {}
    df = pd.read_csv(PREDS)
    need = ["our_elo_home", "our_elo_away", "our_xg_home", "our_xg_away",
            "our_home", "our_draw", "our_away"]
    df = df.dropna(subset=need).copy()
    sup = (df["our_elo_home"] - df["our_elo_away"]).to_numpy(float)
    s = (df["our_xg_home"] - df["our_xg_away"]).to_numpy(float)
    total = (df["our_xg_home"] + df["our_xg_away"]).to_numpy(float)
    a0, a1 = [float(c) for c in np.linalg.lstsq(np.c_[np.ones(len(sup)), sup], s, rcond=None)[0]]
    # match-dependent total (forma b): PRESERVE the authoritative coefficients from the JSON written by
    # national_elo_layer3.main()/build_l3_total_calibration (fit on burn-in REAL totals). Re-deriving
    # from the shipped predictions would NEUTER the matchup if the cache predates the adoption (its
    # totals are ~constant). Only re-derive if absent (legacy JSON).
    total_coef = prev.get("total_coef")
    if total_coef is None:
        total_coef = [float(c) for c in
                      np.linalg.lstsq(np.c_[np.ones(len(sup)), np.abs(sup), sup ** 2], total, rcond=None)[0]]
    else:
        total_coef = [float(c) for c in total_coef]
    # CONSTANT total_mean: preserved from the authoritative JSON (burn-in mean); fallback = mean(total)
    total_mean = float(prev.get("total_mean", np.mean(total)))

    # reconstruct the MATCHUP isotonic using the SAME total the predictions used (the live total)
    cal = df[["our_home", "our_draw", "our_away"]].to_numpy(float)
    raw = np.zeros_like(cal)
    for i in range(len(df)):
        lh, la = raw_xg(sup[i], a0, a1, total_mean, total_coef, matchup=TOTAL_MATCHUP_LIVE)
        raw[i] = wdl(lh, la)
    iso = _reconstruct_iso(raw, cal)
    iso_const = prev.get("iso_const", iso)   # preserved (const-total isotonic for flag-off)

    calib = {
        "a0": a0, "a1": a1, "total_mean": total_mean, "total_coef": total_coef,
        "iso": iso, "iso_const": iso_const,
        "total_matchup": bool(TOTAL_MATCHUP_LIVE),
        "_note": "L3 calibration derived offline from ratings + shipped preds; total_mean/iso_const "
                 "preserved from the national_elo_layer3.main() JSON (flag-off reversal). No API.",
        "_source_fixtures": int(len(df)),
    }
    if not prev:
        print("  WARN: no prior JSON -> total_mean=mean(total) and iso_const=iso (degraded reversal); "
              "run national_elo_layer3.main() first for an exact const calibration.")
    return calib


class Predictor:
    def __init__(self, ratings: dict, calib: dict):
        self.strength = ratings  # name -> float
        self.a0 = calib["a0"]
        self.a1 = calib["a1"]
        self.total_mean = calib["total_mean"]
        self.total_coef = calib.get("total_coef")          # [tb0,tb1,tb2] (forma b) or None
        self.iso = calib["iso"]                              # MATCHUP isotonic (live primary)
        self.iso_const = calib.get("iso_const", calib["iso"])  # CONST-total isotonic (flag-off / A/B)

    def _predict_with(self, sup, matchup):
        """1X2 + xG for a given supremacy and total mode (matchup True -> match-dependent total
        + iso; False -> constant total_mean + iso_const)."""
        lh, la = raw_xg(sup, self.a0, self.a1, self.total_mean, self.total_coef, matchup)
        raw = wdl(lh, la)
        iso = self.iso if matchup else self.iso_const
        cal = np.array([np.interp(raw[k], iso[k]["ux"], iso[k]["uf"]) for k in range(3)])
        cal = np.clip(cal, 1e-6, None)
        cal = cal / cal.sum()
        return cal, lh, la

    def predict(self, home: str, away: str):
        """L3 fields (live total per TOTAL_MATCHUP_LIVE), or None if either team has no rating.
        Always attaches the CONSTANT-total variant in *_const fields for the live A/B panel."""
        sh = self.strength.get(home)
        sa = self.strength.get(away)
        if sh is None or sa is None:
            return None
        sup = sh - sa
        cal, lh, la = self._predict_with(sup, TOTAL_MATCHUP_LIVE)        # live (matchup unless reverted)
        calc, lhc, lac = self._predict_with(sup, False)                  # constant-total (A/B reference)
        return {
            "our_elo_home": round(float(sh), 2), "our_elo_away": round(float(sa), 2),
            "our_home": round(float(cal[0]), 4), "our_draw": round(float(cal[1]), 4),
            "our_away": round(float(cal[2]), 4),
            "our_xg_home": round(float(lh), 2), "our_xg_away": round(float(la), 2),
            # A/B reference: same model with the OLD constant total (never shown; for the scorecard)
            "our_home_const": round(float(calc[0]), 4), "our_draw_const": round(float(calc[1]), 4),
            "our_away_const": round(float(calc[2]), 4),
            "our_xg_home_const": round(float(lhc), 2), "our_xg_away_const": round(float(lac), 2),
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
