"""
SQUAD-QUALITY (player-based) team strength BLENDED with the L3 rating — does it add OOS
predictive power to the 1X2/goals forecast?  READ-ONLY · NO production change · NO API.

HYPOTHESIS: a team strength built from PLAYER quality carries signal over the results-based L3
rating, ESPECIALLY when recent results lag the squad's reality (changed roster / few recent
competitive matches). The results-rating is slow and backward-looking; the squad knows "who is
actually on the pitch".

It does NOT duplicate logic — it REUSES:
  * context_shadow_backtest.WFRatings  -> leak-free WALK-FORWARD L3 strengths (fit_rating on
    matches strictly BEFORE each match date, production weights). The exact baseline harness.
  * props_retest_stats_inputs.team_rates / .confirmed_xi -> the cached prior-season (2023) per
    player /90 rates + confirmed XI (the props backtest cache: data/processed/worldcup/props_backtest).
  * national_elo_layer3 (L3) Isotonic + the L3 margin->Poisson->isotonic functional form, and
    l3_offline.wdl. The candidate is the SAME pipeline with ONE extra margin term.

PLAYER-QUALITY METRIC (leak-free, prior-season 2023, BEFORE every 2024-2025 match):
  games.rating is NOT in the cache (only minutes,g90,a90,sh90,son90,c90,on_ratio), and fetching it
  would cost API (quota = red zone) -> per the task's fallback we use a COMPOSITE from the cached
  data. Crucially these are NATIONAL-TEAM /90 rates (the player's stats FOR the national team in
  2023), i.e. already on a COMMON INTERNATIONAL scale — so the "7.0 in 2nd div != 7.0 in Premier"
  cross-league comparability problem (which afflicts club games.rating) does NOT bite this metric.
  Residual limitation: g90/a90 are OFFENSE-biased (defenders/keepers score low); minutes-weighting
  partially corrects via role/coach-trust. We measure the impact (minutes-only vs +offense).

  per player p (2023):  q_p = z(g90_p) + 0.5 * z(a90_p)         (offensive output; assists half)
  team strength two documented aggregations:
     SQUAD-AVG : minutes-weighted mean of q_p over the whole cached roster (no XI needed -> N large)
     TOP-N     : mean q_p of the N players with most 2023 minutes (de-facto first XI proxy)
  squad_diff = strength(home) - strength(away)   (the FEATURE; local - visitante)
  z(.) standardised over the WHOLE cached player pool (a fixed transform, no target -> documented
  minor look-ahead, same convention as props_matchup_backtest's z-scores).

METHOD (anti-leakage, faithful to L3 "como hoy"):
  margin_hat = a0 + a1*sup_L3            (BASELINE — exactly the L3 fit)
  margin_hat = a0 + a1*sup_L3 + a2*squad_diff   (CANDIDATE — let burn-in lstsq decide a2)
  -> lh,la = ((total+margin)/2,(total-margin)/2) ; total = burn-in mean(gh+ga) [constant, same for
     both models -> isolates the margin/squad effect] ; Poisson wdl ; ISOTONIC fit on burn-in
     (per model). Predict OOS. a0,a1[,a2], total and isotonic are ALL fit on BURN-IN ONLY.
  SAMPLE: international matches between two cached teams. BURN-IN = 2024, OOS = 2025 (clean calendar
  split). sup_L3 walk-forward (date<match); squad from 2023 (< both); result = target only.
  COMPARE OOS: logloss, brier, ECE, accuracy 1X2 (+ Over2.5) with PAIRED BOOTSTRAP IC95%.
  SUBGROUP: thin vs thick RECENT data — min(home,away) prior internationals in the 365d before KO
  (thin = the hypothesis's strong case: results lag squad reality).

OUTPUT (read-only): squad_quality_blend_report.txt + _metrics.csv + _rows.csv
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "scripts"))

import context_shadow_backtest as CB     # WFRatings (walk-forward L3 strengths)
import props_retest_stats_inputs as PR   # team_rates, confirmed_xi (cache loaders)
import national_elo_layer3 as L3         # Isotonic, fit weights, KMAX
import l3_offline                        # wdl (Poisson), frozen calibration

BT = ROOT / "data" / "processed" / "worldcup" / "props_backtest"
DATA = HERE / "international_results.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
REPORT = HERE / "squad_quality_blend_report.txt"
METRICS_CSV = HERE / "squad_quality_blend_metrics.csv"
ROWS_CSV = HERE / "squad_quality_blend_rows.csv"

TOPN = 14            # "first XI + close subs" proxy for the TOP-N aggregation
A_ASSIST = 0.5       # assist weight in the offensive composite
SHRINK_K = 270.0     # minutes-shrinkage prior (~3 full games): rate_eff = rate * m/(m+K). Collapses
#                      minnow FLUKE /90 rates (1 goal in 20 min -> g90=4.5) toward 0 -> kills the
#                      small-sample noise that made tiny nations top the raw ranking. K=0 -> raw.
BURNIN_YEAR = 2024
OOS_YEAR = 2025
MIN_MINUTES = 1.0    # ignore 0-minute cache entries in the weighted mean
RES_IDX = {"H": 0, "D": 1, "A": 2}


# --------------------------------------------------------------- player pool & squad strength
def load_pool():
    """{tid: {pid: rate}} for all cached 2023 teams, plus pooled z-transforms of g90/a90."""
    teams = {}
    g90_all, a90_all = [], []
    for f in os.listdir(BT):
        m = re.match(r"rates_team(\d+)_s2023\.json", f)
        if not m:
            continue
        tid = int(m.group(1))
        d = json.loads((BT / f).read_text(encoding="utf-8"))
        rates = {int(k): v for k, v in (d or {}).items()}
        teams[tid] = rates
        for v in rates.values():
            mins = float(v.get("minutes", 0.0))
            if mins >= MIN_MINUTES:
                sk = mins / (mins + SHRINK_K)   # same minutes-shrinkage as squad_strength
                g90_all.append(float(v.get("g90", 0.0)) * sk)
                a90_all.append(float(v.get("a90", 0.0)) * sk)
    g90_all = np.array(g90_all); a90_all = np.array(a90_all)
    gm, gs = g90_all.mean(), g90_all.std() or 1.0
    am, as_ = a90_all.mean(), a90_all.std() or 1.0
    return teams, (gm, gs, am, as_)


def squad_strength(rates, z, mode, pids=None):
    """Team squad strength from 2023 rates. mode: 'avg' (minutes-weighted over roster) | 'topN'
    (mean of TOPN most-played) | 'min' (minutes-weighted, NO offense -> pure role/depth control) |
    'xi' (minutes-weighted over the given XI pids). q_p = z(g90)+A_ASSIST*z(a90)."""
    gm, gs, am, as_ = z
    items = []
    for pid, v in rates.items():
        mins = float(v.get("minutes", 0.0))
        if mins < MIN_MINUTES:
            continue
        if pids is not None and pid not in pids:
            continue
        # minutes-shrunk rates (empirical-Bayes toward 0): a player with few minutes can't earn an
        # extreme /90 -> removes the minnow small-sample artifact. Then standardise over the pool.
        sk = mins / (mins + SHRINK_K)
        g = float(v.get("g90", 0.0)) * sk
        a = float(v.get("a90", 0.0)) * sk
        q = (g - gm) / gs + A_ASSIST * (a - am) / as_
        items.append((mins, q))
    if not items:
        return None
    items.sort(key=lambda t: -t[0])
    if mode == "topN":
        sel = items[:TOPN]
        return float(np.mean([q for _, q in sel]))
    if mode == "min":
        # control: minutes-weighted mean of a CONSTANT 1.0 -> collapses to 0 info; instead use the
        # minutes CONCENTRATION (top-N share) as a non-offense squad signal (depth/cohesion proxy).
        mins = np.array([m for m, _ in items])
        return float(mins[:TOPN].sum() / mins.sum())
    w = np.array([m for m, _ in items]); q = np.array([qq for _, qq in items])
    return float((w * q).sum() / w.sum())   # 'avg' and 'xi'


# --------------------------------------------------------------- recent-data depth (subgroup cut)
def recent_counts(ir):
    """fn(tid,date)->#internationals for tid in the 365d before date (leak-free, strictly <)."""
    rows = []
    for _, r in ir.iterrows():
        rows.append((int(r["home_id"]), r["date"]))
        rows.append((int(r["away_id"]), r["date"]))
    df = pd.DataFrame(rows, columns=["tid", "date"]).sort_values("date")
    by = {t: g["date"].to_numpy() for t, g in df.groupby("tid")}

    def fn(tid, date):
        d = by.get(int(tid))
        if d is None:
            return 0
        lo = date - np.timedelta64(365, "D")
        return int(((d >= lo) & (d < date)).sum())
    return fn


