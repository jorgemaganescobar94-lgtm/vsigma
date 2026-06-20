"""
FEATURE STUDY A - goals / 1X2 (ISOLATED, analysis/worldcup/). NO market/odds.

Question: beyond the L3 rating supremacy (sup_pre_l3, already walk-forward OOS-safe),
does any extra REAL-DATA feature add OOS signal for goals & 1X2?

Baseline model (per match, L3 parameterisation):
    s = supremacy regression on [1, sup_pre_l3]          -> E[gh-ga]
    T = total constant (mean gh+ga)                       -> E[gh+ga]
    lam_h=(T+s)/2, lam_a=(T-s)/2  -> independent Poisson  -> 1X2 + O2.5 (RAW, no isotonic)
Each candidate feature is added to the supremacy regression (and total where it makes
sense), refit, and scored. We compare the SAME raw-Poisson pipeline so calibration is
not a confound; the lift is purely the feature's incremental OOS value.

Features (real data, free unless noted):
  rest_diff   days-since-last-match(home) - (away), from the full fixture history
  hfa         explicit home indicator (neutral==0)  -> residual home advantage vs sup
  sup2        sup_pre_l3 * |sup_pre_l3|  (nonlinearity: do blowouts bend the goal map?)
  xg_sup      team xG attack/defence rating diff (from worldcup_xg_raw.csv, if available)

Strict walk-forward: refit every REFIT_DAYS on prior rows; predict each row pre-fit;
score on OOS rows (date >= OOS_CUTOFF). Metrics: 1X2 multiclass log-loss + Brier,
goals RMSE (per side). KEEP a feature only on a clear, stable OOS improvement.
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

OUT = Path(__file__).resolve().parent
PERMATCH = OUT / "national_elo_layer3_permatch.csv"
RESULTS = OUT / "international_results.csv"
XG = OUT / "worldcup_xg_raw.csv"
REPORT = OUT / "feature_study_goals_report.txt"
TABLE = OUT / "feature_study_goals_table.csv"

REFIT_DAYS = 45
MIN_PAST = 400
OOS_CUTOFF = "2024-08-01"
HL_DAYS = 730.0
KMAX = 12


def pois_pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def wdl(lh, la):
    M = np.outer(pois_pmf(lh), pois_pmf(la))
    M /= M.sum()
    gh = np.arange(KMAX + 1)[:, None]
    ga = np.arange(KMAX + 1)[None, :]
    o25 = float(M[(gh + ga) >= 3].sum())
    return np.array([M[gh > ga].sum(), M[gh == ga].sum(), M[gh < ga].sum()]), o25


def rest_days(results):
    """days since each team's previous match -> dict (fixture_id, team_id) -> rest (capped 21)."""
    rows = []
    for _, r in results.iterrows():
        rows.append((r["date"], int(r["fixture_id"]), int(r["home_id"])))
        rows.append((r["date"], int(r["fixture_id"]), int(r["away_id"])))
    d = pd.DataFrame(rows, columns=["date", "fixture_id", "team_id"]).sort_values("date")
    last = {}
    out = {}
    for _, r in d.iterrows():
        tid = r["team_id"]
        prev = last.get(tid)
        gap = (r["date"] - prev).days if prev is not None else 21
        out[(int(r["fixture_id"]), tid)] = float(min(max(gap, 0), 21))
        last[tid] = r["date"]
    return out


