"""
OFFLINE STUDY (ISOLATED, analysis/worldcup/) — does the recent xG FORM of each team add
1X2 signal on top of the L3 supremacy? NO API, NO production change, NO ficha change.

Pre-registered success criterion (fixed BEFORE seeing results):
  ADOPT only if OOS 1X2 log-loss improves by >= 0.005 AND ECE does not get worse.
  Otherwise: discard, keep L3 as is.

Coverage gate (also pre-registered): a walk-forward is only CONCLUSIVE for detecting a
0.005 log-loss effect if there are >= 500 OOS matches with a usable xG-form feature
(>= 3 prior xG matches for BOTH teams). Below that, the result is INDICATIVE only.

Inputs (committed, tiny):
  national_elo_layer3_permatch.csv  leak-free walk-forward L3 supremacy (sup_pre_l3) per match
  worldcup_xg_raw.csv               per team-match real xG (fixture_id, team_id, opp_id, xg)
  international_results.csv          dates / ids (to attach a date to each xG row)

Feature (as-of, no leakage): for each team in a match, recent net xG form =
  mean over its last N=5 PRIOR matches (date < match) of (xg_for - xg_against).
xgform_sup = home_form - away_form. Teams with < K prior xG matches are EXCLUDED (no invent).

Model comparison on the SAME match set, walk-forward inside the xG era (leak-free):
  A) L3 pure   : margin_hat = a0 + a1*sup
  B) L3 + xGform: margin_hat = a0 + a1*sup + a2*xgform_sup
Both map margin -> (lh,la) -> independent-Poisson 1X2 with the prior set's total_mean.
Isotonic is omitted on purpose: it is an identical post-process for both, so it cannot
change the A-vs-B comparison; the question is whether the feature adds linear signal.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OUT_DIR = Path(__file__).resolve().parent
PERMATCH = OUT_DIR / "national_elo_layer3_permatch.csv"
XG = OUT_DIR / "worldcup_xg_raw.csv"
IR = OUT_DIR / "international_results.csv"
REPORT = OUT_DIR / "xg_form_study_report.txt"
PERMATCH_OUT = OUT_DIR / "xg_form_study_permatch.csv"

KMAX = 12
EPS = 1e-15
N_FORM = 5            # rolling window for xG form (last N prior matches)
K_MIN = 3            # min prior xG matches per team to keep a match (no-invent fallback)
OOS_CUTOFF = "2024-01-01"
COVERAGE_THRESHOLD = 500   # pre-registered: matches needed for a CONCLUSIVE 0.005 test
MIN_FIT = 60         # min prior xG-era matches before we start predicting (walk-forward)
ADOPT_LL = 0.005     # pre-registered log-loss improvement bar


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def wdl(lh, la):
    M = np.outer(pmf(lh), pmf(la)); M /= M.sum()
    gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
    return np.array([M[gh > ga].sum(), M[gh == ga].sum(), M[gh < ga].sum()])


def margin_to_probs(margin, total_mean):
    lh = max(0.05, (total_mean + margin) / 2.0)
    la = max(0.05, (total_mean - margin) / 2.0)
    p = wdl(lh, la); p = np.clip(p, EPS, None); return p / p.sum()


def logloss(P, Y):
    return float(-np.mean(np.sum(Y * np.log(np.clip(P, EPS, 1.0)), axis=1)))


def brier(P, Y):
    return float(np.mean(np.sum((P - Y) ** 2, axis=1)))


def acc(P, Y):
    return float(np.mean(P.argmax(1) == Y.argmax(1)))


def ece(P, Y, bins=10):
    conf = P.max(1); corr = (P.argmax(1) == Y.argmax(1)).astype(float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(P) * abs(conf[m].mean() - corr[m].mean())
    return float(e)


def build_xg_form():
    """Return DataFrame of matches with xgform_sup attached (as-of, leak-free), plus a date,
    sup_pre_l3, res. Only matches where BOTH teams have >= K_MIN prior xG matches."""
    ir = pd.read_csv(IR)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce")
    date_by_fid = dict(zip(ir["fixture_id"].astype(int), ir["date"]))

    xg = pd.read_csv(XG)
    xg = xg[xg["xg"].notna()].copy()
    xg["date"] = xg["fixture_id"].astype(int).map(date_by_fid)
    xg = xg.dropna(subset=["date"])
    # net xg per (fixture, team) = xg_for - xg_against (opp's xg in the same fixture)
    xg_by = {(int(r.fixture_id), int(r.team_id)): float(r.xg) for r in xg.itertuples()}
    net_rows = []
    for r in xg.itertuples():
        opp_xg = xg_by.get((int(r.fixture_id), int(r.opp_id)))
        if opp_xg is None:
            continue
        net_rows.append({"team_id": int(r.team_id), "date": r.date,
                         "net_xg": float(r.xg) - opp_xg})
    nx = pd.DataFrame(net_rows).sort_values("date")
    hist = {}
    for r in nx.itertuples():
        hist.setdefault(int(r.team_id), []).append((r.date, r.net_xg))

    def form_asof(tid, d):
        prior = [v for (dt, v) in hist.get(int(tid), []) if dt < d]
        if len(prior) < K_MIN:
            return None
        return float(np.mean(prior[-N_FORM:]))

    pm = pd.read_csv(PERMATCH)
    pm["date"] = pd.to_datetime(pm["date"], utc=True, errors="coerce")
    pm = pm.dropna(subset=["date", "sup_pre_l3"])
    rows = []
    for r in pm.itertuples():
        fh = form_asof(int(r.home_id), r.date)
        fa = form_asof(int(r.away_id), r.date)
        if fh is None or fa is None:
            continue
        rows.append({"fixture_id": int(r.fixture_id), "date": r.date,
                     "sup_pre_l3": float(r.sup_pre_l3), "res": int(r.res),
                     "gh": float(r.gh), "ga": float(r.ga),
                     "xgform_sup": fh - fa})
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def walkforward(df, use_xg):
    """Leak-free: for each match i, fit the margin model on prior matches, predict i.
    Returns (P, Y, mask_predicted)."""
    n = len(df)
    sup = df["sup_pre_l3"].to_numpy(float)
    xgf = df["xgform_sup"].to_numpy(float)
    margin = (df["gh"] - df["ga"]).to_numpy(float)
    total = (df["gh"] + df["ga"]).to_numpy(float)
    res = df["res"].to_numpy(int)
    P = np.full((n, 3), np.nan)
    for i in range(n):
        if i < MIN_FIT:
            continue
        if use_xg:
            A = np.c_[np.ones(i), sup[:i], xgf[:i]]
            x = np.array([1.0, sup[i], xgf[i]])
        else:
            A = np.c_[np.ones(i), sup[:i]]
            x = np.array([1.0, sup[i]])
        coef, *_ = np.linalg.lstsq(A, margin[:i], rcond=None)
        tm = float(np.mean(total[:i]))
        P[i] = margin_to_probs(float(x @ coef), tm)
    mask = ~np.isnan(P).any(axis=1)
    Y = np.eye(3)[res]
    return P, Y, mask


def main():
    report = []

    def out(s=""):
        print(s); report.append(s)

    df = build_xg_form()
    oos = df[df["date"] >= pd.Timestamp(OOS_CUTOFF, tz="UTC")].reset_index(drop=True)

    out("=" * 92)
    out("XG-FORM STUDY — does recent xG form add 1X2 signal on top of L3 supremacy?  (OFFLINE)")
    out("=" * 92)
    out(f"feature: net xG form = mean last N={N_FORM} prior matches of (xg_for - xg_against); "
        f"K_MIN={K_MIN} prior per team (else excluded)")
    out(f"usable matches with xgform_sup (both teams >= {K_MIN} prior): {len(df)}  | "
        f"in OOS window (>= {OOS_CUTOFF}): {len(oos)}")
    out("")

    # ---- coverage gate (pre-registered) ----
    out("-" * 92)
    out("COVERAGE GATE (pre-registered)")
    out("-" * 92)
    out(f"  threshold for a CONCLUSIVE 0.005 log-loss test: >= {COVERAGE_THRESHOLD} usable OOS matches")
    out(f"  actual usable OOS matches: {len(oos)}")
    conclusive = len(oos) >= COVERAGE_THRESHOLD
    out(f"  GATE: {'PASS -> conclusive' if conclusive else 'FAIL -> INDICATIVE ONLY (underpowered)'}")
    out("")

    if len(oos) < MIN_FIT + 20:
        out("Too few matches even for an indicative walk-forward; stopping.")
        REPORT.write_text("\n".join(report), encoding="utf-8")
        print(f"\nWritten: {REPORT}")
        return

    # ---- indicative walk-forward A vs B on the SAME predicted set ----
    Pa, Y, ma = walkforward(oos, use_xg=False)
    Pb, _, mb = walkforward(oos, use_xg=True)
    m = ma & mb                                   # compare on the identical set
    Yc = Y[m]
    n = int(m.sum())
    base = np.bincount(oos["res"].to_numpy(int)[m], minlength=3) / max(n, 1)
    Pbase = np.tile(base, (n, 1))

    rows = [("base-rate", Pbase), ("L3 (sup only)", Pa[m]), ("L3 + xG-form", Pb[m])]
    out("-" * 92)
    out(f"WALK-FORWARD OOS  (compared on the SAME {n} matches; isotonic omitted — identical for A/B)")
    out("-" * 92)
    out(f"  {'model':18} {'n':>5} {'logloss':>9} {'brier':>8} {'acc%':>7} {'ECE':>7}")
    res = {}
    for name, P in rows:
        ll, br, ac, ec = logloss(P, Yc), brier(P, Yc), acc(P, Yc) * 100, ece(P, Yc)
        res[name] = (ll, br, ac, ec)
        out(f"  {name:18} {n:>5} {ll:>9.4f} {br:>8.4f} {ac:>7.1f} {ec:>7.4f}")
    out("")

    ll_a, _, _, ec_a = res["L3 (sup only)"]
    ll_b, _, _, ec_b = res["L3 + xG-form"]
    d_ll = ll_a - ll_b           # positive = xG-form improves (lower log-loss)
    d_ece = ec_b - ec_a          # positive = xG-form WORSENS calibration
    out("-" * 92)
    out("VERDICT vs pre-registered criterion (adopt iff Δlogloss >= +0.005 AND ECE not worse)")
    out("-" * 92)
    out(f"  Δlog-loss (L3 - L3+xG) = {d_ll:+.4f}  (need >= +{ADOPT_LL:.3f})")
    out(f"  ECE change (xG - L3)   = {d_ece:+.4f}  (need <= 0)")
    meets = (d_ll >= ADOPT_LL) and (d_ece <= 0)
    if not conclusive:
        out(f"  COVERAGE GATE FAILED ({len(oos)} < {COVERAGE_THRESHOLD}) -> result is INDICATIVE, not conclusive.")
        out(f"  DECISION: DO NOT ADOPT (default to keeping L3; test underpowered for a {ADOPT_LL} effect).")
    else:
        out(f"  DECISION: {'ADOPT' if meets else 'DO NOT ADOPT'} (criterion {'met' if meets else 'not met'}).")
    out("")
    out(f"  raw direction (indicative): xG-form {'helps' if d_ll > 0 else 'hurts/neutral'} "
        f"log-loss by {d_ll:+.4f}; ECE {'worse' if d_ece > 0 else 'same/better'} ({d_ece:+.4f}).")

    oos.assign(P_l3_H=Pa[:, 0], P_xg_H=Pb[:, 0]).to_csv(PERMATCH_OUT, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {REPORT}")
    print(f"Written: {PERMATCH_OUT}")


if __name__ == "__main__":
    main()
