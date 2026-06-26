"""
MARGINAL VALUE of MATCHUP GRANULARITY on the GOAL/ASSIST player props (READ-ONLY · NO production).

Question: the current (validated) method is  λ_player = team_xG(L3) × player_share.  The TEAM xG
already reflects facing a weak opponent (L3 supremacy). The hypothesis under test is the INTERACTION:
do ELITE players exploit WEAK defences MORE than proportionally — i.e. beyond what the team xG already
predicts? If the team xG already captures it, the interaction adds nothing; if the hypothesis holds,
it improves goal/assist over the CURRENT method.

It does NOT duplicate logic: it reuses the props backtest cache + helpers (props_retest_stats_inputs
.confirmed_xi/.team_rates), the production prop math (worldcup_player_props.predict_fixture, which
already returns the per-player λ_goal/λ_assist, + poisson_p_ge1/_logloss/_brier/_ece) and the
walk-forward L3 ratings (context_shadow_backtest.WFRatings) + frozen L3 calibration. The ONLY thing
added is an explicit interaction factor on the player's λ; everything else is identical to the
current method.

BASELINE = the current method (the already-graduated goal/assist props): p = 1−exp(−λ_base) where
λ_base = predict_fixture's λ_goal/λ_assist (= team_xG(L3) × share × XI_ATTR).

MATCHUP variants (explicit, fixed hypotheses — β NOT fit on the test):
  λ_match = λ_base × max(0, 1 + β · z_off · z_weak)
    z_off  = standardised player offensive quality (g90 for goals, a90 for assists, prior season)
    z_weak = standardised opponent defensive WEAKNESS, two forms:
      FORM A: −L3 strength of the opponent (walk-forward)  — same signal already in team xG, re-used
              in INTERACTION with player quality (tests if the interaction adds over the main effect).
      FORM B: opponent goals-conceded per match in prior internationals (walk-forward) — a finer,
              more independent defensive measure not directly in the L3 margin rating.
  z_off·z_weak ≈ 0 on average → the factor mostly REDISTRIBUTES λ toward elite-vs-weak and away from
  elite-vs-strong; if elites really feast on weak defences beyond xG, logloss improves there.

The key test is NOT beating the base rate (the method already does) but beating the CURRENT METHOD —
the MARGINAL value of the interaction. Paired bootstrap IC95% on per-player Δlogloss/Δbrier.

ANTI-LEAKAGE: XI confirmed (observed), rates prior-season, L3 strengths + opp goals-conceded
walk-forward (date < match), target only scored. z-score means/std over the sample is a fixed
transform (documented minor look-ahead, no target leakage). NO API.

OUTPUT: props_matchup_backtest_report.txt + props_matchup_backtest_metrics.csv
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

import props_retest_stats_inputs as PR     # confirmed_xi, team_rates (cache loaders)
import worldcup_player_props as PP         # predict_fixture, poisson_p_ge1, _logloss/_brier/_ece
import context_shadow_backtest as CB       # WFRatings (walk-forward L3 strengths)
import l3_offline                          # raw_xg + frozen calibration

BT = ROOT / "data" / "processed" / "worldcup" / "props_backtest"
INT_RESULTS = HERE / "international_results.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
REPORT = HERE / "props_matchup_backtest_report.txt"
METRICS_CSV = HERE / "props_matchup_backtest_metrics.csv"

BETA = 0.25            # interaction strength (fixed hypothesis): +1SD elite vs +1SD weak -> ×(1+0.25)
BETA_SENS = [-0.25, -0.15, 0.15, 0.25, 0.40]   # sweep incl. the OPPOSITE direction (β<0)


def goal_assist_actuals(fid):
    """Per-player {pid: (goal01, assist01)} from the cached /fixtures/players (mirrors cmd_settle)."""
    p = BT / f"fxplayers_{fid}.json"
    if not p.exists():
        return {}
    store = json.loads(p.read_text(encoding="utf-8"))
    out = {}
    for t in (store or []):
        for pl in (t.get("players") or []):
            pid = (pl.get("player") or {}).get("id")
            gl = ((pl.get("statistics") or [{}])[0].get("goals") or {})
            if pid is None:
                continue
            out[int(pid)] = (1 if PP._num(gl.get("total")) > 0 else 0,
                             1 if PP._num(gl.get("assists")) > 0 else 0)
    return out


def opp_conceded_table(ir):
    """Per (team_id, date) -> mean goals conceded in PRIOR internationals (walk-forward). Returns a
    function gc(team_id, date)->float (sample mean if <3 priors). Leak-free (strictly date<match)."""
    rows = []
    for _, r in ir.iterrows():
        rows.append((int(r["home_id"]), r["date"], float(r["ga"])))   # home concedes ga
        rows.append((int(r["away_id"]), r["date"], float(r["gh"])))   # away concedes gh
    df = pd.DataFrame(rows, columns=["tid", "date", "conceded"]).sort_values("date")
    by = {t: g.reset_index(drop=True) for t, g in df.groupby("tid")}
    glob_mean = float(df["conceded"].mean())

    def gc(tid, date):
        g = by.get(int(tid))
        if g is None:
            return glob_mean
        prior = g[g["date"] < date]["conceded"]
        return float(prior.mean()) if len(prior) >= 3 else glob_mean
    return gc, glob_mean


def run():
    ir = pd.read_csv(INT_RESULTS)
    ir["date"] = pd.to_datetime(ir["date"], utc=True, errors="coerce").dt.tz_localize(None)
    ir = ir.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
    ir["home_id"] = ir["home_id"].astype(int); ir["away_id"] = ir["away_id"].astype(int)
    ir_by_fid = ir.set_index("fixture_id")

    wf = CB.WFRatings(ir.sort_values("date").reset_index(drop=True))
    calib = json.loads(CALIB.read_text(encoding="utf-8"))
    a0, a1, tm = calib["a0"], calib["a1"], calib["total_mean"]
    gc_fn, _gc_mean = opp_conceded_table(ir)

    bt_fids = sorted(int(re.match(r"lineup_(\d+)", f).group(1))
                     for f in os.listdir(BT) if f.startswith("lineup_"))

    rows = []   # per player-row dict
    used_fixtures = 0
    for fid in bt_fids:
        if fid not in ir_by_fid.index:
            continue
        rr = ir_by_fid.loc[fid]
        hid, aid = int(rr["home_id"]), int(rr["away_id"])
        hname, aname = str(rr["home"]), str(rr["away"])
        date = rr["date"]
        strengths = wf.strengths_by_name(date)
        if not strengths or hname not in strengths or aname not in strengths:
            continue
        sup = strengths[hname] - strengths[aname]
        xg_home, xg_away = l3_offline.raw_xg(sup, a0, a1, tm)   # team xG (L3 walk-forward), neutral
        s_opp = {hid: strengths[aname], aid: strengths[hname]}  # opponent strength per side
        act = goal_assist_actuals(fid)
        if not act:
            continue
        sides_ok = False
        for tid, team_xg, opp_id in ((hid, xg_home, aid), (aid, xg_away, hid)):
            xi = PR.confirmed_xi(fid, tid)
            if not xi:
                continue
            rates = PR.team_rates(tid)
            # baseline λ from the CURRENT method (predict_fixture; shots/cards args unused here -> 0)
            preds = PP.predict_fixture(team_xg, 0.0, 0.0, xi, rates)
            opp_w_strength = -float(s_opp[tid])              # weaker opponent -> higher
            opp_gc = gc_fn(opp_id, date)                     # opp goals conceded /match (walk-forward)
            for pr in preds:
                pid = pr["player_id"]
                a = act.get(pid)
                if a is None:
                    continue
                r = rates.get(pid, {})
                rows.append({
                    "fixture_id": fid, "team_id": tid, "player_id": pid,
                    "lam_goal": float(pr["lam_goal"]), "lam_assist": float(pr["lam_assist"]),
                    "g90": float(r.get("g90", 0.0)), "a90": float(r.get("a90", 0.0)),
                    "opp_w_strength": opp_w_strength, "opp_gc": float(opp_gc),
                    "y_goal": int(a[0]), "y_assist": int(a[1]),
                })
            sides_ok = True
        if sides_ok:
            used_fixtures += 1

    df = pd.DataFrame(rows)
    lines = []

    def out(s=""):
        print(s); lines.append(s)

    out("=" * 96)
    out("VALOR MARGINAL de la GRANULARIDAD DE MATCHUP en gol/asistencia — READ-ONLY, sin API")
    out("baseline = método ACTUAL ya validado (λ = xG_equipo(L3) × cuota). matchup = + interacción")
    out("=" * 96)
    out(f"partidos usados={used_fixtures} | filas jugador-prop={len(df)}")
    out(f"β (fuerza de interacción, hipótesis fija) = {BETA}")
    out("z_off = calidad ofensiva del jugador (g90/a90, temp. previa, estandarizado).")
    out("FORM A z_weak = −fuerza L3 del rival (walk-forward; mismo signal del xG, en INTERACCIÓN).")
    out("FORM B z_weak = goles encajados/partido del rival en internacionales previos (walk-forward).")
    out("")

    if df.empty:
        out("Sin filas. Abortado."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return

    def z(col):
        v = df[col].to_numpy(float)
        s = v.std()
        return (v - v.mean()) / (s if s > 0 else 1.0)

    z_g = z("g90"); z_a = z("a90")
    z_wA = z("opp_w_strength"); z_wB = z("opp_gc")

    def score(p, y):
        p = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15)
        y = np.asarray(y, float)
        ll = PP._logloss(p, y); br = PP._brier(p, y); ece = PP._ece(p, y)
        return ll, br, ece

    metrics = []

    def evaluate(prop, lam_col, z_off, beta):
        lam = df[lam_col].to_numpy(float)
        y = df[f"y_{prop}"].to_numpy(int)
        p_base = 1.0 - np.exp(-lam)
        base_rate = y.mean()
        ll_b, br_b, ece_b = score(p_base, y)
        out(f"--- {prop.upper()} (n={len(y)}, base rate={base_rate*100:.1f}%) · β={beta} ---")
        out(f"  {'método':18} {'logloss':>9} {'brier':>8} {'ECE':>7} {'Δll vs base':>12} {'sig?':>16}")
        out(f"  {'ACTUAL (baseline)':18} {ll_b:>9.5f} {br_b:>8.5f} {ece_b:>7.4f} {'—':>12} {'(ref)':>16}")
        rng = np.random.RandomState(20260626)
        for form, z_weak in (("A:−L3opp", z_wA), ("B:opp_gc", z_wB)):
            p_m = 1.0 - np.exp(-np.maximum(0.0, lam * (1.0 + beta * z_off * z_weak)))
            ll_m, br_m, ece_m = score(p_m, y)
            # per-row Δlogloss(base − matchup): >0 = matchup mejor. paired bootstrap.
            pb = np.clip(p_base, 1e-15, 1 - 1e-15); pm = np.clip(p_m, 1e-15, 1 - 1e-15)
            row_ll_b = -(y * np.log(pb) + (1 - y) * np.log(1 - pb))
            row_ll_m = -(y * np.log(pm) + (1 - y) * np.log(1 - pm))
            d = row_ll_b - row_ll_m
            idx = rng.randint(0, len(d), (10000, len(d)))
            bd = d[idx].mean(1)
            lo, hi = np.percentile(bd, 2.5), np.percentile(bd, 97.5)
            sig = "SIGNIF" if (lo > 0 or hi < 0) else "no signif (IC∋0)"
            out(f"  matchup {form:10} {ll_m:>9.5f} {br_m:>8.5f} {ece_m:>7.4f} "
                f"{'':>12} Δll(base−m)={d.mean():+.5f} IC95[{lo:+.5f},{hi:+.5f}] {sig}")
            metrics.append({"prop": prop, "beta": beta, "form": form, "n": int(len(y)),
                            "ll_base": ll_b, "ll_match": ll_m, "br_base": br_b, "br_match": br_m,
                            "ece_base": ece_b, "ece_match": ece_m,
                            "d_ll_mean": float(d.mean()), "ic_lo": float(lo), "ic_hi": float(hi),
                            "significant": bool(lo > 0 or hi < 0),
                            "match_better_pct": float((d > 0).mean())})
        out("")

    evaluate("goal", "lam_goal", z_g, BETA)
    evaluate("assist", "lam_assist", z_a, BETA)

    # β sensitivity (does ANY reasonable β help? report best Δll per prop/form)
    out("--- SENSIBILIDAD a β (Δlogloss base−matchup; >0 = matchup mejor) ---")
    out(f"  {'prop':8} {'form':10} " + " ".join(f"β={b:<5}" for b in BETA_SENS))
    for prop, z_off in (("goal", z_g), ("assist", z_a)):
        lam = df[f"lam_{prop}"].to_numpy(float); y = df[f"y_{prop}"].to_numpy(int)
        pb = np.clip(1.0 - np.exp(-lam), 1e-15, 1 - 1e-15)
        row_b = -(y * np.log(pb) + (1 - y) * np.log(1 - pb))
        for form, z_weak in (("A:−L3opp", z_wA), ("B:opp_gc", z_wB)):
            cells = []
            for b in BETA_SENS:
                pm = np.clip(1.0 - np.exp(-np.maximum(0.0, lam * (1.0 + b * z_off * z_weak))), 1e-15, 1 - 1e-15)
                row_m = -(y * np.log(pm) + (1 - y) * np.log(1 - pm))
                cells.append(f"{(row_b - row_m).mean():+.5f}")
            out(f"  {prop:8} {form:10} " + "   ".join(cells))
    out("")
    out("=" * 96)
    out("LECTURA: lo relevante es Δll(base−matchup) > 0 con IC95% que EXCLUYA 0 (valor marginal real).")
    out("Si el IC incluye 0, el xG de equipo ya captura la calidad del rival y la interacción no aporta.")
    out("=" * 96)

    pd.DataFrame(metrics).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}")


if __name__ == "__main__":
    run()
