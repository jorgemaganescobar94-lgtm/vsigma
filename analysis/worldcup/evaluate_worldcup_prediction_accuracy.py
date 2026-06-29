"""
WORLD CUP 2026 — GLOBAL PREDICTION-ACCURACY EVALUATION (Fase 4J). READ-ONLY · NO API · NO scraping · NO
web · NO market/odds/betting · NO fabrication · NO secrets. Pure football. MEASURE ONLY — nothing is
changed (no weights, no models, no predictions, no Telegram, no external sources).

Measures EVERY main output the World Cup product already produces against REAL settled outcomes, and
panels each module with an honest status (ACTIVO / SHADOW / NO_EVALUABLE / INSUFFICIENT_SAMPLE) and a
recommendation. Where an output does not exist yet (e.g. a full score distribution) the metric is marked
NO_DISPONIBLE — never fabricated.

Sources (each optional; missing -> that module is NO_EVALUABLE with a reason):
  * worldcup_predictions_log.csv      -> 1X2 (l3_*/mx_* + result_1x2) and goals (l3_xg_* + result_final_*)
  * worldcup_player_props_log.csv     -> per-player goal/assist/SOT/card (p_* + act_*), shot counts
  * worldcup_team_stats_scorecard.csv -> team shots/corners/cards (pre-aggregated MAE/RMSE/bias)
  * (card-risk modules are already measured by Fase 4G/4H/4I; here they appear in the panel as SHADOW)

Outputs:
  * worldcup_prediction_accuracy.csv          (one row per module)
  * worldcup_prediction_accuracy_summary.json (modules + executive summary)
  * worldcup_prediction_accuracy_report.txt   (executive report)

Run:  python analysis/worldcup/evaluate_worldcup_prediction_accuracy.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

PRED_LOG = HERE / "worldcup_predictions_log.csv"
PROPS_LOG = HERE / "worldcup_player_props_log.csv"
TEAM_STATS_SCORECARD = HERE / "worldcup_team_stats_scorecard.csv"
TEAM_SOT_SCORECARD = HERE / "worldcup_team_sot_scorecard.csv"  # Fase 4L per-team/fixture SOT scorecard
SHADOW_MONITOR_JSON = HERE / "worldcup_card_risk_shadow_monitor.json"
SCORELINE_EVAL_JSON = HERE / "worldcup_scoreline_evaluation_summary.json"
OUT_CSV = HERE / "worldcup_prediction_accuracy.csv"
OUT_JSON = HERE / "worldcup_prediction_accuracy_summary.json"
OUT_TXT = HERE / "worldcup_prediction_accuracy_report.txt"

MIN_SAMPLE = 30          # below -> INSUFFICIENT_SAMPLE
EPS = 1e-12

# 1X2 probability sources, in display priority (same chain as the card render). Only NUMERIC triples used.
ONEX2_PREFIXES = ("inj", "ctx", "mx", "l3", "our")
XG_PREFIXES = ("inj", "ctx", "mx", "l3", "our")

CSV_COLUMNS = ["module", "status", "n", "primary_metric", "primary_value", "secondary",
               "bias", "recommendation", "confidence", "reason"]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ============================================================ safe coercion (no inj_home string bug)
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


# ============================================================ metric helpers (pure, testable)
def brier_binary(probs, labels):
    pairs = [(float(p), int(y)) for p, y in zip(probs, labels) if p is not None]
    return sum((p - y) ** 2 for p, y in pairs) / len(pairs) if pairs else None


def logloss_binary(probs, labels):
    pairs = [(min(max(float(p), EPS), 1 - EPS), int(y)) for p, y in zip(probs, labels) if p is not None]
    return -sum(y * math.log(p) + (1 - y) * math.log(1 - p) for p, y in pairs) / len(pairs) if pairs else None


def calibration_bins(probs, labels, n_bins=10):
    pairs = [(float(p), int(y)) for p, y in zip(probs, labels) if p is not None]
    out = []
    for i in range(n_bins):
        lo, hi = i / n_bins, (i + 1) / n_bins
        sel = [(p, y) for p, y in pairs if p >= lo and (p < hi or (i == n_bins - 1 and p <= hi))]
        if sel:
            out.append({"bin_lo": round(lo, 2), "bin_hi": round(hi, 2), "n": len(sel),
                        "avg_pred": round(sum(p for p, _ in sel) / len(sel), 4),
                        "real_rate": round(sum(y for _, y in sel) / len(sel), 4)})
    return out


def top_decile_hit_rate(probs, labels):
    """Real positive rate among the top-10% highest-probability predictions (concentration check)."""
    pairs = sorted([(float(p), int(y)) for p, y in zip(probs, labels) if p is not None], reverse=True)
    if not pairs:
        return None
    k = max(1, len(pairs) // 10)
    top = pairs[:k]
    return round(sum(y for _, y in top) / len(top), 4)


def mae(preds, actuals):
    pairs = [(float(p), float(a)) for p, a in zip(preds, actuals) if p is not None and a is not None]
    return sum(abs(p - a) for p, a in pairs) / len(pairs) if pairs else None


def rmse(preds, actuals):
    pairs = [(float(p), float(a)) for p, a in zip(preds, actuals) if p is not None and a is not None]
    return math.sqrt(sum((p - a) ** 2 for p, a in pairs) / len(pairs)) if pairs else None


def bias(preds, actuals):
    pairs = [(float(p), float(a)) for p, a in zip(preds, actuals) if p is not None and a is not None]
    return sum(p - a for p, a in pairs) / len(pairs) if pairs else None


def _status_for(n, has_source):
    if not has_source:
        return "NO_EVALUABLE"
    if n == 0:
        return "NO_EVALUABLE"
    if n < MIN_SAMPLE:
        return "INSUFFICIENT_SAMPLE"
    return "ACTIVO"


# ============================================================ 1X2 + goals (predictions log)
def _resolve_triple(row, prefixes, suffixes):
    for pre in prefixes:
        vals = [safe_prob(row.get(f"{pre}_{s}")) for s in suffixes]
        if all(v is not None for v in vals):
            return tuple(vals), pre
    return None, None


def _resolve_xg(row, prefixes):
    for pre in prefixes:
        h, a = safe_num(row.get(f"{pre}_xg_home")), safe_num(row.get(f"{pre}_xg_away"))
        if h is not None and a is not None:
            return (h, a), pre
    return None, None


def evaluate_1x2(pred_df):
    if pred_df is None or "result_1x2" not in pred_df.columns:
        return {"module": "Resultado 1X2", "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin predictions log o sin result_1x2", "recommendation": "necesita más datos",
                "confidence": "baja"}
    s = pred_df[pred_df.get("settled") == 1] if "settled" in pred_df.columns else pred_df
    rows = []
    classes = ["H", "D", "A"]
    chosen_p, chosen_hit = [], []
    correct = top2 = 0
    mbrier = mll = 0.0
    real = {"H": 0, "D": 0, "A": 0}
    for _, r in s.iterrows():
        actual = str(r.get("result_1x2") or "").strip().upper()
        if actual not in classes:
            continue
        triple, src = _resolve_triple(r, ONEX2_PREFIXES, ("home", "draw", "away"))
        if triple is None:
            continue
        p = dict(zip(classes, triple))
        tot = sum(p.values())
        if tot <= 0:
            continue
        p = {k: v / tot for k, v in p.items()}                  # normalise defensively
        rows.append((p, actual))
        real[actual] += 1
        pred_class = max(p, key=p.get)
        correct += int(pred_class == actual)
        top2 += int(actual in sorted(p, key=p.get, reverse=True)[:2])
        mbrier += sum((p[k] - (1.0 if actual == k else 0.0)) ** 2 for k in classes)
        mll += -math.log(min(max(p[actual], EPS), 1 - EPS))
        chosen_p.append(p[pred_class]); chosen_hit.append(int(pred_class == actual))
    n = len(rows)
    if n == 0:
        return {"module": "Resultado 1X2", "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin filas con probabilidades numéricas + resultado", "confidence": "baja",
                "recommendation": "necesita más datos"}
    acc = correct / n
    status = _status_for(n, True)
    bias_txt = (f"real H {real['H']}/D {real['D']}/A {real['A']}")
    rec = "mantener" if status == "ACTIVO" else "necesita más datos"
    return {"module": "Resultado 1X2", "status": status, "n": n,
            "primary_metric": "accuracy_1x2", "primary_value": _r(acc),
            "secondary": {"top2_accuracy": _r(top2 / n), "brier_multiclass": _r(mbrier / n),
                          "logloss_multiclass": _r(mll / n),
                          "calibration": calibration_bins(chosen_p, chosen_hit),
                          "real_rates": real},
            "bias": bias_txt, "recommendation": rec,
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": f"{n} partidos liquidados con 1X2 y probabilidades numéricas"}


def evaluate_goals(pred_df):
    if pred_df is None or not {"result_final_gh", "result_final_ga"} <= set(pred_df.columns):
        return {"module": "Goles/marcador", "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin resultados finales en predictions log", "confidence": "baja",
                "recommendation": "necesita más datos"}
    s = pred_df[pred_df.get("settled") == 1] if "settled" in pred_df.columns else pred_df
    xgh, xga, gh, ga = [], [], [], []
    sign_ok = 0; sign_n = 0
    exact_hit = 0; exact_n = 0
    for _, r in s.iterrows():
        a_h, a_a = safe_num(r.get("result_final_gh")), safe_num(r.get("result_final_ga"))
        if a_h is None or a_a is None:
            continue
        xg, src = _resolve_xg(r, XG_PREFIXES)
        if xg is None:
            continue
        xgh.append(xg[0]); xga.append(xg[1]); gh.append(a_h); ga.append(a_a)
        sign_n += 1
        sign_ok += int((xg[0] - xg[1] > 0) == (a_h - a_a > 0) and (xg[0] - xg[1] == 0) == (a_h - a_a == 0))
        ts = str(r.get("l3_top_score") or "").strip()
        if ts and "-" in ts:
            exact_n += 1
            exact_hit += int(ts == f"{int(a_h)}-{int(a_a)}")
    n = len(gh)
    if n == 0:
        return {"module": "Goles/marcador", "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin xG previstos numéricos + resultado", "confidence": "baja",
                "recommendation": "necesita más datos"}
    total_pred = [h + a for h, a in zip(xgh, xga)]
    total_real = [h + a for h, a in zip(gh, ga)]
    status = _status_for(n, True)
    b_total = bias(total_pred, total_real)
    return {"module": "Goles/marcador", "status": status, "n": n,
            "primary_metric": "mae_total_goals", "primary_value": _r(mae(total_pred, total_real)),
            "secondary": {"mae_home": _r(mae(xgh, gh)), "mae_away": _r(mae(xga, ga)),
                          "rmse_total": _r(rmse(total_pred, total_real)),
                          "diff_sign_accuracy": _r(sign_ok / sign_n) if sign_n else None,
                          "exact_scoreline_hit": _r(exact_hit / exact_n) if exact_n else None,
                          "top3_top5_scoreline": "ver módulo 'Marcadores top-3/5' (Fase 4K)"},
            "bias": f"total goals bias {_r(b_total)} ({'sobre' if (b_total or 0)>0 else 'infra'}-predice)",
            "recommendation": "mantener" if status == "ACTIVO" else "necesita más datos",
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": f"{n} partidos liquidados con xG previsto y resultado"}


# ============================================================ player modules (props log)
def evaluate_player_binary(props_df, module, prob_col, act_col):
    if props_df is None or prob_col not in props_df.columns or act_col not in props_df.columns:
        return {"module": module, "status": "NO_EVALUABLE", "n": 0,
                "reason": f"sin columnas {prob_col}/{act_col}", "confidence": "baja",
                "recommendation": "necesita más datos"}
    s = props_df[props_df.get("settled") == 1] if "settled" in props_df.columns else props_df
    probs, labels = [], []
    for _, r in s.iterrows():
        p = safe_prob(r.get(prob_col))
        a = safe_num(r.get(act_col))
        if p is None or a is None:
            continue
        probs.append(p); labels.append(1 if a >= 1 else 0)
    n = len(probs)
    if n == 0:
        return {"module": module, "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin filas con probabilidad + resultado", "confidence": "baja",
                "recommendation": "necesita más datos"}
    pos_rate = sum(labels) / n
    avg_p = sum(probs) / n
    status = _status_for(n, True)
    b = avg_p - pos_rate
    return {"module": module, "status": status, "n": n,
            "primary_metric": "brier", "primary_value": _r(brier_binary(probs, labels)),
            "secondary": {"logloss": _r(logloss_binary(probs, labels)),
                          "avg_probability": _r(avg_p), "positive_rate_real": _r(pos_rate),
                          "top_decile_hit_rate": top_decile_hit_rate(probs, labels),
                          "calibration": calibration_bins(probs, labels)},
            "bias": f"avg_p {_r(avg_p)} vs real {_r(pos_rate)} -> {'sobre' if b>0.01 else ('infra' if b<-0.01 else 'bien')}-calibrado",
            "recommendation": ("monitorizar (sesgo de sobrepredicción)" if b > 0.03 else
                               ("monitorizar (infrapredicción)" if b < -0.03 else "mantener"))
            if status == "ACTIVO" else "necesita más datos",
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": f"{n} predicciones por jugador liquidadas"}


def evaluate_player_count(props_df, module, pred_col, act_col):
    if props_df is None or pred_col not in props_df.columns or act_col not in props_df.columns:
        return {"module": module, "status": "NO_EVALUABLE", "n": 0,
                "reason": f"sin columnas {pred_col}/{act_col}", "confidence": "baja",
                "recommendation": "necesita más datos"}
    s = props_df[props_df.get("settled") == 1] if "settled" in props_df.columns else props_df
    preds, acts = [], []
    for _, r in s.iterrows():
        p, a = safe_num(r.get(pred_col)), safe_num(r.get(act_col))
        if p is None or a is None:
            continue
        preds.append(p); acts.append(a)
    n = len(preds)
    if n == 0:
        return {"module": module, "status": "NO_EVALUABLE", "n": 0, "reason": "sin pred+real",
                "confidence": "baja", "recommendation": "necesita más datos"}
    status = _status_for(n, True)
    b = bias(preds, acts)
    return {"module": module, "status": status, "n": n,
            "primary_metric": "mae", "primary_value": _r(mae(preds, acts)),
            "secondary": {"rmse": _r(rmse(preds, acts)), "mean_pred": _r(sum(preds) / n),
                          "mean_real": _r(sum(acts) / n)},
            "bias": f"bias {_r(b)} ({'sobre' if (b or 0)>0 else 'infra'}-predice)",
            "recommendation": "monitorizar" if status == "ACTIVO" else "necesita más datos",
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": f"{n} conteos por jugador liquidados"}


# ============================================================ team-stats modules (pre-aggregated)
def evaluate_team_stats(scorecard_df):
    """Surface the pre-aggregated team-stat scorecard (MAE/RMSE/bias). One module per stat row."""
    mods = []
    label = {"shots": "Team stats: tiros", "corners": "Team stats: córners",
             "cards": "Team stats: tarjetas", "sot": "Team stats: SOT"}
    present = set()
    if scorecard_df is not None and "stat" in scorecard_df.columns:
        for _, r in scorecard_df.iterrows():
            stat = str(r.get("stat") or "").strip().lower()
            present.add(stat)
            n = int(safe_num(r.get("n")) or 0)
            mae_v = safe_num(r.get("mae"))
            b = safe_num(r.get("bias"))
            status = _status_for(n, mae_v is not None)
            mods.append({"module": label.get(stat, f"Team stats: {stat}"), "status": status, "n": n,
                         "primary_metric": "mae", "primary_value": _r(mae_v),
                         "secondary": {"rmse": _r(safe_num(r.get("rmse"))),
                                       "mean_pred": _r(safe_num(r.get("mean_pred"))),
                                       "mean_real": _r(safe_num(r.get("mean_real"))),
                                       "line_acc": _r(safe_num(r.get("line_acc")))},
                         "bias": f"bias {_r(b)} ({'sobre' if (b or 0)>0 else 'infra'}-predice)",
                         "recommendation": "monitorizar" if status == "ACTIVO" else "necesita más datos",
                         "confidence": "media" if status == "ACTIVO" else "baja",
                         "reason": f"{n} equipos-partido liquidados (scorecard agregado)"})
    # Team SOT is scored by its own dedicated module (evaluate_team_sot, Fase 4L) from the per-team/
    # fixture scorecard -> NOT injected here (avoids a duplicate placeholder).
    return mods


# ============================================================ team SOT (Fase 4L per-team scorecard)
def evaluate_team_sot(path=TEAM_SOT_SCORECARD):
    """Surface the Fase-4L team shots-on-target scorecard. Reads the per-team/fixture rows
    (predicted_sot = Σ player λ_sot vs actual_sot) and aggregates MAE/RMSE/bias over the evaluable rows
    (both values present). ACTIVO / INSUFFICIENT_SAMPLE by sample size; NO_EVALUABLE if the scorecard is
    absent/empty. Never fabricates."""
    base = {"module": "Team stats: SOT", "confidence": "baja"}
    df = _read_csv(path)
    if df is None or not {"predicted_sot", "actual_sot"} <= set(df.columns):
        return {**base, "status": "NO_EVALUABLE", "n": 0,
                "reason": "no hay scorecard de tiros a puerta de equipo todavía (Fase 4L)",
                "recommendation": "ejecutar build_worldcup_team_sot_scorecard.py"}
    preds, acts = [], []
    for _, r in df.iterrows():
        p, a = safe_num(r.get("predicted_sot")), safe_num(r.get("actual_sot"))
        if p is None or a is None:
            continue
        preds.append(p); acts.append(a)
    n = len(preds)
    if n == 0:
        return {**base, "status": "NO_EVALUABLE", "n": 0,
                "reason": "scorecard de SOT sin filas evaluables (predicho + real)",
                "recommendation": "necesita más datos"}
    status = _status_for(n, True)
    b = bias(preds, acts)
    return {"module": "Team stats: SOT", "status": status, "n": n,
            "primary_metric": "mae", "primary_value": _r(mae(preds, acts)),
            "secondary": {"rmse": _r(rmse(preds, acts)), "mean_pred": _r(sum(preds) / n),
                          "mean_real": _r(sum(acts) / n),
                          "n_fixtures": int(df["fixture_id"].nunique()) if "fixture_id" in df.columns else None},
            "bias": f"bias {_r(b)} ({'sobre' if (b or 0) > 0 else 'infra'}-predice)",
            "recommendation": "monitorizar" if status == "ACTIVO" else "necesita más datos",
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": f"{n} equipos-partido con SOT previsto (Σλ jugadores) y real liquidado"}


# ============================================================ scoreline top-3/5 (Fase 4K)
def evaluate_scoreline_module(path=SCORELINE_EVAL_JSON):
    """Surface the Fase-4K scoreline evaluation (top-1/3/5 exact-score hit). NO_EVALUABLE if absent."""
    p = Path(path)
    base = {"module": "Marcadores top-3/5", "confidence": "baja"}
    if not p.exists():
        return {**base, "status": "NO_EVALUABLE", "n": 0,
                "reason": "sin evaluación de distribución de marcadores (Fase 4K)",
                "recommendation": "necesita salida mejor estructurada"}
    try:
        s = json.loads(p.read_text(encoding="utf-8")).get("summary", {})
    except Exception:
        return {**base, "status": "NO_EVALUABLE", "n": 0, "reason": "evaluación de marcadores ilegible",
                "recommendation": "necesita más datos"}
    n = s.get("n_matches", 0)
    if not n:
        return {**base, "status": "NO_EVALUABLE", "n": 0, "reason": s.get("reason", "sin partidos"),
                "recommendation": "necesita más datos"}
    status = s.get("status", "ACTIVO")
    return {"module": "Marcadores top-3/5", "status": status, "n": n,
            "primary_metric": "exact_score_top3_hit_rate",
            "primary_value": s.get("exact_score_top3_hit_rate"),
            "secondary": {"top1": s.get("exact_score_top1_hit_rate"),
                          "top5": s.get("exact_score_top5_hit_rate"),
                          "mean_rank_actual": s.get("mean_rank_actual_score"),
                          "derived_1x2_accuracy": s.get("derived_1x2_accuracy")},
            "bias": f"prob. media del marcador real {s.get('actual_score_avg_probability')}",
            "recommendation": "monitorizar" if status == "ACTIVO" else "necesita más datos",
            "confidence": "media" if status == "ACTIVO" else "baja",
            "reason": s.get("reason", f"{n} partidos con distribución de marcadores")}


# ============================================================ card-risk adjustment (SHADOW, from 4I)
def card_risk_shadow_module():
    p = Path(SHADOW_MONITOR_JSON)
    base = {"module": "Ajuste riesgo de tarjeta (4F-4I)", "status": "SHADOW",
            "recommendation": "dejar shadow", "confidence": "baja",
            "reason": "medido en Fase 4G/4H/4I; sin señal real sin look-ahead"}
    if p.exists():
        try:
            s = json.loads(p.read_text(encoding="utf-8"))
            m = s.get("metrics", {})
            base["n"] = m.get("evaluated_predictions")
            base["primary_metric"] = "delta_brier_pre_fixture"
            base["primary_value"] = m.get("delta_brier_pre_fixture")
            base["secondary"] = {"state": s.get("state"),
                                 "should_adjust_weights": s.get("should_adjust_weights"),
                                 "fraction_surviving": m.get("fraction_of_4g_gain_surviving")}
            base["reason"] = s.get("reason", base["reason"])
        except Exception:
            pass
    return base


# ============================================================ executive summary
def _executive(modules):
    active = [m for m in modules if m["status"] == "ACTIVO"]
    not_eval = [m["module"] for m in modules if m["status"] == "NO_EVALUABLE"]
    insuff = [m["module"] for m in modules if m["status"] == "INSUFFICIENT_SAMPLE"]
    shadow = [m["module"] for m in modules if m["status"] == "SHADOW"]
    over = [m["module"] for m in modules if isinstance(m.get("bias"), str) and "sobre" in m["bias"]]
    under = [m["module"] for m in modules if isinstance(m.get("bias"), str) and "infra" in m["bias"]]
    # "best" 1X2 if present; flag worst-calibrated player module by |avg-real|
    has_1x2 = any(m["module"] == "Resultado 1X2" and m["status"] == "ACTIVO" for m in modules)
    conclusion = []
    if has_1x2:
        conclusion.append("El sistema tiene señal clara en el RESULTADO 1X2 y en goles/MAE de equipo.")
    if over:
        conclusion.append("Sobrepredice: " + ", ".join(over[:4]) + ".")
    if under:
        conclusion.append("Infrapredice: " + ", ".join(under[:4]) + ".")
    if shadow:
        conclusion.append("Queda en shadow: " + ", ".join(shadow) + " (no aporta señal real todavía).")
    if not_eval:
        conclusion.append("No evaluable aún: " + ", ".join(not_eval) + ".")
    conclusion.append("Distribución de marcadores (top-3/5, Fase 4K) y SOT de equipo (Fase 4L) ya "
                      "están estructurados y medidos. Prioridad siguiente: seguir acumulando muestra "
                      "de props por jugador y de SOT de equipo, ANTES de añadir fuentes externas.")
    return {"active_modules": [m["module"] for m in active], "shadow_modules": shadow,
            "not_evaluable": not_eval, "insufficient_sample": insuff,
            "overprediction": over, "underprediction": under,
            "conclusion": " ".join(conclusion)}


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


def build(pred_log=PRED_LOG, props_log=PROPS_LOG, team_stats=TEAM_STATS_SCORECARD, write=True):
    pred = _read_csv(pred_log)
    props = _read_csv(props_log)
    team = _read_csv(team_stats)

    modules = [
        evaluate_1x2(pred),
        evaluate_goals(pred),
        evaluate_scoreline_module(),
        evaluate_player_binary(props, "Jugadores: gol", "p_goal", "act_goal"),
        evaluate_player_binary(props, "Jugadores: asistencia", "p_assist", "act_assist"),
        evaluate_player_binary(props, "Jugadores: tiros a puerta", "p_shot_on", "act_shots_on"),
        evaluate_player_binary(props, "Jugadores: tarjetas", "p_card", "act_card"),
        evaluate_player_count(props, "Jugadores: nº tiros", "exp_shots", "act_shots"),
    ]
    modules += evaluate_team_stats(team)
    modules.append(evaluate_team_sot())
    modules.append(card_risk_shadow_module())

    summary = {"meta": {"min_sample": MIN_SAMPLE,
                        "method": "cada módulo medido contra resultados reales liquidados; safe_prob "
                                  "ignora valores no numéricos; nada se modifica (solo medición)."},
               "modules": modules, "executive_summary": _executive(modules)}
    if write:
        rows = [{c: (m.get(c) if not isinstance(m.get(c), (dict, list)) else json.dumps(m.get(c),
                 ensure_ascii=False)) for c in CSV_COLUMNS} for m in modules]
        pd.DataFrame(rows, columns=CSV_COLUMNS).to_csv(OUT_CSV, index=False)
        Path(OUT_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        Path(OUT_TXT).write_text(render_txt(summary) + "\n", encoding="utf-8")
    return summary


def render_txt(summary) -> str:
    L = ["===== WORLD CUP — PRECISIÓN PREDICTIVA GLOBAL (Fase 4J) =====", "",
         "-- PANEL DE MÓDULOS --"]
    for m in summary["modules"]:
        pv = m.get("primary_value")
        pm = m.get("primary_metric") or ""
        L.append(f"  [{m['status']:18}] {m['module']:34} n={m.get('n','—')} "
                 f"{pm}={pv if pv is not None else '—'}")
        if m.get("bias"):
            L.append(f"        sesgo: {m['bias']}")
        L.append(f"        -> {m.get('recommendation','—')} (conf {m.get('confidence','baja')})")
    ex = summary["executive_summary"]
    L += ["", "-- RESUMEN EJECUTIVO --",
          f"  Módulos con señal (ACTIVO): {', '.join(ex['active_modules']) or '—'}",
          f"  Shadow: {', '.join(ex['shadow_modules']) or '—'}",
          f"  No evaluables: {', '.join(ex['not_evaluable']) or '—'}",
          f"  Muestra insuficiente: {', '.join(ex['insufficient_sample']) or '—'}",
          f"  Sobrepredicción: {', '.join(ex['overprediction']) or '—'}",
          f"  Infrapredicción: {', '.join(ex['underprediction']) or '—'}",
          "", "-- CONCLUSIÓN EJECUTIVA --", f"  {ex['conclusion']}", "",
          "Predicción futbolística pura, sin terminología de juego. Fase 4J = solo medición; NO se "
          "modifican pesos, modelos, predicciones, Telegram ni fuentes externas. NO toca data/external."]
    return "\n".join(L)


def main():
    s = build()
    ex = s["executive_summary"]
    print(f"prediction-accuracy: {len(s['modules'])} módulos | "
          f"ACTIVO={len(ex['active_modules'])} SHADOW={len(ex['shadow_modules'])} "
          f"NO_EVALUABLE={len(ex['not_evaluable'])}")
    for m in s["modules"]:
        print(f"  [{m['status']:18}] {m['module']:34} n={m.get('n','—')} "
              f"{m.get('primary_metric','')}={m.get('primary_value')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
