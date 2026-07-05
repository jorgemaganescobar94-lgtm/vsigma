"""
DC GOALS RE-TEST (READ-ONLY · NO API · NO production change).

Follow-up to the bake-off (model_bakeoff_backtest.py). There DC beat L3 on Over2.5 by +0.021 logloss
but FRAGILE (CI95 lower bound grazed 0: [+0.001,+0.046]); BTTS non-significant; 1X2 clearly worse.
Jorge's ask: re-test DC ONLY for the GOALS markets (Over2.5, BTTS, and TOP SCORELINES) on the
EXPANDED OOS that now includes the settled World Cup 2026 fixtures, with:
  * strict anti-leakage walk-forward (isotonic/calibration fit ONLY on burn-in),
  * bootstrap CI95 + p under MULTIPLE seeds (prior result was fragile -> demand robustness),
  * a STRICT adoption gate: DC adopted for a market ONLY if it beats the current L3 with a CI95 that
    CLEARLY excludes 0 (not merely grazes it) AND is robust across seeds. Else -> close the DC topic.

1X2 is OUT OF SCOPE (DC does not improve it, already proven). Honest caveat: the WC settled sample is
a MODEST addition to the historical OOS (only 16 WC-2026 fixtures carry a leak-free sup_pre_l3).

This script REUSES the bake-off machinery verbatim (DC fit, tau, Poisson helpers, isotonic recipe,
walk-forward blocks) and only: (a) extends the OOS window to include 2026, (b) adds the scoreline
market, (c) runs multi-seed bootstrap, (d) reports temporal slices (hist / 2026 / WC-only / all).

OUTPUT: dc_goals_retest_report.txt + dc_goals_retest_metrics.csv + dc_goals_retest_CONCLUSION.md
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = Path(__file__).resolve().parent

# reuse the bake-off harness verbatim (DC already implemented there)
import model_bakeoff_backtest as BO
from model_bakeoff_backtest import (
    score_matrix, matrix_to_markets, dc_tau, fit_dixon_coles, fit_rho,
    build_form, cal_binary, ll_bin, br_bin, pmf_vec, KMAX,
)
import national_elo_layer3 as L3
import l3_offline

DATA = HERE / "international_results.csv"
PERMATCH = HERE / "national_elo_layer3_permatch.csv"
REPORT = HERE / "dc_goals_retest_report.txt"
METRICS = HERE / "dc_goals_retest_metrics.csv"

HL = float(L3.HL_DAYS)
BLOCK_DAYS = BO.BLOCK_DAYS
TRAIN_YEARS = BO.TRAIN_YEARS
CAL_START = BO.CAL_START          # 2019-01-01 burn-in start (same as bake-off)
OOS_LO = "2024-01-01"
OOS_HI = "2027-01-01"             # EXTENDED: was 2026-01-01; now includes settled 2026 (WC) fixtures
BURN_HI = OOS_LO                  # isotonic/L3 coeffs fit ONLY on [CAL_START, OOS_LO)

# STRICT adoption gate. The task demands the CI95 "clearly EXCLUDE 0, not graze it" precisely because
# the prior result was fragile (lo grazed 0 at +0.001). We therefore operationalise "clearly" as a
# COMFORTABLE margin, not the mere sign of the lower bound: the CI95 lower bound must stay above
# CLEAR_MARGIN across ALL bootstrap seeds. CLEAR_MARGIN=+0.005 is five times the prior fragile figure
# and ~1/4 of the observed effect (~+0.021) -> a lower bound below it is still "grazing 0", not a clear
# exclusion. A merely-positive lower bound (e.g. +0.003) does NOT clear this bar by design.
CLEAR_MARGIN = 0.005
SEEDS = [20260626, 1, 7, 42, 101, 2718, 31337, 99991, 424242, 20260705]


def multiseed_boot(d, seeds=SEEDS, nb=20000):
    """Paired bootstrap over multiple seeds. Returns list of (seed, lo, hi, p_gt0) and an aggregate
    dict: mean, min_lo, max_lo (across seeds), all_lo_pos, median p."""
    per = []
    for s in seeds:
        rng = np.random.RandomState(s)
        idx = rng.randint(0, len(d), (nb, len(d)))
        bd = d[idx].mean(1)
        lo = float(np.percentile(bd, 2.5)); hi = float(np.percentile(bd, 97.5))
        p = float((bd > 0).mean())
        per.append((s, lo, hi, p))
    los = np.array([x[1] for x in per]); his = np.array([x[2] for x in per])
    agg = dict(mean=float(d.mean()), min_lo=float(los.min()), max_lo=float(los.max()),
               min_hi=float(his.min()), max_hi=float(his.max()),
               all_lo_pos=bool((los > 0).all()), all_hi_neg=bool((his < 0).all()),
               median_p=float(np.median([x[3] for x in per])))
    return per, agg


def verdict(agg):
    """Strict gate on Δlogloss = L3 - DC (>0 => DC better)."""
    if agg["all_hi_neg"]:
        return "L3 TECHO (DC PEOR, IC excluye 0 por debajo)"
    if agg["mean"] > 0 and agg["all_lo_pos"] and agg["min_lo"] >= CLEAR_MARGIN:
        return "ADOPTAR DC (bate claramente, con margen, y robusto entre semillas)"
    if agg["mean"] > 0 and agg["all_lo_pos"]:
        return f"FRÁGIL — IC roza 0 (min_lo=+{agg['min_lo']:.4f} < margen +{CLEAR_MARGIN}) -> NO adoptar"
    return "NO adoptar (IC incluye 0)"


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

    ir = ir[ir["date"] >= pd.Timestamp(CAL_START)].copy()
    ir = ir[ir["fixture_id"].map(lambda f: int(f) in sup_by_fid)].reset_index(drop=True)
    ir["sup"] = ir["fixture_id"].map(lambda f: sup_by_fid[int(f)])

    arr = {c: ir[c].to_numpy() for c in ("home_id", "away_id", "gh", "ga", "neutral")}
    dates = ir["date"].to_numpy()
    tags = ir["league_tag"].to_numpy()
    fids = ir["fixture_id"].to_numpy().astype(int)
    sup = ir["sup"].to_numpy(float)
    n = len(ir)
    ghf = arr["gh"].astype(float); gaf = arr["ga"].astype(float)

    # ---- walk-forward DC ratings (leak-free), same block cadence as bake-off ----
    dc_lh = np.full(n, np.nan); dc_la = np.full(n, np.nan); dc_rho = np.full(n, np.nan)
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
            A, D, mu, H = fit_dixon_coles(arr["home_id"][prior], arr["away_id"][prior],
                                          ghf[prior], gaf[prior], arr["neutral"][prior], w)
            rho = fit_rho(arr["home_id"][prior], arr["away_id"][prior],
                          ghf[prior], gaf[prior], arr["neutral"][prior], w, A, D, mu, H)
            for i in np.where(blk)[0]:
                h, a, neu = arr["home_id"][i], arr["away_id"][i], arr["neutral"][i]
                if h in A and a in A:
                    dc_lh[i] = mu * A[h] * D[a] * (H if neu == 0 else 1.0)
                    dc_la[i] = mu * A[a] * D[h]
                    dc_rho[i] = rho
            n_blocks += 1
        block_start += pd.Timedelta(days=BLOCK_DAYS)

    # ---- L3 production goals model: margin lstsq + MATCHUP total, coeffs on burn-in only ----
    burn = (dates >= np.datetime64(CAL_START)) & (dates < np.datetime64(BURN_HI))
    Ab = np.c_[np.ones(burn.sum()), sup[burn]]
    a0a1, *_ = np.linalg.lstsq(Ab, (ghf - gaf)[burn], rcond=None)
    a0, a1 = float(a0a1[0]), float(a0a1[1])
    sb = sup[burn]
    tcoef, *_ = np.linalg.lstsq(np.c_[np.ones(len(sb)), np.abs(sb), sb ** 2], (ghf + gaf)[burn], rcond=None)
    tb0, tb1, tb2 = float(tcoef[0]), float(tcoef[1]), float(tcoef[2])
    TCAP = float(l3_offline.TOTAL_CAP)

    def l3_lambdas(i):
        margin = a0 + a1 * sup[i]
        total = min(tb0 + tb1 * abs(sup[i]) + tb2 * sup[i] ** 2, TCAP)
        return max(0.05, (total + margin) / 2.0), max(0.05, (total - margin) / 2.0)

    def l3_matrix(i):
        lh, la = l3_lambdas(i)
        return score_matrix(lh, la)

    def dc_matrix(i):
        lh, la, rho = dc_lh[i], dc_la[i], dc_rho[i]
        return score_matrix(lh, la, dc_tau(lh, la, rho))

    def scoreline_nll(i, M):
        gh = min(int(arr["gh"][i]), KMAX); ga = min(int(arr["ga"][i]), KMAX)
        return -np.log(max(M[gh, ga], 1e-15))

    have_dc = np.isfinite(dc_lh)
    is_wc = tags == "WC"

    # ---- slices on OOS (all require DC prediction; leak-free) ----
    def mask(lo, hi, wc_only=False):
        m = (dates >= np.datetime64(lo)) & (dates < np.datetime64(hi)) & have_dc
        if wc_only:
            m = m & is_wc
        return np.where(m)[0]

    SLICES = {
        "OOS_HIST_2024_2025": mask(OOS_LO, "2026-01-01"),
        "OOS_2026_ALL":       mask("2026-01-01", OOS_HI),
        "OOS_WC2026_ONLY":    mask("2026-01-01", OOS_HI, wc_only=True),
        "OOS_ALL_EXPANDED":   mask(OOS_LO, OOS_HI),
    }

    # burn-in indices for isotonic (fit ONLY here)
    burn_u = np.where(burn & have_dc)[0]
    over_b = ((ghf + gaf)[burn_u] >= 3).astype(int)
    btts_b = ((ghf[burn_u] >= 1) & (gaf[burn_u] >= 1)).astype(int)
    l3_over_b = np.array([matrix_to_markets(l3_matrix(i))[1] for i in burn_u])
    l3_btts_b = np.array([matrix_to_markets(l3_matrix(i))[2] for i in burn_u])
    dc_over_b = np.array([matrix_to_markets(dc_matrix(i))[1] for i in burn_u])
    dc_btts_b = np.array([matrix_to_markets(dc_matrix(i))[2] for i in burn_u])

    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 108)
    out("DC GOALS RE-TEST · L3 (producción) vs DIXON-COLES · Over2.5 / BTTS / MARCADORES · READ-ONLY · sin API · sin prod")
    out("=" * 108)
    out(f"burn-in isotónica/coefs: [{CAL_START}, {BURN_HI})  |  OOS extendido: [{OOS_LO}, {OOS_HI})")
    out(f"bloques walk-forward DC (refit {BLOCK_DAYS}d, ventana {TRAIN_YEARS:.0f}a, HL={HL:.0f}d): {n_blocks}")
    out(f"burn-in usable (DC): {len(burn_u)}")
    for name, idx in SLICES.items():
        wc = int(is_wc[idx].sum())
        out(f"  slice {name:20} n={len(idx):5d}  (WC-tag dentro: {wc})")
    out(f"L3 margin a0={a0:+.4f} a1={a1:.4f}  total tb0={tb0:.3f} tb1={tb1:.3f} tb2={tb2:.3f} cap={TCAP:.2f}")
    out(f"DC rho mediana (OOS all)={np.nanmedian(dc_rho[SLICES['OOS_ALL_EXPANDED']]):+.3f}")
    out(f"GATE estricto: ADOPTAR sólo si Δlogloss>0, todas las semillas lo>0, y min_lo>={CLEAR_MARGIN} (no rozar 0).")
    out(f"semillas bootstrap: {SEEDS}")
    out("")

    metric_rows = []

    for slname, idx in SLICES.items():
        if len(idx) < 30:
            out(f"[{slname}] n={len(idx)} < 30, se omite tabla (muestra insuficiente).")
            out("")
            continue
        over_o = ((ghf + gaf)[idx] >= 3).astype(int)
        btts_o = ((ghf[idx] >= 1) & (gaf[idx] >= 1)).astype(int)

        # calibrated binaries (isotonic fit on burn-in only)
        l3_over_raw = np.array([matrix_to_markets(l3_matrix(i))[1] for i in idx])
        l3_btts_raw = np.array([matrix_to_markets(l3_matrix(i))[2] for i in idx])
        dc_over_raw = np.array([matrix_to_markets(dc_matrix(i))[1] for i in idx])
        dc_btts_raw = np.array([matrix_to_markets(dc_matrix(i))[2] for i in idx])
        l3_over = cal_binary(l3_over_b, over_b, l3_over_raw)
        l3_btts = cal_binary(l3_btts_b, btts_b, l3_btts_raw)
        dc_over = cal_binary(dc_over_b, over_b, dc_over_raw)
        dc_btts = cal_binary(dc_btts_b, btts_b, dc_btts_raw)

        # scorelines: raw NLL of the ACTUAL scoreline under each full matrix (no per-cell isotonic
        # possible; identical treatment for both -> fair; this is exactly where DC's tau acts). Also a
        # top-scoreline hit rate (argmax cell == actual, capped at KMAX).
        l3_sc = np.array([scoreline_nll(i, l3_matrix(i)) for i in idx])
        dc_sc = np.array([scoreline_nll(i, dc_matrix(i)) for i in idx])

        def hit(matfn):
            h = 0
            for i in idx:
                M = matfn(i); am = np.unravel_index(np.argmax(M), M.shape)
                if am == (min(int(arr["gh"][i]), KMAX), min(int(arr["ga"][i]), KMAX)):
                    h += 1
            return h / len(idx)

        out("-" * 108)
        out(f"[{slname}]  n={len(idx)}   real Over2.5={over_o.mean()*100:.1f}%  BTTS={btts_o.mean()*100:.1f}%")
        out("-" * 108)
        out(f"  {'mercado':10} {'L3 logloss':>11} {'DC logloss':>11} {'L3 brier':>9} {'DC brier':>9}  "
            f"{'Δlogloss(L3-DC) media':>21}  {'IC95 (min..max entre semillas)':>34}  {'p':>5}  robusto  veredicto")

        for mk, (l3p, dcp, yo, is_bin) in {
            "Over2.5": (l3_over, dc_over, over_o, True),
            "BTTS":    (l3_btts, dc_btts, btts_o, True),
            "Marcador": (l3_sc, dc_sc, None, False),
        }.items():
            if is_bin:
                l3_loss = ll_bin(l3p, yo); dc_loss = ll_bin(dcp, yo)
                l3_br = float(br_bin(l3p, yo).mean()); dc_br = float(br_bin(dcp, yo).mean())
            else:
                l3_loss = l3p; dc_loss = dcp  # already per-match NLL
                l3_br = np.nan; dc_br = np.nan
            d = l3_loss - dc_loss   # >0 => DC better
            per, agg = multiseed_boot(d)
            vd = verdict(agg)
            rob = "SÍ" if (agg["all_lo_pos"] or agg["all_hi_neg"]) else "NO"
            out(f"  {mk:10} {l3_loss.mean():>11.5f} {dc_loss.mean():>11.5f} {l3_br:>9.5f} {dc_br:>9.5f}  "
                f"{agg['mean']:>+21.5f}  [{agg['min_lo']:+.5f}..{agg['max_hi']:+.5f}]{'':>6}  "
                f"{agg['median_p']:>5.3f}  {rob:>5}   {vd}")
            metric_rows.append(dict(slice=slname, market=mk, n=len(idx),
                                    l3_logloss=float(l3_loss.mean()), dc_logloss=float(dc_loss.mean()),
                                    l3_brier=l3_br, dc_brier=dc_br, delta_mean=agg["mean"],
                                    ci_min_lo=agg["min_lo"], ci_max_lo=agg["max_lo"],
                                    ci_min_hi=agg["min_hi"], ci_max_hi=agg["max_hi"],
                                    all_seeds_lo_pos=agg["all_lo_pos"], median_p=agg["median_p"],
                                    verdict=vd))
        # descriptive scoreline hit-rate
        out(f"  (marcador hit-rate argmax: L3={hit(l3_matrix)*100:.1f}%  DC={hit(dc_matrix)*100:.1f}%)")
        out("")

    out("=" * 108)
    out("LECTURA: Δlogloss(L3-DC)>0 => DC mejor. Gate ADOPTAR exige IC95 que EXCLUYE 0 con claridad en TODAS")
    out(f"las semillas (min_lo>={CLEAR_MARGIN}). Si el IC roza/incluye 0 => FRÁGIL, NO adoptar, cerrar DC.")
    out("Slice primario = OOS_ALL_EXPANDED (2024->2026 incl. WC liquidado). WC-only mostrado por transparencia (n pequeño).")
    out("=" * 108)

    pd.DataFrame(metric_rows).to_csv(METRICS, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS}")
    return metric_rows


if __name__ == "__main__":
    run()