def build_xg_rating_feature(df, xg_raw):
    """Walk-forward team xG attack/defence (time-decayed past means) -> xg_sup per match.
    Returns a dict fixture_id -> xg_sup (home_attack - away_attack + away_def - home_def),
    using ONLY matches strictly before each fixture's date. None where insufficient."""
    xa = xg_raw.dropna(subset=["xg"]).copy()
    if xa.empty:
        return {}
    # attach date per (fixture,team) from df
    fdate = dict(zip(df["fixture_id"], df["date"]))
    xa["date"] = xa["fixture_id"].map(fdate)
    xa = xa.dropna(subset=["date"]).sort_values("date")
    # per team: list of (date, xg_for, xg_against)
    by_team = {}
    # need opponent xg for "against": join on fixture
    piv = xa.pivot_table(index="fixture_id", columns="is_home", values="xg", aggfunc="first")
    recs = []
    for _, r in xa.iterrows():
        fid = r["fixture_id"]
        opp_is_home = 0 if r["is_home"] == 1 else 1
        xg_against = piv.loc[fid, opp_is_home] if (fid in piv.index and opp_is_home in piv.columns) else np.nan
        recs.append((r["date"], int(r["team_id"]), float(r["xg"]),
                     float(xg_against) if pd.notna(xg_against) else np.nan))
    rec = pd.DataFrame(recs, columns=["date", "team_id", "xgf", "xga"]).dropna().sort_values("date")
    for tid, g in rec.groupby("team_id"):
        by_team[int(tid)] = (g["date"].to_numpy(), g["xgf"].to_numpy(float), g["xga"].to_numpy(float))

    def rating(tid, when):
        recd = by_team.get(int(tid))
        if recd is None:
            return None
        dates, xgf, xga = recd
        mask = dates < np.datetime64(when)
        if mask.sum() < 3:
            return None
        w = np.exp(-np.log(2) * (np.datetime64(when) - dates[mask]).astype("timedelta64[D]").astype(float) / HL_DAYS)
        att = np.average(xgf[mask], weights=w)
        deff = np.average(xga[mask], weights=w)
        return att, deff

    out = {}
    gmean = float(rec["xgf"].mean())
    for _, r in df.iterrows():
        rh = rating(int(r["home_id"]), r["date"])
        ra = rating(int(r["away_id"]), r["date"])
        if rh is None or ra is None:
            continue
        # xG supremacy proxy: (home_attack + away_conceded) - (away_attack + home_conceded).
        # Scale is irrelevant — the walk-forward regression coefficient absorbs it.
        sup = (rh[0] + ra[1]) - (ra[0] + rh[1])
        out[int(r["fixture_id"])] = float(sup)
    return out


def fit_linear(X, y, w):
    XtW = X.T * w
    A = XtW @ X
    A[np.diag_indices(A.shape[0])] += 1e-6
    return np.linalg.solve(A, XtW @ y)


