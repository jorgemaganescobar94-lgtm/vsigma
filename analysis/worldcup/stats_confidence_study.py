"""
STATS CONFIDENCE STUDY (READ-ONLY, ISOLATED). Can we raise the OOS confidence of the per-team
corners/shots model beyond the shipped one? NO market, NO production change, NO API.

Reuses the SHIPPED walk-forward harness (stats_model: data load, opp_str feature, Poisson deviance,
ridge-WLS design, constants) and the feature-study rolling helpers (feature_study_stats). It does
NOT duplicate the model — every candidate is the SAME strict walk-forward (refit on prior rows only,
time-decayed, OOS from 2024-08-01), changing ONE thing at a time:

  C0  current shipped model            att/conc + home + opp_str        (ridge-WLS on log(y+0.5))
  base   no opp_str (reference)         att/conc + home
  +own_form   add team's OWN rolling past mean of the same stat (anti-leakage, strictly pre-match)
  +own_str    add team's OWN L3 strength (symmetric to opp_str)
  +both       +own_form +own_str
  GLM    same features as C0 but fit by Poisson IRLS (real GLM) instead of WLS-on-log

Plus a LEARNING CURVE for C0 (cap the training history) to answer "would MORE data help?".

Metrics (all strictly OOS, on the COMMON row set so comparisons are paired & fair):
  * deviance-lift% vs a constant base-rate (the harness headline; comparable to worldcup_stats_validation)
  * incremental vs C0: paired bootstrap on per-row Poisson-deviance difference -> mean lift-diff %,
    95% CI and a one-sided bootstrap p-value (is the candidate SIGNIFICANTLY better than shipped?).

Run:  python analysis/worldcup/stats_confidence_study.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stats_model as SM            # noqa: E402  (data, deviance, constants — the shipped harness)
import feature_study_stats as FS    # noqa: E402  (rolling_form / past_mean — same anti-leakage helpers)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

STATS = ["corners", "shots"]        # the two KEPT stats (cards = noise, excluded as in feature study)
HL, LAM, REFIT, MIN_PAST, CUTOFF = SM.HL_DAYS, SM.LAM, SM.REFIT_DAYS, SM.MIN_PAST, SM.OOS_CUTOFF
REPORT = HERE / "stats_confidence_study_report.txt"
TABLE = HERE / "stats_confidence_study_table.csv"
RNG = np.random.default_rng(0)
NBOOT = 3000


# --------------------------------------------------------------------------- per-row deviance
def _dev_rows(y, lam):
    """Per-observation Poisson deviance contribution (sum = SM.poisson_dev)."""
    y = np.asarray(y, float)
    lam = np.clip(np.asarray(lam, float), 1e-9, None)
    t = np.zeros_like(y)
    pos = y > 0
    t[pos] = y[pos] * np.log(y[pos] / lam[pos])
    return 2.0 * (t - (y - lam))


# --------------------------------------------------------------------------- fitters
def _fit_wls(X, z, w, ridge_start, lam=LAM):
    """Ridge-weighted least squares on z=log(y+0.5) — the SHIPPED fit (att/conc regularised only)."""
    XtW = X.T * w
    A = XtW @ X
    b = XtW @ z
    R = np.zeros(X.shape[1]); R[ridge_start:] = lam
    A[np.diag_indices(A.shape[0])] += R + 1e-8
    return np.linalg.solve(A, b)


def _fit_glm(X, y, w, ridge_start, lam=LAM, iters=40):
    """Penalised Poisson GLM (log link) by IRLS with the SAME time-decay weights and att/conc ridge.
    Predicts E[y] directly (no log-bias), unlike WLS-on-log(y+0.5)."""
    P = X.shape[1]
    beta = np.zeros(P)
    beta[0] = np.log(max(float(np.average(y, weights=w)), 1e-3))
    R = np.zeros(P); R[ridge_start:] = lam
    for _ in range(iters):
        eta = np.clip(X @ beta, -10.0, 10.0)
        mu = np.exp(eta)
        Wt = w * mu
        zt = eta + (y - mu) / np.clip(mu, 1e-9, None)
        XtW = X.T * Wt
        A = XtW @ X
        A[np.diag_indices(P)] += R + 1e-8
        beta_new = np.linalg.solve(A, XtW @ zt)
        if np.max(np.abs(beta_new - beta)) < 1e-7:
            return beta_new
        beta = beta_new
    return beta


# --------------------------------------------------------------------------- walk-forward
def _prep(df, stat):
    """Stat subset + design pieces. Features standardised on the subset; NaN -> 0 (neutral), so EVERY
    candidate predicts on the SAME rows (paired comparison). own_form = team's own decayed past mean."""
    sub = df[df[stat].notna()].copy().sort_values("date").reset_index(drop=True)
    teams = sorted(set(sub["team_id"]) | set(sub["opp_id"]))
    loc = {t: i for i, t in enumerate(teams)}
    own_by = FS.rolling_form(df, stat)               # team_id -> (dates, vals) over FULL history
    sub["own_form"] = [FS.past_mean(own_by, t, d) for t, d in zip(sub["team_id"], sub["date"])]

    def z(col):
        v = sub[col].to_numpy(float)
        m, s = np.nanmean(v), np.nanstd(v) + 1e-9
        return np.nan_to_num((v - m) / s, nan=0.0)

    feats = {"opp_str": z("opp_str"), "own_str": z("own_str"), "own_form": z("own_form")}
    return {
        "sub": sub, "teams": teams,
        "team_l": sub["team_id"].map(loc).to_numpy(),
        "opp_l": sub["opp_id"].map(loc).to_numpy(),
        "home": sub["is_home"].to_numpy(float),
        "y": sub[stat].to_numpy(float),
        "days": ((sub["date"] - sub["date"].min()) / np.timedelta64(1, "D")).to_numpy(float),
        "dates": sub["date"].to_numpy(),
        "feats": feats,
    }


