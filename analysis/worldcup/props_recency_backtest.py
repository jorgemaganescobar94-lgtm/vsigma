"""
PLAYER GOAL-PROP · RECENCY / IN-TOURNAMENT FORM re-test (READ-ONLY · NO API · NO production · NO commit).

QUESTION (Jorge): the production goal props use a FIXED window RATE_SEASONS=[2024,2025] and IGNORE the
in-progress tournament. Does incorporating RECENT / in-tournament goal form improve the goal prop, or
does the more-stable fixed window predict as well or better? The data decides; if the fixed window ties
or wins, we CLOSE it and touch nothing — even though "include the tournament" feels right.

WHY THIS SAMPLE IS A FAIR TEST. The historical props backtest window (Jan–Jun 2024) is full of
TOURNAMENTS (AFCON, Asian Cup, WCQ). A player's 3rd AFCON match is exactly analogous to a WC match with
two group games already played: the in-window accumulator gives leak-free "in-tournament form". So the
2024 tournaments stand in for the 2026 WC in progress.

REUSE, NOT REIMPLEMENT. XI = PR.confirmed_xi (cached confirmed lineups). Prior rates = PR.team_rates
(the 2023 prior-season /90 aggregate — the FIXED-window baseline, strictly pre-2024 = anti-leakage).
Team xG = l3_offline.raw_xg with the frozen calibration + CB.WFRatings walk-forward L3 strengths (same
as props_matchup_backtest). Per-player λ_goal + p_goal + logloss/brier = PP.predict_fixture / PP._logloss
/ PP._brier / PP.poisson_p_ge1 (the production prop math, incl. the EB XI-share shrinkage). The ONLY
thing added is HOW each player's g90 rate is formed before it enters predict_fixture.

VARIANTS (walk-forward, STRICT anti-leakage: fixture M uses ONLY fixtures with date < M):
  V0 (baseline = PRODUCTION method): fixed prior g90 (2023 aggregate), unchanged.
  V1 (direct fix): pool prior + in-window form by minutes -> combined g90 (same EB XI-share shrinkage).
  V2 (principled): blend in-window form toward the prior with a RECENCY strength K:
        w = win_min/(win_min+K);  g90_eff = w·g90_window + (1−w)·g90_prior.
     K tuned ONLY on the TRAIN split; several K probed. K→∞ ≡ V0; K→0 ≡ trust recent form fully.

METRIC: logloss + brier of p_goal (P(scores≥1) vs real) over ALL OOS player-matches. Paired bootstrap
CI95 over >=8 seeds. STRICT GATE (same rigour as DC / calibration re-tests): adopt V1/V2 ONLY if it beats
V0 on the OOS with a CI95 that CLEARLY excludes 0 (comfortable margin) AND robust across seeds. Else CLOSE.

OUTPUT: props_recency_backtest_report.txt + props_recency_backtest_metrics.csv + props_recency_backtest_CONCLUSION.md
Extra (illustrative, NOT decisive): if a variant passes, apply it to TODAY's WC fixtures (Lautaro/Messi+).
NO betting endpoints, no secrets.
"""
from __future__ import annotations

import copy
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

import props_retest_stats_inputs as PR     # confirmed_xi, team_rates (cache loaders)
import worldcup_player_props as PP         # predict_fixture, poisson_p_ge1, _logloss/_brier/_ece, _num
import context_shadow_backtest as CB       # WFRatings (walk-forward L3 strengths)
import l3_offline                          # raw_xg + frozen calibration

BT = ROOT / "data" / "processed" / "worldcup" / "props_backtest"
INT_RESULTS = HERE / "international_results.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
REPORT = HERE / "props_recency_backtest_report.txt"
METRICS_CSV = HERE / "props_recency_backtest_metrics.csv"
CONCLUSION = HERE / "props_recency_backtest_CONCLUSION.md"

