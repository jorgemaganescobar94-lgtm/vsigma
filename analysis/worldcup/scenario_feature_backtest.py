"""
QUALIFICATION SCENARIO ENGINE (correct, FIFA tiebreakers) + BACKTEST of the scenario as a LEARNED
FEATURE of the model (not a fixed multiplier). READ-ONLY · NO production change · NO API.

Extends the context backtest harness (context_shadow_backtest): same sample (last group matchday of
national-team finals tournaments), same walk-forward L3 ratings + frozen calibration, same anti-leakage
(standings reconstructed from PRIOR matchdays). It REUSES reconstruct_groups / WFRatings / the L3
machinery; it does NOT duplicate them.

PART 1 — QUALIFICATION ENGINE (per team, last group matchday of a 4-team group):
  Enumerate the 9 remaining-result combinations (own match W/D/L × the parallel match W/D/L), compute
  final POINTS, and apply the real ordering (points -> goal difference -> goals for -> head-to-head).
  Because GD/GF depend on UNKNOWN scorelines, a tie at the qualification boundary is flagged
  'gd_dependent' (it would be decided by GD/GF/h2h), NOT asserted. Best thirds are handled per format
  (6 groups -> top-2 + 4 thirds; 12 groups -> top-2 + 8 thirds; else top-2 only) using ALL groups'
  current tables (conservative cross-group bound; documented). Output: per-team scenario FEATURES.

PART 2 — SCENARIO AS A LEARNED FEATURE:
  Add the scenario features to the goal model and LET the fit learn their effect on BURN-IN (<2024),
  then evaluate OOS (>=2024) vs the baseline (L3 xG only): goals (Poisson dev), Over2.5/BTTS, 1X2.
  Paired bootstrap IC95%. Strict anti-leakage (features + coefficients only from prior data).

OUTPUT: scenario_feature_backtest_report.txt + scenario_feature_backtest_metrics.csv
"""
from __future__ import annotations

import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import context_shadow_backtest as CB     # reconstruct_groups, WFRatings, data load, L3 calib
import l3_offline                          # raw_xg, wdl (Poisson + frozen calibration)
from qual_engine import classify_team, FEATURES   # single source of truth for the scenario engine

REPORT = HERE / "scenario_feature_backtest_report.txt"
METRICS_CSV = HERE / "scenario_feature_backtest_metrics.csv"


# --------------------------------------------------------------- standings (with GF for tiebreak)
def full_table(group, upto_date):
    """Group table BEFORE upto_date (leak-free): {tid: {name, pts, played, gd, gf}}."""
    acc, name = {}, {}
    tids = set()
    for r in group["matches"]:
        name[int(r.home_id)] = r.home; name[int(r.away_id)] = r.away
        tids.add(int(r.home_id)); tids.add(int(r.away_id))
    for t in tids:
        acc[t] = {"name": name[t], "pts": 0.0, "played": 0, "gd": 0.0, "gf": 0.0}
    for r in group["matches"]:
        if r.date >= upto_date:
            continue
        h, a, gh, ga = int(r.home_id), int(r.away_id), float(r.gh), float(r.ga)
        acc[h]["played"] += 1; acc[a]["played"] += 1
        acc[h]["gd"] += gh - ga; acc[a]["gd"] += ga - gh
        acc[h]["gf"] += gh; acc[a]["gf"] += ga
        if gh > ga:
            acc[h]["pts"] += 3
        elif gh < ga:
            acc[a]["pts"] += 3
        else:
            acc[h]["pts"] += 1; acc[a]["pts"] += 1
    return acc


# classify_team / _status_in_branch / FEATURES / THIRDS_BY_NGROUPS / RES_PTS -> qual_engine (imported)


# --------------------------------------------------------------- PART 1 validation
def _mk_group(rows):
    """rows: [(tid, pts, played, gd, gf)] -> a table dict (synthetic, for validation)."""
    return {t: {"name": str(t), "pts": p, "played": pl, "gd": gd, "gf": gf} for t, p, pl, gd, gf in rows}


