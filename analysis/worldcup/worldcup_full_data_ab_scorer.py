"""
WORLD CUP 2026 — MARCADOR ACUMULADO "FULL-DATA vs ENSEMBLE" (read-only · NO model touch · NO API).

Árbitro EN VIVO, HONESTO, del A/B de la decisión explícita de Jorge (2026-07-01): el modelo full-data
(fd_*, ingiere TODAS las features) corre EN VIVO como base mostrada; el ensemble (ens_*) queda como
sombra. Se ESPERA que el full-data mida PEOR (backtests probaron features de stats/rating nulas para
1X2 de selecciones). Este marcador NO recalcula nada ni toca el modelo: LEE dos logs ya escritos —
  * worldcup_full_data_ab_log.csv  (fd_* y ens_* CONGELADOS al predecir, uno por fixture)
  * worldcup_predictions_log.csv   (result_1x2 + settled tras liquidar)
— y mide el cara a cara ACUMULADO sobre los partidos liquidados con predicción fd (desde que entró).

ANTI-HINDSIGHT: solo filas settled==1 con result_1x2 en {H,D,A} y fd_*/ens_* no nulos. Nada se rellena
retroactivamente. Reporta el peor sin maquillar.

SALIDA (git-add explícito): worldcup_full_data_ab_scorecard.txt / .csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
AB_LOG = HERE / "worldcup_full_data_ab_log.csv"
PRED_LOG = HERE / "worldcup_predictions_log.csv"
TXT = HERE / "worldcup_full_data_ab_scorecard.txt"
CSV = HERE / "worldcup_full_data_ab_scorecard.csv"

SMALL_N = 30
TIE = 5e-4
RES_IDX = {"H": 0, "D": 1, "A": 2}

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _ll(P, y):
    P = np.clip(P, 1e-15, 1.0); P = P / P.sum(1, keepdims=True)
    return float(-np.mean(np.log(P[np.arange(len(y)), y])))


def _brier(P, y):
    Y = np.eye(3)[y]
    return float(np.mean(np.sum((P - Y) ** 2, axis=1)))


def _acc(P, y):
    return float(np.mean(P.argmax(1) == y))


def run():
    lines, rows = [], []

    def out(s=""):
        print(s); lines.append(s)

    if not AB_LOG.exists():
        out("FULL-DATA A/B: sin log todavía (worldcup_full_data_ab_log.csv). Nada que puntuar.")
        TXT.write_text("\n".join(lines), encoding="utf-8")
        return
    ab = pd.read_csv(AB_LOG)
    if PRED_LOG.exists():
        pl = pd.read_csv(PRED_LOG)[["fixture_id", "result_1x2", "settled"]]
        ab = ab.merge(pl, on="fixture_id", how="left")
    else:
        ab["result_1x2"] = np.nan; ab["settled"] = np.nan

    need = ["fd_home", "fd_draw", "fd_away", "ens_home", "ens_draw", "ens_away"]
    m = ab["settled"].fillna(0).astype(float).eq(1) & ab["result_1x2"].isin(list(RES_IDX))
    for c in need:
        m &= ab[c].notna()
    s = ab[m].copy()
    n = len(s)

    out("=" * 84)
    out("MARCADOR FULL-DATA vs ENSEMBLE (1X2) — acumulado, read-only, HONESTO (se espera PEOR)")
    out("=" * 84)
    if n == 0:
        out("Aún no hay partidos liquidados con predicción full-data. Acumulando.")
        TXT.write_text("\n".join(lines), encoding="utf-8")
        pd.DataFrame(columns=["market", "metric", "full_data", "ensemble", "leader", "diff", "n"]).to_csv(CSV, index=False)
        return

    y = s["result_1x2"].map(RES_IDX).to_numpy(int)
    Pfd = s[["fd_home", "fd_draw", "fd_away"]].to_numpy(float)
    Pen = s[["ens_home", "ens_draw", "ens_away"]].to_numpy(float)

    for metric, fn, worse_is_lower in (("logloss", _ll, True), ("brier", _brier, True), ("acc", _acc, False)):
        vfd = fn(Pfd, y); ven = fn(Pen, y)
        if abs(vfd - ven) < TIE:
            leader = "empate"
        elif (vfd < ven) == worse_is_lower:
            leader = "full-data"
        else:
            leader = "ensemble"
        tag = "" if n >= SMALL_N else "  (N<30, orientativo)"
        out(f"  {metric:8}  full-data={vfd:.4f}   ensemble={ven:.4f}   lider={leader}   dif={abs(vfd-ven):.4f}{tag}")
        rows.append({"market": "1x2", "metric": metric, "full_data": round(vfd, 4),
                     "ensemble": round(ven, 4), "leader": leader, "diff": round(abs(vfd - ven), 4), "n": n})

    out("")
    out(f"N liquidados con fd = {n}. Lectura honesta: si full-data queda por detrás (esperado), este")
    out("marcador + el A/B offline son la base para revertir FULL_DATA_LIVE=False. NO se afirma precisión.")
    TXT.write_text("\n".join(lines), encoding="utf-8")
    pd.DataFrame(rows).to_csv(CSV, index=False)
    print(f"\nWritten: {TXT}\nWritten: {CSV}")


if __name__ == "__main__":
    run()