K_GRID = [90.0, 180.0, 270.0, 450.0, 720.0, 1080.0, 2160.0]   # V2 recency strengths (min); large≈V0
SEEDS = [20260707, 1, 7, 42, 101, 2718, 31337, 99991, 424242, 20260705]
BOOT_N = 20000
CLEAR_MARGIN = 0.002   # comfortable margin for goal-prop logloss (base rate ~8%, ll~0.27); scale below DC's
                       # 0.005 (goals-market ll~0.68) but still "clearly not grazing 0". Significance
                       # (all-seeds lo>0) reported separately so a small-but-real effect is visible.
XI_ATTR = float(PP.XI_ATTR)


def player_actuals_goals_minutes(fid):
    """{pid: (goal01, minutes)} from cached /fixtures/players (mirrors cmd_settle parsing)."""
    p = BT / f"fxplayers_{fid}.json"
    if not p.exists():
        return {}
    store = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for t in (store or []):
        for pl in (t.get("players") or []):
            pid = (pl.get("player") or {}).get("id")
            sblk = (pl.get("statistics") or [{}])[0]
            g = sblk.get("games") or {}; gl = sblk.get("goals") or {}
            if pid is None:
                continue
            out[int(pid)] = (1 if PP._num(gl.get("total")) > 0 else 0, PP._num(g.get("minutes")))
    return out


def _variant_rates(rates0, xi, wacc, mode, K=None):
    """Return a rates dict (copy of rates0) with each XI player's g90/minutes rebuilt per variant.
    mode: 'V0' (unchanged) | 'V1' (pool by minutes) | 'V2' (K-blend toward prior)."""
    if mode == "V0":
        return rates0
    rv = copy.deepcopy(rates0)
    for pid in xi:
        r = rv.get(pid, {})
        pm = float(r.get("minutes", 0.0)); pg90 = float(r.get("g90", 0.0))
        pgoals = pg90 * pm / 90.0
        wg, wm = wacc.get(pid, (0.0, 0.0))
        if wm <= 0:
            continue  # no in-window form -> identical to V0 for this player
        if mode == "V1":
            comb_min = pm + wm
            g90_new = (pgoals + wg) / (comb_min / 90.0) if comb_min > 0 else 0.0
            r["g90"] = g90_new; r["minutes"] = comb_min
        else:  # V2
            wg90 = wg / (wm / 90.0)
            w = wm / (wm + K)
            r["g90"] = w * wg90 + (1.0 - w) * pg90
            r["minutes"] = pm + wm
        rv[pid] = r
    return rv


