"""
WORLD CUP 2026 — DISPLAY-CORRECTION READINESS GATE (Fase 4O). SHADOW · READ-ONLY · NO API · NO scraping
· NO web · NO market/odds/betting · NO fabrication · NO secrets · NO external sources. Pure football.
ALERT ONLY — it NEVER activates anything. It aggregates the Fase-4N shadow evaluations (team SOT, team
shots, team corners) and reports, per module and globally, whether a display-only level correction is
READY to be PROPOSED for activation in a later, explicitly-approved phase.

Per module it computes the gates (sample / improvement / bias / no-strong-inversion / anti-look-ahead
available / data quality) and a readiness_status:
  NOT_READY_SAMPLE        n < N_MIN_ACTIVATE (50).
  NOT_READY_NO_SIGNAL     n >= 50 but delta_mae_pre_fixture < DELTA_MAE_MATERIAL (or no anti-look-ahead).
  NOT_READY_BIAS_INVERSION the correction strongly inverts the bias.
  READY_FOR_PROPOSAL      all gates pass (still 🔴 to actually activate — proposal only).
  WATCH                   positive signal but a minor gate (e.g. data quality) does not pass yet.

Global: should_propose_activation_any = True only if at least one module is READY_FOR_PROPOSAL. With the
current state (every module n<50) this is False — nothing is proposed, nothing is activated.

SOURCES (read-only; JSON preferred, CSV fallback): worldcup_team_sot_correction_shadow_monitor.json/.csv,
worldcup_team_stats_level_correction_shadow_summary.json/.csv, worldcup_prediction_accuracy.csv (the 4J
panel, read only to cross-check the shadow modules exist).

OUTPUT (read-only; explicit git-add only):
  * worldcup_display_correction_readiness.csv         (one row per module: metrics + gates + status)
  * worldcup_display_correction_readiness.json        (regenerable -> gitignored)
  * worldcup_display_correction_readiness_report.txt  (no betting language; regenerable -> gitignored)

Run:  python analysis/worldcup/monitor_worldcup_display_correction_readiness.py
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import evaluate_worldcup_team_sot_level_correction as lc      # thresholds (single source of truth)
import monitor_worldcup_team_sot_correction_shadow as mon     # MIN_CORRECTED_ROWS
import display_level_correction as dlc                        # Fase 4P skeleton config status (read-only)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SOT_MONITOR_JSON = HERE / "worldcup_team_sot_correction_shadow_monitor.json"
SOT_MONITOR_CSV = HERE / "worldcup_team_sot_correction_shadow_monitor.csv"
STATS_SHADOW_JSON = HERE / "worldcup_team_stats_level_correction_shadow_summary.json"
STATS_SHADOW_CSV = HERE / "worldcup_team_stats_level_correction_shadow.csv"
PANEL_CSV = HERE / "worldcup_prediction_accuracy.csv"

OUT_CSV = HERE / "worldcup_display_correction_readiness.csv"
OUT_JSON = HERE / "worldcup_display_correction_readiness.json"
OUT_TXT = HERE / "worldcup_display_correction_readiness_report.txt"

N_MIN_ACTIVATE = lc.N_MIN_ACTIVATE
DELTA_MAE_MATERIAL = lc.DELTA_MAE_MATERIAL
MIN_CORRECTED_ROWS = mon.MIN_CORRECTED_ROWS

CSV_COLUMNS = ["module", "n", "rows_to_min_sample", "metric_original_mae",
               "metric_corrected_mae_pre_fixture", "delta_mae_pre_fixture", "delta_rmse_pre_fixture",
               "original_bias", "corrected_bias_pre_fixture", "bias_reduction", "direction_stable",
               "sample_gate", "improvement_gate", "bias_gate", "no_strong_bias_inversion_gate",
               "anti_lookahead_available", "data_quality", "confidence", "readiness_status", "reason"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _num(v):
    try:
        if v is None or v == "":
            return None
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if (f == f and f not in (float("inf"), float("-inf"))) else None


def _read_json(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return None
    try:
        df = pd.read_csv(p)
    except Exception:
        return None
    return df if len(df) else None


# ===================================================================== load per-module raw metrics
def load_sot_metrics():
    """Headline SOT metrics from the Fase-4N monitor (JSON preferred, CSV fallback). anti-look-ahead is
    available whenever the monitor produced a pre_fixture delta. Returns dict or None."""
    j = _read_json(SOT_MONITOR_JSON)
    if j and j.get("n_team_rows"):
        return {"n": int(j.get("n_team_rows") or 0),
                "original_mae": _num(j.get("original_mae")),
                "corrected_mae_pre": _num(j.get("pre_fixture_mae")),
                "delta_mae": _num(j.get("delta_mae_pre_fixture")),
                "delta_rmse": _num(j.get("delta_rmse_pre_fixture")),
                "original_bias": _num(j.get("original_bias")),
                "corrected_bias": _num(j.get("pre_fixture_bias")),
                "n_corrected": int(j.get("n_corrected") or 0),
                "anti_available": j.get("delta_mae_pre_fixture") is not None}
    df = _read_csv(SOT_MONITOR_CSV)
    if df is not None and len(df):
        r = df.iloc[0]
        return {"n": int(_num(r.get("n_team_rows")) or 0),
                "original_mae": _num(r.get("original_mae")),
                "corrected_mae_pre": _num(r.get("pre_fixture_mae")),
                "delta_mae": _num(r.get("delta_mae_pre_fixture")),
                "delta_rmse": _num(r.get("delta_rmse_pre_fixture")),
                "original_bias": _num(r.get("original_bias")),
                "corrected_bias": _num(r.get("pre_fixture_bias")),
                "n_corrected": int(_num(r.get("n_corrected")) or 0),
                "anti_available": _num(r.get("delta_mae_pre_fixture")) is not None}
    return None


def load_stat_metrics(stat):
    """Headline metrics for a team stat (shots/corners) from the Fase-4N shadow summary (JSON preferred,
    CSV fallback). anti_available is False for aggregate-only mode. Returns dict or None."""
    j = _read_json(STATS_SHADOW_JSON)
    if j:
        st = (j.get("stats") or {}).get(stat)
        if st and st.get("n"):
            mode = st.get("mode")
            orig = st.get("original", {}) or {}
            pf = st.get("pre_fixture", {}) or {}
            return {"n": int(st.get("n") or 0),
                    "original_mae": _num(orig.get("mae")),
                    "corrected_mae_pre": _num(pf.get("corrected_mae")),
                    "delta_mae": _num(pf.get("delta_mae")),
                    "delta_rmse": _num(pf.get("delta_rmse")),
                    "original_bias": _num(orig.get("bias")),
                    "corrected_bias": _num(pf.get("corrected_bias")),
                    "n_corrected": int(pf.get("n_corrected") or 0),
                    "anti_available": mode == "per_fixture"}
    df = _read_csv(STATS_SHADOW_CSV)
    if df is not None and "stat" in df.columns:
        sub = df[df["stat"].astype(str) == stat]
        if len(sub):
            base = sub.iloc[0]
            pf_row = sub[sub["correction_type"] == "pre_fixture"]
            pf = pf_row.iloc[0] if len(pf_row) else base
            mode_anti = "pre_fixture" in set(sub["correction_type"].astype(str))
            return {"n": int(_num(base.get("n")) or 0),
                    "original_mae": _num(base.get("original_mae")),
                    "corrected_mae_pre": _num(pf.get("corrected_mae")),
                    "delta_mae": _num(pf.get("delta_mae")),
                    "delta_rmse": None,
                    "original_bias": _num(base.get("original_bias")),
                    "corrected_bias": _num(pf.get("corrected_bias")),
                    "n_corrected": 0, "anti_available": mode_anti}
    return None


# ===================================================================== readiness gate (pure)
def decide_readiness(m):
    """Pure gate. m: per-module metrics dict. Returns a dict with the gates, direction_stable and
    readiness_status. Sample shortfall dominates (NOT_READY_SAMPLE) per governance."""
    n = m.get("n") or 0
    dmae = m.get("delta_mae")
    drmse = m.get("delta_rmse")
    bias_o = m.get("original_bias")
    bias_c = m.get("corrected_bias")
    n_corr = m.get("n_corrected") or 0
    anti = bool(m.get("anti_available"))

    sample_gate = n >= N_MIN_ACTIVATE
    improvement_gate = (dmae is not None and dmae >= DELTA_MAE_MATERIAL
                        and (drmse is None or drmse >= 0))
    bias_gate = (bias_o is not None and bias_c is not None and abs(bias_c) < abs(bias_o) - 1e-9)
    strong_inversion = (bias_o is not None and bias_c is not None and (bias_c * bias_o < 0)
                        and abs(bias_c) > 0.5 * abs(bias_o) + 1e-9)
    no_strong_inversion = not strong_inversion
    data_quality_ok = anti and n_corr >= MIN_CORRECTED_ROWS
    direction_stable = bool(bias_gate and no_strong_inversion)

    if not sample_gate:
        status = "NOT_READY_SAMPLE"
    elif not anti:
        status = "NOT_READY_NO_SIGNAL"
    elif strong_inversion:
        status = "NOT_READY_BIAS_INVERSION"
    elif not improvement_gate:
        status = "NOT_READY_NO_SIGNAL"
    elif bias_gate and (drmse is None or drmse >= 0) and data_quality_ok:
        status = "READY_FOR_PROPOSAL"
    else:
        status = "WATCH"

    return {"sample_gate": sample_gate, "improvement_gate": improvement_gate, "bias_gate": bias_gate,
            "no_strong_bias_inversion_gate": no_strong_inversion,
            "anti_lookahead_available": anti, "data_quality_ok": data_quality_ok,
            "direction_stable": direction_stable, "readiness_status": status, "n_corrected": n_corr}


def _module_reason(status, m, g):
    n = m.get("n") or 0
    if status == "NOT_READY_SAMPLE":
        return f"n={n} < {N_MIN_ACTIVATE} (faltan {max(0, N_MIN_ACTIVATE - n)} filas); señal aparte."
    if status == "NOT_READY_NO_SIGNAL":
        if not g["anti_lookahead_available"]:
            return "sin anti-look-ahead disponible (solo agregado) -> no se puede declarar readiness."
        return f"n>= {N_MIN_ACTIVATE} pero ΔMAE pre_fixture < {DELTA_MAE_MATERIAL}: sin señal material."
    if status == "NOT_READY_BIAS_INVERSION":
        return "la corrección invierte el sesgo de forma fuerte -> no apta."
    if status == "READY_FOR_PROPOSAL":
        return "todas las puertas OK -> candidata a PROPUESTA de activación (🔴, fase posterior)."
    return "señal positiva pero alguna puerta menor (p.ej. data quality) aún no pasa."


# ===================================================================== build
MODULES = [
    ("team_sot_display_correction", "SOT", load_sot_metrics),
    ("team_shots_display_correction", "tiros", lambda: load_stat_metrics("shots")),
    ("team_corners_display_correction", "córners", lambda: load_stat_metrics("corners")),
]


def build(write=True, csv_path=OUT_CSV, json_path=OUT_JSON, txt_path=OUT_TXT):
    rows = []
    mod_summaries = []
    for key, label, loader in MODULES:
        m = loader()
        if not m:
            row = {c: None for c in CSV_COLUMNS}
            row.update({"module": key, "n": 0, "readiness_status": "NO_DATA", "confidence": "baja",
                        "data_quality": "no_data", "anti_lookahead_available": False,
                        "reason": "sin datos de la evaluación shadow correspondiente."})
            rows.append(row)
            mod_summaries.append({"module": key, "label": label, "readiness_status": "NO_DATA", "n": 0})
            continue
        g = decide_readiness(m)
        status = g["readiness_status"]
        n = m.get("n") or 0
        bias_o, bias_c = m.get("original_bias"), m.get("corrected_bias")
        bias_red = (round(abs(bias_o) - abs(bias_c), 4)
                    if (bias_o is not None and bias_c is not None) else None)
        conf = "baja" if status.startswith("NOT_READY") or status == "WATCH" else "media"
        dq = ("evaluable" if g["anti_lookahead_available"] else "aggregate_only")
        row = {
            "module": key, "n": n,
            "rows_to_min_sample": max(0, N_MIN_ACTIVATE - n),
            "metric_original_mae": m.get("original_mae"),
            "metric_corrected_mae_pre_fixture": m.get("corrected_mae_pre"),
            "delta_mae_pre_fixture": m.get("delta_mae"),
            "delta_rmse_pre_fixture": m.get("delta_rmse"),
            "original_bias": bias_o, "corrected_bias_pre_fixture": bias_c, "bias_reduction": bias_red,
            "direction_stable": g["direction_stable"], "sample_gate": g["sample_gate"],
            "improvement_gate": g["improvement_gate"], "bias_gate": g["bias_gate"],
            "no_strong_bias_inversion_gate": g["no_strong_bias_inversion_gate"],
            "anti_lookahead_available": g["anti_lookahead_available"], "data_quality": dq,
            "confidence": conf, "readiness_status": status,
            "reason": _module_reason(status, m, g),
        }
        rows.append(row)
        mod_summaries.append({"module": key, "label": label, "readiness_status": status, "n": n,
                              "delta_mae_pre_fixture": m.get("delta_mae"),
                              "rows_to_min_sample": max(0, N_MIN_ACTIVATE - n),
                              "gates": {k: g[k] for k in ("sample_gate", "improvement_gate", "bias_gate",
                                        "no_strong_bias_inversion_gate", "anti_lookahead_available",
                                        "data_quality_ok")}})

    ready = [s["module"] for s in mod_summaries if s["readiness_status"] == "READY_FOR_PROPOSAL"]
    should_propose = len(ready) > 0
    # first candidate = best signal among modules whose ONLY blocker is sample/data (would be ready)
    near = [r for r in rows if r["readiness_status"] in ("NOT_READY_SAMPLE", "WATCH")
            and r.get("improvement_gate") and r.get("bias_gate")
            and r.get("no_strong_bias_inversion_gate") and r.get("anti_lookahead_available")]
    near.sort(key=lambda r: (r.get("delta_mae_pre_fixture") or 0), reverse=True)
    first_candidate = (ready[0] if ready else (near[0]["module"] if near else None))

    if should_propose:
        action = "preparar PROPUESTA de activación (fase posterior, 🔴 requiere aprobación de Jorge)."
    elif near:
        miss = min(r["rows_to_min_sample"] for r in near)
        action = (f"seguir SHADOW y esperar más muestra (~{miss} filas para n>= {N_MIN_ACTIVATE} en el "
                  f"candidato más cercano: {first_candidate}).")
    else:
        action = "seguir SHADOW; aún sin señal/ muestra suficiente en ningún módulo."

    # Fase 4P skeleton: report that the reversible display-correction config exists and is all-OFF
    # (read-only; this gate NEVER flips a flag).
    try:
        cfg_status = dlc.config_status(dlc.load_display_correction_config())
    except Exception:
        cfg_status = "all_disabled"

    summary = {
        "generated_at_utc": now_iso(),
        "modules": mod_summaries,
        "ready_modules": ready,
        "should_propose_activation_any": should_propose,
        "first_candidate": first_candidate,
        "action_recommended": action,
        "display_correction_config_status": cfg_status,
        "thresholds": {"n_min_activate": N_MIN_ACTIVATE, "delta_mae_material": DELTA_MAE_MATERIAL,
                       "min_corrected_rows": MIN_CORRECTED_ROWS},
        "note": "No activar nada en esta fase.",
    }
    if write:
        pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(csv_path, index=False)
        Path(json_path).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(txt_path).write_text(render_txt(summary, rows) + "\n", encoding="utf-8")
    return summary, rows


# ===================================================================== report
def _f(v, nd=2):
    return "—" if v is None else (f"{v:.{nd}f}" if isinstance(v, (int, float)) else str(v))


def render_txt(summary, rows):
    L = ["⚽ READINESS de correcciones de DISPLAY (SOT / tiros / córners) — SHADOW. "
         "Alerta interna; NO activa nada.", ""]
    L.append(f"should_propose_activation_any = {summary['should_propose_activation_any']}  "
             f"(módulos READY: {', '.join(summary['ready_modules']) or 'ninguno'})")
    L.append(f"primer candidato: {summary['first_candidate'] or '—'}")
    L.append("")
    L.append(f"  {'módulo':32} {'n':>3} {'falt':>4} {'ΔMAE_pf':>8} {'sesgo o->c':>14} {'estado':>22}")
    for r in rows:
        bo, bc = r.get("original_bias"), r.get("corrected_bias_pre_fixture")
        biaschg = f"{_f(bo)}->{_f(bc)}"
        L.append(f"  {r['module']:32} {r['n']:>3} {r.get('rows_to_min_sample','—'):>4} "
                 f"{_f(r.get('delta_mae_pre_fixture')):>8} {biaschg:>14} {r['readiness_status']:>22}")
    L.append("")
    L.append("PUERTAS por módulo (qué falla):")
    for r in rows:
        gates = {"sample": r.get("sample_gate"), "improve": r.get("improvement_gate"),
                 "bias": r.get("bias_gate"), "no_inv": r.get("no_strong_bias_inversion_gate"),
                 "anti_la": r.get("anti_lookahead_available"), "dq": r.get("data_quality") == "evaluable"}
        failed = [k for k, v in gates.items() if v is False]
        L.append(f"   {r['module']:32} -> {('todas OK' if not failed else 'falla: ' + ', '.join(failed))}")
        L.append(f"      {r.get('reason','')}")
    L.append("")
    L.append(f"acción recomendada: {summary['action_recommended']}")
    L.append(f"config de corrección de display (Fase 4P, esqueleto reversible): "
             f"{summary.get('display_correction_config_status', 'all_disabled')} "
             f"(flags OFF -> nada se aplica; activar es 🔴).")
    L.append("")
    L.append(">>> No activar nada en esta fase. La activación de cualquier corrección de display es 🔴 "
             "(propuesta primero, aprobación explícita de Jorge). Este gate NO toca pesos, ni "
             "lam_shot_on, ni el modelo de stats, ni predicción base, ni Telegram. Solo lectura/alerta.")
    L.append("")
    L.append(f"generated_at_utc: {summary['generated_at_utc']}")
    return "\n".join(L)


def main():
    summary, _rows = build()
    print(f"display-correction readiness: should_propose_activation_any="
          f"{summary['should_propose_activation_any']} | first_candidate={summary['first_candidate']}")
    for s in summary["modules"]:
        print(f"  {s['module']:32} n={s['n']:>3} -> {s['readiness_status']}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup display-correction readiness gate (shadow, Fase 4O).")
    ap.parse_args()
    sys.exit(main())
