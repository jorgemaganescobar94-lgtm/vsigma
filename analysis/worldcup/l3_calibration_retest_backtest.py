"""
L3 1X2 CALIBRATION RE-TEST (READ-ONLY · NO API · NO production change · NO commit).

MOTIVATION. The live World-Cup calibration of L3 shows a MONOTONE under-dispersion across the 5
reliability bands (favourites under-called: 60-80 predicts 72% / wins 82%, 80-100 83% / 100%;
underdogs over-called: 0-20 14% / 11%, 20-40 28% / 23%), consistent in L3 and v2 at N=65 — BUT
inside the noise (ECE 0.107 < null p95 0.173). Under-dispersion is EXACTLY what temperature scaling
with T<1 (sharpening) corrects, and epoch drift is what a rolling isotonic corrects.

HONESTY RULE. We do NOT tune anything on the 65 WC matches (that would be fitting the very sample
that raised the question -> overfit-to-the-track). Everything is fit on the burn-in (<2024) and JUDGED
on the large historical OOS [2024-01-01, WC-2026 start). WC-2026 is a SECONDARY holdout: confirmation
only, never used to fit or select. A variant is adopted ONLY if it beats production on the HISTORICAL
OOS with a CI95 that CLEARLY excludes 0 (comfortable margin, not grazing) and is robust across >=8
bootstrap seeds — identical rigour to the DC goals re-test (dc_goals_retest_backtest.py).

REUSE, NOT REIMPLEMENT. The rating model (L3.fit_rating), the Poisson->1X2 map (L3.wdl/L3.pmf), the
isotonic (L3.Isotonic), the metrics (L3.logloss_mc/brier_mc/ece_mc), the weighting scheme
(L3.IMP_BY_TAG/TAG2CONF/HL_DAYS/REFIT_DAYS/XCONF_MULT/LAM/MARGIN_CAP/MIN_PAST/OOS_CUTOFF) and the
total model (l3_offline.TOTAL_CAP/TOTAL_MATCHUP_LIVE) all come from the shipped modules. Only the
walk-forward ORCHESTRATION loop is reproduced here (verbatim to national_elo_layer3.main() lines
~161-262, minus its API-backed WC-prediction tail) so we can (a) refresh the leak-free supremacy
through 2026-07-07 (the committed permatch dump is stale at matchday-1) and (b) add the temperature /
rolling-isotonic variants.

VARIANTS (all judged on the SAME OOS rows):
  C0  PRODUCTION baseline: raw Poisson 1X2 -> isotonic FROZEN on <2024 (matchup total, live flag).
  C1  C0 + multiclass TEMPERATURE T on the H/D/A logits, T fit ONLY on <2024 (internal train/val
      split reported). T<1 = sharpening (the fix under-dispersion predicts).
  C2  ROLLING isotonic (re-fit walk-forward on each match's past only) instead of frozen -> epoch drift.
  C3  TEMPERATURE without isotonic (raw Poisson probs -> T), to see if T alone calibrates better.

METRICS: OOS logloss (PRIMARY judge), brier, ECE, and reliability bands before/after. Fitted T reported
(confirm direction T<1). Paired bootstrap CI95 over MULTIPLE seeds (>=8). Strict adoption gate.

OUTPUT: l3_calibration_retest_report.txt + l3_calibration_retest_metrics.csv + l3_calibration_retest_CONCLUSION.md
This does NOT touch production 1X2, the frozen isotonic, or any committed file. No API, no secrets, no bets.
"""
from __future__ import annotations

import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent

import national_elo_layer3 as L3   # noqa: E402  (no API on import; only main() calls the API)
import l3_offline                  # noqa: E402  (TOTAL_CAP / TOTAL_MATCHUP_LIVE — single source of truth)

DATA = HERE / "international_results.csv"
REPORT = HERE / "l3_calibration_retest_report.txt"
METRICS = HERE / "l3_calibration_retest_metrics.csv"
CONCLUSION = HERE / "l3_calibration_retest_CONCLUSION.md"