def build_rows():
    ir = pd.read_csv(INT_RESULTS)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
    ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
    ir["home_id"] = ir["home_id"].astype(int); ir["away_id"] = ir["away_id"].astype(int)
    ir_by_fid = ir.set_index("fixture_id")
    wf = CB.WFRatings(ir.sort_values("date").reset_index(drop=True))
    calib = json.loads(CALIB.read_text(encoding="utf-8"))
    a0, a1, tm = calib["a0"], calib["a1"], calib["total_mean"]

    fids = sorted(int(re.match(r"lineup_(\d+)", f).group(1))
                  for f in os.listdir(BT) if f.startswith("lineup_"))
    # order fixtures by date so the in-window accumulator is strictly leak-free
    dated = [(ir_by_fid.loc[fid]["date"], fid) for fid in fids if fid in ir_by_fid.index]
    dated.sort()

    wacc = {}          # pid -> (window_goals, window_minutes) from fixtures strictly BEFORE current
    rows = []
    used = 0
    for date, fid in dated:
        rr = ir_by_fid.loc[fid]
        hid, aid = int(rr["home_id"]), int(rr["away_id"])
        hname, aname = str(rr["home"]), str(rr["away"])
        strengths = wf.strengths_by_name(date)
        act = player_actuals_goals_minutes(fid)
        if strengths and hname in strengths and aname in strengths and act:
            sup = strengths[hname] - strengths[aname]
            xg_home, xg_away = l3_offline.raw_xg(sup, a0, a1, tm)   # neutral team xG (L3 walk-forward)
            for tid, team_xg in ((hid, xg_home), (aid, xg_away)):
                xi = PR.confirmed_xi(fid, tid)
                if not xi:
                    continue
                rates0 = PR.team_rates(tid)
                # λ_goal per variant (reuse production predict_fixture verbatim)
                lam = {}
                lam["V0"] = {p["player_id"]: p["lam_goal"]
                             for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi, _variant_rates(rates0, xi, wacc, "V0"))}
                lam["V1"] = {p["player_id"]: p["lam_goal"]
                             for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi, _variant_rates(rates0, xi, wacc, "V1"))}
                for K in K_GRID:
                    lam[f"V2_{K:.0f}"] = {p["player_id"]: p["lam_goal"]
                                          for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi, _variant_rates(rates0, xi, wacc, "V2", K))}
                for pid in xi:
                    if pid not in act:
                        continue
                    y, _mins = act[pid]
                    wg, wm = wacc.get(pid, (0.0, 0.0))
                    row = {"fixture_id": fid, "date": date, "team_id": tid, "player_id": pid,
                           "y_goal": int(y), "window_min": float(wm), "treated": int(wm > 0)}
                    for k, d in lam.items():
                        row[f"lam_{k}"] = float(d.get(pid, 0.0))
                    rows.append(row)
            used += 1
        # UPDATE accumulator AFTER predicting this fixture (strict anti-leakage)
        for pid, (yg, mn) in act.items():
            g, m = wacc.get(pid, (0.0, 0.0))
            wacc[pid] = (g + yg, m + mn)   # note: goals counted as 0/1 scored (matches the target proxy)
    return pd.DataFrame(rows), used


# --------------------------------------------------------------- metrics
def ll_vec(p, y):
    p = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15); y = np.asarray(y, float)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def multiseed_boot(d, seeds=SEEDS, nb=BOOT_N):
    per = []
    for s in seeds:
        rng = np.random.RandomState(s)
        idx = rng.randint(0, len(d), (nb, len(d)))
        bd = d[idx].mean(1)
        per.append((float(np.percentile(bd, 2.5)), float(np.percentile(bd, 97.5))))
    los = np.array([x[0] for x in per]); his = np.array([x[1] for x in per])
    return dict(mean=float(d.mean()), min_lo=float(los.min()), max_hi=float(his.max()),
                all_lo_pos=bool((los > 0).all()), all_hi_neg=bool((his < 0).all()))


def verdict(agg):
    if agg["all_hi_neg"]:
        return "PEOR que V0 (IC excluye 0 por debajo)"
    if agg["mean"] > 0 and agg["all_lo_pos"] and agg["min_lo"] >= CLEAR_MARGIN:
        return "ADOPTAR (bate a V0 con margen y robusto)"
    if agg["mean"] > 0 and agg["all_lo_pos"]:
        return f"FRÁGIL — IC roza 0 (min_lo=+{agg['min_lo']:.5f} < {CLEAR_MARGIN}) -> NO adoptar"
    return "NO adoptar (IC incluye 0)"


def p_from_lam(df, col):
    return 1.0 - np.exp(-df[col].to_numpy(float))


