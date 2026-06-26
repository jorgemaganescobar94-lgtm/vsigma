"""
RE-TEST (READ-ONLY · NO production change) of the historical CARD / SHOTS-ON-TARGET
player-prop backtest, replacing the CONSTANT team inputs (which confounded the first
backtest) with the PRODUCTION STATS MODEL inputs (stats_model.py: Poisson log-linear of
shots/cards with the opp_str feature), estimated WALK-FORWARD (coefficients refit only on
data strictly PRIOR to each match).

It does NOT duplicate logic: it imports the production prop math
(worldcup_player_props.predict_fixture / _logloss / _brier / _ece / poisson_p_ge1) and the
production stats model (stats_model.walkforward). It only replaces the two TEAM-LEVEL inputs
that the first backtest hard-coded:
    * st_shots_team  : 12.0 (constant)  ->  model walk-forward E[team shots]
    * st_cards_total : 3.8  (constant)  ->  model walk-forward E[home cards]+E[away cards]
Everything else is identical to the first backtest and to production:
    * XI = the CONFIRMED startXI from the cached /fixtures/lineups (observed input).
    * Per-player /90 rates = PRIOR-SEASON (2023) rates, already aggregated, from the cache.
    * Shares + Poisson distribution = production predict_fixture (CARD_TEAM_SPLIT=0.5 etc.).
    * Target = per-player actuals from the cached /fixtures/players (output only, never a feature).

ANTI-LEAKAGE: rates are 2023 (strictly before the 2024 matches); stats-model betas are refit
walk-forward on rows with date < match date (MIN_PAST=150, half-life 540d); XI is the observed
confirmed lineup; targets are used only to score. The one acknowledged minor look-ahead is the
opp_str FEATURE (final L3 strength + full-sample standardisation), identical to production's own
stats model; its coefficient is small. Documented, not hidden.

SAMPLE: the first backtest used ~150 international matches (Jan-Jun 2024, AFCON/AsianCup/WCQ).
Only 97 of those 150 are present in worldcup_stats_raw.csv, so the STATS MODEL can only rate the
teams in those 97 (the other 53 are mostly AFCON/AsianCup sides absent from the stats dataset).
The re-test therefore runs on those 97 fixtures, and the CONSTANT baseline is recomputed on the
SAME 97 for an apples-to-apples comparison; the constant baseline is ALSO computed on the full
150 to reproduce the original backtest numbers as a reconstruction check.

OUTPUT (read-only): props_retest_stats_inputs_report.txt + props_retest_stats_inputs_metrics.csv
                    + props_retest_stats_inputs_calibration.csv
NO API. NO Telegram. NO production file touched.
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

# --- reuse production math (no duplication) ---
import worldcup_player_props as PP   # predict_fixture, _logloss, _brier, _ece, poisson_p_ge1
import stats_model as SM             # walkforward, _load_raw

BT = ROOT / "data" / "processed" / "worldcup" / "props_backtest"
INT_RESULTS = HERE / "international_results.csv"
REPORT = HERE / "props_retest_stats_inputs_report.txt"
METRICS_CSV = HERE / "props_retest_stats_inputs_metrics.csv"
CALIB_CSV = HERE / "props_retest_stats_inputs_calibration.csv"

# documented constants from the first (confounded) backtest
CONST_TEAM_SHOTS = 12.0
CONST_MATCH_CARDS = 3.8

XI_SIZE = PP.XI_SIZE


# --------------------------------------------------------------- cached I/O (offline)
def _load_json(name):
    p = BT / name
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def confirmed_xi(fid, tid):
    """Confirmed startXI (<=11 player_ids) for team tid in fixture fid, from cached lineups.
    Mirrors worldcup_player_props.get_xi's confirmed-lineup path (offline, no API)."""
    data = _load_json(f"lineup_{fid}.json")
    for t in (data or []):
        if (t.get("team") or {}).get("id") == int(tid):
            xi = [int((p.get("player") or {}).get("id")) for p in (t.get("startXI") or [])
                  if (p.get("player") or {}).get("id") is not None]
            if len(xi) >= XI_SIZE:
                return xi[:XI_SIZE]
    return []


