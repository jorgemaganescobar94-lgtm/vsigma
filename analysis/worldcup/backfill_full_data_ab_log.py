"""
WORLD CUP 2026 — BACKFILL del A/B FULL-DATA vs ENSEMBLE (offline, 0 API, leakage-free).

CONTEXTO: por un bug de persistencia (worldcup_full_data_ab_log.csv NO estaba en el git-add
explícito del workflow), las filas fd_*/ens_* que build_worldcup_cards.py escribía en cada corrida
de CI nunca se commiteaban -> el A/B quedaba SIEMPRE vacío en el repo. Este script RECONSTRUYE esas
filas para los partidos YA LIQUIDADOS del log, de forma HONESTA y sin look-ahead:

  * fd_*  = worldcup_full_data_model.predict() con el ARTIFACT FIJO (entrenado en burn-in <2024, no
            se re-entrena a diario) y features POINT-IN-TIME (todas usan estrictamente date < kickoff,
            ver Sources._decayed_past_mean / form_ewma / h2h_gd: filtran x[0] < when). Reconstruir hoy
            un fixture pasado da EXACTAMENTE lo que el modelo habría predicho entonces: los resultados
            posteriores no cambian las features previas al saque. -> LEAKAGE-FREE.
  * ens_* = blend 50/50 renormalizado de los mx_*/l3_* CONGELADOS que ya están en el log (idéntico a
            build_worldcup_cards.blend_1x2). No se recalcula ningún modelo; se leen del log.

Se replica FIELMENTE el contrato del live: una fila solo existe si hay mx_* y l3_* (para formar el
ensemble, igual que la condición `pd.notna(rec.get("ens_home"))` del live) y predict() no soft-failea.
neutral=1 igual que el live (build_worldcup_cards pasa 1 fijo). home_id/away_id se mapean desde
international_results.csv (offline). El resultado real lo aporta el scorer desde el predictions_log;
aquí NO se escribe ningún resultado (anti-hindsight).

MERGE: dedup por fixture_id. Las filas YA existentes (escritas por un live real) MANDAN sobre la
reconstrucción (son ground-truth congelado); el backfill solo rellena huecos.

SALIDA (git-add explícito): worldcup_full_data_ab_log.csv
Uso:
  python analysis/worldcup/backfill_full_data_ab_log.py            # escribe/mergea el log
  python analysis/worldcup/backfill_full_data_ab_log.py --dry-run  # solo reporta, no escribe
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import worldcup_full_data_model as ffdm  # noqa: E402

LOG = HERE / "worldcup_predictions_log.csv"
IR = HERE / "international_results.csv"
AB_LOG = HERE / "worldcup_full_data_ab_log.csv"

# Column order matches EXACTLY what build_worldcup_cards.py writes (so a later live run appends cleanly).
AB_COLUMNS = ["fixture_id", "kickoff_utc", "home", "away",
              "fd_home", "fd_draw", "fd_away", "ens_home", "ens_draw", "ens_away",
              "n_features", "n_missing"]


def blend_1x2(ph_a, pd_a, pa_a, ph_b, pd_b, pa_b):
    """Renormalised 50/50 mean of two 1X2 triples. IDENTICAL to build_worldcup_cards.blend_1x2
    (replicated here to avoid importing that module, which pulls the API client). Pure, no model."""
    vals = [ph_a, pd_a, pa_a, ph_b, pd_b, pa_b]
    if any(v is None or pd.isna(v) for v in vals):
        return None
    try:
        p = np.array([(float(ph_a) + float(ph_b)) / 2.0,
                      (float(pd_a) + float(pd_b)) / 2.0,
                      (float(pa_a) + float(pa_b)) / 2.0])
    except (TypeError, ValueError):
        return None
    s = float(p.sum())
    if not (s > 0) or not np.isfinite(s):
        return None
    p = p / s
    return float(p[0]), float(p[1]), float(p[2])


def _id_map(ir_df):
    """fixture_id -> (home_id, away_id) from international_results.csv (offline, no API)."""
    out = {}
    for r in ir_df.dropna(subset=["fixture_id", "home_id", "away_id"]).itertuples(index=False):
        try:
            out[int(r.fixture_id)] = (int(r.home_id), int(r.away_id))
        except (TypeError, ValueError):
            continue
    return out


def reconstruct(log_df, ir_df):
    """Return a list of AB-log row dicts for every SETTLED fixture that has frozen mx_* and l3_*
    (so the ensemble is formable) and for which predict() succeeds. Point-in-time, leakage-free."""
    idmap = _id_map(ir_df)
    rows = []
    settled = log_df[log_df["settled"].fillna(0).astype(float).eq(1)]
    for r in settled.itertuples(index=False):
        # ensemble from the FROZEN mx_*/l3_* already in the log (skip if either missing)
        ens = blend_1x2(getattr(r, "mx_home", None), getattr(r, "mx_draw", None), getattr(r, "mx_away", None),
                        getattr(r, "l3_home", None), getattr(r, "l3_draw", None), getattr(r, "l3_away", None))
        if ens is None:
            continue
        ids = idmap.get(int(r.fixture_id))
        if ids is None:
            continue
        hid, aid = ids
        when = str(r.kickoff_utc)[:10]          # date only, same slice the live passes ((ko)[:10])
        # full-data prediction: strength feature = the frozen L3 (l3_*/l3_xg_*); neutral=1 like live
        fd = ffdm.predict(hid, aid, when, 1,
                          _f(getattr(r, "l3_home", None)), _f(getattr(r, "l3_draw", None)),
                          _f(getattr(r, "l3_away", None)),
                          _f(getattr(r, "l3_xg_home", None)), _f(getattr(r, "l3_xg_away", None)))
        if fd is None:
            continue
        rows.append({
            "fixture_id": int(r.fixture_id), "kickoff_utc": r.kickoff_utc,
            "home": r.home, "away": r.away,
            "fd_home": fd["fd_home"], "fd_draw": fd["fd_draw"], "fd_away": fd["fd_away"],
            "ens_home": round(ens[0], 4), "ens_draw": round(ens[1], 4), "ens_away": round(ens[2], 4),
            "n_features": fd["n_features"], "n_missing": fd["n_missing"]})
    return rows


def _f(v):
    """None-safe float (log cells may be NaN)."""
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main(dry_run=False):
    log_df = pd.read_csv(LOG)
    ir_df = pd.read_csv(IR)
    rows = reconstruct(log_df, ir_df)
    print(f"Backfill: {len(rows)} fixture(s) liquidados reconstruidos (fd_* point-in-time + ens_* congelado).")
    if not rows:
        print("Nada que escribir.")
        return 0

    # merge/dedup by fixture_id; EXISTING (live-written) rows win over reconstruction
    merged = {}
    for row in rows:                                   # reconstruction first...
        merged[int(row["fixture_id"])] = row
    n_preserved = 0
    if AB_LOG.exists():
        old = pd.read_csv(AB_LOG)
        for _, rr in old.iterrows():                   # ...then existing overwrites (ground-truth)
            merged[int(rr["fixture_id"])] = rr.to_dict()
            n_preserved += 1
        print(f"Merge: {n_preserved} fila(s) live existentes PRESERVADAS (mandan sobre el backfill).")

    df = pd.DataFrame([merged[k] for k in merged])
    ordered = AB_COLUMNS + [c for c in df.columns if c not in AB_COLUMNS]
    df = df[ordered].sort_values("kickoff_utc").reset_index(drop=True)
    if dry_run:
        print("--dry-run: no se escribe. Preview:")
        print(df[["fixture_id", "home", "away", "fd_home", "ens_home"]].to_string(index=False))
        return 0
    df.to_csv(AB_LOG, index=False)
    print(f"Escrito -> {AB_LOG.name}  ({len(df)} filas)")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="reporta sin escribir")
    a = ap.parse_args()
    raise SystemExit(main(dry_run=a.dry_run))
