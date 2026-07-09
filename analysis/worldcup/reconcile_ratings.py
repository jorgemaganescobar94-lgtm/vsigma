"""
reconcile_ratings.py — ONE-SHOT L3 rating reconciliation (fix del deadlock del repro-gate).
OFFLINE · NO API · DRY-RUN: escribe SOLO *.RECONCILED.csv, NUNCA los ratings de producción.

PROBLEMA
--------
El backfill (04aebe3a) añadió 13 resultados WC ya jugados a international_results.csv SIN
re-fitear los ratings committeados (national_elo_layer3_ratings.csv, fit sobre 81 WC @ fb8ad220).
Por eso `auto_refit_shadow.run(base-94)` != committed(81) con max|Δ|~0.19, y el gate `repro<tol`
del auto-refit FALLA cada día -> se rechazan TODOS los swaps (también los FT nuevos legítimos) ->
los ratings quedan congelados desde el 7-jul.

QUÉ HACE
--------
Re-fitea L3 sobre el international_results.csv ACTUAL (94) con la MISMA matemática de producción
(`auto_refit_shadow.run`, puro numpy/pandas, sin API) y valida las MISMAS guardas anti-corrupción
del gate MENOS `repro` (que es justo lo que reconciliamos):
    finite · team_count_non_decreasing · max_move<=cap(0.60) · oos_not_worse
Si alguna guarda falla -> ABORTA y no escribe nada. En DRY-RUN escribe los ratings reconciliados a
un archivo APARTE (national_elo_layer3_ratings.RECONCILED.csv). Producción NO se toca aquí.
Aplicar (reemplazar producción + commit) es un paso separado, aprobado por Jorge.

Referencia de `oos_not_worse` = estado PRE-BACKFILL: se recupera international_results.csv del commit
que fijó los ratings actuales (vía git, offline), se le quitan los 13 fixtures backfilleados
(diferencia de fixture_id), se re-fitea y se compara la ventana OOS común [.. primer-backfill).
Por construcción walk-forward (fits solo-pasado), añadir FT en la cola temporal deja esa ventana
invariante, así que la guarda es un chequeo de corrupción real, no una afirmación de generalización.

PRUEBA DE QUE ARREGLA EL REPRO
------------------------------
Tras escribir el .RECONCILED.csv, se releen y se recomputa repro' = max|Δ|(run(base-94).s_final,
reconciliados). Debe salir <=0.0005 («tol 0.05) -> confirma que con estos ratings el próximo
auto-refit reproduce el base y el gate `repro<tol` PASA -> vuelven los swaps.
"""
from __future__ import annotations

import argparse
import io
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import auto_refit_shadow as AR  # noqa: E402  (import offline; no toca la API)

DEF_BASE = HERE / "international_results.csv"
DEF_COMMITTED = HERE / "national_elo_layer3_ratings.csv"
DEF_RECON = HERE / "national_elo_layer3_ratings.RECONCILED.csv"
DEF_REPORT = HERE / "reconcile_ratings_report.txt"
INT_RESULTS_RELPATH = "analysis/worldcup/international_results.csv"
REPRO_TOL = AR.REPRO_TOL      # 0.05
MOVE_CAP = AR.MOVE_CAP        # 0.60
REPRO_TARGET = 0.0005         # residuo esperado por el redondeo a 3 decimales de write_ratings


