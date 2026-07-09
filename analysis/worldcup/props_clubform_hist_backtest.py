"""
PROPS DE GOL · FORMA DE CLUB (sample HISTÓRICO potente) — walk-forward anti-leakage · READ-ONLY · sin prod.

Test definitivo de club-form sobre el backtest histórico de props (~3062 jugador-partido, torneos 2024),
que SÍ tiene potencia (~245 goles vs ~38 del WC). Reutiliza el harness de recencia:
  - sample + V0 nacional POINT-IN-TIME: props_recency_backtest.build_rows lo hace con PR.team_rates
    (agregado nacional PRIOR-SEASON 2023, estrictamente pre-2024 = leak-free) + PP.predict_fixture.
  - team_xg = L3 walk-forward (CB.WFRatings + l3_offline.raw_xg, frozen calib). XI = PR.confirmed_xi.
La ÚNICA adición: cada jugador del XI mezcla su g90 nacional con su g90 de CLUB 2022.

ANTI-LEAKAGE del CLUB: season 2022 (campaña 2022-23, cerrada May-2023) para TODOS los fixtures del sample
(Jan–Jun 2024) -> universalmente pre-partido -> leak-free. NUNCA season 2023 (en curso hasta May-2024).
Filtro anti-selección idéntico: se excluyen bloques con team.id ∈ selecciones (int_results) o league.id==1;
solo cuentan las competiciones de CLUB.

VARIANTES (walk-forward): V0 (nacional prior, = producción) · V1 (blend nacional+club, K en train) ·
V2 (club-only). GATE ESTRICTO: adoptar V1/V2 solo si baten a V0 en OOS con IC95 (paired bootstrap, >=8
semillas) que excluye 0 con margen (>=CLEAR_MARGIN) y robusto. Si no -> cerrar / L1-zero.
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

import props_retest_stats_inputs as PR
import worldcup_player_props as PP
import props_recency_backtest as RB          # ll_vec, multiseed_boot, verdict, SEEDS, CLEAR_MARGIN
import context_shadow_backtest as CB
import l3_offline

BT = ROOT / "data" / "processed" / "worldcup" / "props_backtest"
HIST_CLUB = ROOT / "data" / "processed" / "worldcup" / "hist_club_2022"
INT_RESULTS = HERE / "international_results.csv"
CALIB = HERE / "national_elo_layer3_calibration.json"
REPORT = HERE / "props_clubform_hist_backtest_report.txt"
METRICS = HERE / "props_clubform_hist_backtest_metrics.csv"
CONCLUSION = HERE / "props_clubform_hist_backtest_CONCLUSION.md"

K_GRID = [500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0, 40000.0]   # min de club; grande≈V0


def national_ids():
    import csv
    ids = set()
    with open(INT_RESULTS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            for k in ("home_id", "away_id"):
                try:
                    ids.add(int(float(r[k])))
                except (TypeError, ValueError, KeyError):
                    pass
    return ids


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def load_club_rates(nat):
    """{pid: (g90_club, min_club)} desde hist_club_2022, SOLO bloques de club (anti-selección)."""
    out = {}
    for f in HIST_CLUB.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        resp = d.get("response") or []
        if not resp:
            continue
        item = resp[0]
        pid = (item.get("player") or {}).get("id")
        if pid is None:
            continue
        g = mins = 0.0
        for st in (item.get("statistics") or []):
            tid = (st.get("team") or {}).get("id")
            lid = (st.get("league") or {}).get("id")
            if (lid is not None and int(lid) == 1) or (tid is not None and int(tid) in nat):
                continue  # selección / WC -> excluido
            m = _num((st.get("games") or {}).get("minutes"))
            if m <= 0:
                continue
            g += _num((st.get("goals") or {}).get("total"))
            mins += m
        if mins > 0:
            out[int(pid)] = (g / mins * 90.0, mins)
    return out


def _variant_rates(rates0, xi, club, mode, K=None):
    """rates dict por variante (misma EB shrink de producción vía PP._shares en predict_fixture)."""
    if mode == "V0":
        return rates0
    rv = copy.deepcopy(rates0)
    for pid in xi:
        r = rv.get(pid, {})
        gn = float(r.get("g90", 0.0)); mn = float(r.get("minutes", 0.0))
        gc, mc = club.get(pid, (0.0, 0.0))
        if mc <= 0:
            continue  # sin club -> idéntico a V0 para ese jugador
        if mode == "V2":
            r["g90"] = gc; r["minutes"] = mc
        else:  # V1 blend
            w = mc / (mc + K)
            r["g90"] = w * gc + (1.0 - w) * gn
            r["minutes"] = mn + mc
        rv[pid] = r
    return rv


def build_rows(club):
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
    dated = [(ir_by_fid.loc[fid]["date"], fid) for fid in fids if fid in ir_by_fid.index]
    dated.sort()

    rows = []
    for date, fid in dated:
        rr = ir_by_fid.loc[fid]
        hid, aid = int(rr["home_id"]), int(rr["away_id"])
        hname, aname = str(rr["home"]), str(rr["away"])
        strengths = wf.strengths_by_name(date)
        act = RB.player_actuals_goals_minutes(fid)
        if not (strengths and hname in strengths and aname in strengths and act):
            continue
        sup = strengths[hname] - strengths[aname]
        xg_home, xg_away = l3_offline.raw_xg(sup, a0, a1, tm)
        for tid, team_xg in ((hid, xg_home), (aid, xg_away)):
            xi = PR.confirmed_xi(fid, tid)
            if not xi:
                continue
            rates0 = PR.team_rates(tid)
            lam = {"V0": {p["player_id"]: p["lam_goal"]
                          for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi, _variant_rates(rates0, xi, club, "V0"))},
                   "V2": {p["player_id"]: p["lam_goal"]
                          for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi, _variant_rates(rates0, xi, club, "V2"))}}
            for K in K_GRID:
                lam[f"V1_{int(K)}"] = {p["player_id"]: p["lam_goal"]
                                       for p in PP.predict_fixture(team_xg, 0.0, 0.0, xi,
                                                                   _variant_rates(rates0, xi, club, "V1", K))}
            for pid in xi:
                if pid not in act:
                    continue
                y, _m = act[pid]
                gc, mc = club.get(pid, (0.0, 0.0))
                row = {"fixture_id": fid, "date": date, "team_id": tid, "player_id": pid,
                       "y_goal": int(y), "has_club": int(mc > 0)}
                for k, d in lam.items():
                    row[f"lam_{k}"] = float(d.get(pid, 0.0))
                rows.append(row)
    return pd.DataFrame(rows)


def _p(df, col):
    return np.clip(1.0 - np.exp(-df[col].to_numpy(float)), 1e-15, 1 - 1e-15)


def run():
    nat = national_ids()
    club = load_club_rates(nat)
    df = build_rows(club)
    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 104)
    out("PROPS DE GOL · FORMA DE CLUB (HISTÓRICO potente) — walk-forward anti-leakage · READ-ONLY · sin prod")
    out("=" * 104)
    if df.empty:
        out("Sin filas. Abortado."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return

    y = df["y_goal"].to_numpy(int)
    out(f"jugadores con club-2022: {len(club)} | filas jugador-gol={len(df)} | base rate={y.mean()*100:.1f}% | "
        f"positivos={int(y.sum())} | filas con club(has_club)={int(df['has_club'].sum())} ({df['has_club'].mean()*100:.0f}%)")

    fd = df[["fixture_id", "date"]].drop_duplicates().sort_values("date")
    cut = fd.iloc[len(fd) // 2]["date"]
    df["split"] = np.where(df["date"] < cut, "train", "test")
    tr, te = df[df["split"] == "train"], df[df["split"] == "test"]
    ytr, yte = tr["y_goal"].to_numpy(int), te["y_goal"].to_numpy(int)
    out(f"split temporal: train<{pd.Timestamp(cut).date()}<=test | train={len(tr)} · test(OOS)={len(te)}")

    ll_tr = {K: PP._logloss(_p(tr, f"lam_V1_{int(K)}"), ytr) for K in K_GRID}
    Kstar = min(ll_tr, key=ll_tr.get)
    out(f"K probados (min club): {[int(k) for k in K_GRID]} · semillas={len(RB.SEEDS)} · margen gate={RB.CLEAR_MARGIN}")
    out("--- ajuste K (V1) SOLO en train ---")
    for K in K_GRID:
        out(f"    K={int(K):6d}  logloss_train={ll_tr[K]:.6f}{'   <- K*' if K == Kstar else ''}")
    out(f"  K* = {int(Kstar)} min")
    out("")

    p0 = _p(te, "lam_V0"); d0 = RB.ll_vec(p0, yte)
    variants = {"V0 (nacional prior=prod)": "lam_V0",
                f"V1 (blend K*={int(Kstar)})": f"lam_V1_{int(Kstar)}",
                "V2 (club-2022-only)": "lam_V2"}
    out("-" * 104)
    out(f"[OOS = test] n={len(te)} (base rate={yte.mean()*100:.1f}%) · Δlogloss(V0−Vx)>0 => Vx mejor · GATE")
    out("-" * 104)
    out(f"  {'variante':26} {'logloss':>9} {'brier':>8} {'Δlogloss':>11} {'IC95[min_lo..max_hi]':>26} veredicto")
    mrows = []
    for label, col in variants.items():
        p = _p(te, col); ll = PP._logloss(p, yte); br = PP._brier(p, yte)
        if col == "lam_V0":
            out(f"  {label:26} {ll:>9.5f} {br:>8.5f} {'(baseline)':>11} {'':>26} —")
            mrows.append(dict(variant=label, n=len(te), logloss=ll, brier=br, delta=0.0, lo=np.nan, hi=np.nan, verdict="baseline")); continue
        d = d0 - RB.ll_vec(p, yte); agg = RB.multiseed_boot(d); vd = RB.verdict(agg)
        out(f"  {label:26} {ll:>9.5f} {br:>8.5f} {agg['mean']:>+11.5f} [{agg['min_lo']:+.5f}..{agg['max_hi']:+.5f}] {vd}")
        mrows.append(dict(variant=label, n=len(te), logloss=ll, brier=br, delta=agg["mean"], lo=agg["min_lo"], hi=agg["max_hi"], verdict=vd))

    # subconjunto has_club (donde el efecto vive)
    tem = te[te["has_club"] == 1]
    if len(tem) >= 20:
        ym = tem["y_goal"].to_numpy(int); p0m = _p(tem, "lam_V0"); d0m = RB.ll_vec(p0m, ym)
        pv1 = _p(tem, f"lam_V1_{int(Kstar)}"); a = RB.multiseed_boot(d0m - RB.ll_vec(pv1, ym))
        out("")
        out(f"  [subconjunto HAS_CLUB del test] n={len(tem)}: V1 Δlogloss={a['mean']:+.5f} "
            f"IC95[{a['min_lo']:+.5f}..{a['max_hi']:+.5f}] {'(signif)' if a['all_lo_pos'] or a['all_hi_neg'] else '(IC∋0)'}")
    out("")
    out("=" * 104)
    out(f"GATE: ADOPTAR sólo si Δlogloss(V0−Vx)>0 en OOS con IC95 excluyendo 0 con margen (>=+{RB.CLEAR_MARGIN}) y robusto.")
    out("=" * 104)

    pd.DataFrame(mrows).to_csv(METRICS, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS}")

    passed = [r for r in mrows if str(r["verdict"]).startswith("ADOPTAR")]
    md = ["# Props de gol — forma de CLUB (sample HISTÓRICO potente): veredicto\n",
          "**Read-only · sin commit · sin tocar producción.** Test definitivo de club-form sobre el backtest",
          "histórico de props (torneos 2024, ~3062 jugador-partido) con V0 nacional point-in-time (prior-season",
          "2023, leak-free) + club-2022 (campaña cerrada May-2023, universalmente pre-partido).\n",
          f"- Muestra: {len(df)} jugador-partido · base rate {y.mean()*100:.1f}% · positivos {int(y.sum())} · "
          f"OOS test {len(te)} · K*={int(Kstar)} min · club disponible en {df['has_club'].mean()*100:.0f}% de filas.\n",
          "## Veredicto por variante (juez = OOS, baseline V0 nacional)\n",
          "| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |", "|---|---|---|---|---|"]
    for r in mrows:
        if str(r["verdict"]) == "baseline":
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | (baseline) | — | — |")
        else:
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | {r['delta']:+.5f} | [{r['lo']:+.5f}..{r['hi']:+.5f}] | {r['verdict']} |")
    md.append("\n## Recomendación\n")
    if passed:
        md.append(f"- **{', '.join(r['variant'] for r in passed)}** supera(n) el gate estricto en OOS con potencia "
                  f"({int(y.sum())} goles). **Candidata a ADOPCIÓN 🔴** (tocaría la tasa de las props) — requiere OK de Jorge.")
    else:
        md.append("- **Ninguna variante** supera el gate estricto ni con potencia. La forma de club no bate al")
        md.append("  nacional-only con IC que excluya 0. **Recomendación: cerrar / L1-zero. No tocar props.**")
    md.append("\n_Artefactos: props_clubform_hist_backtest_report.txt · _metrics.csv · este CONCLUSION.md. "
              "No se tocó worldcup_player_props.py._")
    CONCLUSION.write_text("\n".join(md), encoding="utf-8")
    print(f"Written: {CONCLUSION}")
    return mrows, Kstar, bool(passed)


if __name__ == "__main__":
    run()