# --------------------------------------------------------------- L3 functional form (faithful)
def fit_predict(margin_cols, burn, oos, gh, ga, total_burn):
    """margin = lstsq(X, gh-ga) on burn; lh,la from constant total; Poisson wdl; isotonic on burn.
    Returns OOS probability matrix P (len(oos)x3) and the fitted coefficients."""
    Xb = np.column_stack([margin_cols[c][burn] for c in margin_cols])
    Xo = np.column_stack([margin_cols[c][oos] for c in margin_cols])
    yb = (gh - ga)[burn]
    coef, *_ = np.linalg.lstsq(Xb, yb, rcond=None)
    mb = Xb @ coef; mo = Xo @ coef

    def probs(margin):
        lh = np.maximum(0.05, (total_burn + margin) / 2.0)
        la = np.maximum(0.05, (total_burn - margin) / 2.0)
        return np.array([l3_offline.wdl(lh[i], la[i]) for i in range(len(margin))])
    Pb = probs(mb); Po = probs(mo)
    res_b = np.where(gh[burn] > ga[burn], 0, np.where(gh[burn] == ga[burn], 1, 2))
    Yb = np.eye(3)[res_b]
    isos = [L3.Isotonic().fit(Pb[:, k], Yb[:, k]) for k in range(3)]
    Pc = np.column_stack([isos[k].predict(Po[:, k]) for k in range(3)])
    Pc = np.clip(Pc, 1e-6, None); Pc /= Pc.sum(1, keepdims=True)
    return Pc, coef