def _design(P, feat_names, prep):
    T = len(prep["teams"])
    n = len(prep["y"])
    nf = len(feat_names)
    X = np.zeros((n, 2 + nf + 2 * T))
    X[:, 0] = 1.0
    X[:, 1] = prep["home"]
    for j, fn in enumerate(feat_names):
        X[:, 2 + j] = prep["feats"][fn]
    X[np.arange(n), 2 + nf + prep["team_l"]] = 1.0
    X[np.arange(n), 2 + nf + T + prep["opp_l"]] = 1.0
    return X, 2 + nf


def walk(prep, feat_names, method="wls", train_cap=None):
    """Strict OOS walk-forward (refit every REFIT days on prior rows; predict each row pre-fit).
    train_cap: if set, use only the most recent `train_cap` past rows (learning-curve probe)."""
    X, ridge_start = _design(None, feat_names, prep)
    y, z = prep["y"], np.log(prep["y"] + 0.5)
    days = prep["days"]
    n = len(y)
    lam_hat = np.full(n, np.nan)
    beta, last = None, None
    idx_all = np.arange(n)
    for i in range(n):
        if beta is None or (days[i] - last) >= REFIT:
            pm = idx_all[days < days[i]]
            if train_cap is not None and len(pm) > train_cap:
                pm = pm[-train_cap:]
            if len(pm) >= MIN_PAST:
                w = np.exp(-np.log(2) * (days[i] - days[pm]) / HL)
                beta = (_fit_wls(X[pm], z[pm], w, ridge_start) if method == "wls"
                        else _fit_glm(X[pm], y[pm], w, ridge_start))
                last = days[i]
        if beta is not None:
            lam_hat[i] = np.exp(np.clip(X[i] @ beta, -10.0, 10.0))
    oos = (prep["dates"] >= np.datetime64(CUTOFF)) & np.isfinite(lam_hat)
    return lam_hat, oos


# --------------------------------------------------------------------------- significance
def _lift_vs_base(y, lam):
    base = np.full(len(y), float(np.mean(y)))
    db, dm = SM.poisson_dev(y, base), SM.poisson_dev(y, lam)
    return 100.0 * (db - dm) / db if db > 0 else 0.0, db, dm


def _paired_boot(y, lam_c0, lam_cand, base_dev):
    """Paired bootstrap of the per-row deviance REDUCTION (C0 - candidate). Positive => candidate
    better. Returns (mean lift-diff % of base deviance, lo95, hi95, one-sided p that cand NOT better)."""
    d = _dev_rows(y, lam_c0) - _dev_rows(y, lam_cand)     # >0 where candidate has less deviance
    n = len(d)
    obs = d.sum()
    means = np.empty(NBOOT)
    for b in range(NBOOT):
        s = RNG.integers(0, n, n)
        means[b] = d[s].sum()
    lo, hi = np.percentile(means, [2.5, 97.5])
    p = float(np.mean(means <= 0.0))                       # one-sided: prob candidate is not better
    to_pct = lambda v: 100.0 * v / base_dev if base_dev > 0 else 0.0
    return to_pct(obs), to_pct(lo), to_pct(hi), p


