"""
HEAD-TO-HEAD BAKE-OFF (READ-ONLY · NO production · NO API) of three 1X2/goals models for the World
Cup engine, OUT OF SAMPLE on international matches. Question: does ANY model beat the current L3
clearly and significantly, or is L3 the ceiling?

COMMON FRAME (identical for all 3, strict anti-leakage):
  * Same international matches (international_results.csv + the production WALK-FORWARD L3 supremacy
    from national_elo_layer3_permatch.csv = sup_pre_l3, leak-free per match). BURN-IN <2024 to
    train/calibrate, OOS 2024-2025 to evaluate. Same fixtures for the 3 (intersection) -> apples-to-apples.
  * Each model is fit WALK-FORWARD (only data strictly BEFORE each match / block). The final
    ISOTONIC calibration (per class, and per binary OU/BTTS) is fit ONLY on BURN-IN out-of-fold
    predictions, then applied to OOS. Same calibration recipe for the 3.

MODELS:
  1. L3 (champion, reuse as-is): production walk-forward margin-Massey -> sup_pre_l3 (permatch) ->
     margin a0+a1*sup (lstsq on burn-in) -> constant total (burn-in mean) -> Poisson score matrix
     -> isotonic. sup_pre_l3 already includes home advantage for non-neutral (production formula).
  2. DIXON-COLES: per-team attack/defence by weighted Poisson MLE (multiplicative iterative scaling),
     home factor H (only when not neutral), DC low-score tau(rho) correction fit by profile grid.
     Time-decayed, refit walk-forward per block. -> asymmetric lambdas -> tau-corrected score matrix.
  3. ML: sklearn HistGradientBoostingClassifier (multiclass 1X2; binary for Over2.5/BTTS). Leak-free
     walk-forward features (sup_pre_l3, neutral, importance, recent form goal/points rates, recent
     match counts, DC lambdas). Refit per block on prior matches (time-decay sample weights).

ALL THREE share: KMAX=12 Poisson truncation, the same burn-in isotonic calibration, the same OOS set.

OUTPUT (read-only): model_bakeoff_report.txt + model_bakeoff_metrics.csv + model_bakeoff_rows.csv
"""
from __future__ import annotations

import json
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

import national_elo_layer3 as L3   # Isotonic, IMP_BY_TAG, HL_DAYS, MARGIN_CAP, KMAX

try:
    from sklearn.ensemble import HistGradientBoostingClassifier
    HAVE_GBM = True
except Exception:
    HAVE_GBM = False

DATA = HERE / "international_results.csv"
PERMATCH = HERE / "national_elo_layer3_permatch.csv"
REPORT = HERE / "model_bakeoff_report.txt"
METRICS_CSV = HERE / "model_bakeoff_metrics.csv"
ROWS_CSV = HERE / "model_bakeoff_rows.csv"

KMAX = 12
HL = float(L3.HL_DAYS)             # same time-decay half-life as production L3 (730d)
BLOCK_DAYS = 60                    # walk-forward refit cadence for DC and ML (documented)
TRAIN_YEARS = 6.0                  # cap training window (decay makes older negligible)
CAL_START = "2019-01-01"           # burn-in OOF predictions from here (enough for isotonic)
OOS_LO, OOS_HI = "2024-01-01", "2026-01-01"
RES_IDX = {"H": 0, "D": 1, "A": 2}


# ----------------------------- Poisson helpers (shared) -----------------------------
def pmf_vec(lam):
    lam = max(float(lam), 1e-9)
    ks = np.arange(KMAX + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, KMAX + 1)))])
    return np.exp(ks * np.log(lam) - lam - logf)


def score_matrix(lh, la, tau=None):
    M = np.outer(pmf_vec(lh), pmf_vec(la))
    if tau is not None:
        M = M * tau
    M = np.clip(M, 0, None)
    M /= M.sum()
    return M


def matrix_to_markets(M):
    gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
    pH = M[gh > ga].sum(); pD = M[gh == ga].sum(); pA = M[gh < ga].sum()
    tot = gh + ga
    p_over = M[tot >= 3].sum()
    p_btts = M[(gh >= 1) & (ga >= 1)].sum()
    return np.array([pH, pD, pA]), float(p_over), float(p_btts)


