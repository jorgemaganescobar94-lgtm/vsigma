"""
PROPS DE GOL · FORMA DE CLUB — backtest walk-forward anti-leakage · READ-ONLY · sin API · sin prod · sin commit.

PREGUNTA (Jorge, Fase B-A): ¿mezclar la forma de CLUB 2025 (leak-free, campaña cerrada antes del Mundial)
en la tasa de gol del jugador mejora la prop de gol sobre el baseline national-only? El dato decide; si no
bate con IC95 que excluye 0 con claridad -> cerrar / L1-zero, NO tocar producción.

SAMPLE leak-free con datos EN MANO (sin API): los partidos WC-2026 YA LIQUIDADOS. Fuente:
  - worldcup_player_props_log.csv (924 settled): lam_goal V0 CONGELADO pre-KO (producción) + act_goal real.
  - worldcup_player_club_rates.csv (extractor): g90_club (SOLO club) y g90_nat (bloques de selección
    season-2025, baseline nacional leak-free) por jugador.
NOTA de alcance honesta: el sample HISTÓRICO de props (~3062, torneos 2024) NO puede testear la forma de
club sin datos de club de ESOS jugadores (no capturados; club-2025 sería futuro para 2024). Por eso el
test se hace sobre el WC-2026 liquidado (N menor, pero es el único leak-free con datos en mano y sin API).

MATEMÁTICA (idéntica a producción): lam_goal_i = team_xg_eff · share_i ; share = PP._shares (EB shrink,
PRIOR_MIN). team_xg_eff = Σ lam_goal_log del equipo en el fixture (= team_xg·XI_ATTR de PRODUCCIÓN, exacto)
-> solo cambia CÓMO se forma el g90 del jugador antes de la share:
  V0  national-only  : g90 = g90_nat            (baseline recomputado; se reporta su fidelidad vs el log)
  V1  blend K        : g90 = w·g90_club+(1−w)·g90_nat, w=min_club/(min_club+K), K tuneado SOLO en train
  V2  club-only      : g90 = g90_club
GATE (idéntico a DC/recencia/calibración): ADOPTAR V1/V2 solo si baten a V0 en OOS con IC95 (paired
bootstrap, >=8 semillas) que EXCLUYE 0 con margen (>=CLEAR_MARGIN) y robusto. Si no -> cerrar / L1-zero.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import worldcup_player_props as PP           # _shares (EB shrink), _logloss, _brier
import props_recency_backtest as RB          # ll_vec, multiseed_boot, verdict, SEEDS, CLEAR_MARGIN

RATES_DIR = ROOT / "data" / "processed" / "worldcup" / "player_props"


def load_natrates(tid):
    """Rates nacionales EXACTOS de producción (RATE_SEASONS=[2024,2025]) desde el cache de
    fetch_team_rates -> {pid: {g90, minutes, ...}}. {} si falta."""
    p = RATES_DIR / f"rates_team{int(tid)}_s2024-2025.json"
    if not p.exists():
        return {}
    return {int(k): v for k, v in json.loads(p.read_text(encoding="utf-8")).items()}

LOG = HERE / "worldcup_player_props_log.csv"
CLUB = HERE / "worldcup_player_club_rates.csv"
REPORT = HERE / "props_clubform_backtest_report.txt"
METRICS = HERE / "props_clubform_backtest_metrics.csv"
CONCLUSION = HERE / "props_clubform_backtest_CONCLUSION.md"

K_GRID = [500.0, 1000.0, 2000.0, 4000.0, 8000.0, 16000.0, 40000.0]   # min de club; grande≈V0, pequeño≈club


def _rates(xi, natr, club, mode, K=None):
    """rates dict {pid:{g90,minutes}} por variante, para PP._shares (misma EB shrink de producción).
    natr = rates nacionales EXACTOS de producción (rates_team cache)."""
    out = {}
    for pid in xi:
        nr = natr.get(pid, {})
        gn, mn = float(nr.get("g90", 0.0)), float(nr.get("minutes", 0.0))
        c = club.get(pid, {})
        gc, mc = float(c.get("g90_club", 0.0)), float(c.get("club_minutes", 0.0))
        if mode == "V0":
            out[pid] = {"g90": gn, "minutes": mn}
        elif mode == "V2":
            out[pid] = {"g90": gc, "minutes": mc}
        else:  # V1 blend
            w = mc / (mc + K) if mc > 0 else 0.0
            out[pid] = {"g90": w * gc + (1.0 - w) * gn, "minutes": mn + mc}
    return out


def _p_variant(xi, natr, club, team_xg_eff, mode, K=None):
    """p_goal por jugador de la variante: lam = team_xg_eff·share; p=1−exp(−lam)."""
    sh = PP._shares(xi, _rates(xi, natr, club, mode, K), "g90")
    return {pid: 1.0 - np.exp(-(team_xg_eff * sh.get(pid, 0.0))) for pid in xi}


def build():
    log = pd.read_csv(LOG)
    log = log[(log["settled"].fillna(0).astype(int) == 1) & log["act_goal"].notna()].copy()
    log["kickoff_utc"] = pd.to_datetime(log["kickoff_utc"], utc=True, errors="coerce")
    club_df = pd.read_csv(CLUB).set_index("player_id")
    club = {int(i): r._asdict() if hasattr(r, "_asdict") else dict(r)
            for i, r in club_df.iterrows()} if False else \
           {int(i): {k: club_df.loc[i, k] for k in club_df.columns} for i in club_df.index}

    rows = []
    natr_cache = {}
    for (fid, tid), g in log.groupby(["fixture_id", "team_id"]):
        xi = [int(p) for p in g["player_id"].tolist()]
        if len(xi) < 5:
            continue
        team_xg_eff = float(g["lam_goal"].fillna(0).sum())   # = team_xg·XI_ATTR de PRODUCCIÓN (exacto)
        if team_xg_eff <= 0:
            continue
        natr = natr_cache.setdefault(int(tid), load_natrates(int(tid)))   # V0 EXACTO de producción
        y = {int(r.player_id): (1 if float(r.act_goal) > 0 else 0) for r in g.itertuples()}
        p_log = {int(r.player_id): 1.0 - np.exp(-max(0.0, float(r.lam_goal or 0.0))) for r in g.itertuples()}
        pv0 = _p_variant(xi, natr, club, team_xg_eff, "V0")
        pv2 = _p_variant(xi, natr, club, team_xg_eff, "V2")
        pvk = {K: _p_variant(xi, natr, club, team_xg_eff, "V1", K) for K in K_GRID}
        ko = g["kickoff_utc"].iloc[0]
        for pid in xi:
            row = {"fixture_id": fid, "team_id": tid, "player_id": pid, "kickoff": ko,
                   "y": y[pid], "p_log": p_log[pid], "p_v0": pv0[pid], "p_v2": pv2[pid]}
            for K in K_GRID:
                row[f"p_v1_{int(K)}"] = pvk[K][pid]
            rows.append(row)
    return pd.DataFrame(rows)


def _ll(p, y):
    p = np.clip(np.asarray(p, float), 1e-15, 1 - 1e-15)
    return PP._logloss(p, np.asarray(y, int))


def run():
    df = build()
    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 104)
    out("PROPS DE GOL · FORMA DE CLUB — walk-forward anti-leakage · WC-2026 liquidado · READ-ONLY · sin API · sin prod")
    out("=" * 104)
    if df.empty:
        out("Sin filas. Abortado."); REPORT.write_text("\n".join(lines), encoding="utf-8"); return

    y = df["y"].to_numpy(int)
    # fidelidad del baseline recomputado (V0 nat season-2025) vs el V0 CONGELADO del log (producción)
    fid_ll_log = _ll(df["p_log"], y); fid_ll_v0 = _ll(df["p_v0"], y)
    corr = float(np.corrcoef(df["p_log"], df["p_v0"])[0, 1])
    out(f"filas jugador-gol (WC liquidado)={len(df)} | base rate gol={y.mean()*100:.1f}% | positivos={int(y.sum())}")
    out(f"FIDELIDAD baseline: logloss V0_log(producción)={fid_ll_log:.5f} vs V0_recomp(rates EXACTOS 2024-2025)={fid_ll_v0:.5f} "
        f"· corr(p)={corr:.3f}  (esperado ~1.0)")
    out("")

    # split temporal por fixture (train mitad temprana, test mitad tardía)
    fd = df[["fixture_id", "kickoff"]].drop_duplicates().sort_values("kickoff")
    cut = fd.iloc[len(fd) // 2]["kickoff"]
    df["split"] = np.where(df["kickoff"] < cut, "train", "test")
    tr, te = df[df["split"] == "train"], df[df["split"] == "test"]
    yte = te["y"].to_numpy(int); ytr = tr["y"].to_numpy(int)
    out(f"split temporal: train<{pd.Timestamp(cut).date()}<=test | train={len(tr)} · test(OOS)={len(te)}")

    # tune K en TRAIN (min logloss)
    ll_tr = {K: _ll(tr[f"p_v1_{int(K)}"], ytr) for K in K_GRID}
    Kstar = min(ll_tr, key=ll_tr.get)
    out(f"K probados (min club): {[int(k) for k in K_GRID]}  ·  semillas={len(RB.SEEDS)}  ·  margen gate={RB.CLEAR_MARGIN}")
    out("--- ajuste de K (V1) SOLO en train ---")
    for K in K_GRID:
        out(f"    K={int(K):6d}  logloss_train={ll_tr[K]:.6f}{'   <- K*' if K == Kstar else ''}")
    out(f"  K* = {int(Kstar)} min  (w=min_club/(min_club+K*))")
    out("")

    # OOS: baseline = V0_recomp (aísla el efecto CLUB, misma tubería nacional)
    p0 = np.clip(te["p_v0"].to_numpy(float), 1e-15, 1 - 1e-15); d0 = RB.ll_vec(p0, yte)
    variants = {"V0 (nat-only, baseline)": "p_v0",
                f"V1 (blend K*={int(Kstar)})": f"p_v1_{int(Kstar)}",
                "V2 (club-only)": "p_v2"}
    out("-" * 104)
    out(f"[OOS = test] n={len(te)} (base rate={yte.mean()*100:.1f}%) · Δlogloss(V0−Vx)>0 => Vx mejor · juez del GATE")
    out("-" * 104)
    out(f"  {'variante':26} {'logloss':>9} {'brier':>8} {'Δlogloss':>11} {'IC95[min_lo..max_hi]':>26} veredicto")
    mrows = []
    for label, col in variants.items():
        p = np.clip(te[col].to_numpy(float), 1e-15, 1 - 1e-15)
        ll = _ll(p, yte); br = PP._brier(p, yte)
        if col == "p_v0":
            out(f"  {label:26} {ll:>9.5f} {br:>8.5f} {'(baseline)':>11} {'':>26} —")
            mrows.append(dict(variant=label, n=len(te), logloss=ll, brier=br, delta=0.0,
                              lo=np.nan, hi=np.nan, verdict="baseline")); continue
        d = d0 - RB.ll_vec(p, yte); agg = RB.multiseed_boot(d); vd = RB.verdict(agg)
        out(f"  {label:26} {ll:>9.5f} {br:>8.5f} {agg['mean']:>+11.5f} "
            f"[{agg['min_lo']:+.5f}..{agg['max_hi']:+.5f}] {vd}")
        mrows.append(dict(variant=label, n=len(te), logloss=ll, brier=br, delta=agg["mean"],
                          lo=agg["min_lo"], hi=agg["max_hi"], verdict=vd))
    out("")
    # contexto: V1(K*) vs el V0 de PRODUCCIÓN (log) — ¿bate al modelo real?
    pv1 = np.clip(te[f"p_v1_{int(Kstar)}"].to_numpy(float), 1e-15, 1 - 1e-15)
    plog = np.clip(te["p_log"].to_numpy(float), 1e-15, 1 - 1e-15)
    dctx = RB.ll_vec(plog, yte) - RB.ll_vec(pv1, yte); actx = RB.multiseed_boot(dctx)
    out(f"  [contexto] V1(K*) vs V0_PRODUCCIÓN(log): Δlogloss={actx['mean']:+.5f} "
        f"IC95[{actx['min_lo']:+.5f}..{actx['max_hi']:+.5f}] "
        f"{'(signif)' if actx['all_lo_pos'] or actx['all_hi_neg'] else '(IC∋0)'}")
    out("")
    out("=" * 104)
    out(f"GATE: ADOPTAR sólo si Δlogloss(V0−Vx)>0 en OOS con IC95 excluyendo 0 con margen (>=+{RB.CLEAR_MARGIN}) y robusto.")
    out("HONESTIDAD: si roza 0 o empata => cerrar / L1-zero, NO tocar worldcup_player_props.py.")
    out("=" * 104)

    pd.DataFrame(mrows).to_csv(METRICS, index=False)
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWritten: {REPORT}\nWritten: {METRICS}")

    passed = [r for r in mrows if str(r["verdict"]).startswith("ADOPTAR")]
    md = ["# Props de gol — forma de CLUB: veredicto\n",
          "**Read-only · sin API · sin commit · sin tocar producción.** ¿Mezclar la forma de club 2025 (leak-free)",
          "mejora la prop de gol sobre national-only? Test walk-forward sobre el WC-2026 liquidado.\n",
          f"- Muestra: {len(df)} jugador-partido WC · base rate {y.mean()*100:.1f}% · OOS test {len(te)} filas · K*={int(Kstar)} min.",
          f"- Fidelidad baseline recomputado vs V0 producción (log): corr(p)={corr:.3f}.\n",
          "## Veredicto por variante (juez = OOS, baseline V0 nat-only)\n",
          "| variante | logloss | Δlogloss(V0−Vx) | IC95 | veredicto |", "|---|---|---|---|---|"]
    for r in mrows:
        if str(r["verdict"]) == "baseline":
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | (baseline) | — | — |")
        else:
            md.append(f"| {r['variant']} | {r['logloss']:.5f} | {r['delta']:+.5f} | [{r['lo']:+.5f}..{r['hi']:+.5f}] | {r['verdict']} |")
    md.append("\n## Recomendación\n")
    if passed:
        md.append(f"- **{', '.join(r['variant'] for r in passed)}** supera(n) el gate estricto en OOS. Candidata 🔴 "
                  "(tocaría la tasa de las props) — requiere OK de Jorge. NO aplicado.")
    else:
        md.append("- **Ninguna variante** supera el gate estricto en el OOS. La forma de club no bate al national-only")
        md.append("  con IC que excluya 0 con claridad en esta muestra WC. **Recomendación: cerrar / L1-zero. No tocar props.**")
        md.append("  (Coherente con muestra WC pequeña; re-evaluable al crecer N.)")
    md.append("\n_Artefactos: props_clubform_backtest_report.txt · _metrics.csv · este CONCLUSION.md. "
              "No se tocó worldcup_player_props.py._")
    CONCLUSION.write_text("\n".join(md), encoding="utf-8")
    print(f"Written: {CONCLUSION}")
    return mrows, Kstar, bool(passed)


if __name__ == "__main__":
    run()