# --------------------------------------------------------------------------- main
def main():
    df = SM._load_raw()
    strength = SM._l3_strength_by_name()
    df["own_str"] = df["team"].map(strength)              # symmetric to the shipped opp_str

    rep = []

    def out(s=""):
        print(s); rep.append(s)

    out("=" * 100)
    out("STATS CONFIDENCE STUDY — corners / shots  (READ-ONLY, reuses stats_model walk-forward)")
    out("=" * 100)
    out(f"rows={len(df)} fixtures={df['fixture_id'].nunique()} teams={df['team_id'].nunique()} | "
        f"HL={HL:.0f}d ridge={LAM} refit={REFIT}d OOS>={CUTOFF} | boot={NBOOT}")
    out("Training base is ALREADY broad internationals (Friendlies/UNL/WCQ/AFCON/Euro/CopaAmérica/…),")
    out("NOT World-Cup-only. international_results.csv has 9197 fixtures but NO corners/shots -> the")
    out("binding limit is STAT coverage, not match coverage (more would need API extraction).")
    out("")

    CANDS = [
        ("base (no opp_str)", ["__none__"], "wls"),
        ("C0 shipped (+opp_str)", ["opp_str"], "wls"),
        ("+own_form", ["opp_str", "own_form"], "wls"),
        ("+own_str", ["opp_str", "own_str"], "wls"),
        ("+own_form+own_str", ["opp_str", "own_form", "own_str"], "wls"),
        ("GLM Poisson (C0 feats)", ["opp_str"], "glm"),
    ]
    table = []
    for stat in STATS:
        prep = _prep(df, stat)
        # predictions per candidate (feat list "__none__" -> baseline with no extra regressors)
        preds = {}
        for label, feats, method in CANDS:
            fn = [] if feats == ["__none__"] else feats
            preds[label] = walk(prep, fn, method=method)
        # common OOS rows across ALL candidates (paired & fair)
        common = np.ones(len(prep["y"]), bool)
        for label, _, _ in CANDS:
            common &= preds[label][1]
        y = prep["y"][common]
        c0 = preds["C0 shipped (+opp_str)"][0][common]
        _, base_dev, _ = _lift_vs_base(y, np.full(len(y), float(np.mean(y))))

        out(f"--- {stat.upper()}  (n_oos common = {int(common.sum())}, base mean = {y.mean():.2f}) ---")
        out(f"  {'candidate':26} {'devLift%':>9} {'RMSE':>7} {'vsC0 dLift%':>12} {'95% CI':>16} {'p(better)':>10} {'signif':>7}")
        for label, _, _ in CANDS:
            lam = preds[label][0][common]
            lift, _, _ = _lift_vs_base(y, lam)
            rmse = float(np.sqrt(np.mean((y - lam) ** 2)))
            if label == "C0 shipped (+opp_str)":
                row = f"  {label:26} {lift:>8.2f}% {rmse:>7.3f} {'(reference)':>12} {'':>16} {'':>10} {'':>7}"
                sig = "ref"
                d_obs = d_lo = d_hi = 0.0; pval = np.nan
            else:
                d_obs, d_lo, d_hi, pval = _paired_boot(y, c0, lam, base_dev)
                sig = "YES" if (d_lo > 0 and pval < 0.05) else ("WORSE" if d_hi < 0 else "no")
                row = (f"  {label:26} {lift:>8.2f}% {rmse:>7.3f} {d_obs:>+11.2f}% "
                       f"[{d_lo:>+5.2f},{d_hi:>+5.2f}] {pval:>10.3f} {sig:>7}")
            out(row)
            table.append({"stat": stat, "candidate": label, "n_oos": int(common.sum()),
                          "dev_lift_pct": round(lift, 2), "rmse": round(rmse, 3),
                          "vs_c0_dlift_pct": round(d_obs, 2), "ci_lo": round(d_lo, 2),
                          "ci_hi": round(d_hi, 2), "p_better": (None if label.startswith("C0") else round(pval, 3)),
                          "signif": sig})
        out("")

        # ---- learning curve for C0: would MORE data help? ----
        out(f"  learning curve {stat} (C0 feats, cap training history): devLift% by train_cap")
        lc = []
        for cap in (300, 600, 900, 1200, None):
            lam_hat, oos = walk(prep, ["opp_str"], method="wls", train_cap=cap)
            m = oos & common  # score on the same common OOS rows
            lift, _, _ = _lift_vs_base(prep["y"][m], lam_hat[m])
            lc.append((("all" if cap is None else str(cap)), lift, int(m.sum())))
            table.append({"stat": stat, "candidate": f"lcurve_cap_{cap or 'all'}",
                          "n_oos": int(m.sum()), "dev_lift_pct": round(lift, 2)})
        out("    " + " | ".join(f"cap={c}:{l:+.2f}%" for c, l, _ in lc))
        out("")

    out("=" * 100)
    out("READING: devLift% = OOS Poisson-deviance reduction vs a constant base-rate (same metric as")
    out("worldcup_stats_validation.csv). 'vsC0 dLift%' = paired bootstrap deviance reduction of the")
    out("candidate OVER the shipped C0 model, as % of base deviance; signif=YES needs 95% CI>0 AND")
    out("p<0.05. The +opp_str gain over base is the ~4%/~8% the ficha currently relies on.")
    pd.DataFrame(table).to_csv(TABLE, index=False)
    REPORT.write_text("\n".join(rep), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {TABLE}")


if __name__ == "__main__":
    main()