def dc_tau(lh, la, rho):
    """Dixon-Coles low-score correction matrix (KMAX+1 square). Only (0,0),(0,1),(1,0),(1,1) differ."""
    T = np.ones((KMAX + 1, KMAX + 1))
    T[0, 0] = 1.0 - lh * la * rho
    T[0, 1] = 1.0 + lh * rho
    T[1, 0] = 1.0 + la * rho
    T[1, 1] = 1.0 - rho
    return np.clip(T, 1e-6, None)


# ----------------------------- Dixon-Coles fit (weighted iterative scaling) -----------------------------
def fit_dixon_coles(hid, aid, gh, ga, neutral, w, iters=60):
    """Multiplicative attack/defence + home factor by weighted Poisson MLE fixed point. Returns
    (A,D dicts by team_id, mu, H). lambda_home = mu*A_h*D_a*H^(1-neutral); lambda_away = mu*A_a*D_h."""
    teams = np.unique(np.concatenate([hid, aid]))
    A = {t: 1.0 for t in teams}; D = {t: 1.0 for t in teams}
    H = 1.3; mu = max(1e-6, (w * (gh + ga)).sum() / (2 * w.sum()))
    nonneu = (neutral == 0)
    for _ in range(iters):
        # accumulate weighted goals for/against and expected denominators
        gf = defaultdict(float); ga_ = defaultdict(float)
        den_a = defaultdict(float); den_d = defaultdict(float)
        Hh = np.where(nonneu, H, 1.0)
        for i in range(len(hid)):
            h, a = hid[i], aid[i]
            gf[h] += w[i] * gh[i]; gf[a] += w[i] * ga[i]
            ga_[h] += w[i] * ga[i]; ga_[a] += w[i] * gh[i]
            # attack denom for team = sum_w mu*D_opp*H(if home&nonneutral)
            den_a[h] += w[i] * mu * D[a] * Hh[i]
            den_a[a] += w[i] * mu * D[h]
            den_d[a] += w[i] * mu * A[h] * Hh[i]   # defence of away faced home attack
            den_d[h] += w[i] * mu * A[a]
        for t in teams:
            if den_a[t] > 0:
                A[t] = gf[t] / den_a[t]
            if den_d[t] > 0:
                D[t] = ga_[t] / den_d[t]
        # renormalise A,D to geomean 1 (identifiability); mu carries the level
        la_ = np.array([A[t] for t in teams]); ld_ = np.array([D[t] for t in teams])
        ca = np.exp(np.mean(np.log(np.clip(la_, 1e-9, None)))); cd = np.exp(np.mean(np.log(np.clip(ld_, 1e-9, None))))
        for t in teams:
            A[t] /= ca; D[t] /= cd
        # update H and mu given A,D
        num_h = (w[nonneu] * gh[nonneu]).sum()
        den_h = sum(w[i] * mu * A[hid[i]] * D[aid[i]] for i in range(len(hid)) if nonneu[i])
        if den_h > 0:
            H = max(1.0, num_h / den_h)
        exp_goals = 0.0
        for i in range(len(hid)):
            exp_goals += w[i] * (A[hid[i]] * D[aid[i]] * (H if nonneu[i] else 1.0) + A[aid[i]] * D[hid[i]])
        if exp_goals > 0:
            mu = (w * (gh + ga)).sum() / exp_goals
    return A, D, mu, H


