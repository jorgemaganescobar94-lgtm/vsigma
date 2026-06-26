"""
BACKTEST (READ-ONLY · NO production) — MATCH-DEPENDENT GOAL TOTAL vs the constant total in the L3
xG map. Audit candidate #1: does a per-match total calibrate Over/Under 2.5 and BTTS better OOS
WITHOUT hurting the 1X2?

Today  raw_xg:  s = a0 + a1·sup ;  xg = (total_mean ± s)/2  with total_mean CONSTANT (~2.66).
The 1X2 depends on the DIFFERENCE (lh−la = s), NOT on the total, so it should barely move. The
hypothesis: the real total rises in mismatches (and with attacking teams), so a match-dependent total
should calibrate OU/BTTS better.

It does NOT duplicate the calibration machinery: it reuses national_elo_layer3's building blocks
(fit_rating + the exact importance/cross-conf/time-decay weights + wdl + Isotonic) and the SAME
walk-forward + burn-in/OOS split the production L3 calibration uses. Only the TOTAL changes.

METHOD (strict anti-leakage):
  * Walk-forward L3 supremacy + per-team strengths: refit every REFIT_DAYS on PRIOR rows only
    (recomputed here from national_elo_layer3.fit_rating; cross-checked against the committed
    national_elo_layer3_permatch.csv sup_pre_l3).
  * BURN-IN (date < OOS_CUTOFF 2024-01-01): fit margin (a0,a1), the BASELINE constant total_mean,
    and the CANDIDATE total coefficients by least squares on the real total (gh+ga). Nothing is fit
    on the test.
  * OOS (date ≥ 2024-01-01): keep s = a0+a1·sup IDENTICAL; only swap the total. Recompute xg_home/away,
    the Poisson, and from there Over2.5 / BTTS / expected total / 1X2.
  * Compare BASELINE vs CANDIDATE OOS: Over2.5 & BTTS (logloss/brier/ECE), total (MAE), 1X2 no-harm
    (logloss/brier). Paired bootstrap IC95%.

CANDIDATE total forms (fit on burn-in only):
  (a) total = b0 + b1·|sup|                 (mismatch -> more goals)
  (b) total = b0 + b1·|sup| + b2·sup²
  (c) total = c0 + c1·(s_home + s_away)      (combined quality)

OUTPUT: total_goals_backtest_report.txt + total_goals_backtest_metrics.csv
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
import national_elo_layer3 as L3   # fit_rating, wdl, Isotonic, weights/constants (NO API on import)

DATA = HERE / "international_results.csv"
PERMATCH = HERE / "national_elo_layer3_permatch.csv"
REPORT = HERE / "total_goals_backtest_report.txt"
METRICS_CSV = HERE / "total_goals_backtest_metrics.csv"

MIN_TOTAL = 0.4   # floor on a predicted total (avoid degenerate xg); MIN_XG floor below
MIN_XG = 0.05


def walk_forward():
    """Leak-free per-match (sup, s_home, s_away) via the EXACT L3 walk-forward (refit every
    REFIT_DAYS on prior rows). Returns a DataFrame mirroring national_elo_layer3.main's loop."""
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).sort_values("date").reset_index(drop=True)
    df["home_id"] = df["home_id"].astype(int); df["away_id"] = df["away_id"].astype(int)
    n = len(df)
    hid = df["home_id"].to_numpy(); aid = df["away_id"].to_numpy()
    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    neutral = df["neutral"].to_numpy(int); tags = df["league_tag"].to_numpy()
    dates = df["date"].to_numpy()
    days = (dates - dates.min()) / np.timedelta64(1, "D")
    margin = np.clip(gh - ga, -L3.MARGIN_CAP, L3.MARGIN_CAP)
    imp = np.array([L3.IMP_BY_TAG.get(t, 0.8) for t in tags])
    votes = {}
    for i in range(n):
        cf = L3.TAG2CONF.get(tags[i])
        if cf:
            for tid in (hid[i], aid[i]):
                votes.setdefault(tid, Counter())[cf] += 1
    conf = {tid: cc.most_common(1)[0][0] for tid, cc in votes.items()}
    xconf = np.array([L3.XCONF_MULT if (conf.get(hid[i]) and conf.get(aid[i]) and conf[hid[i]] != conf[aid[i]])
                      else 1.0 for i in range(n)])
    base_w = imp * xconf

    sup = np.full(n, np.nan); sh = np.full(n, np.nan); sa = np.full(n, np.nan)
    cur_s, cur_h, last = None, 0.0, None
    for i in range(n):
        if cur_s is None or (last is not None and (days[i] - last) >= L3.REFIT_DAYS):
            pm = days < days[i]
            if pm.sum() >= L3.MIN_PAST:
                w = base_w[pm] * np.exp(-np.log(2) * (days[i] - days[pm]) / L3.HL_DAYS)
                cur_s, cur_h = L3.fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
                last = days[i]
        if cur_s is not None:
            s_h = cur_s.get(hid[i], 0.0); s_a = cur_s.get(aid[i], 0.0)
            sh[i] = s_h; sa[i] = s_a
            sup[i] = (s_h - s_a) + (cur_h if neutral[i] == 0 else 0.0)
    out = pd.DataFrame({"fixture_id": df["fixture_id"], "date": dates, "gh": gh, "ga": ga,
                        "sup": sup, "s_home": sh, "s_away": sa})
    out["is_oos"] = (dates >= np.datetime64(L3.OOS_CUTOFF)).astype(int)
    return out