OOS_LO = "2024-01-01"                 # OOS start (= L3.OOS_CUTOFF burn-in boundary)
WC_START = "2026-06-11"               # first WC-2026 fixture -> PRIMARY = [OOS_LO, WC_START)
OOS_HI = "2027-01-01"

# STRICT adoption gate, IDENTICAL rigour to the DC goals re-test. "Clearly exclude 0, not graze it"
# is operationalised as a COMFORTABLE margin on the CI95 lower bound held across ALL seeds. We keep the
# SAME CLEAR_MARGIN=0.005 as the DC re-test so the bar is not re-negotiated for this study. We ALSO
# report the weaker "all-seeds lo>0" significance separately, so a real-but-small effect that grazes 0
# is visible and honestly labelled FRAGILE (not silently upgraded).
CLEAR_MARGIN = 0.005
SEEDS = [20260707, 1, 7, 42, 101, 2718, 31337, 99991, 424242, 20260705]
BOOT_N = 20000
ROLL_BLOCK_DAYS = 90                  # C2 rolling-isotonic refit cadence


# ----------------------------- helpers ---------------------------------------
def per_match_ll(P, Y):
    """Per-match multiclass logloss vector (-sum_k Y log P)."""
    return -np.sum(Y * np.log(np.clip(P, L3.EPS, 1.0)), axis=1)


def apply_temperature(P, T):
    """Multiclass temperature on the logits log(P): softmax(log P / T) = P^(1/T) normalised. T<1 sharpens."""
    z = np.log(np.clip(P, 1e-12, 1.0)) / T
    z -= z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def fit_temperature(P, Y):
    """T>0 minimising multiclass logloss of softmax(log P / T) on (P,Y). Coarse scan + parabolic refine."""
    def ll(T):
        return L3.logloss_mc(apply_temperature(P, T), Y)
    grid = np.linspace(0.5, 2.0, 61)
    vals = [ll(t) for t in grid]
    j = int(np.argmin(vals))
    lo, hi = grid[max(0, j - 1)], grid[min(len(grid) - 1, j + 1)]
    fine = np.linspace(lo, hi, 61)
    fv = [ll(t) for t in fine]
    return float(fine[int(np.argmin(fv))])


def reliability_bands(P, Y, edges=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0001)):
    """Flattened H/D/A reliability: predicted prob vs realised frequency per band (exactly the
    production scorecard (2) recipe; n_pred = 3 * n_matches)."""
    p = P.reshape(-1)
    y = Y.reshape(-1)
    rows = []
    for i in range(len(edges) - 1):
        m = (p >= edges[i]) & (p < edges[i + 1])
        rows.append((f"{int(edges[i]*100)}-{int(min(edges[i+1],1.0)*100)}%",
                     int(m.sum()),
                     float(p[m].mean()) if m.sum() else float("nan"),
                     float(y[m].mean()) if m.sum() else float("nan")))
    return rows


def multiseed_boot(d, seeds=SEEDS, nb=BOOT_N):
    """Paired bootstrap of a per-match delta d (>0 => variant better than C0), over multiple seeds."""
    per = []
    for s in seeds:
        rng = np.random.RandomState(s)
        idx = rng.randint(0, len(d), (nb, len(d)))
        bd = d[idx].mean(1)
        per.append((s, float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5)), float((bd > 0).mean())))
    los = np.array([x[1] for x in per]); his = np.array([x[2] for x in per])
    return dict(mean=float(d.mean()), min_lo=float(los.min()), max_lo=float(los.max()),
                min_hi=float(his.min()), max_hi=float(his.max()),
                all_lo_pos=bool((los > 0).all()), all_hi_neg=bool((his < 0).all()),
                median_p=float(np.median([x[3] for x in per])))