def run():
    pm = pd.read_csv(PERMATCH)
    pm["date"] = pd.to_datetime(pm["date"], errors="coerce")
    pm = pm.dropna(subset=["date", "sup_pre_l3", "gh", "ga"]).sort_values("date").reset_index(drop=True)

    res = pd.read_csv(RESULTS)
    res["date"] = pd.to_datetime(res["date"], errors="coerce")
    res = res.dropna(subset=["date", "fixture_id"])
    neutral = dict(zip(res["fixture_id"].astype(int), res["neutral"].fillna(0).astype(int)))

    rest = rest_days(res)
    pm["hfa"] = (1 - pm["fixture_id"].astype(int).map(neutral).fillna(0)).astype(float)
    pm["rest_h"] = [rest.get((int(f), int(h)), 21.0) for f, h in zip(pm["fixture_id"], pm["home_id"])]
    pm["rest_a"] = [rest.get((int(f), int(a)), 21.0) for f, a in zip(pm["fixture_id"], pm["away_id"])]
    pm["rest_diff"] = (pm["rest_h"] - pm["rest_a"]) / 7.0          # weeks
    pm["sup2"] = pm["sup_pre_l3"] * pm["sup_pre_l3"].abs()

    xg_feature = {}
    xg_cov = 0
    if XG.exists():
        xg_raw = pd.read_csv(XG)
        xg_feature = build_xg_rating_feature(pm, xg_raw)
        pm["xg_sup"] = pm["fixture_id"].astype(int).map(xg_feature)
        xg_cov = int(pm["xg_sup"].notna().sum())
    else:
        pm["xg_sup"] = np.nan

    # candidate feature sets added to the SUPREMACY regression (baseline = sup_pre_l3 only)
    FEATURES = {
        "baseline (sup_pre_l3)": [],
        "+rest_diff": ["rest_diff"],
        "+hfa": ["hfa"],
        "+sup2": ["sup2"],
        "+xg_sup": ["xg_sup"],
        "+rest+sup2": ["rest_diff", "sup2"],
    }

    days = (pm["date"] - pm["date"].min()).dt.days.to_numpy(float)
    n = len(pm)
    sup = pm["sup_pre_l3"].to_numpy(float)
    gh = pm["gh"].to_numpy(float)
    ga = pm["ga"].to_numpy(float)
    diff = gh - ga
    total = gh + ga
    res_idx = pm["res"].to_numpy(int)                                # 0 home,1 draw,2 away
    oos_cut = np.datetime64(OOS_CUTOFF)
    is_oos = (pm["date"].to_numpy() >= oos_cut)

    report = []

    def out(s=""):
        print(s)
        report.append(s)

    out("=" * 96)
    out("FEATURE STUDY A - goals / 1X2  (baseline = L3 sup_pre_l3; raw Poisson, no isotonic)")
    out("=" * 96)
    out(f"matches={n} | OOS(date>={OOS_CUTOFF})~{int(is_oos.sum())} | refit={REFIT_DAYS}d "
        f"HL={HL_DAYS:.0f}d | xG coverage={xg_cov}/{n} ({xg_cov/max(n,1)*100:.0f}%)")
    out("")
    out(f"  {'feature':24} {'n_oos':>6} {'logloss':>8} {'brier':>7} {'gRMSE':>7} "
        f"{'dLL%':>6} {'dBr%':>6} {'verdict':>10}")
    out("-" * 96)

    rows_table = []
    base_metrics = None
    for name, feats in FEATURES.items():
        # build design matrix columns: intercept + sup + feats
        cols = [np.ones(n), sup] + [pm[f].to_numpy(float) for f in feats]
        # rows with all features present
        valid = np.ones(n, bool)
        for f in feats:
            valid &= np.isfinite(pm[f].to_numpy(float))
        X = np.column_stack(cols)

        sup_hat = np.full(n, np.nan)
        tot_hat = np.full(n, np.nan)
        beta = None
        tbeta = None
        last = None
        for i in range(n):
            if not valid[i]:
                continue
            if beta is None or (days[i] - last) >= REFIT_DAYS:
                pmask = (days < days[i]) & valid
                if pmask.sum() >= MIN_PAST:
                    w = np.exp(-np.log(2) * (days[i] - days[pmask]) / HL_DAYS)
                    beta = fit_linear(X[pmask], diff[pmask], w)
                    tbeta = float(np.average(total[pmask], weights=w))  # total = decayed mean
                    last = days[i]
            if beta is not None:
                sup_hat[i] = X[i] @ beta
                tot_hat[i] = tbeta

        ev = is_oos & np.isfinite(sup_hat) & valid
        no = int(ev.sum())
        if no < 30:                       # too few OOS rows (e.g. sparse xG) -> can't judge
            out(f"  {name:24} {no:>6} {'n/a':>8} {'n/a':>7} {'n/a':>7} "
                f"{'':>6} {'':>6} {'INSUFICIENTE':>12}")
            rows_table.append({"feature": name, "n_oos": no, "logloss": None, "brier": None,
                               "goals_rmse": None, "d_logloss_pct": None, "d_brier_pct": None,
                               "verdict": "insufficient_sample"})
            continue
        lh = np.clip((tot_hat[ev] + sup_hat[ev]) / 2.0, 0.05, None)
        la = np.clip((tot_hat[ev] - sup_hat[ev]) / 2.0, 0.05, None)
        ll = br = 0.0
        sq = 0.0
        for k in range(no):
            p, _ = wdl(lh[k], la[k])
            p = np.clip(p, 1e-9, 1)
            r = res_idx[np.flatnonzero(ev)[k]]
            ll += -np.log(p[r])
            oneh = np.zeros(3); oneh[r] = 1
            br += float(np.sum((p - oneh) ** 2))
            sq += (gh[np.flatnonzero(ev)[k]] - lh[k]) ** 2 + (ga[np.flatnonzero(ev)[k]] - la[k]) ** 2
        ll /= no; br /= no
        grmse = float(np.sqrt(sq / (2 * no)))
        if base_metrics is None:
            base_metrics = (ll, br, grmse)
            dll = dbr = 0.0
            verdict = "BASELINE"
        else:
            dll = 100 * (base_metrics[0] - ll) / base_metrics[0]
            dbr = 100 * (base_metrics[1] - br) / base_metrics[1]
            verdict = "KEEP" if (dll >= 0.5 and dbr >= 0.3) else "discard"
        out(f"  {name:24} {no:>6} {ll:>8.4f} {br:>7.4f} {grmse:>7.3f} "
            f"{dll:>+5.1f}% {dbr:>+5.1f}% {verdict:>10}")
        rows_table.append({"feature": name, "n_oos": no, "logloss": round(ll, 4),
                           "brier": round(br, 4), "goals_rmse": round(grmse, 3),
                           "d_logloss_pct": round(dll, 2), "d_brier_pct": round(dbr, 2),
                           "verdict": verdict})

    out("-" * 96)
    out("dLL%/dBr% = OOS improvement vs baseline (higher=better). KEEP needs dLL>=0.5 AND dBr>=0.3.")
    pd.DataFrame(rows_table).to_csv(TABLE, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {TABLE}\nWritten: {REPORT}")


if __name__ == "__main__":
    run()