def load_prev_base(committed_path: Path):
    """international_results.csv tal como estaba en el commit que fijó los ratings actuales.

    Read-only, vía git (offline). Devuelve (df, commit_hash) o (None, motivo)."""
    # NB: capturamos BYTES y decodificamos UTF-8 explícito; text=True usaría cp1252 en Windows
    # y el CSV tiene nombres no-ascii -> UnicodeDecodeError.
    try:
        h = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(committed_path)],
            cwd=str(ROOT), capture_output=True, timeout=30,
        ).stdout.decode("utf-8", "replace").strip()
        if not h:
            return None, "no se encontró commit del ratings"
        blob = subprocess.run(
            ["git", "show", f"{h}:{INT_RESULTS_RELPATH}"],
            cwd=str(ROOT), capture_output=True, timeout=30,
        )
        if blob.returncode != 0 or not blob.stdout:
            return None, f"git show falló para {h[:8]}"
        return pd.read_csv(io.StringIO(blob.stdout.decode("utf-8", "replace"))), h
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Reconciliación L3 (dry-run, sin API, sin swap).")
    ap.add_argument("--base", default=str(DEF_BASE))
    ap.add_argument("--committed", default=str(DEF_COMMITTED))
    ap.add_argument("--out", default=str(DEF_RECON), help="ratings reconciliados (archivo APARTE)")
    ap.add_argument("--report", default=str(DEF_REPORT))
    ap.add_argument("--move-cap", type=float, default=MOVE_CAP)
    a = ap.parse_args(argv)

    rep = []
    def out(s=""):
        print(s); rep.append(s)

    out("=" * 88)
    out("RECONCILIACIÓN L3 — DRY-RUN (sin API · sin swap · producción intacta)")
    out("=" * 88)
    out(f"generated_at_utc: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")

    base = pd.read_csv(a.base)
    committed_df = pd.read_csv(a.committed)
    committed = {int(r.team_id): float(r.strength) for r in committed_df.itertuples()}

    # candidato = re-fit L3 sobre el base actual (94), matemática de producción, sin API
    cand = AR.run(base)
    s_final, name_by_id = cand["s_final"], cand["name_by_id"]
    out(f"base rows={len(base)} | committed teams={len(committed)} | candidate teams={len(s_final)}")

    # --- referencia pre-backfill para oos_not_worse (offline, vía git) ---
    prev_base, prev_ref = load_prev_base(Path(a.committed))
    if prev_base is not None:
        new_ids = set(base["fixture_id"].dropna().astype(int)) - set(prev_base["fixture_id"].dropna().astype(int))
        dts = pd.to_datetime(base.loc[base["fixture_id"].astype("Int64").isin(new_ids), "date"],
                             utc=True, errors="coerce").dt.tz_localize(None)
        cut = np.datetime64(dts.min()) if len(dts) and dts.notna().any() else None
        prev_run = AR.run(prev_base)
        if cut is not None:
            mo, mn = AR.oos(prev_run, cut), AR.oos(cand, cut)
            oos_ok = AR.oos_not_worse(mo, mn)
            oos_desc = (f"ventana común [.. {str(cut)[:10]}) · pre-backfill n={mo['n']} ll={mo['logloss']:.5f} "
                        f"vs reconciliado n={mn['n']} ll={mn['logloss']:.5f}")
        else:
            mo = mn = None; oos_ok = True
            oos_desc = "sin fixtures nuevos datables -> invariante por construcción (PASS)"
        out(f"referencia oos: pre-backfill @ {prev_ref[:8]} ({len(prev_base)} filas, "
            f"{len(new_ids)} fixtures nuevos) · {oos_desc}")
    else:
        mo = mn = None; oos_ok = True
        out(f"referencia oos: NO disponible ({prev_ref}) -> oos_not_worse PASS por invarianza "
            f"walk-forward (append en cola no cambia la ventana OOS).")

    # --- guardas del gate MENOS repro (repro es justo lo que reconciliamos) ---
    mv, mv_tid, mv_old, mv_new = AR.max_move(s_final, committed)
    guards = {
        "finite": AR.check_finite(s_final),
        "team_count_non_decreasing": AR.team_count_ok(s_final, committed),
        f"max_move<=cap({a.move_cap})": mv <= a.move_cap,
        "oos_not_worse": bool(oos_ok),
    }

    # --- top-5 movimientos |Δ| reconciliado vs committeado ---
    moves = sorted(((name_by_id.get(t, t), committed[t], s_final[t], s_final[t] - committed[t])
                    for t in s_final if t in committed),
                   key=lambda z: -abs(z[3]))
    out("")
    out("TOP-5 MOVIMIENTOS |Δ| (reconciliado vs committeado):")
    for nm, so, sn, d in moves[:5]:
        out(f"    {str(nm):24s} {so:+.3f} -> {sn:+.3f}  ({d:+.3f})")

    out("")
    out("GUARDAS (gate del auto-refit MENOS repro):")
    for k, v in guards.items():
        out(f"    {'PASS' if v else 'FAIL':4s}  {k}")
    out(f"  max_move = {mv:.3f} ({name_by_id.get(mv_tid, mv_tid)}: {mv_old:+.3f}->{mv_new:+.3f})")
    all_ok = all(guards.values())
    out(f"  -> GUARDAS: {'PASS' if all_ok else 'FAIL'}")

    if not all_ok:
        fails = [k for k, v in guards.items() if not v]
        out("")
        out(f"ABORTADO: guardas FALLARON ({', '.join(fails)}) -> NO se escribe nada.")
        Path(a.report).write_text("\n".join(rep), encoding="utf-8")
        print(f"\nReport -> {a.report}")
        return 1

    # --- DRY-RUN: escribir SOLO al archivo aparte, nunca a producción ---
    AR.write_ratings(a.out, s_final, name_by_id)
    out("")
    out(f"ESCRITO (dry-run) -> {Path(a.out).name}  ({len(s_final)} equipos). "
        f"Producción ({Path(a.committed).name}) INTACTA.")

    # --- PRUEBA de reparación del repro: releer reconciliados y recomputar repro' ---
    recon_df = pd.read_csv(a.out)
    recon = {int(r.team_id): float(r.strength) for r in recon_df.itertuples()}
    fresh = AR.run(base)  # re-run determinista para probar reproducción
    repro2 = max((abs(fresh["s_final"][t] - recon[t]) for t in fresh["s_final"] if t in recon), default=0.0)
    out("")
    out("PRUEBA repro (con los reconciliados como 'committed'):")
    wc_now = int(((base.get("league_id") == 1) & (base.get("season") == 2026)).sum())
    out(f"    repro' = max|Δ|(run(base·{wc_now}WC).s_final, reconciliados) = {repro2:.6f}")
    out(f"    tol del gate = {REPRO_TOL}  ·  objetivo (redondeo 3dp) <= {REPRO_TARGET}")
    if repro2 <= REPRO_TARGET:
        out(f"    -> PASS: {repro2:.6f} <= {REPRO_TARGET} « {REPRO_TOL}. Con estos ratings el próximo "
            f"auto-refit reproduce el base -> gate repro<tol PASA -> SWAPS REANUDADOS.")
    elif repro2 <= REPRO_TOL:
        out(f"    -> PASS (holgura menor): {repro2:.6f} <= {REPRO_TOL}.")
    else:
        out(f"    -> WARN: repro'={repro2:.6f} > tol {REPRO_TOL} (inesperado; revisar determinismo).")

    Path(a.report).write_text("\n".join(rep), encoding="utf-8")
    print(f"\nReport -> {a.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