def part1_validation(out):
    out("=" * 96)
    out("PARTE 1 — MOTOR DE CLASIFICACIÓN: validación con casos construidos")
    out("=" * 96)
    # (tid, pts, played, gd, gf). Match = teams 1 vs 2; parallel = 3 vs 4. Evaluamos al equipo 1
    # salvo que se indique. ng = nº de grupos del torneo (para mejores terceros).
    cases = [
        # A clinched: A=6, nadie llega a 6 ni ganando -> entra incluso perdiendo
        ("clasificado (cierto)", _mk_group([(1, 6, 2, 4, 6), (2, 2, 2, -1, 2), (3, 1, 2, -1, 2), (4, 1, 2, -2, 1)]), 1, 2, 1, 8, "qualified"),
        # A le vale el empate: A=4, paralelo C,D=1 (techo 4) -> empate=5 entra; perder no
        ("le vale empate (controla)", _mk_group([(1, 4, 2, 2, 4), (2, 3, 2, 0, 3), (3, 1, 2, -1, 2), (4, 1, 2, -1, 2)]), 1, 2, 1, 8, "draw_enough"),
        # A debe ganar: ganar=6 entra seguro; empatar=4 empata con B (frontera); perder fuera
        ("debe ganar (solo ganando)", _mk_group([(1, 3, 2, 0, 3), (2, 3, 2, 0, 3), (3, 1, 2, -1, 2), (4, 1, 2, -1, 2)]), 1, 2, 1, 8, "must_win"),
        # depende del otro partido / GD: todos parejos
        ("depende de otros / GD", _mk_group([(1, 3, 2, 0, 3), (2, 3, 2, 0, 3), (3, 3, 2, 0, 3), (4, 0, 2, 0, 1)]), 1, 2, 1, 8, "depends/gd"),
        # eliminado: 4º seguro (los otros 3 por encima de su techo) incluso con terceros
        ("eliminado (4º seguro)", _mk_group([(1, 6, 2, 5, 7), (2, 6, 2, 5, 7), (3, 4, 2, 0, 3), (4, 0, 2, -10, 0)]), 3, 4, 4, 6, "eliminated"),
        # posible mejor tercero (6 grupos): 3º por puntos, no 4º -> NO eliminado
        ("vivo como mejor tercero", _mk_group([(1, 6, 2, 4, 6), (2, 6, 2, 4, 6), (3, 1, 2, -4, 2), (4, 1, 2, -4, 2)]), 3, 4, 3, 6, "alive_as_third"),
    ]
    out("")
    for label, g, h, a, team, ng, expect in cases:
        feat, lab = classify_team(g, h, a, team, [g], ng)
        flags = ",".join(f for f in FEATURES if feat[f])
        out(f"  {label:30} -> {lab:18} [{flags or '—'}]   (esperado: {expect})")
    out("")


# --------------------------------------------------------------- build the sample (reuse CB)
def build_sample():
    raw = pd.read_csv(CB.DATA)
    raw["date"] = CB.pd.to_datetime(raw["date"], utc=True, errors="coerce").dt.tz_localize(None)
    raw = raw.dropna(subset=["date", "home_id", "away_id", "gh", "ga"]).copy()
    raw["home_id"] = raw["home_id"].astype(int); raw["away_id"] = raw["away_id"].astype(int)
    wf = CB.WFRatings(raw.sort_values("date").reset_index(drop=True))
    import json
    calib = json.loads(CB.CALIB.read_text(encoding="utf-8"))
    a0, a1, tm = calib["a0"], calib["a1"], calib["total_mean"]
    tcoef = calib.get("total_coef")

    rows = []
    fin = raw[raw["league_tag"].isin(CB.FINALS_TAGS)]
    for (tag, season), sub in fin.groupby(["league_tag", "season"]):
        if len(sub) < 6:
            continue
        groups, ok = CB.reconstruct_groups(sub)
        if not ok:
            continue
        n_groups = len(groups)
        # final-matchday matches per group: each team's last (3rd) group game
        for gi, g in enumerate(groups):
            seen = {}
            for r in g["matches"]:
                h, a = int(r.home_id), int(r.away_id)
                oh, oa = seen.get(h, 0) + 1, seen.get(a, 0) + 1
                seen[h], seen[a] = oh, oa
                if oh == 3 and oa == 3:                 # both playing their final group game
                    date = r.date
                    all_tables = [full_table(gg, date) for gg in groups]
                    table = all_tables[gi]
                    if h not in table or a not in table:
                        continue
                    fh, _lh = classify_team(table, h, a, h, all_tables, n_groups)
                    fa, _la = classify_team(table, h, a, a, all_tables, n_groups)
                    # L3 walk-forward xG (neutral) — reuse CB.WFRatings + frozen calibration
                    strengths = wf.strengths_by_name(date)
                    if not strengths or r.home not in strengths or r.away not in strengths:
                        continue
                    sup = strengths[r.home] - strengths[r.away]
                    xgh, xga = l3_offline.raw_xg(sup, a0, a1, tm, tcoef, matchup=False)  # baseline xG
                    is_oos = int(date >= np.datetime64("2024-01-01"))
                    # one row per TEAM-match (for the goal model)
                    rows.append({"is_oos": is_oos, "side": "home", "xg": xgh, "opp_xg": xga,
                                 "goals": float(r.gh), "opp_goals": float(r.ga), **{f"f_{k}": fh[k] for k in FEATURES}})
                    rows.append({"is_oos": is_oos, "side": "away", "xg": xga, "opp_xg": xgh,
                                 "goals": float(r.ga), "opp_goals": float(r.gh), **{f"f_{k}": fa[k] for k in FEATURES}})
                    rows[-2]["match"] = rows[-1]["match"] = f"{tag}{int(season)}#{gi}:{r.home}-{r.away}"
                    rows[-2]["res"] = rows[-1]["res"] = ("H" if r.gh > r.ga else "D" if r.gh == r.ga else "A")
    return pd.DataFrame(rows)