def over25(L):
    """P(total>=3) for total~Poisson(L) (sum of two independent Poissons)."""
    L = np.maximum(L, 1e-9)
    return 1.0 - np.exp(-L) * (1.0 + L + L * L / 2.0)


def btts(lh, la):
    return (1.0 - np.exp(-np.maximum(lh, 0.0))) * (1.0 - np.exp(-np.maximum(la, 0.0)))


def _ll(p, y):
    p = np.clip(p, 1e-15, 1 - 1e-15); y = np.asarray(y, float)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def _ece(p, y, bins=10):
    p = np.asarray(p, float); y = np.asarray(y, float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (p > edges[i]) & (p <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(p) * abs(p[m].mean() - y[m].mean())
    return float(e)


def run():
    wf = walk_forward()
    # cross-check vs committed permatch sup (faithfulness of the recomputed walk-forward)
    drift = None
    try:
        pm = pd.read_csv(PERMATCH)[["fixture_id", "sup_pre_l3"]]
        j = wf.merge(pm, on="fixture_id", how="inner").dropna(subset=["sup", "sup_pre_l3"])
        drift = float(np.nanmax(np.abs(j["sup"] - j["sup_pre_l3"]))) if len(j) else None
    except Exception:
        drift = None

    d = wf.dropna(subset=["sup", "s_home", "s_away"]).copy()
    burn = d[d["is_oos"] == 0]
    oos = d[d["is_oos"] == 1]
    sup_b = burn["sup"].to_numpy(float); tot_b = (burn["gh"] + burn["ga"]).to_numpy(float)
    sq_b = burn["s_home"].to_numpy(float) + burn["s_away"].to_numpy(float)

    # margin map (a0,a1) on burn-in (same as production)
    A = np.c_[np.ones(len(sup_b)), sup_b]
    (a0, a1), *_ = np.linalg.lstsq(A, (burn["gh"] - burn["ga"]).to_numpy(float), rcond=None)
    total_mean = float(tot_b.mean())   # BASELINE constant total

    # candidate total coefficients (least squares on real total, burn-in only)
    cand = {}
    cand["a |sup|"] = np.linalg.lstsq(np.c_[np.ones(len(sup_b)), np.abs(sup_b)], tot_b, rcond=None)[0]
    cand["b |sup|+sup2"] = np.linalg.lstsq(np.c_[np.ones(len(sup_b)), np.abs(sup_b), sup_b ** 2], tot_b, rcond=None)[0]
    cand["c s_h+s_a"] = np.linalg.lstsq(np.c_[np.ones(len(sup_b)), sq_b], tot_b, rcond=None)[0]

    def xg_from(total, s):
        lh = np.maximum(MIN_XG, (total + s) / 2.0); la = np.maximum(MIN_XG, (total - s) / 2.0)
        return lh, la

    s_burn = a0 + a1 * sup_b
    res_b = np.where(burn["gh"].to_numpy() > burn["ga"].to_numpy(), 0,
                     np.where(burn["gh"].to_numpy() == burn["ga"].to_numpy(), 1, 2))
    Yb = np.eye(3)[res_b]

    # ---- OOS arrays ----
    sup_o = oos["sup"].to_numpy(float); sq_o = oos["s_home"].to_numpy(float) + oos["s_away"].to_numpy(float)
    gh_o = oos["gh"].to_numpy(float); ga_o = oos["ga"].to_numpy(float)
    tot_o = gh_o + ga_o
    s_o = a0 + a1 * sup_o
    real_over = (tot_o >= 3).astype(int)
    real_btts = ((gh_o >= 1) & (ga_o >= 1)).astype(int)
    res_o = np.where(gh_o > ga_o, 0, np.where(gh_o == ga_o, 1, 2)); Yo = np.eye(3)[res_o]

    def total_of(name, sup, sq):
        if name == "baseline":
            return np.full(len(sup), total_mean)
        if name == "a |sup|":
            b = cand["a |sup|"]; return b[0] + b[1] * np.abs(sup)
        if name == "b |sup|+sup2":
            b = cand["b |sup|+sup2"]; return b[0] + b[1] * np.abs(sup) + b[2] * sup ** 2
        if name == "c s_h+s_a":
            b = cand["c s_h+s_a"]; return b[0] + b[1] * sq
        raise ValueError(name)

    def metrics_for(name):
        """Fit THIS model's isotonic on burn-in with its OWN total (as it would be deployed), then
        evaluate OOS. -> fair 1X2 no-harm comparison (re-calibrated, not the baseline isotonic)."""
        tb = np.maximum(MIN_TOTAL, total_of(name, sup_b, sq_b))
        lhb, lab = xg_from(tb, s_burn)
        rawb = np.array([L3.wdl(lhb[i], lab[i]) for i in range(len(lhb))])
        isos = [L3.Isotonic().fit(rawb[:, k], Yb[:, k]) for k in range(3)]
        to = np.maximum(MIN_TOTAL, total_of(name, sup_o, sq_o))
        lh, la = xg_from(to, s_o)
        L = lh + la
        p_over = over25(L); p_btts = btts(lh, la)
        raw = np.array([L3.wdl(lh[i], la[i]) for i in range(len(lh))])
        cal = np.column_stack([isos[k].predict(raw[:, k]) for k in range(3)])
        cal = np.clip(cal, 1e-6, None); cal = cal / cal.sum(1, keepdims=True)
        return lh, la, L, p_over, p_btts, cal

    rng = np.random.RandomState(20260626)

    def boot_ic(d_per):   # paired bootstrap IC95% of mean(d_per)  (>0 = candidate better)
        idx = rng.randint(0, len(d_per), (10000, len(d_per)))
        bd = d_per[idx].mean(1)
        return float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))

    lines = []

    def out(s=""):
        print(s); lines.append(s)

    out("=" * 100)
    out("BACKTEST · TOTAL DE GOLES dependiente del partido vs total CONSTANTE — READ-ONLY, sin API")
    out("=" * 100)
    out(f"walk-forward recomputado (refit cada {L3.REFIT_DAYS}d, MIN_PAST={L3.MIN_PAST}); "
        f"cross-check sup vs permatch committeado: max|Δ|={drift if drift is not None else 'n/a'}")
    out(f"burn-in={len(burn)} (date<{L3.OOS_CUTOFF}) | OOS={len(oos)} | margin: s={a0:+.3f}{a1:+.3f}·sup")
    out("")
    out("(a) FORMAS DEL TOTAL y coeficientes (ajustados SOLO en burn-in, lstsq sobre gh+ga):")
    out(f"   baseline (constante)  total = {total_mean:.4f}")
    b = cand["a |sup|"];        out(f"   (a) |sup|            total = {b[0]:+.4f} {b[1]:+.4f}·|sup|")
    b = cand["b |sup|+sup2"];   out(f"   (b) |sup|+sup^2      total = {b[0]:+.4f} {b[1]:+.4f}·|sup| {b[2]:+.4f}·sup^2")
    b = cand["c s_h+s_a"];      out(f"   (c) s_home+s_away    total = {b[0]:+.4f} {b[1]:+.4f}·(s_h+s_a)")
    out("")

    # baseline OOS metrics
    _, _, L_base, po_base, pb_base, cal_base = metrics_for("baseline")
    base = {
        "over_ll": float(_ll(po_base, real_over).mean()), "over_br": float(((po_base - real_over) ** 2).mean()),
        "over_ece": _ece(po_base, real_over),
        "btts_ll": float(_ll(pb_base, real_btts).mean()), "btts_br": float(((pb_base - real_btts) ** 2).mean()),
        "btts_ece": _ece(pb_base, real_btts),
        "total_mae": float(np.abs(L_base - tot_o).mean()),
        "x_ll": float(-np.mean(np.sum(Yo * np.log(np.clip(cal_base, 1e-15, 1)), axis=1))),
        "x_br": float(np.mean(np.sum((cal_base - Yo) ** 2, axis=1))),
    }
    out("(b)/(d) OOS — BASELINE (total constante):")
    out(f"   Over2.5 : logloss {base['over_ll']:.5f} brier {base['over_br']:.5f} ECE {base['over_ece']:.4f}")
    out(f"   BTTS    : logloss {base['btts_ll']:.5f} brier {base['btts_br']:.5f} ECE {base['btts_ece']:.4f}")
    out(f"   total   : MAE {base['total_mae']:.4f} (real medio {tot_o.mean():.3f}, pred {L_base.mean():.3f})")
    out(f"   1X2     : logloss {base['x_ll']:.5f} brier {base['x_br']:.5f}  [chequeo de NO-DAÑO]")
    out("")

    metrics_rows = [{"model": "baseline", **base}]
    for name in ("a |sup|", "b |sup|+sup2", "c s_h+s_a"):
        _, _, L_c, po_c, pb_c, cal_c = metrics_for(name)
        m = {
            "over_ll": float(_ll(po_c, real_over).mean()), "over_br": float(((po_c - real_over) ** 2).mean()),
            "over_ece": _ece(po_c, real_over),
            "btts_ll": float(_ll(pb_c, real_btts).mean()), "btts_br": float(((pb_c - real_btts) ** 2).mean()),
            "btts_ece": _ece(pb_c, real_btts),
            "total_mae": float(np.abs(L_c - tot_o).mean()),
            "x_ll": float(-np.mean(np.sum(Yo * np.log(np.clip(cal_c, 1e-15, 1)), axis=1))),
            "x_br": float(np.mean(np.sum((cal_c - Yo) ** 2, axis=1))),
        }
        # paired bootstrap of Δlogloss(baseline − candidate); >0 = candidate better
        d_over = _ll(po_base, real_over) - _ll(po_c, real_over)
        d_btts = _ll(pb_base, real_btts) - _ll(pb_c, real_btts)
        rx_base = -np.sum(Yo * np.log(np.clip(cal_base, 1e-15, 1)), axis=1)
        rx_c = -np.sum(Yo * np.log(np.clip(cal_c, 1e-15, 1)), axis=1)
        d_x = rx_base - rx_c                                   # >0 = candidate better on 1X2
        ic_o = boot_ic(d_over); ic_b = boot_ic(d_btts); ic_x = boot_ic(d_x)
        sig_o = "SIGNIF" if (ic_o[0] > 0 or ic_o[1] < 0) else "no signif (IC∋0)"
        sig_b = "SIGNIF" if (ic_b[0] > 0 or ic_b[1] < 0) else "no signif (IC∋0)"
        # 1X2 NO-HARM: harm only if the candidate is SIGNIFICANTLY worse (IC entirely < 0)
        harm = ic_x[1] < 0
        out(f"CANDIDATO ({name}) vs baseline — Δ = baseline − candidato (>0 = candidato mejor):")
        out(f"   Over2.5 : ll {m['over_ll']:.5f} (Δ {base['over_ll']-m['over_ll']:+.5f}) brier {m['over_br']:.5f} "
            f"ECE {m['over_ece']:.4f} | IC95[{ic_o[0]:+.5f},{ic_o[1]:+.5f}] {sig_o}")
        out(f"   BTTS    : ll {m['btts_ll']:.5f} (Δ {base['btts_ll']-m['btts_ll']:+.5f}) brier {m['btts_br']:.5f} "
            f"ECE {m['btts_ece']:.4f} | IC95[{ic_b[0]:+.5f},{ic_b[1]:+.5f}] {sig_b}")
        out(f"   total   : MAE {m['total_mae']:.4f} (Δ {base['total_mae']-m['total_mae']:+.4f}, pred medio {L_c.mean():.3f})")
        out(f"   1X2     : logloss {m['x_ll']:.5f} (Δ {base['x_ll']-m['x_ll']:+.6f}) | IC95[{ic_x[0]:+.6f},{ic_x[1]:+.6f}] "
            f"-> {'DAÑA 1X2 (signif. peor)' if harm else 'OK no daña (cambio negligible/no signif.)'}")
        out("")
        metrics_rows.append({"model": name, **m, "ic_over_lo": ic_o[0], "ic_over_hi": ic_o[1],
                             "ic_btts_lo": ic_b[0], "ic_btts_hi": ic_b[1],
                             "ic_x_lo": ic_x[0], "ic_x_hi": ic_x[1], "harms_1x2": bool(harm)})

    # (c) ¿sube el total con |sup|?
    ba = cand["a |sup|"]
    out("(c) ¿el total real SUBE con |sup|? coef b1 (forma a) = "
        f"{ba[1]:+.4f} goles por unidad de |sup|  ->  "
        f"{'sube (mismatch -> más goles)' if ba[1] > 0 else 'NO sube' if ba[1] <= 0 else ''}")
    rng_sup = np.percentile(np.abs(sup_o), [10, 90])
    out(f"    rango |sup| OOS p10..p90 = {rng_sup[0]:.2f}..{rng_sup[1]:.2f} -> "
        f"swing de total ≈ {ba[1]*(rng_sup[1]-rng_sup[0]):+.3f} goles entre partido parejo y desajuste.")
    out("")
    out("=" * 100)
    out("LECTURA: integrar SOLO si OU/BTTS mejora claro Y significativo (IC95% excluye 0, Δ>0) SIN dañar")
    out("el 1X2. Si no es significativo o daña el 1X2 -> el total constante ya es suficiente -> descartar.")
    out("=" * 100)

    pd.DataFrame(metrics_rows).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}")


if __name__ == "__main__":
    run()