def fit_rho(hid, aid, gh, ga, neutral, w, A, D, mu, H, grid=np.linspace(-0.18, 0.18, 19)):
    """Profile-likelihood grid for the DC rho on the SAME weighted prior data."""
    nonneu = (neutral == 0)
    lh = np.array([mu * A[hid[i]] * D[aid[i]] * (H if nonneu[i] else 1.0) for i in range(len(hid))])
    la = np.array([mu * A[aid[i]] * D[hid[i]] for i in range(len(hid))])
    gh_i = gh.astype(int); ga_i = ga.astype(int)
    best, brho = -1e18, 0.0
    for rho in grid:
        # tau only for the four low-score cells
        tau = np.ones(len(hid))
        m00 = (gh_i == 0) & (ga_i == 0); m01 = (gh_i == 0) & (ga_i == 1)
        m10 = (gh_i == 1) & (ga_i == 0); m11 = (gh_i == 1) & (ga_i == 1)
        tau[m00] = 1 - lh[m00] * la[m00] * rho
        tau[m01] = 1 + lh[m01] * rho
        tau[m10] = 1 + la[m10] * rho
        tau[m11] = 1 - rho
        if np.any(tau <= 0):
            continue
        ll = (w * np.log(tau)).sum()   # only the tau part varies with rho (Poisson part fixed)
        if ll > best:
            best, brho = ll, rho
    return float(brho)


# ----------------------------- recent-form features (leak-free) -----------------------------
def build_form(ir):
    """Per match: each team's rolling goals-for/against rate & points rate over last 10 prior
    internationals, and #matches in prior 365d. Strictly date<match (leak-free)."""
    rec = defaultdict(list)   # tid -> list of (date, gf, ga, pts)
    feats = {}
    for r in ir.itertuples(index=False):
        d = r.date
        out = {}
        for tid, gf, ga, opp_gf in ((int(r.home_id), r.gh, r.ga, r.ga), (int(r.away_id), r.ga, r.gh, r.gh)):
            hist = rec[tid]
            last = hist[-10:]
            if last:
                gfr = np.mean([h[1] for h in last]); gar = np.mean([h[2] for h in last])
                ptr = np.mean([h[3] for h in last])
            else:
                gfr = gar = 1.0; ptr = 1.0
            n365 = sum(1 for h in hist if (d - h[0]).days <= 365)
            side = "home" if tid == int(r.home_id) else "away"
            out[side] = (gfr, gar, ptr, n365)
        feats[int(r.fixture_id)] = out
        # append AFTER computing (leak-free)
        ph = 3 if r.gh > r.ga else (1 if r.gh == r.ga else 0)
        pa = 3 if r.ga > r.gh else (1 if r.gh == r.ga else 0)
        rec[int(r.home_id)].append((d, r.gh, r.ga, ph))
        rec[int(r.away_id)].append((d, r.ga, r.gh, pa))
    return feats


# ----------------------------- calibration & scoring -----------------------------
def cal_multiclass(raw_burn, Yb, raw_oos):
    isos = [L3.Isotonic().fit(raw_burn[:, k], Yb[:, k]) for k in range(3)]
    P = np.column_stack([isos[k].predict(raw_oos[:, k]) for k in range(3)])
    P = np.clip(P, 1e-6, None); P /= P.sum(1, keepdims=True)
    return P


def cal_binary(p_burn, y_burn, p_oos):
    iso = L3.Isotonic().fit(p_burn, y_burn)
    p = np.clip(iso.predict(p_oos), 1e-6, 1 - 1e-6)
    return p


def ll_multi(P, Y):
    Pc = np.clip(P, 1e-15, 1.0); Pc /= Pc.sum(1, keepdims=True)
    return -np.sum(Y * np.log(Pc), axis=1)


def br_multi(P, Y):
    Pc = np.clip(P, 1e-15, 1.0); Pc /= Pc.sum(1, keepdims=True)
    return np.sum((Pc - Y) ** 2, axis=1)


def ece_multi(P, Y, bins=10):
    conf = P.max(1); corr = (P.argmax(1) == Y.argmax(1)).astype(float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(P) * abs(conf[m].mean() - corr[m].mean())
    return float(e)


def ll_bin(p, y):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def br_bin(p, y):
    return (p - y) ** 2


def paired_boot(d, seed=20260626, nb=20000):
    rng = np.random.RandomState(seed)
    idx = rng.randint(0, len(d), (nb, len(d)))
    bd = d[idx].mean(1)
    return float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5)), float((bd > 0).mean())


