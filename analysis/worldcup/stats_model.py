"""
PASO B - opponent-adjusted DATA model for corners / cards / shots (ISOLATED).

Real match stats only (worldcup_stats_raw.csv). NO market/odds. NOT production.

Model (per stat, independently): the count a team produces in a match is Poisson with
    log E[count] = mu + gamma*is_home + att[team] + conc[opponent]
  * att[team]  = how many of the stat the team generates (attack/propensity)
  * conc[opp]  = how many the opponent concedes/induces
  * gamma      = home advantage; mu = global mean log-count
Fit by ridge-regularised weighted least squares on log(count+0.5), time-decayed. Ridge
on att/conc only (not mu/gamma) -> thin teams shrink to the mean (= base-rate).

WC is played at neutral venues -> predictions use is_home=0 for both teams.
Per fixture: per-team expected count, total (sum of two Poissons), and O/U line prob.

Walk-forward OOS validation reports, honestly, how predictable each stat really is
(lift of the model's Poisson deviance vs a base-rate constant). Expected: weak.

Roles:
  fit_and_save()    LOCAL: fit from raw, validate OOS, write ratings + calibration JSON +
                    report + per-fixture WC predictions.
  load_predictor()  CI-safe offline predictor from committed ratings + calibration.
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
RAW = OUT_DIR / "worldcup_stats_raw.csv"
RATINGS = OUT_DIR / "worldcup_stats_ratings.csv"
CALIB = OUT_DIR / "worldcup_stats_calibration.json"
PREDS = OUT_DIR / "worldcup_stats_predictions.csv"
REPORT = OUT_DIR / "worldcup_stats_model_report.txt"
VALID = OUT_DIR / "worldcup_stats_validation.csv"
L3_PREDS = OUT_DIR / "worldcup_our_model_predictions.csv"  # source of current WC fixtures

STATS = ["corners", "cards", "shots"]          # cards = yellow + red
HL_DAYS = 540.0
LAM = 8.0
REFIT_DAYS = 45
MIN_PAST = 150
OOS_CUTOFF = "2024-08-01"
KMAX = 40                                       # Poisson support for O/U totals
DEFAULT_LINES = {"corners": 9.5, "cards": 3.5, "shots": 22.5}  # refined from data medians
SHOW_LIFT_MIN = 4.0  # require real signal: OOS deviance-lift % below this ("muy débil"/noise) is
                     # hidden from the ficha (kept in the scorecard). cards (~+2%) fail; corners/shots pass.


def _pois_pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def prob_over(lam_total, line):
    """P(total > line) for total ~ Poisson(lam_total)."""
    pmf = _pois_pmf(lam_total)
    k_need = int(np.floor(line)) + 1
    return float(pmf[k_need:].sum())


def _load_raw():
    df = pd.read_csv(RAW)
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=["date", "team_id", "opp_id"])
    df["team_id"] = df["team_id"].astype(int)
    df["opp_id"] = df["opp_id"].astype(int)
    df["cards"] = df["yellow"].astype(float) + df["red"].fillna(0).astype(float)
    return df.sort_values("date").reset_index(drop=True)


def fit_stat(team_l, opp_l, home, z, w, T, lam=LAM):
    """Ridge WLS. Returns beta = [mu, gamma, att(0..T-1), conc(0..T-1)]."""
    N = len(z)
    P = 2 + 2 * T
    X = np.zeros((N, P))
    X[:, 0] = 1.0
    X[:, 1] = home
    X[np.arange(N), 2 + team_l] = 1.0
    X[np.arange(N), 2 + T + opp_l] = 1.0
    XtW = X.T * w
    A = XtW @ X
    b = XtW @ z
    reg = np.zeros(P)
    reg[2:] = lam               # regularise att/conc only
    A[np.diag_indices(P)] += reg
    return np.linalg.solve(A, b)


def poisson_dev(y, lam):
    y = np.asarray(y, float)
    lam = np.clip(np.asarray(lam, float), 1e-9, None)
    pos = y > 0
    t = np.zeros_like(y)
    t[pos] = y[pos] * np.log(y[pos] / lam[pos])
    return float(2.0 * np.sum(t - (y - lam)))


def _design(df, stat, teams):
    loc = {t: i for i, t in enumerate(teams)}
    sub = df[df[stat].notna()].copy()
    team_l = sub["team_id"].map(loc).to_numpy()
    opp_l = sub["opp_id"].map(loc).to_numpy()
    home = sub["is_home"].to_numpy(float)
    y = sub[stat].to_numpy(float)
    z = np.log(y + 0.5)
    days = (sub["date"] - sub["date"].min()) / np.timedelta64(1, "D")
    return sub, team_l, opp_l, home, y, z, days.to_numpy(float)


def walkforward(df, stat, teams):
    """Strict OOS: refit every REFIT_DAYS on prior rows; predict each row pre-fit."""
    loc = {t: i for i, t in enumerate(teams)}
    T = len(teams)
    sub, team_l, opp_l, home, y, z, days = _design(df, stat, teams)
    n = len(sub)
    lam_hat = np.full(n, np.nan)
    beta = None
    last = None
    for i in range(n):
        if beta is None or (days[i] - last) >= REFIT_DAYS:
            pm = days < days[i]
            if pm.sum() >= MIN_PAST:
                w = np.exp(-np.log(2) * (days[i] - days[pm]) / HL_DAYS)
                beta = fit_stat(team_l[pm], opp_l[pm], home[pm], z[pm], w, T)
                last = days[i]
        if beta is not None:
            mu, gamma = beta[0], beta[1]
            lam_hat[i] = np.exp(mu + gamma * home[i] + beta[2 + team_l[i]] + beta[2 + T + opp_l[i]])
    dates = sub["date"].to_numpy()
    oos = (dates >= np.datetime64(OOS_CUTOFF)) & np.isfinite(lam_hat)
    return sub, y, lam_hat, oos


def fit_and_save():
    df = _load_raw()
    teams = sorted(set(df["team_id"]) | set(df["opp_id"]))
    name_by_id = {}
    for _, r in df.iterrows():
        name_by_id[int(r["team_id"])] = r["team"]
        name_by_id[int(r["opp_id"])] = r["opp"]
    T = len(teams)
    report = []

    def out(s=""):
        print(s)
        report.append(s)

    out("=" * 92)
    out("PASO B - opponent-adjusted DATA model (corners / cards / shots). NO market.")
    out("=" * 92)
    out(f"stat rows: {len(df)} team-matches | fixtures: {df['fixture_id'].nunique()} | teams: {T} | "
        f"dates {str(df['date'].min())[:10]}..{str(df['date'].max())[:10]}")
    out(f"HL={HL_DAYS:.0f}d ridge={LAM} refit={REFIT_DAYS}d OOS_cutoff={OOS_CUTOFF}")
    out("")
    out("WALK-FORWARD OOS — predictability vs base-rate (honest: stats are noisy)")
    out("-" * 92)
    out(f"  {'stat':8} {'n_oos':>6} {'mean':>6} {'baseMAE':>8} {'modelMAE':>9} "
        f"{'dev_base':>9} {'dev_model':>10} {'lift%':>7} {'verdict':>14}")

    ratings = {int(t): {"team": name_by_id.get(int(t), str(t))} for t in teams}
    calib = {}
    valrows = []
    lines_used = {}
    for stat in STATS:
        sub, y, lam_hat, oos = walkforward(df, stat, teams)
        yo = y[oos]
        lo = lam_hat[oos]
        base = float(np.mean(y[~np.isnan(y)]))   # global base-rate (constant)
        base_arr = np.full(len(yo), base)
        mae_b = float(np.mean(np.abs(yo - base_arr)))
        mae_m = float(np.mean(np.abs(yo - lo)))
        dev_b = poisson_dev(yo, base_arr)
        dev_m = poisson_dev(yo, lo)
        lift = 100 * (dev_b - dev_m) / dev_b if dev_b > 0 else 0.0
        verdict = ("nada/ruido" if lift < 1 else "muy débil" if lift < 4
                   else "débil" if lift < 8 else "moderada")
        out(f"  {stat:8} {len(yo):>6} {base:>6.2f} {mae_b:>8.2f} {mae_m:>9.2f} "
            f"{dev_b:>9.1f} {dev_m:>10.1f} {lift:>+6.1f}% {verdict:>14}")
        valrows.append({"stat": stat, "n_oos": len(yo), "base_mean": round(base, 3),
                        "base_mae": round(mae_b, 3), "model_mae": round(mae_m, 3),
                        "dev_lift_pct": round(lift, 2), "verdict": verdict})

        # FINAL fit on all data (decay to latest date) -> ratings
        _, team_l, opp_l, home, _, z, days = _design(df, stat, teams)
        w = np.exp(-np.log(2) * (days.max() - days) / HL_DAYS)
        beta = fit_stat(team_l, opp_l, home, z, w, T)
        mu, gamma = float(beta[0]), float(beta[1])
        # gate: a stat with OOS lift below SHOW_LIFT_MIN is noise -> hidden from the ficha
        # (still settled + scored in the scorecard). corners/shots usually pass; cards usually not.
        calib[stat] = {"mu": mu, "gamma": gamma,
                       "lift": round(float(lift), 2), "show": bool(lift >= SHOW_LIFT_MIN)}
        for i, t in enumerate(teams):
            ratings[int(t)][f"{stat}_att"] = round(float(beta[2 + i]), 4)
            ratings[int(t)][f"{stat}_conc"] = round(float(beta[2 + T + i]), 4)
        # data-refined O/U line: round(median total) - 0.5
        tot = df.groupby("fixture_id")[stat].sum()
        med = float(np.median(tot.dropna())) if len(tot.dropna()) else DEFAULT_LINES[stat]
        line = round(med) - 0.5
        lines_used[stat] = line
        calib[stat]["line"] = line

    out("-" * 92)
    out("lift% = reduction in OOS Poisson deviance vs a constant base-rate. Higher = more")
    out("predictable. Cards are essentially noise; corners/shots carry a little signal.")
    out(f"O/U lines (from data medians): {lines_used}")
    out("")

    # top/bottom teams per stat (sanity)
    rdf = pd.DataFrame([ratings[int(t)] for t in teams])
    for stat in STATS:
        top = rdf.sort_values(f"{stat}_att", ascending=False).head(5)
        out(f"  most {stat} generated (att): " + ", ".join(
            f"{r['team']} {r[f'{stat}_att']:+.2f}" for _, r in top.iterrows()))

    # per-fixture WC predictions (from L3 fixture list)
    pred = Predictor(ratings_df=rdf, calib=calib)
    prows = []
    if L3_PREDS.exists():
        for _, r in pd.read_csv(L3_PREDS).iterrows():
            p = pred.predict(str(r["home"]), str(r["away"]))
            if p:
                prows.append({"fixture_id": int(r["fixture_id"]), "home": r["home"], "away": r["away"], **p})

    RATINGS.parent.mkdir(parents=True, exist_ok=True)
    rdf.to_csv(RATINGS, index=False)
    CALIB.write_text(json.dumps(calib, indent=2, ensure_ascii=False), encoding="utf-8")
    pd.DataFrame(valrows).to_csv(VALID, index=False)
    if prows:
        pd.DataFrame(prows).to_csv(PREDS, index=False)
    REPORT.write_text("\n".join(report), encoding="utf-8")
    out(f"WC fixture stat-predictions written: {len(prows)}")
    print(f"\nWritten: {RATINGS}\nWritten: {CALIB}\nWritten: {VALID}\nWritten: {PREDS}\nWritten: {REPORT}")


class Predictor:
    """Offline per-fixture stats predictor from ratings + calibration. NO API."""
    def __init__(self, ratings_df=None, calib=None):
        if ratings_df is None:
            ratings_df = pd.read_csv(RATINGS)
        if calib is None:
            calib = json.loads(CALIB.read_text(encoding="utf-8"))
        self.calib = calib
        # per-stat gating from OOS validation: show only stats that beat the base-rate
        self.show = {s: bool(calib.get(s, {}).get("show", True)) for s in STATS}
        self.lift = {s: float(calib.get(s, {}).get("lift", 0.0) or 0.0) for s in STATS}
        self.att = {}
        self.conc = {}
        for _, r in ratings_df.iterrows():
            nm = str(r["team"])
            for stat in STATS:
                self.att.setdefault(stat, {})[nm] = float(r.get(f"{stat}_att", 0.0) or 0.0)
                self.conc.setdefault(stat, {})[nm] = float(r.get(f"{stat}_conc", 0.0) or 0.0)

    def predict(self, home, away):
        """Per-stat expected counts (neutral venue), total, and O/U line prob. None if unknown."""
        if home not in self.att.get("corners", {}) or away not in self.att.get("corners", {}):
            return None
        out = {}
        for stat in STATS:
            mu = self.calib[stat]["mu"]
            line = self.calib[stat].get("line", DEFAULT_LINES[stat])
            # neutral: is_home = 0 for both
            lam_h = float(np.exp(mu + self.att[stat][home] + self.conc[stat][away]))
            lam_a = float(np.exp(mu + self.att[stat][away] + self.conc[stat][home]))
            tot = lam_h + lam_a
            out[f"{stat}_home"] = round(lam_h, 2)
            out[f"{stat}_away"] = round(lam_a, 2)
            out[f"{stat}_total"] = round(tot, 2)
            out[f"{stat}_line"] = line
            out[f"{stat}_over"] = round(prob_over(tot, line), 4)
        return out


def load_predictor():
    if not (RATINGS.exists() and CALIB.exists()):
        return None
    return Predictor()


def shown_stats():
    """Set of stats whose OOS lift cleared SHOW_LIFT_MIN (renderable in the ficha).
    Offline/CI-safe: reads the committed calibration; defaults to all if absent."""
    try:
        calib = json.loads(CALIB.read_text(encoding="utf-8"))
    except Exception:
        return set(STATS)
    return {s for s in STATS if bool(calib.get(s, {}).get("show", True))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fit", action="store_true", help="LOCAL: fit from raw, validate, save")
    a = ap.parse_args()
    if a.fit:
        fit_and_save()
    else:
        ap.print_help()