def run():
    df, used = build_rows()
    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 104)
    out("PROPS DE GOL · RECENCIA / FORMA DE TORNEO — walk-forward anti-leakage · READ-ONLY · sin API · sin prod")
    out("=" * 104)
    if df.empty:
        out("Sin filas. Abortado."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return

    # time split for tuning V2's K (train = earlier half of fixtures by date)
    fdates = df[["fixture_id", "date"]].drop_duplicates().sort_values("date")
    cut = fdates.iloc[len(fdates) // 2]["date"]
    df["split"] = np.where(df["date"] < cut, "train", "test")
    tr = df[df["split"] == "train"]; te = df[df["split"] == "test"]
    y_te = te["y_goal"].to_numpy(int)

    out(f"partidos usados={used} | filas jugador-gol={len(df)} | base rate gol={df['y_goal'].mean()*100:.1f}%")
    out(f"filas con FORMA intra-ventana (treated, window_min>0)={int(df['treated'].sum())} "
        f"({df['treated'].mean()*100:.1f}%)  ·  positivos treated={int(df.loc[df['treated']==1,'y_goal'].sum())}")
    out(f"split temporal: train<{pd.Timestamp(cut).date()}<=test | train={len(tr)} filas · test(OOS)={len(te)} filas")
    out(f"K probados (V2, min): {[int(k) for k in K_GRID]}  ·  semillas bootstrap={len(SEEDS)}  ·  margen gate={CLEAR_MARGIN}")
    out("")

    # tune K* on TRAIN (min logloss over ALL train rows)
    y_tr = tr["y_goal"].to_numpy(int)
    ll_tr = {K: PP._logloss(np.clip(1 - np.exp(-tr[f"lam_V2_{K:.0f}"].to_numpy(float)), 1e-15, 1 - 1e-15), y_tr)
             for K in K_GRID}
    Kstar = min(ll_tr, key=ll_tr.get)
    out("--- ajuste de K (V2) SOLO en train (logloss train por K) ---")
    for K in K_GRID:
        mark = "  <- K* óptimo" if K == Kstar else ""
        out(f"    K={int(K):5d}min  logloss_train={ll_tr[K]:.6f}{mark}")
    out(f"  K* (recencia óptima, tuneada en train) = {int(Kstar)} min  (w=win_min/(win_min+K*))")
    out("")

    # evaluate on TEST (OOS). variants: V0, V1, V2(K*)
    variant_cols = {"V0 (producción)": "lam_V0", "V1 (pool minutos)": "lam_V1",
                    f"V2 (K*={int(Kstar)})": f"lam_V2_{Kstar:.0f}"}
    p0 = np.clip(p_from_lam(te, "lam_V0"), 1e-15, 1 - 1e-15)
    d0 = ll_vec(p0, y_te)
    out("-" * 104)
    out(f"[OOS = test] n={len(te)}  (base rate gol={y_te.mean()*100:.1f}%)  · Δlogloss(V0−Vx)>0 => Vx mejor")
    out("-" * 104)
    out(f"  {'variante':20} {'logloss':>9} {'brier':>8} {'Δlogloss medio':>15} {'IC95[min_lo..max_hi]':>26} {'veredicto'}")
    metric_rows = []
    for label, col in variant_cols.items():
        p = np.clip(p_from_lam(te, col), 1e-15, 1 - 1e-15)
        ll = PP._logloss(p, y_te); br = PP._brier(p, y_te)
        if col == "lam_V0":
            out(f"  {label:20} {ll:>9.5f} {br:>8.5f} {'(baseline)':>15} {'':>26} —")
            metric_rows.append(dict(variant=label, n=len(te), logloss=ll, brier=br,
                                    delta_mean=0.0, ci_min_lo=np.nan, ci_max_hi=np.nan, verdict="baseline"))
            continue
        d = d0 - ll_vec(p, y_te)
        agg = multiseed_boot(d); vd = verdict(agg)
        out(f"  {label:20} {ll:>9.5f} {br:>8.5f} {agg['mean']:>+15.5f} "
            f"[{agg['min_lo']:+.5f}..{agg['max_hi']:+.5f}] {vd}")
        metric_rows.append(dict(variant=label, n=len(te), logloss=ll, brier=br, delta_mean=agg["mean"],
                                ci_min_lo=agg["min_lo"], ci_max_hi=agg["max_hi"], verdict=vd))
    out("")

    # TREATED-ONLY subset (where the variants actually differ) — informative, NOT the gate
    tem = te[te["treated"] == 1]
    if len(tem) >= 20:
        ym = tem["y_goal"].to_numpy(int)
        p0m = np.clip(p_from_lam(tem, "lam_V0"), 1e-15, 1 - 1e-15); d0m = ll_vec(p0m, ym)
        out(f"  [subconjunto TREATED del test] n={len(tem)} (solo filas con forma intra-ventana; aquí vive el efecto):")
        for label, col in variant_cols.items():
            if col == "lam_V0":
                out(f"     {label:20} logloss={PP._logloss(p0m, ym):.5f} (ref)"); continue
            pm = np.clip(p_from_lam(tem, col), 1e-15, 1 - 1e-15)
            dm = d0m - ll_vec(pm, ym); aggm = multiseed_boot(dm)
            out(f"     {label:20} logloss={PP._logloss(pm, ym):.5f}  Δ={aggm['mean']:+.5f} "
                f"IC95[{aggm['min_lo']:+.5f}..{aggm['max_hi']:+.5f}] {'(signif)' if aggm['all_lo_pos'] or aggm['all_hi_neg'] else '(IC∋0)'}")
    else:
        out(f"  [subconjunto TREATED del test] n={len(tem)} < 20: muestra insuficiente para bootstrap fiable.")
    out("")
    out("=" * 104)
    out("GATE: ADOPTAR sólo si Δlogloss(V0−Vx)>0 en OOS con IC95 que excluye 0 con margen (>=+" + f"{CLEAR_MARGIN}) y robusto.")
    out("HONESTIDAD: si la ventana fija empata/gana o el efecto roza 0 => cerrar, NO tocar producción.")
    out("=" * 104)

    pd.DataFrame(metric_rows).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}")

    # ---- CONCLUSION.md ----
    mr = pd.DataFrame(metric_rows)
    passed = [r for _, r in mr.iterrows() if str(r["verdict"]).startswith("ADOPTAR")]
    md = ["# Props de gol — recencia / forma de torneo: veredicto\n",
          "**Read-only · sin API · sin commit · sin tocar producción.** ¿Incorporar la forma reciente/del",
          "torneo a las props de gol mejora sobre la ventana fija `RATE_SEASONS=[2024,2025]`? Test walk-forward",
          "anti-leakage sobre el backtest histórico de props (torneos 2024 = análogo del Mundial en curso).\n",
          f"- Muestra: {len(df)} jugador-partido · base rate gol {df['y_goal'].mean()*100:.1f}% · "
          f"{int(df['treated'].sum())} filas con forma intra-ventana ({df['treated'].mean()*100:.1f}%).",
          f"- OOS (test temporal): {len(te)} filas. K* recencia (tuneado SOLO en train) = **{int(Kstar)} min**.\n",
          "## Veredicto por variante (juez = OOS test)\n",
          "| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |",
          "|---|---|---|---|---|"]
    for _, r in mr.iterrows():
        if r["variant"].startswith("V0"):
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | (baseline) | — | — |")
        else:
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | {r['delta_mean']:+.5f} | "
                      f"[{r['ci_min_lo']:+.5f}..{r['ci_max_hi']:+.5f}] | {r['verdict']} |")
    md.append("\n## Recomendación\n")
    if passed:
        md.append(f"- **{', '.join(r['variant'] for r in passed)}** supera(n) el gate estricto en OOS. "
                  "Candidata(s) — requiere aprobación 🔴 de Jorge (tocaría la ventana de las props). NO aplicado.")
    else:
        md.append("- **Ninguna variante** supera el gate estricto en el OOS. La ventana fija (más estable) predice")
        md.append("  igual o mejor que perseguir la forma reciente: el efecto no excluye 0 con claridad. Coherente con")
        md.append("  que la forma intra-torneo es muestra pequeña y ruidosa (rachas que regresan a la media).")
        md.append("  **Recomendación: cerrar. Mantener V0 (`RATE_SEASONS` fija) sin cambios.** El dato decide, no la intuición.")
    md.append("\n_Artefactos: props_recency_backtest_report.txt · props_recency_backtest_metrics.csv · este CONCLUSION.md. "
              "No se tocó worldcup_player_props.py ni RATE_SEASONS._")
    CONCLUSION.write_text("\n".join(md), encoding="utf-8")
    print(f"Written: {CONCLUSION}")
    return mr, Kstar, bool(passed)


if __name__ == "__main__":
    run()