def team_rates(tid):
    """Prior-season (2023) aggregated /90 rates {pid: rate dict} from cache; {} if absent."""
    for f in os.listdir(BT):
        m = re.match(rf"rates_team{int(tid)}_s.*\.json", f)
        if m:
            d = _load_json(f)
            return {int(k): v for k, v in (d or {}).items()}
    return {}


def actuals(fid):
    """Per-player actuals from cached /fixtures/players. Mirrors cmd_settle parsing.
    Returns {pid: {'card':0/1, 'shots_on':float}}."""
    store = _load_json(f"fxplayers_{fid}.json")
    out = {}
    for t in (store or []):
        for pl in (t.get("players") or []):
            pid = (pl.get("player") or {}).get("id")
            sblk = (pl.get("statistics") or [{}])[0]
            sh = sblk.get("shots") or {}
            cd = sblk.get("cards") or {}
            if pid is None:
                continue
            out[int(pid)] = {
                "card": 1 if (PP._num(cd.get("yellow")) + PP._num(cd.get("red"))) > 0 else 0,
                "shots_on": PP._num(sh.get("on")),
            }
    return out


# --------------------------------------------------------------- stats-model walk-forward inputs
def build_model_inputs():
    """Leak-free per-(fixture,team_id) E[shots] and E[cards] from stats_model.walkforward.
    Returns dict[(fid,tid)] -> {'shots':lam, 'cards':lam}, and the set of fixtures covered."""
    df = SM._load_raw()
    os_mean = float(df["opp_str"].mean())
    os_std = float(df["opp_str"].std()) or 1.0
    df["opp_str_z"] = ((df["opp_str"].fillna(os_mean) - os_mean) / os_std).astype(float)
    teams = sorted(set(df["team_id"]) | set(df["opp_id"]))
    out = {}
    for stat in ("shots", "cards"):
        sub, y, lam_hat, oos = SM.walkforward(df, stat, teams)
        sub = sub.reset_index(drop=True)
        for i in range(len(sub)):
            fid = int(sub.at[i, "fixture_id"])
            tid = int(sub.at[i, "team_id"])
            if np.isfinite(lam_hat[i]):
                out.setdefault((fid, tid), {})[stat] = float(lam_hat[i])
    return out


# --------------------------------------------------------------- scoring
def score(p, y):
    p = np.asarray(p, float)
    y = np.asarray(y, float)
    base = float(y.mean())
    pbase = np.full_like(p, base, dtype=float)
    ll = PP._logloss(p, y)
    br = PP._brier(p, y)
    ece = PP._ece(p, y)
    llb = PP._logloss(pbase, y)
    brb = PP._brier(pbase, y)
    grad = bool(ll < llb and br < brb and ece <= 0.08)
    return {
        "n": int(len(y)), "base": base, "logloss": ll, "brier": br, "ece": ece,
        "ll_base": llb, "br_base": brb,
        "ll_skill_pct": 100 * (llb - ll) / llb if llb > 0 else 0.0,
        "br_skill_pct": 100 * (brb - br) / brb if brb > 0 else 0.0,
        "graduates": grad,
    }


def calibration_bands(p, y, edges=(0.0, 0.1, 0.2, 0.3, 0.5, 1.0)):
    p = np.asarray(p, float)
    y = np.asarray(y, float)
    rows = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        m = (p > lo) & (p <= hi) if i > 0 else (p >= lo) & (p <= hi)
        if m.sum():
            rows.append({"band": f"({lo:.2f},{hi:.2f}]", "n": int(m.sum()),
                         "pred_mean": float(p[m].mean()), "obs_rate": float(y[m].mean()),
                         "gap": float(p[m].mean() - y[m].mean())})
    return rows


