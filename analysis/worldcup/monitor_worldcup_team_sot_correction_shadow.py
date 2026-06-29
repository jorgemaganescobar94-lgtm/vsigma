"""
WORLD CUP 2026 — TEAM SOT CORRECTION ACTIVATION MONITOR (Fase 4N). SHADOW · READ-ONLY · NO API · NO
scraping · NO web · NO market/odds/betting · NO fabrication · NO secrets · NO external sources. Pure
football. MONITOR ONLY — it NEVER activates anything: it reads the Fase-4M SOT level-correction
evaluation and decides, against conservative governance gates, whether the display correction *would*
qualify for activation. The correction itself stays SHADOW until an explicitly-approved later phase.

DECISION (should_activate_display_correction = True) requires ALL of:
  * n_team_rows >= N_MIN_ACTIVATE (50);
  * delta_mae_pre_fixture >= DELTA_MAE_MATERIAL (0.15)   [anti-look-ahead, on the corrected rows];
  * delta_rmse_pre_fixture > 0;
  * abs(pre_fixture_bias) < abs(original_bias)           [bias moves toward 0];
  * no strong bias inversion;
  * enough corrected rows (data quality).
pre_fixture (online) is decisive; the cumulative fit is ignored for activation (it is optimistic).

With the current state (n=38 < 50) this returns should_activate_display_correction=False even though the
pre_fixture signal is positive — exactly the conservative behaviour intended.

SOURCES (read-only): worldcup_team_sot_level_correction_summary.json (preferred); if absent it recomputes
in-memory from worldcup_team_sot_scorecard.csv via the Fase-4M evaluator (no writes there). The per-row
worldcup_team_sot_level_correction.csv is read for the corrected/kept counts cross-check.

OUTPUT (read-only; explicit git-add only):
  * worldcup_team_sot_correction_shadow_monitor.csv        (one row: metrics + gates + decision)
  * worldcup_team_sot_correction_shadow_monitor.json       (regenerable -> gitignored)
  * worldcup_team_sot_correction_shadow_monitor_report.txt (no betting language; regenerable -> gitignored)

Run:  python analysis/worldcup/monitor_worldcup_team_sot_correction_shadow.py
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
import evaluate_worldcup_team_sot_level_correction as lc  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SOT_SCORECARD = HERE / "worldcup_team_sot_scorecard.csv"
CORRECTION_CSV = HERE / "worldcup_team_sot_level_correction.csv"
CORRECTION_JSON = HERE / "worldcup_team_sot_level_correction_summary.json"
OUT_CSV = HERE / "worldcup_team_sot_correction_shadow_monitor.csv"
OUT_JSON = HERE / "worldcup_team_sot_correction_shadow_monitor.json"
OUT_TXT = HERE / "worldcup_team_sot_correction_shadow_monitor_report.txt"

N_MIN_ACTIVATE = lc.N_MIN_ACTIVATE
DELTA_MAE_MATERIAL = lc.DELTA_MAE_MATERIAL
MIN_CORRECTED_ROWS = 20      # data-quality floor: enough online-corrected rows to trust the signal

CSV_COLUMNS = ["n_team_rows", "n_fixtures", "original_mae", "original_rmse", "original_bias",
               "pre_fixture_mae", "pre_fixture_rmse", "pre_fixture_bias", "delta_mae_pre_fixture",
               "delta_rmse_pre_fixture", "bias_reduction", "n_corrected", "n_kept_original",
               "recommendation", "should_activate_display_correction"]


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ===================================================================== load metrics
def load_summary(json_path=CORRECTION_JSON, scorecard_path=SOT_SCORECARD):
    """Preferred: the Fase-4M summary JSON. Fallback: recompute in memory from the scorecard (no
    writes). Returns the summary dict, or a 0-row summary if neither source is usable."""
    p = Path(json_path)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    summary, _rows = lc.build(scorecard_path, write=False)
    return summary


def extract_metrics(summary):
    """Pull the headline numbers the monitor reports. pre_fixture_* use the on-corrected subset (the
    honest online comparison). Returns a flat dict; None where the summary lacks data."""
    n = summary.get("n_team_rows", 0)
    orig = summary.get("original", {}) or {}
    pf = (summary.get("anti_look_ahead", {}) or {}).get("pre_fixture", {}) or {}
    original_bias = orig.get("bias")
    pre_bias = pf.get("bias_corrected_on_corrected")
    bias_reduction = None
    if original_bias is not None and pre_bias is not None:
        bias_reduction = round(abs(original_bias) - abs(pre_bias), 4)
    return {
        "n_team_rows": n,
        "n_fixtures": summary.get("n_fixtures", 0),
        "original_mae": orig.get("mae"), "original_rmse": orig.get("rmse"), "original_bias": original_bias,
        "pre_fixture_mae": pf.get("mae_corrected_on_corrected"),
        "pre_fixture_rmse": pf.get("rmse_corrected_on_corrected"),
        "pre_fixture_bias": pre_bias,
        "delta_mae_pre_fixture": pf.get("delta_mae_on_corrected"),
        "delta_rmse_pre_fixture": pf.get("delta_rmse_on_corrected"),
        "bias_reduction": bias_reduction,
        "n_corrected": pf.get("n_corrected", 0),
        "n_kept_original": pf.get("n_kept_original", 0),
        "recommendation": summary.get("recommendation", "NO_CHANGE"),
    }


# ===================================================================== activation gate (pure)
def decide_activation(m):
    """Conservative governance gate. Returns (should_activate: bool, reason: str, gates: dict). pure."""
    n = m.get("n_team_rows") or 0
    d_mae = m.get("delta_mae_pre_fixture")
    d_rmse = m.get("delta_rmse_pre_fixture")
    bias_o = m.get("original_bias")
    bias_c = m.get("pre_fixture_bias")
    n_corr = m.get("n_corrected") or 0

    g_sample = n >= N_MIN_ACTIVATE
    g_mae = d_mae is not None and d_mae >= DELTA_MAE_MATERIAL
    g_rmse = d_rmse is not None and d_rmse > 0
    g_bias_better = (bias_o is not None and bias_c is not None and abs(bias_c) < abs(bias_o) - 1e-9)
    g_no_strong_inversion = not (bias_o is not None and bias_c is not None
                                 and (bias_c * bias_o < 0) and abs(bias_c) > 0.5 * abs(bias_o) + 1e-9)
    g_data_quality = n_corr >= MIN_CORRECTED_ROWS

    gates = {"sample_ge_min": bool(g_sample), "delta_mae_material": bool(g_mae),
             "delta_rmse_positive": bool(g_rmse), "bias_moves_to_zero": bool(g_bias_better),
             "no_strong_inversion": bool(g_no_strong_inversion), "data_quality_ok": bool(g_data_quality)}
    should = all(gates.values())

    if should:
        reason = (f"todas las puertas OK: n={n}>= {N_MIN_ACTIVATE}, ΔMAE {d_mae:+.2f} (>= "
                  f"{DELTA_MAE_MATERIAL}), ΔRMSE {d_rmse:+.2f}>0, sesgo {bias_o:+.2f}->{bias_c:+.2f} "
                  f"hacia 0, sin inversión fuerte, n_corregidas={n_corr}. Candidata a activación de "
                  f"display en una fase posterior (requiere aprobación explícita de Jorge).")
    else:
        failed = [k for k, v in gates.items() if not v]
        bits = []
        if not g_sample:
            bits.append(f"n={n} < {N_MIN_ACTIVATE}")
        if not g_mae:
            bits.append(f"ΔMAE {('%.2f' % d_mae) if d_mae is not None else 'n/a'} < {DELTA_MAE_MATERIAL}")
        if not g_rmse:
            bits.append("ΔRMSE no positivo")
        if not g_bias_better:
            bits.append("sesgo no se acerca a 0")
        if not g_no_strong_inversion:
            bits.append("inversión fuerte de sesgo")
        if not g_data_quality:
            bits.append(f"pocas filas corregidas ({n_corr} < {MIN_CORRECTED_ROWS})")
        reason = ("NO activar (señal puede ser positiva pero no cumple gobernanza): "
                  + "; ".join(bits) + ".")
    return should, reason, gates


# ===================================================================== build
def build(json_path=CORRECTION_JSON, scorecard_path=SOT_SCORECARD, correction_csv=CORRECTION_CSV,
          write=True, csv_path=OUT_CSV, out_json=OUT_JSON, txt_path=OUT_TXT):
    summary = load_summary(json_path, scorecard_path)
    m = extract_metrics(summary)
    should, reason, gates = decide_activation(m)

    # cross-check corrected/kept counts from the per-row CSV when present (read-only sanity)
    cc = {}
    p = Path(correction_csv)
    if p.exists():
        try:
            df = pd.read_csv(p)
            if "correction_mode" in df.columns:
                cc = {"csv_pre_fixture_applied": int((df["correction_mode"] == "pre_fixture_applied").sum()),
                      "csv_pre_fixture_kept_original": int((df["correction_mode"] == "pre_fixture_kept_original").sum())}
        except Exception:
            cc = {}

    out = {"generated_at_utc": now_iso(), **m,
           "should_activate_display_correction": should,
           "activation_gates": gates, "decision_reason": reason,
           "thresholds": {"n_min_activate": N_MIN_ACTIVATE, "delta_mae_material": DELTA_MAE_MATERIAL,
                          "min_corrected_rows": MIN_CORRECTED_ROWS},
           "cross_check": cc}

    if write:
        row = {c: out.get(c) for c in CSV_COLUMNS}
        pd.DataFrame([row], columns=CSV_COLUMNS).to_csv(csv_path, index=False)
        Path(out_json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(txt_path).write_text(render_txt(out) + "\n", encoding="utf-8")
    return out


# ===================================================================== report
def _f(v, nd=2):
    return "—" if v is None else f"{v:.{nd}f}"


def render_txt(out):
    L = ["⚽ Monitor de ACTIVACIÓN — corrección de nivel SOT de equipo (SHADOW). "
         "NO activa nada; solo evalúa puertas de gobernanza.", ""]
    if not out.get("n_team_rows"):
        L.append("Sin filas evaluables todavía -> should_activate_display_correction=False.")
        L.append("")
        L.append(f"generated_at_utc: {out['generated_at_utc']}")
        return "\n".join(L)
    L.append(f"n_team_rows={out['n_team_rows']} · n_fixtures={out['n_fixtures']}")
    L.append(f"original     : MAE {_f(out['original_mae'])} · RMSE {_f(out['original_rmse'])} · "
             f"sesgo {_f(out['original_bias'])}")
    L.append(f"pre_fixture  : MAE {_f(out['pre_fixture_mae'])} · RMSE {_f(out['pre_fixture_rmse'])} · "
             f"sesgo {_f(out['pre_fixture_bias'])}  (sobre {out['n_corrected']} filas corregidas; "
             f"{out['n_kept_original']} mantenidas)")
    L.append(f"delta        : ΔMAE {_f(out['delta_mae_pre_fixture'])} · ΔRMSE "
             f"{_f(out['delta_rmse_pre_fixture'])} · reducción |sesgo| {_f(out['bias_reduction'])}")
    L.append("")
    L.append("PUERTAS DE ACTIVACIÓN:")
    for k, v in out["activation_gates"].items():
        L.append(f"   [{'OK ' if v else 'NO '}] {k}")
    L.append("")
    L.append(f">>> should_activate_display_correction = {out['should_activate_display_correction']}")
    L.append(f"    {out['decision_reason']}")
    th = out["thresholds"]
    L.append(f"    umbrales: n>= {th['n_min_activate']} · ΔMAE>= {th['delta_mae_material']} · "
             f"filas corregidas>= {th['min_corrected_rows']}.")
    L.append("")
    L.append("Recordatorio de gobernanza: aunque todas las puertas pasen, la activación de la corrección "
             "de display es 🔴 (requiere aprobación explícita de Jorge en una fase posterior). Este "
             "monitor NO aplica nada: ni pesos, ni lam_shot_on, ni predicción base, ni Telegram.")
    L.append("")
    L.append(f"generated_at_utc: {out['generated_at_utc']}")
    return "\n".join(L)


def main(json_path=CORRECTION_JSON, scorecard_path=SOT_SCORECARD):
    out = build(json_path, scorecard_path)
    print(f"SOT activation monitor: n={out.get('n_team_rows')} ΔMAE_pre_fixture="
          f"{out.get('delta_mae_pre_fixture')} -> should_activate="
          f"{out.get('should_activate_display_correction')}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="World Cup team SOT correction activation monitor (shadow, Fase 4N).")
    ap.add_argument("--json", default=str(CORRECTION_JSON))
    ap.add_argument("--scorecard", default=str(SOT_SCORECARD))
    a = ap.parse_args()
    sys.exit(main(a.json, a.scorecard))