# ----------------------------- main -----------------------------
def run():
    ir = pd.read_csv(DATA)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
    ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
    ir["home_id"] = ir["home_id"].astype(int); ir["away_id"] = ir["away_id"].astype(int)
    ir["neutral"] = ir["neutral"].astype(int)
    ir = ir.sort_values("date").reset_index(drop=True)

    pm = pd.read_csv(PERMATCH)
    pm["date"] = pd.to_datetime(pm["date"], errors="coerce")
    sup_by_fid = {int(r.fixture_id): float(r.sup_pre_l3) for r in pm.itertuples(index=False)
                  if pd.notna(r.sup_pre_l3)}

    feats = build_form(ir)
    imp = {t: L3.IMP_BY_TAG.get(t, 0.8) for t in ir["league_tag"].unique()}

    # only matches we can feature: have sup_pre_l3 and date >= CAL_START
    ir = ir[ir["date"] >= pd.Timestamp(CAL_START)].copy()
    ir = ir[ir["fixture_id"].map(lambda f: int(f) in sup_by_fid)].reset_index(drop=True)
    ir["sup"] = ir["fixture_id"].map(lambda f: sup_by_fid[int(f)])

    arr = {c: ir[c].to_numpy() for c in ("home_id", "away_id", "gh", "ga", "neutral")}
    dates = ir["date"].to_numpy()
    tags = ir["league_tag"].to_numpy()
    fids = ir["fixture_id"].to_numpy().astype(int)
    sup = ir["sup"].to_numpy(float)
    n = len(ir)
    res = np.where(arr["gh"] > arr["ga"], 0, np.where(arr["gh"] == arr["ga"], 1, 2))

    # ---- walk-forward blocks: DC ratings + ML model fit on prior data, predict the block ----
    dc_lh = np.full(n, np.nan); dc_la = np.full(n, np.nan); dc_rho = np.full(n, np.nan)
    ml_raw = np.full((n, 3), np.nan)
    ml_over = np.full(n, np.nan); ml_btts = np.full(n, np.nan)

    # feature matrix (leak-free per match). cols 0-10 set now; cols 11,12 = DC lambdas filled per
    # match in its own walk-forward block (NaN until then; HistGBM handles NaN natively).
    Xrows = np.full((n, 13), np.nan)
    for i in range(n):
        fo = feats[fids[i]]
        h = fo.get("home", (1, 1, 1, 0)); a = fo.get("away", (1, 1, 1, 0))
        Xrows[i, 0:11] = [sup[i], arr["neutral"][i], imp.get(tags[i], 0.8),
                          h[0], h[1], h[2], a[0], a[1], a[2], h[3], a[3]]

    block_start = pd.Timestamp(CAL_START)
    last_date = ir["date"].max()
    n_blocks = 0
    while block_start <= last_date:
        bs = np.datetime64(block_start)
        be = np.datetime64(block_start + pd.Timedelta(days=BLOCK_DAYS))
        prior = (dates < bs) & (dates >= np.datetime64(block_start - pd.Timedelta(days=int(TRAIN_YEARS * 365))))
        blk = (dates >= bs) & (dates < be)
        if blk.sum() == 0:
            block_start += pd.Timedelta(days=BLOCK_DAYS); continue
        if prior.sum() >= 300:
            age = (bs - dates[prior]) / np.timedelta64(1, "D")
            w = np.array([imp.get(t, 0.8) for t in tags[prior]]) * np.exp(-np.log(2) * age / HL)
            # DC fit
            A, D, mu, H = fit_dixon_coles(arr["home_id"][prior], arr["away_id"][prior],
                                          arr["gh"][prior].astype(float), arr["ga"][prior].astype(float),
                                          arr["neutral"][prior], w)
            rho = fit_rho(arr["home_id"][prior], arr["away_id"][prior],
                          arr["gh"][prior].astype(float), arr["ga"][prior].astype(float),
                          arr["neutral"][prior], w, A, D, mu, H)
            # DC predict block
            for i in np.where(blk)[0]:
                h, a, neu = arr["home_id"][i], arr["away_id"][i], arr["neutral"][i]
                if h in A and a in A:
                    lh = mu * A[h] * D[a] * (H if neu == 0 else 1.0)
                    la = mu * A[a] * D[h]
                    dc_lh[i], dc_la[i], dc_rho[i] = lh, la, rho
                    Xrows[i, 11] = lh; Xrows[i, 12] = la   # DC lambdas as ML features (separate cols)
            # ML fit (multiclass 1X2 + binary over/btts) on prior, predict block
            if HAVE_GBM:
                # ML features = cols 0-10 (sup_L3, neutral, imp, form rates, recent counts). DC
                # lambdas (cols 11,12) are NOT fed to the ML (avoids ML<-DC coupling and the
                # all-NaN-early-column binning failure). sup_pre_l3 already carries the L3 signal.
                Xp = Xrows[prior][:, :11]; yp = res[prior]
                over_p = ((arr["gh"][prior] + arr["ga"][prior]) >= 3).astype(int)
                btts_p = ((arr["gh"][prior] >= 1) & (arr["ga"][prior] >= 1)).astype(int)
                clf = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=0.05,
                                                     l2_regularization=1.0, min_samples_leaf=40)
                clf.fit(Xp, yp, sample_weight=w)
                cls = list(clf.classes_)
                proba = clf.predict_proba(Xrows[blk][:, :11])
                P = np.zeros((blk.sum(), 3))
                for j, c in enumerate(cls):
                    P[:, c] = proba[:, j]
                ml_raw[blk] = P
                for stat, store, yv in (("over", ml_over, over_p), ("btts", ml_btts, btts_p)):
                    cb = HistGradientBoostingClassifier(max_depth=3, max_iter=200, learning_rate=0.05,
                                                        l2_regularization=1.0, min_samples_leaf=40)
                    cb.fit(Xp, yv, sample_weight=w)
                    pp = cb.predict_proba(Xrows[blk][:, :11])
                    store[blk] = pp[:, list(cb.classes_).index(1)] if 1 in cb.classes_ else 0.0
            n_blocks += 1
        block_start += pd.Timedelta(days=BLOCK_DAYS)

    # ---- L3 model: margin lstsq on burn-in, Poisson; isotonic later (shared) ----
    burn = (dates >= np.datetime64(CAL_START)) & (dates < np.datetime64(OOS_LO))
    oos = (dates >= np.datetime64(OOS_LO)) & (dates < np.datetime64(OOS_HI))
    ghf = arr["gh"].astype(float); gaf = arr["ga"].astype(float)
    Ab = np.c_[np.ones(burn.sum()), sup[burn]]
    a0a1, *_ = np.linalg.lstsq(Ab, (ghf - gaf)[burn], rcond=None)
    a0, a1 = float(a0a1[0]), float(a0a1[1])
    total_const = float((ghf + gaf)[burn].mean())
    # PRODUCTION L3 total = MATCHUP (forma b): total = tb0+tb1|sup|+tb2 sup^2 (lstsq/burn-in), capped
    # at TOTAL_CAP. The shipped engine uses this (not the constant) -> the L3 baseline here must too,
    # else the goals comparison would handicap L3 unfairly. 1X2 is unaffected (depends on the margin).
    import l3_offline  # noqa: E402  (TOTAL_CAP only; no API on import)
    sb = sup[burn]
    tcoef, *_ = np.linalg.lstsq(np.c_[np.ones(len(sb)), np.abs(sb), sb ** 2], (ghf + gaf)[burn], rcond=None)
    tb0, tb1, tb2 = (float(tcoef[0]), float(tcoef[1]), float(tcoef[2]))
    TCAP = float(l3_offline.TOTAL_CAP)

    def l3_total(s):
        return min(tb0 + tb1 * abs(s) + tb2 * s * s, TCAP)

    def l3_raw_markets(idx, matchup=True):
        out_p = np.zeros((len(idx), 3)); out_o = np.zeros(len(idx)); out_b = np.zeros(len(idx))
        for j, i in enumerate(idx):
            margin = a0 + a1 * sup[i]
            total = l3_total(sup[i]) if matchup else total_const
            lh = max(0.05, (total + margin) / 2.0); la = max(0.05, (total - margin) / 2.0)
            P, po, pb = matrix_to_markets(score_matrix(lh, la))
            out_p[j] = P; out_o[j] = po; out_b[j] = pb
        return out_p, out_o, out_b

    def dc_raw_markets(idx):
        out_p = np.zeros((len(idx), 3)); out_o = np.zeros(len(idx)); out_b = np.zeros(len(idx))
        for j, i in enumerate(idx):
            lh, la, rho = dc_lh[i], dc_la[i], dc_rho[i]
            P, po, pb = matrix_to_markets(score_matrix(lh, la, dc_tau(lh, la, rho)))
            out_p[j] = P; out_o[j] = po; out_b[j] = pb
        return out_p, out_o, out_b

    # rows where ALL models have predictions (apples-to-apples intersection)
    have_dc = np.isfinite(dc_lh)
    have_ml = np.isfinite(ml_raw).all(1) if HAVE_GBM else np.ones(n, bool)
    usable = have_dc & have_ml
    burn_u = np.where(burn & usable)[0]; oos_u = np.where(oos & usable)[0]
    Yb = np.eye(3)[res[burn_u]]; Yo = np.eye(3)[res[oos_u]]
    over_b = ((ghf + gaf)[burn_u] >= 3).astype(int); over_o = ((ghf + gaf)[oos_u] >= 3).astype(int)
    btts_b = ((ghf[burn_u] >= 1) & (gaf[burn_u] >= 1)).astype(int)
    btts_o = ((ghf[oos_u] >= 1) & (gaf[oos_u] >= 1)).astype(int)

    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 104)
    out("BAKE-OFF OOS · L3 (campeón) vs DIXON-COLES vs ML(GBM) — 1X2 y goles · READ-ONLY · sin API · sin producción")
    out("=" * 104)
    out(f"ML learner: {'sklearn HistGradientBoostingClassifier' if HAVE_GBM else 'NO sklearn -> ML omitido'}")
    out(f"bloques walk-forward (refit DC/ML cada {BLOCK_DAYS}d, ventana {TRAIN_YEARS}a, HL={HL:.0f}d): {n_blocks}")
    out(f"partidos USABLES (los 3 con predicción): burn-in {len(burn_u)} | OOS 2024-2025 {len(oos_u)}")
    out(f"L3 margin: a0={a0:+.4f} a1={a1:.4f} total_const={total_const:.3f} (lstsq/burn-in)")
    out(f"DC rho (último bloque)≈{np.nanmedian(dc_rho[oos_u]):+.3f} (mediana OOS)")
    out("")

    # build calibrated OOS predictions per model
    models = {}
    l3_b = l3_raw_markets(burn_u, matchup=True); l3_o = l3_raw_markets(oos_u, matchup=True)
    l3c_b = l3_raw_markets(burn_u, matchup=False); l3c_o = l3_raw_markets(oos_u, matchup=False)
    dc_b = dc_raw_markets(burn_u); dc_o = dc_raw_markets(oos_u)
    models["L3"] = (cal_multiclass(l3_b[0], Yb, l3_o[0]),
                    cal_binary(l3_b[1], over_b, l3_o[1]), cal_binary(l3_b[2], btts_b, l3_o[2]))
    models["L3_const"] = (cal_multiclass(l3c_b[0], Yb, l3c_o[0]),
                          cal_binary(l3c_b[1], over_b, l3c_o[1]), cal_binary(l3c_b[2], btts_b, l3c_o[2]))
    models["DixonColes"] = (cal_multiclass(dc_b[0], Yb, dc_o[0]),
                            cal_binary(dc_b[1], over_b, dc_o[1]), cal_binary(dc_b[2], btts_b, dc_o[2]))
    if HAVE_GBM:
        models["ML_GBM"] = (cal_multiclass(ml_raw[burn_u], Yb, ml_raw[oos_u]),
                            cal_binary(ml_over[burn_u], over_b, ml_over[oos_u]),
                            cal_binary(ml_btts[burn_u], btts_b, ml_btts[oos_u]))

    # ---- 1X2 table ----
    out("-" * 104)
    out("1X2 (H/D/A) OOS — calibración isotónica en burn-in para los 3")
    out("-" * 104)
    out(f"  {'modelo':12} {'logloss':>9} {'brier':>8} {'ECE':>7} {'acc%':>6}   {'Δlogloss vs L3 (IC95%, paired boot)':>44}")
    metrics = []
    base_ll = ll_multi(models["L3"][0], Yo)
    for name, (P, _po, _pb) in models.items():
        llv = ll_multi(P, Yo); brv = br_multi(P, Yo)
        ll = llv.mean(); br = brv.mean(); ece = ece_multi(P, Yo); acc = float((P.argmax(1) == res[oos_u]).mean())
        if name == "L3":
            sigtxt = "(campeón ref)"
        else:
            d = base_ll - llv   # >0 = este modelo mejor que L3
            lo, hi, p = paired_boot(d)
            sigtxt = f"Δ={d.mean():+.5f} [{lo:+.5f},{hi:+.5f}] {'BATE' if lo>0 else ('PEOR' if hi<0 else 'no signif')}"
        out(f"  {name:12} {ll:>9.5f} {br:>8.5f} {ece:>7.4f} {acc*100:>5.1f}%   {sigtxt:>44}")
        metrics.append({"market": "1x2", "model": name, "n": len(oos_u), "logloss": ll, "brier": br,
                        "ece": ece, "acc": acc})
    out("")

    # ---- goals: Over2.5 & BTTS ----
    for mk, yo, idxcol in (("Over2.5", over_o, 1), ("BTTS", btts_o, 2)):
        out("-" * 104)
        out(f"{mk} (binario) OOS — calibración isotónica en burn-in")
        out("-" * 104)
        out(f"  real {mk}={yo.mean()*100:.0f}%   {'modelo':12} {'logloss':>9} {'brier':>8}   {'Δlogloss vs L3 (IC95%)':>40}")
        base = ll_bin(models["L3"][idxcol], yo)
        for name, tup in models.items():
            p = tup[idxcol]
            ll = ll_bin(p, yo); br = br_bin(p, yo)
            if name == "L3":
                sigtxt = "(campeón ref)"
            else:
                d = base - ll
                lo, hi, _p = paired_boot(d)
                sigtxt = f"Δ={d.mean():+.5f} [{lo:+.5f},{hi:+.5f}] {'BATE' if lo>0 else ('PEOR' if hi<0 else 'no signif')}"
            out(f"  {'':16} {name:12} {ll.mean():>9.5f} {br.mean():>8.5f}   {sigtxt:>40}")
            metrics.append({"market": mk, "model": name, "n": len(oos_u),
                            "logloss": float(ll.mean()), "brier": float(br.mean()), "ece": np.nan, "acc": np.nan})
        out("")

    out("=" * 104)
    out("LECTURA: 'BATE' = IC95% de Δlogloss(L3−modelo) EXCLUYE 0 con media>0 (mejora clara y significativa).")
    out("Si todos los IC incluyen 0 (o son PEOR), L3 es el techo en ese mercado.")
    out("=" * 104)

    pd.DataFrame(metrics).to_csv(METRICS_CSV, index=False)
    rows_out = ir.iloc[oos_u][["fixture_id", "date", "home", "away", "neutral", "gh", "ga"]].copy()
    rows_out["res"] = pd.Series(res[oos_u], index=rows_out.index).map({0: "H", 1: "D", 2: "A"})
    for name, (P, po, pb) in models.items():
        rows_out[f"{name}_H"] = P[:, 0]; rows_out[f"{name}_D"] = P[:, 1]; rows_out[f"{name}_A"] = P[:, 2]
        rows_out[f"{name}_over25"] = po; rows_out[f"{name}_btts"] = pb
    rows_out.to_csv(ROWS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}\nWritten: {ROWS_CSV}")


if __name__ == "__main__":
    run()
