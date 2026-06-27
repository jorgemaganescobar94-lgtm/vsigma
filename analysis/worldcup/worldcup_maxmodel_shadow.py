"""
WORLD CUP "MAX" SHADOW MODEL (A/B vs L3). ISOLATED, analysis/worldcup/. NO market/odds, NO API to
train (0 calls — international_results.csv + L3 per-match supremacy, both committed), NO production,
NO Telegram. This is a SHADOW model run head-to-head against the shipped L3; it NEVER replaces it.

IDEA: take the L3's point-in-time supremacy (sup_pre_l3, already walk-forward in
national_elo_layer3_permatch.csv) as the CORE feature and enrich it with result-derived, strictly
pre-match features (form, H2H, rest, neutral). Fit a REGULARISED multinomial logit (+ isotonic, like
L3) for 1X2 and Poisson regressions for goals. Compare OOS, head-to-head, to the shipped L3.

ANTI-LEAKAGE: every feature is point-in-time (sup_pre_l3 is the L3 walk-forward rating difference;
form/H2H/rest are time-decayed EWMAs over STRICTLY-PRIOR fixtures). The L3 baseline is reproduced
EXACTLY from the committed calibration (l3_offline.Predictor) applied to the same sup_pre. Both models
use the SAME burn-in (<2024-01-01) / OOS (>=2024-01-01) split as the shipped L3 -> fair A/B.

OUTPUT (shadow only, git-add explicit): scorecard A/B vs L3 + per-fixture WC shadow predictions.
Squad quality (squad_quality_raw_48.csv) is a WC-only DISPLAY adjustment, NOT a training feature
(historical coverage ~0). Live injuries are an optional, clearly-labelled WC adjustment (see --injuries).

Run:  python analysis/worldcup/worldcup_maxmodel_shadow.py
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import l3_offline  # noqa: E402  (committed L3 calibration -> faithful baseline; no API on import)

from sklearn.linear_model import LogisticRegressionCV, PoissonRegressor  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RESULTS = HERE / "international_results.csv"
PERMATCH = HERE / "national_elo_layer3_permatch.csv"
RATINGS = HERE / "national_elo_layer3_ratings.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
WC_PREDS = HERE / "worldcup_our_model_predictions.csv"
SQUAD = HERE / "squad_quality_raw_48.csv"
REPORT = HERE / "worldcup_maxmodel_shadow_report.txt"
SCORECARD = HERE / "worldcup_maxmodel_shadow_scorecard.csv"
WC_SHADOW = HERE / "worldcup_maxmodel_shadow_predictions.csv"

OOS_CUTOFF = np.datetime64("2024-01-01")
HL_FORM = 365.0          # form half-life (faster than strength's 730d)
HL_STREAK = 90.0         # short-term momentum
HL_H2H = 1095.0          # head-to-head decays slowly
REST_CAP = 21.0
KMAX = 10
NBOOT = 3000
RNG = np.random.default_rng(0)
# CALIBRACIÓN SUAVE: el escalón de la isotónica colapsaba entradas distintas y mapeaba extremos a 0
# (rompía honestidad + granularidad). Temperature scaling = monótona, continua, fit SOLO en burn-in.
EPS_FLOOR = 0.03     # suelo por clase: nunca 0.0%; tapado honesto y visible (>=3%, no falsa certeza)
XG_CAP = 3.0         # tope per-team de xG (favoritos no deben dispararse; L3 ~<=2.9)


def _softmax(z):
    z = np.asarray(z, float)
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def _floor_norm(P, eps=EPS_FLOOR):
    """Clip each class to >=eps and renormalise -> no class ever exactly 0/1 (honest)."""
    P = np.clip(np.asarray(P, float), eps, None)
    return P / P.sum(axis=1, keepdims=True)


def _fit_temperature(logits, Y):
    """Single temperature T>0 minimising burn-in multinomial logloss of softmax(logits/T). SMOOTH +
    monotone: preserves the per-fixture ranking (distinct inputs -> distinct outputs), no plateaus,
    no exact zeros. Fit on the supplied (burn-in) rows only -> no leakage."""
    from scipy.optimize import minimize_scalar
    logits = np.asarray(logits, float)

    def nll(log_t):
        P = np.clip(_softmax(logits / np.exp(log_t)), 1e-12, 1.0)
        return -np.mean(np.sum(Y * np.log(P), axis=1))

    r = minimize_scalar(nll, bounds=(np.log(0.3), np.log(8.0)), method="bounded")
    return float(np.exp(r.x))


# ------------------------------------------------------------------ metrics (3-class one-hot)
def _ll_rows(P, Y):
    P = np.clip(P, 1e-15, 1.0)
    return -np.sum(Y * np.log(P), axis=1)


def _brier_rows(P, Y):
    return np.sum((P - Y) ** 2, axis=1)


def _ece(P, Y, bins=10):
    conf = P.max(1); pred = P.argmax(1); true = Y.argmax(1); hit = (pred == true).astype(float)
    e = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        m = (conf > lo) & (conf <= hi)
        if m.sum():
            e += m.mean() * abs(hit[m].mean() - conf[m].mean())
    return float(e)


def _boot_diff(loss_a, loss_b):
    """Paired bootstrap of mean(loss_a - loss_b) (>0 => b better). Returns (obs, lo, hi, p_b_not_better)."""
    d = np.asarray(loss_a) - np.asarray(loss_b)
    n = len(d)
    obs = float(d.mean())
    bs = np.array([d[RNG.integers(0, n, n)].mean() for _ in range(NBOOT)])
    return obs, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), float(np.mean(bs <= 0))


# ------------------------------------------------------------------ Poisson O/U & BTTS
def _pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def _ou_btts(lh, la):
    M = np.outer(_pmf(lh), _pmf(la)); M /= M.sum()
    gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
    over25 = float(M[(gh + ga) >= 3].sum())
    btts = float(M[(gh >= 1) & (ga >= 1)].sum())
    # safety net: OU/BTTS never degenerate to exactly 0/1 (honest)
    clip = lambda v: min(max(v, EPS_FLOOR), 1.0 - EPS_FLOOR)
    return clip(over25), clip(btts)


# ------------------------------------------------------------------ anti-leakage feature build
def build_features():
    """Point-in-time features per fixture from international_results (strictly-prior EWMAs) joined to
    the L3 per-match supremacy. Returns a DataFrame in date order with the feature matrix + actuals."""
    pm = pd.read_csv(PERMATCH)
    pm["date"] = pd.to_datetime(pm["date"], utc=True, errors="coerce").dt.tz_localize(None)
    pm = pm.dropna(subset=["date", "home_id", "away_id", "sup_pre_l3", "gh", "ga"]).copy()
    ir = pd.read_csv(RESULTS)
    neut = {int(r.fixture_id): int(r.neutral) for r in ir.itertuples() if pd.notna(r.fixture_id)}
    pm["neutral"] = pm["fixture_id"].map(neut).fillna(0).astype(int)
    pm = pm.sort_values("date").reset_index(drop=True)

    # per-team EWMA state: gf, ga, ppg (HL_FORM), streak ppg (HL_STREAK); last_date for rest
    gf, ga, ppg, strk, lastd = {}, {}, {}, {}, {}
    h2h = {}                                   # frozenset{a,b} -> {"S":margin_sum,"W":w,"ref":lower_id}
    glob = {"gf": 1.3, "ppg": 1.3}             # neutral fallback (≈ global mean goals/ppg)

    def ewma_get(d, tid, store, hl):
        rec = store.get(tid)
        if rec is None:
            return None
        s, w, ld = rec
        return s / w if w > 0 else None

    rows = []
    for r in pm.itertuples():
        h, a, d = int(r.home_id), int(r.away_id), r.date
        feat = {}
        # form diffs (home - away); None -> 0 (neutral)
        for name, store, hl, fb in (("gf", gf, HL_FORM, glob["gf"]), ("ga", ga, HL_FORM, glob["gf"]),
                                    ("ppg", ppg, HL_FORM, glob["ppg"]), ("strk", strk, HL_STREAK, glob["ppg"])):
            vh = ewma_get(d, h, store, hl); va = ewma_get(d, a, store, hl)
            feat[f"{name}_diff"] = (vh if vh is not None else fb) - (va if va is not None else fb)
        # rest diff
        rh = min((d - lastd[h]).days, REST_CAP) if h in lastd else REST_CAP
        ra = min((d - lastd[a]).days, REST_CAP) if a in lastd else REST_CAP
        feat["rest_diff"] = (rh - ra) / 7.0
        # H2H decayed margin from home's perspective
        key = frozenset((h, a)); rec = h2h.get(key)
        if rec and rec["W"] > 0:
            m = rec["S"] / rec["W"]
            feat["h2h"] = m if rec["ref"] == h else -m
        else:
            feat["h2h"] = 0.0
        feat["neutral"] = float(r.neutral)
        feat["sup_pre_l3"] = float(r.sup_pre_l3)
        feat["fixture_id"] = int(r.fixture_id); feat["date"] = d
        feat["gh"] = float(r.gh); feat["ga"] = float(r.ga)
        feat["res"] = 0 if r.gh > r.ga else (1 if r.gh == r.ga else 2)
        rows.append(feat)

        # ---- UPDATE state AFTER using it (strictly past) ----
        ph, pa = (3, 0) if r.gh > r.ga else ((1, 1) if r.gh == r.ga else (0, 3))
        for tid, gfor, gag, pts in ((h, r.gh, r.ga, ph), (a, r.ga, r.gh, pa)):
            for name, store, hl, val in (("gf", gf, HL_FORM, gfor), ("ga", ga, HL_FORM, gag),
                                         ("ppg", ppg, HL_FORM, pts), ("strk", strk, HL_STREAK, pts)):
                s, w, ld = store.get(tid, (0.0, 0.0, d))
                dec = 0.5 ** (max((d - ld).days, 0) / hl)
                store[tid] = (s * dec + val, w * dec + 1.0, d)
            lastd[tid] = d
        ref = min(h, a); margin = (r.gh - r.ga) if ref == h else (r.ga - r.gh)
        rec = h2h.get(key, {"S": 0.0, "W": 0.0, "ref": ref})
        dec = 0.5 ** (max((d - rec.get("ld", d)).days, 0) / HL_H2H) if rec["W"] > 0 else 1.0
        rec["S"] = rec["S"] * dec + margin; rec["W"] = rec["W"] * dec + 1.0; rec["ref"] = ref; rec["ld"] = d
        h2h[key] = rec
    return pd.DataFrame(rows)


FEATURES = ["sup_pre_l3", "gf_diff", "ga_diff", "ppg_diff", "strk_diff", "rest_diff", "h2h", "neutral"]


def main(do_injuries=False):
    df = build_features()
    burn = df["date"].to_numpy() < OOS_CUTOFF
    oos = ~burn
    X = df[FEATURES].to_numpy(float)
    res = df["res"].to_numpy(int)
    Y = np.eye(3)[res]
    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    rep = []

    def out(s=""):
        print(s); rep.append(s)

    out("=" * 100)
    out("WORLD CUP MAX SHADOW MODEL — A/B vs shipped L3 (1X2 + goals). 0 API, anti-leakage, walk-forward.")
    out("=" * 100)
    out(f"fixtures={len(df)} | burn-in(<2024-01-01)={int(burn.sum())} | OOS={int(oos.sum())} | boot={NBOOT}")
    out(f"features={FEATURES}")
    out("")

    # ---------- L3 BASELINE (faithful: committed calibration applied to sup_pre) ----------
    import json
    calib = json.loads(CALIB.read_text(encoding="utf-8"))
    l3 = l3_offline.Predictor(ratings={}, calib=calib)
    matchup = bool(l3_offline.TOTAL_MATCHUP_LIVE)
    P_l3 = np.zeros((len(df), 3)); lh_l3 = np.zeros(len(df)); la_l3 = np.zeros(len(df))
    for i, s in enumerate(df["sup_pre_l3"].to_numpy(float)):
        cal, lh, la = l3._predict_with(s, matchup)
        P_l3[i] = cal; lh_l3[i] = lh; la_l3[i] = la

    # ---------- MAX MODEL 1X2 (regularised multinomial logit + isotonic, burn-in fit) ----------
    sc = StandardScaler().fit(X[burn])
    Xs = sc.transform(X)
    clf = LogisticRegressionCV(Cs=10, cv=5, max_iter=2000, scoring="neg_log_loss")
    clf.fit(Xs[burn], res[burn])
    # SMOOTH monotone calibration (temperature scaling, burn-in only) + eps-floor -> distinct inputs
    # give distinct outputs and no class is ever 0/1 (replaces the step-isotonic that collapsed/zeroed).
    logit = clf.decision_function(Xs)                 # columns ordered by clf.classes_ (0,1,2)
    T = _fit_temperature(logit[burn], Y[burn])
    P_mx = _floor_norm(_softmax(logit / T))

    # ---------- MAX MODEL goals (Poisson regressions, burn-in fit; xG capped) ----------
    pr_h = PoissonRegressor(alpha=1e-2, max_iter=2000).fit(Xs[burn], gh[burn])
    pr_a = PoissonRegressor(alpha=1e-2, max_iter=2000).fit(Xs[burn], ga[burn])
    lh_mx = np.minimum(pr_h.predict(Xs), XG_CAP); la_mx = np.minimum(pr_a.predict(Xs), XG_CAP)

    # ---------- A/B SCORECARD (OOS) ----------
    o = oos
    out("-" * 100)
    out("A/B OOS — 1X2  (positive Δ => MAX better than L3; signif if 95% CI excludes 0)")
    out("-" * 100)
    out(f"  {'metric':10} {'L3':>9} {'MAX':>9} {'Δ(L3-MAX)':>11} {'95% CI':>20} {'p':>7} {'signif':>7}")
    scrows = []

    def line(metric, la_, lb_, rows_a, rows_b, lower_better=True):
        va, vb = float(np.mean(la_)), float(np.mean(lb_))
        if rows_a is not None:
            obs, lo, hi, p = _boot_diff(rows_a, rows_b)   # mean(L3_loss - MAX_loss); >0 => MAX better
            sig = "YES" if (lo > 0) else ("WORSE" if hi < 0 else "no")
            out(f"  {metric:10} {va:>9.4f} {vb:>9.4f} {obs:>+11.4f} [{lo:>+7.4f},{hi:>+7.4f}] {p:>7.3f} {sig:>7}")
            scrows.append({"metric": metric, "L3": round(va, 5), "MAX": round(vb, 5),
                           "delta_L3_minus_MAX": round(obs, 5), "ci_lo": round(lo, 5),
                           "ci_hi": round(hi, 5), "p": round(p, 3), "signif": sig})
        else:
            d = "MAX" if (vb > va) else "L3"
            out(f"  {metric:10} {va:>9.4f} {vb:>9.4f} {'(higher='+d+')':>11}")
            scrows.append({"metric": metric, "L3": round(va, 5), "MAX": round(vb, 5)})

    line("logloss", _ll_rows(P_l3[o], Y[o]), _ll_rows(P_mx[o], Y[o]),
         _ll_rows(P_l3[o], Y[o]), _ll_rows(P_mx[o], Y[o]))
    line("brier", _brier_rows(P_l3[o], Y[o]), _brier_rows(P_mx[o], Y[o]),
         _brier_rows(P_l3[o], Y[o]), _brier_rows(P_mx[o], Y[o]))
    accs_l3 = (P_l3[o].argmax(1) == res[o]).astype(float)
    accs_mx = (P_mx[o].argmax(1) == res[o]).astype(float)
    line("accuracy", accs_l3, accs_mx, None, None)
    out(f"  {'ECE':10} {_ece(P_l3[o], Y[o]):>9.4f} {_ece(P_mx[o], Y[o]):>9.4f}   (lower=better)")
    scrows.append({"metric": "ECE", "L3": round(_ece(P_l3[o], Y[o]), 5), "MAX": round(_ece(P_mx[o], Y[o]), 5)})

    out("")
    out("-" * 100)
    out("A/B OOS — GOALS (Over 2.5 & BTTS, binary logloss/brier)")
    out("-" * 100)
    out(f"  {'metric':12} {'L3':>9} {'MAX':>9} {'Δ(L3-MAX)':>11} {'95% CI':>20} {'p':>7} {'signif':>7}")
    ou_l3 = np.array([_ou_btts(lh_l3[i], la_l3[i]) for i in range(len(df))])
    ou_mx = np.array([_ou_btts(lh_mx[i], la_mx[i]) for i in range(len(df))])
    y_over = ((gh + ga) >= 3).astype(float); y_btts = ((gh >= 1) & (ga >= 1)).astype(float)

    def binll(p, y):
        p = np.clip(p, 1e-15, 1 - 1e-15); return -(y * np.log(p) + (1 - y) * np.log(1 - p))

    for j, (mname, yv) in enumerate([("OU2.5_ll", y_over), ("BTTS_ll", y_btts)]):
        la_ = binll(ou_l3[o, j], yv[o]); lb_ = binll(ou_mx[o, j], yv[o])
        obs, lo, hi, p = _boot_diff(la_, lb_)
        sig = "YES" if lo > 0 else ("WORSE" if hi < 0 else "no")
        out(f"  {mname:12} {la_.mean():>9.4f} {lb_.mean():>9.4f} {obs:>+11.4f} [{lo:>+7.4f},{hi:>+7.4f}] {p:>7.3f} {sig:>7}")
        scrows.append({"metric": mname, "L3": round(float(la_.mean()), 5), "MAX": round(float(lb_.mean()), 5),
                       "delta_L3_minus_MAX": round(obs, 5), "ci_lo": round(lo, 5), "ci_hi": round(hi, 5),
                       "p": round(p, 3), "signif": sig})
    out("")

    # ---------- WC SHADOW PREDICTIONS (max model refit on ALL data) ----------
    out("-" * 100)
    out("WC SHADOW PREDICTIONS (max model refit on ALL data; L3 side-by-side; squad = WC-only adj)")
    out("-" * 100)
    sc_all = StandardScaler().fit(X); Xa = sc_all.transform(X)
    clf_all = LogisticRegressionCV(Cs=10, cv=5, max_iter=2000, scoring="neg_log_loss").fit(Xa, res)
    T_all = _fit_temperature(clf_all.decision_function(Xa), Y)   # smooth calibration for live preds
    prh = PoissonRegressor(alpha=1e-2, max_iter=2000).fit(Xa, gh)
    pra = PoissonRegressor(alpha=1e-2, max_iter=2000).fit(Xa, ga)
    n_wc = _write_wc_shadow(df, sc_all, clf_all, T_all, prh, pra, out, do_injuries)

    SCORECARD.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(scrows).to_csv(SCORECARD, index=False)
    REPORT.write_text("\n".join(rep), encoding="utf-8")
    print(f"\nWritten: {SCORECARD}\nWritten: {WC_SHADOW} ({n_wc} fixtures)\nWritten: {REPORT}")


def _latest_team_features(df):
    """Most-recent EWMA feature snapshot per team_id (for WC fixtures). Rebuilds the same EWMAs and
    keeps the final state — point-in-time as of the last historical match."""
    # reuse build_features's final per-team state by re-deriving from international_results tail:
    # simplest faithful proxy -> average of a team's last rows' diffs is complex; instead we expose
    # the per-team absolute EWMAs by re-running a light pass.
    ir = pd.read_csv(RESULTS)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
    ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).sort_values("date")
    gf, ga, ppg, strk, lastd = {}, {}, {}, {}, {}
    for r in ir.itertuples():
        for tid, gfor, gag, pts, opp in ((int(r.home_id), r.gh, r.ga, None, int(r.away_id)),
                                         (int(r.away_id), r.ga, r.gh, None, int(r.home_id))):
            pts = (3 if gfor > gag else (1 if gfor == gag else 0))
            for name, store, hl, val in (("gf", gf, HL_FORM, gfor), ("ga", ga, HL_FORM, gag),
                                         ("ppg", ppg, HL_FORM, pts), ("strk", strk, HL_STREAK, pts)):
                s, w, ld = store.get(tid, (0.0, 0.0, r.date))
                dec = 0.5 ** (max((r.date - ld).days, 0) / hl)
                store[tid] = (s * dec + val, w * dec + 1.0, r.date)
            lastd[tid] = r.date
    out = {}
    g = {"gf": 1.3, "ppg": 1.3}
    for tid in set(list(gf) + list(ppg)):
        out[tid] = {
            "gf": gf[tid][0] / gf[tid][1] if tid in gf else g["gf"],
            "ga": ga[tid][0] / ga[tid][1] if tid in ga else g["gf"],
            "ppg": ppg[tid][0] / ppg[tid][1] if tid in ppg else g["ppg"],
            "strk": strk[tid][0] / strk[tid][1] if tid in strk else g["ppg"],
        }
    return out, g


def _write_wc_shadow(df, scaler, clf, temperature, prh, pra, out, do_injuries):
    if not WC_PREDS.exists() or not RATINGS.exists():
        out("  (no WC fixtures / ratings -> skipped)");
        pd.DataFrame().to_csv(WC_SHADOW, index=False); return 0
    rat = {int(r.team_id): float(r.strength) for r in pd.read_csv(RATINGS).itertuples()}
    name2id = {str(r.team): int(r.team_id) for r in pd.read_csv(RATINGS).itertuples()}
    feats, _g = _latest_team_features(df)
    # squad quality (WC-only display adjustment): mean of (top-league apps) per team -> z-scored
    squad_z = {}
    if SQUAD.exists():
        sq = pd.read_csv(SQUAD)
        TOP = {"Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"}
        q = sq.assign(top=sq["club_league"].isin(TOP).astype(float)).groupby("team")["top"].mean()
        if len(q):
            mu, sd = q.mean(), q.std() or 1.0
            squad_z = {name2id.get(t): float((v - mu) / sd) for t, v in q.items() if name2id.get(t)}

    wc = pd.read_csv(WC_PREDS)
    rows = []
    for r in wc.itertuples():
        h = name2id.get(str(r.home)); a = name2id.get(str(r.away))
        if h is None or a is None or h not in rat or a not in rat:
            continue
        fh, fa = feats.get(h, {"gf": _g["gf"], "ga": _g["gf"], "ppg": _g["ppg"], "strk": _g["ppg"]}), \
                 feats.get(a, {"gf": _g["gf"], "ga": _g["gf"], "ppg": _g["ppg"], "strk": _g["ppg"]})
        x = np.array([[rat[h] - rat[a], fh["gf"] - fa["gf"], fh["ga"] - fa["ga"],
                       fh["ppg"] - fa["ppg"], fh["strk"] - fa["strk"], 0.0, 0.0, 1.0]])  # neutral, rest=0, h2h=0
        xs = scaler.transform(x)
        pc = _floor_norm(_softmax(clf.decision_function(xs) / temperature))[0]   # smooth + eps-floor
        lh = min(float(prh.predict(xs)[0]), XG_CAP); la = min(float(pra.predict(xs)[0]), XG_CAP)
        sqd = (squad_z.get(h, 0.0) - squad_z.get(a, 0.0))
        rows.append({"fixture_id": int(r.fixture_id), "home": r.home, "away": r.away,
                     "mx_home": round(float(pc[0]), 4), "mx_draw": round(float(pc[1]), 4),
                     "mx_away": round(float(pc[2]), 4), "mx_xg_home": round(lh, 2), "mx_xg_away": round(la, 2),
                     "l3_home": round(float(r.our_home), 4), "l3_draw": round(float(r.our_draw), 4),
                     "l3_away": round(float(r.our_away), 4), "l3_xg_home": float(r.our_xg_home),
                     "l3_xg_away": float(r.our_xg_away), "squad_adj_diff": round(sqd, 3)})
    pd.DataFrame(rows).to_csv(WC_SHADOW, index=False)
    out(f"  WC shadow fixtures written: {len(rows)} (mx_* = shadow; l3_* = shipped; squad_adj_diff = WC-only)")
    if do_injuries:
        out("  [injuries] live layer requested -> see --injuries handler (not run by default; needs API).")
    return len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--injuries", action="store_true", help="(optional) live WC injuries adjust (needs API)")
    a = ap.parse_args()
    main(do_injuries=a.injuries)
