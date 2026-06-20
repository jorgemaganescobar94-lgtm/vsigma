"""
FEATURE STUDY B - corners / shots (ISOLATED, analysis/worldcup/). NO market/odds.

Question: beyond the opponent-adjusted baseline (mu + gamma*home + att[team] + conc[opp]),
does any extra REAL-DATA feature add OOS signal for a team's corner/shot count?

Baseline = the shipped stats_model design. Each candidate feature is added as ONE extra
regressor to the ridge-WLS design, refit strict walk-forward, scored by OOS RMSE on the
raw count. KEEP only on a clear, stable RMSE improvement.

Features (real data, free; rolling = team's time-decayed PAST mean, strictly pre-match):
  poss_form   team rolling possession %         (possession-heavy -> more corners?)
  sot_form    team rolling shots-on-target       (finishing volume tendency)
  rest        team days-since-last-match (capped) (congestion/fatigue)
  opp_str     opponent L3 strength rating         (pinning weak teams -> more corners/shots?)
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
RAW = OUT / "worldcup_stats_raw.csv"
RESULTS = OUT / "international_results.csv"
L3RATINGS = OUT / "national_elo_layer3_ratings.csv"
REPORT = OUT / "feature_study_stats_report.txt"
TABLE = OUT / "feature_study_stats_table.csv"

STATS = ["corners", "shots"]            # the two KEPT stats (cards = noise, excluded)
HL_DAYS = 540.0
LAM = 8.0                               # ridge on att/conc (as in stats_model)
REFIT_DAYS = 45
MIN_PAST = 200
OOS_CUTOFF = "2024-08-01"
FEAT_HL = 540.0


def rest_days(results):
    rows = []
    for _, r in results.iterrows():
        rows.append((r["date"], int(r["fixture_id"]), int(r["home_id"])))
        rows.append((r["date"], int(r["fixture_id"]), int(r["away_id"])))
    d = pd.DataFrame(rows, columns=["date", "fixture_id", "team_id"]).sort_values("date")
    last, out = {}, {}
    for _, r in d.iterrows():
        tid = r["team_id"]
        prev = last.get(tid)
        gap = (r["date"] - prev).days if prev is not None else 21
        out[(int(r["fixture_id"]), tid)] = float(min(max(gap, 0), 21))
        last[tid] = r["date"]
    return out


def rolling_form(df, col):
    """team_id -> (dates ndarray, values ndarray); for strictly-past decayed means."""
    sub = df.dropna(subset=[col])[["date", "team_id", col]].sort_values("date")
    by = {}
    for tid, g in sub.groupby("team_id"):
        by[int(tid)] = (g["date"].to_numpy(), g[col].to_numpy(float))
    return by


def past_mean(by, tid, when):
    rec = by.get(int(tid))
    if rec is None:
        return None
    dates, vals = rec
    mask = dates < np.datetime64(when)
    if mask.sum() < 3:
        return None
    d, v = dates[mask], vals[mask]
    w = np.exp(-np.log(2) * (np.datetime64(when) - d).astype("timedelta64[D]").astype(float) / FEAT_HL)
    return float(np.average(v, weights=w))


def fit_ridge(X, y, w, n_dummy_start):
    XtW = X.T * w
    A = XtW @ X
    b = XtW @ y
    reg = np.zeros(X.shape[1])
    reg[n_dummy_start:] = LAM            # ridge on att/conc dummies only (not mu/gamma/feature)
    A[np.diag_indices(A.shape[0])] += reg + 1e-8
    return np.linalg.solve(A, b)


def run():
    df = pd.read_csv(RAW)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date", "team_id", "opp_id"]).sort_values("date").reset_index(drop=True)
    df["team_id"] = df["team_id"].astype(int)
    df["opp_id"] = df["opp_id"].astype(int)

    res = pd.read_csv(RESULTS)
    res["date"] = pd.to_datetime(res["date"], errors="coerce")
    res = res.dropna(subset=["date", "fixture_id"])
    rest = rest_days(res)

    # L3 strength by team name (ratings file) -> map to team_id via names in df
    strength = {}
    if L3RATINGS.exists():
        rt = pd.read_csv(L3RATINGS)
        name2str = {str(r["team"]): float(r["strength"]) for _, r in rt.iterrows()}
        for _, r in df.iterrows():
            strength[int(r["team_id"])] = name2str.get(str(r["team"]))
            strength[int(r["opp_id"])] = name2str.get(str(r["opp"]))

    poss_by = rolling_form(df, "possession")
    sot_by = rolling_form(df, "sot")

    # precompute per-row features
    df["rest"] = [rest.get((int(f), int(t)), 21.0) / 7.0
                  for f, t in zip(df["fixture_id"], df["team_id"])]
    df["opp_str"] = [strength.get(int(o)) for o in df["opp_id"]]
    df["poss_form"] = [past_mean(poss_by, t, d) for t, d in zip(df["team_id"], df["date"])]
    df["sot_form"] = [past_mean(sot_by, t, d) for t, d in zip(df["team_id"], df["date"])]

    FEATURES = {
        "baseline": [],
        "+poss_form": ["poss_form"],
        "+sot_form": ["sot_form"],
        "+rest": ["rest"],
        "+opp_str": ["opp_str"],
    }

    report = []

    def out(s=""):
        print(s)
        report.append(s)

    out("=" * 96)
    out("FEATURE STUDY B - corners / shots  (baseline = opponent-adjusted att/conc + home)")
    out("=" * 96)
    out(f"rows={len(df)} fixtures={df['fixture_id'].nunique()} | refit={REFIT_DAYS}d "
        f"HL={HL_DAYS:.0f}d ridge={LAM} | OOS>={OOS_CUTOFF}")
    out("")

    rows_table = []
    for stat in STATS:
        out(f"--- {stat.upper()} ---")
        out(f"  {'feature':16} {'n_oos':>6} {'baseRMSE/RMSE':>14} {'dRMSE%':>7} {'verdict':>10}")
        base_rmse = None
        for name, feats in FEATURES.items():
            sub = df[df[stat].notna()].copy()
            for f in feats:
                sub = sub[np.isfinite(sub[f].astype(float))]
            sub = sub.reset_index(drop=True)
            teams = sorted(set(sub["team_id"]) | set(sub["opp_id"]))
            loc = {t: i for i, t in enumerate(teams)}
            T = len(teams)
            y = sub[stat].to_numpy(float)
            z = np.log(y + 0.5)
            home = sub["is_home"].to_numpy(float)
            team_l = sub["team_id"].map(loc).to_numpy()
            opp_l = sub["opp_id"].map(loc).to_numpy()
            days = (sub["date"] - sub["date"].min()).dt.days.to_numpy(float)
            fcols = [sub[f].to_numpy(float) for f in feats]
            # standardise feature columns (helps ridge-free coef + comparability)
            fcols = [(c - np.nanmean(c)) / (np.nanstd(c) + 1e-9) for c in fcols]
            nf = len(feats)
            P = 2 + nf + 2 * T          # [mu, gamma, feats..., att(T), conc(T)]
            n = len(sub)

            def design(idx):
                X = np.zeros((len(idx), P))
                X[:, 0] = 1.0
                X[:, 1] = home[idx]
                for j, c in enumerate(fcols):
                    X[:, 2 + j] = c[idx]
                X[np.arange(len(idx)), 2 + nf + team_l[idx]] = 1.0
                X[np.arange(len(idx)), 2 + nf + T + opp_l[idx]] = 1.0
                return X

            lam_hat = np.full(n, np.nan)
            beta = None
            last = None
            allidx = np.arange(n)
            for i in range(n):
                if beta is None or (days[i] - last) >= REFIT_DAYS:
                    pmask = days < days[i]
                    if pmask.sum() >= MIN_PAST:
                        pidx = allidx[pmask]
                        w = np.exp(-np.log(2) * (days[i] - days[pidx]) / HL_DAYS)
                        beta = fit_ridge(design(pidx), z[pidx], w, 2 + nf)
                        last = days[i]
                if beta is not None:
                    xi = design(np.array([i]))[0]
                    lam_hat[i] = np.exp(xi @ beta)
            oos = (sub["date"].to_numpy() >= np.datetime64(OOS_CUTOFF)) & np.isfinite(lam_hat)
            no = int(oos.sum())
            rmse = float(np.sqrt(np.mean((y[oos] - lam_hat[oos]) ** 2)))
            if base_rmse is None:
                base_rmse = rmse
                drmse = 0.0
                verdict = "BASELINE"
            else:
                drmse = 100 * (base_rmse - rmse) / base_rmse
                verdict = "KEEP" if drmse >= 0.5 else "discard"
            out(f"  {name:16} {no:>6} {base_rmse if name=='baseline' else rmse:>14.4f} "
                f"{drmse:>+6.1f}% {verdict:>10}")
            rows_table.append({"stat": stat, "feature": name, "n_oos": no,
                               "rmse": round(rmse, 4), "d_rmse_pct": round(drmse, 2),
                               "verdict": verdict})
        out("")

    out("dRMSE% = OOS RMSE improvement vs baseline (higher=better). KEEP needs dRMSE>=0.5%.")
    pd.DataFrame(rows_table).to_csv(TABLE, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {TABLE}\nWritten: {REPORT}")


if __name__ == "__main__":
    run()