# --------------------------------------------------------------- scoring
def _ll(P, Y):
    Pc = np.clip(P, 1e-15, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
    return -np.sum(Y * np.log(Pc), axis=1)


def _br(P, Y):
    Pc = np.clip(P, 1e-15, 1.0); Pc = Pc / Pc.sum(1, keepdims=True)
    return np.sum((Pc - Y) ** 2, axis=1)


def _ece(P, Y, bins=10):
    conf = P.max(1); corr = (P.argmax(1) == Y.argmax(1)).astype(float)
    edges = np.linspace(0, 1, bins + 1); e = 0.0
    for i in range(bins):
        m = (conf > edges[i]) & (conf <= edges[i + 1])
        if m.sum():
            e += m.sum() / len(P) * abs(conf[m].mean() - corr[m].mean())
    return float(e)


def paired_boot(d, seed=20260626, nboot=20000):
    rng = np.random.RandomState(seed)
    idx = rng.randint(0, len(d), (nboot, len(d)))
    bd = d[idx].mean(1)
    return float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5)), float((bd > 0).mean())


def run():
    ir = pd.read_csv(DATA)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
    ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga", "home", "away"]).copy()
    ir["home_id"] = ir["home_id"].astype(int); ir["away_id"] = ir["away_id"].astype(int)
    ir = ir.sort_values("date").reset_index(drop=True)

    teams, z = load_pool()
    cached = set(teams.keys())
    wf = CB.WFRatings(ir)            # walk-forward L3 strengths (leak-free)
    rc = recent_counts(ir)

    # candidate sample: matches in {burn-in, oos} years between two cached teams
    yr = ir["date"].dt.year
    samp = ir[(yr.isin([BURNIN_YEAR, OOS_YEAR])) &
              ir["home_id"].isin(cached) & ir["away_id"].isin(cached)].copy()

    # precompute squad strengths per team for each aggregation
    strum = {}
    for mode in ("avg", "topN", "min"):
        strum[mode] = {tid: squad_strength(teams[tid], z, mode) for tid in cached}

    rows = []
    for r in samp.itertuples(index=False):
        date = r.date
        S = wf.strengths_by_name(date)
        if not S or r.home not in S or r.away not in S:
            continue
        sup = S[r.home] - S[r.away]
        rec = {"fixture_id": int(r.fixture_id), "date": str(date)[:10], "year": int(date.year),
               "home": r.home, "away": r.away, "home_id": int(r.home_id), "away_id": int(r.away_id),
               "gh": float(r.gh), "ga": float(r.ga), "sup_l3": float(sup),
               "res": ("H" if r.gh > r.ga else ("D" if r.gh == r.ga else "A")),
               "recent_min": min(rc(r.home_id, date), rc(r.away_id, date))}
        ok = True
        for mode in ("avg", "topN", "min"):
            sh = strum[mode].get(int(r.home_id)); sa = strum[mode].get(int(r.away_id))
            if sh is None or sa is None:
                ok = False; break
            rec[f"sqd_{mode}"] = sh - sa
        if ok:
            rows.append(rec)

    df = pd.DataFrame(rows)
    lines = []

    def out(s=""):
        print(s); lines.append(s)

    out("=" * 100)
    out("SQUAD-QUALITY (jugadores) BLEND con L3 — ¿añade poder predictivo OOS al 1X2/goles? READ-ONLY")
    out("=" * 100)
    out("fuerza-por-jugadores: compuesto OFENSIVO de tasas /90 de SELECCIÓN 2023 (escala internacional")
    out(f"común -> sin problema de comparabilidad entre ligas). q_p=z(g90)+{A_ASSIST}*z(a90). Agregación:")
    out(f"  avg = media ponderada por minutos sobre la plantilla; topN = media de los {TOPN} con más minutos;")
    out("  min = concentración de minutos top-N (señal NO ofensiva: profundidad/cohesión, control).")
    out("LIMITACIÓN honesta: g90/a90 son ofensivos (defensas/porteros puntúan bajo); minutos corrigen")
    out("parcialmente por rol. games.rating NO está en caché y traerlo costaría API (cuota=rojo) -> compuesto.")
    out("")
    out(f"equipos con rates 2023 en caché: {len(cached)}")
    if df.empty:
        out("Sin filas utilizables."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return
    burn = df[df["year"] == BURNIN_YEAR]; oos = df[df["year"] == OOS_YEAR]
    out(f"muestra: {len(df)} partidos (entre 2 equipos cacheados, con L3 walk-forward).")
    out(f"  BURN-IN {BURNIN_YEAR}: {len(burn)}  |  OOS {OOS_YEAR}: {len(oos)}")
    out(f"correlación sup_L3 ~ sqd_avg (toda la muestra): r={df['sup_l3'].corr(df['sqd_avg']):+.3f} "
        f"(alta r -> el L3 ya contiene gran parte de la calidad de plantilla)")
    out("")

    gh = df["gh"].to_numpy(float); ga = df["ga"].to_numpy(float)
    bmask = (df["year"] == BURNIN_YEAR).to_numpy()
    omask = (df["year"] == OOS_YEAR).to_numpy()
    total_burn = float((gh + ga)[bmask].mean())
    yo = df["res"].map(RES_IDX).to_numpy(int)[omask]
    Yo = np.eye(3)[yo]
    sup = df["sup_l3"].to_numpy(float)
    ones = np.ones(len(df))

    metrics = []

    def eval_model(name, cols):
        P, coef = fit_predict(cols, bmask, omask, gh, ga, total_burn)
        ll = _ll(P, Yo); br = _br(P, Yo); ece = _ece(P, Yo); acc = float((P.argmax(1) == yo).mean())
        return {"name": name, "P": P, "coef": coef, "ll": ll.mean(), "br": br.mean(),
                "ece": ece, "acc": acc, "ll_v": ll, "br_v": br}

    base = eval_model("baseline [sup_L3]", {"1": ones, "sup": sup})
    out("-" * 100)
    out("1X2 OOS — BASELINE (sólo supremacía L3) vs CANDIDATO (+ diferencial de plantilla). a2 aprendido en burn-in.")
    out("-" * 100)
    hdr = f"  {'modelo':30} {'logloss':>8} {'brier':>8} {'ECE':>7} {'acc%':>6} {'a2 (peso plantilla)':>22}"
    out(hdr); out("  " + "-" * (len(hdr) - 2))
    out(f"  {'baseline [sup_L3]':30} {base['ll']:>8.5f} {base['br']:>8.5f} {base['ece']:>7.4f} "
        f"{base['acc']*100:>5.1f}% {'—':>22}")

    for mode, lbl in (("avg", "+sqd_avg (min-weighted)"), ("topN", f"+sqd_top{TOPN}"),
                      ("min", "+sqd_min (no-offense ctrl)")):
        sq = df[f"sqd_{mode}"].to_numpy(float)
        cand = eval_model(f"cand {mode}", {"1": ones, "sup": sup, "sqd": sq})
        a2 = cand["coef"][2]
        d_ll = base["ll_v"] - cand["ll_v"]   # >0 = candidate better
        d_br = base["br_v"] - cand["br_v"]
        lo, hi, p = paired_boot(d_ll)
        blo, bhi, bp = paired_boot(d_br)
        sig = "SIGNIF" if (lo > 0 or hi < 0) else "no signif"
        out(f"  {lbl:30} {cand['ll']:>8.5f} {cand['br']:>8.5f} {cand['ece']:>7.4f} "
            f"{cand['acc']*100:>5.1f}% {a2:>+22.4f}")
        out(f"     Δlogloss(base−cand) mean={d_ll.mean():+.5f} IC95[{lo:+.5f},{hi:+.5f}] P(Δ>0)={p*100:.0f}% -> {sig}"
            f"  | Δbrier mean={d_br.mean():+.5f} IC95[{blo:+.5f},{bhi:+.5f}]")
        metrics.append({"prop": "1x2", "model": mode, "n_oos": int(omask.sum()),
                        "ll_base": base["ll"], "ll_cand": cand["ll"], "br_base": base["br"],
                        "br_cand": cand["br"], "ece_base": base["ece"], "ece_cand": cand["ece"],
                        "acc_base": base["acc"], "acc_cand": cand["acc"], "a2": float(a2),
                        "d_ll_mean": float(d_ll.mean()), "ic_lo": lo, "ic_hi": hi,
                        "p_dgt0": p, "signif": bool(lo > 0 or hi < 0)})
    out("")

    # ---- SUBGROUP: thin vs thick recent data (hypothesis is strongest when results lag squad) ----
    out("-" * 100)
    out("SUBGRUPO: ¿ayuda MÁS con POCOS partidos recientes? (min(local,visit) internacionales en 365d previos)")
    out("-" * 100)
    thr = int(np.median(df["recent_min"]))
    out(f"  umbral (mediana recent_min) = {thr}.  thin = recent_min <= {thr};  thick = > {thr}.")
    sq_avg = df["sqd_avg"].to_numpy(float)
    cand_avg = eval_model("cand avg", {"1": ones, "sup": sup, "sqd": sq_avg})
    rec_oos = df["recent_min"].to_numpy(int)[omask]
    for cutname, cmask in (("thin (pocos)", rec_oos <= thr), ("thick (muchos)", rec_oos > thr)):
        if cmask.sum() < 10:
            out(f"  {cutname:16} n={int(cmask.sum())} (muestra muy chica, omitido)"); continue
        d_ll = (base["ll_v"] - cand_avg["ll_v"])[cmask]
        lo, hi, p = paired_boot(d_ll)
        sig = "SIGNIF" if (lo > 0 or hi < 0) else "no signif"
        out(f"  {cutname:16} n={int(cmask.sum()):>3}  ll_base={base['ll_v'][cmask].mean():.5f} "
            f"ll_cand={cand_avg['ll_v'][cmask].mean():.5f}  Δll={d_ll.mean():+.5f} "
            f"IC95[{lo:+.5f},{hi:+.5f}] P(Δ>0)={p*100:.0f}% -> {sig}")
        metrics.append({"prop": "1x2_subgroup", "model": cutname, "n_oos": int(cmask.sum()),
                        "ll_base": float(base["ll_v"][cmask].mean()),
                        "ll_cand": float(cand_avg["ll_v"][cmask].mean()),
                        "d_ll_mean": float(d_ll.mean()), "ic_lo": lo, "ic_hi": hi,
                        "p_dgt0": p, "signif": bool(lo > 0 or hi < 0)})
    out("")

    # ---- Over 2.5 (secondary): same margin models drive a total via burn-in; OU from Poisson ----
    # (total constant = burn mean; squad affects only the margin -> OU effect is indirect/small.)
    out("-" * 100)
    out("Over 2.5 (secundario): el total es constante (media burn-in) e igual para ambos modelos -> el")
    out("diferencial de plantilla sólo mueve el reparto local/visitante, no el total. Se reporta por")
    out("completitud; el 1X2 es el test principal de la hipótesis.")
    real_over = ((gh + ga)[omask] >= 3).astype(int)
    out(f"  real Over2.5 OOS = {real_over.mean()*100:.0f}%  (n={len(real_over)})  "
        f"(total constante burn-in = {total_burn:.3f} -> P(Over) idéntica entre modelos; sin señal added)")
    out("")

    out("=" * 100)
    best = max((m for m in metrics if m["prop"] == "1x2"), key=lambda m: m["d_ll_mean"])
    verdict = ("AÑADE señal (Δll>0 con IC95% que excluye 0)" if best["signif"] and best["d_ll_mean"] > 0
               else "NO añade señal OOS distinguible (IC95% incluye 0) -> el L3 ya la captura")
    out(f"VEREDICTO 1X2 (mejor agregación = {best['model']}): {verdict}.")
    out(f"  a2={best['a2']:+.4f}, Δlogloss OOS={best['d_ll_mean']:+.5f}, IC95[{best['ic_lo']:+.5f},{best['ic_hi']:+.5f}].")
    out("=" * 100)

    df.to_csv(ROWS_CSV, index=False)
    pd.DataFrame(metrics).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}\nWritten: {ROWS_CSV}")


if __name__ == "__main__":
    run()
