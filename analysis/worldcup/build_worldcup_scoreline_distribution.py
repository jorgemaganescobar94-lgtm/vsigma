"""
WORLD CUP 2026 — SCORELINE DISTRIBUTION (Fase 4K). READ-ONLY · NO API · NO scraping · NO web · NO
market/odds/betting · NO fabrication · NO secrets. Pure football. The base model is NOT modified —
this is a structured DERIVED output (top-3/5 scorelines) from the xG/λ the system already produces.

For each fixture with numeric expected goals, builds an independent-Poisson scoreline grid (0..MAXG per
side), the top-5 most likely scorelines, and the 1X2 distribution implied by that grid (a sanity check
against the existing 1X2). λ priority is safe and explicit; a non-numeric value never reaches the math
(safe_num) — the inj_home/inj_away string bug cannot recur.

λ priority (spec §2): inj_xg > ctx_xg > mx_xg > l3_xg > our_xg. No λ -> fixture NOT generated (no_evaluable).

Outputs:
  * worldcup_scoreline_distribution.csv   (one row per top scoreline per fixture)
  * worldcup_scoreline_distribution.json  (grouped by fixture)
  * worldcup_scoreline_distribution_report.txt

Run:  python analysis/worldcup/build_worldcup_scoreline_distribution.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

PRED_LOG = HERE / "worldcup_predictions_log.csv"
OUT_CSV = HERE / "worldcup_scoreline_distribution.csv"
OUT_JSON = HERE / "worldcup_scoreline_distribution.json"
OUT_TXT = HERE / "worldcup_scoreline_distribution_report.txt"

MAXG = 10          # grid 0..MAXG per side for the 1X2 derivation (top-5 are always low scores)
TOP_N = 5
LAMBDA_PREFIXES = ("inj", "ctx", "mx", "l3", "our")   # spec §2 priority

CSV_COLUMNS = [
    "fixture_id", "kickoff_utc", "home", "away", "source_lambda", "lambda_home", "lambda_away",
    "rank", "score_home", "score_away", "scoreline", "probability", "implied_result",
    "distribution_home_win", "distribution_draw", "distribution_away_win",
    "data_quality", "confidence", "reason",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ safe coercion (no string bug)
def safe_num(v):
    try:
        if v is None:
            return None
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if (f == f and f not in (float("inf"), float("-inf"))) else None


def safe_prob(v):
    f = safe_num(v)
    return f if (f is not None and 0.0 <= f <= 1.0) else None


def _r(v, nd=4):
    return None if v is None else round(float(v), nd)


# ============================================================ Poisson core (pure, reusable, testable)
def poisson_pmf(k, lam):
    """P(X=k) for X~Poisson(lam). 0 for negative/invalid."""
    lam = safe_num(lam)
    if lam is None or lam < 0 or k < 0:
        return 0.0
    return math.exp(-lam) * (lam ** k) / math.factorial(k)


def scoreline_distribution(lambda_home, lambda_away, maxg=MAXG):
    """Independent-Poisson grid {(i,j): prob} over 0..maxg, normalised to sum 1 (tail folded in).
    Returns ({}, None) when either λ is missing/invalid — NEVER fabricates."""
    lh, la = safe_num(lambda_home), safe_num(lambda_away)
    if lh is None or la is None or lh < 0 or la < 0:
        return {}, None
    ph = [poisson_pmf(i, lh) for i in range(maxg + 1)]
    pa = [poisson_pmf(j, la) for j in range(maxg + 1)]
    grid = {(i, j): ph[i] * pa[j] for i in range(maxg + 1) for j in range(maxg + 1)}
    total = sum(grid.values())
    if total <= 0:
        return {}, None
    grid = {k: v / total for k, v in grid.items()}
    return grid, total


def implied_result(i, j):
    return "H" if i > j else ("A" if i < j else "D")


def top_scorelines(grid, n=TOP_N):
    """Top-n (score_home, score_away, probability) sorted by probability desc, then by lower total."""
    items = sorted(grid.items(), key=lambda kv: (-kv[1], kv[0][0] + kv[0][1], kv[0][0]))
    return [{"score_home": i, "score_away": j, "scoreline": f"{i}-{j}",
             "probability": round(p, 4), "implied_result": implied_result(i, j)}
            for (i, j), p in items[:n]]


def distribution_1x2(grid):
    """1X2 implied by the grid: (home_win, draw, away_win)."""
    hw = sum(p for (i, j), p in grid.items() if i > j)
    dr = sum(p for (i, j), p in grid.items() if i == j)
    aw = sum(p for (i, j), p in grid.items() if i < j)
    return {"home_win": round(hw, 4), "draw": round(dr, 4), "away_win": round(aw, 4)}


def resolve_lambdas(row, prefixes=LAMBDA_PREFIXES):
    """First numeric (xg_home, xg_away) pair by priority. Returns (lh, la, source) or (None, None, None)."""
    for pre in prefixes:
        h, a = safe_num(row.get(f"{pre}_xg_home")), safe_num(row.get(f"{pre}_xg_away"))
        if h is not None and a is not None:
            return h, a, pre
    return None, None, None


# ============================================================ per-fixture build
def build_fixture_distribution(row):
    """Build the §3 per-fixture distribution dict, or a no_evaluable stub. NEVER fabricates λ."""
    lh, la, src = resolve_lambdas(row)
    fid = row.get("fixture_id")
    base = {"fixture_id": int(fid) if pd.notna(fid) else None,
            "home": row.get("home"), "away": row.get("away"),
            "kickoff_utc": row.get("kickoff_utc")}
    if lh is None:
        base.update({"lambda_home": None, "lambda_away": None, "source_lambda": None,
                     "top_5_scorelines": [], "distribution_1x2": None,
                     "data_quality": "baja", "confidence": "baja",
                     "reason": "sin goles esperados (xG/λ) numéricos — no se genera distribución"})
        return base
    grid, _ = scoreline_distribution(lh, la)
    top5 = top_scorelines(grid, TOP_N)
    d1x2 = distribution_1x2(grid)
    base.update({"lambda_home": _r(lh, 3), "lambda_away": _r(la, 3), "source_lambda": src,
                 "top_5_scorelines": top5, "distribution_1x2": d1x2,
                 "data_quality": "media", "confidence": "media",
                 "reason": f"Poisson independiente sobre λ={src}_xg (modelo base sin modificar)"})
    return base


# ============================================================ build / I/O
def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


def build(pred_log=PRED_LOG, write=True):
    pred = _read_csv(pred_log)
    fixtures, csv_rows = [], []
    if pred is not None and {"fixture_id"} <= set(pred.columns):
        for _, r in pred.iterrows():
            fx = build_fixture_distribution(r)
            if fx["fixture_id"] is None:
                continue
            fixtures.append(fx)
            if not fx["top_5_scorelines"]:
                continue
            d = fx["distribution_1x2"] or {}
            for rank, sc in enumerate(fx["top_5_scorelines"], 1):
                csv_rows.append({
                    "fixture_id": fx["fixture_id"], "kickoff_utc": fx["kickoff_utc"],
                    "home": fx["home"], "away": fx["away"], "source_lambda": fx["source_lambda"],
                    "lambda_home": fx["lambda_home"], "lambda_away": fx["lambda_away"],
                    "rank": rank, "score_home": sc["score_home"], "score_away": sc["score_away"],
                    "scoreline": sc["scoreline"], "probability": sc["probability"],
                    "implied_result": sc["implied_result"],
                    "distribution_home_win": d.get("home_win"), "distribution_draw": d.get("draw"),
                    "distribution_away_win": d.get("away_win"),
                    "data_quality": fx["data_quality"], "confidence": fx["confidence"],
                    "reason": fx["reason"],
                })
    payload = {"meta": {"fixtures_total": len(fixtures),
                        "fixtures_with_distribution": sum(1 for f in fixtures if f["top_5_scorelines"]),
                        "maxg": MAXG, "top_n": TOP_N,
                        "method": "Poisson independiente sobre xG/λ existente; modelo base NO modificado; "
                                  "λ priority inj>ctx>mx>l3>our; safe_num evita el bug de strings."},
               "scoreline_distribution": fixtures}
    if write:
        pd.DataFrame(csv_rows, columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
        Path(OUT_JSON).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(payload) + "\n", encoding="utf-8")
    return payload


def render_txt(payload) -> str:
    meta = payload["meta"]
    L = ["===== WORLD CUP — DISTRIBUCIÓN DE MARCADORES (Fase 4K) =====", "",
         f"Fixtures: {meta['fixtures_total']} · con distribución: {meta['fixtures_with_distribution']} "
         f"(grid 0..{meta['maxg']}, top-{meta['top_n']})", ""]
    shown = [f for f in payload["scoreline_distribution"] if f["top_5_scorelines"]][:8]
    for f in shown:
        d = f["distribution_1x2"] or {}
        L.append(f"  {f['home']} vs {f['away']}  (λ {f['lambda_home']}-{f['lambda_away']} · {f['source_lambda']})")
        tops = " · ".join(f"{s['scoreline']} {s['probability']*100:.0f}%" for s in f["top_5_scorelines"])
        L.append(f"      top-5: {tops}")
        L.append(f"      1X2 derivado: V {d.get('home_win')} · E {d.get('draw')} · D {d.get('away_win')}")
    L.append("")
    L.append("Predicción futbolística pura, sin terminología de juego. Salida derivada del xG existente; "
             "el modelo base NO se modifica. NO toca data/external.")
    return "\n".join(L)


def main():
    p = build()
    m = p["meta"]
    print(f"scoreline distribution: {m['fixtures_with_distribution']}/{m['fixtures_total']} fixtures "
          f"-> {OUT_CSV.name} / {OUT_JSON.name}")
    for f in [x for x in p["scoreline_distribution"] if x["top_5_scorelines"]][:5]:
        tops = ", ".join(f"{s['scoreline']} {s['probability']*100:.0f}%" for s in f["top_5_scorelines"][:3])
        print(f"  {f['home']} vs {f['away']}: {tops}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