def verdict(agg):
    """Strict gate on Δlogloss = C0 - Cx (>0 => variant better)."""
    if agg["all_hi_neg"]:
        return "PEOR que C0 (IC excluye 0 por debajo)"
    if agg["mean"] > 0 and agg["all_lo_pos"] and agg["min_lo"] >= CLEAR_MARGIN:
        return "ADOPTAR (bate a C0 con margen cómodo y robusto entre semillas)"
    if agg["mean"] > 0 and agg["all_lo_pos"]:
        return f"FRÁGIL — IC roza 0 (min_lo=+{agg['min_lo']:.4f} < margen +{CLEAR_MARGIN}) -> NO adoptar"
    return "NO adoptar (IC incluye 0)"


# ----------------------------- walk-forward (reused orchestration) -----------
def build_walk_forward():
    """Reproduce national_elo_layer3.main()'s leak-free walk-forward (lines ~150-262) using the shipped
    L3 primitives, WITHOUT its API tail. Returns a dict of per-match arrays + burn-in coefficients."""
    df = pd.read_csv(DATA)
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.tz_localize(None)
    df = df.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).sort_values("date").reset_index(drop=True)
    df["home_id"] = df["home_id"].astype(int); df["away_id"] = df["away_id"].astype(int)
    n = len(df)

    # confederation votes (cross-conf up-weight) — verbatim recipe
    votes = {}
    for _, r in df.iterrows():
        cf = L3.TAG2CONF.get(r["league_tag"])
        if cf:
            for tid in (r["home_id"], r["away_id"]):
                votes.setdefault(tid, Counter())[cf] += 1
    conf = {tid: cc.most_common(1)[0][0] for tid, cc in votes.items()}

    hid = df["home_id"].to_numpy(); aid = df["away_id"].to_numpy()
    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    neutral = df["neutral"].to_numpy(int); tags = df["league_tag"].to_numpy()
    dates = df["date"].to_numpy()
    days = (dates - dates.min()) / np.timedelta64(1, "D")
    margin = np.clip(gh - ga, -L3.MARGIN_CAP, L3.MARGIN_CAP)
    imp = np.array([L3.IMP_BY_TAG.get(t, 0.8) for t in tags])
    xconf = np.array([L3.XCONF_MULT if (conf.get(hid[i]) and conf.get(aid[i]) and conf[hid[i]] != conf[aid[i]])
                      else 1.0 for i in range(n)])
    base_w = imp * xconf
    res = np.where(gh > ga, 0, np.where(gh == ga, 1, 2)); Y = np.eye(3)[res]

    # walk-forward: refit every REFIT_DAYS on prior matches (time-decayed) — verbatim
    sup_pre = np.full(n, np.nan)
    last_fit_day = None; cur_s, cur_h = None, 0.0; n_refits = 0
    for i in range(n):
        if cur_s is None or (days[i] - last_fit_day) >= L3.REFIT_DAYS:
            pm = days < days[i]
            if pm.sum() >= L3.MIN_PAST:
                w = base_w[pm] * np.exp(-np.log(2) * (days[i] - days[pm]) / L3.HL_DAYS)
                cur_s, cur_h = L3.fit_rating(hid[pm], aid[pm], neutral[pm], margin[pm], w)
                last_fit_day = days[i]; n_refits += 1
        if cur_s is not None:
            sh = cur_s.get(hid[i], 0.0); sa = cur_s.get(aid[i], 0.0)
            sup_pre[i] = (sh - sa) + (cur_h if neutral[i] == 0 else 0.0)

    ok = np.isfinite(sup_pre)
    burn = (dates < np.datetime64(OOS_LO)) & ok
    # burn-in margin + total (matchup, forma b) — verbatim recipe
    A = np.c_[np.ones(int(burn.sum())), sup_pre[burn]]
    a0a1, *_ = np.linalg.lstsq(A, (gh - ga)[burn], rcond=None)
    a0, a1 = float(a0a1[0]), float(a0a1[1])
    total_mean = float(np.mean((gh + ga)[burn]))
    sb = sup_pre[burn]
    tcoef, *_ = np.linalg.lstsq(np.c_[np.ones(len(sb)), np.abs(sb), sb ** 2], (gh + ga)[burn], rcond=None)
    tb0, tb1, tb2 = float(tcoef[0]), float(tcoef[1]), float(tcoef[2])

    return dict(df=df, n=n, dates=dates, tags=tags, sup=sup_pre, ok=ok, burn=burn, Y=Y, res=res,
                gh=gh, ga=ga, a0=a0, a1=a1, total_mean=total_mean, tcoef=(tb0, tb1, tb2),
                n_refits=n_refits, matchup=bool(l3_offline.TOTAL_MATCHUP_LIVE))