# --------------------------------------------------------------- PART 2 — scenario as a learned feature
def _pois_dev(y, lam):
    y = np.asarray(y, float); lam = np.clip(np.asarray(lam, float), 1e-9, None)
    pos = y > 0
    t = np.zeros_like(y); t[pos] = y[pos] * np.log(y[pos] / lam[pos])
    return float(2.0 * np.sum(t - (y - lam)))


def _over25(L):
    L = np.maximum(L, 1e-9)
    return 1.0 - np.exp(-L) * (1.0 + L + L * L / 2.0)


def _btts(lh, la):
    return (1.0 - np.exp(-np.maximum(lh, 0.0))) * (1.0 - np.exp(-np.maximum(la, 0.0)))


def _ll_bin(p, y):
    p = np.clip(p, 1e-15, 1 - 1e-15); y = np.asarray(y, float)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def _ece(p, y, bins=10):
    p = np.asarray(p, float); y = np.asarray(y, float)
    e = 0.0
    for i in range(bins):
        m = (p > i / bins) & (p <= (i + 1) / bins)
        if m.sum():
            e += m.sum() / len(p) * abs(p[m].mean() - y[m].mean())
    return float(e)


def run():
    lines = []

    def out(s=""):
        print(s); lines.append(s)

    part1_validation(out)

    df = build_sample()
    out("=" * 96)
    out("PARTE 2 — ESCENARIO COMO FEATURE APRENDIDA (no multiplicador fijo)")
    out("=" * 96)
    if df.empty:
        out("Sin muestra."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return
    n_matches = df["match"].nunique()
    burn = df[df["is_oos"] == 0]; oos = df[df["is_oos"] == 1]
    out(f"team-matches={len(df)} (partidos={n_matches}) | burn-in(<2024)={len(burn)} | OOS(>=2024)={len(oos)}")
    out("distribución de features (team-matches con la flag activa):")
    for f in FEATURES:
        out(f"   f_{f:18} burn={int(burn[f'f_{f}'].sum()):3}  OOS={int(oos[f'f_{f}'].sum()):3}")
    out("")
    if len(oos) < 20:
        out(f"MUESTRA OOS PEQUEÑA (n={len(oos)} team-matches): los resultados son orientativos.")
    out("")

    # ---- learned scenario effect on GOALS (burn-in): log((g+0.5)/(xg+0.5)) ~ features ----
    rb = np.log((burn["goals"].to_numpy(float) + 0.5) / (burn["xg"].to_numpy(float) + 0.5))
    Fcols = [f"f_{k}" for k in FEATURES]
    # derived parsimonious feature: 'low_stakes' = nada que jugarse por top-2 (clasificado o eliminado)
    for d in (df, burn, oos):
        d["f_low_stakes"] = ((d["f_qualified"] == 1) | (d["f_eliminated"] == 1)).astype(int)

    def fit(cols, ridge=0.0):
        cols = [c for c in cols if burn[c].sum() > 0 and burn[c].sum() < len(burn)]
        X = np.c_[np.ones(len(burn)), burn[cols].to_numpy(float)]
        A = X.T @ X + ridge * np.eye(X.shape[1]); A[0, 0] -= ridge   # no penalizar el intercepto
        beta = np.linalg.solve(A, X.T @ rb)
        return cols, beta

    def rate(d, cols, beta):
        adj = beta[0] + d[cols].to_numpy(float) @ beta[1:]
        return np.maximum(0.05, (d["xg"].to_numpy(float) + 0.5) * np.exp(adj) - 0.5)

    rng = np.random.RandomState(20260626)

    def boot(dper):
        idx = rng.randint(0, len(dper), (10000, len(dper)))
        b = dper[idx].mean(1)
        return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))

    # per-match pairing (OOS)
    H = oos[oos["side"] == "home"].set_index("match")
    Av = oos[oos["side"] == "away"].set_index("match")
    common = [m for m in sorted(oos["match"].unique()) if m in H.index and m in Av.index]
    H, Av = H.loc[common], Av.loc[common]
    gh = H["goals"].to_numpy(float); ga = Av["goals"].to_numpy(float)
    real_over = ((gh + ga) >= 3).astype(int); real_btts = ((gh >= 1) & (ga >= 1)).astype(int)
    res = np.where(gh > ga, 0, np.where(gh == ga, 1, 2)); Y = np.eye(3)[res]
    import json
    iso = json.loads(CB.CALIB.read_text(encoding="utf-8")).get("iso_const")

    def wdl_cal(lh, la):
        P = np.array([l3_offline.wdl(lh[i], la[i]) for i in range(len(lh))])
        C = np.column_stack([np.interp(P[:, k], iso[k]["ux"], iso[k]["uf"]) for k in range(3)])
        C = np.clip(C, 1e-6, None); return C / C.sum(1, keepdims=True)

    lh_b, la_b = H["xg"].to_numpy(float), Av["xg"].to_numpy(float)
    base = {"over": _over25(lh_b + la_b), "btts": _btts(lh_b, la_b), "x": wdl_cal(lh_b, la_b)}
    y_g = oos["goals"].to_numpy(float); base_dev = _pois_dev(y_g, oos["xg"].to_numpy(float))

    metrics = []

    def evaluate(label, cols, ridge=0.0):
        cols, beta = fit(cols, ridge)
        out(f"\n--- modelo: {label}  (features: {', '.join(c[2:] for c in cols)}; ridge={ridge}) ---")
        out("  coef (×mult): " + " · ".join(f"{c[2:]} {beta[i+1]:+.2f}(×{np.exp(beta[i+1]):.2f})"
                                             for i, c in enumerate(cols)) + f"  | intercepto {beta[0]:+.2f}")
        dev_f = _pois_dev(y_g, rate(oos, cols, beta))
        out(f"  GOLES Poisson dev OOS: base {base_dev:.1f} vs feat {dev_f:.1f} (Δ {base_dev-dev_f:+.1f})")
        lh_f, la_f = rate(H, cols, beta), rate(Av, cols, beta)
        feat = {"over": _over25(lh_f + la_f), "btts": _btts(lh_f, la_f), "x": wdl_cal(lh_f, la_f)}
        for name, yv in (("Over2.5", real_over), ("BTTS", real_btts)):
            key = "over" if name == "Over2.5" else "btts"
            d = _ll_bin(base[key], yv) - _ll_bin(feat[key], yv); ic = boot(d)
            sig = "SIGNIF" if (ic[0] > 0 or ic[1] < 0) else "no signif (IC∋0)"
            out(f"  {name:8} ll base {_ll_bin(base[key], yv).mean():.4f} feat {_ll_bin(feat[key], yv).mean():.4f} "
                f"(Δ {d.mean():+.4f}) | IC95[{ic[0]:+.4f},{ic[1]:+.4f}] {sig}")
            metrics.append({"model": label, "metric": name, "d_mean": float(d.mean()),
                            "ic_lo": ic[0], "ic_hi": ic[1], "n": len(common)})
        rb_ = -np.sum(Y * np.log(np.clip(base["x"], 1e-15, 1)), axis=1)
        rf_ = -np.sum(Y * np.log(np.clip(feat["x"], 1e-15, 1)), axis=1)
        d = rb_ - rf_; ic = boot(d)
        sig = "SIGNIF" if (ic[0] > 0 or ic[1] < 0) else "no signif (IC∋0)"
        out(f"  {'1X2':8} ll base {rb_.mean():.4f} feat {rf_.mean():.4f} (Δ {d.mean():+.4f}) | IC95[{ic[0]:+.4f},{ic[1]:+.4f}] {sig}")
        metrics.append({"model": label, "metric": "1X2", "d_mean": float(d.mean()),
                        "ic_lo": ic[0], "ic_hi": ic[1], "n": len(common)})

    out("Δ = baseline − feature (logloss); >0 con IC95% que EXCLUYE 0 = la feature MEJORA OOS.")
    evaluate("FULL (8 flags, OLS)", Fcols, ridge=0.0)
    evaluate("FULL + ridge", Fcols, ridge=10.0)
    evaluate("PARSIMONIOSO (low_stakes + must_win)", ["f_low_stakes", "f_must_win"], ridge=0.0)
    out("")
    out("=" * 96)
    out("LECTURA: la feature aporta solo si Δ>0 con IC95% que EXCLUYE 0 (mejora real OOS) en goles/OU/")
    out("BTTS sin dañar el 1X2. Si los IC incluyen 0 (o la muestra es pequeña) -> no concluyente.")
    out("=" * 96)

    pd.DataFrame(metrics).to_csv(METRICS_CSV, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS_CSV}")


if __name__ == "__main__":
    run()
