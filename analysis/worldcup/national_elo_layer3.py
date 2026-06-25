"""
LAYER 3 - continuous strength-of-schedule rating (replaces Layer-2's blunt
confederation offset). Offline, NO API (reads international_results.csv),
NO production, NO .env, NO git.

Problem (Layer 2): the per-confederation offset over-boosts CONMEBOL (Argentina)
and penalises strong members of weak confederations (Canada). Fix: connect the Elo
graph properly. Instead of an online Elo + bloc offset, fit a WEIGHTED RIDGE MASSEY
margin rating over the WHOLE connected graph (one strength per team, joint least
squares = the fixed point of iterative rating passes), where cross-confederation
matches (WC, intercontinental play-offs, inter-conf friendlies) are heavily up-
weighted so every team is calibrated against REAL opposition strength.

Kept from Layer 2: isotonic calibration (helped). Dropped: experience shrinkage
(hurt); ridge regularisation handles thin teams correctly instead.

Walk-forward: refit the rating every REFIT_DAYS on all prior matches (time-decayed);
predict each match pre-fit. Calibrate isotonic on burn-in, validate OOS vs L2.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from api_football_client import APIFootballClient  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
DATA = OUT_DIR / "international_results.csv"
EPS = 1e-15
KMAX = 12
OOS_CUTOFF = "2024-01-01"
import os
HL_DAYS = float(os.environ.get("L3_HL", 730.0))          # national-team strength is slow-moving
REFIT_DAYS = 30
XCONF_MULT = float(os.environ.get("L3_XCONF", 3.0))      # up-weight cross-confederation matches
MARGIN_CAP = 4.0
LAM = float(os.environ.get("L3_LAM", 6.0))               # ridge toward mean (tuned: 12 over-compressed)
HFA_GOALS_PRIOR = 0.0    # home adv fit jointly; neutral matches carry none
MIN_PAST = 300

IMP_BY_TAG = {
    "Friendlies": 0.6, "EAFF": 0.6, "ASEAN": 0.6, "SAFF": 0.6, "COSAFA": 0.6, "BalticCup": 0.6,
    "GulfCup": 0.7, "OFC_NationsCup": 0.7, "ArabCup": 0.8, "UNL": 1.0, "CONCACAF_NL": 1.0,
    "WCQ_Europe": 1.1, "WCQ_Asia": 1.1, "WCQ_Africa": 1.1, "WCQ_CONCACAF": 1.1, "WCQ_SA": 1.1,
    "WCQ_Oceania": 1.0, "WCQ_ICPlayoff": 1.6, "AFCONQ": 1.0, "AsianCupQ": 1.0, "Euro": 1.4,
    "AFCON": 1.3, "AsianCup": 1.3, "CopaAmerica": 1.4, "GoldCup": 1.2, "ConfedCup": 1.3, "WC": 1.6,
}
TAG2CONF = {
    "WCQ_Europe": "UEFA", "Euro": "UEFA", "UNL": "UEFA", "BalticCup": "UEFA",
    "WCQ_Asia": "AFC", "AsianCup": "AFC", "AsianCupQ": "AFC", "EAFF": "AFC", "ASEAN": "AFC",
    "SAFF": "AFC", "GulfCup": "AFC", "WCQ_Africa": "CAF", "AFCON": "CAF", "AFCONQ": "CAF",
    "COSAFA": "CAF", "WCQ_SA": "CONMEBOL", "CopaAmerica": "CONMEBOL", "WCQ_CONCACAF": "CONCACAF",
    "GoldCup": "CONCACAF", "CONCACAF_NL": "CONCACAF", "WCQ_Oceania": "OFC", "OFC_NationsCup": "OFC",
}


def logloss_mc(P, Y):
    return float(-np.mean(np.sum(Y * np.log(np.clip(P, EPS, 1.0)), axis=1)))


def brier_mc(P, Y):
    return float(np.mean(np.sum((P - Y) ** 2, axis=1)))


def acc_mc(P, Y):
    return float(np.mean(P.argmax(1) == Y.argmax(1)))


def ece_mc(P, Y, bins=10):
    conf = P.max(1); corr = (P.argmax(1) == Y.argmax(1)).astype(float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(P) * abs(conf[m].mean() - corr[m].mean())
    return float(e)


def pmf(lam, k=KMAX):
    ks = np.arange(k + 1)
    logf = np.concatenate([[0.0], np.cumsum(np.log(np.arange(1, k + 1)))])
    return np.exp(ks * np.log(max(lam, 1e-9)) - lam - logf)


def wdl(lh, la):
    M = np.outer(pmf(lh), pmf(la)); M /= M.sum()
    gh = np.arange(KMAX + 1)[:, None]; ga = np.arange(KMAX + 1)[None, :]
    return np.array([M[gh > ga].sum(), M[gh == ga].sum(), M[gh < ga].sum()])


def _pava(y, w):
    lvl, wt, cnt = [], [], []
    for i in range(len(y)):
        lvl.append(float(y[i])); wt.append(float(w[i])); cnt.append(1)
        while len(lvl) > 1 and lvl[-2] > lvl[-1]:
            v2, w2, c2 = lvl.pop(), wt.pop(), cnt.pop()
            v1, w1, c1 = lvl.pop(), wt.pop(), cnt.pop()
            lvl.append((v1 * w1 + v2 * w2) / (w1 + w2)); wt.append(w1 + w2); cnt.append(c1 + c2)
    out = np.empty(len(y)); idx = 0
    for v, cc in zip(lvl, cnt):
        out[idx:idx + cc] = v; idx += cc
    return out


class Isotonic:
    def fit(self, p, y):
        p = np.asarray(p, float); y = np.asarray(y, float)
        o = np.argsort(p, kind="mergesort"); ps, ys = p[o], y[o]
        f = _pava(ys, np.ones_like(ys)); ux, uf, i = [], [], 0
        while i < len(ps):
            j = i
            while j + 1 < len(ps) and ps[j + 1] == ps[i]:
                j += 1
            ux.append(ps[i]); uf.append(f[i:j + 1].mean()); i = j + 1
        self.ux = np.array(ux); self.uf = np.array(uf); return self

    def predict(self, p):
        return np.interp(np.asarray(p, float), self.ux, self.uf)


def fit_rating(hid, aid, neutral, y, w):
    """Weighted ridge Massey margin rating. Returns dict team->strength, home_adv."""
    teams = np.unique(np.concatenate([hid, aid]))
    loc = {t: i for i, t in enumerate(teams)}
    nt = len(teams)
    hl = np.array([loc[t] for t in hid]); al = np.array([loc[t] for t in aid])
    c = nt  # home-adv column
    M = np.zeros((nt + 1, nt + 1)); b = np.zeros(nt + 1)
    np.add.at(M, (hl, hl), w); np.add.at(M, (al, al), w)
    np.add.at(M, (hl, al), -w); np.add.at(M, (al, hl), -w)
    wh = w * (1 - neutral)
    np.add.at(M, (hl, c), wh); np.add.at(M, (c, hl), wh)
    np.add.at(M, (al, c), -wh); np.add.at(M, (c, al), -wh)
    M[c, c] += wh.sum()
    np.add.at(b, hl, w * y); np.add.at(b, al, -w * y); b[c] += np.sum(wh * y)
    M[np.arange(nt), np.arange(nt)] += LAM
    theta = np.linalg.solve(M, b)
    return {t: theta[loc[t]] for t in teams}, float(theta[c])


def main():
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).sort_values("date").reset_index(drop=True)
    df["home_id"] = df["home_id"].astype(int); df["away_id"] = df["away_id"].astype(int)
    n = len(df)
    report = []

    def out(s=""):
        print(s); report.append(s)

    # confederation (for cross-conf weighting only)
    votes = {}
    for _, r in df.iterrows():
        cf = TAG2CONF.get(r["league_tag"])
        if cf:
            for tid in (r["home_id"], r["away_id"]):
                votes.setdefault(tid, Counter())[cf] += 1
    conf = {tid: cc.most_common(1)[0][0] for tid, cc in votes.items()}

    hid = df["home_id"].to_numpy(); aid = df["away_id"].to_numpy()
    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    neutral = df["neutral"].to_numpy(int); tags = df["league_tag"].to_numpy()
    dates = df["date"].to_numpy()
    days = (dates - dates.min()) / np.timedelta64(1, "D")
    margin = np.clip(gh - ga, -MARGIN_CAP, MARGIN_CAP)
    imp = np.array([IMP_BY_TAG.get(t, 0.8) for t in tags])
    xconf = np.array([XCONF_MULT if (conf.get(hid[i]) and conf.get(aid[i]) and conf[hid[i]] != conf[aid[i]])
                      else 1.0 for i in range(n)])
    base_w = imp * xconf

    is_oos = dates >= np.datetime64(OOS_CUTOFF); burn = ~is_oos
    res = np.where(gh > ga, 0, np.where(gh == ga, 1, 2)); Y = np.eye(3)[res]

    out("=" * 96)
    out("LAYER 3 - continuous strength-of-schedule rating (weighted ridge Massey, cross-conf up-weight)")
    out("=" * 96)
    out(f"matches={n} | burn-in={int(burn.sum())} | OOS={int(is_oos.sum())} | "
        f"HL={HL_DAYS:.0f}d refit={REFIT_DAYS}d xconf_w={XCONF_MULT} ridge={LAM}")
    out("")

    # ---- walk-forward: refit every REFIT_DAYS on prior matches (time-decayed) ----
    sup_pre = np.full(n, np.nan)
    last_fit_day = None
    cur_s, cur_h = None, 0.0
    n_refits = 0
    for i in range(n):
        if cur_s is None or (days[i] - last_fit_day) >= REFIT_DAYS:
            pm = days < days[i]
            if pm.sum() >= MIN_PAST:
                w = base_w[pm] * np.exp(-np.log(2) * (days[i] - days[pm]) / HL_DAYS)
                cur_s, cur_h = fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
                last_fit_day = days[i]; n_refits += 1
        if cur_s is not None:
            sh = cur_s.get(hid[i], 0.0); sa = cur_s.get(aid[i], 0.0)
            sup_pre[i] = (sh - sa) + (cur_h if neutral[i] == 0 else 0.0)
    out(f"refits={n_refits} | matches with a rating={int(np.isfinite(sup_pre).sum())}")
    # dump per-match walk-forward L3 supremacy (leak-free) for downstream blends
    pd.DataFrame({"fixture_id": df["fixture_id"], "date": df["date"], "home_id": hid, "away_id": aid,
                  "sup_pre_l3": sup_pre, "gh": gh, "ga": ga, "res": res,
                  "is_oos": is_oos.astype(int)}).to_csv(OUT_DIR / "national_elo_layer3_permatch.csv", index=False)

    # ---- supremacy scaling + total, fit on burn-in only ----
    ok = np.isfinite(sup_pre)
    bturn = burn & ok
    A = np.c_[np.ones(bturn.sum()), sup_pre[bturn]]
    coef, *_ = np.linalg.lstsq(A, (gh - ga)[bturn], rcond=None)
    a0, a1 = float(coef[0]), float(coef[1])
    total_mean = float(np.mean((gh + ga)[bturn]))
    out(f"burn-in calibration: total={total_mean:.3f} | margin = {a0:+.3f} + {a1:.3f}*raw_sup")
    out("")

    def probs(sup):
        s = a0 + a1 * sup
        lh = max(0.05, (total_mean + s) / 2.0); la = max(0.05, (total_mean - s) / 2.0)
        return wdl(lh, la), lh, la

    P3 = np.zeros((n, 3))
    for i in range(n):
        if ok[i]:
            P3[i] = probs(sup_pre[i])[0]
    P3[~ok] = np.array([0.45, 0.27, 0.28])  # fallback (rare, early matches)
    P3 /= P3.sum(1, keepdims=True)

    # ---- isotonic calibration (fit on burn-in) ----
    isos = [Isotonic().fit(P3[bturn, k], Y[bturn, k]) for k in range(3)]
    P3c = np.c_[isos[0].predict(P3[:, 0]), isos[1].predict(P3[:, 1]), isos[2].predict(P3[:, 2])]
    P3c = np.clip(P3c, 1e-6, None); P3c /= P3c.sum(1, keepdims=True)

    # base-rate
    base = np.bincount(res[burn], minlength=3) / burn.sum()
    Pbase = np.tile(base, (n, 1))

    # ---- validation OOS vs Layer 2 (read its CSV) ----
    oo = is_oos & ok
    out("-" * 96)
    out("VALIDATION OOS - Layer 3 vs base-rate (and Layer-2 reference from its CSV)")
    out("-" * 96)
    rows = []
    base_ll = logloss_mc(Pbase[oo], Y[oo])
    for name, P in [("base_rate", Pbase), ("L3_raw", P3), ("L3+calib (SHIPPED)", P3c)]:
        ll = logloss_mc(P[oo], Y[oo])
        rows.append({"model": name, "logloss": round(ll, 5), "brier": round(brier_mc(P[oo], Y[oo]), 5),
                     "acc": round(acc_mc(P[oo], Y[oo]), 4), "ECE": round(ece_mc(P[oo], Y[oo]), 4),
                     "ll_lift_vs_base%": round(100 * (base_ll - ll) / base_ll, 2)})
    l2csv = OUT_DIR / "national_elo_layer2_validation.csv"
    if l2csv.exists():
        l2 = pd.read_csv(l2csv)
        for key in ["L1_elo", "+conf (SHIPPED)", "+conf+calib"]:
            r = l2[l2["model"] == key]
            if len(r):
                rr = r.iloc[0]
                rows.append({"model": f"[L2] {key}", "logloss": rr["logloss"], "brier": rr["brier"],
                             "acc": rr["acc"], "ECE": rr["ECE"], "ll_lift_vs_base%": rr["ll_lift_vs_base%"]})
    vt = pd.DataFrame(rows)
    out(vt.to_string(index=False))
    out("  (NOTE: L3 OOS rows where a rating exists; same OOS window as L2.)")
    out("")

    # ---- top current ratings (sanity) ----
    pm = days < days.max() + 1
    w = base_w[pm] * np.exp(-np.log(2) * (days.max() - days[pm]) / HL_DAYS)
    s_final, h_final = fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
    name_by_id = {}
    for _, r in df.iterrows():
        name_by_id[int(r["home_id"])] = r["home"]; name_by_id[int(r["away_id"])] = r["away"]
    top = sorted(s_final.items(), key=lambda kv: -kv[1])[:15]
    out("-" * 96)
    out(f"TOP 15 current strength ratings (goals vs avg; home_adv={h_final:+.2f})")
    out("-" * 96)
    for tid, s in top:
        out(f"  {name_by_id.get(tid, tid):24s} {s:+.2f}")
    out("")

    # ---- WC predictions L3, compare to L2 + market on outlier cases ----
    l2_pred = {}
    pred_path = OUT_DIR / "worldcup_our_model_predictions.csv"
    l2_snap = OUT_DIR / "worldcup_l2_predictions.csv"  # dedicated L2 snapshot (not the shared file)
    if l2_snap.exists():
        for _, r in pd.read_csv(l2_snap).iterrows():
            l2_pred[int(r["fixture_id"])] = (r["our_home"], r["our_away"])
    mkt = {}
    cards_csv = OUT_DIR / "worldcup_cards.csv"
    if cards_csv.exists():
        for _, r in pd.read_csv(cards_csv).iterrows():
            if pd.notna(r.get("mkt_home")):
                mkt[int(r["fixture_id"])] = (r["mkt_home"], r["mkt_away"])

    c = APIFootballClient()
    wc = c.fixtures(league=1, season=2026).get("response", []) or []
    preds, comp = [], []
    for f in wc:
        if (f.get("fixture", {}).get("status") or {}).get("short") != "NS":
            continue
        h = f.get("teams", {}).get("home") or {}; a = f.get("teams", {}).get("away") or {}
        if h.get("id") is None or a.get("id") is None:
            continue
        hidd, aidd = int(h["id"]), int(a["id"])
        sup = s_final.get(hidd, 0.0) - s_final.get(aidd, 0.0)  # WC neutral, no HFA
        P, lh, la = probs(sup)
        P = P / P.sum()
        pc = np.array([isos[0].predict([P[0]])[0], isos[1].predict([P[1]])[0], isos[2].predict([P[2]])[0]])
        pc = np.clip(pc, 1e-6, None); pc = pc / pc.sum()
        fid = f["fixture"]["id"]
        preds.append({"fixture_id": fid, "home": h.get("name"), "away": a.get("name"),
                      "our_elo_home": round(s_final.get(hidd, 0.0), 2), "our_elo_away": round(s_final.get(aidd, 0.0), 2),
                      "our_home": round(float(pc[0]), 4), "our_draw": round(float(pc[1]), 4),
                      "our_away": round(float(pc[2]), 4), "our_xg_home": round(lh, 2), "our_xg_away": round(la, 2)})
        if fid in mkt and fid in l2_pred:
            comp.append((h.get("name"), a.get("name"), mkt[fid], l2_pred[fid], (pc[0], pc[2])))

    out("-" * 96)
    out("OUTLIER CASES: home-win % (and away) — market vs L2 vs L3")
    out("-" * 96)
    out(f"  {'match':32s} {'mkt_H/A':>13} {'L2_H/A':>13} {'L3_H/A':>13}")
    focus = ["Canada", "Argentina", "Uzbekistan", "Ghana", "Austria", "France", "Portugal", "Mexico", "USA"]
    shown = 0
    for hn, an, mk, l2p, l3p in comp:
        if any(k in hn or k in an for k in focus):
            out(f"  {hn+' vs '+an:32s} "
                f"{mk[0]*100:5.0f}/{mk[1]*100:<4.0f}  {l2p[0]*100:5.0f}/{l2p[1]*100:<4.0f}  "
                f"{l3p[0]*100:5.0f}/{l3p[1]*100:<4.0f}")
            shown += 1
    out("")

    pd.DataFrame(preds).to_csv(pred_path, index=False)
    vt.to_csv(OUT_DIR / "national_elo_layer3_validation.csv", index=False)
    pd.DataFrame([{"team_id": k, "team": name_by_id.get(k, k), "strength": round(v, 3)}
                  for k, v in sorted(s_final.items(), key=lambda kv: -kv[1])]).to_csv(
        OUT_DIR / "national_elo_layer3_ratings.csv", index=False)
    (OUT_DIR / "national_elo_layer3_report.txt").write_text("\n".join(report), encoding="utf-8")
    print(f"\nWritten: {OUT_DIR/'national_elo_layer3_validation.csv'}")
    print(f"Written: {pred_path} (now Layer-3)")
    print(f"Written: {OUT_DIR/'national_elo_layer3_ratings.csv'}")
    print(f"Written: {OUT_DIR/'national_elo_layer3_report.txt'}")


if __name__ == "__main__":
    main()