def raw_probs(sup, a0, a1, tcoef, total_mean, matchup):
    tb0, tb1, tb2 = tcoef
    s = a0 + a1 * sup
    total = min(tb0 + tb1 * abs(sup) + tb2 * sup * sup, l3_offline.TOTAL_CAP) if matchup else total_mean
    lh = max(0.05, (total + s) / 2.0); la = max(0.05, (total - s) / 2.0)
    return L3.wdl(lh, la)


# ----------------------------- main run --------------------------------------
def run():
    st = build_walk_forward()
    n, dates, tags = st["n"], st["dates"], st["tags"]
    sup, ok, burn, Y = st["sup"], st["ok"], st["burn"], st["Y"]
    a0, a1, tcoef, total_mean, matchup = st["a0"], st["a1"], st["tcoef"], st["total_mean"], st["matchup"]
    df = st["df"]
    is_wc = (df["league_id"].to_numpy() == 1) & (df["season"].to_numpy() == 2026)

    # raw Poisson 1X2 for every match (leak-free: sup_pre is walk-forward, coeffs are burn-in)
    P_raw = np.zeros((n, 3))
    for i in range(n):
        P_raw[i] = raw_probs(sup[i], a0, a1, tcoef, total_mean, matchup) if ok[i] else np.array([0.45, 0.27, 0.28])
    P_raw /= P_raw.sum(1, keepdims=True)

    # ---- C0: isotonic FROZEN on burn-in ----
    isos0 = [L3.Isotonic().fit(P_raw[burn, k], Y[burn, k]) for k in range(3)]
    Pc0 = np.c_[isos0[0].predict(P_raw[:, 0]), isos0[1].predict(P_raw[:, 1]), isos0[2].predict(P_raw[:, 2])]
    Pc0 = np.clip(Pc0, 1e-6, None); Pc0 /= Pc0.sum(1, keepdims=True)

    # ---- C1: C0 + temperature (T fit on burn-in; internal train/val split reported) ----
    T1 = fit_temperature(Pc0[burn], Y[burn])
    burn_idx = np.where(burn)[0]
    half = len(burn_idx) // 2                        # time-ordered internal split (df is date-sorted)
    T1_tr = fit_temperature(Pc0[burn_idx[:half]], Y[burn_idx[:half]])
    T1_va = fit_temperature(Pc0[burn_idx[half:]], Y[burn_idx[half:]])
    Pc1 = apply_temperature(Pc0, T1)

    # ---- C3: temperature WITHOUT isotonic (fit on burn-in) ----
    T3 = fit_temperature(P_raw[burn], Y[burn])
    Pc3 = apply_temperature(P_raw, T3)

    # ---- C2: ROLLING isotonic (re-fit on each match's past only; raw coeffs stay burn-in) ----
    Pc2 = Pc0.copy()                                  # for burn-in rows keep frozen (not evaluated там)
    order = np.argsort(dates, kind="mergesort")       # already sorted, but be safe
    d64 = dates
    oos_lo64 = np.datetime64(OOS_LO)
    # for every OOS match, fit isotonic on all matches strictly before its rolling-block start
    oos_mask = ok & (d64 >= oos_lo64)
    block_start = pd.Timestamp(OOS_LO)
    last = pd.Timestamp(dates.max())
    while block_start <= last:
        bs = np.datetime64(block_start); be = np.datetime64(block_start + pd.Timedelta(days=ROLL_BLOCK_DAYS))
        prior = ok & (d64 < bs)
        blk = oos_mask & (d64 >= bs) & (d64 < be)
        if blk.sum() and prior.sum() >= L3.MIN_PAST:
            isr = [L3.Isotonic().fit(P_raw[prior, k], Y[prior, k]) for k in range(3)]
            Q = np.c_[isr[0].predict(P_raw[blk, 0]), isr[1].predict(P_raw[blk, 1]), isr[2].predict(P_raw[blk, 2])]
            Q = np.clip(Q, 1e-6, None); Q /= Q.sum(1, keepdims=True)
            Pc2[blk] = Q
        block_start += pd.Timedelta(days=ROLL_BLOCK_DAYS)

    variants = {"C0_prod": Pc0, "C1_temp": Pc1, "C2_rolliso": Pc2, "C3_temp_noiso": Pc3}

    # ---- slices ----
    prim = np.where(ok & (dates >= np.datetime64(OOS_LO)) & (dates < np.datetime64(WC_START)) & ~is_wc)[0]
    seco = np.where(ok & is_wc)[0]
    allo = np.where(ok & (dates >= np.datetime64(OOS_LO)) & (dates < np.datetime64(OOS_HI)))[0]
    SLICES = {"OOS_PRIMARY_2024_preWC": prim, "OOS_SECONDARY_WC2026": seco, "OOS_ALL": allo}

    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 110)
    out("L3 1X2 CALIBRATION RE-TEST · producción(C0) vs temperature(C1/C3) vs isotónica rolling(C2) · READ-ONLY · sin API · sin prod")
    out("=" * 110)
    out(f"burn-in (fit isotónica/T/coefs): fecha < {OOS_LO}   |   PRIMARY OOS: [{OOS_LO}, {WC_START})   |   WC-2026: >= {WC_START}")
    out(f"matches={n}  refits walk-forward={st['n_refits']}  con rating={int(ok.sum())}  burn-in={int(burn.sum())}  matchup_total={matchup}")
    out(f"L3 margin a0={a0:+.4f} a1={a1:.4f}  |  total forma-b tb0={tcoef[0]:.3f} tb1={tcoef[1]:.3f} tb2={tcoef[2]:.3f} (cap {l3_offline.TOTAL_CAP})")
    out(f"TEMPERATURE ajustada en burn-in:  C1 (sobre isotónica) T={T1:.4f}   C3 (sin isotónica) T={T3:.4f}   [T<1 = sharpening]")
    out(f"  C1 estabilidad train/val interno (burn-in por fecha): T_train={T1_tr:.4f}  T_val={T1_va:.4f}  (deben coincidir ~)")
    for name, idx in SLICES.items():
        out(f"  slice {name:26} n={len(idx):5d}  (WC dentro: {int(is_wc[idx].sum())})")
    out(f"GATE estricto (idéntico a DC): ADOPTAR sólo si Δlogloss(C0-Cx)>0, TODAS las semillas lo>0, y min_lo>={CLEAR_MARGIN} (no rozar 0).")
    out(f"semillas bootstrap ({len(SEEDS)}): {SEEDS}")
    out("")

    metric_rows = []
    for slname, idx in SLICES.items():
        Yi = Y[idx]
        out("-" * 110)
        out(f"[{slname}]  n={len(idx)}   base 1X2 real: H={Yi[:,0].mean()*100:.1f}% D={Yi[:,1].mean()*100:.1f}% A={Yi[:,2].mean()*100:.1f}%")
        out("-" * 110)
        out(f"  {'variante':16} {'logloss':>9} {'brier':>8} {'ECE':>7} {'acc%':>6}   {'Δlogloss(C0-Cx) media':>21}  {'IC95 [min_lo..max_hi] semillas':>32}  {'p':>5}  veredicto")
        base_ll = None
        d0 = per_match_ll(Pc0[idx], Yi)
        for vname, PV in variants.items():
            Pi = PV[idx]
            ll = L3.logloss_mc(Pi, Yi); br = L3.brier_mc(Pi, Yi); ece = L3.ece_mc(Pi, Yi); acc = L3.acc_mc(Pi, Yi)
            if vname == "C0_prod":
                base_ll = ll
                out(f"  {vname:16} {ll:>9.5f} {br:>8.5f} {ece:>7.4f} {acc*100:>6.1f}   {'(baseline)':>21}  {'':>32}  {'':>5}  —")
                metric_rows.append(dict(slice=slname, variant=vname, n=len(idx), logloss=ll, brier=br, ece=ece,
                                        acc=acc, T=np.nan, delta_mean=0.0, ci_min_lo=np.nan, ci_max_hi=np.nan,
                                        all_lo_pos=False, median_p=np.nan, verdict="baseline"))
                continue
            d = d0 - per_match_ll(Pi, Yi)   # >0 => variant better than C0
            agg = multiseed_boot(d)
            vd = verdict(agg)
            Tv = T1 if vname == "C1_temp" else (T3 if vname == "C3_temp_noiso" else np.nan)
            out(f"  {vname:16} {ll:>9.5f} {br:>8.5f} {ece:>7.4f} {acc*100:>6.1f}   {agg['mean']:>+21.5f}  "
                f"[{agg['min_lo']:+.5f}..{agg['max_hi']:+.5f}]{'':>3}  {agg['median_p']:>5.3f}  {vd}")
            metric_rows.append(dict(slice=slname, variant=vname, n=len(idx), logloss=ll, brier=br, ece=ece,
                                    acc=acc, T=Tv, delta_mean=agg["mean"], ci_min_lo=agg["min_lo"],
                                    ci_max_hi=agg["max_hi"], all_lo_pos=agg["all_lo_pos"],
                                    median_p=agg["median_p"], verdict=vd))
        out("")
        # reliability bands before/after (C0 vs C1 vs C2) on this slice
        out(f"  RELIABILITY (H/D/A aplanado, n_pred={3*len(idx)}) — predicho vs real por banda:")
        out(f"      {'banda':9} | {'C0 n/pred/real':>22} | {'C1 pred/real':>16} | {'C2 pred/real':>16}")
        b0 = reliability_bands(Pc0[idx], Yi); b1 = reliability_bands(Pc1[idx], Yi); b2 = reliability_bands(Pc2[idx], Yi)
        for (band, nn, p0, r0), (_, _, p1, r1), (_, _, p2, r2) in zip(b0, b1, b2):
            out(f"      {band:9} | n={nn:4d} pred={p0*100:4.0f}% real={r0*100:4.0f}% | {p1*100:4.0f}% / {r1*100:4.0f}%      | {p2*100:4.0f}% / {r2*100:4.0f}%")
        out("")

    out("=" * 110)
    out("LECTURA: Δlogloss(C0-Cx)>0 => la variante Cx mejora sobre producción. El JUEZ es OOS_PRIMARY (histórico grande).")
    out(f"ADOPTAR exige IC95 que excluye 0 con claridad en TODAS las semillas (min_lo>={CLEAR_MARGIN}). WC-2026 = confirmación,")
    out("no validador: si sólo mejora en WC pero no en el histórico => sospechoso (overfit a la pista) => NO adoptar.")
    out("Si el efecto roza/incluye 0 en el histórico => FRÁGIL/ruido => cerrar (no corregible con muestra fiable).")
    out("=" * 110)

    pd.DataFrame(metric_rows).to_csv(METRICS, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}")
    print(f"Written: {METRICS}")

    # ---- CONCLUSION.md (verdict per variant, judged on PRIMARY) ----
    mr = pd.DataFrame(metric_rows)
    prim_rows = mr[mr["slice"] == "OOS_PRIMARY_2024_preWC"]
    wc_rows = mr[mr["slice"] == "OOS_SECONDARY_WC2026"]
    def vrow(dfx, v):
        r = dfx[dfx["variant"] == v]
        return r.iloc[0] if len(r) else None
    md = []
    md.append("# L3 1X2 CALIBRATION RE-TEST — veredicto\n")
    md.append("**Read-only · sin API · sin cambio de producción · sin commit.** Motivado por la infra-dispersión")
    md.append("monótona del L3 en las 5 bandas del Mundial (favoritos infra-llamados, underdogs sobre-llamados),")
    md.append("consistente en L3 y v2 (N=65) pero DENTRO del ruido (ECE 0.107 < p95 nulo 0.173). Regla de honestidad:")
    md.append("nada se ajusta a los 65 partidos del Mundial; todo se ajusta en burn-in (<2024) y se JUZGA en el OOS")
    md.append(f"histórico grande [{OOS_LO}, {WC_START}). WC-2026 es holdout secundario (confirmación, nunca ajuste).\n")
    md.append(f"- **Temperatura ajustada (burn-in):** C1 (sobre isotónica) **T={T1:.4f}**, C3 (sin isotónica) **T={T3:.4f}**. "
              f"Estabilidad train/val interno de C1: T_train={T1_tr:.4f} / T_val={T1_va:.4f}.")
    md.append(f"  {'T<1 confirma sharpening (corrige la infra-dispersión).' if T1 < 1 else 'T>=1: NO sharpening — la infra-dispersión no se confirma fuera del Mundial.'}\n")
    md.append(f"- **Gate:** idéntico a la re-prueba DC — ADOPTAR sólo si Δlogloss(C0-Cx)>0 en el histórico, con IC95 que")
    md.append(f"  excluye 0 con margen cómodo (min_lo≥{CLEAR_MARGIN}) y robusto en {len(SEEDS)} semillas.\n")
    md.append("## Veredicto por variante (juez = OOS_PRIMARY histórico)\n")
    md.append("| variante | logloss C0→Cx | ΔECE | Δlogloss medio | IC95 (min_lo..max_hi) | veredicto |")
    md.append("|---|---|---|---|---|---|")
    c0p = vrow(prim_rows, "C0_prod")
    for v in ["C1_temp", "C2_rolliso", "C3_temp_noiso"]:
        r = vrow(prim_rows, v)
        if r is None:
            continue
        md.append(f"| {v} | {c0p['logloss']:.5f}→{r['logloss']:.5f} | {r['ece']-c0p['ece']:+.4f} | "
                  f"{r['delta_mean']:+.5f} | [{r['ci_min_lo']:+.5f}..{r['ci_max_hi']:+.5f}] | {r['verdict']} |")
    md.append("\n## Confirmación WC-2026 (secundario, NO decide)\n")
    md.append("| variante | logloss C0→Cx | ΔECE | Δlogloss medio | veredicto WC |")
    md.append("|---|---|---|---|---|")
    c0w = vrow(wc_rows, "C0_prod")
    for v in ["C1_temp", "C2_rolliso", "C3_temp_noiso"]:
        r = vrow(wc_rows, v)
        if r is None or c0w is None:
            continue
        md.append(f"| {v} | {c0w['logloss']:.5f}→{r['logloss']:.5f} | {r['ece']-c0w['ece']:+.4f} | {r['delta_mean']:+.5f} | {r['verdict']} |")
    adopt = [v for v in ["C1_temp", "C2_rolliso", "C3_temp_noiso"]
             if (vrow(prim_rows, v) is not None and str(vrow(prim_rows, v)["verdict"]).startswith("ADOPTAR"))]
    md.append("\n## Recomendación\n")
    if adopt:
        md.append(f"- **{', '.join(adopt)}** supera(n) el gate estricto en el histórico. Candidata(s) a adopción — "
                  "requiere aprobación 🔴 de Jorge (toca la calibración del 1X2 de producción). NO aplicado.")
    else:
        md.append("- **Ninguna variante** supera el gate estricto en el OOS histórico. La infra-dispersión observada en")
        md.append("  el Mundial es coherente con RUIDO (ECE dentro del p95 nulo) y/o no es corregible con la muestra")
        md.append("  fiable disponible. **Recomendación: cerrar el tema, mantener C0 (producción) sin cambios.**")
    md.append("\n_Artefactos: l3_calibration_retest_report.txt · l3_calibration_retest_metrics.csv · este CONCLUSION.md. "
              "No se tocó producción ni la isotónica congelada._")
    CONCLUSION.write_text("\n".join(md), encoding="utf-8")
    print(f"Written: {CONCLUSION}")
    return metric_rows


if __name__ == "__main__":
    run()