# --------------------------------------------------------------- main
def run():
    ir = pd.read_csv(INT_RESULTS).set_index("fixture_id")
    model_in = build_model_inputs()
    covered = sorted({fid for (fid, _t) in model_in.keys()})

    bt_lineups = sorted(int(re.match(r"lineup_(\d+)", f).group(1))
                        for f in os.listdir(BT) if f.startswith("lineup_"))

    def fixtures_for(scope):
        if scope == "150":
            return [f for f in bt_lineups if f in ir.index]
        return [f for f in bt_lineups if f in ir.index and f in covered]

    def collect(fixtures, mode):
        """mode: 'const' or 'model'. Returns dict prop -> (p_list, y_list)."""
        acc = {"card": ([], []), "shot_on": ([], [])}
        used = 0
        for fid in fixtures:
            if fid not in ir.index:
                continue
            hid = int(ir.at[fid, "home_id"])
            aid = int(ir.at[fid, "away_id"])
            act = actuals(fid)
            if not act:
                continue
            sides_ok = False
            # match-total model cards (production consumes a MATCH total, split 50/50 inside)
            mc_h = model_in.get((fid, hid), {}).get("cards")
            mc_a = model_in.get((fid, aid), {}).get("cards")
            model_match_cards = (mc_h or 0.0) + (mc_a or 0.0) if (mc_h is not None or mc_a is not None) else None
            for tid in (hid, aid):
                xi = confirmed_xi(fid, tid)
                if not xi:
                    continue
                rates = team_rates(tid)
                if mode == "const":
                    team_shots = CONST_TEAM_SHOTS
                    match_cards = CONST_MATCH_CARDS
                else:
                    ts = model_in.get((fid, tid), {}).get("shots")
                    if ts is None or model_match_cards is None:
                        continue
                    team_shots = ts
                    match_cards = model_match_cards
                preds = PP.predict_fixture(1.0, team_shots, match_cards, xi, rates)
                for pr in preds:
                    pid = pr["player_id"]
                    a = act.get(pid)
                    if a is None:
                        continue
                    acc["card"][0].append(pr["p_card"]); acc["card"][1].append(a["card"])
                    y_son = 1 if a["shots_on"] >= 1 else 0
                    acc["shot_on"][0].append(pr["p_shot_on"]); acc["shot_on"][1].append(y_son)
                sides_ok = True
            if sides_ok:
                used += 1
        return acc, used

    lines = []
    def out(s=""):
        print(s); lines.append(s)

    out("=" * 92)
    out("RE-TEST · TARJETA y TIROS-A-PUERTA con INPUTS DEL MODELO DE STATS (vs constantes)")
    out("READ-ONLY · sin cambios en producción · sin API · sin Telegram")
    out("=" * 92)
    out(f"muestra original backtest: {len(fixtures_for('150'))} partidos cacheados (ene-jun 2024).")
    out(f"cubiertos por el modelo de stats (en worldcup_stats_raw.csv): {len(fixtures_for('97'))} partidos.")
    out("  -> los 53 restantes (AFCON/AsianCup en su mayoria) NO estan en el dataset del modelo;")
    out("     el modelo no puede ratearlos sin inventar. Se excluyen del re-test (documentado).")
    out("")
    out("ANTI-LEAKAGE confirmado:")
    out("  * rates /90 = temporada 2023 (estrictamente previa a los partidos de 2024).")
    out("  * betas del modelo de stats = walk-forward, refit solo con date<partido (MIN_PAST=150, HL=540d).")
    out("  * XI = startXI CONFIRMADO (input observado).  target = actuals (solo salida).")
    out("  * unica mira-adelante menor: feature opp_str (L3 final + estandarizacion full-sample),")
    out("    identica a la del modelo de stats de produccion; coef pequenio. Documentado.")
    out("")

    metrics_rows = []
    calib_rows = []

    def emit(title, acc, scope_tag, mode_tag):
        out("-" * 92)
        out(title)
        hdr = (f"  {'prop':9} {'n':>5} {'base%':>6} {'logloss':>8} {'ll_base':>8} {'ll_skill':>8} "
               f"{'brier':>7} {'br_base':>7} {'br_skill':>8} {'ECE':>6} {'GRADUA?':>8}")
        out(hdr); out("  " + "-" * (len(hdr) - 2))
        for prop in ("card", "shot_on"):
            p, y = acc[prop]
            if not y:
                out(f"  {prop:9}  (sin datos)"); continue
            s = score(p, y)
            out(f"  {prop:9} {s['n']:>5} {s['base']*100:>5.1f}% {s['logloss']:>8.4f} {s['ll_base']:>8.4f} "
                f"{s['ll_skill_pct']:>+7.1f}% {s['brier']:>7.4f} {s['br_base']:>7.4f} {s['br_skill_pct']:>+7.1f}% "
                f"{s['ece']:>6.3f} {('SI' if s['graduates'] else 'no'):>8}")
            metrics_rows.append({"scope": scope_tag, "inputs": mode_tag, "prop": prop, **s})
            for cb in calibration_bands(p, y):
                calib_rows.append({"scope": scope_tag, "inputs": mode_tag, "prop": prop, **cb})
        out("")

    # A) CONSTANTS on full 150 (reconstruction check vs original note: shots ECE~0.079; cards tail-optimist)
    accA, nA = collect(fixtures_for("150"), "const")
    emit(f"A) CONSTANTES (tiros=12, tarjetas=3.8) · muestra ORIGINAL ({nA} partidos) — reproduccion",
         accA, "150_const_recon", "const")

    # B) CONSTANTS on the 97 covered (apples-to-apples control)
    accB, nB = collect(fixtures_for("97"), "const")
    emit(f"B) CONSTANTES · MISMOS {nB} partidos del re-test (control apples-to-apples)",
         accB, "97_const", "const")

    # C) MODEL inputs on the 97 covered (the re-test)
    accC, nC = collect(fixtures_for("97"), "model")
    emit(f"C) INPUTS DEL MODELO DE STATS · {nC} partidos (EL RE-TEST)",
         accC, "97_model", "model")

    # calibration-by-band detail (B vs C) for the tail-optimism question
    out("-" * 92)
    out("CALIBRACION POR BANDA (B constantes vs C modelo, mismos 97 partidos)")
    cdf = pd.DataFrame(calib_rows)
    for prop in ("card", "shot_on"):
        out(f"\n  {prop.upper()}:")
        out(f"    {'banda':12} {'inputs':7} {'n':>5} {'pred%':>7} {'obs%':>7} {'gap':>7}")
        for scope, mode in (("97_const", "const"), ("97_model", "model")):
            sub = cdf[(cdf["scope"] == scope) & (cdf["prop"] == prop)]
            for _, r in sub.iterrows():
                out(f"    {r['band']:12} {mode:7} {int(r['n']):>5} {r['pred_mean']*100:>6.1f}% "
                    f"{r['obs_rate']*100:>6.1f}% {r['gap']*100:>+6.1f}%")
    out("")
    out("=" * 92)
    out("LECTURA:")
    out("  * skill>0 y GRADUA?=SI exige: logloss Y brier baten baseline Y ECE<=0.08.")
    out("  * compara B (constantes) vs C (modelo) en los MISMOS partidos para aislar el cambio de input.")
    out("  * 'gap' = pred% - obs% por banda; gap>0 en la cola = sobre-optimista (lo que se vio antes).")
    out("=" * 92)

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    pd.DataFrame(metrics_rows).to_csv(METRICS_CSV, index=False)
    cdf.to_csv(CALIB_CSV, index=False)
    print(f"\nWritten: {REPORT}")
    print(f"Written: {METRICS_CSV}")
    print(f"Written: {CALIB_CSV}")


if __name__ == "__main__":
    run()
